# Claude Code Documentation Changes — 2026-03-26

## Summary

This update is dominated by two new hook events (`CwdChanged` and `FileChanged`) for reactive environment management, plus expanded enterprise channel controls (`allowedChannelPlugins`). Several smaller additions fill out the VS Code integration, plugin manifest schema, interactive mode keybindings, and CLI surface area.

---

## Significant Changes

### Hooks

- **Two new hook events: `CwdChanged` and `FileChanged`**: The hooks system gains reactive environment management events. `CwdChanged` fires whenever Claude changes the working directory (e.g., via a `cd` command). `FileChanged` fires when a watched file changes on disk; the `matcher` field configures which filenames to watch (pipe-separated basenames like `.envrc|.env`).

  > "A `CwdChanged` hook fixes this: it runs each time Claude changes directory, so you can reload the correct variables for the new location. The hook writes the updated values to `CLAUDE_ENV_FILE`, which Claude Code applies before each Bash command."

  Both events have access to `CLAUDE_ENV_FILE` for injecting environment variables into subsequent Bash commands — the same mechanism previously exclusive to `SessionStart` hooks. `CwdChanged` provides `old_cwd` and `new_cwd` input fields. `FileChanged` provides `file_path` and `event` (`change`, `add`, or `unlink`).

  Both hooks can return a `watchPaths` array in their output to dynamically update which files `FileChanged` monitors. Neither event supports decision control (they cannot block the directory or file change). Only `type: "command"` hooks are supported for these events.

  - *Implication*: Teams using `direnv` or per-directory virtualenvs can now have Claude's Bash tool automatically pick up environment changes as it moves between directories — closing a long-standing gap between interactive shell behavior and Claude's Bash environment.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md), [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)

- **`CwdChanged` added to matcher-exempt events**: The reference table listing events that silently ignore `matcher` fields was updated to include `CwdChanged`.

  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **`CLAUDE_ENV_FILE` scope expanded**: Previously documented as available only for `SessionStart` hooks; now documented as available to `SessionStart`, `CwdChanged`, and `FileChanged` hooks.

  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md), [Hooks reference](https://code.claude.com/docs/en/hooks.md)

---

### Channels (Enterprise)

- **New `allowedChannelPlugins` managed setting**: Team and Enterprise admins can now replace the Anthropic default channel plugin allowlist with their own list. Each entry specifies a `marketplace` and `plugin` name. When set, it replaces the Anthropic allowlist entirely — only listed plugins can register as channels.

  > "Admins on Team and Enterprise plans can replace that allowlist with their own by setting `allowedChannelPlugins` in managed settings. Use this to restrict which official plugins are allowed, approve channels from your own internal marketplace, or both."

  ```json
  {
    "channelsEnabled": true,
    "allowedChannelPlugins": [
      { "marketplace": "claude-plugins-official", "plugin": "telegram" },
      { "marketplace": "acme-corp-plugins", "plugin": "internal-alerts" }
    ]
  }
  ```

  An empty array blocks all allowlisted plugins (though `--dangerously-load-development-channels` can still bypass it). To block channels entirely including the dev flag, leave `channelsEnabled` unset instead.

  - *Implication*: Enterprises can now approve internal or custom channel plugins without requiring Anthropic marketplace submission, and can restrict which official channels (Telegram, Discord, iMessage) users can connect.
  - *Source*: [Channels](https://code.claude.com/docs/en/channels.md), [Channels reference](https://code.claude.com/docs/en/channels-reference.md)

- **Enterprise controls table restructured**: The previous single-row plan-type table was replaced with a two-row table covering both `channelsEnabled` and `allowedChannelPlugins`, with "When not configured" column clarifying defaults.

  - *Source*: [Channels](https://code.claude.com/docs/en/channels.md)

---

### Plugins Reference

- **New `userConfig` plugin manifest field**: Plugins can now declare configuration values that Claude Code prompts users for when the plugin is enabled — eliminating the need to hand-edit `settings.json` for plugin credentials.

  > "The `userConfig` field declares values that Claude Code prompts the user for when the plugin is enabled. Use this instead of requiring users to hand-edit `settings.json`."

  Keys are substituted as `${user_config.KEY}` in MCP/LSP server configs and hook commands. Non-sensitive values go to `settings.json` under `pluginConfigs[<plugin-id>].options`; sensitive values go to the system keychain (with an ~2 KB limit). Both are exported as `CLAUDE_PLUGIN_OPTION_<KEY>` environment variables to subprocesses.

  - *Implication*: Plugin authors can build a first-run configuration flow without requiring users to know internal file paths or JSON structure.
  - *Source*: [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md)

- **New `channels` plugin manifest field**: Plugins can declare message channels that push events into a running session, binding each channel to a plugin-provided MCP server. Per-channel `userConfig` is supported for credentials like bot tokens.

  - *Source*: [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md)

---

### VS Code Integration

- **New URI handler for launching tabs from external tools**: The extension now registers a URI handler at `vscode://anthropic.claude-code/open`. Any script, shell alias, or browser bookmarklet can open a new Claude Code tab directly.

  > "Use it to open a new Claude Code tab from your own tooling: a shell alias, a browser bookmarklet, or any script that can open a URL. If VS Code isn't already running, opening the URL launches it first."

  Two optional query parameters:

  | Parameter | Description |
  |-----------|-------------|
  | `prompt`  | URL-encoded text to pre-fill in the prompt box (not auto-submitted) |
  | `session` | Session ID to resume; falls back to a new conversation if not found |

  Invoked via `open "vscode://anthropic.claude-code/open"` on macOS, `xdg-open` on Linux, or `start` on Windows.

  - *Implication*: Enables custom automation workflows — e.g., git hooks that open a pre-filled Claude tab, CI integrations that resume an existing session, or IDE extensions that hand off to Claude.
  - *Source*: [VS Code](https://code.claude.com/docs/en/vs-code.md)

---

### Memory

- **AGENTS.md interoperability guidance**: New section documents how to integrate Claude Code in repos that already use `AGENTS.md` for other coding agents. Recommends creating a `CLAUDE.md` that imports `AGENTS.md` via the `@` syntax, avoiding duplication while still supporting Claude-specific additions.

  > "If your repository already uses `AGENTS.md` for other coding agents, create a `CLAUDE.md` that imports it so both tools read the same instructions without duplicating them."

  Example:
  ```markdown
  @AGENTS.md

  ## Claude Code

  Use plan mode for changes under `src/billing/`.
  ```

  - *Implication*: Teams already using Codex or other AGENTS.md-aware agents get a clean integration path with Claude Code.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

---

### CLI & Commands

- **New top-level `claude plugin` command**: Added to the CLI reference as a first-class command (alias: `claude plugins`) for managing Claude Code plugins. Previously plugin management was primarily done via the in-session `/plugin` slash command.

  - *Source*: [CLI reference](https://code.claude.com/docs/en/cli-reference.md)

- **`/plan` accepts an optional description argument**: The `/plan` command signature changed from `/plan` to `/plan [description]`. Passing a description enters plan mode and immediately starts with that task (e.g., `/plan fix the auth bug`).

  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

- **`/copy` can write to file over SSH**: The picker that appears when code blocks are present now supports pressing `w` to write the selection to a file instead of the clipboard — useful when clipboard access is unavailable in remote SSH sessions.

  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

- **`/status` works mid-response**: `/status` can now be used while Claude is actively responding, without waiting for the current response to finish.

  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

- **`/loop` added to bundled skills list**: The bundled skills description in `commands.md` was updated to explicitly include `/loop` alongside `/simplify`, `/batch`, and `/debug`.

  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

---

### Interactive Mode & Keybindings

- **Kill background agents: `Ctrl+F` → `Ctrl+X Ctrl+K`**: The keyboard shortcut to kill all background agents changed from `Ctrl+F` to `Ctrl+X Ctrl+K`.

  - *Implication*: Developers relying on `Ctrl+F` for this action will need to update their muscle memory.
  - *Source*: [Interactive mode](https://code.claude.com/docs/en/interactive-mode.md)

- **New shortcut: `Option+O` / `Alt+O` toggles fast mode**: Added to the general controls table alongside the existing model and extended thinking shortcuts.

  - *Source*: [Interactive mode](https://code.claude.com/docs/en/interactive-mode.md)

- **`Ctrl+X Ctrl+E` added as alias for external editor**: The readline-native binding `Ctrl+X Ctrl+E` is now documented alongside `Ctrl+G` for opening a prompt in the default text editor.

  - *Source*: [Interactive mode](https://code.claude.com/docs/en/interactive-mode.md)

- **New "Transcript viewer" shortcuts section**: Documents shortcuts active when the transcript viewer (`Ctrl+O`) is open: `Ctrl+E` toggles show-all content (rebindable via `transcript:toggleShowAll`), and `q` / `Ctrl+C` / `Esc` exit the viewer (latter two rebindable via `transcript:exit`).

  - *Source*: [Interactive mode](https://code.claude.com/docs/en/interactive-mode.md)

- **Background task output mechanism clarified**: Changed from "Output is buffered and Claude can retrieve it using the TaskOutput tool" to "Output is written to a file and Claude can retrieve it using the Read tool."

  - *Source*: [Interactive mode](https://code.claude.com/docs/en/interactive-mode.md)

- **Paste image description updated**: `Ctrl+V` / `Cmd+V` / `Alt+V` description now specifies that pasting an image "inserts an `[Image #N]` chip at the cursor so you can reference it positionally in your prompt" rather than the previous generic description.

  - *Source*: [Interactive mode](https://code.claude.com/docs/en/interactive-mode.md)

---

### Environment Variables

- **New `CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK`**: Set to `1` to disable the non-streaming fallback when a streaming request fails mid-stream. Streaming errors propagate to the retry layer instead. Useful for proxy/gateway setups where the fallback causes duplicate tool execution.

  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **New `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`**: Set to `1` to strip Anthropic and cloud provider credentials from subprocess environments (Bash tool, hooks, MCP stdio servers). The parent Claude process retains credentials; child processes cannot read them, reducing prompt injection exposure. `claude-code-action` sets this automatically when `allowed_non_write_users` is configured.

  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

---

## Notable Details

- **Changelog entries removed**: Two recent changelog entries were removed from `changelog.md`: `disableDeepLinkRegistration` (setting to prevent `claude-cli://` protocol handler registration) and transcript search (press `/` in transcript mode to search, `n`/`N` to step through matches). This may indicate these features were rolled back or consolidated differently before the public release.

- **`CwdChanged` `watchPaths` output controls `FileChanged` watch list**: The two new hook events are designed to work together. A `CwdChanged` hook can return a fresh `watchPaths` array to reset which files `FileChanged` monitors when entering a new directory — important for tools like `direnv` where the relevant files change per-directory. Returning an empty array clears the dynamic list.

- **`FileChanged` matcher serves dual purpose**: Unlike other hook matchers that are purely filters, the `FileChanged` matcher both *configures* which files to watch (setting up the file system watcher) and *filters* which hooks run when a change occurs.

- **Plugin `userConfig` sensitive values and keychain limits**: Plugin-declared sensitive config values go to the system keychain (or `~/.claude/.credentials.json` as fallback), which is shared with OAuth tokens and has an approximately 2 KB total limit. Plugin authors should keep sensitive values small.

- **`allowedChannelPlugins` requires `channelsEnabled: true`**: Setting `allowedChannelPlugins` alone has no effect; `channelsEnabled` must be `true`. An empty `allowedChannelPlugins` array still allows `--dangerously-load-development-channels` to bypass it for local testing.

- **Settings page restructured with scopes section**: `settings.md` gained a prominent "Configuration scopes" section documenting the four-tier hierarchy (Managed → Command line → Local → Project → User), with a "What uses scopes" table mapping features like subagents, MCP servers, and plugins to their file locations per scope.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `hooks.md` | Modified | +129/-52 | Added `CwdChanged` and `FileChanged` event reference sections with full schemas; updated matcher table, decision control table, and event type support table |
| `plugins-reference.md` | Modified | +95/-45 | Added `userConfig` and `channels` manifest fields with schemas and examples |
| `hooks-guide.md` | Modified | +88/-39 | Added "Reload environment when directory or files change" example section; updated hook events table |
| `settings.md` | Modified | +66/-57 | Added Configuration scopes section with four-tier hierarchy and scope feature table |
| `commands.md` | Modified | +67/-67 | Table reformatting; added `/loop` to bundled skills list; updated `/plan`, `/copy`, `/status` descriptions |
| `vs-code.md` | Modified | +25/-0 | Added "Launch a VS Code tab from other tools" section with URI handler documentation |
| `channels.md` | Modified | +27/-6 | Added `allowedChannelPlugins` enterprise setting section; restructured enterprise controls table |
| `memory.md` | Modified | +19/-5 | Added AGENTS.md interop section |
| `interactive-mode.md` | Modified | +14/-4 | Updated keybindings (`Ctrl+X Ctrl+K`, `Ctrl+X Ctrl+E`, `Option+O`); added transcript viewer shortcuts; clarified background task output mechanism |
| `keybindings.md` | Modified | +14/-12 | Minor updates to keybinding action table |
| `cli-reference.md` | Modified | +18/-17 | Added `claude plugin` as a top-level command |
| `sub-agents.md` | Modified | +9/-1 | Minor documentation updates |
| `env-vars.md` | Modified | +3/-1 | Added `CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK` and `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`; updated `CLAUDE_ENV_FILE` description |
| `monitoring-usage.md` | Modified | +3/-2 | Minor updates |
| `sandboxing.md` | Modified | +2/-0 | Minor additions |
| `channels-reference.md` | Modified | +1/-1 | Added note that Team/Enterprise admins can use `allowedChannelPlugins` as alternative to official submission |
| `features-overview.md` | Modified | +1/-1 | Fixed anchor link for `.claude/rules/` |
| `skills.md` | Modified | +1/-1 | Minor update |
| `tools-reference.md` | Modified | +1/-1 | Minor update |
| `changelog.md` | Modified | +0/-2 | Removed two changelog entries (`disableDeepLinkRegistration` and transcript search) |

---

*Generated from Claude Code CLI documentation changes detected on 2026-03-26*
