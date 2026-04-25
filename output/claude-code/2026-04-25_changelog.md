# Claude Code Documentation Changes — 2026-04-25

## Summary

The only documentation change detected is the addition of the **v2.1.120** release entry to the changelog page. This release spans 23 items including a significant Windows dependency removal, a new `ultrareview` CI subcommand, skill enhancements, two VSCode-specific fixes, and a critical crash fix for the Bash `find` tool on macOS/Linux.

## Significant Changes

### New Features

- **`claude ultrareview [target]` subcommand**: A new non-interactive subcommand enables running `/ultrareview` from CI pipelines or scripts. It prints findings to stdout, supports `--json` for machine-readable output, and exits `0` on completion or `1` on failure.
  > `Added \`claude ultrareview [target]\` subcommand to run \`/ultrareview\` non-interactively from CI or scripts — prints findings to stdout (\`--json\` for raw output) and exits 0 on completion or 1 on failure`
  - *Implication*: Enables automated code review gating in CI without requiring an interactive session.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`${CLAUDE_EFFORT}` in skill content**: Skills can now read the current effort level via this template variable.
  > `Skills can now reference the current effort level with \`${CLAUDE_EFFORT}\` in their content`
  - *Implication*: Skills can conditionally adapt behavior (e.g., verbosity, depth) based on the active effort setting without external configuration.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`AI_AGENT` environment variable for subprocesses**: Claude Code now sets this env var when spawning subprocesses, allowing tools like `gh` to attribute network traffic to Claude Code.
  > `Set \`AI_AGENT\` environment variable for subprocesses so \`gh\` can attribute traffic to Claude Code`
  - *Implication*: Improves observability and attribution for GitHub CLI usage driven by Claude Code.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Windows

- **Git for Windows no longer required**: When Git Bash is absent, Claude Code now falls back to PowerShell as the shell tool instead of failing.
  > `Windows: Git for Windows (Git Bash) is no longer required — when absent, Claude Code uses PowerShell as the shell tool`
  - *Implication*: Removes a significant installation prerequisite on Windows, broadening out-of-the-box compatibility.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Plugin / Marketplace

- **`claude plugin validate` accepts additional top-level fields**: The validator now accepts `$schema`, `version`, and `description` at the top level of `marketplace.json`, and `$schema` in `plugin.json`.
  > `\`claude plugin validate\` now accepts \`$schema\`, \`version\`, and \`description\` at the top level of \`marketplace.json\` and \`$schema\` in \`plugin.json\``
  - *Implication*: Plugin authors can now include schema declarations and metadata without validation errors.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### VS Code Integration

- **`/usage` opens native Account & Usage dialog**: In the VS Code extension, `/usage` now surfaces the native Account & Usage UI rather than returning plain-text session cost.
  > `\[VSCode] \`/usage\` now opens the native Account & Usage dialog instead of returning plain-text session cost`
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Voice dictation respects `language` setting**: VS Code voice dictation now reads the `language` field from `~/.claude/settings.json`.
  > `\[VSCode] Voice dictation now respects the \`language\` setting in \`~/.claude/settings.json\``
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Bug Fixes

- **Critical: `find` exhausting file descriptors on macOS/Linux**: The Bash tool's use of `find` could exhaust open file descriptors on large directory trees, causing host-wide crashes on macOS and Linux native builds.
  > `Fixed \`find\` in the Bash tool exhausting open file descriptors on large directory trees, causing host-wide crashes (macOS/Linux native builds)`
  - *Implication*: High-severity stability fix; users on large codebases should update immediately.

- **Telemetry suppression not working for API/enterprise users**: `DISABLE_TELEMETRY` and `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` were not suppressing usage metrics for API and enterprise users.
  > `Fixed \`DISABLE_TELEMETRY\` / \`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC\` not suppressing usage metrics telemetry for API and enterprise users`
  - *Implication*: Enterprise deployments relying on these flags for compliance had a gap; this restores expected behavior.

- **Esc closing MCP server connection (regression in 2.1.105)**: Pressing Esc during a stdio MCP tool call was closing the entire server connection.
  > `Fixed pressing Esc during a stdio MCP tool call closing the entire server connection (regression in 2.1.105)`

- **False-positive "Dangerous rm operation" prompts**: Multi-line bash commands in auto mode containing both a pipe and a redirect triggered incorrect dangerous-operation warnings.
  > `Fixed false-positive "Dangerous rm operation" permission prompts in auto mode for multi-line bash commands containing both a pipe and a redirect`

- **`/rewind` and interactive overlays unresponsive after `--resume`**: Keyboard input stopped working in interactive overlays when launching with `claude --resume`.
  > `Fixed \`/rewind\` and other interactive overlays not responding to keyboard input after launching with \`claude --resume\``

- **Terminal scrollback duplication in non-fullscreen mode**: Visible during resize, dialog dismiss, and long sessions.

- **Long selection menus clipping in fullscreen mode**: The focused option now stays on screen while scrolling.

- **Write tool output collapsing on "+N lines" click in fullscreen**.

- **Slash command picker jumping while typing**: Highlight logic improved to only match contiguous substrings (shown in blue).

- **`/plugin` marketplace load failure on unrecognized source format**: Previously, one bad entry could prevent the entire marketplace from loading. Now, the bad entry is shown but triggers an "update required" prompt when installation is attempted.

### UX Improvements

- **Spinner tips suppressed when features are already set up**: Tips recommending desktop app installation or skill/agent creation are hidden if those are already present.

- **"Use PgUp/PgDn to scroll" hint**: Shown when the terminal sends arrow key events instead of scroll events, guiding users in terminals with non-standard input handling.

- **Faster session start with many unauthorized claude.ai connectors**: Session initialization is faster when multiple connectors are configured but not authorized.

- **Auto mode denial message links to configuration docs**: The message shown when a request is denied in auto mode now includes a direct link to the relevant configuration documentation.

- **Auto-compact shows "auto" instead of misleading token count**: In auto mode, the auto-compact indicator now displays `auto` (lowercase, no token count) instead of a value that didn't reflect actual context usage.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +25 / -0 | Added v2.1.120 release entry (April 25, 2026) with 23 items |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-25*
