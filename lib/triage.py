"""Rule-based triage of documentation changes by significance."""

from __future__ import annotations

from datetime import datetime, timezone

from lib.differ import DiffReport


def classify_changes(report: DiffReport, source_key: str) -> dict:
    """Classify each change in a DiffReport by significance.

    Returns a triage dict with source, date, and per-change classifications.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    changes = []

    for path in report.new_pages:
        changes.append({
            "path": path,
            "classification": "SIGNIFICANT",
            "reason": "rule: new_page",
            "additions": 0,
            "deletions": 0,
        })

    for path in report.removed_pages:
        changes.append({
            "path": path,
            "classification": "SIGNIFICANT",
            "reason": "rule: removed_page",
            "additions": 0,
            "deletions": 0,
        })

    for page in report.page_changes:
        total_lines = page.additions + page.deletions

        if page.new_sections or page.removed_sections:
            classification = "SIGNIFICANT"
            reason = "rule: heading_change"
        elif total_lines > 50:
            classification = "SIGNIFICANT"
            reason = "rule: line_count>50"
        elif total_lines < 5:
            classification = "MINOR"
            reason = "rule: line_count<5"
        else:
            classification = "SIGNIFICANT"
            reason = "rule: default"

        changes.append({
            "path": page.path,
            "classification": classification,
            "reason": reason,
            "additions": page.additions,
            "deletions": page.deletions,
        })

    return {
        "source": source_key,
        "date": today,
        "changes": changes,
    }
