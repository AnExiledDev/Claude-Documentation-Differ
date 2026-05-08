"""Tests for lib/tokens.py — token estimation and model selection."""

from __future__ import annotations

from pathlib import Path

import pytest

from lib.differ import DiffReport, PageChange
from lib.tokens import (
    BYTES_PER_TOKEN,
    PROMPT_OVERHEAD_TOKENS,
    THRESHOLD_TRUNCATE,
    THRESHOLD_LARGE_MODEL,
    BUDGET_SONNET,
    BUDGET_SONNET_1M,
    TRUNCATE_NORMAL,
    TRUNCATE_AGGRESSIVE,
    estimate_workspace_tokens,
    select_model,
    ModelSelection,
)


# ---------------------------------------------------------------------------
# select_model
# ---------------------------------------------------------------------------

class TestSelectModel:

    def test_standard_tier(self):
        """Below truncation threshold → sonnet, normal truncation."""
        sel = select_model(50_000)
        assert sel.model == "sonnet"
        assert sel.budget == BUDGET_SONNET
        assert sel.max_page_lines == TRUNCATE_NORMAL

    def test_aggressive_truncation_tier(self):
        """Between truncation and large model thresholds."""
        sel = select_model(THRESHOLD_TRUNCATE + 1)
        assert sel.model == "sonnet"
        assert sel.budget == BUDGET_SONNET
        assert sel.max_page_lines == TRUNCATE_AGGRESSIVE

    def test_large_model_tier(self):
        """Above large model threshold → sonnet[1m]."""
        sel = select_model(THRESHOLD_LARGE_MODEL + 1)
        assert sel.model == "sonnet[1m]"
        assert sel.budget == BUDGET_SONNET_1M
        assert sel.max_page_lines == TRUNCATE_NORMAL

    def test_explicit_model_overrides(self):
        """Explicit model bypasses automatic selection."""
        sel = select_model(999_999, explicit_model="opus")
        assert sel.model == "opus"
        assert "explicit" in sel.reason

    def test_explicit_model_auto_is_ignored(self):
        """'auto' as explicit model still triggers dynamic selection."""
        sel = select_model(50_000, explicit_model="auto")
        assert sel.model == "sonnet"

    def test_explicit_budget_override(self):
        """User-specified budget overrides tier default."""
        sel = select_model(50_000, explicit_budget=10.0)
        assert sel.budget == 10.0

    def test_explicit_budget_with_large_model(self):
        sel = select_model(THRESHOLD_LARGE_MODEL + 1, explicit_budget=50.0)
        assert sel.model == "sonnet[1m]"
        assert sel.budget == 50.0

    def test_boundary_at_truncate_threshold(self):
        """Exactly at the threshold → standard tier (not aggressive)."""
        sel = select_model(THRESHOLD_TRUNCATE)
        assert sel.max_page_lines == TRUNCATE_NORMAL

    def test_boundary_at_large_model_threshold(self):
        """Exactly at the threshold → aggressive truncation (not large model)."""
        sel = select_model(THRESHOLD_LARGE_MODEL)
        assert sel.model == "sonnet"
        assert sel.max_page_lines == TRUNCATE_AGGRESSIVE

    def test_reason_includes_token_count(self):
        sel = select_model(75_000)
        assert "75,000" in sel.reason

    def test_estimated_tokens_preserved(self):
        sel = select_model(42_000)
        assert sel.estimated_tokens == 42_000


# ---------------------------------------------------------------------------
# estimate_workspace_tokens
# ---------------------------------------------------------------------------

class TestEstimateWorkspaceTokens:

    def test_diff_only(self, tmp_path: Path):
        """Estimation with just a diff and no page files."""
        report = DiffReport(old_ref="a", new_ref="b", timestamp="t")
        diff_text = "x" * 4000  # 4000 bytes = ~1000 tokens
        tokens = estimate_workspace_tokens(tmp_path, report, diff_text)

        expected_diff = 4000 // BYTES_PER_TOKEN
        # At least diff tokens + overhead
        assert tokens >= expected_diff + PROMPT_OVERHEAD_TOKENS

    def test_includes_page_content(self, tmp_path: Path):
        """New and modified page content contributes to token estimate."""
        # Create a page file
        page_dir = tmp_path / "docs" / "api" / "en"
        page_dir.mkdir(parents=True)
        page_file = page_dir / "overview.md"
        page_file.write_text("content " * 500)  # ~4000 bytes

        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            new_pages=["docs/api/en/overview.md"],
        )
        tokens = estimate_workspace_tokens(tmp_path, report, "small diff")

        # Should be more than just diff + overhead (page content adds tokens)
        diff_only = estimate_workspace_tokens(
            tmp_path,
            DiffReport(old_ref="a", new_ref="b", timestamp="t"),
            "small diff",
        )
        assert tokens > diff_only

    def test_truncates_long_pages(self, tmp_path: Path):
        """Pages longer than max_page_lines are truncated in estimation."""
        page_dir = tmp_path / "docs"
        page_dir.mkdir(parents=True)
        page_file = page_dir / "big.md"
        # Write 1000 lines
        page_file.write_text("\n".join(f"line {i}" for i in range(1000)))

        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            new_pages=["docs/big.md"],
        )

        tokens_normal = estimate_workspace_tokens(
            tmp_path, report, "", max_page_lines=500
        )
        tokens_aggressive = estimate_workspace_tokens(
            tmp_path, report, "", max_page_lines=200
        )
        # Aggressive truncation should yield fewer tokens
        assert tokens_aggressive < tokens_normal

    def test_missing_page_file_skipped(self, tmp_path: Path):
        """Pages that don't exist on disk are silently skipped."""
        report = DiffReport(
            old_ref="a", new_ref="b", timestamp="t",
            new_pages=["nonexistent/page.md"],
        )
        # Should not raise
        tokens = estimate_workspace_tokens(tmp_path, report, "diff")
        assert tokens > 0
