# Claude Code Documentation Changes — 2026-05-09

## Summary

Three documentation pages were updated to reflect releases v2.1.136 and v2.1.137. The most significant behavioral change is a correction to how `--resume` handles permission modes in hooks: it now restores the session's prior permission mode automatically (with documented exceptions), reversing previous guidance that required users to re-pass `--permission-mode` on resume. The setup page also gained a new upgrade instruction for npm users.

## Significant Changes

### Behavior Changes

- **`--resume` now restores permission mode automatically**: The hooks documentation changed a `<Warning>` to a `<Note>` and reversed the stated behavior. Previously, the docs warned that `--resume` does *not* restore the permission mode and required users to pass `--permission-mode` again manually.

  > `--resume` restores the permission mode that was active when the tool was deferred, so you do not need to pass `--permission-mode` again. The exceptions are `plan` and `bypassPermissions`, which are never carried over. Passing `--permission-mode` explicitly on resume overrides the restored value.

  - *Implication*: Developers using deferred tools with non-default permission modes no longer need to remember to re-pass `--permission-mode` on resume. The two exceptions (`plan` and `bypassPermissions`) must still be specified explicitly.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md)

### Configuration

- **New `settings.autoMode.hard_deny` setting** (v2.1.136): A new auto mode classifier rule that blocks actions unconditionally, regardless of user intent or allow exceptions.
  - *Implication*: Provides a stricter enforcement layer for auto mode beyond the existing allow/deny rules — useful in enterprise or security-sensitive deployments where certain actions must never be permitted.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **New `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL` env var** (v2.1.136): Re-enables the session quality survey for enterprises that capture responses via OpenTelemetry.
  - *Implication*: Enterprise deployments using OTel telemetry pipelines can opt back in to the session survey that was previously disabled for those environments.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **New `sandbox.bwrapPath` and `sandbox.socatPath` settings** (v2.1.133, carried in this diff): Allows specifying custom binary paths for bubblewrap and socat on Linux/WSL.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

### Installation

- **Explicit npm upgrade guidance added**: The setup page now documents the correct upgrade command for npm installations:

  > To upgrade an npm installation, run `npm install -g @anthropic-ai/claude-code@latest`. Avoid `npm update -g`, which respects the semver range from the original install and may not move you to the newest release.

  - *Implication*: `npm update -g` silently staying on older versions was likely a common support issue; this guidance prevents it without requiring any tool changes.
  - *Source*: [setup.md](https://code.claude.com/docs/en/setup.md)

### Bug Fixes (v2.1.136 — notable items)

- **MCP server persistence fix**: MCP servers configured in `.mcp.json`, plugins, and claude.ai connectors were silently disappearing after `/clear` in VS Code, JetBrains, and Agent SDK. Now fixed.
- **OAuth token race condition fix**: A concurrent credential write could overwrite a freshly-rotated OAuth token, forcing re-login. Fixed.
- **MCP OAuth refresh token fix**: Multiple remote MCP servers refreshing tokens concurrently would lose tokens. Users no longer need daily re-authentication.
- **`--resume`/`--continue` with underscores**: Sessions in project paths containing underscores were not found by `--resume`/`--continue`. Fixed.
- **Plan mode file write bypass**: Plan mode was not blocking file writes when a matching `Edit(...)` allow rule existed. Fixed.
- **WSL2 clipboard image paste**: Image paste from Windows clipboard now works via a PowerShell fallback when `xclip`/`wl-paste` cannot read image data.
- **`AskUserQuestion` multi-select**: Multi-select answers supplied as an array were being discarded. Fixed.
- **`CronList` output**: Was missing qualifiers and the scheduled prompt. Fixed.
- **Plugin `skills` entry bug**: A `skills` entry in `plugin.json` was hiding the plugin's default `skills/` directory; listing a file path now shows an error instead of failing silently.
- **`CLAUDE_ENV_FILE` hook env vars**: Env vars from `CLAUDE_ENV_FILE` in `SessionStart` hooks were going stale after `/resume` or `/clear`. Fixed.
- **Extended thinking 400 error**: An API 400 error occurred when extended thinking emitted a redacted thinking block after a tool call. Fixed.

### IDE / Platform

- **VS Code Windows activation fix** (v2.1.137): The VS Code extension was failing to activate on Windows. This is a standalone patch release.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +59/−0 | Added v2.1.137 and v2.1.136 release entries |
| hooks.md | Modified | +3/−3 | Corrected `--resume` permission mode behavior; changed Warning to Note |
| setup.md | Modified | +2/−0 | Added npm upgrade guidance (`npm install -g ... @latest`) |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-09*
