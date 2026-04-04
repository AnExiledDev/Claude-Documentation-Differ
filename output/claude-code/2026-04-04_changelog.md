# Claude Code Documentation Changes — 2026-04-04

## Summary

15 pages were modified in this update with 142 additions and 89 deletions. The most substantive changes cover a new interactive Bedrock setup wizard, a new `forceRemoteSettingsRefresh` fail-closed enforcement mechanism for managed deployments, a new `--remote-control-session-name-prefix` flag, multi-line shell execution blocks in skills, and the removal of two slash commands (`/pr-comments` in v2.1.91 and `/vim` in v2.1.92).

## Significant Changes

### Configuration & Enterprise Policy

- **Fail-closed startup enforcement (`forceRemoteSettingsRefresh`)**: A new managed setting blocks CLI startup until remote managed settings are freshly fetched from the server. If the fetch fails, the CLI exits rather than proceeding with cached or no settings.
  > "When this setting is active, the CLI blocks at startup until remote settings are freshly fetched. If the fetch fails, the CLI exits rather than proceeding without the policy. This setting self-perpetuates: once delivered from the server, it is also cached locally so that subsequent startups enforce the same behavior even before the first successful fetch of a new session."
  - *Implication*: Enterprises requiring strict policy enforcement can guarantee managed settings are always applied at startup. Requires connectivity to `api.anthropic.com`; if unreachable, users cannot start Claude Code.
  - *Source*: [server-managed-settings.md](https://code.claude.com/docs/en/server-managed-settings.md), [permissions.md](https://code.claude.com/docs/en/permissions.md), [settings.md](https://code.claude.com/docs/en/settings.md)

- **New `disableSkillShellExecution` setting**: Disables inline shell execution for `` !`...` `` and ` ```! ` blocks in skills and custom commands from user, project, plugin, or additional-directory sources.
  > "Commands are replaced with `[shell command execution disabled by policy]` instead of being run. Bundled and managed skills are not affected. Most useful in managed settings where users cannot override it."
  - *Implication*: Managed deployments can lock down shell execution within user-defined skills without affecting built-in functionality.
  - *Source*: [settings.md](https://code.claude.com/docs/en/settings.md), [skills.md](https://code.claude.com/docs/en/skills.md)

### Amazon Bedrock

- **Interactive Bedrock setup wizard**: A new guided wizard is available from the login screen and via the `/setup-bedrock` command for configuring Bedrock credentials without manual environment variable editing.
  > "Select **3rd-party platform** at the `claude` login prompt, then choose **Amazon Bedrock** to launch it. The wizard guides you through each step and writes the resulting configuration to your settings: AWS authentication, Region selection, Credential verification, Model pinning."
  - *Implication*: First-time Bedrock users get a streamlined setup path. Returning users can update credentials, region, or model pins via `/setup-bedrock`.
  - *Source*: [amazon-bedrock.md](https://code.claude.com/docs/en/amazon-bedrock.md), [commands.md](https://code.claude.com/docs/en/commands.md)

### Remote Control

- **New `--remote-control-session-name-prefix` flag**: Controls the prefix used for auto-generated Remote Control session names. Previously, auto-generated names always used the machine hostname as the prefix with no way to override it via a flag.
  > "Prefix for auto-generated Remote Control session names when no explicit name is set. Defaults to your machine's hostname, producing names like `myhost-graceful-unicorn`."
  - *Implication*: Useful for distinguishing sessions from multiple machines or environments sharing the same Remote Control pool. The environment variable `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX` provides a persistent alternative.
  - *Source*: [remote-control.md](https://code.claude.com/docs/en/remote-control.md), [cli-reference.md](https://code.claude.com/docs/en/cli-reference.md), [env-vars.md](https://code.claude.com/docs/en/env-vars.md)

- **Clarified session title fallback order**: The fourth fallback for a Remote Control session name is now an auto-generated name (e.g., `myhost-graceful-unicorn`) rather than the first prompt message. The prompt still updates the title once sent, but no longer serves as the initial fallback.
  - *Source*: [remote-control.md](https://code.claude.com/docs/en/remote-control.md)

### Skills

- **Multi-line shell blocks (` ```! `)**: Skills now support fenced code blocks opened with ` ```! ` for multi-line inline shell execution, in addition to the existing single-line `` !`command` `` form.
  > "For multi-line commands, use a fenced code block opened with ` ```! ` instead of the inline form."
  - *Implication*: Skills that previously needed workarounds for multi-command shell snippets can now use a cleaner block syntax.
  - *Source*: [skills.md](https://code.claude.com/docs/en/skills.md)

### MCP

- **Clarified `anthropic/maxResultSizeChars` behavior**: The annotation raises a per-tool persist-to-disk threshold but does not bypass the global `MAX_MCP_OUTPUT_TOKENS` cap.
  > "The annotation raises the per-tool persist threshold but does not bypass the global `MAX_MCP_OUTPUT_TOKENS` limit, which defaults to 25,000 tokens or roughly 100,000 characters. To return results larger than that, users must also raise `MAX_MCP_OUTPUT_TOKENS`."
  - *Implication*: MCP server authors relying solely on the annotation to deliver very large results need to also account for the token cap.
  - *Source*: [mcp.md](https://code.claude.com/docs/en/mcp.md)

### Removed / Deprecated Commands

- **`/pr-comments` removed (v2.1.91+)**: The command is removed as of v2.1.91. The documentation now directs users to ask Claude directly to view pull request comments instead.
  - *Source*: [commands.md](https://code.claude.com/docs/en/commands.md)

- **`/vim` removed (v2.1.92+)**: The toggle command is removed as of v2.1.92. Vim mode is now configured exclusively through `/config` → Editor mode.
  > "Removed in v2.1.92. To toggle between Vim and Normal editing modes, use `/config` → Editor mode."
  - *Implication*: Any scripts or documentation referencing `/vim` need to be updated. The underlying `editorMode` setting in `~/.claude.json` is unchanged.
  - *Source*: [commands.md](https://code.claude.com/docs/en/commands.md), [interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md), [keybindings.md](https://code.claude.com/docs/en/keybindings.md), [terminal-config.md](https://code.claude.com/docs/en/terminal-config.md)

## Notable Details

- **`/release-notes` updated**: The command now opens an interactive version picker rather than showing all versions in a single scroll. "Select a specific version to see its release notes, or choose to show all versions."
- **WSL sandboxing note added**: The troubleshooting page documents that sandboxed commands cannot launch Windows binaries (e.g., `cmd.exe`, `powershell.exe`, or executables under `/mnt/c/`). The workaround is to add them to `excludedCommands`. — *Source*: [troubleshooting.md](https://code.claude.com/docs/en/troubleshooting.md)
- **`editorMode` setting description updated**: The entry no longer states "Written automatically when you run `/vim`" (consistent with `/vim` removal). The `/config` UI label is now documented as "Editor mode" rather than "Key binding mode". — *Source*: [settings.md](https://code.claude.com/docs/en/settings.md)
- **`data-usage.md` link wording**: Minor wording change; "read more" link updated to "see settings reference".

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| [amazon-bedrock.md](https://code.claude.com/docs/en/amazon-bedrock.md) | Modified | +11 / -0 | New "Set up with the interactive wizard" section |
| [cli-reference.md](https://code.claude.com/docs/en/cli-reference.md) | Modified | +63 / -62 | Added `--remote-control-session-name-prefix` flag; table reformatted |
| [commands.md](https://code.claude.com/docs/en/commands.md) | Modified | +4 / -3 | `/pr-comments` and `/vim` marked removed; `/setup-bedrock` added; `/release-notes` updated |
| [data-usage.md](https://code.claude.com/docs/en/data-usage.md) | Modified | +1 / -1 | Minor link text update |
| [env-vars.md](https://code.claude.com/docs/en/env-vars.md) | Modified | +1 / -0 | Added `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX` variable |
| [interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md) | Modified | +1 / -1 | Removed `/vim` reference; now points to `/config` → Editor mode |
| [keybindings.md](https://code.claude.com/docs/en/keybindings.md) | Modified | +1 / -1 | Vim mode activation description updated to reflect `/vim` removal |
| [mcp.md](https://code.claude.com/docs/en/mcp.md) | Modified | +5 / -3 | Clarified `anthropic/maxResultSizeChars` annotation vs. `MAX_MCP_OUTPUT_TOKENS` |
| [permissions.md](https://code.claude.com/docs/en/permissions.md) | Modified | +1 / -0 | Added `forceRemoteSettingsRefresh` to managed-only settings table |
| [remote-control.md](https://code.claude.com/docs/en/remote-control.md) | Modified | +11 / -8 | New `--remote-control-session-name-prefix` flag; session title fallback order updated |
| [server-managed-settings.md](https://code.claude.com/docs/en/server-managed-settings.md) | Modified | +23 / -7 | New "Enforce fail-closed startup" section; security table updated |
| [settings.md](https://code.claude.com/docs/en/settings.md) | Modified | +3 / -1 | Added `disableSkillShellExecution` and `forceRemoteSettingsRefresh`; `editorMode` description updated |
| [skills.md](https://code.claude.com/docs/en/skills.md) | Modified | +14 / -1 | New "Environment" section documenting ` ```! ` multi-line blocks; `disableSkillShellExecution` policy noted |
| [terminal-config.md](https://code.claude.com/docs/en/terminal-config.md) | Modified | +1 / -1 | Vim Mode activation updated to reference `/config` → Editor mode |
| [troubleshooting.md](https://code.claude.com/docs/en/troubleshooting.md) | Modified | +2 / -0 | Added WSL sandbox note about Windows binary restrictions |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-04*
