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


def _run_git(args: list[str], cwd: Path) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
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
    word_diff: bool = True,
    path_filter: str | None = None,
) -> str:
    """Get the full diff text between two refs.

    Args:
        repo_dir: Path to the git repository
        old_ref: Old commit reference
        new_ref: New commit reference
        word_diff: Use word-level diff (better for prose)
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
