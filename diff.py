#!/usr/bin/env python3
"""Analyze documentation changes and generate changelogs.

Usage:
    python3 diff.py                           # Analyze all sources (uncommitted)
    python3 diff.py --source claude-code      # Analyze Claude Code docs only
    python3 diff.py --source api              # Analyze Claude API docs only
    python3 diff.py HEAD~1 HEAD               # Compare two commits
    python3 diff.py --changelog               # Generate AI-powered changelog
    python3 diff.py --since 2026-02-01        # Changes since date
    python3 diff.py --since-last-changelog    # Changes since last changelog commit
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lib.differ import (
    analyze_changes,
    build_url_manifest,
    categorize_changes,
    get_file_content,
    get_full_diff,
    get_last_changelog_commit,
    DiffReport,
    API_CATEGORIES,
)
from lib.triage import classify_changes
from sources import get_source, get_all_sources, Source

_SCRIPT_DIR = Path(__file__).resolve().parent
_DOCS_DIR = _SCRIPT_DIR / "docs"
_OUTPUT_DIR = _SCRIPT_DIR / "output"

# Max lines per page to include in workspace (prevents context overflow)
_MAX_PAGE_LINES = 500
# Max categories for split changelogs
_MAX_CATEGORIES = 5


def _get_source_paths(source: Source) -> tuple[Path, Path]:
    """Get paths for a source.

    Returns:
        (docs_dir, output_dir)
    """
    docs_dir = _DOCS_DIR / source.docs_dir
    output_dir = _OUTPUT_DIR / source.output_dir
    return docs_dir, output_dir


def _generate_index(output_dir: Path, source_name: str) -> None:
    """Auto-generate index.md listing all date subdirectories (newest first)."""
    date_dirs = sorted(
        [
            d
            for d in output_dir.iterdir()
            if d.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}$", d.name)
        ],
        key=lambda d: d.name,
        reverse=True,
    )

    if not date_dirs:
        return

    lines = [
        f"# {source_name} Changelog Index",
        "",
    ]

    for date_dir in date_dirs:
        md_files = sorted(f for f in date_dir.iterdir() if f.suffix == ".md")
        if not md_files:
            continue

        lines.append(f"## {date_dir.name}")
        lines.append("")
        for f in md_files:
            lines.append(f"- [{f.name}]({date_dir.name}/{f.name})")
        lines.append("")

    index_path = output_dir / "index.md"
    index_path.write_text("\n".join(lines))


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


def _truncate_content(content: str, max_lines: int = _MAX_PAGE_LINES) -> str:
    """Truncate content to max_lines, adding a truncation note."""
    lines = content.split("\n")
    if len(lines) <= max_lines:
        return content
    truncated = "\n".join(lines[:max_lines])
    truncated += f"\n\n[... truncated, {len(lines) - max_lines} more lines ...]"
    return truncated


def _prepare_changelog_workspace(
    source: Source,
    report: DiffReport,
    full_diff: str,
    workspace_dir: Path,
) -> None:
    """Prepare workspace files for Claude changelog generation.

    Creates an enriched workspace with full page content, URL manifest,
    and structured diff data to give Claude maximum context.
    """
    workspace_dir.mkdir(parents=True, exist_ok=True)

    # Write summary JSON
    summary_path = workspace_dir / "summary.json"
    summary_path.write_text(json.dumps(report.to_dict(), indent=2))

    # Write full diff (unified format)
    diff_path = workspace_dir / "full_diff.txt"
    diff_path.write_text(full_diff)

    # Write markdown report
    report_path = workspace_dir / "report.md"
    report_path.write_text(report.to_markdown())

    # Build and write URL manifest
    docs_prefix = f"docs/{source.key}/"
    manifest = build_url_manifest(report, source.base_url, docs_prefix)
    manifest_path = workspace_dir / "url_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    # Write full content of new pages
    docs_prefix_str = docs_prefix
    new_pages_dir = workspace_dir / "new_pages"
    if report.new_pages:
        new_pages_dir.mkdir(parents=True, exist_ok=True)
        for page_path in report.new_pages:
            content = get_file_content(_SCRIPT_DIR, page_path)
            if content:
                # Use path relative to docs prefix, replacing / with _
                # to avoid collisions (e.g., api/create.md and sdks/create.md)
                rel = page_path
                if rel.startswith(docs_prefix_str):
                    rel = rel[len(docs_prefix_str) :]
                safe_name = rel.replace("/", "_")
                out = new_pages_dir / safe_name
                out.write_text(_truncate_content(content))

    # Write current content of modified pages
    modified_pages_dir = workspace_dir / "modified_pages"
    if report.page_changes:
        modified_pages_dir.mkdir(parents=True, exist_ok=True)
        # Sort by change magnitude (most changed first)
        sorted_changes = sorted(
            report.page_changes,
            key=lambda c: c.additions + c.deletions,
            reverse=True,
        )
        for change in sorted_changes:
            content = get_file_content(_SCRIPT_DIR, change.path)
            if content:
                rel = change.path
                if rel.startswith(docs_prefix_str):
                    rel = rel[len(docs_prefix_str) :]
                safe_name = rel.replace("/", "_")
                out = modified_pages_dir / safe_name
                out.write_text(_truncate_content(content))

    # Write triage classification
    try:
        triage = classify_changes(report, source.key)
        triage_path = workspace_dir / "triage.json"
        triage_path.write_text(json.dumps(triage, indent=2))
    except Exception as e:
        print(f"  WARNING: Triage classification failed: {e}", file=sys.stderr)


def _generate_changelog(
    source: Source,
    report: DiffReport,
    full_diff: str,
    output_path: Path,
    model: str = "sonnet",
    budget: float | None = None,
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

    _prepare_changelog_workspace(source, report, full_diff, workspace)

    # Find system prompt (source-specific)
    system_prompt = _SCRIPT_DIR / source.prompt_file
    if not system_prompt.exists():
        print(f"  ERROR: System prompt not found: {system_prompt}", file=sys.stderr)
        return False

    # Build CLI command
    user_prompt = (
        f"Generate a changelog for {source.name} documentation changes. "
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


def _generate_category_changelogs(
    source: Source,
    report: DiffReport,
    old_ref: str,
    new_ref: str,
    date_dir: Path,
    model: str = "sonnet",
    budget: float | None = None,
    force: bool = False,
) -> bool:
    """Generate split changelogs by category for large diffs.

    Creates a master changelog that references category-specific changelogs.
    Each category gets its own Claude invocation with a focused diff.

    Args:
        date_dir: Date subdirectory (e.g., output/api/2026-04-16/)

    Returns True if any changelogs were generated.
    """
    date_str = date_dir.name

    docs_prefix = f"docs/{source.key}/"
    sub_reports = categorize_changes(report, docs_prefix)

    if not sub_reports:
        return False

    # Sort categories by total changes (most active first)
    sorted_cats = sorted(
        sub_reports.items(),
        key=lambda kv: kv[1].total_changes,
        reverse=True,
    )

    # Merge small categories into "other" if we have too many
    if len(sorted_cats) > _MAX_CATEGORIES:
        keep = sorted_cats[: _MAX_CATEGORIES - 1]
        merge = sorted_cats[_MAX_CATEGORIES - 1 :]

        # Merge the remaining into an "other" report
        other_new = []
        other_removed = []
        other_modified = []
        for _, sub in merge:
            other_new.extend(sub.new_pages)
            other_removed.extend(sub.removed_pages)
            other_modified.extend(sub.page_changes)

        other_report = DiffReport(
            old_ref=report.old_ref,
            new_ref=report.new_ref,
            timestamp=report.timestamp,
            new_pages=other_new,
            removed_pages=other_removed,
            page_changes=other_modified,
        )
        sorted_cats = keep + [("other", other_report)]

    # Generate a changelog for each category
    category_files = []
    any_success = False

    for cat_key, sub_report in sorted_cats:
        if sub_report.total_changes == 0:
            continue

        cat_name = API_CATEGORIES.get(cat_key, cat_key.replace("-", " ").title())
        cat_filename = f"{cat_key}_changelog.md"
        cat_path = date_dir / cat_filename

        print(f"\n  Category: {cat_name} ({sub_report.total_changes} changes)")

        # Get category-specific diff
        cat_diff = get_full_diff(
            _SCRIPT_DIR,
            old_ref,
            new_ref,
            path_filter=f"docs/{source.key}/en/{cat_key}/",
        )

        success = _generate_changelog(
            source=source,
            report=sub_report,
            full_diff=cat_diff,
            output_path=cat_path,
            model=model,
            budget=budget,
            force=force,
        )

        if success:
            any_success = True
            category_files.append((cat_name, cat_filename, sub_report))

    # Generate master changelog that references category changelogs
    if category_files:
        master_path = date_dir / "changelog.md"
        master_lines = [
            f"# {source.name} Documentation Changes — {date_str}",
            "",
            "## Summary",
            "",
            f"- **{report.total_changes}** total changes across"
            f" **{len(category_files)}** categories",
            f"- {len(report.new_pages)} new pages,"
            f" {len(report.removed_pages)} removed,"
            f" {len(report.page_changes)} modified",
            "",
            "## Category Changelogs",
            "",
        ]

        for cat_name, cat_filename, sub in category_files:
            master_lines.append(
                f"- **[{cat_name}]({cat_filename})**: "
                f"{sub.total_changes} changes "
                f"({len(sub.new_pages)} new, {len(sub.page_changes)} modified)"
            )

        master_lines.extend(
            [
                "",
                "---",
                f"*Generated from {source.name} documentation changes detected on"
                f" {date_str}*",
            ]
        )

        master_path.write_text("\n".join(master_lines))
        print(f"\n  Master changelog: {master_path.name}")

    return any_success


def _process_source(
    source: Source,
    old_ref: str,
    new_ref: str,
    args: argparse.Namespace,
) -> bool:
    """Process a single source for diffs and optional changelog.

    Returns:
        True if changes were found, False otherwise.
    """
    docs_dir, output_dir = _get_source_paths(source)

    # Check if docs repo exists and has commits
    if not docs_dir.exists():
        print(
            f"ERROR: {docs_dir}/ directory not found. Run fetch.py first.",
            file=sys.stderr,
        )
        return False

    if not _has_commits(_SCRIPT_DIR):
        print("ERROR: No commits in repository yet.", file=sys.stderr)
        print("Run fetch.py to populate documentation first.", file=sys.stderr)
        return False

    print(f"Analyzing {source.name} changes: {old_ref} → {new_ref}")
    print(f"  Source: {docs_dir}")

    # Analyze changes (relative to docs/source_key/ directory)
    try:
        report = analyze_changes(
            _SCRIPT_DIR, old_ref, new_ref, path_filter=f"docs/{source.key}/"
        )
    except Exception as e:
        print(f"ERROR: Failed to analyze changes: {e}", file=sys.stderr)
        return False

    print()
    print(f"Changes found:")
    print(f"  New pages:      {len(report.new_pages)}")
    print(f"  Removed pages:  {len(report.removed_pages)}")
    print(f"  Modified pages: {len(report.page_changes)}")

    if report.total_changes == 0:
        print("\nNo changes detected.")
        return False

    # Create date subdirectory for output
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    hour_str = now.strftime("%H")
    date_dir = output_dir / date_str
    date_dir.mkdir(parents=True, exist_ok=True)

    # Write reports
    base_name = args.output or "diff"

    if args.format in ("json", "both"):
        json_path = date_dir / f"{base_name}.json"
        json_path.write_text(json.dumps(report.to_dict(), indent=2))
        print(f"\n  Written: {json_path}")

    if args.format in ("markdown", "both"):
        md_path = date_dir / f"{base_name}.md"
        md_path.write_text(report.to_markdown())
        print(f"  Written: {md_path}")

    # Generate changelog if requested
    if args.changelog:
        print(f"\nGenerating AI-powered changelog for {source.name}...")
        full_diff = get_full_diff(
            _SCRIPT_DIR, old_ref, new_ref, path_filter=f"docs/{source.key}/"
        )

        # Use category splitting for large diffs (API docs)
        if source.key == "api" and report.total_changes > 10:
            print(
                f"  Large diff detected ({report.total_changes} changes) —"
                " splitting by category"
            )
            _generate_category_changelogs(
                source=source,
                report=report,
                old_ref=old_ref,
                new_ref=new_ref,
                date_dir=date_dir,
                model=args.model,
                budget=args.budget,
                force=args.force,
            )
        else:
            changelog_path = date_dir / f"partial_{hour_str}h_changelog.md"
            _generate_changelog(
                source=source,
                report=report,
                full_diff=full_diff,
                output_path=changelog_path,
                model=args.model,
                budget=args.budget,
                force=args.force,
            )

        # Regenerate source index
        _generate_index(output_dir, source.name)

    return True


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
        "--source",
        "-s",
        choices=["claude-code", "api", "all"],
        default="all",
        help="Source to analyze (default: all)",
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
        "--since-last-changelog",
        action="store_true",
        help="Compare from the last changelog commit (accumulates changes)",
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
        default=None,
        help="Max budget for changelog generation (default: no limit)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )
    args = parser.parse_args()

    # Resolve refs
    old_ref = args.old_ref
    new_ref = args.new_ref

    if args.since_last_changelog:
        # Find the last changelog commit and diff from there
        source_label = None
        if args.source != "all":
            source_label = get_source(args.source).commit_label
        last_cl = get_last_changelog_commit(_SCRIPT_DIR, source_label)
        if last_cl:
            old_ref = last_cl
            print(f"Using last changelog commit as base: {old_ref[:8]}")
        else:
            print(
                "No previous changelog commit found (within 7 days), using HEAD~1",
                file=sys.stderr,
            )
    elif args.since:
        since_commit = _get_commit_for_date(_SCRIPT_DIR, args.since)
        if since_commit:
            old_ref = f"{since_commit}~1" if since_commit else "HEAD~1"
        else:
            print(
                f"WARNING: No commits found since {args.since}",
                file=sys.stderr,
            )

    # Determine which sources to process
    if args.source == "all":
        sources = get_all_sources()
    else:
        sources = [get_source(args.source)]

    # Process each source
    any_changes = False
    for i, source in enumerate(sources):
        if i > 0:
            print("\n" + "=" * 60 + "\n")

        has_changes = _process_source(source, old_ref, new_ref, args)
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
