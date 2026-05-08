"""Tests for diff.py — CLI helper functions."""

from __future__ import annotations

import re
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# diff.py uses sys.path.insert, so we need to ensure the project root is importable
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from diff import _truncate_content, _get_commit_for_date, _generate_index


# ---------------------------------------------------------------------------
# _truncate_content
# ---------------------------------------------------------------------------

class TestTruncateContent:

    def test_short_content_unchanged(self):
        content = "line1\nline2\nline3"
        assert _truncate_content(content, max_lines=10) == content

    def test_exact_limit_unchanged(self):
        content = "\n".join(f"line{i}" for i in range(500))
        assert _truncate_content(content, max_lines=500) == content

    def test_over_limit_truncated(self):
        lines = [f"line{i}" for i in range(100)]
        content = "\n".join(lines)
        result = _truncate_content(content, max_lines=50)

        # First 50 lines should be present
        assert "line0" in result
        assert "line49" in result
        # Line 50+ should not
        assert "line50" not in result
        # Truncation note
        assert "[... truncated, 50 more lines ...]" in result

    def test_custom_limit(self):
        content = "\n".join(f"line{i}" for i in range(20))
        result = _truncate_content(content, max_lines=5)
        assert "[... truncated, 15 more lines ...]" in result

    def test_single_line(self):
        assert _truncate_content("hello", max_lines=1) == "hello"

    def test_empty_content(self):
        assert _truncate_content("", max_lines=10) == ""


# ---------------------------------------------------------------------------
# _get_commit_for_date
# ---------------------------------------------------------------------------

class TestGetCommitForDate:

    @patch("diff.subprocess.run")
    def test_finds_commit(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="abc123\ndef456\n",
            stderr="",
        )
        result = _get_commit_for_date(Path("/repo"), "2026-05-01")
        assert result == "abc123"  # First (oldest) commit after the date

    @patch("diff.subprocess.run")
    def test_no_commits_found(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr="",
        )
        result = _get_commit_for_date(Path("/repo"), "2099-01-01")
        assert result is None

    @patch("diff.subprocess.run")
    def test_passes_date_to_git(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0, stdout="", stderr=""
        )
        _get_commit_for_date(Path("/repo"), "2026-03-15")
        cmd = mock_run.call_args[0][0]
        assert "--since" in cmd
        assert "2026-03-15" in cmd


# ---------------------------------------------------------------------------
# _generate_index
# ---------------------------------------------------------------------------

class TestGenerateIndex:

    def test_generates_index_with_dates(self, tmp_path: Path):
        """Creates index.md listing date directories and their files."""
        # Create date subdirectories with files
        d1 = tmp_path / "2026-05-07"
        d1.mkdir()
        (d1 / "partial_06h_changelog.md").write_text("content")
        (d1 / "daily.md").write_text("content")

        d2 = tmp_path / "2026-05-08"
        d2.mkdir()
        (d2 / "partial_00h_changelog.md").write_text("content")

        _generate_index(tmp_path, "Test Source")

        index = (tmp_path / "index.md").read_text()
        assert "# Test Source Changelog Index" in index
        # Newest first
        lines = index.split("\n")
        idx_08 = next(i for i, l in enumerate(lines) if "2026-05-08" in l)
        idx_07 = next(i for i, l in enumerate(lines) if "2026-05-07" in l)
        assert idx_08 < idx_07  # 08 appears before 07

    def test_skips_non_date_directories(self, tmp_path: Path):
        """Non-date directories (e.g., '.workspace') are ignored."""
        (tmp_path / ".workspace").mkdir()
        d = tmp_path / "2026-05-08"
        d.mkdir()
        (d / "changelog.md").write_text("content")

        _generate_index(tmp_path, "Source")

        index = (tmp_path / "index.md").read_text()
        assert ".workspace" not in index

    def test_no_date_dirs_no_index(self, tmp_path: Path):
        """If there are no date directories, don't create index.md."""
        _generate_index(tmp_path, "Source")
        assert not (tmp_path / "index.md").exists()

    def test_skips_empty_date_dirs(self, tmp_path: Path):
        """Date dirs with no .md files don't get a section."""
        d = tmp_path / "2026-05-08"
        d.mkdir()
        # No .md files, just a .json
        (d / "data.json").write_text("{}")

        d2 = tmp_path / "2026-05-07"
        d2.mkdir()
        (d2 / "changelog.md").write_text("content")

        _generate_index(tmp_path, "Source")

        index = (tmp_path / "index.md").read_text()
        assert "2026-05-07" in index
        assert "2026-05-08" not in index

    def test_links_are_relative(self, tmp_path: Path):
        d = tmp_path / "2026-05-08"
        d.mkdir()
        (d / "daily.md").write_text("content")

        _generate_index(tmp_path, "Source")

        index = (tmp_path / "index.md").read_text()
        assert "[daily.md](2026-05-08/daily.md)" in index
