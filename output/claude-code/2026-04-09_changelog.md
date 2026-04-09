# Claude Code Documentation Changes — 2026-04-09

## Summary

Seventeen pages were updated across authentication, hooks, remote control, VS Code extension, commands, and monitoring. The most significant additions are: a new `claude setup-token` CLI command for generating long-lived OAuth tokens for CI pipelines; a new `--spawn=session` mode for Remote Control server; VS Code-native Remote Control support; and a restructured commands reference that consolidates built-in commands and bundled skills into a single unified page.

## Significant Changes

### Authentication

- **New `claude setup-token` command**: Generates a one-year OAuth token for CI pipelines and scripts where interactive browser login is unavailable. The token is printed to the terminal but not saved; developers must copy it and set `CLAUDE_CODE_OAUTH_TOKEN` in their environment.
  > "The command walks you through OAuth authorization and prints a token to the terminal. It does not save the token anywhere; copy it and set it as the `CLAUDE_CODE_OAUTH_TOKEN` environment variable wherever you want to authenticate."
  - *Implication*: Teams running Claude Code in CI now have a subscription-backed auth path without needing an API key. The token is inference-only and cannot establish Remote Control sessions. Bare mode (`--bare`) does not read this token—use `ANTHROPIC_API_KEY` or `apiKeyHelper` instead.
  - *Source*: [Authentication](https://code.claude.com/docs/en/authentication.md)

- **`CLAUDE_CODE_OAUTH_TOKEN` is now priority #5 in the authentication chain**: The new long-lived token slot sits between `apiKeyHelper` output (slot 4) and subscription OAuth credentials from `/login` (now slot 6).
  - *Source*: [Authentication](https://code.claude.com/docs/en/authentication.md)

### Hooks

- **Matcher pattern evaluation rules formally documented**: The `matcher` field behavior is now explicitly defined as a three-way rule rather than simply "a regex":
  > | Matcher value | Evaluated as |
  > |---|---|
  > | `"*"`, `""`, or omitted | Match all — fires on every occurrence |
  > | Only letters, digits, `_`, and `\|` | Exact string or `\|`-separated list of exact strings |
  > | Contains any other character | JavaScript regular expression |
  - *Implication*: A matcher like `mcp__memory` contains only letters and underscores, so it is treated as an exact string and matches no tool. The correct form is `mcp__memory__.*` (the `.*` triggers regex evaluation). This was previously undocumented and likely caused silent failures for developers writing MCP hooks.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **`FileChanged` matcher roles clarified — watch list and filter are separate**: The `matcher` value serves two distinct roles for `FileChanged`: building the file watch list (split on `|` into literal filenames), and filtering which hook groups run when a file changes (using standard matcher rules).
  > "Build the watch list: the value is split on `|` and each segment is registered as a literal filename in the working directory, so `".envrc|.env"` watches exactly those two files. Regex patterns are not useful here: a value like `^\.env` would watch a file literally named `^\.env`."
  - *Implication*: Regex patterns should not be used in `FileChanged` matchers for the watch list—only pipe-separated exact filenames are supported.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md), [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)

- **MCP tool matcher documentation corrected**: The docs now explicitly warn that `mcp__memory` (no special characters) matches no tool—`.*` is required to target all tools from a server.
  > "To match every tool from a server, append `.*` to the server prefix. The `.*` is required: a matcher like `mcp__memory` contains only letters and underscores, so it is compared as an exact string and matches no tool."
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

### Remote Control

- **New `--spawn=session` mode**: A single-session mode that serves exactly one connection and rejects additional ones. Cannot be used with `--capacity`.
  > "`session`: single-session mode. Serves exactly one session and rejects additional connections. Set at startup only."
  - *Implication*: Useful for dedicated setups where concurrent access must be prevented. The `w` runtime toggle (between `same-dir` and `worktree`) does not apply to `session` mode, which is fixed at startup.
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

- **VS Code extension now supports `/remote-control`**: The VS Code Claude Code extension gains a `/remote-control` command (alias `/rc`) for starting a Remote Control session directly from the panel. Requires Claude Code v2.1.79 or later.
  > "A banner appears above the prompt box showing connection status. Once connected, click **Open in browser** in the banner to go directly to the session... To disconnect, click the close icon on the banner or run `/remote-control` again."
  - *Implication*: VS Code users no longer need to switch to a terminal to start Remote Control. The VS Code command does not support the `--name` argument or QR codes; the session title is derived from conversation history.
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

- **Limitations wording updated to cover VS Code**: "Terminal must stay open" is reworded to "Local process must keep running," explicitly covering cases where VS Code itself is closed.
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

### VS Code Extension

- **New "Sign in" step added to getting-started flow**: Authentication is now a discrete setup step with guidance for common failure cases.
  > "If you have `ANTHROPIC_API_KEY` set in your shell but still see the sign-in prompt, VS Code may not have inherited your shell environment. Launch VS Code from a terminal with `code .` so it inherits your environment variables, or sign in with your Claude account instead."
  - *Source*: [VS Code extension](https://code.claude.com/docs/en/vs-code.md)

- **`enableNewConversationShortcut` default changed from `true` to `false`**: The `Cmd/Ctrl+N` new conversation shortcut is now opt-in. The command table also now notes it "requires `enableNewConversationShortcut` set to `true`."
  - *Implication*: Users who rely on `Cmd+N` to start a new conversation must now explicitly enable this setting after updating.
  - *Source*: [VS Code extension](https://code.claude.com/docs/en/vs-code.md)

- **New `usePythonEnvironment` setting** (default: `true`): Activates the workspace's Python environment when running Claude. Requires the Python extension.
  - *Source*: [VS Code extension](https://code.claude.com/docs/en/vs-code.md)

- **`selectedModel` setting removed from the documented settings table**: No longer appears in the extension settings reference. Per-session model selection via `/model` is unaffected.
  - *Source*: [VS Code extension](https://code.claude.com/docs/en/vs-code.md)

### Commands Reference Restructured

- **`commands.md` renamed from "Built-in commands" to "Commands"**: The page is now the unified reference for both built-in commands and bundled skills. Bundled skills (`/batch`, `/claude-api`, `/debug`, `/loop`, `/simplify`) are listed inline in the commands table with a **[Skill]** label to distinguish them from hard-coded CLI behaviors.
  > "The table below lists all the commands included in Claude Code. Entries marked **[Skill]** are bundled skills. They use the same mechanism as skills you write yourself: a prompt handed to Claude, which Claude can also invoke automatically when relevant. Everything else is a built-in command whose behavior is coded into the CLI."
  - *Implication*: The bundled skills table has been removed from `skills.md` and consolidated into the commands reference. All internal `#built-in-commands` anchor links across the docs have been updated.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md), [Skills](https://code.claude.com/docs/en/skills.md)

- **Interactive mode "Commands" section scope expanded**: Now clarifies that the `/` menu includes commands contributed by plugins and MCP servers in addition to built-in commands and skills.
  > "The `/` menu shows everything you can invoke: built-in commands, bundled and user-authored skills, and commands contributed by plugins and MCP servers."
  - *Source*: [Interactive mode](https://code.claude.com/docs/en/interactive-mode.md)

### Monitoring

- **New "Detect retry exhaustion" section**: Clarifies that `claude_code.api_error` fires only after Claude Code gives up retrying—not for each failed attempt. The `attempt` attribute now explicitly documents total attempts made (including the initial request; `1` means no retries occurred).
  > "Claude Code retries failed API requests internally and emits a single `claude_code.api_error` event only after it gives up, so the event itself is the terminal signal for that request. Intermediate retry attempts are not logged as separate events."
  - *Implication*: Operators monitoring API reliability should group `api_error` events by `session.id` and check for a later `api_request` event to distinguish a recovered session from one that stalled permanently.
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

## Notable Details

- **JetBrains plugin npm package name corrected**: The "Claude command" example changed from `npx @anthropic/claude` to `npx @anthropic-ai/claude-code`. The previous package reference was incorrect. Source: [JetBrains](https://code.claude.com/docs/en/jetbrains.md)

- **`CLAUDE_CODE_OAUTH_TOKEN` env var description updated**: Now explicitly states the token can be generated with `claude setup-token`, linking to the new authentication docs section. Source: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **Remote Control `--spawn` toggle scope clarified**: The `w` runtime toggle switches between `same-dir` and `worktree` only. The new `session` mode is set at startup and cannot be toggled. Source: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

- **`features-overview.md` bundled skills link updated**: "Skills" tab now links to `/en/commands` instead of `/en/skills#bundled-skills`, consistent with the commands page restructure. Source: [Features overview](https://code.claude.com/docs/en/features-overview.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| authentication.md | Modified | +21/-2 | New `claude setup-token` section; `CLAUDE_CODE_OAUTH_TOKEN` added at auth priority #5 |
| hooks.md | Modified | +39/-24 | Matcher evaluation rules formally documented; `FileChanged` and MCP matcher semantics clarified |
| hooks-guide.md | Modified | +21/-21 | `FileChanged` matcher docs updated to match hooks.md |
| remote-control.md | Modified | +27/-13 | New `--spawn=session` mode; VS Code `/remote-control` command documented; limitations updated |
| vs-code.md | Modified | +23/-15 | New sign-in step; `enableNewConversationShortcut` default changed to `false`; new `usePythonEnvironment` setting; `selectedModel` removed |
| commands.md | Modified | +13/-4 | Renamed "Built-in commands" → "Commands"; bundled skills listed with [Skill] labels |
| monitoring-usage.md | Modified | +9/-1 | New "Detect retry exhaustion" section; `attempt` field semantics clarified |
| interactive-mode.md | Modified | +8/-8 | Section renamed; `/` menu described as including plugins and MCP commands |
| skills.md | Modified | +4/-12 | Bundled skills table removed; page now defers to commands reference |
| cli-reference.md | Modified | +1/0 | Added `claude setup-token` to CLI commands table |
| env-vars.md | Modified | +1/-1 | `CLAUDE_CODE_OAUTH_TOKEN` description links to `setup-token` docs |
| jetbrains.md | Modified | +1/-1 | Corrected npm package name to `@anthropic-ai/claude-code` |
| features-overview.md | Modified | +1/-1 | Bundled skills link updated to point to commands page |
| checkpointing.md | Modified | +1/-1 | "Built-in commands" link updated to "Commands" |
| claude-code-on-the-web.md | Modified | +1/-1 | `/autofix-pr` link anchor updated |
| scheduled-tasks.md | Modified | +1/-1 | `/loop` link updated from `skills#bundled-skills` to `commands` |
| voice-dictation.md | Modified | +1/-1 | "Built-in commands" link updated to "Commands" |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-09*
