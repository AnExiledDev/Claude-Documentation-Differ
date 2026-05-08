# Claude Code Documentation Changes — 2026-03-21

## Summary

Version 2.1.81 was released with 28 changelog entries covering a new `--bare` scripting flag, a `--channels` permission relay for remote approvals, numerous bug fixes, and behavioral changes to plan mode and Windows streaming. Alongside the release, documentation was updated to clarify admin controls for Remote Control and web sessions, add new IDE auto-connect settings, and add a comparison table to the channels page. A follow-up update corrected the canonical name of the `--allowedTools` flag in the GitHub Actions reference.

---

## Significant Changes

### New Features (v2.1.81)

- **`--bare` flag for headless scripting**: A new flag strips all interactive subsystems from `-p` (print/SDK mode) calls — no hooks, LSP, plugin sync, or skill directory walks execute. Requires `ANTHROPIC_API_KEY` or `apiKeyHelper` via `--settings`; OAuth and keychain auth are explicitly disabled. Auto-memory is fully disabled.
  > Added `--bare` flag for scripted `-p` calls — skips hooks, LSP, plugin sync, and skill directory walks; requires `ANTHROPIC_API_KEY` or an `apiKeyHelper` via `--settings` (OAuth and keychain auth disabled); auto-memory fully disabled
  - *Implication*: Enables faster, more deterministic CI/scripting pipelines where side-effects from plugins and memory are undesirable.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`--channels` permission relay**: Channel servers that declare the `permission` capability can now forward tool approval prompts to your phone, enabling unattended sessions to pause and request human approval remotely.
  > Added `--channels` permission relay — channel servers that declare the permission capability can forward tool approval prompts to your phone
  - *Implication*: Removes the need for `--dangerously-skip-permissions` in setups where a human is available on a mobile channel.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **MCP OAuth now supports CIMD (SEP-991)**: MCP OAuth flow was updated to support Client ID Metadata Document for servers that don't support Dynamic Client Registration.
  > Updated MCP OAuth to support Client ID Metadata Document (CIMD / SEP-991) for servers without Dynamic Client Registration
  - *Implication*: Broader MCP server compatibility without requiring DCR support.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### GitHub Actions CLI Flag

- **`--allowedTools` is now the canonical flag name (was `--allowed-tools`)**: The GitHub Actions reference documentation updated the flag name from kebab-case to camelCase, and explicitly documents the hyphenated form as a still-working alias.
  > `--allowedTools`: Comma-separated list of allowed tools. The `--allowed-tools` alias also works.
  - *Implication*: Existing workflows using `--allowed-tools` continue to work without modification, but new scripts should prefer `--allowedTools` to match the documented canonical form.
  - *Source*: [GitHub Actions](https://code.claude.com/docs/en/github-actions.md)

### Behavioral Changes (v2.1.81)

- **Plan mode hides "clear context" by default**: The "clear context" option in plan mode is now hidden. Restore it with `"showClearContextOnPlanAccept": true` in settings.
  > Changed plan mode to hide the "clear context" option by default (restore with `"showClearContextOnPlanAccept": true`)
  - *Implication*: Teams relying on this UI option must explicitly re-enable it via settings.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Line-by-line streaming disabled on Windows/WSL**: Response streaming is disabled on Windows (including WSL in Windows Terminal) due to rendering issues.
  > Disabled line-by-line response streaming on Windows (including WSL in Windows Terminal) due to rendering issues
  - *Implication*: Windows users will see responses rendered differently; this is a regression workaround, not a permanent design change.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Configuration

- **Two new global config settings documented**: `settings.md` now documents `autoConnectIde` and `autoInstallIdeExtension` in the global config settings table (stored in `~/.claude.json`).
  > `autoConnectIde` — Automatically connect to a running IDE when Claude Code starts from an external terminal. Default: `false`. Appears in `/config` as **Auto-connect to IDE (external terminal)**
  >
  > `autoInstallIdeExtension` — Automatically install the Claude Code IDE extension when running from a VS Code terminal. Default: `true`. Appears in `/config` as **Auto-install IDE extension**
  - *Implication*: These were previously undocumented; developers managing multi-terminal or external-terminal setups can now configure IDE connectivity explicitly.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL` now cross-references settings key**: The env var docs note that this is equivalent to setting `autoInstallIdeExtension` to `false`.
  > Skip auto-installation of IDE extensions. Equivalent to setting [`autoInstallIdeExtension`](/en/settings#global-config-settings) to `false`
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

### Permissions & Admin Controls

- **`allow_remote_sessions` managed settings key removed**: The previously documented `allow_remote_sessions` key has been removed from the managed-only settings table. Access to Remote Control and web sessions is now controlled through the Admin Settings UI, not via managed settings JSON.
  > Access to [Remote Control](/en/remote-control) and [web sessions](/en/claude-code-on-the-web) is not controlled by a managed settings key. On Team and Enterprise plans, an admin enables or disables these features in [Claude Code admin settings](https://claude.ai/admin-settings/claude-code).
  - *Implication*: Admins managing these features via managed settings JSON need to switch to the UI-based admin console. Any automation relying on `allow_remote_sessions` in managed settings will no longer have effect.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

- **Desktop admin settings reorganized**: The admin settings list in `desktop.md` was reworked with clearer labels and new entries:
  - "Enable or disable the Code tab" → renamed to **"Code in the desktop"**
  - New: **"Code in the web"** — enable or disable web sessions
  - New: **"Remote Control"** — enable or disable Remote Control
  - Removed: "Disable Claude Code on the web" (replaced by the above)
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

- **Remote Control troubleshooting clarified**: The error message guidance for "Remote Control is disabled by your organization's policy" now recommends running `/status` first to identify the auth method in use. The admin toggle for Remote Control is clarified as a standalone server-side setting, no longer described as depending on the "Claude Code on the web" toggle.
  > Run `/status` first to see which login method and subscription you're using.
  > This is a server-side organization setting, not a [managed settings](/en/permissions#managed-only-settings) key.
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

### Channels

- **New "How channels compare" section**: `channels.md` gained a comparison table distinguishing channels from Claude Code on the web, Claude in Slack, standard MCP servers, and Remote Control.
  > Channels fill the gap in that list by pushing events from non-Claude sources into your already-running local session.

  | Feature | What it does | Good for |
  |---|---|---|
  | Claude Code on the web | Runs tasks in a fresh cloud sandbox | Delegating self-contained async work |
  | Claude in Slack | Spawns a web session from an `@Claude` mention | Starting tasks from team conversation context |
  | Standard MCP server | Claude queries it; nothing pushed to session | On-demand read/query access |
  | Remote Control | You drive your local session from claude.ai | Steering an in-progress session while away |

  - *Implication*: Clarifies when to choose channels vs. other integration approaches.
  - *Source*: [Channels](https://code.claude.com/docs/en/channels.md)

- **MCP config path guidance updated in channels-reference**: The step instructing users to register a channel server now correctly references `~/.claude.json` for user-level config (instead of implying `~/.mcp.json`).
  > For user-level config in `~/.claude.json`, use the full absolute path so the server can be found from any project
  - *Source*: [Channels Reference](https://code.claude.com/docs/en/channels-reference.md)

### Sandboxing

- **Clarification on `.` path resolution in allowRead**: The sandboxing docs now explicitly note that `.` in `allowRead` resolves relative to where the settings file lives — project root for project settings, `~/.claude` for user settings.
  > The `.` in `allowRead` resolves to the project root because this configuration lives in project settings. If you placed the same configuration in `~/.claude/settings.json`, `.` would resolve to `~/.claude` instead, and project files would remain blocked by the `denyRead` rule.
  - *Implication*: Prevents a common misconfiguration where user-level sandbox rules unintentionally fail to allow project file access.
  - *Source*: [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)

### Plugins

- **Plugin catalog link added**: The official Anthropic marketplace section now links to the plugin catalog at `claude.com/plugins`.
  > Run `/plugin` and go to the **Discover** tab to browse what's available, or view the catalog at [claude.com/plugins](https://claude.com/plugins).
  - *Source*: [Discover Plugins](https://code.claude.com/docs/en/discover-plugins.md)

---

## Notable Details

- **v2.1.81 bug fix count**: 14 distinct bug fixes in this release, notably:
  - Multi-session OAuth token refresh no longer forces re-authentication across concurrent sessions.
  - `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` now correctly suppresses the structured-outputs beta header (fixes 400 errors on proxy gateways forwarding to Vertex/Bedrock).
  - Node.js 18 crash fixed.
  - Worktree session resumption now switches back to the correct worktree.
  - VSCode: Windows PATH inheritance for Bash tool fixed (regression from v2.1.78).
  - Race condition in background agent task output polling resolved.

- **Plugin freshness**: Ref-tracked plugins now re-clone on every load to pick up upstream changes — a behavioral change that could affect startup time for users with ref-tracked plugins.

- **Skills docs**: The backtick command injection syntax (`` !`<command>` ``) had malformed escaping in the previous docs; the formatting was corrected.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +30/−0 | Added v2.1.81 release entry |
| channels.md | Modified | +19/−0 | New "How channels compare" section and ToC entry |
| settings.md | Modified | +8/−6 | Added `autoConnectIde` and `autoInstallIdeExtension` to global config table |
| skills.md | Modified | +4/−4 | Fixed backtick command syntax formatting |
| channels-reference.md | Modified | +3/−3 | Corrected MCP config path references (`~/.claude.json` vs `~/.mcp.json`) |
| remote-control.md | Modified | +3/−3 | Improved troubleshooting guidance; clarified admin toggle independence |
| desktop.md | Modified | +3/−2 | Reorganized admin settings list with new Remote Control and web session entries |
| permissions.md | Modified | +4/−1 | Removed `allow_remote_sessions` key; added Note about UI-based control |
| sandboxing.md | Modified | +3/−1 | Clarified `.` path resolution in `allowRead` per settings file location |
| discover-plugins.md | Modified | +1/−1 | Added link to plugin catalog at claude.com/plugins |
| env-vars.md | Modified | +1/−1 | Cross-referenced `autoInstallIdeExtension` setting from env var docs |
| github-actions.md | Modified | +1/−1 | Renamed `--allowed-tools` to `--allowedTools`; old name retained as alias |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-21*
