# Claude Code Documentation Changes — 2026-05-19

## Summary

Version 2.1.144 released on May 19, 2026, bringing 40+ bug fixes and quality-of-life improvements focused on background sessions, MCP stability, terminal rendering, and plugin management. The errors reference was expanded with two new sections covering organization-level subscription blocking and Usage Policy refusals. Minor clarifications were made to home-directory trust behavior in the security docs and glossary.

## Significant Changes

### Release: Version 2.1.144

- **`/resume` support for background sessions**: Background sessions started via `claude --bg` or agent view now appear in the `/resume` picker alongside interactive sessions, marked with `bg`.
  - *Implication*: Users managing background and interactive sessions no longer need separate recovery flows.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/model` is now per-session; press `d` to set default**: The `/model` command changes the model for the current session only. A new `d` keybinding in the model picker sets the default for new sessions.
  > `/model` now changes the model for the current session only; press `d` in the model picker to set a default for new sessions
  - *Implication*: This is a behavior change — previous behavior applied the model selection more broadly. Users who relied on `/model` to persist across sessions must now use `d` in the picker.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **"Extra usage" renamed to "usage credits"**: The `/extra-usage` command is now `/usage-credits`. The old name still works as an alias.
  > Renamed "extra usage" to "usage credits" across CLI copy; `/extra-usage` is now `/usage-credits` (old name still works)
  - *Implication*: No immediate migration required, but scripts or documentation referencing the old command should be updated.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Fixed startup hang on unreachable API (up to 75s)**: Side-channel API calls now time out after 15s instead of blocking startup indefinitely when `api.anthropic.com` is unreachable (e.g., captive portal, firewall, VPN).
  > Fixed startup hanging up to 75s when `api.anthropic.com` is unreachable (captive portal, firewall, VPN issues) — side-channel API calls now time out after 15s
  - *Implication*: Claude Code becomes usable much faster in network-restricted environments.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Fixed MCP paginated `tools/list` dropping tools**: MCP servers that return tools via paginated responses were silently only returning the first page. All pages are now fetched.
  > Fixed MCP servers with paginated `tools/list` responses only returning the first page, silently dropping tools
  - *Implication*: MCP integrations with large tool sets (exceeding one page) will now expose all their tools correctly.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Fixed `claude mcp list` silently failing on malformed `.mcp.json`**: When `.mcp.json` uses VS Code's `"servers"` key instead of `"mcpServers"`, the CLI now shows a configuration error instead of reporting no servers.
  > Fixed `claude mcp list` silently reporting no servers when `.mcp.json` can't be parsed (e.g. using VS Code's `"servers"` key instead of `"mcpServers"`) — now shows configuration errors
  - *Implication*: VS Code users migrating MCP configurations to Claude Code will now get actionable diagnostics.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Fixed macOS background session crash for Full Disk Access-protected folders**: A regression in 2.1.143 caused background sessions to crash with "exit 1 before init" when the project lived under a Full Disk Access-protected folder. Resolved.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/bg` and `←`-detach now preserve `/add-dir` directories**: Directories added with `/add-dir` are now retained when detaching from a background session.
  - *Implication*: Working context is no longer lost when switching between foreground and background modes.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Background session Windows fixes**: Multiple Windows-specific fixes: `PgUp`/`PgDn`, mouse wheel, and `Ctrl+O` navigation now work in attached background sessions; pressing `←` in `claude agents` no longer leaves the list unresponsive; CJK ghost characters fixed in Agent View on Windows Terminal.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Plugin and `/doctor` improvements**:
  - `/plugin` browse and discover panes now show when a plugin was last updated.
  - Plugin marketplace add/update now respects `CLAUDE_CODE_PLUGIN_PREFER_HTTPS`.
  - `/plugin` returns to the Installed list after enabling, disabling, or uninstalling.
  - `/doctor` now shows an exec-form example when a command hook is missing the `command` field.
  - Skill-listing truncation is no longer shown as a startup notification — run `/doctor` for the full breakdown.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### New Error Reference Sections

- **"Your organization has disabled Claude subscription access"**: New error section documents the `oauth_org_not_allowed` error code, which occurs when an organization's server-side policy blocks subscription-based login to Claude Code.
  > Your organization does not allow signing in to Claude Code with a subscription login. Running `/login` again with the same account returns the same error.
  > This is a server-side organization setting, so it cannot be overridden from local settings, environment variables, or CLI flags.
  - *Implication*: Affected users must use a Console API key instead or ask an admin to enable access. Admins who don't see the option should contact Anthropic support.
  - *Source*: [Errors](https://code.claude.com/docs/en/errors.md)

- **"Usage Policy refusal"**: New error section documents the response when conversation content triggers a Usage Policy check. Clarifies that the check evaluates the full conversation — resuming with `--continue` or `--resume` will re-trigger it since the transcript on disk still contains the triggering content.
  > The check evaluates the full conversation, not only your latest prompt, so sending a new message in the same session usually re-triggers the same refusal.
  - *Implication*: The prescribed recovery path is `/rewind` to step back before the triggering turn, or `/clear` to start fresh (prior conversation remains available via `/resume`). In non-interactive `-p` mode, rewind is unavailable — retry with a rephrased prompt or new session.
  - *Source*: [Errors](https://code.claude.com/docs/en/errors.md)

## Minor Changes

- **[glossary.md]**: Updated "Project trust" definition — removed "one-time dialog" phrasing. Now explicitly states that trust is saved per project directory, but home directory trust is session-only and the prompt reappears on each launch (+1/-1 lines).

- **[security.md]**: Added note under Trust verification: when Claude Code starts directly in the home directory, trust acceptance is not written to disk and prompts reappear on each launch. The recommended workaround is to start from a project subdirectory (+1/-0 lines).

- **[voice-dictation.md]**: Clarified `voice:pushToTalk` binding behavior — binding a custom key replaces the default `Space` binding rather than adding a second trigger. The `"space": null` line in examples is for clarity only and can be omitted (+1/-1 lines).

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| changelog.md | Modified | SIGNIFICANT | +55/-0 | New version entry: 2.1.144 (May 19, 2026) with 40+ bug fixes and improvements |
| errors.md | Modified | SIGNIFICANT | +67/-33 | Two new error sections: org subscription block and Usage Policy refusal; new entries in error lookup table |
| glossary.md | Modified | MINOR | +1/-1 | "Project trust" definition updated to clarify home-dir session-only trust |
| security.md | Modified | MINOR | +1/-0 | Added home-directory trust persistence note under Trust verification |
| voice-dictation.md | Modified | MINOR | +1/-1 | Clarified `voice:pushToTalk` key replacement vs. additive binding behavior |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-19*
