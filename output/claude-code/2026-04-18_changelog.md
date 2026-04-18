# Claude Code Documentation Changes — 2026-04-18

## Summary

11 pages were modified in this update (76 additions, 52 deletions). The changes center on three themes: expanded keyboard input capabilities (text selection extension in fullscreen mode, new multiline editing shortcuts), a new `network.deniedDomains` sandbox setting for fine-grained network blocking, and a bug fix in version 2.1.114. Several smaller clarifications touch permissions, remote control, scheduled loops, and the ultrareview confirmation dialog.

## Significant Changes

### Sandbox & Permissions

- **New `network.deniedDomains` setting**: A new sandbox configuration key blocks specific domains even when a broader `allowedDomains` wildcard would otherwise permit them. Takes precedence over `allowedDomains` and merges from all settings sources regardless of `allowManagedDomainsOnly`.
  > `network.deniedDomains` — Array of domains to block for outbound network traffic. Supports the same wildcard syntax as `allowedDomains`. Takes precedence over `allowedDomains` when both match. Merged from all settings sources regardless of `allowManagedDomainsOnly`.
  - *Implication*: Administrators can now allowlist `*.example.com` while carving out exceptions like `uploads.example.com` without restructuring their entire domain allowlist.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md), [Sandboxing](https://code.claude.com/docs/en/sandboxing.md), [Permissions](https://code.claude.com/docs/en/permissions.md)

- **Exec wrapper limitations documented**: `watch`, `setsid`, `ionice`, and `flock` are now explicitly documented as always-prompting — prefix rules like `Bash(watch *)` do not auto-approve them. The same restriction applies to `find -exec` and `find -delete`.
  > Exec wrappers such as `watch`, `setsid`, `ionice`, and `flock` always prompt and cannot be auto-approved by a prefix rule like `Bash(watch *)`. The same applies to `find` with `-exec` or `-delete`: a `Bash(find *)` rule does not cover these forms. To approve a specific invocation, write an exact-match rule for the full command string.
  - *Implication*: Rules designed to broadly approve a command via prefix may silently fail for these wrappers. Developers relying on `Bash(find *)` to cover `-exec` variants should add exact-match rules.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

- **Fixed wildcard example in permissions docs**: The example `Bash(git:*)` (which used a colon) was corrected to `Bash(git *)` (with a space), matching the documented syntax for multi-argument wildcard matching.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

### Keyboard Input & Text Editing

- **New selection extension keybindings in fullscreen mode**: Six new keybinding actions — `selection:extendLeft`, `selection:extendRight`, `selection:extendUp`, `selection:extendDown`, `selection:extendLineStart`, `selection:extendLineEnd` — are now documented with default bindings (`Shift+Arrow`, `Shift+Home`, `Shift+End`). The viewport scrolls automatically when the selection reaches the top or bottom edge.
  > With a selection active, hold `Shift` and press the arrow keys to extend it from the keyboard. `Shift+↑` and `Shift+↓` scroll the viewport when the selection reaches the top or bottom edge. `Shift+Home` and `Shift+End` extend to the start or end of the current line.
  - *Implication*: Users in fullscreen mode can now select text using keyboard-only workflows; all six actions are rebindable via `~/.claude/keybindings.json`.
  - *Source*: [Fullscreen](https://code.claude.com/docs/en/fullscreen.md), [Keybindings](https://code.claude.com/docs/en/keybindings.md)

- **New multiline input editing shortcuts**: `Ctrl+A` (move to line start) and `Ctrl+E` (move to line end) are now documented for multiline prompt input, along with `Ctrl+W` (delete previous word, with `Ctrl+Backspace` alias on Windows).
  > `Ctrl+U` — Delete from cursor to line start. Stores deleted text for pasting. Repeat to clear across lines in multiline input. On macOS, terminal emulators including iTerm2 and Terminal.app map `Cmd+Backspace` to this shortcut.
  - *Implication*: `Ctrl+U` behavior is clarified — it deletes from cursor to line start (not the entire buffer), and repeating it clears across lines. `Ctrl+Y` now also pastes content deleted by `Ctrl+W`.
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

- **`Ctrl+P`/`Ctrl+N` as history navigation alternatives**: Up/Down arrow keys now share their entry with `Ctrl+P`/`Ctrl+N`. The behavior in multiline input is also clarified: arrows and these shortcuts first move the cursor within the prompt; history navigation only activates once the cursor is already at the top or bottom edge.
  > In multiline input, first moves the cursor within the prompt. Once the cursor is already on the top or bottom edge, pressing again navigates command history.
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

### Scheduled Tasks

- **New "Stop a loop" section**: Documents that pressing `Esc` while a `/loop` is waiting for its next iteration cancels the pending wakeup. Explicitly distinguishes this from tasks scheduled via natural language (those are unaffected by `Esc` and must be deleted through the task manager).
  > To stop a `/loop` while it is waiting for the next iteration, press `Esc`. This clears the pending wakeup so the loop does not fire again. Tasks you scheduled by asking Claude directly are not affected by `Esc` and stay in place until you delete them.
  - *Source*: [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks.md)

### Commands

- **`/fewer-permission-prompts` replaces `/less-permission-prompts`**: The skill command for scanning transcripts and adding allowlist rules to `.claude/settings.json` has been renamed. The old `/less-permission-prompts` entry is removed from the commands table.
  - *Implication*: Users with documentation bookmarks or muscle memory for `/less-permission-prompts` should update to `/fewer-permission-prompts`.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

- **`/compact` description expanded**: The command description now explains that it summarizes (rather than just "compacts") the conversation and links to context-window documentation covering what survives compaction.
  > Free up context by summarizing the conversation so far. Optionally pass focus instructions for the summary. See how compaction handles rules, skills, and memory files.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

### Remote Control

- **`@` file path autocomplete in Remote Control sessions**: The feature list for Remote Control now notes that typing `@` autocompletes file paths from the local project, even when connected from a browser or mobile device.
  > your filesystem, MCP servers, tools, and project configuration all stay available, and typing `@` autocompletes file paths from your local project
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

- **`/extra-usage` added to remote-capable commands**: `/extra-usage` is now listed among the commands that work from mobile and web (alongside `/compact`, `/clear`, `/context`, `/cost`, `/exit`, `/recap`, and `/reload-plugins`).
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

### Bug Fixes

- **v2.1.114 — Permission dialog crash fix**: Version 2.1.114 (April 18, 2026) fixes a crash in the permission dialog that occurred when an agent teams teammate requested tool permission.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

## Notable Details

- **Ultrareview confirmation dialog now shows scope detail**: The dialog now includes the file and line count when reviewing a branch, giving developers a clearer cost/scope signal before confirming.
  > Claude Code shows a confirmation dialog with the review scope (including the file and line count when reviewing a branch), your remaining free runs, and the estimated cost.
  - *Source*: [Ultrareview](https://code.claude.com/docs/en/ultrareview.md)

- **`network.deniedDomains` merges across all sources**: Unlike `allowedDomains` (which can be locked to managed settings via `allowManagedDomainsOnly`), `deniedDomains` is always merged from user, project, and managed settings. This means individual developers can add their own deny entries even in managed deployments.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| settings.md | Modified | +24/-22 | Added `network.deniedDomains` setting and updated example config |
| keybindings.md | Modified | +20/-14 | Added 6 selection-extension keybinding actions for fullscreen mode |
| interactive-mode.md | Modified | +12/-9 | New `Ctrl+A`, `Ctrl+E`, `Ctrl+W` shortcuts; clarified multiline cursor/history navigation |
| scheduled-tasks.md | Modified | +4/-0 | New "Stop a loop" section documenting `Esc` to cancel pending loop |
| permissions.md | Modified | +4/-2 | Documented exec wrapper limitations; fixed `Bash(git *)` example; added `deniedDomains` mention |
| changelog.md | Modified | +4/-0 | Added v2.1.114 entry (permission dialog crash fix) |
| fullscreen.md | Modified | +2/-0 | Documented Shift+arrow keyboard selection extension |
| commands.md | Modified | +2/-2 | Renamed `/less-permission-prompts` → `/fewer-permission-prompts`; expanded `/compact` description |
| remote-control.md | Modified | +2/-2 | Added `@` path autocomplete note; added `/extra-usage` to remote-capable commands |
| sandboxing.md | Modified | +1/-0 | Added `deniedDomains` bullet to configuration overview |
| ultrareview.md | Modified | +1/-1 | Confirmation dialog now shows file and line count for branch reviews |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-18*
