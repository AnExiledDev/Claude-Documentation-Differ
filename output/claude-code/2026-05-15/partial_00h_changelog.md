# Claude Code Documentation Changes — 2026-05-15

## Summary

Two documentation pages were updated: `agent-view.md` gained a new `--name` flag example for background sessions, and `changelog.md` was updated with the v2.1.142 release notes from May 14, 2026. The release is substantial — 8 new `claude agents` flags, a default model upgrade for fast mode, plugin improvements, and 14+ bug fixes.

## Significant Changes

### CLI Flags

- **New `--name` flag for background sessions**: The `--bg` command now accepts a `--name` argument to set a custom display name in agent view, replacing the auto-generated session title.
  > Pass `--name` to set the session's display name in agent view instead of the auto-generated one:
  > ```bash
  > claude --bg --name "flaky-test-fix" "investigate the flaky SettingsChangeDetector test"
  > ```
  - *Implication*: Makes it easier to identify specific background sessions at a glance, especially when running multiple concurrent agents.
  - *Source*: [agent-view.md](https://code.claude.com/docs/en/agent-view.md)

- **New `claude agents` dispatch flags (v2.1.142)**: Eight new flags can now be passed when dispatching background sessions via `claude agents`: `--add-dir`, `--settings`, `--mcp-config`, `--plugin-dir`, `--permission-mode`, `--model`, `--effort`, and `--dangerously-skip-permissions`.
  > Added new `claude agents` flags: `--add-dir`, `--settings`, `--mcp-config`, `--plugin-dir`, `--permission-mode`, `--model`, `--effort`, and `--dangerously-skip-permissions` to configure dispatched background sessions
  - *Implication*: Background agents can now be configured with per-session MCP configs, plugins, models, and permission modes — enabling more fine-grained multi-agent setups without modifying global settings.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

### Model Defaults

- **Fast mode upgraded to Opus 4.7 by default**: Fast mode previously used Opus 4.6; it now defaults to Opus 4.7. Users can revert with `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1`.
  > Fast mode now uses Opus 4.7 by default (previously Opus 4.6). Set `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1` to pin fast mode to Opus 4.6
  - *Implication*: Fast mode responses will use a newer model without any action required; teams with reproducibility requirements may need the override env var.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

### Plugins & Skills

- **Root-level `SKILL.md` now surfaces as a skill**: Plugins with a root-level `SKILL.md` and no `skills/` subdirectory are now automatically surfaced as a skill, without requiring the subdirectory structure.
  > Plugins with a root-level `SKILL.md` and no `skills/` subdirectory are now surfaced as a skill
  - *Implication*: Simplifies single-skill plugin authoring — no need to create a `skills/` directory for simple plugins.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Plugin details pane shows LSP servers**: The `/plugin` details pane and `claude plugin details` command now display which LSP servers a plugin provides.
  > The `/plugin` details pane and `claude plugin details` now show LSP servers a plugin provides
  - *Implication*: Developers can inspect LSP capabilities without reading plugin source code.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

### Bug Fixes (v2.1.142)

- **`MCP_TOOL_TIMEOUT` now applies to remote HTTP/SSE servers**: The timeout setting was previously ignored for remote HTTP and SSE MCP servers, capping all tool calls at 60 seconds regardless of configuration.
- **Background sessions now recognize pre-existing git worktrees**: Previously, background sessions blocked edits when a worktree already existed because `EnterWorktree` refused to create a duplicate.
- **macOS sleep/wake daemon reconnect fixed**: The daemon now detects system clock jumps on wake rather than treating elapsed sleep time as idle time, preventing background session disconnects.
- **Daemon upgrade crash-loop fixed**: The daemon no longer stays running after binary upgrades (e.g., `brew upgrade`), which caused dispatched agents to crash-loop on the deleted binary path.
- **`--dangerously-skip-permissions` now persists across retire/wake cycles** for background sessions.
- **Claude-in-Chrome extension crash-loop fixed**: Background agents no longer crash when the Chrome extension is connected without a shared tab.
- **Link clicks fixed in attached sessions**: The background worker's headless browser shim no longer intercepts link clicks when a `claude agents` session is attached.
- **`claude agents` now uses `$EDITOR`/`$VISUAL`**: The "v to open in editor" keybind previously used the daemon's default editor instead of the shell's `$EDITOR`/`$VISUAL` environment variable.
- **Windows deadlock on network drives fixed**: `claude agents` no longer deadlocks on Windows with network-drive working directories; Ctrl+C now works during startup.
- **Apple Terminal background-color bleed fixed**: 256-color-only terminals no longer show background-color artifacts when attaching to a `claude agents` session.
- **Session titles from URLs fixed**: Session titles are no longer derived from the URL when the first message is a link.
- **Duplicate `/model` breadcrumbs eliminated**: Redundant `set_model` requests from remote clients no longer inject duplicate `/model` breadcrumbs into transcripts.
- **Plugin `skills: ["./"]` false error fixed**: Plugins using `skills: ["./"]` no longer show a spurious "path escapes plugin directory" error.
- **Plugin cache cleanup fixed**: Cache cleanup no longer deletes the active plugin version directory when installation metadata is absent.
- **Plugin browse "0 installs" display fixed**: The `/plugin` browse pane now correctly shows install counts for newly published plugins.
- **Plugin advisory key-shadowing warnings improved**: Plugin advisories now name every `plugin.json` key that shadows a default folder.

### Improvements (v2.1.142)

- **Reactive compaction seeded from overflow size**: The first compaction attempt now uses the original request's overflow size as a seed, avoiding a wasted near-full-context retry.
- **Clearer hook configuration error**: Configuring a prompt- or agent-type hook for `SessionStart`, `Setup`, or `SubagentStart` now shows an explicit "use a command-type hook instead" error.
- **Stale model suggestion removed**: The `/model claude-sonnet-4-20250514` suggestion was removed from Usage Policy refusal messages.

## Minor Changes

- **`/web-setup` replacement warning**: `/web-setup` now warns before replacing an existing GitHub App connection. (+included in v2.1.142 changelog)

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| `en/agent-view.md` | Modified | SIGNIFICANT | +6/-0 | Added `--name` flag documentation for naming background sessions |
| `en/changelog.md` | Modified | SIGNIFICANT | +27/-0 | Added v2.1.142 release notes (May 14, 2026) |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-15*
