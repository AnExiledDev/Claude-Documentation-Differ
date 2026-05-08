---
group: a
title: Hybrid Triage System
issue: "2.2"
parallel: true
depends_on: []
files:
  - lib/triage.py (create)
  - diff.py (modify _prepare_changelog_workspace)
---

## Acceptance Criteria

- [ ] `lib/triage.py` exports `classify_changes(report: DiffReport, source_key: str) -> dict` returning triage JSON structure
- [ ] Classification rules applied in priority order: new_page, removed_page, heading_change, line_count>50, line_count<5, default SIGNIFICANT
- [ ] Each change entry includes: path, classification (SIGNIFICANT|MINOR|SKIP), reason, additions, deletions
- [ ] New pages classified as SIGNIFICANT with reason `"rule: new_page"`
- [ ] Removed pages classified as SIGNIFICANT with reason `"rule: removed_page"`
- [ ] Pages with heading changes (new_sections or removed_sections non-empty) classified as SIGNIFICANT
- [ ] Pages with >50 total line changes classified as SIGNIFICANT
- [ ] Pages with <5 total line changes classified as MINOR
- [ ] Default classification is SIGNIFICANT (conservative — AI can downgrade)
- [ ] `_prepare_changelog_workspace()` in `diff.py` calls `classify_changes()` and writes `triage.json` to workspace dir
- [ ] Triage failure (exception) is caught and logged — does not block changelog generation
