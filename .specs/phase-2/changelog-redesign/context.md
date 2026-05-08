---
title: Phase 2 AI Context
---

# AI Implementation Context

## Invariants

1. **Triage before prompts**: `lib/triage.py` and its workspace integration must be complete before prompt files are updated. The prompts reference `triage.json` — it must exist.
2. **Empty-partials guard**: The daily merge MUST exit 0 with no output when no `partial_*_changelog.md` files exist. Never create an empty `daily.md`. Never fail.
3. **triage.json is workspace-only**: Written to `.changelog_workspace/triage.json`. Never committed. Cleaned up with the rest of the workspace after generation.
4. **Backward compatibility**: Old commits without triage.json must still work — prompts should say "if triage.json exists, use it" not "read triage.json" as a hard requirement.
5. **Source-agnostic triage**: Rules apply to both claude-code and api sources identically. No source-specific logic in `lib/triage.py`.

## Anti-Patterns to Avoid

- Do NOT add triage as a hard dependency for changelog generation. If triage fails or is absent, changelog generation proceeds without it.
- Do NOT create daily.md from scratch — it must synthesize actual partial content. If there's nothing to synthesize, write nothing.
- Do NOT add squashing logic to the daily merge workflow (that's Phase 3).
- Do NOT modify the existing per-run changelog generation flow in `_process_source()`. Triage integrates into `_prepare_changelog_workspace()` only.
- Do NOT create per-source merge prompts. One shared `lib/prompts/daily_merge.md`.

## Key File Locations

| File | Role | Status |
|------|------|--------|
| `diff.py:128-194` | `_prepare_changelog_workspace()` — add triage.json here | Modify |
| `lib/differ.py:18-27` | `PageChange` dataclass — has `additions`, `deletions`, `new_sections`, `removed_sections` | Read-only (triage uses these fields) |
| `lib/prompts/claude_code.md` | Claude Code prompt — add triage + structured output | Modify |
| `lib/prompts/api.md` | API prompt — add triage + structured output | Modify |
| `lib/triage.py` | New triage module | Create |
| `merge_daily.py` | New daily merge CLI script | Create |
| `lib/prompts/daily_merge.md` | New daily merge synthesis prompt | Create |
| `.github/workflows/daily-merge.yml` | New daily merge workflow | Create |
| `sources.py` | Source config — read-only, used by merge script | Read-only |

## Triage JSON Schema

```json
{
  "source": "claude-code",
  "date": "2026-05-08",
  "changes": [
    {
      "path": "docs/claude-code/en/hooks.md",
      "classification": "SIGNIFICANT",
      "reason": "rule: heading_change",
      "additions": 25,
      "deletions": 3
    },
    {
      "path": "docs/claude-code/en/settings.md",
      "classification": "MINOR",
      "reason": "rule: line_count<5",
      "additions": 2,
      "deletions": 1
    }
  ]
}
```

## Triage Classification Rules (in priority order)

1. New page (in `report.new_pages`) → SIGNIFICANT, reason: `"rule: new_page"`
2. Removed page (in `report.removed_pages`) → SIGNIFICANT, reason: `"rule: removed_page"`
3. Has heading changes (`new_sections` or `removed_sections` non-empty) → SIGNIFICANT, reason: `"rule: heading_change"`
4. Total line changes (additions + deletions) > 50 → SIGNIFICANT, reason: `"rule: line_count>50"`
5. Total line changes < 5 → MINOR, reason: `"rule: line_count<5"`
6. Everything else → SIGNIFICANT (default to significant; AI can downgrade)

## Daily Merge Script Design

- CLI: `python3 merge_daily.py --source claude-code [--date 2026-05-08] [--model sonnet] [--budget N] [--force]`
- Default date: today (UTC)
- Glob: `output/{source}/{date}/partial_*_changelog.md`
- If zero partials found → print message, exit 0
- If partials found → feed them to Claude with `daily_merge.md` prompt → write `daily.md`
- Regenerate `output/{source}/index.md` after writing

## Workflow Schedule

- `daily-merge.yml` runs at 23:55 UTC
- Runs for both sources (claude-code and api) sequentially
- Uses same auth pattern: `CLAUDE_CODE_OAUTH_TOKEN` secret
- Concurrency group: `daily-merge` (separate from source workflows for now; shared group deferred to Phase 3)
