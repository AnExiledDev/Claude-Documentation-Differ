# Claude Code Documentation Changes — 2026-04-25

## Summary

One page was modified with 25 lines deleted and no additions. The entire **v2.1.120** release entry was removed from the changelog page. Both snapshots are from the same day (00:29 UTC → 06:33 UTC), indicating the release notes were published and then retracted within hours. The entry's content covered a substantial set of features and fixes across Windows, CI tooling, plugins, VS Code, and several bug fixes.

## Notable Details

The retracted `2.1.120` entry contained the following items, noted here for reference. These have not been confirmed as released — they were visible briefly in the documentation and subsequently removed:

### Features (retracted)

- **Windows: Git Bash no longer required** — Claude Code would fall back to PowerShell as the shell tool when Git for Windows is absent, removing a significant Windows install prerequisite.
- **`claude ultrareview [target]` subcommand** — A non-interactive subcommand for running `/ultrareview` from CI or scripts, printing findings to stdout with `--json` for machine-readable output. Exits `0` on completion, `1` on failure.
- **`${CLAUDE_EFFORT}` in skill content** — Skills could read the current effort level via this template variable, enabling effort-adaptive behavior.
- **`AI_AGENT` environment variable for subprocesses** — Would be set when spawning subprocesses, allowing `gh` and similar tools to attribute network traffic to Claude Code.
- **`claude plugin validate` expanded acceptance** — Would accept `$schema`, `version`, and `description` at the top level of `marketplace.json`; `$schema` in `plugin.json`.

### VS Code (retracted)

- **`/usage` opens native Account & Usage dialog** — Instead of returning plain-text session cost.
- **Voice dictation respects `language` setting** — Reads `language` from `~/.claude/settings.json`.

### Bug Fixes (retracted)

- **Critical: `find` exhausting file descriptors** — `find` in the Bash tool could exhaust open file descriptors on large directory trees, causing host-wide crashes on macOS/Linux native builds.
- **Telemetry suppression gap for API/enterprise users** — `DISABLE_TELEMETRY` / `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` were not suppressing usage metrics for API and enterprise users.
- **Esc closing MCP server connection** (regression in 2.1.105) — Pressing Esc during a stdio MCP tool call closed the entire server connection.
- **False-positive "Dangerous rm operation" prompts** — Triggered incorrectly in auto mode for multi-line bash commands containing both a pipe and a redirect.
- **`/rewind` and interactive overlays unresponsive after `--resume`** — Keyboard input stopped working in interactive overlays when launching with `claude --resume`.
- **Terminal scrollback duplication** in non-fullscreen mode (resize, dialog dismiss, long sessions).
- **Long selection menus clipping** below the terminal in fullscreen mode.
- **Write tool output collapsing** instead of expanding on "+N lines" click in fullscreen.
- **Slash command picker jumping** while typing; highlight now matches only contiguous substrings in blue.
- **`/plugin` marketplace failing to load** when one entry used an unrecognized source format — now shows the bad entry but prompts to update when installation is attempted.

### UX Improvements (retracted)

- Spinner tips for installing the desktop app or creating skills/agents hidden when already configured.
- "Use PgUp/PgDn to scroll" hint shown when the terminal sends arrow keys instead of scroll events.
- Faster session start when many `claude.ai` connectors are configured but not authorized.
- Auto mode denial message now links to the configuration docs.
- Auto-compact in auto mode displays `auto` (lowercase, no token count) instead of a misleading token value.

> **Note**: Because this entry was removed from the documentation between the two snapshots compared here, none of the above changes are confirmed released. Monitor the [Claude Code Changelog](https://code.claude.com/docs/en/changelog.md) for a future entry (likely `2.1.120` or later) that re-publishes these release notes.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +0 / -25 | Removed the `2.1.120` release entry (April 25, 2026) in its entirety |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-25. Comparing `3c599892` → `HEAD`. Source: [Claude Code Changelog](https://code.claude.com/docs/en/changelog.md)*
