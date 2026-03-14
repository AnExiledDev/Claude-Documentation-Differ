# Claude Code Documentation Changes — 2026-03-14

## Summary

12 pages were modified in this update, covering the v2.1.75 release notes, a substantial expansion of Remote Control documentation (new interactive session mode and server mode flags), a new network configuration note for GitHub Enterprise Cloud users, and the addition of UTM tracking parameters to external pricing/sales links across all pages.

## Significant Changes

### Features (v2.1.75 — March 13, 2026)

- **1M context window now default for Opus 4.6 on Max/Team/Enterprise**: Previously required extra usage credits; now included by default.
  > "Added 1M context window for Opus 4.6 by default for Max, Team, and Enterprise plans (previously required extra usage)"
  - *Implication*: Users on qualifying plans no longer need to take action to access the larger context window.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/color` command added for all users**: Sets a custom prompt-bar color for the current session.
  > "Added `/color` command for all users to set a prompt-bar color for your session"
  - *Implication*: Useful for visually distinguishing multiple concurrent Claude Code sessions.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Session name on prompt bar**: The session name set via `/rename` now displays directly on the prompt bar.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Memory file timestamps**: Memory files now carry last-modified timestamps, allowing Claude to reason about whether a memory is current or stale.
  > "Added last-modified timestamps to memory files, helping Claude reason about which memories are fresh vs. stale"
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Hook source shown in permission prompts**: When a hook requires confirmation, the UI now identifies whether it originates from settings, a plugin, or a skill.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Bug Fixes (v2.1.75)

- **Bash `!` in piped commands fixed**: Bash tool was mangling `!` characters in piped commands (e.g., `jq 'select(.x != .y)'`). Now works correctly.
- **Voice mode activation on fresh installs**: Fixed a bug requiring `/voice` to be toggled twice on a fresh install.
- **Model name display**: Fixed the Claude Code header not updating after switching models via `/model` or Option+P.
- **Session crash on undefined attachment computation**: Fixed a crash when attachment message computation returns `undefined`.
- **Token estimation accuracy**: Fixed over-counting tokens for `thinking` and `tool_use` blocks, which was causing premature context compaction.
- **Organization-disabled plugins hidden**: Plugins force-disabled by an organization admin no longer appear in the `/plugin` Installed tab.
- **`/resume` preserving session names**: Fixed session names being lost after resuming a forked or continued session.
- **macOS startup performance**: Improved startup on macOS non-MDM machines by skipping unnecessary subprocess spawns.
- **Async hook messages suppressed by default**: Async hook completion messages are now hidden unless `--verbose` or transcript mode is active.
- *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Breaking Change (v2.1.75)

- **Windows managed settings path removed**: The deprecated fallback path `C:\ProgramData\ClaudeCode\managed-settings.json` has been removed.
  > "Breaking change: Removed deprecated Windows managed settings fallback at `C:\ProgramData\ClaudeCode\managed-settings.json` — use `C:\Program Files\ClaudeCode\managed-settings.json`"
  - *Implication*: Windows users or admins still using the old path must migrate to `C:\Program Files\ClaudeCode\managed-settings.json`.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Remote Control — New Interactive Session Mode

- **`--remote-control` / `--rc` flag added**: A new CLI flag launches a standard interactive Claude Code session with Remote Control enabled simultaneously, rather than starting a dedicated server process.
  > "To start a normal interactive Claude Code session with Remote Control enabled, use the `--remote-control` flag (or `--rc`)... This gives you a full interactive session in your terminal that you can also control from claude.ai or the Claude app. Unlike `claude remote-control` (server mode), you can type messages locally while the session is also available remotely."
  - *Implication*: Previously, enabling Remote Control required either `claude remote-control` (server-only, no local input) or `/remote-control` inside an existing session. The new `--remote-control` flag lets users start a session that is simultaneously local and remotely accessible from the outset.
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md), [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **Server mode: `--spawn` flag for concurrent session management**: The `claude remote-control` server mode now supports a `--spawn <mode>` flag controlling how concurrent remote sessions are created.
  > "`--spawn <mode>`: How concurrent sessions are created. Press `w` at runtime to toggle. • `same-dir` (default): all sessions share the current working directory... • `worktree`: each on-demand session gets its own git worktree. Requires a git repository."
  - *Implication*: Teams running a shared Remote Control server can now route each remote user into an isolated git worktree, preventing conflicts when multiple users edit the same files.
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

- **Server mode: `--capacity` flag**: Sets the maximum number of concurrent remote sessions. Defaults to 32.
  > "`--capacity <N>`: Maximum number of concurrent sessions. Default is 32."
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

- **Limitations clarified**: The "one remote session at a time" limitation is now scoped explicitly to interactive processes (not server mode).
  > "One remote session per interactive process: outside of server mode, each Claude Code instance supports one remote session at a time. Use server mode with `--spawn` to run multiple concurrent sessions from a single process."
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

### Network Configuration — GitHub Enterprise Cloud IP Allowlisting

- **New guidance for GitHub Enterprise Cloud IP restrictions**: A new paragraph documents how Claude Code on the web and Code Review connect from Anthropic-managed infrastructure, and how to configure IP allowlisting.
  > "Claude Code on the web and Code Review connect to your repositories from Anthropic-managed infrastructure. If your GitHub Enterprise Cloud organization restricts access by IP address, enable IP allow list inheritance for installed GitHub Apps... The Claude GitHub App registers its IP ranges, so enabling this setting allows access without manual configuration."
  - *Implication*: Organizations with IP allowlists on GitHub Enterprise Cloud previously had to discover and add Anthropic IP ranges manually. This documents the preferred approach (enabling GitHub App IP list inheritance) and provides a fallback link to the Anthropic API IP addresses page.
  - *Source*: [Network Config](https://code.claude.com/docs/en/network-config.md)

## Notable Details

- **UTM parameter rollout across all pricing/sales links**: Every external link to `claude.com/pricing` and `anthropic.com/contact-sales` (and `anthropic.com/contact-sales`) across authentication, quickstart, overview, desktop quickstart, fast mode, legal, server-managed settings, and third-party integrations pages now includes UTM parameters (e.g., `?utm_source=claude_code&utm_medium=docs&utm_content=<page_context>`). This is purely an analytics instrumentation change and does not affect user-facing behavior.

- **`claude remote-control` description updated in CLI reference**: The command description now explicitly states it "Runs in server mode (no local interactive session)", clarifying the distinction from the new `--remote-control` interactive flag.

- **Code block attribute duplication in overview.md and quickstart.md**: Install command code blocks had a formatting artifact introduced — `theme={null}` appears repeated 7 times (e.g., `` ```bash theme={null} theme={null} ... ``). This is a documentation source artifact and does not affect rendered output for users reading the docs site.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| remote-control.md | Modified | +30/-10 | Added interactive session mode (`--remote-control`/`--rc`), `--spawn` and `--capacity` server flags, restructured tabs |
| changelog.md | Modified | +22/-0 | Added v2.1.75 release notes (March 13, 2026) |
| cli-reference.md | Modified | +17/-16 | Added `--remote-control`/`--rc` flag; updated `claude remote-control` description to clarify server mode |
| overview.md | Modified | +7/-7 | UTM parameters on pricing links; code block formatting artifact |
| quickstart.md | Modified | +7/-7 | UTM parameters on pricing links; code block formatting artifact |
| authentication.md | Modified | +3/-3 | UTM parameters on pricing and contact-sales links |
| network-config.md | Modified | +2/-0 | New paragraph on GitHub Enterprise Cloud IP allowlisting |
| desktop-quickstart.md | Modified | +2/-2 | UTM parameters on pricing links |
| fast-mode.md | Modified | +1/-1 | UTM parameters on Teams/Enterprise pricing links |
| legal-and-compliance.md | Modified | +1/-1 | UTM parameters on contact-sales link |
| server-managed-settings.md | Modified | +1/-1 | UTM parameters on Teams/Enterprise pricing links |
| third-party-integrations.md | Modified | +1/-1 | UTM parameters on Enterprise contact-sales link |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-14*
