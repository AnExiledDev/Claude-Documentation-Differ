# Claude Code Documentation Changes — 2026-03-26

## Summary

Version 2.1.84 was released on March 26, 2026, introducing a Windows PowerShell tool as an opt-in preview, new environment variables for customizing pinned model display and capability detection on third-party providers (Bedrock, Vertex AI, Foundry), and a `TaskCreated` hook event. Hooks gained HTTP support for `WorktreeCreate` and a per-hook `shell` field for PowerShell. Several UI improvements were documented including new footer keybindings and a VSCode rate-limit warning banner, alongside numerous bug fixes.

---

## Significant Changes

### Features — Windows PowerShell Tool (Preview)

- **New `PowerShell` tool for Windows**: Claude Code can now run PowerShell commands natively on Windows instead of routing through Git Bash. This is an opt-in preview requiring `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`.
  > "On Windows, Claude Code can run PowerShell commands natively instead of routing through Git Bash. This is an opt-in preview."
  > "Claude Code auto-detects `pwsh.exe` (PowerShell 7+) with a fallback to `powershell.exe` (PowerShell 5.1). The Bash tool remains registered alongside the PowerShell tool, so you may need to ask Claude to use PowerShell."
  - *Implication*: Windows users can now write PowerShell-native scripts and commands without Git Bash translation. The `PowerShell` tool requires permission (same as `Bash`).
  - *Source*: [Tools Reference](https://code.claude.com/docs/en/tools-reference.md)

- **Preview limitations**: Auto mode, PowerShell profiles, and sandboxing are not yet supported. Native Windows only (not WSL). Git Bash is still required to start Claude Code.
  - *Source*: [Tools Reference](https://code.claude.com/docs/en/tools-reference.md)

- **`defaultShell` setting**: New `settings.json` key routes interactive `!` commands through PowerShell. Accepts `"bash"` (default) or `"powershell"`. Requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`shell` field on command hooks**: Individual hooks can now run in PowerShell by setting `"shell": "powershell"`. This works regardless of whether `CLAUDE_CODE_USE_POWERSHELL_TOOL` is set, because hooks spawn PowerShell directly.
  > "`shell`: Shell to use for this hook. Accepts `"bash"` (default) or `"powershell"`. Setting `"powershell"` runs the command via PowerShell on Windows. Does not require `CLAUDE_CODE_USE_POWERSHELL_TOOL` since hooks spawn PowerShell directly"
  - *Implication*: Teams can migrate individual hooks to PowerShell incrementally without enabling the full PowerShell tool.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

- **`shell` frontmatter field in skills**: Skills can declare `shell: powershell` to run `` !`command` `` blocks via PowerShell on Windows. Requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

---

### Features — Model Configuration (Third-Party Providers)

- **Pinned model display name and capability overrides**: New companion environment variables allow operators on Bedrock, Vertex AI, and Foundry to customize how pinned models appear in the `/model` picker and declare which features they support. These variables have no effect when using the Anthropic API directly.

  New variables follow the pattern `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL_{NAME,DESCRIPTION,SUPPORTED_CAPABILITIES}`:

  | Variable suffix | Purpose |
  |---|---|
  | `_NAME` | Display name in `/model` picker |
  | `_DESCRIPTION` | Display description in `/model` picker |
  | `_SUPPORTED_CAPABILITIES` | Comma-separated capability declarations |

  Supported capability values: `effort`, `max_effort`, `thinking`, `adaptive_thinking`, `interleaved_thinking`.

  > "Claude Code enables features like effort levels and extended thinking by matching the model ID against known patterns. Provider-specific IDs such as Bedrock ARNs or custom deployment names often don't match these patterns, leaving supported features disabled. Set `_SUPPORTED_CAPABILITIES` to tell Claude Code which features the model actually supports."

  - *Implication*: Bedrock/Vertex/Foundry operators who pin models with non-standard IDs (ARNs, deployment names) can now unlock effort levels and thinking features that were previously silently disabled.
  - *Source*: [Model Configuration](https://code.claude.com/docs/en/model-config.md), [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

---

### Features — Hooks

- **`WorktreeCreate` now supports HTTP hooks**: Previously only `type: "command"` hooks were supported for `WorktreeCreate`. HTTP hooks can now return the created worktree path via `hookSpecificOutput.worktreePath` in the response JSON.
  > "Command hooks (`type: "command"`): print the path on stdout. HTTP hooks (`type: "http"`): return `{ "hookSpecificOutput": { "hookEventName": "WorktreeCreate", "worktreePath": "/absolute/path" } }` in the response body."
  - *Implication*: `WorktreeCreate` hooks can now be implemented as remote HTTP endpoints, enabling centralized worktree management services.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

- **`WorktreeRemove` no longer restricted to command hooks**: The documentation previously stated `WorktreeRemove` only supports `type: "command"` hooks. This restriction has been removed.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

- **`TaskCreated` hook event added**: A new hook fires when a task is created via `TaskCreate`.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Corrected hook type support table**: Several events previously listed as "only `command`" now document support for both `command` and `http` hooks. `SessionStart` is explicitly called out as supporting only `command` hooks.
  > "Events that support `command` and `http` hooks but not `prompt` or `agent`: [ConfigChange, CwdChanged, FileChanged, InstructionsLoaded, Notification, PostCompact, PreCompact, SessionEnd, StopFailure, SubagentStart, TeammateIdle, WorktreeCreate, WorktreeRemove]"
  > "`SessionStart` supports only `command` hooks."
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

---

### Features — Keybindings

- **New footer navigation actions**: Two keybinding actions were added to the `Footer` context: `footer:up` (Up arrow, deselects at top) and `footer:down` (Down arrow). This corresponds to the bug fix for up/down arrow keys being unresponsive when a footer item is focused.
  - *Source*: [Keybindings](https://code.claude.com/docs/en/keybindings.md)

---

### Version 2.1.84 — Additional Changes (from changelog)

The following changes appear in the v2.1.84 release entry and are not yet fully reflected in the reference documentation:

- **`CLAUDE_STREAM_IDLE_TIMEOUT_MS`**: New env var to configure the streaming idle watchdog threshold (default 90s).
- **`allowedChannelPlugins` managed setting**: Allows team/enterprise admins to define a channel plugin allowlist.
- **`x-client-request-id` header**: Added to API requests to aid in debugging timeouts.
- **Idle-return prompt**: After 75+ minutes away, users are nudged to `/clear` to avoid unnecessary token re-caching.
- **Deep link terminal preference**: `claude-cli://` links now open in the user's preferred terminal instead of the first terminal detected.
- **`paths:` frontmatter accepts YAML list**: Rules and skills `paths:` now accepts a YAML list of globs (not just a single glob).
- **MCP tool description cap**: Tool descriptions and server instructions are capped at 2KB to prevent OpenAPI-generated servers from bloating context.
- **MCP server deduplication**: Servers configured both locally and via claude.ai connectors are deduplicated — local config wins.
- **Background bash interactive-prompt detection**: Tasks stuck on an interactive prompt surface a notification after ~45 seconds.
- **Token count display**: Counts ≥1M now display as "1.5m" instead of "1512.6k".
- **Global system-prompt caching**: Now works when `ToolSearch` is enabled, including with MCP tools configured.
- **`#123` auto-link removed**: Issue/PR references are only clickable when written as `owner/repo#123` — bare `#123` no longer auto-links.
- **Unavailable slash commands hidden**: Commands unavailable for the current auth setup (`/voice`, `/mobile`, `/chrome`, `/upgrade`, etc.) are now hidden rather than shown.
- **[VSCode] Rate limit warning banner**: Shows usage percentage and reset time.
- **Stats screenshot speed**: Ctrl+S in `/stats` now works in all builds and is 16× faster.
- **Bug fixes**: Voice push-to-talk, `Ctrl+U` kill-to-line-start, null chord unbinding, mouse events in transcript search, workflow subagent API 400 errors, emoji background color, `Edit(.claude)` permission sticking, large file attachment hang, MCP tool/resource cache leak on reconnect, partial clone repository startup (Scalar/GVFS), IME composition/CJK input, transient macOS keychain errors, cold-start race with core tool deferral.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

### Plugin Marketplace URL Update

- **`code-review` plugin reference updated**: The install command for the `code-review` plugin changed from `claude-code-marketplace` to `claude-plugins-official` in both the CLI reference and the `/review` deprecation notice.
  > `claude plugin install code-review@claude-plugins-official`
  - *Implication*: Existing install commands referencing `claude-code-marketplace` for `code-review` are outdated. The GitHub URL also changed to `github.com/anthropics/claude-plugins-official`.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md), [Commands](https://code.claude.com/docs/en/commands.md)

---

## Notable Details

- The `env-vars.md` change (+119/-109) is primarily a formatting reflow — column separator widths were widened to accommodate longer new variable names (`ANTHROPIC_DEFAULT_HAIKU_MODEL_SUPPORTED_CAPABILITIES`). Net new variables: `CLAUDE_CODE_USE_POWERSHELL_TOOL` and the nine `ANTHROPIC_DEFAULT_*_MODEL_{NAME,DESCRIPTION,SUPPORTED_CAPABILITIES}` vars.
- `setup.md` code blocks gained duplicate `theme={null}` attributes (a doc tooling artifact, not a functional change), plus a new paragraph pointing Windows users to the PowerShell tool documentation.
- The `plugins.md` change corrects the namespace example from `/greet:hello` to `/my-first-plugin:hello`, matching the actual plugin name used in the quickstart.
- The v2.1.84 changelog entry also restores two items that were removed from the v2.1.83 entry in the prior diff: `disableDeepLinkRegistration` and transcript search — both now appear in 2.1.84 instead.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +45/-0 | Added v2.1.84 release entry (March 26, 2026) |
| tools-reference.md | Modified | +37/-0 | New PowerShell tool section with enable instructions, shell selection, and preview limitations |
| env-vars.md | Modified | +119/-109 | Added `CLAUDE_CODE_USE_POWERSHELL_TOOL` and 9 new `ANTHROPIC_DEFAULT_*_MODEL_*` vars; column formatting reflow |
| model-config.md | Modified | +35/-0 | New "Customize pinned model display and capabilities" section for third-party providers |
| hooks.md | Modified | +40/-12 | Added `shell` hook field, HTTP support for `WorktreeCreate`, Windows PowerShell section, corrected hook type support table |
| skills.md | Modified | +14/-13 | Added `shell` frontmatter field; column formatting reflow |
| keybindings.md | Modified | +8/-6 | Added `footer:up` and `footer:down` keybinding actions |
| setup.md | Modified | +7/-5 | Added PowerShell tool reference for Windows; code block attribute cleanup |
| settings.md | Modified | +1/-0 | Added `defaultShell` setting |
| cli-reference.md | Modified | +1/-1 | Updated `code-review` plugin install example to `claude-plugins-official` |
| commands.md | Modified | +1/-1 | Updated `/review` deprecation URL to `claude-plugins-official` |
| plugins.md | Modified | +1/-1 | Fixed namespace example from `/greet:hello` to `/my-first-plugin:hello` |

---

*Generated from Claude Code CLI documentation changes detected on 2026-03-26*
