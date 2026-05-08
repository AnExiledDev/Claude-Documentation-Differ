---
group: c
title: Daily Merge Workflow
issue: "2.1"
parallel: true
depends_on: []
files:
  - merge_daily.py (create)
  - lib/prompts/daily_merge.md (create)
  - .github/workflows/daily-merge.yml (create)
---

## Acceptance Criteria

- [x] `merge_daily.py` CLI script: `--source`, `--date` (default: today UTC), `--model` (default: sonnet), `--budget`, `--force` flags
- [x] Globs `output/{source}/{date}/partial_*_changelog.md` for partials
- [x] Empty-partials guard: zero partials → prints message, exits 0, writes nothing
- [x] When partials exist: reads all, feeds to Claude with `daily_merge.md` prompt, writes `daily.md` in same date subdir
- [x] Existing `daily.md` not overwritten unless `--force` passed
- [x] Regenerates `output/{source}/index.md` after writing `daily.md`
- [x] `lib/prompts/daily_merge.md` instructs Claude to synthesize partials into coherent daily changelog: deduplicate, prioritize significant changes, preserve source URLs
- [x] `.github/workflows/daily-merge.yml` runs at 23:55 UTC daily
- [x] Workflow processes both sources (claude-code and api) sequentially
- [x] Workflow uses `CLAUDE_CODE_OAUTH_TOKEN` secret for auth
- [x] Workflow has its own concurrency group (`daily-merge`)
- [x] Workflow commits and pushes `daily.md` with message: `"Add {source_name} daily changelog for YYYY-MM-DD"`
- [x] Workflow handles zero-change days gracefully (no failure, no empty commits)
