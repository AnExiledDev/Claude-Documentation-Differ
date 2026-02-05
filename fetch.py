#!/usr/bin/env python3
"""Fetch Claude Code documentation and track changes.

Usage:
    python3 fetch.py                    # Fetch latest docs
    python3 fetch.py --check            # Check for changes without saving
    python3 fetch.py --changelog        # Fetch and generate changelog if changed
    python3 fetch.py --force            # Fetch even if recently run
"""

from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lib.fetcher import fetch_all_pages, FetchSummary

_SCRIPT_DIR = Path(__file__).resolve().parent
_DOCS_DIR = _SCRIPT_DIR / "docs"
_EN_DIR = _DOCS_DIR / "en"
_METADATA_FILE = _DOCS_DIR / "metadata.json"


def _print_progress(current: int, total: int, message: str) -> None:
    """Print progress to stdout."""
    if total > 0:
        print(f"  [{current}/{total}] {message}")
    else:
        print(f"  {message}")


def _load_metadata() -> dict:
    """Load metadata from docs/metadata.json."""
    if _METADATA_FILE.exists():
        return json.loads(_METADATA_FILE.read_text())
    return {}


def _save_metadata(data: dict) -> None:
    """Save metadata to docs/metadata.json."""
    _METADATA_FILE.write_text(json.dumps(data, indent=2))


def _git_has_changes() -> bool:
    """Check if there are uncommitted changes in docs/."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(_DOCS_DIR),
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def _git_commit(message: str) -> bool:
    """Commit all changes in docs/."""
    try:
        # Add all changes
        subprocess.run(
            ["git", "add", "-A"],
            cwd=str(_DOCS_DIR),
            check=True,
            capture_output=True,
        )

        # Check if there's anything to commit
        result = subprocess.run(
            ["git", "diff", "--staged", "--quiet"],
            cwd=str(_DOCS_DIR),
        )

        if result.returncode == 0:
            # No changes to commit
            return False

        # Commit
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=str(_DOCS_DIR),
            check=True,
            capture_output=True,
        )
        return True

    except subprocess.CalledProcessError as e:
        print(
            f"  Git error: {e.stderr if hasattr(e, 'stderr') else e}", file=sys.stderr
        )
        return False


def _run_changelog() -> None:
    """Run diff.py --changelog to generate a changelog."""
    diff_script = _SCRIPT_DIR / "diff.py"
    if diff_script.exists():
        print("\nGenerating changelog...")
        subprocess.run(
            [sys.executable, str(diff_script), "--changelog"],
            cwd=str(_SCRIPT_DIR),
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch Claude Code documentation and track changes."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Dry run - fetch and show what would change without saving",
    )
    parser.add_argument(
        "--changelog",
        action="store_true",
        help="Generate changelog after fetching if changes detected",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Fetch even if recently run",
    )
    parser.add_argument(
        "--rate-limit",
        type=float,
        default=1.0,
        help="Seconds between requests (default: 1.0)",
    )
    args = parser.parse_args()

    # Ensure output directory exists
    _EN_DIR.mkdir(parents=True, exist_ok=True)

    # Check last run time
    metadata = _load_metadata()
    last_run = metadata.get("last_run")

    if last_run and not args.force and not args.check:
        last_dt = datetime.fromisoformat(last_run)
        now = datetime.now(timezone.utc)
        hours_since = (now - last_dt).total_seconds() / 3600

        if hours_since < 1:
            print(
                f"Last run was {hours_since:.1f} hours ago. Use --force to run anyway."
            )
            return

    print("Fetching Claude Code documentation...")
    print(f"  Output: {_EN_DIR}")
    print(f"  Mode: {'dry run' if args.check else 'write'}")
    print()

    # Run the async fetch
    summary: FetchSummary = asyncio.run(
        fetch_all_pages(
            output_dir=_EN_DIR,
            rate_limit=args.rate_limit,
            progress_callback=_print_progress,
            dry_run=args.check,
        )
    )

    print()
    print(f"Fetch complete:")
    print(f"  Total pages: {summary.total_pages}")
    print(f"  Successful:  {summary.successful}")
    print(f"  Failed:      {summary.failed}")

    # Report failures
    if summary.failed > 0:
        print("\nFailed pages:")
        for result in summary.results:
            if not result.success:
                print(f"  - {result.filename}: {result.error}")

    # If dry run, just report what would happen
    if args.check:
        print("\n[Dry run - no files written]")
        return

    # Update metadata
    metadata["last_run"] = datetime.now(timezone.utc).isoformat()
    metadata["total_pages"] = summary.total_pages
    metadata["successful"] = summary.successful
    metadata["failed"] = summary.failed
    _save_metadata(metadata)

    # Check for changes and commit
    if _git_has_changes():
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        commit_msg = f"Docs update: {timestamp}"

        print(f"\nChanges detected, committing...")
        if _git_commit(commit_msg):
            print(f"  Committed: {commit_msg}")

            # Generate changelog if requested
            if args.changelog:
                _run_changelog()
        else:
            print("  No changes to commit (files unchanged)")
    else:
        print("\nNo changes detected")


if __name__ == "__main__":
    main()
