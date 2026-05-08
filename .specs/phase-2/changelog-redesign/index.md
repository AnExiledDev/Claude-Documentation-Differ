---
approval: approved
created: 2026-05-08
phase: 2
title: Changelog Redesign
---

# Phase 2: Changelog Redesign

## Intent

Upgrade changelog generation from flat, overwrite-prone output to a structured pipeline with rule-based triage, enhanced AI prompts, and end-of-day synthesis. This builds on Phase 1's date-subdirectory layout.

## Scope

**In scope:**
- Issue 2.1: Daily merge workflow (AI-synthesized `daily.md`)
- Issue 2.2: Hybrid triage system (rule-based `triage.json` → AI reads it)
- Issue 2.3: Enhanced changelog prompts (structured output, triage awareness)

**Out of scope:**
- Issue 2.4: Already shipped in Phase 1 (date subdirectories)
- Commit squashing (Phase 3, issue 3.5)
- Dynamic model selection (Phase 4)
- Workflow consolidation (Phase 3)

## Decisions

### Already Decided (from ISSUES.md)
- Triage model: hybrid — rules write `triage.json`, AI reads and can override
- Triage rules: new/removed pages = SIGNIFICANT, heading changes = SIGNIFICANT, >50 lines = SIGNIFICANT, <5 lines = MINOR, metadata.json only = SKIP
- Triage JSON schema: `{"changes": [{"path", "classification", "reason", "additions", "deletions"}]}`
- Daily merge: separate workflow at ~23:55 UTC, reads partials, writes `daily.md`
- Empty-partials guard: no partials → exit 0, no empty `daily.md`
- Group ordering: 2.2 (triage) must complete before 2.3 (prompts)

### Decided Here
- Merge script: `merge_daily.py` at project root (consistent with `fetch.py`, `diff.py`)
- One shared merge prompt: `lib/prompts/daily_merge.md` (partials already source-specific)
- Triage module: `lib/triage.py`

## Groups

| Group | Issue | Summary | Dependencies |
|-------|-------|---------|--------------|
| A | 2.2 | Triage system — `lib/triage.py` + workspace integration | None |
| B | 2.3 | Enhanced prompts — structured output + triage awareness | A |
| C | 2.1 | Daily merge workflow + script + prompt | None |

A and C are parallel. B depends on A.

## Risks

1. **Daily merge auth/cost**: Same Claude CLI auth pattern as existing workflows. Mitigated by budget cap.
2. **Triage false positives**: Rule thresholds may miscategorize. Mitigated by AI override capability.
3. **Empty-partials edge cases**: Date subdir exists but contains only `diff.md` and no partials. Merge script must glob specifically for `partial_*_changelog.md`.

## Testing Strategy

- Triage module: unit-testable pure functions (Phase 6 adds formal tests; manual verification here)
- Prompts: verify by inspecting workspace output after a dry run
- Daily merge: verify empty-partials guard with manual test (no partials → clean exit)

## Rollback

All changes are additive. Existing partial changelog generation is unchanged. Daily merge is a new workflow that can be disabled by removing the file. Triage is integrated into workspace prep but doesn't block changelog generation if absent.
