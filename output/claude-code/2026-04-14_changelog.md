# Claude Code Documentation Changes — 2026-04-14

## Summary

Version 2.1.105 (April 13, 2026) is the headline release, bringing 20+ fixes and improvements including PreCompact hook blocking, plugin background monitors, `/doctor` one-key fixes, and a new `when_to_use` skill field. Documentation also adds subagent status line customization, expanded terminal newline setup guides, new Windows troubleshooting entries, two new OTel telemetry events, and new Bash permission sections covering compound commands and process wrappers.

---

## Significant Changes

### Hooks

- **PreCompact now supports blocking**: The `PreCompact` hook event has been promoted from "side effects only" to a blocking event. Hooks can now prevent compaction by exiting with code 2 or returning `{"decision": "block"}`.
  > Exit with code 2 to block compaction. For a manual `/compact`, the stderr message is shown to the user. You can also block by returning JSON with `"decision": "block"`.
  >
  > Blocking automatic compaction has different effects depending on when it fires. If compaction was triggered proactively before the context limit, Claude Code skips it and the conversation continues uncompacted. If compaction was triggered to recover from a context-limit error already returned by the API, the underlying error surfaces and the current request fails.
  - *Implication*: Hooks that need to gate compaction (e.g., to save state before context is reduced) now have a supported mechanism. Existing `PreCompact` hooks are unchanged unless they start returning `decision: block`.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

- **SessionEnd hook timeout now auto-scales**: The default 1.5-second budget for `SessionEnd` hooks is now automatically raised to the highest per-hook `timeout` configured in settings files (up to 60 seconds). Plugin-provided hook timeouts do not raise the budget.
  > If a hook needs more time, set a per-hook `timeout` in the hook configuration. The overall budget is automatically raised to the highest per-hook timeout configured in settings files, up to 60 seconds.
  - *Implication*: You no longer need to set `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` globally just to accommodate one slow hook — set `timeout` on the individual hook configuration instead.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

### Skills

- **New `when_to_use` frontmatter field**: Skills gain a new optional `when_to_use` field that appends additional context (trigger phrases, example requests) to the skill listing. It counts toward the 1,536-character combined cap.
  > `when_to_use`: Additional context for when Claude should invoke the skill, such as trigger phrases or example requests. Appended to `description` in the skill listing and counts toward the 1,536-character cap.
  - *Implication*: Skill authors can now separate core description from invocation guidance without being penalized against the character cap for `description` alone.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

- **Skill description cap raised from 250 to 1,536 characters**: The per-entry listing cap for combined `description` + `when_to_use` text has increased sixfold.
  > Or trim the `description` and `when_to_use` text at the source: front-load the key use case, since each entry's combined text is capped at 1,536 characters regardless of budget.
  - *Implication*: Skills with detailed instructions will no longer be silently truncated in the listing. A startup warning is also emitted when descriptions are still too long.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

- **Live change detection documented**: A new section documents that Claude Code watches skill directories for file changes and hot-reloads skill edits without restarting. Creating a new top-level skills directory that did not exist at session start still requires a restart.
  > Claude Code watches skill directories for file changes. Adding, editing, or removing a skill under `~/.claude/skills/`, the project `.claude/skills/`, or a `.claude/skills/` inside an `--add-dir` directory takes effect within the current session without restarting.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

### Plugins

- **Plugin background monitors via `monitors` manifest key**: A new top-level manifest field `monitors` allows plugins to declare background Monitor tool configurations that auto-arm at session start or when a skill in the plugin is invoked.
  > `monitors`: Background [Monitor](/en/tools-reference#monitor-tool) configurations that auto-arm when the plugin is enabled at session start or when a skill in this plugin is invoked.
  - *Implication*: Plugins can now ship persistent background monitoring without requiring the user to manually invoke a skill. The default `monitors/monitors.json` path is replaced if the manifest specifies `monitors`.
  - *Source*: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

### Status Line

- **New `subagentStatusLine` setting**: A new settings key allows customizing the row body rendered for each subagent in the agent panel, replacing the default `name · description · token count` layout.
  > The `subagentStatusLine` setting renders a custom row body for each [subagent](/en/sub-agents) shown in the agent panel below the prompt. Use it to replace the default `name · description · token count` row with your own formatting.
  >
  > The command runs once per refresh tick with all visible subagent rows passed as a single JSON object on stdin. The input includes the [base hook fields](/en/hooks#common-input-fields) plus `columns` (the usable row width) and a `tasks` array, where each task has `id`, `name`, `type`, `status`, `description`, `label`, `startTime`, `tokenCount`, `tokenSamples`, and `cwd`.
  - *Implication*: Teams managing multiple subagents can display richer per-agent context (token samples, elapsed time, etc.) using the same shell-script approach as the main status line. Plugins can ship a default `subagentStatusLine` in their `settings.json`.
  - *Source*: [Customize your status line](https://code.claude.com/docs/en/statusline.md)

### Permissions

- **Compound commands now save per-subcommand rules**: When approving a compound command (e.g., `git status && npm test`) with "Yes, don't ask again", Claude Code now saves a separate allow rule for each subcommand that requires approval, rather than a single rule for the full compound string.
  > When you approve a compound command with "Yes, don't ask again", Claude Code saves a separate rule for each subcommand that requires approval... so future `npm test` invocations are recognized regardless of what precedes the `&&`. Up to 5 rules may be saved for a single compound command.
  - *Implication*: Previously approved compound commands may now match more broadly; review saved rules if you see unexpected auto-approvals.
  - *Source*: [Configure permissions](https://code.claude.com/docs/en/permissions.md)

- **Process wrapper stripping documented**: Claude Code now strips a fixed set of process wrappers (`timeout`, `time`, `nice`, `nohup`, `stdbuf`, and bare `xargs`) before matching Bash permission rules. This means `Bash(npm test *)` also matches `timeout 30 npm test`.
  > Before matching Bash rules, Claude Code strips a fixed set of process wrappers so a rule like `Bash(npm test *)` also matches `timeout 30 npm test`. The recognized wrappers are `timeout`, `time`, `nice`, `nohup`, and `stdbuf`.
  - *Implication*: Permissions rules should be written for the inner command; wrappers are transparent. Development environment runners (`direnv exec`, `devbox run`, `npx`, etc.) are NOT stripped and require explicit rules.
  - *Source*: [Configure permissions](https://code.claude.com/docs/en/permissions.md)

### Monitoring / Telemetry

- **Two new OTel event types**: The monitoring documentation adds two new events logged via `OTEL_LOGS_EXPORTER`:
  - `claude_code.plugin_installed` — fired on plugin install from both `claude plugin install` CLI and the `/plugin` UI. Attributes include `plugin.name`, `plugin.version`, `marketplace.name`, `marketplace.is_official`, and `install.trigger` (`"cli"` or `"ui"`).
  - `claude_code.skill_activated` — fired when a skill is invoked.
  - *Implication*: Organizations tracking plugin adoption or skill usage patterns can now capture these events in their existing OTel pipeline without additional instrumentation.
  - *Source*: [Monitoring](https://code.claude.com/docs/en/monitoring-usage.md)

### Terminal Configuration

- **Newline setup guide expanded**: The terminal configuration page now has distinct subsections for three newline scenarios previously collapsed into flat text:
  - **Shift+Enter in tmux**: New instructions to enable extended key reporting in `~/.tmux.conf` (`set -s extended-keys on` + `set -as terminal-features 'xterm*:extkeys'`).
  - **Option+Enter on macOS**: New tabbed instructions covering Terminal.app, iTerm2, and VS Code for enabling Option-as-Meta mode.
  - *Source*: [Terminal configuration](https://code.claude.com/docs/en/terminal-config.md)

### Troubleshooting

- **Windows: wrong install command section** replaces the former `` `irm` or `&&` not recognized `` entry. The new section covers three cases: `irm` not recognized (running CMD instead of PowerShell), `&&` not valid (running CMD command in PowerShell), and `bash` not recognized (running macOS/Linux installer on Windows).
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

- **New: Windows 32-bit PowerShell error** (`Claude Code does not support 32-bit Windows`): Documents that Windows PowerShell (x86) triggers this error on 64-bit machines, and provides the `[Environment]::Is64BitOperatingSystem` check to distinguish between the two cases.
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

### CLI / Commands

- **`/doctor` gains interactive fix key**: The `/doctor` command description is updated to note that results now show with status icons, and pressing `F` sends the diagnostics report to Claude to fix reported issues.
  > Diagnose and verify your Claude Code installation and settings. Results show with status icons. Press `f` to have Claude fix any reported issues.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

- **`/proactive` alias for `/loop`**: `/proactive` is now documented as an alias for the `/loop` command.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

### Environment Variables

- **`CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` scope expanded**: When set to `1`, the variable now loads `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md`, *and* `CLAUDE.local.md` from `--add-dir` directories (previously only `CLAUDE.md` was documented).
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **Streaming watchdog split into two variables**: `CLAUDE_ENABLE_STREAM_WATCHDOG` is redefined as the *event-level* watchdog (off by default), and a new variable `CLAUDE_ENABLE_BYTE_WATCHDOG` controls the *byte-level* watchdog (on by default for Anthropic API connections). The byte watchdog has a minimum 5-minute timeout; the event watchdog defaults to 90 seconds.
  - *Implication*: Users who previously relied on `CLAUDE_ENABLE_STREAM_WATCHDOG=1` to protect against hung connections on the Anthropic API will find the byte watchdog now handles that case by default. Third-party providers (Bedrock, Vertex, Foundry) still use the event-level watchdog.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

---

## Notable Details

- **Keybindings: `doctor:fix` action added**: A new `doctor:fix` binding (default key `F`) is listed in the keybindings reference under a new "Doctor actions" context. Only active when issues are found.
- **Keybindings: `chat:newline` now defaults to `Ctrl+J`**: Previously listed as `(unbound)`, `chat:newline` now has a default binding.
- **`CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` behavior clarified**: The env var now explicitly overrides the budget rather than being the only way to raise it. Per-hook `timeout` settings are the preferred mechanism.
- **WSL setup instructions simplified**: The `setup.md` Windows section no longer lists WSL 1 vs. WSL 2 sandboxing differences; it now simply instructs users to open WSL and run the Linux installer from within the WSL terminal.
- **discover-plugins.md**: Added a recovery tip — when a plugin is not found, run `/plugin marketplace update claude-plugins-official` or `/plugin marketplace add anthropics/claude-plugins-official` before retrying.
- **Plugin directory layout**: `monitors/` is now listed in the standard plugin layout alongside `hooks/`, `skills/`, etc.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +40/-0 | Added v2.1.105 release entry (April 13, 2026) |
| troubleshooting.md | Modified | +47/-20 | New Windows 32-bit error section; replaced `irm`/`&&` section with "wrong install command"; updated error lookup table |
| monitoring-usage.md | Modified | +35/-0 | Added `plugin_installed` and `skill_activated` OTel event types |
| terminal-config.md | Modified | +25/-10 | New Shift+Enter in tmux and Option+Enter on macOS subsections |
| permissions.md | Modified | +22/-8 | New Compound commands and Process wrappers subsections |
| skills.md | Modified | +22/-17 | New `when_to_use` field, Live change detection section, cap raised to 1,536 chars |
| plugins-reference.md | Modified | +31/-26 | Added `monitors` manifest key, updated file layout and path behavior docs |
| statusline.md | Modified | +19/-0 | New Subagent status lines section |
| interactive-mode.md | Modified | +19/-19 | Keybinding table reformatting (no net new content) |
| hooks.md | Modified | +18/-14 | PreCompact now blocking; SessionEnd timeout auto-scales; decision table updated |
| setup.md | Modified | +14/-6 | WSL instructions simplified; Git for Windows note scoped to native Windows only |
| keybindings.md | Modified | +10/-1 | New Doctor actions section; `chat:newline` default set to `Ctrl+J` |
| env-vars.md | Modified | +5/-4 | `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` expanded; stream watchdog split; `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` clarified |
| commands.md | Modified | +2/-2 | `/doctor` and `/loop` descriptions updated |
| discover-plugins.md | Modified | +2/-0 | Recovery tip for missing marketplace |
| sub-agents.md | Modified | +4/-0 | Minor additions (related to subagentStatusLine cross-reference) |
| memory.md | Modified | +2/-2 | Minor clarification |
| network-config.md | Modified | +2/-0 | Minor addition |
| overview.md | Modified | +1/-1 | Minor wording change |
| quickstart.md | Modified | +1/-1 | Minor wording change |
| mcp.md | Modified | +1/-1 | Minor wording change |
| plugins.md | Modified | +1/-1 | Minor wording change |
| tools-reference.md | Modified | +2/-2 | Minor wording change |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-14*
