# Claude Code Documentation Changes — 2026-05-07

## Summary

Six documentation pages were updated in this batch, covering three new environment variables, a breaking semantic change to status line context-window token fields (as of v2.1.132), JetBrains IDE scroll improvements, and an expansion of Windows Terminal's native Shift+Enter support. No pages were added or removed.

## Significant Changes

### Environment Variables

- **New: `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS`**: Controls the stall timeout for background subagents. If no streaming progress event arrives within the window, the subagent is aborted and the task marked failed, surfacing any partial result to the parent.
  > Stall timeout in milliseconds for background subagents. Default `600000` (10 minutes). The timer resets on each streaming progress event; if no progress arrives within the window, the subagent is aborted and the task is marked failed, surfacing any partial result to the parent
  - *Implication*: Teams running long background subagent chains can tune this value if 10 minutes is too short or too aggressive for their workloads.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **New: `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN`**: Hard-disables fullscreen (alternate-screen) rendering and falls back to the classic main-screen renderer, regardless of any saved `tui` setting.
  > Set to `1` to disable [fullscreen rendering](/en/fullscreen) and use the classic main-screen renderer. The conversation stays in your terminal's native scrollback so `Cmd+f` and tmux copy mode work as usual. Takes precedence over `CLAUDE_CODE_NO_FLICKER` and the [`tui`](/en/settings#available-settings) setting. You can also switch with `/tui default`
  - *Implication*: Users who rely on `Cmd+f` search or tmux copy mode can force the classic renderer system-wide via an env var rather than having to remember `/tui default` each session.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **New: `CLAUDE_CODE_SESSION_ID`**: Exposes the current Claude Code session ID inside Bash and PowerShell tool subprocesses.
  > Set automatically in Bash and PowerShell tool subprocesses to the current session ID. Matches the `session_id` field passed to [hooks](/en/hooks). Updated on `/clear`. Use to correlate scripts and external tools with the Claude Code session that launched them
  - *Implication*: Scripts and external tooling invoked by Claude Code can now self-identify which session launched them, complementing the existing hooks `session_id` field.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **Updated: `CLAUDE_CODE_SCROLL_SPEED` now ignored in JetBrains terminal**: The scroll-speed multiplier has no effect inside the JetBrains IDE terminal, where Claude Code uses its own scroll handling.
  > Ignored in the JetBrains IDE terminal, where Claude Code uses its own scroll handling
  - *Implication*: JetBrains users should not attempt to tune this variable; scroll behavior is managed automatically.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

### Status Line — Breaking Semantic Change in v2.1.132

- **`total_input_tokens` / `total_output_tokens` now reflect live context window, not cumulative session totals**: As of v2.1.132, these fields report the tokens *currently in the context window* from the most recent API response. Before v2.1.132 they were running session sums that could exceed the context window size.
  > Token counts currently in the context window, from the most recent API response. Input includes cache reads and writes. Before v2.1.132 these were cumulative session totals
  - The `context_window` object description was rewritten to match:
  > **Combined totals** (`total_input_tokens`, `total_output_tokens`): tokens currently in the context window. `total_input_tokens` is the sum of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`; `total_output_tokens` is the output tokens from the most recent response. Both are `0` before the first API response.
  - *Implication*: Any status-line script or tool (e.g., [ccstatusline](https://github.com/sirmalloc/ccstatusline)) that treats `total_input_tokens` / `total_output_tokens` as cumulative session counters will produce incorrect results after upgrading past v2.1.132. Update scripts to treat these fields as point-in-time context snapshots. Use `current_usage` for per-component breakdown (cache hits vs. fresh input).
  - *Source*: [Status Line](https://code.claude.com/docs/en/statusline.md)

### JetBrains IDE Integration

- **New section: "Scroll in the JetBrains IDE terminal"**: Documents Claude Code's custom scroll handling for JetBrains and identifies known scroll-wheel bugs in version 2025.2.
  > In the JetBrains IDE terminal, Claude Code applies its own scroll handling and ignores `CLAUDE_CODE_SCROLL_SPEED`. The terminal sends scroll events at a much higher rate than other emulators, so a multiplier tuned elsewhere overshoots here.
  >
  > In 2025.2, the terminal also has scroll-wheel bugs that produce spurious arrow keys and wrong-direction events. Claude Code detects these at runtime and mitigates them automatically… For the best scroll experience, upgrade to 2025.3 or later. Claude Code shows a hint the first time you scroll if it detects the bug.
  - *Implication*: JetBrains users on 2025.2 will see automatic mitigation for spurious scroll events; upgrading to 2025.3+ is recommended for the cleanest experience.
  - *Source*: [Fullscreen Rendering](https://code.claude.com/docs/en/fullscreen.md)

### Terminal Support

- **Windows Terminal now supports native Shift+Enter**: Windows Terminal was moved from the "Not available" category to the "Works without setup" group for Shift+Enter newline insertion.

  Before:
  > Windows Terminal, gnome-terminal, JetBrains IDEs such as PyCharm and Android Studio — Not available; use Ctrl+J or `\` then Enter

  After:
  > Ghostty, Kitty, iTerm2, WezTerm, Warp, Apple Terminal, Windows Terminal — Works without setup

  - *Implication*: Windows Terminal users no longer need `Ctrl+J` or `\`+Enter workarounds for multi-line input.
  - *Source*: [Terminal Configuration](https://code.claude.com/docs/en/terminal-config.md), [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

### Extended Thinking — macOS Keyboard Shortcut

- **`Option+T` (toggle extended thinking) no longer requires Option-as-Meta configuration on macOS**: As of v2.1.132, the shortcut works natively on macOS. The requirement was also removed from the model configuration reference table.
  > As of v2.1.132 this shortcut works on macOS without configuring Option as Meta
  - *Implication*: macOS users on v2.1.132+ can use `Option+T` to toggle extended thinking without modifying iTerm2 or Apple Terminal settings. `Alt+T` was also removed from the list of shortcuts that require Option-as-Meta setup in the macOS keyboard note.
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md), [Model Configuration](https://code.claude.com/docs/en/model-config.md)

## Notable Details

- The `context_window` troubleshooting section was simplified: the warning that cumulative totals might exceed the context window size was removed, consistent with the semantic change above.
- The fullscreen page's closing paragraph was reworded: it now references unsetting `CLAUDE_CODE_NO_FLICKER` (not just `CLAUDE_CODE_NO_FLICKER`) and explicitly mentions `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` as a way to force the classic renderer independent of the saved `tui` setting.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| env-vars.md | Modified | +4 / -1 | Added `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS`, `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN`, `CLAUDE_CODE_SESSION_ID`; noted JetBrains scroll-speed exclusion |
| fullscreen.md | Modified | +7 / -1 | New section on JetBrains IDE terminal scroll; updated closing paragraph with `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN` guidance |
| statusline.md | Modified | +7 / -8 | Breaking: `total_input_tokens`/`total_output_tokens` semantics changed from cumulative to live context window as of v2.1.132 |
| terminal-config.md | Modified | +5 / -5 | Windows Terminal promoted to native Shift+Enter support |
| interactive-mode.md | Modified | +4 / -4 | Windows Terminal added to native Shift+Enter list; `Alt+T` no longer requires Option-as-Meta on macOS (v2.1.132+) |
| model-config.md | Modified | +1 / -1 | Removed Option-as-Meta requirement note for `Option+T` extended thinking toggle |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-07*
