"""Token estimation and dynamic model selection for changelog generation.

Estimates workspace token count and selects the appropriate model tier,
budget cap, and truncation level. Thresholds are configurable via env vars.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from lib.differ import DiffReport

# Approximate bytes-per-token ratio for English text / markdown
BYTES_PER_TOKEN = 4

# Estimated overhead for system prompt, user prompt, and formatting
PROMPT_OVERHEAD_TOKENS = 5_000

# Token thresholds (configurable via env vars)
THRESHOLD_TRUNCATE = int(os.environ.get("DIFFER_THRESHOLD_TRUNCATE", "100000"))
THRESHOLD_LARGE_MODEL = int(os.environ.get("DIFFER_THRESHOLD_LARGE", "180000"))

# Budget caps per model tier (USD)
BUDGET_SONNET = 2.00
BUDGET_SONNET_1M = 8.00

# Truncation limits (lines per page in workspace)
TRUNCATE_NORMAL = 500
TRUNCATE_AGGRESSIVE = 200


@dataclass
class ModelSelection:
    """Result of dynamic model selection."""

    model: str
    budget: float
    max_page_lines: int
    estimated_tokens: int
    reason: str


def estimate_workspace_tokens(
    repo_dir: Path,
    report: DiffReport,
    full_diff: str,
    max_page_lines: int = TRUNCATE_NORMAL,
) -> int:
    """Estimate total tokens Claude will process for changelog generation.

    Approximates the workspace content:
    - Full diff text (usually the dominant factor)
    - New and modified page content (truncated to max_page_lines)
    - Metadata (summary JSON, report markdown, URL manifest, triage)
    - Prompt overhead (system prompt + user prompt + formatting)

    Args:
        repo_dir: Repository root directory
        report: DiffReport with change details
        full_diff: Full unified diff text
        max_page_lines: Lines-per-page truncation limit for estimation

    Returns:
        Estimated total token count
    """
    # 1. Diff tokens
    diff_tokens = len(full_diff.encode("utf-8")) // BYTES_PER_TOKEN

    # 2. Page content tokens (new + modified, truncated)
    page_tokens = 0
    page_paths = list(report.new_pages) + [c.path for c in report.page_changes]
    for page_path in page_paths:
        full_path = repo_dir / page_path
        if not full_path.exists():
            continue
        try:
            content = full_path.read_text(errors="replace")
        except OSError:
            continue
        lines = content.split("\n")
        if len(lines) > max_page_lines:
            content = "\n".join(lines[:max_page_lines])
        page_tokens += len(content.encode("utf-8")) // BYTES_PER_TOKEN

    # 3. Metadata tokens (summary JSON, report.md, url_manifest, triage)
    # Estimate as ~3x the summary JSON size
    report_json = json.dumps(report.to_dict())
    metadata_tokens = (len(report_json.encode("utf-8")) // BYTES_PER_TOKEN) * 3

    return diff_tokens + page_tokens + metadata_tokens + PROMPT_OVERHEAD_TOKENS


def select_model(
    estimated_tokens: int,
    explicit_model: str | None = None,
    explicit_budget: float | None = None,
) -> ModelSelection:
    """Select model, budget, and truncation level based on estimated tokens.

    Tiers:
    - < 100k tokens: sonnet, 500 lines/page, $2.00
    - 100k-180k tokens: sonnet, 200 lines/page (aggressive truncation), $2.00
    - > 180k tokens: sonnet[1m], 500 lines/page, $8.00

    When explicit_model is set (and not "auto"), it takes precedence.
    When explicit_budget is set, it overrides the tier default.

    Args:
        estimated_tokens: Estimated total workspace tokens
        explicit_model: User-specified model (bypasses auto when not "auto"/None)
        explicit_budget: User-specified budget override

    Returns:
        ModelSelection with resolved model, budget, truncation, and reasoning
    """
    if explicit_model and explicit_model != "auto":
        budget = explicit_budget if explicit_budget is not None else BUDGET_SONNET
        return ModelSelection(
            model=explicit_model,
            budget=budget,
            max_page_lines=TRUNCATE_NORMAL,
            estimated_tokens=estimated_tokens,
            reason=f"explicit: {explicit_model}",
        )

    if estimated_tokens > THRESHOLD_LARGE_MODEL:
        budget = explicit_budget if explicit_budget is not None else BUDGET_SONNET_1M
        return ModelSelection(
            model="sonnet[1m]",
            budget=budget,
            max_page_lines=TRUNCATE_NORMAL,
            estimated_tokens=estimated_tokens,
            reason=(
                f"{estimated_tokens:,} tokens > {THRESHOLD_LARGE_MODEL:,} "
                f"-> extended context"
            ),
        )

    if estimated_tokens > THRESHOLD_TRUNCATE:
        budget = explicit_budget if explicit_budget is not None else BUDGET_SONNET
        return ModelSelection(
            model="sonnet",
            budget=budget,
            max_page_lines=TRUNCATE_AGGRESSIVE,
            estimated_tokens=estimated_tokens,
            reason=(
                f"{estimated_tokens:,} tokens > {THRESHOLD_TRUNCATE:,} "
                f"-> sonnet + aggressive truncation ({TRUNCATE_AGGRESSIVE} lines/page)"
            ),
        )

    budget = explicit_budget if explicit_budget is not None else BUDGET_SONNET
    return ModelSelection(
        model="sonnet",
        budget=budget,
        max_page_lines=TRUNCATE_NORMAL,
        estimated_tokens=estimated_tokens,
        reason=f"{estimated_tokens:,} tokens -> standard sonnet",
    )
