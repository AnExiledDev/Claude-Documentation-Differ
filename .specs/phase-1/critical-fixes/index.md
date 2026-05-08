---
title: "Phase 1: Critical Fixes"
approval: approved
created: 2026-05-08
---

# Phase 1: Critical Fixes

Fixes data loss from changelog overwrites, silent git failures, and ambiguous commit messages that break `--since-last-changelog`.

## Scope

**In scope:** Issues 1.1, 1.2, 1.3, 2.4 (from ISSUES.md)
**Out of scope:** Migration of existing 286 flat output files into date subdirectories (cosmetic, not blocking)

## Already Decided

- Output layout: `output/{source}/{YYYY-MM-DD}/partial_{HH}h_changelog.md` (ISSUES.md)
- Issues 1.1 + 2.4 ship as one atomic change (architectural constraint)
- Issue 1.3 must fix both commit messages AND the `get_last_changelog_commit()` grep (architectural constraint)
- Auto-generated `index.md` per source as TOC

## Needs Your Input

1. **Existing file migration**: Skip moving 286 old flat files into date subdirs? They're already committed, moving is cosmetic and creates a large diff. New runs will use the new layout regardless.
2. **Backward compat for grep**: Old commits say `"Add changelog for YYYY-MM-DD"`. New format will be `"Add Claude Code changelog for YYYY-MM-DD (HHh)"`. The grep in `get_last_changelog_commit()` should match BOTH old and new formats during transition. Agreed?

## Groups

| Group | Description | Files |
|-------|-------------|-------|
| A: Output restructure | Date subdirs, partial filenames, index generation, workflow globs | `diff.py`, both `.yml` |
| B: Git error handling | `_run_git()` returncode checking | `lib/differ.py` |
| C: Commit messages | Source-specific messages + fix dead `source_name` param | `diff.py`, `lib/differ.py`, both `.yml` |

## Risks

- Workflow glob changes can't be CI-tested locally; one wrong pattern = broken workflow
- Grep backward compat: must match old AND new commit message formats
