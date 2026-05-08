"""Shared fixtures for documentation-differ tests."""

from __future__ import annotations

import pytest

from lib.differ import DiffReport, PageChange


@pytest.fixture
def empty_report() -> DiffReport:
    """A DiffReport with no changes."""
    return DiffReport(
        old_ref="abc1234",
        new_ref="def5678",
        timestamp="2026-05-08T12:00:00+00:00",
    )


@pytest.fixture
def sample_report() -> DiffReport:
    """A DiffReport with a mix of new, removed, and modified pages."""
    return DiffReport(
        old_ref="abc1234",
        new_ref="def5678",
        timestamp="2026-05-08T12:00:00+00:00",
        new_pages=[
            "docs/api/en/agent-sdk/overview.md",
            "docs/api/en/agent-sdk/quickstart.md",
        ],
        removed_pages=[
            "docs/api/en/resources/deprecated.md",
        ],
        page_changes=[
            PageChange(
                path="docs/api/en/about-claude/models.md",
                status="modified",
                additions=25,
                deletions=10,
                new_sections=["## New Model Pricing"],
                removed_sections=[],
            ),
            PageChange(
                path="docs/api/en/sdks/python.md",
                status="modified",
                additions=3,
                deletions=1,
                new_sections=[],
                removed_sections=[],
            ),
            PageChange(
                path="docs/api/en/agents-and-tools/tool-use.md",
                status="modified",
                additions=80,
                deletions=20,
                new_sections=["### Streaming Tool Use"],
                removed_sections=["### Legacy Tool Format"],
            ),
        ],
    )
