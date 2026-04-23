# Claude Code Documentation Changes — 2026-04-23

## Summary

This update introduces a new administrator deployment guide, a `PostToolBatch` hook event, MCP tool hooks, custom color themes, one-off scheduled routines, and Vim visual mode. Across 29 modified pages and 1 new page, notable changes include the `/cost` → `/usage` command rename (with aliases retained), a `$defaults` sentinel for auto mode configuration, a new `claude install` CLI command, and new enterprise settings for WSL/Windows policy inheritance.

---

## Significant Changes

### New: Administrator Deployment Guide

- **`admin-setup.md` — Organization deployment decision map**: A new top-level page for IT administrators deploying Claude Code at org scale. Covers provider selection, four managed-settings delivery mechanisms, enforcement controls, usage visibility, and data handling — each row in a decision table links to the relevant reference page.
  > "Claude Code enforces organization policy through managed settings that take precedence over local developer configuration. You deliver those settings from the Claude admin console, your mobile device management (MDM) system, or a file on disk."

  Key content:
  - Priority order of managed settings: server-managed (highest) → plist/registry → file-based → Windows user registry (lowest)
  - New `wslInheritsWindowsSettings` setting: set in Windows HKLM or `C:\Program Files\ClaudeCode\managed-settings.json` to extend Windows policy to WSL
  - Enforcement control table covering permissions, sandboxing, MCP server restrictions, plugin marketplace restrictions, hook restrictions, and version floor
  - Verification: developers run `/status` to confirm which managed settings source is active: `(remote)`, `(plist)`, `(HKLM)`, `(HKCU)`, or `(file)`
  - *Implication*: Admins now have a single starting page instead of having to assemble the deployment picture from multiple reference pages.
  - *Source*: [admin-setup.md](https://code.claude.com/docs/en/admin-setup.md)

---

### Hooks

- **New `PostToolBatch` hook event**: Fires exactly once after all parallel tool calls in a batch resolve, before the next model call. `PostToolUse` fires per-tool (concurrently); `PostToolBatch` fires once with the full set. Supports all five hook types and `decision: "block"` to halt the agentic loop.
  > "PostToolBatch fires exactly once with the full batch, so it is the right place to inject context that depends on the set of tools that ran rather than on any single tool. There is no matcher for this event."

  The batch input schema includes `tool_calls` — an array with `tool_name`, `tool_input`, `tool_use_id`, and `tool_response` for every call. `tool_response` is the serialized `tool_result` content the model sees (distinct from `PostToolUse`'s structured `Output` object).
  - *Implication*: Enables batch-level linting summaries, cross-file consistency checks, and context injection that needs to know what the full set of parallel edits was.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md)

- **New `mcp_tool` hook type**: Calls a tool on an already-connected MCP server as a hook handler. The tool's text output is processed identically to command-hook stdout. Supports `${path}` substitution in the `input` field.
  > "call a tool on an already-connected MCP server. The tool's text output is treated like command-hook stdout."

  Fields: `server` (required, MCP server name), `tool` (required, tool name), `input` (optional, arguments with `${path}` interpolation). If the server is not connected or the tool returns `isError: true`, the hook produces a non-blocking error and execution continues.
  - *Implication*: Security scanning, compliance checking, or any MCP-server capability can now be wired directly into hook events without a wrapper shell script.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md)

- **`if` field extended to `PermissionDenied`**: The `if` filter field on hook handlers now works on `PermissionDenied` events in addition to `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, and `PermissionRequest`.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md), [hooks-guide.md](https://code.claude.com/docs/en/hooks-guide.md)

- **`SessionStart` now supports `mcp_tool` hooks**: Previously only `command` hooks were supported on `SessionStart`. The `Setup` event also supports `command` and `mcp_tool`, but not `http`, `prompt`, or `agent`.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md)

---

### Custom Color Themes

- **Custom theme support (`~/.claude/themes/`)**: Users can now create JSON color theme files in `~/.claude/themes/`. Each file specifies a `base` preset (`dark`, `light`, `dark-daltonized`, `light-daltonized`, `dark-ansi`, `light-ansi`) and an `overrides` map of color tokens. Requires Claude Code v2.1.118+.
  > "Claude Code watches `~/.claude/themes/` and reloads when a file changes, so edits made in your editor apply to a running session without a restart."

  The `/theme` command now shows local custom themes, plugin-contributed themes, and a **New custom theme…** entry. Selecting a custom theme stores `custom:<slug>` as the preference. `Ctrl+E` on any custom theme in the picker opens it for editing. Color values accept `#rrggbb`, `#rgb`, `rgb(r,g,b)`, `ansi256(n)`, or `ansi:<name>`.

  Example:
  ```json
  {
    "name": "Dracula",
    "base": "dark",
    "overrides": {
      "claude": "#bd93f9",
      "error": "#ff5555",
      "success": "#50fa7b"
    }
  }
  ```
  - *Implication*: Teams and plugin authors can now distribute named color themes; users can iterate on themes without restarting their session.
  - *Source*: [terminal-config.md](https://code.claude.com/docs/en/terminal-config.md)

- **Plugins can ship themes**: Plugin manifests now support a `themes/` component path. Plugin themes appear in `/theme` alongside built-ins and local themes. Pressing `Ctrl+E` on a plugin theme copies it into `~/.claude/themes/` for local editing. Selecting a plugin theme persists `custom:<plugin-name>:<slug>`.
  - *Source*: [plugins-reference.md](https://code.claude.com/docs/en/plugins-reference.md)

---

### `/usage` Command (Replaces `/cost` Terminology)

- **`/usage` is now the canonical command; `/cost` and `/stats` become aliases**:
  - `/cost` → now documented as "Alias for `/usage`"
  - `/stats` → now documented as "Alias for `/usage`. Opens on the Stats tab"
  - `/usage` → now documented as "Show session cost, plan usage limits, and activity stats"

  > "The Session block in `/usage` shows API token usage and is intended for API users. Claude Max and Pro subscribers have usage included in their subscription, so the session cost figure isn't relevant for billing purposes. Subscribers see plan usage bars and activity stats on the same screen."

  The `costs.md` section is renamed from "Using the `/cost` command" to "Using the `/usage` command". All cross-references in `~/.claude/stats-cache.json` descriptions, remote-control docs, and context-management guides are updated to `/usage`.
  - *Implication*: Existing sessions using `/cost` or `/stats` continue to work unchanged (they are aliases). The `/usage` command consolidates what was previously split across two commands.
  - *Source*: [commands.md](https://code.claude.com/docs/en/commands.md), [costs.md](https://code.claude.com/docs/en/costs.md)

---

### Routines: One-Off Scheduled Runs

- **Routines can now be scheduled to fire once at a specific future time**: In addition to recurring cadences, a schedule trigger can be set as a one-off timestamp. After it fires, the routine auto-disables and the web UI marks it as **Ran**.
  > "A one-off schedule fires the routine a single time at a specific timestamp. Use it to remind yourself later in the week, to open a cleanup PR after a rollout finishes, or to kick off a follow-up task when an upstream change lands."

  Create from the CLI using natural language:
  ```
  /schedule tomorrow at 9am, summarize yesterday's merged PRs
  /schedule in 2 weeks, open a cleanup PR that removes the feature flag
  ```
  One-off runs do not count against the daily routine run cap but do draw down regular subscription usage.
  - *Implication*: Routines are no longer purely recurring; they can now be used as deferred one-shot tasks without needing a separate workflow.
  - *Source*: [routines.md](https://code.claude.com/docs/en/routines.md)

---

### Vim Visual Mode

- **Vim mode now supports visual selection (`v`/`V`)**:
  > "Press `v` for character-wise selection or `V` for line-wise selection. Motions extend the selection, and operators act on it directly."

  New operators in visual mode: `d`/`x` (delete), `y` (yank), `c`/`s` (change), `p` (replace with register), `r{char}` (replace each char), `~`/`u`/`U` (case toggle), `>`/`<` (indent), `J` (join lines), `o` (swap cursor/anchor), text objects (`iw`, `aw`, `i"`, etc.), `v`/`V` (toggle character-wise/line-wise or exit). Block-wise visual mode (`Ctrl+V`) is not supported.

  The statusline `vim.mode` field now reports `VISUAL` and `VISUAL LINE` in addition to `NORMAL` and `INSERT`.
  - *Source*: [interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md), [statusline.md](https://code.claude.com/docs/en/statusline.md)

---

### Auto Mode: `$defaults` Sentinel

- **`"$defaults"` in `environment`, `allow`, and `soft_deny` arrays splices in built-in rules**: Previously, setting any of these arrays replaced the entire default list, which meant force-push blocking, data exfiltration rules, etc. were silently dropped. Now you include the literal string `"$defaults"` to inherit built-in rules at that position.

  > "To keep the built-in rules while adding your own, include the literal string `"$defaults"` in the array. The default rules are spliced in at that position, so your custom rules can go before or after them, and you continue to inherit updates as the built-in list changes across releases."

  The previous `claude auto-mode defaults` copy-paste workflow is now a fallback for when you need to remove or rewrite a built-in rule. The `Danger` callout is repositioned: it now warns about what happens when you *omit* `"$defaults"`, not about the act of customizing.

  `claude auto-mode config` now shows `"$defaults"` expanded in place for verification.
  - *Implication*: Customizing auto mode classifier rules is now much safer — adding entries no longer silently removes security defaults.
  - *Source*: [auto-mode-config.md](https://code.claude.com/docs/en/auto-mode-config.md), [settings.md](https://code.claude.com/docs/en/settings.md)

---

### CLI and Installation

- **New `claude install [version]` command**: Install or reinstall the native binary at a specific version. Accepts a version string like `2.1.118`, or the strings `stable` or `latest`.
  > `claude install [version]` — Install or reinstall the native binary. Accepts a version like `2.1.118`, or `stable` or `latest`.
  - *Source*: [cli-reference.md](https://code.claude.com/docs/en/cli-reference.md)

- **New `DISABLE_UPDATES` environment variable**: Blocks all update paths including manual `claude update` and `claude install`. Stricter than `DISABLE_AUTOUPDATER`, which only stops the background check. `DISABLE_UPDATES` is intended for organizations that distribute Claude Code through their own channels and need users to stay on the provided version.
  - *Source*: [env-vars.md](https://code.claude.com/docs/en/env-vars.md), [setup.md](https://code.claude.com/docs/en/setup.md)

- **`--continue` and `--resume` now include sessions from `/add-dir` directories**: If a session was started from a different directory but added the current directory with `/add-dir`, it now appears in the `--continue` and `--resume` pickers and the `/resume` interactive list.
  > "Includes sessions that added this directory with `/add-dir`"
  - *Source*: [cli-reference.md](https://code.claude.com/docs/en/cli-reference.md), [commands.md](https://code.claude.com/docs/en/commands.md)

---

### Plugin System

- **`claude plugin tag` CLI command**: Creates a release git tag in the `{plugin-name}--v{version}` format required for semver constraint resolution. Validates plugin contents, checks that `plugin.json` and the marketplace entry agree on the version, requires a clean working tree, and refuses if the tag already exists. Options: `--push`, `--dry-run`, `-f`/`--force`.
  - *Source*: [plugins-reference.md](https://code.claude.com/docs/en/plugins-reference.md), [plugin-dependencies.md](https://code.claude.com/docs/en/plugin-dependencies.md)

- **Plugin version management overhauled**: The `version` field in `plugin.json` is now documented as optional. Two explicit strategies are now documented:
  - **Explicit version** (`"version": "2.1.0"` in `plugin.json`): users only get updates when the field is bumped
  - **Commit-SHA version** (omit `version`): every new commit is treated as a new version — suitable for internal or actively-developed plugins

  > "If you set `version` in `plugin.json`, you must bump it every time you want users to receive changes. Pushing new commits alone is not enough, because Claude Code sees the same version string and keeps the cached copy."
  - *Source*: [plugins-reference.md](https://code.claude.com/docs/en/plugins-reference.md), [plugin-marketplaces.md](https://code.claude.com/docs/en/plugin-marketplaces.md), [plugins.md](https://code.claude.com/docs/en/plugins.md)

- **New "Pin dependency versions" section in plugin-marketplaces.md**: Cross-references the `{plugin-name}--v{version}` git-tag convention and semver constraint syntax from plugin-marketplaces to plugin-dependencies.
  - *Source*: [plugin-marketplaces.md](https://code.claude.com/docs/en/plugin-marketplaces.md)

---

### Enterprise Settings

- **New `wslInheritsWindowsSettings` setting**: When `true` in the Windows HKLM registry key or `C:\Program Files\ClaudeCode\managed-settings.json`, WSL reads managed settings from the Windows policy chain in addition to `/etc/claude-code`. Only honored in admin-writable locations.
  - *Source*: [settings.md](https://code.claude.com/docs/en/settings.md), [permissions.md](https://code.claude.com/docs/en/permissions.md)

---

## Notable Details

- **Agent teams: `broadcast` removed**: The `broadcast` concept ("send to all teammates simultaneously") is removed from the agent teams docs. It's replaced by: "send one message per recipient." This simplifies the mental model and removes a cost-amplifying shortcut.
  - *Source*: [agent-teams.md](https://code.claude.com/docs/en/agent-teams.md)

- **`/color` syncs to claude.ai when Remote Control is connected**: The `/color` command description now notes that when Remote Control is active, the prompt bar color syncs to claude.ai/code.
  - *Source*: [commands.md](https://code.claude.com/docs/en/commands.md)

- **Auto mode opt-in behavior in mode cycle**: Cycling `Shift+Tab` to auto mode now shows an opt-in prompt until accepted. Selecting **No, don't ask again** removes auto from the cycle permanently.
  - *Source*: [permission-modes.md](https://code.claude.com/docs/en/permission-modes.md)

- **Keybindings: `Cmd+P`/`Cmd+T` removed; modifier key semantics clarified**: The defaults for `chat:modelPicker` and `chat:thinkingToggle` are now `Meta+P` and `Meta+T` only (no `Cmd+` variant). The `meta` key group now maps to Alt/Option. A new `cmd`/`super`/`win` group targets the OS command key but only in terminals that report the Super modifier (Kitty keyboard protocol, xterm `modifyOtherKeys`).
  - *Source*: [keybindings.md](https://code.claude.com/docs/en/keybindings.md)

- **Data usage: updated diagram, added encryption-at-rest table**: The diagram alt-text now references "distribution server" instead of "NPM". A new per-provider encryption-at-rest table is added (Anthropic API: AES-256 disk encryption with ZDR option; Bedrock: AWS KMS-backed AES-256; Vertex: Google-managed CMEK; Foundry: AES-256 via Anthropic infrastructure). TLS is now described as "TLS 1.2+" rather than just "TLS".
  - *Source*: [data-usage.md](https://code.claude.com/docs/en/data-usage.md)

- **LLM gateway: `_NAME` and `_DESCRIPTION` env vars now work for `ANTHROPIC_BASE_URL` gateways**: Previously documented as third-party-provider-only, these variables now also take effect when `ANTHROPIC_BASE_URL` points to an LLM gateway. No effect when connecting directly to `api.anthropic.com`.
  - *Source*: [model-config.md](https://code.claude.com/docs/en/model-config.md)

- **Features overview: new "Hook vs Skill" comparison tab**: A new tab directly contrasts hooks (guaranteed to fire, zero context cost unless output returned) against skills (Claude interprets and applies; loads into context). Includes the note: "Put guardrails in hooks. An instruction like 'never edit `.env`' in CLAUDE.md or a skill is a request, not a guarantee. A `PreToolUse` hook that blocks the edit is enforcement."
  - *Source*: [features-overview.md](https://code.claude.com/docs/en/features-overview.md)

- **`availableModels` no longer mentions Config tool**: The setting description no longer lists the "Config tool" as a way to switch models; only `/model`, `--model`, and `ANTHROPIC_MODEL` are mentioned. This indicates the Config tool route has been removed.
  - *Source*: [model-config.md](https://code.claude.com/docs/en/model-config.md), [settings.md](https://code.claude.com/docs/en/settings.md)

---

## New Pages

- **[admin-setup.md](https://code.claude.com/docs/en/admin-setup.md)** — Administrator deployment decision map covering API provider choice, managed settings delivery (server-managed, plist/registry, file-based, Windows user registry), enforcement controls (permissions, sandboxing, MCP, plugins, hooks, version floor), usage visibility, data handling, and onboarding resources.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| admin-setup.md | New | +132 | Administrator deployment decision map |
| hooks.md | Modified | +150/-47 | PostToolBatch event, mcp_tool hook type, updated lifecycle diagram |
| plugins-reference.md | Modified | +68/-32 | Themes section, plugin tag command, version management overhaul |
| plugin-marketplaces.md | Modified | +33/-15 | Pin dependency versions section, version resolution clarification |
| features-overview.md | Modified | +30/-10 | Hook vs Skill comparison tab, updated hook description |
| terminal-config.md | Modified | +36/-2 | Custom theme creation section |
| routines.md | Modified | +24/-4 | One-off scheduled run support |
| interactive-mode.md | Modified | +31/-9 | Visual mode section (v/V selection) |
| hooks-guide.md | Modified | +21/-19 | PostToolBatch and mcp_tool additions |
| claude-directory.md | Modified | +23/-2 | themes/ folder, /usage reference updates |
| data-usage.md | Modified | +13/-4 | Encryption-at-rest table, TLS 1.2+, updated diagram |
| permissions.md | Modified | +14/-13 | wslInheritsWindowsSettings managed-only setting |
| auto-mode-config.md | Modified | +15/-11 | $defaults sentinel, reorganized danger callout |
| keybindings.md | Modified | +8/-6 | Modifier key clarification, removed Cmd+ defaults |
| plugin-dependencies.md | Modified | +8/-5 | claude plugin tag command |
| plugins.md | Modified | +7/-7 | Version management strategy choice |
| commands.md | Modified | +6/-6 | /usage canonical, /cost and /stats as aliases |
| costs.md | Modified | +5/-5 | Renamed /cost section to /usage |
| settings.md | Modified | +3/-2 | wslInheritsWindowsSettings, $defaults in autoMode example |
| cli-reference.md | Modified | +3/-2 | claude install command, /add-dir session inclusion |
| setup.md | Modified | +2/-0 | DISABLE_UPDATES vs DISABLE_AUTOUPDATER clarification |
| env-vars.md | Modified | +2/-1 | DISABLE_UPDATES new variable |
| model-config.md | Modified | +2/-2 | LLM gateway NAME/DESCRIPTION vars, remove Config tool from availableModels |
| agent-teams.md | Modified | +1/-5 | Removed broadcast concept |
| common-workflows.md | Modified | +1/-1 | /add-dir session inclusion in /resume |
| desktop-scheduled-tasks.md | Modified | +1/-1 | One-off scheduling mention |
| permission-modes.md | Modified | +1/-1 | Auto mode opt-in prompt behavior |
| remote-control.md | Modified | +1/-1 | /cost → /usage in remote commands list |
| scheduled-tasks.md | Modified | +1/-1 | One-off scheduling mention |
| statusline.md | Modified | +1/-1 | VISUAL and VISUAL LINE vim modes |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-23*
