---
title: "Phase 1: Critical Fixes — AI Context"
---

# AI Implementation Context

## Invariants

- Output paths MUST use date subdirectories: `output/{source.key}/{YYYY-MM-DD}/`
- Partial changelogs MUST include hour: `partial_{HH}h_changelog.md`
- Category changelogs (API split): `{cat_key}_changelog.md` inside date subdir
- Diff reports: `diff.md` inside date subdir
- `_run_git()` MUST check returncode by default
- `get_last_changelog_commit()` MUST use source_name in its grep pattern
- Workflow commit messages MUST include source name + hour

## Anti-patterns

- Do NOT change `_run_git()` callers that already handle empty output correctly — just add the check param
- Do NOT migrate existing flat output files — new code writes to new paths, old files stay
- Do NOT break backward compat for `--since-last-changelog` — grep must match old `"Add.*changelog"` AND new `"Add.*{source}.*changelog"` patterns
- Do NOT touch the "Push metadata-only update" workflow steps — they're unrelated to Phase 1

## Key Code Locations

### Issue 1.1 + 2.4 — Output restructure
- `diff.py:454` — `date_str` used for flat filename, needs date subdir
- `diff.py:493` — same for `--changelog` path
- `diff.py:335-336` — category changelog filename (already has `{date_str}_{cat_key}_changelog.md`)
- `diff.py:364` — master changelog path
- `diff.py:455` — `base_name` for diff report
- Workflow summary steps: `doc-differ.yml:127`, `api-differ.yml:128` — `ls output/{source}/*_changelog.md`
- Workflow git add: `doc-differ.yml:98`, `api-differ.yml:99` — `git add output/{source}/ || true`

### Issue 1.2 — _run_git
- `lib/differ.py:151-159` — the function itself
- Callers: `lib/differ.py:226-234` (analyze_changes), `lib/differ.py:263-264` (file_diff), `lib/differ.py:329` (get_full_diff)

### Issue 1.3 — Commit messages + grep
- `lib/differ.py:350-365` — `get_last_changelog_commit()`, grep is `"Add.*changelog"` (ignores source_name)
- `diff.py:581` — callsite passes `"changelog"` not source name
- `doc-differ.yml:99` — commit message `"Add changelog for $(date)"`
- `api-differ.yml:100` — same

## Index Generation

Auto-generate `output/{source}/index.md` after writing any changelog.
Format: sorted date list (newest first) with links to `daily.md` (when it exists, Phase 2) or partials.
Keep it simple — this is a machine-generated TOC, not a human-curated doc.

## Workflow Glob Updates

After restructure, the summary step needs to find changelogs inside date subdirs:
```bash
# Old
CHANGELOG=$(ls output/claude-code/*_changelog.md 2>/dev/null | head -1)
# New — find today's partial
TODAY=$(date -u +%Y-%m-%d)
CHANGELOG=$(ls output/claude-code/$TODAY/partial_*_changelog.md 2>/dev/null | tail -1)
```

The `git add` already uses `output/{source}/` which covers subdirs — no change needed there.
