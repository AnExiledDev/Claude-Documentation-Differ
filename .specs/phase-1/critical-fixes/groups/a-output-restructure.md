---
group: A
title: Output restructure (1.1 + 2.4 atomic)
files:
  - diff.py
  - .github/workflows/doc-differ.yml
  - .github/workflows/api-differ.yml
---

## Acceptance Criteria

- [ ] Output path for changelogs uses date subdirectory: `output/{source}/{YYYY-MM-DD}/partial_{HH}h_changelog.md`
- [ ] Output path for diff reports uses date subdirectory: `output/{source}/{YYYY-MM-DD}/diff.md`
- [ ] Category changelogs (API split) write to: `output/{source}/{YYYY-MM-DD}/{cat_key}_changelog.md`
- [ ] Master changelog (API split) writes to: `output/{source}/{YYYY-MM-DD}/changelog.md`
- [ ] `output/{source}/index.md` auto-generated after each changelog write, listing all date dirs newest-first
- [ ] Workflow summary steps updated to find changelogs in date subdirs
- [ ] `--force` flag correctly overwrites partials within date subdirs
- [ ] Date subdir created automatically (parents=True) before writing
