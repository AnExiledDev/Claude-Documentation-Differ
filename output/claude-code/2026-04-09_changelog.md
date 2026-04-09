# Claude Code Documentation Changes — 2026-04-09

## Summary

14 pages were modified across permission modes, MCP output limits, fullscreen navigation, status line configuration, and observability. The most substantive changes are an expansion of `acceptEdits` mode to include common filesystem commands, a revised model for per-tool MCP output size limits that decouples `anthropic/maxResultSizeChars` from `MAX_MCP_OUTPUT_TOKENS`, and new status line features including a timer-based `refreshInterval` and a new `workspace.git_worktree` data field.

## Significant Changes

### Permission Modes

- **`acceptEdits` mode now auto-approves common filesystem commands**: In addition to file edits, `acceptEdits` mode automatically approves `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, and `sed` when they operate on paths inside the working directory or `additionalDirectories`.
  > `acceptEdits` mode lets Claude create and edit files in your working directory without prompting. In addition to file edits, `acceptEdits` mode auto-approves common filesystem Bash commands: `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, and `sed`. Like file edits, these are auto-approved only for paths inside your working directory or `additionalDirectories`. Paths outside that scope, writes to protected paths, and all other Bash commands still prompt.
  - *Implication*: Scripts and CI jobs using `acceptEdits` will require fewer permission prompts for routine file-system scaffolding without widening the permission surface to arbitrary shell commands.
  - *Source*: [Permission Modes](https://code.claude.com/docs/en/permission-modes.md)

- **Auto mode trusts sandbox network access requests**: "Sandbox network access requests" was added to auto mode's list of pre-trusted action categories.
  - *Implication*: Sandboxed network calls no longer trigger prompts when running in auto mode.
  - *Source*: [Permission Modes](https://code.claude.com/docs/en/permission-modes.md)

### MCP Output Limits

- **`anthropic/maxResultSizeChars` now applies independently of `MAX_MCP_OUTPUT_TOKENS` for text content**: The relationship between the per-tool annotation and the global environment variable has been fundamentally revised. Previously the annotation raised a persist threshold but did not bypass the global token limit, requiring users to also raise `MAX_MCP_OUTPUT_TOKENS`. Now the annotation applies independently for text content; image content from annotated tools remains subject to the token limit.
  > The annotation applies independently of `MAX_MCP_OUTPUT_TOKENS` for text content, so users don't need to raise the environment variable for tools that declare it. Tools that return image data are still subject to the token limit.
  - *Implication*: MCP server authors can set `_meta["anthropic/maxResultSizeChars"]` to allow large text results without requiring end-users to adjust any environment variable. The example value in the docs was reduced from 500,000 to 200,000 characters.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

- **Section renamed: "Override result size per tool" → "Raise the limit for a specific tool"**: The heading was updated to better reflect that the annotation raises a ceiling rather than overriding a shared limit.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

- **`MAX_MCP_OUTPUT_TOKENS` env-var description updated**: The entry now links to the `anthropic/maxResultSizeChars` section and clarifies that text content from annotated tools uses the character limit, while image content still uses the token limit.
  > Tools that declare [`anthropic/maxResultSizeChars`](/en/mcp#raise-the-limit-for-a-specific-tool) use that character limit for text content instead, but image content from those tools is still subject to this variable (default: 25000)
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

### Fullscreen Navigation

- **`Ctrl+O` now cycles through three states instead of toggling transcript mode**: Previously `Ctrl+O` toggled between the normal prompt and transcript mode. It now cycles through three states: normal prompt → transcript mode → focus view (last prompt + one-line tool summary with edit diffstats + final response) → back to normal prompt. `Esc` or `q` exit transcript mode directly back to the prompt; `Ctrl+O` no longer serves as the exit key.
  > In fullscreen rendering, `Ctrl+O` cycles through three states: normal prompt, transcript mode, and focus view. Press it once to enter transcript mode, press it again to return to a focus view showing just your last prompt, a one-line summary of tool calls with edit diffstats, and the final response. Press it a third time to return to the normal prompt screen.
  - *Implication*: The new focus view provides a compact summary of the last turn without scrolling the full transcript — useful for quickly reviewing what Claude just did.
  - *Source*: [Fullscreen](https://code.claude.com/docs/en/fullscreen.md)

- **`Ctrl+O` description updated in keyboard shortcuts table**: The description changed from "Toggle verbose output" to "Toggle transcript viewer" and was expanded to describe the three-state cycle in fullscreen rendering.
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

### Status Line

- **New `refreshInterval` field for status line configuration**: An optional `refreshInterval` field (minimum: `1` second) re-runs the status line command on a fixed timer in addition to event-driven updates.
  > The optional `refreshInterval` field re-runs your command every N seconds in addition to the event-driven updates. The minimum is `1`. Set this when your status line shows time-based data such as a clock, or when background subagents change git state while the main session is idle. Leave it unset to run only on events.
  - *Implication*: Status lines displaying clocks, external metrics, or git state updated by background subagents can now stay current without requiring user interaction to trigger a refresh.
  - *Source*: [Status Line](https://code.claude.com/docs/en/statusline.md)

- **New `workspace.git_worktree` field in status line JSON data**: Status line scripts now receive a `workspace.git_worktree` field containing the git worktree name when the current directory is inside a linked worktree created with `git worktree add`. This is distinct from `worktree.*` fields, which only appear during `--worktree` sessions.
  > `workspace.git_worktree`: Git worktree name when the current directory is inside a linked worktree created with `git worktree add`. Absent in the main working tree. Populated for any git worktree, unlike `worktree.*` which applies only to `--worktree` sessions.
  - *Implication*: Status line scripts can now display worktree context for ordinary `git worktree add` workflows, not just Claude-managed `--worktree` sessions.
  - *Source*: [Status Line](https://code.claude.com/docs/en/statusline.md)

### Observability / Telemetry

- **`TRACEPARENT` propagated to Bash subprocesses when tracing is active**: Bash subprocesses now automatically inherit a `TRACEPARENT` environment variable containing the W3C trace context of the active tool execution span.
  > When tracing is active, Bash subprocesses automatically inherit a `TRACEPARENT` environment variable containing the W3C trace context of the active tool execution span. This lets any subprocess that reads `TRACEPARENT` parent its own spans under the same trace, enabling end-to-end distributed tracing through scripts and commands that Claude runs.
  - *Implication*: Custom scripts executed by Claude Code can participate in distributed traces without additional configuration, making it straightforward to correlate Claude-initiated shell activity in observability platforms.
  - *Source*: [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage.md)

### Settings / Sandbox

- **New `network.allowMachLookup` sandbox setting (macOS)**: A new sandbox network option allows specifying additional XPC/Mach service names the sandbox may look up, with support for a single trailing `*` for prefix matching.
  > `network.allowMachLookup`: Additional XPC/Mach service names the sandbox may look up (macOS only). Supports a single trailing `*` for prefix matching. Needed for tools that communicate via XPC such as the iOS Simulator or Playwright.
  - *Implication*: macOS users running Claude Code with sandboxing enabled can now unblock tools like iOS Simulator or Playwright that communicate via XPC without disabling the sandbox entirely.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Desktop / Platform

- **Windows ARM64 "remote sessions only" restriction removed**: The download entry for Windows ARM64 previously carried the caveat "(remote sessions only)". That restriction has been dropped, indicating full local session support on Windows ARM64.
  - *Source*: [Overview](https://code.claude.com/docs/en/overview.md)

## Notable Details

- The `acceptEdits` expansion is consistently applied across six pages — `desktop.md`, `headless.md`, `how-claude-code-works.md`, `permission-modes.md`, `permissions.md`, and `sub-agents.md` — indicating a coordinated documentation update rather than a new behavior description added in isolation.
- The MCP example value for `anthropic/maxResultSizeChars` in `mcp.md` was reduced from `500000` to `200000` characters. The hard ceiling of 500,000 characters is still stated in prose; the change likely reflects an updated recommended practice value.
- The `refreshInterval` documentation note explicitly references background subagents: "while a coordinator waits on background subagents." This positions the feature as particularly relevant for multi-agent workflows where the main session may be idle for extended periods.
- The image data carve-out for `anthropic/maxResultSizeChars` is now stated in three places: the `mcp.md` annotation description, the warning block, and the `env-vars.md` table — emphasizing it as a key behavioral boundary developers and MCP server authors should be aware of.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| statusline.md | Modified | +38/-31 | New `refreshInterval` field; new `workspace.git_worktree` data field; JSON schema example updated |
| interactive-mode.md | Modified | +19/-19 | Updated `Ctrl+O` description to "Toggle transcript viewer"; added fullscreen cycle behavior detail |
| permission-modes.md | Modified | +12/-9 | `acceptEdits` expanded to include filesystem commands; auto mode trusts sandbox network |
| fullscreen.md | Modified | +11/-8 | `Ctrl+O` three-state cycle documented; keybinding table updated; exit key clarified |
| permissions.md | Modified | +8/-8 | `acceptEdits` description updated to reflect filesystem command auto-approval |
| mcp.md | Modified | +7/-6 | Section renamed; `anthropic/maxResultSizeChars` now independent of token limit for text; example value lowered |
| overview.md | Modified | +6/-6 | Windows ARM64 caveat removed; `theme={null}` attribute duplication (metadata noise only) |
| monitoring-usage.md | Modified | +2/-0 | `TRACEPARENT` propagation to Bash subprocesses documented |
| settings.md | Modified | +1/-0 | New `network.allowMachLookup` sandbox setting added |
| desktop.md | Modified | +1/-1 | `acceptEdits` description updated |
| env-vars.md | Modified | +1/-1 | `MAX_MCP_OUTPUT_TOKENS` description updated with per-tool annotation behavior |
| headless.md | Modified | +1/-1 | `acceptEdits` description updated |
| how-claude-code-works.md | Modified | +1/-1 | `acceptEdits` description updated |
| sub-agents.md | Modified | +1/-1 | `acceptEdits` description updated |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-09*
