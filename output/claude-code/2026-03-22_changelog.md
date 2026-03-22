# Claude Code Documentation Changes — 2026-03-22

## Summary

Six documentation pages were updated with no pages added or removed. The changes introduce a new `user.account_id` OTel attribute, expand plugin agent frontmatter field documentation, clarify the scope of `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS`, add tmux passthrough guidance for notifications, and refine terminal progress bar support details.

## Significant Changes

### Monitoring & Telemetry

- **New `user.account_id` OTel attribute**: A new standard attribute `user.account_id` is now documented alongside the existing `user.account_uuid`. It provides the account ID in tagged format matching Anthropic admin APIs.
  > `user.account_id` — Account ID in tagged format matching Anthropic admin APIs (when authenticated), such as `user_01BWBeN28...`
  - *Implication*: This attribute is controlled by `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (default: `true`) and can now be used for metric segmentation. The `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` description has been updated to reflect that it gates both `user.account_uuid` and `user.account_id`. The alerting segmentation note also now includes `user.account_id`.
  - *Source*: [Monitoring](https://code.claude.com/docs/en/monitoring-usage.md)

- **Event-only attributes formally documented**: Two attributes are now explicitly listed as event-only (excluded from metrics due to unbounded cardinality):
  > Events additionally include the following attributes. These are never attached to metrics because they would cause unbounded cardinality:
  > * `prompt.id`: UUID correlating a user prompt with all subsequent events until the next prompt.
  > * `workspace.host_paths`: host workspace directories selected in the desktop app, as a string array
  - *Implication*: `workspace.host_paths` is a newly documented attribute. Monitoring pipelines that rely on event data should be aware of this additional field when running the desktop app.
  - *Source*: [Monitoring](https://code.claude.com/docs/en/monitoring-usage.md)

### Plugin Agent Configuration

- **Plugin agent frontmatter fields fully enumerated**: The plugins reference now shows a complete example with `model`, `effort`, `maxTurns`, and `disallowedTools` in the agent frontmatter code block, and explicitly documents all supported fields and security restrictions.
  > Plugin agents support `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, and `isolation` frontmatter fields. The only valid `isolation` value is `"worktree"`. For security reasons, `hooks`, `mcpServers`, and `permissionMode` are not supported for plugin-shipped agents.
  - *Implication*: Plugin authors now have an authoritative reference for which frontmatter fields are available and which are explicitly blocked for security reasons.
  - *Source*: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

### Git Instructions Scope Clarification

- **`CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` now also disables the git status snapshot**: The description was updated to include "and the git status snapshot" in what gets removed from Claude's system prompt.
  > Set to `1` to remove built-in commit and PR workflow instructions **and the git status snapshot** from Claude's system prompt. Useful when using your own git workflow skills.
  - *Implication*: Users who set this flag should be aware that the git status snapshot is also suppressed — this affects context Claude has about the current repo state, not just workflow guidance. The `includeGitInstructions` setting in `settings.md` was updated with identical wording.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md), [Settings](https://code.claude.com/docs/en/settings.md)

### Channels Plugin Installation

- **Plugin marketplace troubleshooting improved**: The "plugin not found" error guidance now distinguishes between a missing and an outdated marketplace, and adds a required post-install step.
  > If Claude Code reports that the plugin is not found in any marketplace, your marketplace is either missing or outdated. Run `/plugin marketplace update claude-plugins-official` to refresh it, or `/plugin marketplace add anthropics/claude-plugins-official` if you haven't added it before. Then retry the install.
  >
  > After installing, run `/reload-plugins` to activate the plugin's configure command.
  - *Implication*: The `/reload-plugins` step after installation is new and required to make the plugin's configure command (e.g. `/telegram:configure`) available in the current session without a restart. This applies to Telegram and Discord channel plugins.
  - *Source*: [Channels](https://code.claude.com/docs/en/channels.md)

### Terminal Configuration

- **tmux passthrough requirement documented**: A new section explains that notifications and the terminal progress bar are intercepted by tmux unless passthrough is explicitly enabled.
  > When running Claude Code inside tmux, notifications and the terminal progress bar only reach the outer terminal, such as iTerm2, Kitty, or Ghostty, if you enable passthrough in your tmux configuration:
  > ```
  > set -g allow-passthrough on
  > ```
  - *Implication*: Users who noticed missing desktop notifications or absent progress bars when running Claude Code inside tmux now have the resolution documented.
  - *Source*: [Terminal Config](https://code.claude.com/docs/en/terminal-config.md)

- **Vim mode `editorMode` config key documented**: The terminal-config Vim Mode section now includes a direct reference to configuring `editorMode` in `~/.claude.json`, enabling programmatic configuration without using `/vim`.
  > To set the mode directly in your config file, set the [`editorMode`](/en/settings#global-config-settings) global config key to `"vim"` in `~/.claude.json`.
  - *Source*: [Terminal Config](https://code.claude.com/docs/en/terminal-config.md)

## Notable Details

- **`terminalProgressBarEnabled` supported terminals updated**: The setting description changed from "Windows Terminal and iTerm2" to "ConEmu, Ghostty 1.2.0+, and iTerm2 3.6.6+". This is a more precise list — notably Windows Terminal is no longer listed, and Ghostty now appears with a minimum version requirement.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`editorMode` added to global config settings table**: A new entry `editorMode` documents the `"normal"` or `"vim"` key binding modes for the input prompt. It is written automatically when `/vim` is run, and appears in `/config` as **Key binding mode**.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`settings.md` bulk reformat**: The available settings table accounts for 55 additions and 54 deletions. The content changes are the `includeGitInstructions` and `terminalProgressBarEnabled` / `editorMode` updates noted above; the remaining diff is column-width adjustment in the markdown table.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| settings.md | Modified | +55/-54 | `includeGitInstructions` scope update (git status snapshot); `editorMode` added to global config; `terminalProgressBarEnabled` supported terminal list refined; table reformatting |
| monitoring-usage.md | Modified | +21/-15 | New `user.account_id` standard attribute; `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` scope expanded; event-only attributes (`prompt.id`, `workspace.host_paths`) documented |
| terminal-config.md | Modified | +9/-1 | tmux passthrough guidance added for notifications and progress bar; `editorMode` config key reference added to Vim mode section |
| plugins-reference.md | Modified | +6/-0 | Plugin agent frontmatter fields fully documented with example and security restrictions |
| channels.md | Modified | +7/-3 | Marketplace troubleshooting updated to distinguish missing vs. outdated; `/reload-plugins` step added post-install |
| env-vars.md | Modified | +1/-1 | `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` now explicitly includes git status snapshot in what it disables |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-22*
