# Claude Code Documentation Changes — 2026-04-02

## Summary

This update introduces two significant hook system expansions: a new `PermissionDenied` hook event for reacting to auto mode classifier denials, and a `"defer"` decision value for `PreToolUse` that enables Agent SDK integrations to pause Claude at a tool call and resume with externally-collected input. Several smaller additions include a new `showThinkingSummaries` setting, a new `MCP_CONNECTION_NONBLOCKING` env var, expanded `forceLoginOrgUUID` to accept arrays, and a behavior change to `cleanupPeriodDays`.

## Significant Changes

### Hooks

#### New `PermissionDenied` hook event

A new lifecycle hook event fires when the auto mode classifier denies a tool call. It does not fire on manual denials, `PreToolUse` blocks, or `deny` rule matches — only on auto mode classifier rejections.

> `PermissionDenied` — When a tool call is denied by the auto mode classifier. Return `{retry: true}` to tell the model it may retry the denied tool call

The hook cannot block (exit code 2 is ignored since the denial has already occurred). Its only decision control is `hookSpecificOutput.retry: true`, which injects a message into the conversation telling the model it may retry. Matches on tool name like other tool events, and supports the `if` field for narrow filtering. Supports `command` and `http` hook types; `prompt` and `agent` types are not available.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

- *Implication*: Teams using auto mode can now programmatically observe and react to classifier denials — logging them, adjusting configuration, or selectively allowing retries — without pausing for user input.
- *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md), [hooks-guide.md](https://code.claude.com/docs/en/hooks-guide.md), [plugins-reference.md](https://code.claude.com/docs/en/plugins-reference.md)

#### New `"defer"` decision value for `PreToolUse`

`PreToolUse` hooks now support a fourth `permissionDecision` value: `"defer"`. This exits the Claude Code process gracefully with the pending tool call preserved, allowing a calling process (such as an Agent SDK app) to collect external input and resume the session.

> `"defer"` is for integrations that run `claude -p` as a subprocess and read its JSON output, such as an Agent SDK app or a custom UI built on top of Claude Code. It lets that calling process pause Claude at a tool call, collect input through its own interface, and resume where it left off. Claude Code honors this value only in non-interactive mode with the `-p` flag. In interactive sessions it logs a warning and ignores the hook result.

The process exits with `stop_reason: "tool_deferred"` and a `deferred_tool_use` field carrying the tool's `id`, `name`, and `input`. On resume, the hook fires again and can return `"allow"` with modified `updatedInput` to inject the collected answer.

Key constraints:
- Requires **Claude Code v2.1.89 or later**
- Only works when Claude makes a single tool call in the turn (batch tool calls cause defer to be ignored with a warning)
- `--resume` does not restore the permission mode from the prior session; pass the same `--permission-mode` flag on resume
- Precedence when multiple `PreToolUse` hooks return different decisions: `deny` > `defer` > `ask` > `allow`

The documented primary use case is `AskUserQuestion`: Claude wants to ask the user something, but there is no terminal to answer in. The hook defers the call, the caller surfaces the question in its own UI, and resumes with the answer injected via `updatedInput`.

- *Implication*: This is the formal mechanism for Agent SDK wrappers to implement interactive prompting in otherwise non-interactive `claude -p` pipelines.
- *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md), [hooks-guide.md](https://code.claude.com/docs/en/hooks-guide.md)

#### Hook context output cap documented

> Hook output injected into context (`additionalContext`, `systemMessage`, or plain stdout) is capped at 10,000 characters. Output that exceeds this limit is saved to a file and replaced with a preview and file path, the same way large tool results are handled.

- *Implication*: Hook scripts that emit large context strings will have their output truncated to a file reference. Scripts should be reviewed if they produce verbose output.
- *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md)

### Settings

#### New `showThinkingSummaries` setting

A new `settings.json` key controls whether extended thinking summaries are visible in interactive sessions.

> When unset or `false` (default in interactive mode), thinking blocks are redacted by the API and shown as a collapsed stub. Redaction only changes what you see, not what the model generates: to reduce thinking spend, lower the budget or disable thinking instead. Non-interactive mode (`-p`) and SDK callers always receive summaries regardless of this setting.

Related: the `common-workflows.md` warning about thinking token charges was updated to note that charges apply even when summaries are redacted, and that collapsed stubs are the default interactive mode behavior.

- *Implication*: Developers debugging extended thinking in interactive sessions can set `showThinkingSummaries: true` to see full summaries. This does not affect billing.
- *Source*: [settings.md](https://code.claude.com/docs/en/settings.md), [common-workflows.md](https://code.claude.com/docs/en/common-workflows.md)

#### `forceLoginOrgUUID` now accepts an array of UUIDs

Previously documented as accepting only a single UUID string, `forceLoginOrgUUID` now also accepts an array:

> Accepts a single UUID string, which also pre-selects that organization during login, or an array of UUIDs where any listed organization is accepted without pre-selection. When set in managed settings, login fails if the authenticated account does not belong to a listed organization; an empty array fails closed and blocks login with a misconfiguration message.

- *Implication*: Managed deployments spanning multiple orgs can now enforce login to any one of an approved set of organizations without requiring separate configurations.
- *Source*: [settings.md](https://code.claude.com/docs/en/settings.md)

#### `cleanupPeriodDays` behavior change: `0` is now rejected

The previous behavior of `cleanupPeriodDays: 0` (delete all transcripts at startup and disable session persistence) has been removed:

> Setting to `0` is rejected with a validation error. To disable transcript writes entirely in non-interactive mode (`-p`), use the `--no-session-persistence` flag or the `persistSession: false` SDK option; there is no interactive-mode equivalent.

The minimum valid value is now `1`.

- *Implication*: Existing configurations or scripts that use `cleanupPeriodDays: 0` will now error. Migrate to `--no-session-persistence` for non-interactive pipelines.
- *Source*: [settings.md](https://code.claude.com/docs/en/settings.md)

### Permissions & Auto Mode

#### New "Recently denied" tab in `/permissions`

Auto mode denials are now surfaced in the `/permissions` dialog under a "Recently denied" tab. Press `r` on a denied action to mark it for retry — exiting the dialog will then send a message to the model indicating it may retry that tool call.

> When auto mode denies a tool call, a notification appears and the denied action is recorded in `/permissions` under the Recently denied tab.

The `/permissions` command description in the command reference was also expanded to reflect its full capabilities:

> Manage allow, ask, and deny rules for tool permissions. Opens an interactive dialog where you can view rules by scope, add or remove rules, manage working directories, and review recent auto mode denials.

- *Implication*: The `/permissions` UI is now the primary interactive surface for reviewing and recovering from auto mode false positives, complementing the programmatic `PermissionDenied` hook.
- *Source*: [permissions.md](https://code.claude.com/docs/en/permissions.md), [commands.md](https://code.claude.com/docs/en/commands.md), [permission-modes.md](https://code.claude.com/docs/en/permission-modes.md)

### MCP

#### New `MCP_CONNECTION_NONBLOCKING` environment variable

> Set to `true` in non-interactive mode (`-p`) to skip the MCP connection wait entirely. Useful for scripted pipelines where MCP tools are not needed. Without this variable, the first query waits up to 5 seconds for `--mcp-config` server connections.

- *Implication*: Pipelines using `claude -p` that don't need MCP tools can avoid a 5-second startup delay by setting this variable.
- *Source*: [env-vars.md](https://code.claude.com/docs/en/env-vars.md)

### Sub-agents

#### Running background subagents now appear in `@`-mention typeahead

> Named background subagents currently running in the session also appear in the typeahead, showing their status next to the name.

- *Implication*: Users can now see and mention in-flight background subagents directly from the input box without knowing their names in advance.
- *Source*: [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md)

## Notable Details

- **Fullscreen / iTerm2 mouse reporting**: Added a note that mouse wheel scrolling requires the terminal to forward mouse events. For iTerm2, this is a per-profile setting under Settings → Profiles → Terminal → Enable mouse reporting. The same setting is required for click-to-expand and text selection. ([fullscreen.md](https://code.claude.com/docs/en/fullscreen.md))

- **Bash mode auto-activation on paste**: Pasting text that starts with `!` into an empty interactive-mode prompt now enters bash mode automatically, matching the behavior of typing `!`. ([interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md))

- **Hooks lifecycle diagram updated**: The `hooks-lifecycle.svg` image was updated to include `PermissionDenied` as a side branch from `PermissionRequest` for auto-mode denials. ([hooks.md](https://code.claude.com/docs/en/hooks.md))

- **`--output-format` now formatted as inline code**: A minor fix in `common-workflows.md` corrected `--output-format` from plain text to backtick-wrapped inline code in a tip callout.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| hooks.md | Modified | +142/-46 | New `PermissionDenied` event, `"defer"` for PreToolUse, hook output cap, updated decision control tables |
| settings.md | Modified | +60/-59 | New `showThinkingSummaries` key, `forceLoginOrgUUID` array support, `cleanupPeriodDays` behavior change |
| permissions.md | Modified | +6/-0 | New "Review auto mode denials" section documenting `/permissions` Recently denied tab |
| hooks-guide.md | Modified | +6/-3 | `PermissionDenied` added to event table and matcher table; `"defer"` mentioned in PreToolUse guide |
| common-workflows.md | Modified | +2/-2 | Thinking token charge warning updated; `--output-format` formatting fix |
| fullscreen.md | Modified | +2/-0 | iTerm2 mouse reporting note for wheel scrolling |
| env-vars.md | Modified | +1/-0 | New `MCP_CONNECTION_NONBLOCKING` variable |
| interactive-mode.md | Modified | +1/-0 | Bash mode auto-activation on paste |
| permission-modes.md | Modified | +1/-1 | Auto mode denial notification now mentions `/permissions` Recently denied tab |
| plugins-reference.md | Modified | +1/-0 | `PermissionDenied` added to plugin hook event table |
| commands.md | Modified | +1/-1 | Expanded `/permissions` command description |
| sub-agents.md | Modified | +1/-1 | Running background subagents appear in typeahead with status |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-02*
