#!/usr/bin/env python3
"""Merge partial changelogs into a daily summary using Claude Code CLI.

Usage:
    python3 merge_daily.py --source claude-code          # Merge today's partials
    python3 merge_daily.py --source api                  # Merge API partials
    python3 merge_daily.py --source all                  # Merge all sources
    python3 merge_daily.py --source claude-code --date 2026-05-08
    python3 merge_daily.py --source all --force          # Overwrite existing daily.md
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from diff import _generate_index
from sources import get_source, get_all_sources, Source

_SCRIPT_DIR = Path(__file__).resolve().parent
_OUTPUT_DIR = _SCRIPT_DIR / "output"


def _merge_source(
    source: Source,
    date_str: str,
    model: str = "sonnet",
    budget: float | None = None,
    force: bool = False,
) -> bool:
    """Merge partial changelogs for a single source on a given date.

    Returns True if daily.md was generated successfully.
    """
    date_dir = _OUTPUT_DIR / source.output_dir / date_str

    # Find partial changelogs
    if not date_dir.exists():
        print(f"No partial changelogs found for {source.name} on {date_str}. Skipping.")
        return False

    partials = sorted(date_dir.glob("partial_*_changelog.md"))

    if not partials:
        print(f"No partial changelogs found for {source.name} on {date_str}. Skipping.")
        return False

    # Check if daily.md already exists
    daily_path = date_dir / "daily.md"
    if daily_path.exists() and not force:
        print(f"Daily changelog already exists: {daily_path}")
        print("  Use --force to overwrite")
        return False

    print(f"Merging {len(partials)} partial changelog(s) for {source.name} on {date_str}...")
    for p in partials:
        print(f"  - {p.name}")

    # Check for authentication
    has_api_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
    has_oauth = bool(os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"))

    if not has_api_key and not has_oauth:
        print(
            "  WARNING: No authentication found. Set ANTHROPIC_API_KEY or CLAUDE_CODE_OAUTH_TOKEN",
            file=sys.stderr,
        )

    # Prepare workspace
    workspace = _OUTPUT_DIR / ".merge_workspace"
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True, exist_ok=True)

    try:
        # Write each partial's content to workspace
        partial_info = []
        for partial in partials:
            content = partial.read_text()
            dest = workspace / partial.name
            dest.write_text(content)
            partial_info.append({
                "filename": partial.name,
                "path": str(dest.resolve()),
                "size_bytes": len(content),
            })

        # Write manifest
        manifest = {
            "source_key": source.key,
            "source_name": source.name,
            "date": date_str,
            "partial_count": len(partials),
            "partials": partial_info,
            "output_path": str(daily_path.resolve()),
        }
        manifest_path = workspace / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Find system prompt
        system_prompt = _SCRIPT_DIR / "lib" / "prompts" / "daily_merge.md"
        if not system_prompt.exists():
            print(f"  ERROR: System prompt not found: {system_prompt}", file=sys.stderr)
            return False

        # Build CLI command
        user_prompt = (
            f"Merge partial changelogs for {source.name} on {date_str}. "
            f"Workspace: {workspace.resolve()}. "
            f"Read manifest.json for file listings, then read all partial changelog files. "
            f"Write the merged daily changelog to: {daily_path.resolve()}"
        )

        cmd = [
            "claude",
            "-p",
            user_prompt,
            "--system-prompt-file",
            str(system_prompt),
            "--model",
            model,
            "--dangerously-skip-permissions",
            "--allowedTools",
            "Read",
            "Write",
        ]

        if budget is not None:
            cmd.extend(["--max-budget-usd", str(budget)])
            budget_label = f"${budget}"
        else:
            budget_label = "unlimited"

        print(f"  Invoking Claude CLI (model={model}, budget={budget_label})...")
        t0 = time.monotonic()

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(_SCRIPT_DIR),
        )

        t1 = time.monotonic()
        print(f"  Claude CLI finished in {t1 - t0:.1f}s (exit code {result.returncode})")

        if result.returncode != 0:
            print(f"  STDERR: {result.stderr[:2000]}", file=sys.stderr)

        # Verify output
        if daily_path.exists():
            size = daily_path.stat().st_size
            print(f"  Written: daily.md ({size:,} bytes)")

            # Regenerate source index
            output_dir = _OUTPUT_DIR / source.output_dir
            _generate_index(output_dir, source.name)

            return True
        else:
            print(f"  ERROR: Claude did not write daily.md", file=sys.stderr)
            if result.stdout:
                print(f"  stdout (last 1000 chars): {result.stdout[-1000:]}")
            return False

    finally:
        # Clean up workspace
        if workspace.exists():
            shutil.rmtree(workspace)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge partial changelogs into a daily summary."
    )
    parser.add_argument(
        "--source",
        "-s",
        required=True,
        choices=["claude-code", "api", "all"],
        help="Source to merge",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="Date to merge (default: today UTC, format YYYY-MM-DD)",
    )
    parser.add_argument(
        "--model",
        default="sonnet",
        help="Model for Claude CLI (default: sonnet)",
    )
    parser.add_argument(
        "--budget",
        type=float,
        default=None,
        help="Max budget USD (default: no limit)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing daily.md",
    )
    args = parser.parse_args()

    # Resolve date
    date_str = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Determine which sources to process
    if args.source == "all":
        sources = get_all_sources()
    else:
        sources = [get_source(args.source)]

    # Process each source
    any_merged = False
    for i, source in enumerate(sources):
        if i > 0:
            print("\n" + "=" * 60 + "\n")

        success = _merge_source(
            source=source,
            date_str=date_str,
            model=args.model,
            budget=args.budget,
            force=args.force,
        )
        any_merged = any_merged or success

    # Final summary
    if len(sources) > 1:
        print("\n" + "=" * 60)
        if any_merged:
            print("Daily merge completed for one or more sources.")
        else:
            print("No daily merges were generated.")


if __name__ == "__main__":
    main()
