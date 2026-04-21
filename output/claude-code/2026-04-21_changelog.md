# Claude Code Documentation Changes — 2026-04-21

## Summary

Version 2.1.116 was released on April 20, 2026 with performance improvements, bug fixes, and UX polish. Alongside the release, the terminal configuration guide was significantly restructured from a feature list into a symptom-based troubleshooting format, and hooks documentation was clarified to explain how the `if` field matches Bash subcommands rather than whole commands.

## Significant Changes

### Version Release: 2.1.116 (April 20, 2026)

- **`/resume` performance on large sessions**: Sessions of 40MB+ load up to 67% faster; dead-fork entries are handled more efficiently.
  > `/resume` on large sessions is significantly faster (up to 67% on 40MB+ sessions) and handles sessions with many dead-fork entries more efficiently
  - *Implication*: Long-running or frequently resumed sessions no longer incur the previous load penalty.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **MCP startup optimization**: `resources/templates/list` is now deferred until the first `@`-mention, reducing startup time when multiple stdio MCP servers are configured.
  - *Implication*: Faster launch for projects with many MCP integrations.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Fullscreen scroll sensitivity in editor terminals**: `/terminal-setup` now configures the editor's scroll sensitivity for VS Code, Cursor, and Windsurf.
  > Smoother fullscreen scrolling in VS Code, Cursor, and Windsurf terminals — `/terminal-setup` now configures the editor's scroll sensitivity
  - *Implication*: Running `/terminal-setup` picks up this new configuration automatically; no separate step needed.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Thinking spinner progress display**: The spinner now shows inline progress text ("still thinking", "thinking more", "almost done thinking") replacing the separate hint row.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`/config` search matches option values**: Searching "vim" in `/config` now surfaces the Editor mode setting.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`/doctor` accessible during response**: Can now be opened while Claude is responding, without waiting for the turn to finish.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Plugin dependency auto-install**: `/reload-plugins` and background plugin auto-update now auto-install missing plugin dependencies from previously added marketplaces.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **GitHub rate limit hint in Bash tool**: When `gh` commands hit GitHub's API rate limit, agents now receive a hint to back off rather than retry blindly.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Usage tab improvements**: The Settings Usage tab now shows 5-hour and weekly usage immediately and no longer fails when the usage endpoint is rate-limited.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Agent frontmatter hooks**: Hooks declared in agent frontmatter now fire when the agent runs as a main-thread agent via `--agent`.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Security fix — sandbox auto-allow**: Sandbox auto-allow no longer bypasses the dangerous-path safety check for `rm`/`rmdir` targeting `/`, `$HOME`, or other critical system directories.
  > Security: sandbox auto-allow no longer bypasses the dangerous-path safety check for `rm`/`rmdir` targeting `/`, `$HOME`, or other critical system directories
  - *Implication*: This closes a potential data-loss vector for automated workflows that rely on sandbox auto-allow.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Bug fixes**: Devanagari and Indic script rendering alignment; Ctrl+- undo in Kitty protocol terminals (iTerm2, Ghostty, kitty, WezTerm, Windows Terminal); Cmd+Left/Right line navigation in Kitty protocol terminals (Warp fullscreen, kitty, Ghostty, WezTerm); Ctrl+Z hang when launched via wrapper (npx, bun run); scrollback duplication in inline mode on resize; modal search overflow at short terminal heights; VS Code integrated terminal blank cells during scrolling; intermittent API 400 error from cache control TTL ordering; `/branch` rejecting transcripts >50MB; `/resume` silently showing empty conversations on large session load errors; `/plugin` Installed tab duplicate display; `/update` and `/tui` not working after entering a worktree mid-session.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

---

### Terminal Configuration Guide — Major Restructure

- **Page reorganized as symptom-based troubleshooting guide**: The terminal configuration page was retitled from "Optimize your terminal setup" to "Configure your terminal for Claude Code" and now opens with a symptom index.
  > Claude Code works in any terminal without configuration. This page is for when something specific is not behaving the way you expect. Find your symptom below.
  - *Implication*: Readers can jump directly to their specific problem rather than reading a full feature list. The old section-based structure (Themes, Line breaks, Notification setup, etc.) is gone.
  - *Source*: [terminal-config.md](https://code.claude.com/docs/en/terminal-config.md)

- **Shift+Enter terminal support expanded**: Warp and Apple Terminal are now listed as supporting Shift+Enter natively (no setup required), joining Ghostty, Kitty, iTerm2, and WezTerm. VS Code, Cursor, Windsurf, Alacritty, and Zed still require `/terminal-setup`.
  > | Ghostty, Kitty, iTerm2, WezTerm, Warp, Apple Terminal | Works without setup |
  > | VS Code, Cursor, Windsurf, Alacritty, Zed | Run `/terminal-setup` once |
  - *Implication*: Warp users no longer need to run `/terminal-setup` for Shift+Enter (though the command still configures other keybindings).
  - *Source*: [terminal-config.md](https://code.claude.com/docs/en/terminal-config.md)

- **tmux setup consolidated**: The tmux section now presents all three required lines together with explanation.
  ```
  set -g allow-passthrough on
  set -s extended-keys on
  set -as terminal-features 'xterm*:extkeys'
  ```
  Previously `allow-passthrough` (for notifications) and `extended-keys` (for Shift+Enter) were documented in separate sections. Developers running Claude Code in tmux should confirm all three lines are present.
  - *Source*: [terminal-config.md](https://code.claude.com/docs/en/terminal-config.md)

- **Fullscreen rendering setup documented**: The `CLAUDE_CODE_NO_FLICKER` env var is now documented inline in the terminal config page (bash, PowerShell, and settings.json examples), with a clearer symptom description.
  > If the display flickers or the scroll position jumps while Claude is working, switch to fullscreen rendering mode
  - *Source*: [terminal-config.md](https://code.claude.com/docs/en/terminal-config.md)

- **Vim mode section simplified**: The detailed key list was removed from terminal-config.md and replaced with a pointer to the [Vim editor mode reference](/en/interactive-mode#vim-editor-mode). A note was added that Vim motions are not remappable via the keybindings file.
  - *Source*: [terminal-config.md](https://code.claude.com/docs/en/terminal-config.md)

---

### Hooks — `if` Field Semantics Clarified

- **`if` matches Bash subcommands, not whole commands**: The documentation now specifies that `if: "Bash(git *)"` matches against individual subcommands parsed from the Bash input, not just whether the command string starts with `git`. For compound commands like `npm test && git push`, the hook fires because `git push` matches as a subcommand.
  > For compound commands like `npm test && git push`, Claude Code evaluates each subcommand and fires the hook because `git push` matches.
  - *Implication*: Hooks using Bash `if` patterns are broader than previously understood — a `Bash(git *)` filter will also fire on chained or piped commands that include a `git` subcommand.
  - *Source*: [hooks-guide.md](https://code.claude.com/docs/en/hooks-guide.md)

- **`if` always fires on unparseable commands**: When a Bash command is too complex to parse into subcommands, hooks with an `if` field fire unconditionally rather than being skipped.
  > The hook only spawns if the tool call matches the pattern, or if a Bash command is too complex to parse.
  - *Implication*: Hooks intended as narrow filters may run on complex shell constructs. Design hooks to be safe when they receive unexpected input.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md)

- **`PermissionDenied` removed from `if`-supported events**: The `if` field is now documented as only valid on `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, and `PermissionRequest`. `PermissionDenied` was previously listed and has been removed.
  - *Implication*: Any hook using `if` on a `PermissionDenied` event was already being silently dropped; the documentation now matches this behavior.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md)

- **`if` field syntax note added**: A new paragraph clarifies that the `if` field holds exactly one permission rule with no `&&`, `||`, or list syntax. Multiple conditions require separate hook handlers.
  > The `if` field holds exactly one permission rule. There is no `&&`, `||`, or list syntax for combining rules; to apply multiple conditions, define a separate hook handler for each.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md)

- **`SessionStart` hook added to direnv example**: The direnv environment variable guide now pairs a `SessionStart` hook with `CwdChanged` so variables are loaded both when a session begins and when Claude changes directory. The command also changed from append (`>>`) to overwrite (`>`).
  > Pairing a `SessionStart` hook with a `CwdChanged` hook fixes this. `SessionStart` loads the variables for the directory you launch in, and `CwdChanged` reloads them each time Claude changes directory.
  - *Implication*: Existing direnv setups using only `CwdChanged` will miss the initial load if Claude's working directory at session start contains an `.envrc`. Add the `SessionStart` hook and switch `>>` to `>`.
  - *Source*: [hooks-guide.md](https://code.claude.com/docs/en/hooks-guide.md)

---

### Interactive Mode — Minor Updates

- **Vim mode gains `u` (undo)**: The Vim editor mode key table now includes `u` for undo in NORMAL mode.
  - *Source*: [interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md)

- **Warp and Apple Terminal added to native Shift+Enter list**: The multiline input table now reflects that Warp and Apple Terminal support Shift+Enter without configuration.
  > Shift+Enter works without configuration in iTerm2, WezTerm, Ghostty, Kitty, Warp, and Apple Terminal.
  - *Source*: [interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md)

- **"Terminal.app" renamed to "Apple Terminal"**: The product name throughout interactive-mode.md was updated to match Apple's current branding.
  - *Source*: [interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md)

- **iTerm2 Option key instructions made more precise**: The navigation path now includes the "General" sub-tab: Settings → Profiles → Keys → **General** → set Left/Right Option key to "Esc+".
  - *Source*: [interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md)

---

### Commands Reference — Minor Updates

- **`/terminal-setup` terminal list updated**: Description now lists VS Code, Cursor, Windsurf, Alacritty, and Zed as terminals requiring setup (Warp removed from the list).
  - *Source*: [commands.md](https://code.claude.com/docs/en/commands.md)

- **`/theme` description updated**: Changed "follows your terminal's dark or light mode" to "matches your terminal's light or dark background" — a wording shift suggesting the detection method is background luminance rather than an OS-level dark mode signal.
  - *Source*: [commands.md](https://code.claude.com/docs/en/commands.md)

---

### Environment Variables — Clarification

- **`CLAUDE_ENV_FILE` description made more precise**: The description now states the file's contents are run "in the same shell process" so exports become visible to the Bash command, replacing the vaguer "sources before each Bash command."
  > Path to a shell script whose contents Claude Code runs before each Bash command in the same shell process, so exports in the file are visible to the command.
  - *Implication*: Confirms that environment variable exports in the file propagate correctly to the tool invocation — not just to a subshell.
  - *Source*: [env-vars.md](https://code.claude.com/docs/en/env-vars.md)

## Notable Details

- The `/terminal-setup` command reference was updated to add **Cursor** and **Windsurf** alongside VS Code — these editor-embedded terminals now have first-class mention, consistent with the 2.1.116 note about scroll sensitivity improvements in those same editors.
- The direnv `>>` → `>` change (append vs. overwrite) is semantically significant: appending could cause env vars from previous directories to accumulate across `CwdChanged` events, while overwriting ensures only the current directory's vars are active.
- The `PermissionDenied` removal from `if`-supported hook events was applied consistently across both `hooks.md` (field reference table) and `hooks-guide.md` (prose explanation), indicating a deliberate correction rather than a doc drift fix.
- Apple Terminal (Terminal.app) receiving first-class mention for native Shift+Enter support and the `/terminal-setup` first-run prompt story suggests improved onboarding coverage for macOS users who have not installed a third-party terminal emulator.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| terminal-config.md | Modified | +106/-65 | Full page restructure: symptom-based guide replacing feature-list format; tmux setup consolidated; Warp/Apple Terminal added to native Shift+Enter list |
| changelog.md | Modified | +27/-0 | Version 2.1.116 entry added (April 20, 2026) |
| hooks-guide.md | Modified | +18/-6 | `if` field subcommand semantics; `SessionStart` added to direnv example; `>>` → `>` for env file writes |
| hooks.md | Modified | +12/-10 | `if` field table updated; `PermissionDenied` removed; new paragraph on `if` syntax constraints |
| interactive-mode.md | Modified | +11/-10 | Vim mode `u` (undo) added; Warp/Apple Terminal native Shift+Enter; terminal name and nav path fixes |
| commands.md | Modified | +2/-2 | `/terminal-setup` terminal list updated; `/theme` description wording refined |
| env-vars.md | Modified | +1/-1 | `CLAUDE_ENV_FILE` description clarifies same-shell-process execution |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-21*
