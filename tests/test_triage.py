"""Tests for lib/triage.py — rule-based change classification."""

from __future__ import annotations

import pytest

from lib.differ import DiffReport, PageChange
from lib.triage import classify_changes


class TestClassifyChanges:

    def test_new_pages_are_significant(self):
        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            new_pages=["docs/api/en/new-feature.md"],
        )
        result = classify_changes(report, "api")
        assert len(result["changes"]) == 1
        assert result["changes"][0]["classification"] == "SIGNIFICANT"
        assert result["changes"][0]["reason"] == "rule: new_page"

    def test_removed_pages_are_significant(self):
        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            removed_pages=["docs/api/en/deprecated.md"],
        )
        result = classify_changes(report, "api")
        assert result["changes"][0]["classification"] == "SIGNIFICANT"
        assert result["changes"][0]["reason"] == "rule: removed_page"

    def test_heading_changes_are_significant(self):
        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            page_changes=[
                PageChange(
                    path="docs/api/en/overview.md",
                    status="modified",
                    additions=5,
                    deletions=2,
                    new_sections=["## New Section"],
                ),
            ],
        )
        result = classify_changes(report, "api")
        assert result["changes"][0]["classification"] == "SIGNIFICANT"
        assert result["changes"][0]["reason"] == "rule: heading_change"

    def test_large_changes_are_significant(self):
        """Changes with >50 total lines are SIGNIFICANT."""
        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            page_changes=[
                PageChange(
                    path="docs/api/en/big-change.md",
                    status="modified",
                    additions=40,
                    deletions=15,
                ),
            ],
        )
        result = classify_changes(report, "api")
        assert result["changes"][0]["classification"] == "SIGNIFICANT"
        assert result["changes"][0]["reason"] == "rule: line_count>50"

    def test_small_changes_are_minor(self):
        """Changes with <5 total lines are MINOR."""
        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            page_changes=[
                PageChange(
                    path="docs/api/en/typo-fix.md",
                    status="modified",
                    additions=2,
                    deletions=1,
                ),
            ],
        )
        result = classify_changes(report, "api")
        assert result["changes"][0]["classification"] == "MINOR"
        assert result["changes"][0]["reason"] == "rule: line_count<5"

    def test_medium_changes_default_significant(self):
        """Changes between 5-50 lines with no headings → SIGNIFICANT (default)."""
        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            page_changes=[
                PageChange(
                    path="docs/api/en/medium.md",
                    status="modified",
                    additions=15,
                    deletions=10,
                ),
            ],
        )
        result = classify_changes(report, "api")
        assert result["changes"][0]["classification"] == "SIGNIFICANT"
        assert result["changes"][0]["reason"] == "rule: default"

    def test_metadata_fields(self):
        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            new_pages=["page.md"],
        )
        result = classify_changes(report, "claude-code")
        assert result["source"] == "claude-code"
        assert "date" in result

    def test_empty_report(self):
        report = DiffReport(old_ref="a", new_ref="b", timestamp="t")
        result = classify_changes(report, "api")
        assert result["changes"] == []

    def test_additions_deletions_in_output(self):
        """Modified page stats are propagated to triage output."""
        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            page_changes=[
                PageChange(
                    path="p.md", status="modified",
                    additions=30, deletions=20,
                ),
            ],
        )
        result = classify_changes(report, "api")
        change = result["changes"][0]
        assert change["additions"] == 30
        assert change["deletions"] == 20

    def test_boundary_exactly_5_lines(self):
        """Exactly 5 total lines → not MINOR (requires <5)."""
        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            page_changes=[
                PageChange(
                    path="p.md", status="modified",
                    additions=3, deletions=2,
                ),
            ],
        )
        result = classify_changes(report, "api")
        # 3+2=5, which is not <5, so it falls through to default
        assert result["changes"][0]["classification"] == "SIGNIFICANT"

    def test_boundary_exactly_50_lines(self):
        """Exactly 50 total lines → not line_count>50 (requires >50)."""
        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            page_changes=[
                PageChange(
                    path="p.md", status="modified",
                    additions=30, deletions=20,
                ),
            ],
        )
        result = classify_changes(report, "api")
        # 30+20=50, which is not >50, so it falls to default
        assert result["changes"][0]["reason"] == "rule: default"
