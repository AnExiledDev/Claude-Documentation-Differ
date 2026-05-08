#!/usr/bin/env python3
"""Git-based documentation diff analysis.

Provides structured analysis of changes between documentation versions,
identifying new sections, removed content, and modifications.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class PageChange:
    """Change to a single documentation page."""

    path: str
    status: str  # 'added', 'modified', 'deleted'
    additions: int = 0
    deletions: int = 0
    new_sections: list[str] = field(default_factory=list)
    removed_sections: list[str] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "status": self.status,
            "additions": self.additions,
            "deletions": self.deletions,
            "new_sections": self.new_sections,
            "removed_sections": self.removed_sections,
            "summary": self.summary,
        }


@dataclass
class DiffReport:
    """Full diff report between two versions."""

    old_ref: str
    new_ref: str
    timestamp: str
    page_changes: list[PageChange] = field(default_factory=list)
    new_pages: list[str] = field(default_factory=list)
    removed_pages: list[str] = field(default_factory=list)

    @property
    def total_changes(self) -> int:
        return len(self.page_changes) + len(self.new_pages) + len(self.removed_pages)

    @property
    def summary(self) -> dict:
        return {
            "old_ref": self.old_ref,
            "new_ref": self.new_ref,
            "timestamp": self.timestamp,
            "new_pages": len(self.new_pages),
            "removed_pages": len(self.removed_pages),
            "modified_pages": len(self.page_changes),
            "total_additions": sum(p.additions for p in self.page_changes),
            "total_deletions": sum(p.deletions for p in self.page_changes),
        }

    def to_dict(self) -> dict:
        return {
            "old_ref": self.old_ref,
            "new_ref": self.new_ref,
            "timestamp": self.timestamp,
            "summary": self.summary,
            "new_pages": self.new_pages,
            "removed_pages": self.removed_pages,
            "page_changes": [p.to_dict() for p in self.page_changes],
        }

    def to_markdown(self) -> str:
        """Generate a markdown summary of the diff."""
        lines = [
            f"# Documentation Diff Report",
            f"",
            f"**Comparing:** `{self.old_ref}` → `{self.new_ref}`",
            f"**Generated:** {self.timestamp}",
            f"",
            f"## Summary",
            f"",
            f"- New pages: {len(self.new_pages)}",
            f"- Removed pages: {len(self.removed_pages)}",
            f"- Modified pages: {len(self.page_changes)}",
            f"",
        ]

        if self.new_pages:
            lines.extend(
                [
                    "## New Pages",
                    "",
                ]
            )
            for page in self.new_pages:
                lines.append(f"- `{page}`")
            lines.append("")

        if self.removed_pages:
            lines.extend(
                [
                    "## Removed Pages",
                    "",
                ]
            )
            for page in self.removed_pages:
                lines.append(f"- `{page}`")
            lines.append("")

        if self.page_changes:
            lines.extend(
                [
                    "## Modified Pages",
                    "",
                ]
            )
            for change in self.page_changes:
                lines.append(f"### `{change.path}`")
                lines.append(f"")
                lines.append(f"+{change.additions} / -{change.deletions} lines")
                lines.append("")

                if change.new_sections:
                    lines.append("**New sections:**")
                    for section in change.new_sections:
                        lines.append(f"- {section}")
                    lines.append("")

                if change.removed_sections:
                    lines.append("**Removed sections:**")
                    for section in change.removed_sections:
                        lines.append(f"- {section}")
                    lines.append("")

                if change.summary:
                    lines.append(f"**Summary:** {change.summary}")
                    lines.append("")

        return "\n".join(lines)


def _run_git(args: list[str], cwd: Path, check: bool = True) -> str:
    """Run a git command and return stdout.

    Args:
        args: Git subcommand and arguments
        cwd: Working directory for the command
        check: If True (default), raise on non-zero exit code

    Raises:
        subprocess.CalledProcessError: If check=True and git returns non-zero
    """
    result = subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode,
            ["git"] + args,
            result.stdout,
            result.stderr,
        )
    return result.stdout


def _parse_diff_stat(stat_output: str) -> dict[str, tuple[int, int]]:
    """Parse git diff --numstat output.

    Returns dict of {filename: (additions, deletions)}
    """
    changes = {}
    for line in stat_output.strip().split("\n"):
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) >= 3:
            adds = int(parts[0]) if parts[0] != "-" else 0
            dels = int(parts[1]) if parts[1] != "-" else 0
            filename = parts[2]
            changes[filename] = (adds, dels)
    return changes


def _extract_section_changes(diff_text: str) -> tuple[list[str], list[str]]:
    """Extract added/removed section headings from diff.

    Returns (new_sections, removed_sections)
    """
    new_sections = []
    removed_sections = []

    for line in diff_text.split("\n"):
        # Look for heading changes (## or ### lines)
        if line.startswith("+") and not line.startswith("+++"):
            match = re.match(r"^\+\s*(#{1,4}\s+.+)", line)
            if match:
                new_sections.append(match.group(1).strip())
        elif line.startswith("-") and not line.startswith("---"):
            match = re.match(r"^-\s*(#{1,4}\s+.+)", line)
            if match:
                removed_sections.append(match.group(1).strip())

    return new_sections, removed_sections


def analyze_changes(
    repo_dir: Path,
    old_ref: str = "HEAD~1",
    new_ref: str = "HEAD",
    path_filter: str | None = None,
) -> DiffReport:
    """Analyze changes between two Git refs.

    Args:
        repo_dir: Path to the git repository
        old_ref: Old commit reference (default: HEAD~1)
        new_ref: New commit reference (default: HEAD)
        path_filter: Optional path prefix to filter changes (e.g., "docs/claude-code/")

    Returns:
        DiffReport with detailed change information
    """
    timestamp = datetime.now(timezone.utc).isoformat()

    # Build git diff args with optional path filter
    base_args = ["diff"]
    path_args = ["--", path_filter] if path_filter else []

    # Get list of changed files with stats
    numstat = _run_git(
        base_args + ["--numstat", old_ref, new_ref] + path_args,
        repo_dir,
    )
    file_stats = _parse_diff_stat(numstat)

    # Get list of files by change type
    name_status = _run_git(
        base_args + ["--name-status", old_ref, new_ref] + path_args,
        repo_dir,
    )

    new_pages = []
    removed_pages = []
    page_changes = []

    for line in name_status.strip().split("\n"):
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) < 2:
            continue

        status = parts[0]
        filename = parts[1] if len(parts) == 2 else parts[2]  # Handle renames

        # Only process markdown files in en/
        if not filename.endswith(".md"):
            continue

        if status == "A":
            new_pages.append(filename)
        elif status == "D":
            removed_pages.append(filename)
        elif status.startswith("M") or status.startswith("R"):
            # Get detailed diff for this file
            file_diff = _run_git(
                ["diff", old_ref, new_ref, "--", filename],
                repo_dir,
            )

            new_sections, removed_sections = _extract_section_changes(file_diff)
            adds, dels = file_stats.get(filename, (0, 0))

            change = PageChange(
                path=filename,
                status="modified",
                additions=adds,
                deletions=dels,
                new_sections=new_sections,
                removed_sections=removed_sections,
            )
            page_changes.append(change)

    return DiffReport(
        old_ref=old_ref,
        new_ref=new_ref,
        timestamp=timestamp,
        page_changes=page_changes,
        new_pages=new_pages,
        removed_pages=removed_pages,
    )


def analyze_uncommitted(repo_dir: Path) -> DiffReport:
    """Analyze uncommitted changes (staged and unstaged).

    Args:
        repo_dir: Path to the git repository

    Returns:
        DiffReport for uncommitted changes
    """
    return analyze_changes(repo_dir, old_ref="HEAD", new_ref="")


def get_full_diff(
    repo_dir: Path,
    old_ref: str = "HEAD~1",
    new_ref: str = "HEAD",
    word_diff: bool = False,
    path_filter: str | None = None,
) -> str:
    """Get the full diff text between two refs.

    Args:
        repo_dir: Path to the git repository
        old_ref: Old commit reference
        new_ref: New commit reference
        word_diff: Use word-level diff (default: False for cleaner parsing)
        path_filter: Optional path prefix to filter changes

    Returns:
        Full diff text
    """
    args = ["diff"]
    if word_diff:
        args.append("--word-diff")
    args.extend([old_ref, new_ref])
    if path_filter:
        args.extend(["--", path_filter])

    return _run_git(args, repo_dir)


def get_last_changelog_commit(
    repo_dir: Path,
    source_name: str | None = None,
    max_age_days: int = 7,
) -> str | None:
    """Find the commit that last added a changelog for this source.

    Tries source-specific pattern first (e.g., "Add Claude Code changelog"),
    then falls back to generic "Add.*changelog" for backward compatibility
    with old commit message format.

    Args:
        repo_dir: Path to the git repository
        source_name: Source label to search for (e.g., "Claude Code", "API")
        max_age_days: Maximum age in days to search back

    Returns:
        Commit hash, or None if no changelog commit found within window
    """
    patterns = []
    if source_name:
        patterns.append(f"Add.*{source_name}.*changelog")
    patterns.append("Add.*changelog")

    for pattern in patterns:
        result = subprocess.run(
            [
                "git",
                "log",
                f"--since={max_age_days} days ago",
                "--format=%H",
                "-1",
                "--grep",
                pattern,
            ],
            cwd=str(repo_dir),
            capture_output=True,
            text=True,
        )
        commit = result.stdout.strip()
        if commit:
            return commit
    return None


def get_file_content(repo_dir: Path, filepath: str) -> str | None:
    """Read file content from the current working tree.

    Args:
        repo_dir: Path to the git repository
        filepath: Relative path to the file

    Returns:
        File content, or None if file doesn't exist
    """
    full_path = repo_dir / filepath
    if full_path.exists():
        return full_path.read_text()
    return None


def build_url_manifest(
    report: DiffReport,
    base_url: str,
    docs_prefix: str,
) -> dict[str, str]:
    """Build a mapping of doc file paths to their source URLs.

    Args:
        report: DiffReport with changed files
        base_url: Base URL for the documentation (e.g., "https://code.claude.com/docs")
        docs_prefix: Prefix in git paths to strip (e.g., "docs/claude-code/")

    Returns:
        Dict mapping relative paths to full URLs
    """
    manifest = {}

    all_paths = (
        report.new_pages + report.removed_pages + [c.path for c in report.page_changes]
    )

    for path in all_paths:
        # Strip the docs prefix to get the relative URL path
        rel = path
        if rel.startswith(docs_prefix):
            rel = rel[len(docs_prefix) :]

        url = f"{base_url}/{rel}"
        manifest[path] = url

    return manifest


# API docs category mapping based on path prefix
API_CATEGORIES: dict[str, str] = {
    "about-claude": "About Claude",
    "agent-sdk": "Agent SDK",
    "agents-and-tools": "Agents & Tools",
    "build-with-claude": "Building with Claude",
    "administration": "Administration",
    "resources": "Resources",
    "sdks": "SDKs",
    "api": "API Reference",
    "release-notes": "Release Notes",
    "test-and-evaluate": "Testing & Evaluation",
}


def categorize_changes(
    report: DiffReport,
    docs_prefix: str,
) -> dict[str, DiffReport]:
    """Split a DiffReport into category-based sub-reports.

    Categories are determined by the first path segment after docs_prefix/en/.
    E.g., "docs/api/en/agent-sdk/overview.md" → "agent-sdk" → "Agent SDK"

    Args:
        report: Full DiffReport to split
        docs_prefix: Prefix in git paths (e.g., "docs/api/")

    Returns:
        Dict mapping category key to DiffReport for that category
    """

    def _get_category(filepath: str) -> str:
        """Extract category from a file path."""
        rel = filepath
        if rel.startswith(docs_prefix):
            rel = rel[len(docs_prefix) :]
        # Strip leading en/
        if rel.startswith("en/"):
            rel = rel[3:]
        # First path segment is the category
        parts = rel.split("/")
        if len(parts) > 1:
            return parts[0]
        return "_root"

    # Group all changes by category
    categories: dict[str, dict] = {}

    for path in report.new_pages:
        cat = _get_category(path)
        categories.setdefault(cat, {"new": [], "removed": [], "modified": []})
        categories[cat]["new"].append(path)

    for path in report.removed_pages:
        cat = _get_category(path)
        categories.setdefault(cat, {"new": [], "removed": [], "modified": []})
        categories[cat]["removed"].append(path)

    for change in report.page_changes:
        cat = _get_category(change.path)
        categories.setdefault(cat, {"new": [], "removed": [], "modified": []})
        categories[cat]["modified"].append(change)

    # Build sub-reports
    sub_reports = {}
    for cat_key, data in categories.items():
        cat_name = API_CATEGORIES.get(cat_key, cat_key.replace("-", " ").title())
        sub_reports[cat_key] = DiffReport(
            old_ref=report.old_ref,
            new_ref=report.new_ref,
            timestamp=report.timestamp,
            new_pages=data["new"],
            removed_pages=data["removed"],
            page_changes=data["modified"],
        )

    return sub_reports
