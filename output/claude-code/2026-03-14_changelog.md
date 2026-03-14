# Claude Code Documentation Changes — 2026-03-14

## Summary

Claude Code version 2.1.76 ships MCP elicitation support (MCP servers can now prompt users for structured input mid-task), two new hook event pairs (`Elicitation`/`ElicitationResult` and `PostCompact`), two new CLI flags (`--name`/`-n` and `--effort`), and a new `/effort` slash command. The hooks guide was substantially reworked: the first-hook walkthrough now directs users to edit settings JSON directly, repositioning `/hooks` from an interactive configuration tool to a read-only browser. Fourteen pages were modified across hooks, MCP, CLI, settings, and workflow documentation.

---

## Significant Changes

### Features

- **MCP Elicitation Support**: MCP servers can now request structured user input mid-task via an interactive dialog (form fields or a browser URL). A new section was added to the MCP page documenting this capability, and two new hook events (`Elicitation`, `ElicitationResult`) allow hooks to intercept and override elicitation responses before they reach the server.
  > "Added MCP elicitation support — MCP servers can now request structured input mid-task via an interactive dialog (form fields or browser URL)"
  > "Added new `Elicitation` and `ElicitationResult` hooks to intercept and override responses before they're sent back"
  - *Implication*: MCP tool authors can build interactive flows that collect user input inline without out-of-band channels. Developers using hooks can audit, modify, or veto what gets sent back to the server.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md), [MCP](https://code.claude.com/docs/en/mcp.md)

- **`PostCompact` Hook Event**: A new hook fires after context compaction completes, complementing the existing `PreCompact` event.
  > "`PostCompact` — After context compaction completes"
  - *Implication*: Hooks can now inject fresh context or run cleanup logic immediately after compaction rather than only before it.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **`--name` / `-n` CLI Flag**: Sets a human-readable display name for a session at startup, shown in `/resume` and the terminal title. Named sessions can be resumed with `claude --resume <name>`.
  > "`--name`, `-n` — Set a display name for the session, shown in `/resume` and the terminal title. You can resume a named session with `claude --resume <name>`. `/rename` changes the name mid-session and also shows it on the prompt bar"
  - *Implication*: Named sessions make managing concurrent or long-running Claude Code sessions significantly easier — no more copying UUIDs to resume specific sessions.
  - *Source*: [CLI reference](https://code.claude.com/docs/en/cli-reference.md)

- **`--effort` CLI Flag**: Sets the model effort level (`low`, `medium`, `high`, `max`) at session startup. Session-scoped and does not persist to settings.
  > "`--effort` — Set the effort level for the current session. Options: `low`, `medium`, `high`, `max` (Opus 4.6 only). Session-scoped and does not persist to settings"
  - *Implication*: Effort level is now a first-class launch parameter alongside `--model`, enabling scripted sessions with explicit reasoning budgets without touching persistent configuration.
  - *Source*: [CLI reference](https://code.claude.com/docs/en/cli-reference.md)

- **`/effort` Slash Command**: New in-session command to change effort level without navigating the `/model` picker.
  > "`/effort [low|medium|high|max|auto]` — Set the model effort level. `low`, `medium`, and `high` persist across sessions. `max` applies to the current session only and requires Opus 4.6. `auto` resets to the model default. Without an argument, shows the current level. Takes effect immediately without waiting for the current response to finish"
  - *Implication*: Effort can now be changed at any point mid-session with a single command, and `auto` provides an explicit way to return to the model default.
  - *Source*: [Built-in commands](https://code.claude.com/docs/en/commands.md)

- **`worktree.sparsePaths` Setting**: New configuration option under a new `Worktree settings` section that limits git sparse-checkout to specified directories when using `claude --worktree` in large monorepos.
  > "Added `worktree.sparsePaths` setting for `claude --worktree` in large monorepos to check out only the directories you need via git sparse-checkout"
  - *Implication*: Reduces worktree startup time and disk usage in monorepos by skipping directories the session doesn't need.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`feedbackSurveyRate` Setting**: Enterprise admins can now configure the sampling rate for in-session quality surveys via this new setting. Per-user opt-out remains available via `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

### Configuration & Documentation

- **`/hooks` repositioned as read-only**: The hooks guide's first-hook walkthrough was rewritten to guide users to edit `~/.claude/settings.json` directly rather than using the `/hooks` interactive menu. The menu is now described only as a read-only configuration browser. The best-practices page was updated to match.
  > *(New)*: "To create a hook, add a `hooks` block to a settings file. This walkthrough creates a desktop notification hook..."
  > *(Previous)*: "The fastest way to create a hook is through the `/hooks` interactive menu in Claude Code."
  > *(best-practices.md, new)*: "Edit `.claude/settings.json` directly to configure hooks by hand, and run `/hooks` to browse what's configured."
  - *Implication*: Hook authoring now has a clear recommended path: JSON config or asking Claude. The `/hooks` menu is no longer framed as a hook creation tool.
  - *Source*: [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md), [Best practices](https://code.claude.com/docs/en/best-practices.md)

- **Notification hook example shows full JSON config**: The hooks guide's Notification hook walkthrough replaced bare shell command snippets with full `settings.json` JSON blocks. A new step was added to narrow the hook matcher to specific notification types. The new `elicitation_dialog` matcher value is included as an option.

  | Matcher | Fires when |
  |---|---|
  | `permission_prompt` | Claude needs approval for a tool use |
  | `idle_prompt` | Claude is done and waiting for the next prompt |
  | `auth_success` | Authentication completes |
  | `elicitation_dialog` | Claude is asking the user a question |

  - *Source*: [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)

- **`CLAUDE_CODE_EFFORT_LEVEL` env var updated**: Now documents `max` (Opus 4.6 only) and `auto` (reset to model default) as valid values, and clarifies its precedence over `/effort` and the `effortLevel` setting.
  > "Set the effort level for supported models. Values: `low`, `medium`, `high`, `max` (Opus 4.6 only), or `auto` to use the model default. Takes precedence over `/effort` and the `effortLevel` setting."
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **`/effort` referenced in cost-reduction guidance**: The costs page updated its advice on managing extended thinking costs to reference `/effort` alongside `/model` as a way to reduce thinking token spend.
  - *Source*: [Costs](https://code.claude.com/docs/en/costs.md)

- **Common workflows expanded**: Plan Mode now has a structured multi-step walkthrough covering `--permission-mode plan`, headless mode (`-p`), and `Ctrl+G` to edit a plan in an external editor. The subagents section was also expanded with explicit steps for viewing, using, and creating custom subagents.
  - *Source*: [Common workflows](https://code.claude.com/docs/en/common-workflows.md)

---

### Bug Fixes (v2.1.76)

- **Deferred tool schema loss after compaction**: Tools loaded via `ToolSearch` were losing their input schemas after conversation compaction, causing array and number parameters to be rejected with type errors. Fixed.
- **Auto-compaction circuit breaker**: Auto-compaction now stops retrying after 3 consecutive failures instead of retrying indefinitely.
- **Plan mode re-approval**: Fixed plan mode asking for re-approval after the plan was already accepted.
- **`Bash(cmd:*)` permission rules with `#` in quoted arguments**: Rules were not matching when a quoted argument contained `#`. Fixed.
- **Clipboard in tmux over SSH**: Now attempts both direct terminal write and tmux clipboard integration.
- **`/export` success message**: Fixed showing only the filename instead of the full file path.
- **Voice mode on Windows (npm install)**: Fixed `/voice` not working on Windows when installed via npm.
- **Voice mode keypresses**: Fixed voice mode swallowing keypresses while a permission dialog or plan editor was open.
- **Remote Control reliability**: Fixed sessions silently dying when the server reaps idle environments; rapid messages now batched instead of queued one-at-a-time; stale work items no longer cause redelivery after JWT refresh.
- **Bridge session recovery**: Fixed bridge sessions failing to recover after extended WebSocket disconnects.
- **Slash commands not found for exact match of soft-hidden commands**: Fixed.
- **LSP plugin server registration**: Fixed LSP plugins not registering servers when LSP Manager initialized before marketplaces were reconciled.
- **MCP reconnect spinner**: Fixed the spinner persisting after successful reconnection.
- **1M context "Context limit reached" error**: Fixed a spurious error when invoking a skill with `model:` frontmatter on a 1M-context session.
- **Adaptive thinking error with non-standard model strings**: Fixed "adaptive thinking is not supported on this model" error.
- **`[VSCode]`**: Fixed gitignore patterns containing commas silently excluding entire filetypes from the @-mention file picker.
- *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

### Improvements (v2.1.76)

- **`--worktree` startup performance**: Now reads git refs directly and skips redundant `git fetch` when the remote branch is already available locally.
- **Background agent partial results preserved**: Killing a background agent now preserves its partial results in the conversation context.
- **Model fallback notifications**: Now always visible (previously hidden behind `--verbose`), with human-friendly model names.
- **Stale worktree cleanup**: Worktrees left behind after an interrupted parallel run are now automatically cleaned up.
- **Remote Control session titles**: Now derived from the user's first prompt instead of showing "Interactive session".
- **Blockquote readability on dark terminals**: Text is now italic with a left bar instead of dim.
- **`/voice` language feedback**: Now shows the dictation language on enable and warns if the `language` setting isn't supported for voice input.
- **`--plugin-dir` accepts one path per flag**: Updated to only accept one path to support subcommands. Use repeated `--plugin-dir` for multiple directories.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| hooks.md | Modified | +177/-21 | Added `PostCompact`, `Elicitation`, and `ElicitationResult` hook events with full input/output schemas; updated hook lifecycle diagram and event table |
| common-workflows.md | Modified | +85/-45 | Expanded Plan Mode walkthrough with startup flags and editor shortcut; expanded subagents section |
| commands.md | Modified | +64/-63 | Added `/effort` command entry; updated command descriptions throughout |
| cli-reference.md | Modified | +54/-52 | Added `--effort` and `--name`/`-n` flags to the flags reference table |
| hooks-guide.md | Modified | +34/-45 | Rewrote first-hook walkthrough to use JSON config instead of `/hooks` interactive menu; added matcher narrowing step |
| changelog.md | Modified | +38/-0 | Added v2.1.76 release notes (March 14, 2026) |
| mcp.md | Modified | +13/-0 | Added "Respond to MCP elicitation requests" section |
| settings.md | Modified | +11/-0 | Added `Worktree settings` section with `worktree.sparsePaths` |
| model-config.md | Modified | +8/-4 | Updated effort level docs to include `/effort` command and `max`/`auto` values |
| overview.md | Modified | +5/-5 | Minor content updates |
| quickstart.md | Modified | +5/-5 | Minor content updates |
| env-vars.md | Modified | +1/-1 | Updated `CLAUDE_CODE_EFFORT_LEVEL` to document `max` and `auto` values and precedence |
| costs.md | Modified | +1/-1 | Updated effort-level cost-reduction guidance to reference `/effort` |
| best-practices.md | Modified | +1/-1 | Updated `/hooks` description to reflect read-only browser role |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-14*
