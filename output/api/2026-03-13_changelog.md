# Claude API Documentation Changes — 2026-03-13

## Summary

This update's primary change is a terminology shift in the Agent SDK documentation: "plugin commands" are now called "plugin skills," with `commands/` designated as a legacy format in favor of `skills/`. Several other pages received minor updates including a cosmetic fix in the models table, consolidation of streaming refusals guidance, and a rate limits note about Sonnet 4.6.

## Significant Changes

### Agent SDK

- **Plugin "commands" renamed to "skills"**: The Agent SDK plugins documentation has been updated throughout to replace "commands" terminology with "skills." The section previously titled "Using plugin commands" is now "Using plugin skills," code comments updated accordingly, and the troubleshooting section "Commands not available" is now "Skills not appearing."
  > "Skills from plugins are automatically namespaced with the plugin name to avoid conflicts. When invoked as slash commands, the format is `plugin-name:skill-name`."
  - *Implication*: This is a documentation alignment change, not a breaking API change — the underlying behavior is the same. However, the `commands/` plugin directory is now explicitly marked as a legacy format; developers building new plugins should use `skills/` instead.
  - *Source*: [Plugins in the SDK](https://platform.claude.com/docs/en/agent-sdk/plugins.md)

- **`commands/` directory marked as legacy in plugin structure**: A new note has been added to the plugin structure reference making the deprecation explicit:
  > "The `commands/` directory is a legacy format. Use `skills/` for new plugins. Claude Code continues to support both formats for backward compatibility."
  - The plugin directory structure now shows `skills/` as the primary location for agent capabilities with a note that `commands/` is "Legacy: use skills/ instead."
  - *Source*: [Plugins in the SDK](https://platform.claude.com/docs/en/agent-sdk/plugins.md)

- **Slash commands documentation updated with skills migration note**: The slash commands page now includes a note indicating that `.claude/commands/` is a legacy format:
  > "The `.claude/commands/` directory is the legacy format. The recommended format is `.claude/skills/<name>/SKILL.md`, which supports the same slash-command invocation (`/name`) plus autonomous invocation by Claude. See Skills for the current format."
  - The file locations section now labels both project commands (`.claude/commands/`) and personal commands (`~/.claude/commands/`) with "(legacy; prefer `.claude/skills/`)" notes.
  - *Source*: [Slash Commands in the SDK](https://platform.claude.com/docs/en/agent-sdk/slash-commands.md)

### Models

- **Claude Haiku 3 API alias display fix**: In the legacy models comparison table, the API alias column for Claude Haiku 3 (deprecated) changed from `—` (em dash) to `N/A`.
  - *Implication*: Cosmetic/display fix only. No functional change.
  - *Source*: [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

### Streaming Refusals

- **Simplified streaming refusals page**: The handle-streaming-refusals page had a net reduction of 4 lines (+1/-5), indicating some content was consolidated or removed. The current page retains a Tip noting that developers who encounter frequent `refusal` stop reasons with Sonnet 4.5 or Opus 4.1 can try falling back to Sonnet 4 (`claude-sonnet-4-20250514`), which has different usage restrictions.
  - *Source*: [Streaming refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md)

## Notable Details

- **Release notes reformatting** (`+44/-44` lines): The release notes page shows equal additions and deletions at a large scale, indicating significant reformatting of existing content rather than new entries. The most recent entry remains February 19, 2026 (automatic caching launch, Sonnet 3.7 and Haiku 3.5 retirement, Haiku 3 deprecation announcement). No new release notes entries were added.

- **Rate limits — Sonnet 4.6 added to long context section**: The long context rate limits section now reads "When using Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5, or Sonnet 4" — Sonnet 4.6 was added to the list of models eligible for the 1M token context window with dedicated rate limits.
  - *Source*: [Rate limits](https://platform.claude.com/docs/en/api/rate-limits.md)

- **PDF support and build overview**: Both pages received minor 2-line updates, likely model ID updates within code examples (e.g., referencing `claude-opus-4-6` in sample requests). No functional documentation changes.

- **`whats-new-claude-4-6.md`**: Minor 2-line update (+2/-2); no section additions or removals. Likely a wording refinement within an existing section.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| agent-sdk/plugins.md | Modified | +22/-19 | Renamed "commands" to "skills" throughout; marked `commands/` directory as legacy format |
| agent-sdk/slash-commands.md | Modified | +6/-2 | Added notes that `.claude/commands/` is legacy; recommend migrating to `.claude/skills/` |
| release-notes/overview.md | Modified | +44/-44 | Reformatting of existing content; no new entries added |
| test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md | Modified | +1/-5 | Consolidated content; net 4 lines removed |
| about-claude/models/whats-new-claude-4-6.md | Modified | +2/-2 | Minor wording update |
| build-with-claude/pdf-support.md | Modified | +2/-2 | Minor update, likely model reference |
| api/rate-limits.md | Modified | +1/-1 | Added Sonnet 4.6 to long context rate limits model list |
| build-with-claude/overview.md | Modified | +1/-1 | Minor update |
| about-claude/models/overview.md | Modified | +1/-1 | Changed "—" to "N/A" for Haiku 3 API alias in legacy table |

---
*Generated from Claude API documentation changes detected on 2026-03-13*
