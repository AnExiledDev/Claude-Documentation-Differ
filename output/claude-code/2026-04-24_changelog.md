# Claude Code Documentation Changes — 2026-04-24

## Summary

14 documentation pages were modified with 62 additions and 47 deletions. The most significant change is a settings restructuring in v2.1.119 that migrates several UI preferences (`editorMode`, `showTurnDuration`, `terminalProgressBarEnabled`, `autoScrollEnabled`, `teammateMode`) from `~/.claude.json` into the standard `settings.json` hierarchy. Additional notable changes include new `duration_ms` fields in hook payloads, new status line fields for effort/thinking state, PowerShell auto mode reaching parity with Bash, and expanded `--from-pr` platform support.

## Significant Changes

### Configuration

- **Settings migration: UI preferences moved to `settings.json` (v2.1.119+)**: Five settings previously stored only in `~/.claude.json` are now first-class `settings.json` keys: `autoScrollEnabled`, `editorMode`, `showTurnDuration`, `terminalProgressBarEnabled`, and `teammateMode`.
  > *Versions before v2.1.119 also store `autoScrollEnabled`, `editorMode`, `showTurnDuration`, `teammateMode`, and `terminalProgressBarEnabled` here instead of in `settings.json`.*
  - *Implication*: These settings can now be managed via managed/policy settings, project settings, and the standard settings hierarchy rather than requiring direct edits to `~/.claude.json`. Existing `~/.claude.json` values remain supported on older versions.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **New setting `prUrlTemplate`**: Allows customizing the URL used for PR badge links in the footer and tool-result summaries.
  > *URL template for the PR badge shown in the footer and in tool-result summaries. Substitutes `{host}`, `{owner}`, `{repo}`, `{number}`, and `{url}` from the `gh`-reported PR URL. Use to point PR links at an internal code-review tool instead of `github.com`.*
  - *Implication*: Teams using internal code review tools can redirect PR links without affecting `#123` autolinks in Claude's prose.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **Plugin dependency auto-update behavior clarified**: Updates now fetch the highest satisfying git tag rather than the marketplace's latest version, so constrained dependencies continue receiving updates within their allowed range.
  > *Auto-update fetches a constrained dependency at the highest git tag that satisfies every installed plugin's range, rather than at the marketplace's latest version, so the dependency continues to receive updates within its allowed range.*
  - *Implication*: Plugins with version range constraints will still receive updates within their allowed range rather than being fully frozen at the current version.
  - *Source*: [Plugin Dependencies](https://code.claude.com/docs/en/plugin-dependencies.md)

### Hooks

- **New `duration_ms` field in `PostToolUse` and `PostToolUseFailure` payloads**: Both hook event types now include tool execution time in milliseconds, excluding time spent in permission prompts and `PreToolUse` hooks.
  > *`duration_ms` — Optional. Tool execution time in milliseconds. Excludes time spent in permission prompts and PreToolUse hooks*
  - *Implication*: Hook scripts can now measure and act on tool execution latency — useful for performance monitoring, slow-tool alerting, or audit logging.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

### Status Line

- **New `effort.level` and `thinking.enabled` fields**: The status line JSON payload now includes the current reasoning effort level and whether extended thinking is active.
  > *`effort.level` — Current reasoning effort (`low`, `medium`, `high`, `xhigh`, or `max`). Reflects the live session value, including mid-session `/effort` changes. Absent when the current model does not support the effort parameter*
  > *`thinking.enabled` — Whether extended thinking is enabled for the session*
  - *Implication*: Status line scripts can now display effort level and thinking state. `effort` is a conditional field — only present when the model supports it.
  - *Source*: [Status Line](https://code.claude.com/docs/en/statusline.md)

### CLI

- **`--from-pr` now supports multi-platform PR/MR URLs**: The flag previously described only GitHub PR numbers/URLs; it now explicitly supports GitHub Enterprise, GitLab merge request, and Bitbucket pull request URLs.
  > *Accepts a PR number, a GitHub or GitHub Enterprise PR URL, a GitLab merge request URL, or a Bitbucket pull request URL. Sessions are linked automatically when Claude creates the pull request*
  - *Implication*: Teams on GitLab, Bitbucket, or GitHub Enterprise can use `--from-pr` to resume sessions linked to their platform's PRs/MRs.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

### Environment Variables

- **New `CLAUDE_CODE_HIDE_CWD` variable**: Set to `1` to hide the working directory from the startup logo.
  > *Set to `1` to hide the working directory in the startup logo. Useful for screenshares or recordings where the path exposes your OS username*
  - *Implication*: Useful for demos, recordings, or documentation screenshots where the home directory path would expose a username.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

### MCP

- **Tool search disabled by default on Vertex AI**: MCP tool search (`ENABLE_TOOL_SEARCH`) is now explicitly disabled by default on Vertex AI, not only for non-first-party proxy hosts.
  > *MCP tool search is disabled by default on Vertex AI because the endpoint does not accept the required beta header. All MCP tool definitions load upfront instead. To opt in, set `ENABLE_TOOL_SEARCH=true`.*
  - *Implication*: Vertex AI users with large MCP tool sets should note that all tools load upfront. Opt in via `ENABLE_TOOL_SEARCH=true` if the endpoint supports it.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md), [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai.md)

- **Windows `cmd /c` wrapper note removed**: The warning requiring `cmd /c npx` when adding native Windows MCP servers via `stdio` transport has been removed.
  - *Implication*: The workaround is no longer necessary. Windows users running MCP servers via `npx` no longer need to wrap the command with `cmd /c`.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

### PowerShell Tool

- **Auto mode now works with PowerShell**: The known limitation "Auto mode does not work with the PowerShell tool yet" has been removed from the tools reference.
  - *Implication*: PowerShell commands are now governed by auto mode like Bash commands. The permission-modes page was also updated: blanket `PowerShell(*)` allow rules are now dropped when entering auto mode, consistent with the existing `Bash(*)` behavior.
  - *Source*: [Tools Reference](https://code.claude.com/docs/en/tools-reference.md), [Permission Modes](https://code.claude.com/docs/en/permission-modes.md)

### Observability (OpenTelemetry)

- **New `tool_use_id` field in tool execution and permission decision OTel events**: Both event types now carry a unique per-invocation identifier that matches the `tool_use_id` passed to hooks.
  > *`tool_use_id`: Unique identifier for this tool invocation. Matches the `tool_use_id` passed to hooks, allowing correlation between OTel events and hook-captured data.*
  - *Implication*: Enables joining hook logs with OTel telemetry on a per-invocation basis for end-to-end tracing.
  - *Source*: [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **New `tool_input_size_bytes` field in tool execution OTel events**: Records the byte size of the JSON-serialized tool input.
  - *Implication*: Allows monitoring input size distributions alongside existing result sizes (`tool_result_size_bytes`), useful for identifying large-input outliers that may affect latency.
  - *Source*: [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage.md)

## Notable Details

- **`editorMode` storage location corrected in terminal-config.md**: Documentation now states that `editorMode` is set in `~/.claude/settings.json` (not `~/.claude.json`), and the link target updated from `settings#global-config-settings` to `settings#available-settings` — consistent with the v2.1.119 settings migration.
- **`teammateMode` link target corrected in agent-teams.md**: Now points to `settings#available-settings` instead of `settings#global-config-settings`.
- **`~/.claude.json` description narrowed**: The settings.md description no longer lists "preferences (theme, notification settings, editor mode)" as stored in `~/.claude.json`. That file now stores OAuth session, MCP configs, per-project state, and caches.
- **`claude-directory.md` examples updated**: The `~/.claude.json` tips and example JSON now reference `autoConnectIde` and `externalEditorContext` (IDE-specific toggles that remain in `~/.claude.json`) instead of `showTurnDuration` and `terminalProgressBarEnabled` (which moved to `settings.json`).

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| settings.md | Modified | +16/-11 | Settings migration: UI prefs moved to `settings.json`; new `prUrlTemplate`, `autoScrollEnabled`, `editorMode`, `showTurnDuration`, `terminalProgressBarEnabled`, `teammateMode` entries added |
| hooks.md | Modified | +13/-6 | `duration_ms` field added to `PostToolUse` and `PostToolUseFailure` event payloads |
| mcp.md | Modified | +8/-19 | Windows `cmd /c` warning removed; tool search default updated for Vertex AI |
| statusline.md | Modified | +9/-0 | New `effort.level` and `thinking.enabled` status line fields with example JSON |
| monitoring-usage.md | Modified | +3/-0 | `tool_use_id` and `tool_input_size_bytes` added to OTel tool events |
| google-vertex-ai.md | Modified | +2/-0 | MCP tool search disabled-by-default on Vertex AI documented |
| env-vars.md | Modified | +2/-1 | New `CLAUDE_CODE_HIDE_CWD` env var; `ENABLE_TOOL_SEARCH` updated for Vertex AI |
| claude-directory.md | Modified | +3/-3 | Tips and example JSON updated to reflect settings migration |
| terminal-config.md | Modified | +2/-2 | `editorMode` storage location and link targets updated |
| cli-reference.md | Modified | +1/-1 | `--from-pr` expanded to GitHub Enterprise, GitLab, and Bitbucket |
| plugin-dependencies.md | Modified | +1/-1 | Auto-update behavior for constrained dependencies clarified |
| permission-modes.md | Modified | +1/-1 | `PowerShell(*)` added to auto mode blanket-rule drop list |
| agent-teams.md | Modified | +1/-1 | `teammateMode` link target updated to `settings#available-settings` |
| tools-reference.md | Modified | +0/-1 | PowerShell auto mode limitation removed |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-24*
