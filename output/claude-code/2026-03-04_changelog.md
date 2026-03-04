# Claude Code Documentation Changes — 2026-03-04

## Summary

The primary change is expansion of effort level support to Sonnet 4.6 (previously Opus 4.6 only), with coordinated updates across three pages. A new official changelog page (`changelog.md`) was also added, surfacing the Claude Code GitHub CHANGELOG.md as a documentation page for the first time.

## Significant Changes

### Model Configuration

- **Effort levels extended to Sonnet 4.6**: The `CLAUDE_CODE_EFFORT_LEVEL` environment variable and `/model` effort slider now apply to both Opus 4.6 and Sonnet 4.6, not just Opus 4.6. The description has been generalized from model-specific language to apply broadly.

  > "Effort is supported on Opus 4.6 and Sonnet 4.6. The effort slider appears in `/model` when a supported model is selected."

  Previously: `"Effort is currently supported on Opus 4.6."`

  - *Implication*: Developers using Sonnet 4.6 can now tune thinking depth via `CLAUDE_CODE_EFFORT_LEVEL=low|medium|high` or the `/model` picker.
  - *Source*: [model-config.md](https://code.claude.com/docs/en/model-config.md)

- **`high` effort is no longer documented as the default**: All three modified pages previously described `high` as the default effort level (e.g., `"low, medium, high (default)"`). The `"(default)"` annotation has been removed from every occurrence.

  > "Three levels are available: **low**, **medium**, and **high**."

  Previously: `"Three levels are available: **low**, **medium**, and **high** (default)."`

  - *Implication*: This aligns documentation with the v2.1.68 changelog entry stating "Opus 4.6 now defaults to medium effort for Max and Team subscribers." Developers relying on default high effort should verify their settings.
  - *Source*: [model-config.md](https://code.claude.com/docs/en/model-config.md), [settings.md](https://code.claude.com/docs/en/settings.md), [common-workflows.md](https://code.claude.com/docs/en/common-workflows.md)

## New Pages

- **changelog.md** — The official Claude Code GitHub `CHANGELOG.md` is now published as a documentation page. It covers all release notes from v2.1.68 back through earlier versions, including features, bug fixes, and platform-specific changes. [View](https://code.claude.com/docs/en/changelog.md)

## Notable Details

- The `CLAUDE_CODE_EFFORT_LEVEL` env var documentation in `settings.md` dropped both `"(default)"` from the `high` value and the phrase `"Currently supported with Opus 4.6 only"` in a single line change — a concise indication that the default and supported model set both changed simultaneously.
- The common-workflows.md table entry for effort level also removed the word "default" and added Sonnet 4.6 as a supported model in its description field, making all three pages consistent.
- The metadata indicates yesterday's run had 1 failed page fetch (out of 58 successful); today's run shows 59/59 successful — the new `changelog.md` was the previously-failing page now successfully fetched.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | New | +1550 | Official Claude Code release changelog, covering v2.1.10 through v2.1.68 |
| model-config.md | Modified | +3/-3 | Effort levels extended to Sonnet 4.6; "high" no longer marked as default |
| common-workflows.md | Modified | +1/-1 | Effort level table updated to include Sonnet 4.6 and drop "default" label |
| settings.md | Modified | +1/-1 | `CLAUDE_CODE_EFFORT_LEVEL` env var updated for Sonnet 4.6 support and no default |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-04*
