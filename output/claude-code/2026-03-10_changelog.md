# Claude Code Documentation Changes — 2026-03-10

## Summary

Version 2.1.72 is documented in the official changelog with a large set of new features and bug fixes. Across four other pages, `CLAUDE.local.md` is removed as a documented convention — the local-scope memory file no longer appears in the reference table, best-practices examples, or desktop compatibility notes. The tools reference table in `settings.md` has been substantially expanded to include newly available tools including `CronCreate/Delete/List`, `EnterWorktree`, `ExitWorktree`, `ToolSearch`, and MCP resource tools.

## Significant Changes

### Version 2.1.72 Release

- **ExitWorktree tool added**: A new `ExitWorktree` tool is available to leave an `EnterWorktree` session and return to the original directory.
  > Added ExitWorktree tool to leave an EnterWorktree session
  - *Implication*: Agents working in isolated git worktrees can now cleanly exit back to the original directory programmatically.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/plan` accepts an inline description**: The `/plan` command now accepts an optional description argument that enters plan mode and immediately starts working on it.
  > Added optional description argument to /plan (e.g., /plan fix the auth bug) that enters plan mode and immediately starts
  - *Implication*: Saves the extra step of entering plan mode and then typing a prompt.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/copy` `w` key writes directly to file**: In the `/copy` UI, pressing `w` now writes the focused selection directly to a file, bypassing the clipboard.
  > Added w key in /copy to write the focused selection directly to a file, bypassing the clipboard (useful over SSH)
  - *Implication*: Makes `/copy` usable in SSH sessions where clipboard integration is unavailable.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`CLAUDE_CODE_DISABLE_CRON` environment variable**: A new environment variable that immediately stops all scheduled cron jobs mid-session.
  > Added CLAUDE_CODE_DISABLE_CRON environment variable to immediately stop scheduled cron jobs mid-session
  - *Implication*: Provides a kill-switch for recurring scheduled tasks without ending the session entirely.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Bash auto-approval allowlist expanded**: `lsof`, `pgrep`, `tput`, `ss`, `fd`, and `fdfind` are now auto-approved without prompting.
  > Added lsof, pgrep, tput, ss, fd, and fdfind to the bash auto-approval allowlist, reducing permission prompts for common read-only operations
  - *Implication*: Fewer interruptions when Claude uses standard diagnostic and file-search tools.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Agent tool `model` parameter restored**: Per-invocation model overrides on the `Agent` tool are available again.
  > Restored the model parameter on the Agent tool for per-invocation model overrides
  - *Implication*: Developers can route sub-agents to different models (e.g., a faster model for simpler sub-tasks).
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Effort levels simplified — `max` removed**: Levels are now `low/medium/high` with new symbols `○ ◐ ●`. A brief notification replaces the persistent icon. Use `/effort auto` to reset to default.
  > Simplified effort levels to low/medium/high (removed max) with new symbols (○ ◐ ●) and a brief notification instead of a persistent icon. Use /effort auto to reset to default
  - *Implication*: Existing configurations or scripts referencing `max` effort will need to be updated to `high`.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **HTML comments in CLAUDE.md now hidden from Claude**: `<!-- ... -->` comments in CLAUDE.md files are no longer visible to Claude when auto-injected, but remain readable via the `Read` tool.
  > Changed CLAUDE.md HTML comments (<!-- ... -->) to be hidden from Claude when auto-injected. Comments remain visible when read with the Read tool
  - *Implication*: Teams can add internal notes inside CLAUDE.md HTML comments without those notes influencing Claude's behavior.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Prompt cache invalidation fixed in SDK**: `query()` calls in the SDK were incorrectly invalidating prompt caches; this is now fixed.
  > Fixed prompt cache invalidation in SDK query() calls, reducing input token costs up to 12x
  - *Implication*: SDK users may see significantly lower input token costs (up to 12x reduction) without any code changes.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/clear` no longer kills background tasks**: Previously `/clear` would kill background agent and bash tasks; now only foreground tasks are cleared.
  > Fixed /clear killing background agent/bash tasks — only foreground tasks are now cleared
  - *Implication*: Background work continues safely when a user clears their conversation.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **VSCode: URI handler for programmatic tab opening**: A new `vscode://anthropic.claude-code/open` URI handler opens a new Claude Code tab, with optional `prompt` and `session` query parameters.
  > VSCode: Added vscode://anthropic.claude-code/open URI handler to open a new Claude Code tab programmatically, with optional prompt and session query parameters
  - *Implication*: Enables IDE workflows and external tools to launch Claude Code sessions with pre-filled context.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Notable bug fixes in 2.1.72**:
  - Skill hooks firing twice per event when a hooks-enabled skill is invoked by the model
  - `--continue` not resuming from the most recent point after `--compact`
  - `--effort` CLI flag being reset by unrelated settings writes on startup
  - Plugin installation failing on Windows (EEXIST in OneDrive folders), plus marketplace blocking user-scope installs when a project-scope install exists
  - Worktree isolation issues: Task tool resume not restoring cwd; background task notifications missing `worktreePath`/`worktreeBranch`
  - Sandbox permission issues: certain file writes incorrectly allowed without prompting; output redirections to allowlisted dirs (like `/tmp/claude/`) prompting unnecessarily
  - Permission rule matching: wildcards not matching commands with heredocs/embedded newlines/no arguments; deny rules not applying to all command forms
  - Session crashes in Desktop/SDK when `Read` returned files containing U+2028/U+2029 characters
  - Parallel tool calls where a failed `Read`/`WebFetch`/`Glob` would cancel its siblings — only Bash errors now cascade
  - "Always Allow" saving permission rules that never match again
  - `transcript_path` pointing to the wrong directory for resumed/forked sessions

### CLAUDE.local.md Removed as a Convention

Across four pages, all references to `CLAUDE.local.md` as a local-scope memory file have been removed. This is a coordinated documentation change reflecting the feature's removal.

- **`memory.md` — Local instructions scope row dropped**: The "Local instructions" row (`./CLAUDE.local.md`) has been removed from the CLAUDE.md scopes table entirely. The recommended alternative for private per-project preferences is now importing a file from your home directory via the shared `CLAUDE.md`.
  > For personal preferences you don't want to check in, import a file from your home directory. The import goes in the shared CLAUDE.md, but the file it points to stays on your machine
  - *Implication*: Users relying on `CLAUDE.local.md` for per-project private instructions should migrate to the home-directory import pattern.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

- **`best-practices.md` — CLAUDE.local.md alternative removed**: The project-root CLAUDE.md bullet previously described naming it `CLAUDE.local.md` and `.gitignore`-ing it as an option; that option is gone.
  > **Project root (`./CLAUDE.md`)**: check into git to share with your team
  - *Source*: [Best Practices](https://code.claude.com/docs/en/best-practices.md)

- **`desktop.md` — CLAUDE.local.md compatibility note removed**: The desktop/CLI shared configuration list previously included `CLAUDE.local.md`; now only `CLAUDE.md` is listed.
  > **[CLAUDE.md](/en/memory)** files in your project are used by both
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

- **`settings.md` — Local scope and CLAUDE.md table updated**: The Local scope file pattern is now explicitly `.claude/settings.local.json` (previously `.claude/*.local.*`), and the CLAUDE.md row in the scopes-by-feature table no longer lists a local-scope file.
  > | **Local** | `.claude/settings.local.json` | You, in this repository only | No (gitignored) |
  > | **CLAUDE.md** | `~/.claude/CLAUDE.md` | `CLAUDE.md` or `.claude/CLAUDE.md` | — |
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Tools Reference Table Expanded (`settings.md`)

The built-in tools table has been reorganized alphabetically and expanded with newly documented tools. Several tools were renamed or had descriptions updated.

- **New tools added to the reference**:
  - `CronCreate` — Schedules a recurring or one-shot prompt within the current session (session-scoped; gone when Claude exits). See [scheduled tasks](/en/scheduled-tasks).
  - `CronDelete` — Cancels a scheduled task by ID
  - `CronList` — Lists all scheduled tasks in the session
  - `EnterPlanMode` — Switches to plan mode to design an approach before coding
  - `EnterWorktree` — Creates an isolated git worktree and switches into it
  - `ExitWorktree` — Exits a worktree session and returns to the original directory
  - `ListMcpResourcesTool` — Lists resources exposed by connected MCP servers
  - `ReadMcpResourceTool` — Reads a specific MCP resource by URI
  - `TaskStop` — Kills a running background task by ID (replaces `KillShell`)
  - `TodoWrite` — Manages the session task checklist; available in non-interactive mode and Agent SDK. Interactive sessions use `TaskCreate/Get/List/Update` instead.
  - `ToolSearch` — Searches for and loads deferred tools when tool search is enabled (replaces `MCPSearch`)

- **Tools renamed**:
  - `MCPSearch` → `ToolSearch` (reflects broader applicability beyond MCP tools)
  - `KillShell` → `TaskStop` (generalized from bash shells to any background task type)

- **Description updates**:
  - `Agent`: now "Spawns a subagent with its own context window to handle a task" (previously "Runs a sub-agent to handle complex, multi-step tasks")
  - `ExitPlanMode`: now "Presents a plan for approval and exits plan mode" (previously "Prompts the user to exit plan mode and start coding")

  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

## Notable Details

- **`/config` UX behavioral change**: Escape now cancels changes (instead of closing with saves applied); Enter saves and closes; Space toggles boolean settings. Users with muscle memory for the old behavior should note this.
- **Bash command parsing switched to native module**: Faster initialization and eliminates a memory leak in long sessions. No user-facing API change.
- **Bundle size reduced ~510 KB**: Smaller install footprint.
- **`ToolSearch` now works with `ANTHROPIC_BASE_URL`**: Previously, tool search required no custom base URL to activate. It now activates with `ANTHROPIC_BASE_URL` set as long as `ENABLE_TOOL_SEARCH` is also set.
- **"Always Allow" permission rule fix**: Rules that would never match again are no longer saved, preventing permission configuration bloat over time.
- **`CLAUDE.local.md` removal is consistent across all four affected pages**, indicating a deliberate deprecation rather than an editorial cleanup. Users with existing `CLAUDE.local.md` files should verify whether Claude Code still loads them and plan a migration.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `changelog.md` | Modified | +54/-2 | Added version 2.1.72 entry with features, improvements, and bug fixes |
| `settings.md` | Modified | +34/-25 | Tools table expanded with ~11 new tools; local scope and CLAUDE.md table updated |
| `memory.md` | Modified | +7/-10 | Removed CLAUDE.local.md scope row; updated private preference guidance |
| `best-practices.md` | Modified | +1/-1 | Removed CLAUDE.local.md as an alternative to project CLAUDE.md |
| `desktop.md` | Modified | +1/-1 | Removed CLAUDE.local.md from desktop/CLI shared configuration list |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-10*
