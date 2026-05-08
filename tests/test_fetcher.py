"""Tests for lib/fetcher.py — URL extraction and fetch result types."""

from __future__ import annotations

import pytest

from lib.fetcher import extract_relative_path, FetchResult, FetchSummary


# ---------------------------------------------------------------------------
# extract_relative_path
# ---------------------------------------------------------------------------

class TestExtractRelativePath:

    def test_claude_code_url(self):
        """Standard Claude Code docs URL."""
        url = "https://code.claude.com/docs/en/overview.md"
        base = "https://code.claude.com/docs"
        assert extract_relative_path(url, base) == "en/overview.md"

    def test_api_nested_url(self):
        """Deeply nested API docs URL."""
        url = "https://platform.claude.com/docs/en/api/messages/create.md"
        base = "https://platform.claude.com/docs"
        assert extract_relative_path(url, base) == "en/api/messages/create.md"

    def test_api_top_level(self):
        url = "https://platform.claude.com/docs/en/overview.md"
        base = "https://platform.claude.com/docs"
        assert extract_relative_path(url, base) == "en/overview.md"

    def test_fallback_to_base_url_stripping(self):
        """When no 'en/' in path, falls back to stripping base_url path."""
        url = "https://example.com/docs/some/page.md"
        base = "https://example.com/docs"
        result = extract_relative_path(url, base)
        assert result == "some/page.md"

    def test_last_resort_full_path(self):
        """When nothing else matches, returns full path sans leading slash."""
        url = "https://example.com/totally/different/path.md"
        base = "https://other.com"
        result = extract_relative_path(url, base)
        assert result == "totally/different/path.md"

    def test_en_in_middle_of_path(self):
        """Finds 'en/' even when not immediately after base."""
        url = "https://example.com/v2/docs/en/deep/nested/file.md"
        base = "https://example.com"
        assert extract_relative_path(url, base) == "en/deep/nested/file.md"

    def test_preserves_hyphens_and_underscores(self):
        url = "https://code.claude.com/docs/en/my-feature_v2.md"
        base = "https://code.claude.com/docs"
        assert extract_relative_path(url, base) == "en/my-feature_v2.md"


# ---------------------------------------------------------------------------
# FetchResult / FetchSummary
# ---------------------------------------------------------------------------

class TestFetchResult:

    def test_successful_result(self):
        r = FetchResult(
            url="https://example.com/page.md",
            relative_path="en/page.md",
            content="# Page",
            success=True,
        )
        assert r.success
        assert r.error is None
        assert r.content == "# Page"

    def test_failed_result(self):
        r = FetchResult(
            url="https://example.com/missing.md",
            relative_path="en/missing.md",
            content=None,
            success=False,
            error="Page not found (404)",
        )
        assert not r.success
        assert r.content is None
        assert "404" in r.error


class TestFetchSummary:

    def test_all_successful(self):
        results = [
            FetchResult("u1", "p1", "c1", True),
            FetchResult("u2", "p2", "c2", True),
        ]
        s = FetchSummary(total_pages=2, successful=2, failed=0, results=results)
        assert s.all_successful

    def test_has_failures(self):
        results = [
            FetchResult("u1", "p1", "c1", True),
            FetchResult("u2", "p2", None, False, "timeout"),
        ]
        s = FetchSummary(total_pages=2, successful=1, failed=1, results=results)
        assert not s.all_successful
