#!/usr/bin/env python3
"""Fetch Claude Code documentation and track changes.

Usage:
    python3 fetch.py                    # Fetch latest docs
    python3 fetch.py --check            # Check for changes without saving
    python3 fetch.py --force            # Fetch even if recently run

Note: This script only fetches documentation. Git commits and changelog
generation are handled by the GitHub Actions workflow.
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

    # Report if changes were detected (commit is handled by workflow)
    if _git_has_changes():
        print("\nChanges detected in docs/ (ready for commit)")
    else:
        print("\nNo changes detected")


if __name__ == "__main__":
    main()
