# Claude Code Documentation Changes — 2026-03-31

## Summary

A new "fullscreen rendering" research preview was introduced (opt-in via `CLAUDE_CODE_NO_FLICKER=1`, requires v2.1.88+) that eliminates terminal flicker, keeps memory usage flat, and adds mouse support. Supporting changes landed across env vars, terminal config, agent teams, code review troubleshooting, and the desktop setup guide, with minor hook debugging clarifications.

## Significant Changes

### Features

- **Fullscreen Rendering (Research Preview)**: A new alternate rendering mode for the Claude Code CLI that uses the terminal's alternate screen buffer (like `vim` or `htop`) to eliminate flicker, keep memory usage flat in long conversations, and add mouse support. Enabled via `CLAUDE_CODE_NO_FLICKER=1`. Requires Claude Code v2.1.88 or later.
  > "Fullscreen rendering is an alternative rendering path for the Claude Code CLI that eliminates flicker, keeps memory usage flat in long conversations, and adds mouse support. It draws the interface on the terminal's alternate screen buffer, like vim or htop, and only renders messages that are currently visible."
  - *Implication*: Particularly useful in VS Code integrated terminal, tmux, and iTerm2 where scroll position jumping or screen flashing during tool output streaming is common.
  - *Source*: [Fullscreen rendering](https://code.claude.com/docs/en/fullscreen.md)

### Configuration

- **Three new environment variables for fullscreen rendering**:
  - `CLAUDE_CODE_NO_FLICKER=1` — Enables fullscreen rendering (the research preview itself).
  - `CLAUDE_CODE_DISABLE_MOUSE=1` — Disables mouse capture within fullscreen rendering while retaining flicker-free rendering and flat memory. Restores the terminal's native copy-on-select behavior.
  - `CLAUDE_CODE_SCROLL_SPEED` — Sets the mouse wheel scroll multiplier (1–20). Useful when terminals send one scroll event per physical notch without amplification (e.g., VS Code integrated terminal).
    > "Set to 3 to match vim if your terminal sends one wheel event per notch without amplification"
  - *Implication*: `CLAUDE_CODE_DISABLE_MOUSE=1` is the recommended escape hatch for SSH or tmux users who rely on native terminal text selection.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

### Agent Teams

- **Subagent definitions usable as teammate types**: Teammates spawned in an agent team can now reference any subagent definition (from project, user, plugin, or CLI scope). The teammate inherits the subagent's system prompt, tools, and model, letting roles like `security-reviewer` be defined once and reused across both delegated subagents and team teammates.
  > "To use a subagent definition, mention it by name when asking Claude to spawn the teammate: `Spawn a teammate using the security-reviewer agent type to audit the auth module.`"
  - *Implication*: Reduces duplication when a role needs to work both as a subagent and as a parallel teammate in multi-agent workflows.
  - *Source*: [Agent teams](https://code.claude.com/docs/en/agent-teams.md)

- **Team config is runtime state — do not hand-edit**: Documentation now explicitly warns that `~/.claude/teams/{team-name}/config.json` is overwritten on every state update and must not be pre-authored or edited manually.
  > "The team config holds runtime state such as session IDs and tmux pane IDs, so don't edit it by hand or pre-author it: your changes are overwritten on the next state update."
  - *Implication*: Also clarifies there is no project-level team config — a file like `.claude/teams/teams.json` in the project directory is not recognized by Claude Code.
  - *Source*: [Agent teams](https://code.claude.com/docs/en/agent-teams.md)

### Code Review

- **New Troubleshooting section**: Added guidance for two common failure modes: retriggering a failed or timed-out review, and locating findings that don't appear as inline PR comments.
  > "The Re-run button in GitHub's Checks tab does not retrigger Code Review. Use the comment command or a new push instead."
  - *Implication*: To retrigger, comment `@claude review once` on the PR. Findings that GitHub rejected as inline comments (e.g., on lines that moved) are still available in the check run Details, Files changed annotations, and the review body under **Additional findings**.
  - *Source*: [Code review](https://code.claude.com/docs/en/code-review.md)

- **Annotations are independent of inline comments**: Clarified that the severity table and per-line annotations in the **Files changed** tab are written to the check run separately from inline review comments.
  > "Annotations and the severity table are written to the check run independently of inline review comments, so they remain available even if GitHub rejects an inline comment on a line that moved."
  - *Source*: [Code review](https://code.claude.com/docs/en/code-review.md)

### Desktop App

- **Computer use setup flow restructured**: The enable instructions for computer use were rewritten as a three-step guide. A new first step explicitly requires updating to the latest Claude Desktop before proceeding.
  > "Make sure you have the latest version of Claude Desktop. Download or update at claude.com/download, then restart the app."
  - *Implication*: The page now also notes the feature requires macOS with a Pro or Max plan, and corrects the settings path from `Settings > Desktop app > General` to `Settings > General` (under **Desktop app**).
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

### Hooks

- **`TaskCreated` exit code 2 behavior clarified**: The description changed from "Prevents the task from being created" to "Rolls back the task creation" — a semantic distinction indicating the task is created first, then rolled back, rather than blocked upfront.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

- **Hook debug output updated**: The `--debug` example output was simplified, and verbose hook matching details (matcher counts, query matching) are now surfaced via a separate env var rather than `Ctrl+O`.
  > "For more granular hook matching details, set `CLAUDE_CODE_DEBUG_LOG_LEVEL=verbose` to see additional log lines such as hook matcher counts and query matching."
  - *Implication*: `Ctrl+O` is no longer documented as toggling verbose hook output.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

## New Pages

- **[fullscreen.md](https://code.claude.com/docs/en/fullscreen.md)** — Complete reference for the fullscreen rendering research preview: how to enable it, mouse support details, scroll shortcuts and keybinding customization, transcript mode with `less`-style search (`Ctrl+o`), tmux compatibility notes (including a warning against `tmux -CC` / iTerm2 integration mode), and how to disable mouse capture while keeping flicker-free rendering.

## Notable Details

- The fullscreen rendering page notes a specific incompatibility: **iTerm2's tmux integration mode (`tmux -CC`)** causes mouse wheel and double-click to malfunction. Regular tmux inside iTerm2 (without `-CC`) is fine.
- The `CLAUDE_CODE_SCROLL_SPEED` documentation suggests `3` as the value that matches `vim`'s default scroll behavior — a practical calibration hint for users migrating muscle memory from terminal text editors.
- The sub-agents page received a one-line cross-reference note pointing to the new agent-teams subagent integration, keeping both pages mutually consistent.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| fullscreen.md | New | +145 | Full reference for opt-in fullscreen rendering research preview |
| code-review.md | Modified | +22/-1 | Added Troubleshooting section; clarified annotation independence |
| desktop.md | Modified | +21/-5 | Restructured computer use setup as a step-by-step guide; corrected settings path |
| agent-teams.md | Modified | +16/-0 | Added subagent-as-teammate feature; clarified team config is runtime state only |
| hooks.md | Modified | +4/-5 | Clarified TaskCreated rollback behavior; updated debug instructions |
| terminal-config.md | Modified | +4/-0 | Added "Reduce flicker and memory usage" section pointing to fullscreen rendering |
| env-vars.md | Modified | +3/-0 | Added CLAUDE_CODE_NO_FLICKER, CLAUDE_CODE_DISABLE_MOUSE, CLAUDE_CODE_SCROLL_SPEED |
| sub-agents.md | Modified | +2/-0 | Added cross-reference note: subagent definitions are usable in agent teams |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-31*
