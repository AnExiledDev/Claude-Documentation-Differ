#!/usr/bin/env python3
"""Analyze documentation changes and generate changelogs.

Usage:
    python3 diff.py                     # Analyze uncommitted changes
    python3 diff.py HEAD~1 HEAD         # Compare two commits
    python3 diff.py --changelog         # Generate AI-powered changelog
    python3 diff.py --since 2026-02-01  # Changes since date
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lib.differ import analyze_changes, get_full_diff, DiffReport

_SCRIPT_DIR = Path(__file__).resolve().parent
_DOCS_DIR = _SCRIPT_DIR / "docs"
_OUTPUT_DIR = _SCRIPT_DIR / "output"


def _has_commits(repo_dir: Path) -> bool:
    """Check if the repo has any commits."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(repo_dir),
        capture_output=True,
    )
    return result.returncode == 0


def _get_commit_for_date(repo_dir: Path, date_str: str) -> str | None:
    """Get the first commit after a date."""
    result = subprocess.run(
        ["git", "log", "--since", date_str, "--format=%H", "--reverse"],
        cwd=str(repo_dir),
        capture_output=True,
        text=True,
    )
    commits = result.stdout.strip().split("\n")
    return commits[0] if commits and commits[0] else None


def _prepare_changelog_workspace(
    report: DiffReport,
    full_diff: str,
    workspace_dir: Path,
) -> None:
    """Prepare workspace files for Claude changelog generation."""
    workspace_dir.mkdir(parents=True, exist_ok=True)

    # Write summary JSON
    summary_path = workspace_dir / "summary.json"
    summary_path.write_text(json.dumps(report.to_dict(), indent=2))

    # Write full diff
    diff_path = workspace_dir / "full_diff.txt"
    diff_path.write_text(full_diff)

    # Write markdown report
    report_path = workspace_dir / "report.md"
    report_path.write_text(report.to_markdown())


def _generate_changelog(
    report: DiffReport,
    full_diff: str,
    output_path: Path,
    model: str = "sonnet",
    budget: float | None = 0.50,
    force: bool = False,
) -> bool:
    """Generate a changelog using Claude Code CLI.

    Supports authentication via:
    - ANTHROPIC_API_KEY (API key)
    - CLAUDE_CODE_OAUTH_TOKEN (OAuth token for headless mode)

    Returns True if changelog was generated successfully.
    """
    import os

    # Check for authentication
    has_api_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
    has_oauth = bool(os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"))

    if not has_api_key and not has_oauth:
        print(
            "  WARNING: No authentication found. Set ANTHROPIC_API_KEY or CLAUDE_CODE_OAUTH_TOKEN",
            file=sys.stderr,
        )

    if output_path.exists() and not force:
        print(f"  Changelog already exists: {output_path.name}")
        print("  Use --force to overwrite")
        return False

    # Prepare workspace
    workspace = _OUTPUT_DIR / ".changelog_workspace"
    if workspace.exists():
        shutil.rmtree(workspace)

    _prepare_changelog_workspace(report, full_diff, workspace)

    # Find system prompt
    system_prompt = _SCRIPT_DIR / "lib" / "changelog_prompt.md"
    if not system_prompt.exists():
        print(f"  ERROR: System prompt not found: {system_prompt}", file=sys.stderr)
        return False

    # Build CLI command
    user_prompt = (
        f"Generate a changelog for documentation changes. "
        f"Workspace: {workspace.resolve()}. "
        f"Write output to: {output_path.resolve()}"
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

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(_SCRIPT_DIR),
        )

        t1 = time.monotonic()
        print(
            f"  Claude CLI finished in {t1 - t0:.1f}s (exit code {result.returncode})"
        )

        if result.returncode != 0:
            print(f"  STDERR: {result.stderr[:2000]}", file=sys.stderr)

        # Verify output
        if output_path.exists():
            size = output_path.stat().st_size
            print(f"  Written: {output_path.name} ({size:,} bytes)")
            return True
        else:
            print(f"  ERROR: Claude did not write {output_path.name}", file=sys.stderr)
            if result.stdout:
                print(f"  stdout (last 1000 chars): {result.stdout[-1000:]}")
            return False

    finally:
        # Clean up workspace
        if workspace.exists():
            shutil.rmtree(workspace)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze documentation changes and generate changelogs."
    )
    parser.add_argument(
        "old_ref",
        nargs="?",
        default="HEAD~1",
        help="Old commit reference (default: HEAD~1)",
    )
    parser.add_argument(
        "new_ref",
        nargs="?",
        default="HEAD",
        help="New commit reference (default: HEAD)",
    )
    parser.add_argument(
        "--changelog",
        action="store_true",
        help="Generate AI-powered changelog",
    )
    parser.add_argument(
        "--since",
        metavar="DATE",
        help="Compare from first commit after DATE (e.g., 2026-02-01)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "markdown", "both"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: auto-generated)",
    )
    parser.add_argument(
        "--model",
        default="sonnet",
        help="Model for changelog generation (default: sonnet)",
    )
    parser.add_argument(
        "--budget",
        type=float,
        default=0.50,
        help="Max budget for changelog generation (default: $0.50)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )
    args = parser.parse_args()

    # Check if docs repo exists and has commits
    if not _DOCS_DIR.exists():
        print("ERROR: docs/ directory not found. Run fetch.py first.", file=sys.stderr)
        sys.exit(1)

    if not _has_commits(_DOCS_DIR):
        print("ERROR: No commits in docs/ repository yet.", file=sys.stderr)
        print("Run fetch.py to populate documentation first.", file=sys.stderr)
        sys.exit(1)

    # Resolve refs
    old_ref = args.old_ref
    new_ref = args.new_ref

    if args.since:
        since_commit = _get_commit_for_date(_DOCS_DIR, args.since)
        if since_commit:
            old_ref = f"{since_commit}~1" if since_commit else "HEAD~1"
        else:
            print(f"WARNING: No commits found since {args.since}", file=sys.stderr)

    print(f"Analyzing changes: {old_ref} → {new_ref}")
    print(f"  Repository: {_DOCS_DIR}")

    # Analyze changes
    try:
        report = analyze_changes(_DOCS_DIR, old_ref, new_ref)
    except Exception as e:
        print(f"ERROR: Failed to analyze changes: {e}", file=sys.stderr)
        sys.exit(1)

    print()
    print(f"Changes found:")
    print(f"  New pages:      {len(report.new_pages)}")
    print(f"  Removed pages:  {len(report.removed_pages)}")
    print(f"  Modified pages: {len(report.page_changes)}")

    if report.total_changes == 0:
        print("\nNo changes detected.")
        return

    # Ensure output directory exists
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate output filename
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    base_name = args.output or f"{date_str}_diff"

    # Write reports
    if args.format in ("json", "both"):
        json_path = _OUTPUT_DIR / f"{base_name}.json"
        json_path.write_text(json.dumps(report.to_dict(), indent=2))
        print(f"\n  Written: {json_path}")

    if args.format in ("markdown", "both"):
        md_path = _OUTPUT_DIR / f"{base_name}.md"
        md_path.write_text(report.to_markdown())
        print(f"  Written: {md_path}")

    # Generate changelog if requested
    if args.changelog:
        print("\nGenerating AI-powered changelog...")
        full_diff = get_full_diff(_DOCS_DIR, old_ref, new_ref)
        changelog_path = _OUTPUT_DIR / f"{date_str}_changelog.md"

        _generate_changelog(
            report=report,
            full_diff=full_diff,
            output_path=changelog_path,
            model=args.model,
            budget=args.budget,
            force=args.force,
        )


if __name__ == "__main__":
    main()
