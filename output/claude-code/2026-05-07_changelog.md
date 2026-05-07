# Claude Code Documentation Changes — 2026-05-07

## Summary

Two documentation pages were updated: the official changelog gained 31 lines documenting the `2.1.132` release (May 6, 2026), and the settings reference received a one-line clarification linking `autoUpdatesChannel` to the `DISABLE_AUTOUPDATER` environment variable. No pages were added or removed.

## Significant Changes

### New Release: 2.1.132 (May 6, 2026)

#### New Environment Variables

- **`CLAUDE_CODE_SESSION_ID` in Bash subprocesses**: The session ID is now injected into the Bash tool's subprocess environment, matching the value passed to hooks.
  > "Added `CLAUDE_CODE_SESSION_ID` environment variable to the Bash tool subprocess environment, matching the `session_id` passed to hooks"
  - *Implication*: Scripts running inside Claude Code's Bash tool can now self-identify their session without separate plumbing. Useful for logging and hook coordination.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1`**: New opt-out for the fullscreen alternate-screen renderer, keeping the conversation in the terminal's native scrollback buffer instead.
  > "Added `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` env var to opt out of the fullscreen alternate-screen renderer and keep the conversation in the terminal's native scrollback"
  - *Implication*: Users who prefer standard terminal scrollback (e.g., for copy-paste workflows or logging) can now disable the alternate screen without losing other features.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

#### Terminal & Input Fixes

- **Graceful SIGINT handling**: External `SIGINT` signals (IDE stop button, `kill -INT`) now trigger proper graceful shutdown — terminal modes are restored and the `--resume` hint is printed instead of an abrupt exit.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`--resume` emoji crash fix**: `--resume` no longer fails with `no low surrogate in string` when a tool error truncation split a multi-byte emoji; pre-corrupted sessions are sanitized on load.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`--permission-mode` + plan mode resume**: The `--permission-mode` flag is no longer ignored when resuming a plan-mode session via `-p --continue`/`--resume`, and plan mode is now correctly re-applied after `ExitPlanMode` within the same session.
  - *Implication*: Developers relying on permission constraints during automated plan-mode resumptions should now see consistent behavior.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Fullscreen blank screen after sleep/suspend**: Fixed a blank screen appearing after laptop sleep/wake or `Ctrl+Z`/`fg` until the next keystroke or stream output.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Unicode/grapheme cursor fixes**: Fixed cursor landing mid-grapheme on `Ctrl+E/A/K/U`/arrow keys when Indic conjuncts or ZWJ emoji wrap across lines. Also fixed vim operators corrupting NFD decomposed accented characters.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Paste reliability fixes**:
  - Pasting text starting with `/` no longer silently swallows input or triggers an unknown-command reply.
  - Pasting no longer dumps stray escape sequences when focus events or mouse-tracking reports interleave with bracketed paste.
  - Added a `"Pasting…"` footer hint while a Ctrl+V image paste is being read from the clipboard.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

#### IDE Integration Fixes

- **VS Code / Cursor mouse wheel speed**: Fixed mouse wheel scrolling being too fast in Cursor and VS Code 1.92–1.104 due to an upstream `xterm.js` bug.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **JetBrains 2025.2 scroll-wheel**: Fixed scroll-wheel handling in JetBrains IDE 2025.2 terminals (spurious arrow keys, wrong-direction events, runaway acceleration).
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Windows Terminal `/terminal-setup` error**: Fixed a contradictory error displayed in Windows Terminal — Shift+Enter is natively supported there and should not have been flagged.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Windows background session keyboard input**: Fixed dead keyboard input on Windows after re-opening a background session from `claude agents`.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

#### MCP Server Fixes

- **Unbounded memory growth with stdio MCP servers**: Fixed 10GB+ RSS memory growth when a stdio MCP server writes non-protocol data to stdout.
  - *Implication*: Long-running sessions with verbose or misconfigured MCP servers should no longer exhaust system memory.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **MCP tool fetch failure visibility**: MCP servers that connect but fail `tools/list` previously showed 0 tools silently; they now retry once and display "connected · tools fetch failed" in `/mcp`.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **MCP auth status accuracy**: Unauthorized `claude.ai` MCP connectors now show "needs auth" instead of "failed", and headless `-p` mode no longer retries non-transient 4xx connection failures.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

#### Slash Command & UI Fixes

- **`/usage` clipboard hang on Linux/X11**: Fixed `Ctrl+S` in `/usage` hanging when copying the stats screenshot to the clipboard.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/effort` env var ignored**: Fixed `/effort` picker not reflecting the `CLAUDE_CODE_EFFORT_LEVEL` environment variable override.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/status` wrong default model**: Fixed `/status` showing the wrong default model for some users.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Slash command autocomplete size**: Fixed the autocomplete popup being capped at ~3–5 visible commands instead of scaling with terminal height.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Statusline `context_window` token counts**: Fixed the `context_window` metric reflecting cumulative session totals rather than current context usage.
  - *Implication*: Status line integrations and hooks reading `context_window` will now get accurate per-request values.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Alt+T (thinking toggle) on macOS**: Fixed Alt+T not working on macOS terminals without "Option as Meta" enabled (iTerm2, Terminal.app defaults).
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

#### Other Fixes

- **Bedrock/Vertex prompt caching**: Fixed 400 errors on Bedrock and Vertex when `ENABLE_PROMPT_CACHING_1H` is set.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Configuration

- **`autoUpdatesChannel` links to `DISABLE_AUTOUPDATER`**: The settings reference for `autoUpdatesChannel` now explicitly mentions how to disable auto-updates entirely.
  > "To disable auto-updates entirely, set [`DISABLE_AUTOUPDATER`](/en/setup#disable-auto-updates) in `env`"
  - *Implication*: This cross-link surfaces the full disable option, which was previously only discoverable via the setup page. Administrators managing deployments where auto-updates should be suppressed now have a clear path from the settings table.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

## Notable Details

- The `2.1.131` release (also dated May 6, 2026) was already present in the previous snapshot; `2.1.132` is the newly documented release. Two releases shipped on the same calendar date.
- The fullscreen renderer banner update (`/tui fullscreen`) now advertises lower memory usage, mouse support, and auto-copy on select — signaling active investment in the TUI renderer as the preferred interface.
- The MCP "needs auth" fix (vs. "failed") is a subtle but meaningful UX distinction: it allows tooling and users to distinguish transient errors from authentication requirements and act accordingly.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +31 / -0 | Added `2.1.132` release entry with 3 new features and 24 bug fixes |
| settings.md | Modified | +1 / -1 | Added `DISABLE_AUTOUPDATER` cross-link to `autoUpdatesChannel` description |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-07*
