# Claude Code Documentation Changes — 2026-05-04

## Summary

Five pages were updated with no new or removed pages. The most substantive changes clarify the security boundaries of the `autoMemoryDirectory` setting (now restricted from project and local settings files) and expand the documentation on how hook `ok: false` responses behave differently across event types. One npm update command was corrected.

## Significant Changes

### Hooks

- **`ok: false` behavior now differs by hook event type**: The docs previously stated that returning `"ok": false` from an LLM hook feeds the `reason` back to Claude so it can adjust. This has been corrected to distinguish two behaviors:
  > For `Stop` and `SubagentStop`, an `ok: false` reason is fed back to Claude as its next instruction and the turn continues. For all other supported events, the turn ends and the reason appears in the chat as a warning line; Claude does not see it. This is equivalent to returning `"continue": false` from a command hook.
  - *Implication*: Developers building LLM-type hooks for non-Stop events (e.g., `PreToolUse`, `PostToolUse`) should not expect Claude to react to the `reason` string — it is user-visible only. Only `Stop` and `SubagentStop` hooks continue the turn and pass the reason as Claude's next instruction.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md), [hooks-guide.md](https://code.claude.com/docs/en/hooks-guide.md)

### Configuration

- **`autoMemoryDirectory` restricted from project and local settings (security)**: The setting can no longer be loaded from `.claude/settings.json` (project) or local settings files. The accepted sources are now policy settings, user settings (`~/.claude/settings.json`), and the `--settings` flag.
  > Not accepted from project or local settings, since a cloned repository could supply either file to redirect memory writes to sensitive locations.
  - *Implication*: If you previously set `autoMemoryDirectory` in a project's `.claude/settings.json`, it will be silently ignored. Move the setting to `~/.claude/settings.json`.
  - *Source*: [settings.md](https://code.claude.com/docs/en/settings.md)

- **`autoMemoryDirectory` path validation clarified**: The value must now be an absolute path or start with `~/`. The docs previously said only "accepts `~/`-expanded paths."
  > The value must be an absolute path or start with `~/`.
  - *Source*: [memory.md](https://code.claude.com/docs/en/memory.md)

### Installation

- **npm update command corrected**: The recommended command to update Claude Code via npm changed from `npm update -g @anthropic-ai/claude-code` to `npm install -g @anthropic-ai/claude-code@latest`.
  > **npm**: `npm install -g @anthropic-ai/claude-code@latest`
  - *Implication*: `npm update` does not reliably pull the latest version when a package is already installed globally; `npm install` with an explicit `@latest` tag is the correct approach.
  - *Source*: [discover-plugins.md](https://code.claude.com/docs/en/discover-plugins.md)

## Notable Details

- The `memory.md` page now explicitly scopes `autoMemoryDirectory` to "your user settings at `~/.claude/settings.json`" rather than the more ambiguous "user or local settings." This wording aligns with the security restriction above and removes the implication that local settings are a valid source.
- The hooks reference table in `hooks.md` also updated the `reason` field description from "Explanation shown to Claude" to the more accurate "Explanation for the block" — reflecting that Claude does not see the reason for most hook events.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| hooks.md | Modified | +6/-4 | Expanded `reason` field docs to distinguish Stop/SubagentStop behavior from other events |
| memory.md | Modified | +2/-2 | Clarified `autoMemoryDirectory` path requirements and accepted settings sources |
| settings.md | Modified | +1/-1 | Updated `autoMemoryDirectory` description to reflect new source restrictions |
| hooks-guide.md | Modified | +1/-1 | Corrected `ok: false` behavior description for non-Stop hook events |
| discover-plugins.md | Modified | +1/-1 | Fixed npm update command to use `npm install -g @latest` |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-04*
