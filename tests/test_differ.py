"""Tests for lib/differ.py — diff parsing, analysis, and categorization."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from lib.differ import (
    PageChange,
    DiffReport,
    _parse_diff_stat,
    _extract_section_changes,
    _run_git,
    analyze_changes,
    build_url_manifest,
    categorize_changes,
    get_last_changelog_commit,
    get_file_content,
    API_CATEGORIES,
)


# ---------------------------------------------------------------------------
# _parse_diff_stat
# ---------------------------------------------------------------------------

class TestParseDiffStat:
    """Tests for _parse_diff_stat (git diff --numstat parsing)."""

    def test_normal_output(self):
        output = "10\t5\tdocs/api/en/overview.md\n3\t1\tdocs/api/en/models.md\n"
        result = _parse_diff_stat(output)
        assert result == {
            "docs/api/en/overview.md": (10, 5),
            "docs/api/en/models.md": (3, 1),
        }

    def test_binary_files(self):
        """Binary files show '-' for additions/deletions."""
        output = "-\t-\timages/logo.png\n5\t2\tREADME.md\n"
        result = _parse_diff_stat(output)
        assert result == {
            "images/logo.png": (0, 0),
            "README.md": (5, 2),
        }

    def test_empty_input(self):
        assert _parse_diff_stat("") == {}
        assert _parse_diff_stat("\n") == {}

    def test_single_file(self):
        output = "42\t0\tdocs/claude-code/en/new-feature.md"
        result = _parse_diff_stat(output)
        assert result == {"docs/claude-code/en/new-feature.md": (42, 0)}

    def test_tabs_in_filename(self):
        """Lines with fewer than 3 tab-separated parts are skipped."""
        output = "malformed line\n10\t5\tvalid.md\n"
        result = _parse_diff_stat(output)
        assert result == {"valid.md": (10, 5)}


# ---------------------------------------------------------------------------
# _extract_section_changes
# ---------------------------------------------------------------------------

class TestExtractSectionChanges:
    """Tests for _extract_section_changes (heading diff extraction)."""

    def test_added_headings(self):
        diff = (
            "+## New Feature\n"
            "+### Sub Feature\n"
            " some context\n"
        )
        new, removed = _extract_section_changes(diff)
        assert new == ["## New Feature", "### Sub Feature"]
        assert removed == []

    def test_removed_headings(self):
        diff = (
            "-## Old Feature\n"
            "-### Deprecated Section\n"
        )
        new, removed = _extract_section_changes(diff)
        assert new == []
        assert removed == ["## Old Feature", "### Deprecated Section"]

    def test_mixed_changes(self):
        diff = (
            "+## Added Section\n"
            "-## Removed Section\n"
            "+### New Subsection\n"
            " unchanged line\n"
        )
        new, removed = _extract_section_changes(diff)
        assert new == ["## Added Section", "### New Subsection"]
        assert removed == ["## Removed Section"]

    def test_ignores_diff_markers(self):
        """Lines starting with +++ or --- are file markers, not content."""
        diff = (
            "+++ b/docs/overview.md\n"
            "--- a/docs/overview.md\n"
            "+## Real Heading\n"
        )
        new, removed = _extract_section_changes(diff)
        assert new == ["## Real Heading"]
        assert removed == []

    def test_no_headings(self):
        diff = (
            "+just some added text\n"
            "-just some removed text\n"
            " context\n"
        )
        new, removed = _extract_section_changes(diff)
        assert new == []
        assert removed == []

    def test_h1_through_h4(self):
        """Should match # through ####."""
        diff = (
            "+# H1\n"
            "+## H2\n"
            "+### H3\n"
            "+#### H4\n"
            "+##### H5 should not match\n"
        )
        new, _ = _extract_section_changes(diff)
        assert len(new) == 4
        assert "# H1" in new
        assert "#### H4" in new


# ---------------------------------------------------------------------------
# PageChange
# ---------------------------------------------------------------------------

class TestPageChange:

    def test_to_dict(self):
        pc = PageChange(
            path="docs/api/en/overview.md",
            status="modified",
            additions=10,
            deletions=5,
            new_sections=["## New"],
            removed_sections=["## Old"],
            summary="Updated overview",
        )
        d = pc.to_dict()
        assert d["path"] == "docs/api/en/overview.md"
        assert d["status"] == "modified"
        assert d["additions"] == 10
        assert d["deletions"] == 5
        assert d["new_sections"] == ["## New"]
        assert d["removed_sections"] == ["## Old"]
        assert d["summary"] == "Updated overview"

    def test_defaults(self):
        pc = PageChange(path="test.md", status="added")
        assert pc.additions == 0
        assert pc.deletions == 0
        assert pc.new_sections == []
        assert pc.removed_sections == []
        assert pc.summary == ""


# ---------------------------------------------------------------------------
# DiffReport
# ---------------------------------------------------------------------------

class TestDiffReport:

    def test_total_changes(self, sample_report: DiffReport):
        # 2 new + 1 removed + 3 modified = 6
        assert sample_report.total_changes == 6

    def test_total_changes_empty(self, empty_report: DiffReport):
        assert empty_report.total_changes == 0

    def test_summary(self, sample_report: DiffReport):
        s = sample_report.summary
        assert s["new_pages"] == 2
        assert s["removed_pages"] == 1
        assert s["modified_pages"] == 3
        assert s["total_additions"] == 25 + 3 + 80
        assert s["total_deletions"] == 10 + 1 + 20

    def test_to_dict_roundtrip(self, sample_report: DiffReport):
        d = sample_report.to_dict()
        assert d["old_ref"] == "abc1234"
        assert d["new_ref"] == "def5678"
        assert len(d["new_pages"]) == 2
        assert len(d["removed_pages"]) == 1
        assert len(d["page_changes"]) == 3

    def test_to_markdown_contains_key_sections(self, sample_report: DiffReport):
        md = sample_report.to_markdown()
        assert "# Documentation Diff Report" in md
        assert "## New Pages" in md
        assert "## Removed Pages" in md
        assert "## Modified Pages" in md
        assert "agent-sdk/overview.md" in md
        assert "resources/deprecated.md" in md
        assert "+25 / -10 lines" in md

    def test_to_markdown_empty_report(self, empty_report: DiffReport):
        md = empty_report.to_markdown()
        assert "# Documentation Diff Report" in md
        assert "New pages: 0" in md
        assert "## New Pages" not in md

    def test_to_markdown_section_details(self, sample_report: DiffReport):
        md = sample_report.to_markdown()
        assert "**New sections:**" in md
        assert "## New Model Pricing" in md
        assert "**Removed sections:**" in md
        assert "### Legacy Tool Format" in md


# ---------------------------------------------------------------------------
# _run_git
# ---------------------------------------------------------------------------

class TestRunGit:

    @patch("lib.differ.subprocess.run")
    def test_success(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0, stdout="output\n", stderr=""
        )
        result = _run_git(["status"], Path("/repo"))
        assert result == "output\n"
        mock_run.assert_called_once_with(
            ["git", "status"],
            cwd="/repo",
            capture_output=True,
            text=True,
        )

    @patch("lib.differ.subprocess.run")
    def test_failure_raises(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=128, stdout="", stderr="fatal: bad ref"
        )
        with pytest.raises(subprocess.CalledProcessError) as exc_info:
            _run_git(["log", "--bad-flag"], Path("/repo"))
        assert exc_info.value.returncode == 128

    @patch("lib.differ.subprocess.run")
    def test_check_false_no_raise(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=1, stdout="", stderr="error"
        )
        result = _run_git(["diff"], Path("/repo"), check=False)
        assert result == ""


# ---------------------------------------------------------------------------
# build_url_manifest
# ---------------------------------------------------------------------------

class TestBuildUrlManifest:

    def test_strips_prefix_and_builds_urls(self, sample_report: DiffReport):
        manifest = build_url_manifest(
            sample_report,
            base_url="https://platform.claude.com/docs",
            docs_prefix="docs/api/",
        )
        # New pages
        assert manifest["docs/api/en/agent-sdk/overview.md"] == (
            "https://platform.claude.com/docs/en/agent-sdk/overview.md"
        )
        # Removed pages
        assert manifest["docs/api/en/resources/deprecated.md"] == (
            "https://platform.claude.com/docs/en/resources/deprecated.md"
        )
        # Modified pages
        assert manifest["docs/api/en/about-claude/models.md"] == (
            "https://platform.claude.com/docs/en/about-claude/models.md"
        )

    def test_empty_report(self, empty_report: DiffReport):
        manifest = build_url_manifest(
            empty_report,
            base_url="https://example.com",
            docs_prefix="docs/",
        )
        assert manifest == {}

    def test_path_without_prefix(self):
        """Paths not starting with docs_prefix are kept as-is in the URL."""
        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            new_pages=["other/file.md"],
        )
        manifest = build_url_manifest(report, "https://example.com", "docs/")
        assert manifest["other/file.md"] == "https://example.com/other/file.md"


# ---------------------------------------------------------------------------
# categorize_changes
# ---------------------------------------------------------------------------

class TestCategorizeChanges:

    def test_categorizes_by_path_segment(self, sample_report: DiffReport):
        sub_reports = categorize_changes(sample_report, "docs/api/")
        assert "agent-sdk" in sub_reports
        assert "resources" in sub_reports
        assert "about-claude" in sub_reports
        assert "sdks" in sub_reports
        assert "agents-and-tools" in sub_reports

    def test_category_contents(self, sample_report: DiffReport):
        sub_reports = categorize_changes(sample_report, "docs/api/")

        # agent-sdk should have 2 new pages
        agent_sdk = sub_reports["agent-sdk"]
        assert len(agent_sdk.new_pages) == 2
        assert agent_sdk.total_changes == 2

        # about-claude should have 1 modified page
        about = sub_reports["about-claude"]
        assert len(about.page_changes) == 1
        assert about.page_changes[0].additions == 25

    def test_empty_report(self, empty_report: DiffReport):
        sub_reports = categorize_changes(empty_report, "docs/api/")
        assert sub_reports == {}

    def test_root_level_file(self):
        """Files directly under en/ (no subdirectory) get '_root' category."""
        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            new_pages=["docs/api/en/index.md"],
        )
        sub_reports = categorize_changes(report, "docs/api/")
        assert "_root" in sub_reports

    def test_preserves_refs_and_timestamp(self, sample_report: DiffReport):
        sub_reports = categorize_changes(sample_report, "docs/api/")
        for sub in sub_reports.values():
            assert sub.old_ref == "abc1234"
            assert sub.new_ref == "def5678"
            assert sub.timestamp == "2026-05-08T12:00:00+00:00"


# ---------------------------------------------------------------------------
# get_last_changelog_commit
# ---------------------------------------------------------------------------

class TestGetLastChangelogCommit:

    @patch("lib.differ.subprocess.run")
    def test_source_specific_match(self, mock_run):
        """Finds commit with source-specific pattern."""
        mock_run.return_value = MagicMock(
            returncode=0, stdout="abc123\n", stderr=""
        )
        result = get_last_changelog_commit(Path("/repo"), "Claude Code")
        assert result == "abc123"
        # Should search source-specific pattern first
        call_args = mock_run.call_args_list[0]
        assert "Add.*Claude Code.*changelog" in call_args[0][0]

    @patch("lib.differ.subprocess.run")
    def test_falls_back_to_generic(self, mock_run):
        """Falls back to generic pattern when source-specific finds nothing."""
        # First call (source-specific) returns nothing
        # Second call (generic) returns a commit
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="", stderr=""),
            MagicMock(returncode=0, stdout="def456\n", stderr=""),
        ]
        result = get_last_changelog_commit(Path("/repo"), "Claude Code")
        assert result == "def456"

    @patch("lib.differ.subprocess.run")
    def test_no_source_name(self, mock_run):
        """Without source_name, only searches generic pattern."""
        mock_run.return_value = MagicMock(
            returncode=0, stdout="abc123\n", stderr=""
        )
        result = get_last_changelog_commit(Path("/repo"))
        assert result == "abc123"
        # Only one call (generic pattern)
        assert mock_run.call_count == 1

    @patch("lib.differ.subprocess.run")
    def test_no_commit_found(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0, stdout="", stderr=""
        )
        result = get_last_changelog_commit(Path("/repo"))
        assert result is None

    @patch("lib.differ.subprocess.run")
    def test_respects_max_age_days(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0, stdout="", stderr=""
        )
        get_last_changelog_commit(Path("/repo"), max_age_days=60)
        call_args = mock_run.call_args_list[0][0][0]
        assert "--since=60 days ago" in call_args


# ---------------------------------------------------------------------------
# get_file_content
# ---------------------------------------------------------------------------

class TestGetFileContent:

    def test_reads_existing_file(self, tmp_path: Path):
        f = tmp_path / "test.md"
        f.write_text("hello world")
        assert get_file_content(tmp_path, "test.md") == "hello world"

    def test_returns_none_for_missing(self, tmp_path: Path):
        assert get_file_content(tmp_path, "nonexistent.md") is None

    def test_nested_path(self, tmp_path: Path):
        nested = tmp_path / "a" / "b"
        nested.mkdir(parents=True)
        f = nested / "deep.md"
        f.write_text("deep content")
        assert get_file_content(tmp_path, "a/b/deep.md") == "deep content"


# ---------------------------------------------------------------------------
# analyze_changes (integration-style with mocked git)
# ---------------------------------------------------------------------------

class TestAnalyzeChanges:

    @patch("lib.differ._run_git")
    def test_detects_all_change_types(self, mock_git):
        """Verifies new, deleted, and modified files are classified correctly."""
        # Call 1: numstat
        mock_git.side_effect = [
            "15\t3\tdocs/api/en/overview.md\n",        # numstat
            "A\tdocs/api/en/new-page.md\n"             # name-status
            "D\tdocs/api/en/old-page.md\n"
            "M\tdocs/api/en/overview.md\n",
            "+## Added Heading\n-## Removed Heading\n",  # file diff
        ]

        report = analyze_changes(Path("/repo"), "HEAD~1", "HEAD", "docs/api/")

        assert len(report.new_pages) == 1
        assert "docs/api/en/new-page.md" in report.new_pages
        assert len(report.removed_pages) == 1
        assert "docs/api/en/old-page.md" in report.removed_pages
        assert len(report.page_changes) == 1
        assert report.page_changes[0].path == "docs/api/en/overview.md"
        assert report.page_changes[0].additions == 15

    @patch("lib.differ._run_git")
    def test_skips_non_markdown(self, mock_git):
        mock_git.side_effect = [
            "5\t2\tmetadata.json\n",    # numstat
            "M\tmetadata.json\n",       # name-status
        ]

        report = analyze_changes(Path("/repo"))
        assert report.total_changes == 0

    @patch("lib.differ._run_git")
    def test_handles_renames(self, mock_git):
        """Renamed files use the destination path (parts[2])."""
        mock_git.side_effect = [
            "10\t5\tdocs/api/en/new-name.md\n",                      # numstat
            "R100\tdocs/api/en/old-name.md\tdocs/api/en/new-name.md\n",  # name-status
            "+## Section\n",                                           # file diff
        ]

        report = analyze_changes(Path("/repo"))
        assert len(report.page_changes) == 1
        assert report.page_changes[0].path == "docs/api/en/new-name.md"
