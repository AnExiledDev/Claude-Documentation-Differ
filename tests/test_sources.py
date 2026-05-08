"""Tests for sources.py — source configuration and lookup."""

from __future__ import annotations

import pytest

from sources import get_source, get_all_sources, Source, SOURCES


# ---------------------------------------------------------------------------
# Source dataclass
# ---------------------------------------------------------------------------

class TestSource:

    def test_docs_dir_matches_key(self):
        source = get_source("claude-code")
        assert source.docs_dir == "claude-code"

    def test_output_dir_matches_key(self):
        source = get_source("api")
        assert source.output_dir == "api"

    def test_frozen(self):
        source = get_source("claude-code")
        with pytest.raises(AttributeError):
            source.key = "something-else"


# ---------------------------------------------------------------------------
# get_source
# ---------------------------------------------------------------------------

class TestGetSource:

    def test_claude_code(self):
        source = get_source("claude-code")
        assert source.key == "claude-code"
        assert source.name == "Claude Code CLI"
        assert "code.claude.com" in source.index_url
        assert source.commit_label == "Claude Code"

    def test_api(self):
        source = get_source("api")
        assert source.key == "api"
        assert source.name == "Claude API"
        assert "platform.claude.com" in source.index_url
        assert source.commit_label == "API"

    def test_invalid_key_raises(self):
        with pytest.raises(ValueError, match="Unknown source: nonexistent"):
            get_source("nonexistent")

    def test_error_lists_valid_keys(self):
        with pytest.raises(ValueError, match="claude-code"):
            get_source("bad-key")


# ---------------------------------------------------------------------------
# get_all_sources
# ---------------------------------------------------------------------------

class TestGetAllSources:

    def test_returns_all(self):
        sources = get_all_sources()
        assert len(sources) == len(SOURCES)
        keys = {s.key for s in sources}
        assert "claude-code" in keys
        assert "api" in keys

    def test_returns_list_of_source(self):
        sources = get_all_sources()
        for s in sources:
            assert isinstance(s, Source)


# ---------------------------------------------------------------------------
# Source configuration integrity
# ---------------------------------------------------------------------------

class TestSourceConfig:
    """Verify that all configured sources have valid fields."""

    @pytest.mark.parametrize("key", list(SOURCES.keys()))
    def test_has_required_fields(self, key: str):
        source = SOURCES[key]
        assert source.key
        assert source.name
        assert source.index_url.startswith("https://")
        assert source.url_pattern
        assert source.prompt_file.endswith(".md")
        assert source.base_url.startswith("https://")
        assert source.commit_label

    @pytest.mark.parametrize("key", list(SOURCES.keys()))
    def test_prompt_file_exists(self, key: str):
        """Prompt files referenced in source config must exist on disk."""
        from pathlib import Path
        source = SOURCES[key]
        prompt_path = Path(__file__).resolve().parent.parent / source.prompt_file
        assert prompt_path.exists(), f"Missing prompt file: {source.prompt_file}"
