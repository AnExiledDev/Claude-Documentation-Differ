---
group: C
title: Source-specific commit messages + fix get_last_changelog_commit (1.3)
files:
  - diff.py
  - lib/differ.py
  - .github/workflows/doc-differ.yml
  - .github/workflows/api-differ.yml
---

## Acceptance Criteria

- [ ] `doc-differ.yml` commit message: `"Add Claude Code changelog for YYYY-MM-DD (HHh)"`
- [ ] `api-differ.yml` commit message: `"Add API changelog for YYYY-MM-DD"`
- [ ] `get_last_changelog_commit()` uses `source_name` in grep pattern: `f"Add.*{source_name}.*changelog"`
- [ ] Grep pattern also matches old format `"Add.*changelog"` for backward compat during transition
- [ ] Callsite at `diff.py:581` passes source display name (e.g., `"Claude Code"`, `"API"`) instead of `"changelog"`
