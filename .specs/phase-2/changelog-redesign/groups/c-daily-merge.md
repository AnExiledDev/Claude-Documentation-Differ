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

- [ ] `merge_daily.py` CLI script: `--source`, `--date` (default: today UTC), `--model` (default: sonnet), `--budget`, `--force` flags
- [ ] Globs `output/{source}/{date}/partial_*_changelog.md` for partials
- [ ] Empty-partials guard: zero partials → prints message, exits 0, writes nothing
- [ ] When partials exist: reads all, feeds to Claude with `daily_merge.md` prompt, writes `daily.md` in same date subdir
- [ ] Existing `daily.md` not overwritten unless `--force` passed
- [ ] Regenerates `output/{source}/index.md` after writing `daily.md`
- [ ] `lib/prompts/daily_merge.md` instructs Claude to synthesize partials into coherent daily changelog: deduplicate, prioritize significant changes, preserve source URLs
- [ ] `.github/workflows/daily-merge.yml` runs at 23:55 UTC daily
- [ ] Workflow processes both sources (claude-code and api) sequentially
- [ ] Workflow uses `CLAUDE_CODE_OAUTH_TOKEN` secret for auth
- [ ] Workflow has its own concurrency group (`daily-merge`)
- [ ] Workflow commits and pushes `daily.md` with message: `"Add {source_name} daily changelog for YYYY-MM-DD"`
- [ ] Workflow handles zero-change days gracefully (no failure, no empty commits)
