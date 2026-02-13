"""Source configuration for documentation tracking.

Defines all documentation sources with their URLs, patterns, and settings.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Source:
    """Configuration for a documentation source."""

    key: str
    name: str
    index_url: str
    url_pattern: str
    prompt_file: str
    base_url: str

    @property
    def docs_dir(self) -> str:
        """Directory name for storing docs (e.g., 'claude-code', 'api')."""
        return self.key

    @property
    def output_dir(self) -> str:
        """Directory name for output changelogs."""
        return self.key


SOURCES: Dict[str, Source] = {
    "claude-code": Source(
        key="claude-code",
        name="Claude Code CLI",
        index_url="https://code.claude.com/docs/llms.txt",
        url_pattern=r"https://code\.claude\.com/docs/en/[\w-]+\.md",
        prompt_file="lib/prompts/claude_code.md",
        base_url="https://code.claude.com/docs",
    ),
    "api": Source(
        key="api",
        name="Claude API",
        index_url="https://platform.claude.com/llms.txt",
        url_pattern=r"https://platform\.claude\.com/docs/en/[\w/-]+\.md",
        prompt_file="lib/prompts/api.md",
        base_url="https://platform.claude.com/docs",
    ),
}


def get_source(key: str) -> Source:
    """Get a source by key, raising ValueError if not found."""
    if key not in SOURCES:
        valid_keys = ", ".join(SOURCES.keys())
        raise ValueError(f"Unknown source: {key}. Valid sources: {valid_keys}")
    return SOURCES[key]


def get_all_sources() -> list[Source]:
    """Get all configured sources."""
    return list(SOURCES.values())
