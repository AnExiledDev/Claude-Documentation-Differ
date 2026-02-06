#!/usr/bin/env python3
"""Fetch documentation from configured sources and track changes.

Usage:
    python3 fetch.py                          # Fetch all sources
    python3 fetch.py --source claude-code     # Fetch Claude Code docs only
    python3 fetch.py --source api             # Fetch Claude API docs only
    python3 fetch.py --check                  # Dry run
    python3 fetch.py --force                  # Fetch even if recently run

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
from sources import get_source, get_all_sources, Source

_SCRIPT_DIR = Path(__file__).resolve().parent
_DOCS_DIR = _SCRIPT_DIR / "docs"


def _print_progress(current: int, total: int, message: str) -> None:
    """Print progress to stdout."""
    if total > 0:
        print(f"  [{current}/{total}] {message}")
    else:
        print(f"  {message}")


def _get_source_dirs(source: Source) -> tuple[Path, Path, Path]:
    """Get directories for a source.

    Returns:
        (source_dir, en_dir, metadata_file)
    """
    source_dir = _DOCS_DIR / source.docs_dir
    en_dir = source_dir / "en"
    metadata_file = source_dir / "metadata.json"
    return source_dir, en_dir, metadata_file


def _load_metadata(source: Source) -> dict:
    """Load metadata for a source."""
    _, _, metadata_file = _get_source_dirs(source)
    if metadata_file.exists():
        return json.loads(metadata_file.read_text())
    return {}


def _save_metadata(source: Source, data: dict) -> None:
    """Save metadata for a source."""
    source_dir, _, metadata_file = _get_source_dirs(source)
    source_dir.mkdir(parents=True, exist_ok=True)
    metadata_file.write_text(json.dumps(data, indent=2))


def _git_has_changes(source: Source) -> bool:
    """Check if there are uncommitted changes in the source's docs."""
    source_dir, _, _ = _get_source_dirs(source)
    result = subprocess.run(
        ["git", "status", "--porcelain", str(source_dir)],
        cwd=str(_SCRIPT_DIR),
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def _fetch_source(
    source: Source,
    force: bool = False,
    check: bool = False,
    rate_limit: float = 1.0,
) -> bool:
    """Fetch a single source.

    Returns:
        True if changes were detected, False otherwise.
    """
    source_dir, en_dir, _ = _get_source_dirs(source)

    # Ensure output directory exists
    source_dir.mkdir(parents=True, exist_ok=True)

    # Check last run time
    metadata = _load_metadata(source)
    last_run = metadata.get("last_run")

    if last_run and not force and not check:
        last_dt = datetime.fromisoformat(last_run)
        now = datetime.now(timezone.utc)
        hours_since = (now - last_dt).total_seconds() / 3600

        if hours_since < 1:
            print(
                f"Last run was {hours_since:.1f} hours ago. Use --force to run anyway."
            )
            return False

    print(f"Fetching {source.name} documentation...")
    print(f"  Source: {source.index_url}")
    print(f"  Output: {source_dir}")
    print(f"  Mode: {'dry run' if check else 'write'}")
    print()

    # Run the async fetch
    summary: FetchSummary = asyncio.run(
        fetch_all_pages(
            output_dir=source_dir,
            index_url=source.index_url,
            url_pattern=source.url_pattern,
            base_url=source.base_url,
            rate_limit=rate_limit,
            progress_callback=_print_progress,
            dry_run=check,
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
                print(f"  - {result.relative_path}: {result.error}")

    # If dry run, just report what would happen
    if check:
        print("\n[Dry run - no files written]")
        return False

    # Update metadata
    metadata["last_run"] = datetime.now(timezone.utc).isoformat()
    metadata["total_pages"] = summary.total_pages
    metadata["successful"] = summary.successful
    metadata["failed"] = summary.failed
    _save_metadata(source, metadata)

    # Report if changes were detected
    has_changes = _git_has_changes(source)
    if has_changes:
        print(f"\nChanges detected in {source_dir.name}/ (ready for commit)")
    else:
        print("\nNo changes detected")

    return has_changes


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch documentation from configured sources and track changes."
    )
    parser.add_argument(
        "--source",
        "-s",
        choices=["claude-code", "api", "all"],
        default="all",
        help="Source to fetch (default: all)",
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

    # Determine which sources to fetch
    if args.source == "all":
        sources = get_all_sources()
    else:
        sources = [get_source(args.source)]

    # Fetch each source
    any_changes = False
    for i, source in enumerate(sources):
        if i > 0:
            print("\n" + "=" * 60 + "\n")

        has_changes = _fetch_source(
            source=source,
            force=args.force,
            check=args.check,
            rate_limit=args.rate_limit,
        )
        any_changes = any_changes or has_changes

    # Final summary
    if len(sources) > 1:
        print("\n" + "=" * 60)
        if any_changes:
            print("Changes detected in one or more sources.")
        else:
            print("No changes detected in any source.")


if __name__ == "__main__":
    main()
