# Claude Code Documentation Changes — 2026-05-11

## Summary

Two pages were modified, both related to skill listing budget controls. The changes document two new settings — `skillListingBudgetFraction` and `maxSkillDescriptionChars` — and update the skill troubleshooting guide to reflect the new configuration options and improved overflow behavior introduced in Claude Code v2.1.105.

## Significant Changes

### Configuration

- **New setting: `skillListingBudgetFraction`**: Controls what fraction of the model's context window is reserved for the skill listing Claude sees each turn. Default is `0.01` (1%). When the listing overflows the budget, descriptions for least-used skills are collapsed to bare names rather than truncated uniformly.
  > `skillListingBudgetFraction` — Fraction of the model's context window reserved for the skill listing Claude sees each turn (default: `0.01` = 1%). When the listing exceeds the budget, descriptions for the least-used skills are collapsed to bare names so Claude can still invoke them but won't see why. Raise to keep more descriptions visible at the cost of more context per turn. `/doctor` shows the current truncation count and which skills are affected. Requires Claude Code v2.1.105 or later.
  - *Implication*: Developers with many skills who want to tune context consumption now have a settings-based alternative to the `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable. The `0.02` example value in the docs doubles the default budget.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **New setting: `maxSkillDescriptionChars`**: Adds a per-skill character cap on the combined `description` and `when_to_use` text (default: `1536`). Previously this cap was hardcoded and undocumented.
  > `maxSkillDescriptionChars` — Per-skill character cap on the combined `description` and `when_to_use` text in the skill listing Claude sees each turn (default: `1536`). Text longer than this is truncated. Raise to keep long descriptions intact at the cost of more context per turn; lower to fit more skills under `skillListingBudgetFraction`. Requires Claude Code v2.1.105 or later.
  - *Implication*: The 1,536-character cap was previously implicit and only discoverable via source. Making it configurable allows developers to either relax the cap for information-dense skills or tighten it to fit more skills in budget.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Skills

- **Skill description overflow behavior clarified and updated**: The "Skill descriptions are cut short" troubleshooting section was rewritten to reflect smarter overflow handling and the new settings-based controls.

  Previous text described a fixed "fallback of 8,000 characters" and instructed users to set the `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable to raise the limit. The updated text:
  - Removes the 8,000-character fallback reference (replaced by the dynamic budget model)
  - Clarifies that overflow drops descriptions for the *least-used* skills first, preserving descriptions for frequently invoked skills
  - Adds `/doctor` as a diagnostic tool for checking budget overflow and identifying affected skills
  - Points to `skillListingBudgetFraction` as the preferred settings-based control, with `SLASH_COMMAND_TOOL_CHAR_BUDGET` now described as setting "a fixed character count" (an alternative, not the primary path)
  - Notes that the per-skill cap of 1,536 characters is configurable via `maxSkillDescriptionChars`

  > The budget scales at 1% of the model's context window. When it overflows, descriptions for the skills you invoke least are dropped first, so the skills you actually use keep their full text. Run `/doctor` to see whether the budget is overflowing and which skills are affected.
  - *Implication*: Users with large skill collections should use `/doctor` first before manually tuning env vars or settings. The least-recently-used pruning means high-frequency skills are less likely to be silently degraded.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

## Notable Details

- Both new settings (`skillListingBudgetFraction` and `maxSkillDescriptionChars`) carry a `min-version: 2.1.105` annotation in the source, meaning they are silently ignored on older installations.
- The `skillListingBudgetFraction` setting interacts with `skillOverrides`: setting low-priority skills to `"name-only"` remains the recommended way to free budget without raising the fraction.
- The removal of the "fallback of 8,000 characters" language signals that the dynamic 1%-of-context-window model is now the sole budget mechanism; there is no longer a static floor.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| settings.md | Modified | +2 / -0 | Added `maxSkillDescriptionChars` and `skillListingBudgetFraction` settings entries |
| skills.md | Modified | +2 / -2 | Rewrote skill description budget overflow section; added `/doctor` guidance and links to new settings |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-11*
