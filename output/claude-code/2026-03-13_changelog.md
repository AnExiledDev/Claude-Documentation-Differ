# Claude Code Documentation Changes — 2026-03-13

## Summary

The dominant change is a wholesale replacement of the `changelog.md` source: the old page was scraped GitHub HTML (complete with navigation chrome, star counts, and raw markdown preview), while the new page is a properly formatted documentation page using `<Update>` tags with clean, structured entries. This brings five new version releases (2.1.70–2.1.74) into the official docs. Alongside the changelog update, the `settings.md` reference table was expanded with three new settings entries (`autoMemoryDirectory`, `includeGitInstructions`, `modelOverrides`), and six pages received minimum version requirement notices.

---

## Significant Changes

### Changelog Reformatting and New Releases (v2.1.70–v2.1.74)

- **Changelog page converted from GitHub scrape to structured documentation**: The previous `changelog.md` was a scraped dump of the GitHub repository page, including raw navigation HTML, star/fork counts, and a `Preview` tab artefact. The new page is a first-class documentation page with per-version `<Update label="..." description="...">` tags, consistent formatting, and a direct link to the source CHANGELOG.md on GitHub.
  > This page is generated from the [CHANGELOG.md on GitHub](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md).
  - *Implication*: Changelog entries are now readable in the docs site without navigating to GitHub, and each release is a distinct collapsible block rather than a flat markdown wall.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### New Features Documented in Changelog

#### v2.1.74 (March 12, 2026)

- **`autoMemoryDirectory` setting**: Configures a custom directory for auto-memory storage. Accepts `~/`-expanded paths. Not accepted in project settings to prevent repos from redirecting memory writes to sensitive locations.
  > Added `autoMemoryDirectory` setting to configure a custom directory for auto-memory storage

- **`/context` command gains actionable suggestions**: Identifies context-heavy tools, memory bloat, and capacity warnings with specific optimization tips.
  > Added actionable suggestions to `/context` command — identifies context-heavy tools, memory bloat, and capacity warnings with specific optimization tips

- **Memory leak fix (Node.js/npm)**: Streaming API response buffers were not released when the generator was terminated early, causing unbounded RSS growth.

- **Managed policy `ask` rules fix**: Rules were being bypassed by user `allow` rules or skill `allowed-tools`.

- **Full model IDs in agent frontmatter**: `claude-opus-4-5` and similar full IDs were silently ignored in `model:` fields; agents now accept the same model values as `--model`.

- **MCP OAuth fixes**: Hanging callback port, refresh token expiry not prompting re-auth (for HTTP 200 error servers like Slack), and `SessionEnd` hook timeout now configurable via `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`.

- **Voice mode fix (macOS native binary)**: The binary now includes the `audio-input` entitlement so macOS prompts for microphone permission correctly.

- **RTL text rendering fix**: Hebrew, Arabic, and other RTL text now renders correctly in Windows Terminal, conhost, and VS Code integrated terminal.

- **`--plugin-dir` behavior change**: Local dev copies now override installed marketplace plugins with the same name (unless force-enabled by managed settings).
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

#### v2.1.73 (March 11, 2026)

- **`modelOverrides` setting**: Maps model picker entries to provider-specific model IDs (e.g., Bedrock inference profile ARNs).
  > Added `modelOverrides` setting to map model picker entries to custom provider model IDs (e.g. Bedrock inference profile ARNs)
  - *Implication*: Bedrock and Vertex users can now map standard Anthropic model names to their custom inference profile ARNs without using environment variables.

- **Default Opus model updated on Bedrock/Vertex/Foundry**: Changed to Opus 4.6 (was Opus 4.1).
  > Changed default Opus model on Bedrock, Vertex, and Microsoft Foundry to Opus 4.6 (was Opus 4.1)

- **`/output-style` deprecated**: Replaced by `/config`. Output style is now fixed at session start for better prompt caching.
  > Deprecated `/output-style` command — use `/config` instead. Output style is now fixed at session start for better prompt caching

- **SSL certificate error guidance**: Added actionable guidance when OAuth login or connectivity checks fail due to SSL certificate errors (corporate proxies, `NODE_EXTRA_CA_CERTS`).
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

#### v2.1.72 (March 10, 2026)

- **`ExitWorktree` tool added**: Leaves an `EnterWorktree` session.
  > Added `ExitWorktree` tool to leave an `EnterWorktree` session

- **`CLAUDE_CODE_DISABLE_CRON` env var**: Immediately stops scheduled cron jobs mid-session.
  > Added `CLAUDE_CODE_DISABLE_CRON` environment variable to immediately stop scheduled cron jobs mid-session

- **Bash auto-approval allowlist expanded**: `lsof`, `pgrep`, `tput`, `ss`, `fd`, and `fdfind` added, reducing permission prompts for common read-only operations.

- **`model` parameter restored on Agent tool**: Per-invocation model overrides work again.
  > Restored the `model` parameter on the Agent tool for per-invocation model overrides

- **CLAUDE.md HTML comments hidden from Claude**: `<!-- ... -->` blocks are hidden when auto-injected into context. They remain visible when read with the Read tool.
  > Changed CLAUDE.md HTML comments (`<!-- ... -->`) to be hidden from Claude when auto-injected. Comments remain visible when read with the Read tool

- **Effort levels simplified**: Reduced to low/medium/high (max removed) with new symbols (○ ◐ ●). Use `/effort auto` to reset.
  > Simplified effort levels to low/medium/high (removed max) with new symbols (○ ◐ ●) and a brief notification instead of a persistent icon

- **`/config` improvements**: Escape cancels changes, Enter saves and closes, Space toggles settings.

- **Prompt cache fix in SDK `query()` calls**: Reduces input token costs up to 12× by fixing cache invalidation.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

#### v2.1.71 (March 7, 2026)

- **`/loop` command**: Runs a prompt or slash command on a recurring interval.
  > Added `/loop` command to run a prompt or slash command on a recurring interval (e.g. `/loop 5m check the deploy`)

- **Cron scheduling tools**: `CronCreate`, `CronList`, `CronDelete` added for recurring prompts within a session.

- **`voice:pushToTalk` keybinding**: Makes the voice activation key rebindable in `keybindings.json` (default: space). Modifier+letter combos like `meta+k` have zero typing interference.
  > Added `voice:pushToTalk` keybinding to make the voice activation key rebindable in `keybindings.json`

- **Additional bash allowlist commands**: `fmt`, `comm`, `cmp`, `numfmt`, `expr`, `test`, `printf`, `getconf`, `seq`, `tsort`, and `pr`.

- **Bridge session reconnection improvement**: Completes within seconds after laptop wake, instead of up to 10 minutes.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

#### v2.1.70 (March 6, 2026)

- **Third-party gateway tool search fix**: Tool search now correctly detects proxy endpoints and disables `tool_reference` blocks when `ANTHROPIC_BASE_URL` is set.
- **Bedrock effort parameter fix**: Fixed `API Error: 400 This model does not support the effort parameter` for custom inference profiles.
- **Clipboard fix for non-ASCII on Windows/WSL**: Uses PowerShell `Set-Clipboard` to correctly handle CJK and emoji.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

### Configuration

- **Three new settings entries in `settings.md`**: The settings reference table was expanded to document settings that shipped in recent releases but were not yet in the docs:

  | Setting | Description | Added in |
  |---|---|---|
  | `autoMemoryDirectory` | Custom directory for auto-memory storage; not accepted in project settings | v2.1.74 |
  | `includeGitInstructions` | Remove built-in commit/PR workflow instructions from Claude's system prompt (default: `true`) | v2.1.69 |
  | `modelOverrides` | Map Anthropic model IDs to provider-specific IDs (e.g. Bedrock ARNs) | v2.1.73 |

  The `fastModePerSessionOptIn` entry was also added (documented separately in fast-mode.md). Descriptions for existing settings were also reformatted for consistency.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`autoMemoryDirectory` documented in memory.md**: The storage location section now explains how to set a custom directory and notes the scope restriction.
  > To store auto memory in a different location, set `autoMemoryDirectory` in your user or local settings
  > This setting is accepted from policy, local, and user settings. It is not accepted from project settings (`.claude/settings.json`) to prevent a shared project from redirecting auto memory writes to sensitive locations.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

---

### Documentation Housekeeping

- **Version requirement notices added to six pages**: A consistent `<Note>` block with minimum version and `claude --version` check was added to each of these pages:

  | Page | Minimum Version |
  |---|---|
  | Agent teams | v2.1.32 |
  | Fast mode | v2.1.36 |
  | Keybindings | v2.1.18 |
  | Memory (auto memory section) | v2.1.59 |
  | Remote Control | v2.1.51 |
  | Scheduled tasks | v2.1.72 |

  - *Implication*: Users on older installations will now see an explicit minimum version requirement before they attempt to use these features.
  - *Sources*: [Agent Teams](https://code.claude.com/docs/en/agent-teams.md), [Fast Mode](https://code.claude.com/docs/en/fast-mode.md), [Keybindings](https://code.claude.com/docs/en/keybindings.md), [Memory](https://code.claude.com/docs/en/memory.md), [Remote Control](https://code.claude.com/docs/en/remote-control.md), [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks.md)

- **CDN image URL refresh on three pages**: Diagram images in `hooks.md`, `how-claude-code-works.md`, and `features-overview.md` were updated to a new CDN path (`c5r9_6tjPMzFdDDT` replacing `TBPmHzr19mDCuhZi` and `JWoaQLhotXStH4d2`). Image alt text and dimensions are unchanged; this is a CDN asset refresh with no content impact.

---

## Notable Details

- **`/output-style` deprecation signal**: The decision to fix output style at session start "for better prompt caching" (v2.1.73) indicates that mid-session style switching was causing prompt cache invalidation—a meaningful latency and cost concern. Administrators relying on `outputStyle` in settings.json should note that it still works, but dynamic changes via command are now discouraged.

- **CLAUDE.md comment hiding**: The change to strip `<!-- ... -->` from context when auto-injected (v2.1.72) means developers can now annotate their CLAUDE.md files with HTML comments for human readers without those comments consuming context tokens or influencing model behavior. However, if Claude uses the Read tool on CLAUDE.md directly, comments are visible.

- **`modelOverrides` scope**: The setting maps standard model identifiers (e.g., `claude-opus-4-6`) to arbitrary provider-specific strings. This is distinct from `availableModels` (which restricts the picker) and `model` (which sets the default). It enables Bedrock users to swap in inference profile ARNs per-model without changing their workflow.

- **Changelog source shift**: The old `changelog.md` content included GitHub navigation HTML as literal text (e.g., "Fork 6.3k Star 77.1k", "Issues 5k+"), which indicates it was populated by scraping the GitHub rendered page rather than the raw file. The new content is sourced from the raw CHANGELOG.md and formatted for Mintlify with `<Update>` components.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +2245 / -1810 | Reformatted from GitHub-scraped HTML to structured documentation; adds v2.1.70–2.1.74 release notes |
| settings.md | Modified | +50 / -50 | New settings entries: `autoMemoryDirectory`, `includeGitInstructions`, `modelOverrides`; table reformatted |
| agent-teams.md | Modified | +4 / -0 | Added version requirement note (v2.1.32+) |
| fast-mode.md | Modified | +4 / -0 | Added version requirement note (v2.1.36+) |
| keybindings.md | Modified | +4 / -0 | Added version requirement note (v2.1.18+) |
| memory.md | Modified | +4 / -0 | Added version requirement note for auto memory (v2.1.59+) |
| remote-control.md | Modified | +4 / -0 | Added version requirement note (v2.1.51+) |
| scheduled-tasks.md | Modified | +4 / -0 | Added version requirement note (v2.1.72+) |
| hooks.md | Modified | +2 / -2 | CDN image URL refresh (no content change) |
| how-claude-code-works.md | Modified | +2 / -2 | CDN image URL refresh (no content change) |
| features-overview.md | Modified | +1 / -1 | CDN image URL refresh (no content change) |
| data-usage.md | Modified | +1 / -1 | Minor text change |
| vs-code.md | Modified | +1 / -1 | Minor text change |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-13*
