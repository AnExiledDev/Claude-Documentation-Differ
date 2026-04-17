# Claude Code Documentation Changes — 2026-04-17

## Summary

Two pages were modified with small but meaningful content changes. The `model-config` page gains a clarification on context window limits for the `opusplan` alias. The `routines` page removes the "From fork" PR filter field and its associated example.

## Significant Changes

### Model Configuration

- **`opusplan` context window clarified**: New text explicitly states that the plan-mode Opus phase in `opusplan` runs with the standard 200K context window, and that the automatic 1M context upgrade does **not** apply to `opusplan` — only to the bare `opus` model setting.
  > The plan-mode Opus phase runs with the standard 200K context window. The automatic 1M upgrade described in [Extended context](#extended-context) applies to the `opus` model setting and does not extend to `opusplan`.
  - *Implication*: Developers relying on the 1M token extended context window for large codebases should use the `opus` model setting directly rather than `opusplan`.
  - *Source*: [Model Configuration](https://code.claude.com/docs/en/model-config.md)

### Routines / PR Filters

- **"From fork" PR filter removed**: The `From fork` row has been removed from the PR filter fields table, and the "External contributor triage" example (which demonstrated routing fork-based PRs through extra security review) has also been removed.
  - *Implication*: Fork-based PR filtering is no longer a documented filter condition in routines. Teams that were routing external contributions via this filter will need an alternative approach (e.g., label-based gates or branch-naming conventions).
  - *Source*: [Routines](https://code.claude.com/docs/en/routines.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| model-config.md | Modified | +2 / -0 | Added context window clarification for `opusplan` alias |
| routines.md | Modified | +0 / -2 | Removed `From fork` PR filter field and its associated example |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-17*
