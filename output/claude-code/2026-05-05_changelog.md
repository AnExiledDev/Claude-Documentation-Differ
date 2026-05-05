# Claude Code Documentation Changes — 2026-05-05

## Summary

Seven pages were modified with 116 additions and 27 deletions. The primary change is documentation of the v2.1.128 release (May 4, 2026), which includes a large batch of bug fixes and several CLI/MCP behavioral changes. Supporting docs were updated to reflect new Windows PowerShell examples, expanded LLM hook semantics, and a new VS Code troubleshooting entry for macOS Tahoe.

## Significant Changes

### Release: v2.1.128 (May 4, 2026)

- **`EnterWorktree` branch-creation fix**: `EnterWorktree` now creates the new branch from local `HEAD` as documented, instead of `origin/<default-branch>`. Previously, unpushed commits were silently dropped.
  > `EnterWorktree` now creates the new branch from local HEAD as documented, instead of `origin/<default-branch>` — unpushed commits are no longer dropped
  - *Implication*: Agents and scripts using `EnterWorktree` on branches with unpushed commits will no longer lose those commits.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`OTEL_*` variables no longer inherited by subprocesses**: Bash, hooks, MCP, and LSP subprocesses no longer inherit `OTEL_*` environment variables.
  > Subprocesses (Bash, hooks, MCP, LSP) no longer inherit `OTEL_*` environment variables, so OTEL-instrumented apps run via the Bash tool no longer pick up the CLI's own OTLP endpoint
  - *Implication*: Fixes cross-contamination where OTEL-instrumented apps invoked via the Bash tool received the CLI's own OTLP configuration.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`workspace` is now a reserved MCP server name**: Existing MCP servers named `workspace` will be skipped with a warning.
  > MCP: `workspace` is now a reserved server name — existing servers with that name will be skipped with a warning
  - *Implication*: Users with an MCP server configured as `workspace` must rename it.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`--plugin-dir` now accepts `.zip` archives**: Plugin directories can now be supplied as zip archives in addition to unpacked directories.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`--channels` now works with console/API key authentication**: Console organizations with managed settings must set `channelsEnabled: true` to enable channels.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Bare `/color` picks a random session color**: Running `/color` with no arguments now selects a random color for the session.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/mcp` shows tool counts and zero-tool warnings**: The `/mcp` command now displays the tool count for each connected server and flags servers that connected with 0 tools.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **MCP reconnect no longer floods the conversation**: Re-announced tools on reconnect are summarized by server prefix rather than listing every tool name.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **SDK hosts receive persistent `localSettings` suggestion**: "Always allow" for Bash permission prompts now writes to `.claude/settings.local.json` rather than a transient setting.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Notable bug fixes in v2.1.128**:
  - Fixed crash loop when piping >10 MB to `claude -p` via stdin
  - Fixed parallel shell tool calls: a failing read-only command (grep, git diff, ls) no longer cancels sibling calls
  - Fixed `headless --output-format stream-json`: `init.plugin_errors` now includes `--plugin-dir` load failures
  - Fixed sub-agent progress summaries missing prompt cache (~3× `cache_creation` reduction)
  - Fixed `/plugin update` never detecting new versions of npm-sourced plugins
  - Fixed sub-agent summaries firing repeatedly on idle sub-agents (token cost reduction)
  - Fixed MCP stdio servers receiving corrupted arguments when `CLAUDE_CODE_SHELL_PREFIX` is set and an argument contains spaces or shell metacharacters
  - Fixed Bedrock default model resolving to `global.*` instead of region-appropriate prefix
  - Fixed markdown link labels being lost on terminals without OSC 8 hyperlink support — links now render as `label (url)` instead of just the URL
  - Fixed sessions on 1M-context models with smaller autocompact windows being falsely blocked with "Prompt is too long"
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### LLM Hook `ok: false` Semantics Expanded

- **Per-event blocking behavior now fully documented**: Both `hooks.md` and `hooks-guide.md` were updated to specify exactly what happens when an LLM hook returns `ok: false`, broken out by event type.
  > What happens on `ok: false` depends on the event:
  > * `Stop` and `SubagentStop`: the reason is fed back to Claude as its next instruction and the turn continues
  > * `PreToolUse`: the tool call is denied and the reason is returned to Claude as the tool error, equivalent to a command hook's `permissionDecision: "deny"`
  > * `PostToolUse`, `PostToolBatch`, `UserPromptSubmit`, and `UserPromptExpansion`: the turn ends and the reason appears in the chat as a warning line
  > * `PostToolUseFailure`, `TaskCreated`, and `TaskCompleted`: the reason is returned to Claude as a tool error, similar to `PreToolUse`
  > * `PermissionRequest`: `ok: false` has no effect. To deny an approval from a hook, use a command hook returning `hookSpecificOutput.decision.behavior: "deny"`
  - *Implication*: Previously the docs only distinguished `Stop`/`SubagentStop` from "all other events." The new breakdown adds `PreToolUse`, `PostToolUseFailure`, `TaskCreated`, `TaskCompleted`, and `PermissionRequest` as distinct cases — relevant for anyone writing LLM hooks that need to control flow on these events.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md), [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)

### Sub-agents: Windows PowerShell Support Added

- **`--agents` flag now has a Windows PowerShell example**: The `--agents` CLI example was converted from a single bash block to a tabbed view showing macOS/Linux/WSL and Windows PowerShell variants (using PowerShell here-string syntax `@'...'@`).
  - *Implication*: Windows users can now follow a documented pattern for passing the multi-line JSON argument via PowerShell.
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

- **Hook scripts on Windows now documented**: Sub-agents documentation now explicitly notes that on Windows, hook scripts should be written in PowerShell with `shell: powershell` in the hook entry.
  > On Windows, write hook scripts in PowerShell and add `shell: powershell` to the hook entry as shown in running hooks in PowerShell
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

- **Subagent loading clarification**: The session-reload note was updated to distinguish between file-based and UI-created subagents.
  > Subagents created through the `/agents` interface take effect immediately without a restart. [Subagents added or edited directly on disk require a session restart to load.]
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

- **Built-in subagent name corrected**: The "Claude Code Guide" built-in subagent is now documented as `claude-code-guide` (lowercase, matching the actual identifier format used by other built-in agents).
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

### VS Code: macOS Tahoe `Cmd+Esc` Conflict

- **New troubleshooting entry for `Cmd+Esc` on macOS Tahoe**: macOS Tahoe and later binds `Cmd+Esc` to the system Game Overlay by default, intercepting the keypress before VS Code receives it.
  > On macOS Tahoe and later, the system Game Overlay shortcut is bound to `Cmd+Esc` by default and intercepts the keypress before it reaches VS Code. To free the shortcut: Open System Settings → Keyboard → Keyboard Shortcuts → Game Controllers → Clear the Game Overlay checkbox
  - *Implication*: Users on macOS Tahoe+ who find `Cmd+Esc` non-functional for Claude Code should either clear the system shortcut or rebind the `Claude Code: Focus input` action in VS Code.
  - *Source*: [VS Code integration](https://code.claude.com/docs/en/vs-code.md)

### Features Overview: Context Window Row Added

- **Skills vs. Subagents comparison table gains "Context window impact" row**: A new row was added explicitly comparing how skills and subagents affect context consumption.
  > | **Context window impact** | Adds to your main window | Uses a separate window with its own input and output tokens |
  - *Implication*: Clarifies a previously undocumented distinction — subagents do not consume tokens from the main session context window.
  - *Source*: [Features overview](https://code.claude.com/docs/en/features-overview.md)

### Voice Dictation: Reserved Keys Note

- **Clarification on keys that cannot be bound**: A new sentence explains that some keys are never delivered to terminal applications and cannot be bound (e.g., `Caps Lock`).
  > Some keys are not delivered to terminal applications and cannot be bound at all. For example, `Caps Lock` shows an error if you try to bind it.
  - *Implication*: Explains an error users may encounter when attempting to configure `Caps Lock` as the push-to-talk key.
  - *Source*: [Voice dictation](https://code.claude.com/docs/en/voice-dictation.md)

## Notable Details

- The `sessionTitle` field in `UserPromptSubmit` hook output had its description simplified — the phrase "same effect as `/rename`" was removed. The behavior is unchanged, but the cross-reference is gone.
- The auto mode classifier error now includes a hint (`retry`, `/compact`, or run with `--debug`) when it cannot evaluate an action — previously the error was opaque.
- `/model` picker collapsed duplicate Opus 4.7 entries and now shows the current Opus model as "Opus" rather than "Opus 4.7", suggesting a display-name normalization as the model lineup evolves.
- The v2.1.128 entry documents a fix for stale `installed_plugins.json` entries pointing at deleted cache directories polluting `PATH` — a subtle but impactful correctness fix for plugin management.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +40/-0 | Added v2.1.128 release entry (May 4, 2026) with ~30 items |
| sub-agents.md | Modified | +43/-18 | Windows PowerShell examples, loading clarification, hook script guidance |
| hooks.md | Modified | +10/-2 | Expanded `ok: false` semantics for all LLM hook event types |
| features-overview.md | Modified | +6/-5 | Added "Context window impact" row to Skills vs. Subagents table |
| vs-code.md | Modified | +10/-0 | New troubleshooting section for `Cmd+Esc` on macOS Tahoe |
| hooks-guide.md | Modified | +4/-1 | Aligned `ok: false` event-specific descriptions with hooks.md |
| voice-dictation.md | Modified | +3/-1 | Added note on keys not deliverable to terminal apps (e.g. Caps Lock) |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-05*
