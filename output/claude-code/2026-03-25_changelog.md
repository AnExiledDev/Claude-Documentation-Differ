# Claude Code Documentation Changes — 2026-03-25

## Summary

The Claude Code changelog page received a single addition: the release notes for version **2.1.83** (March 25, 2026). This is a substantial release covering new policy management, hook events, security settings, a `TaskOutput` deprecation, keybinding changes, performance improvements, and an extensive list of bug fixes across core, sandbox, voice, remote control, and VS Code.

---

## Significant Changes

### New Settings & Environment Variables

- **`managed-settings.d/` drop-in directory**: A new directory sits alongside `managed-settings.json`, allowing separate teams to deploy independent policy fragments that are merged alphabetically.
  > *"letting separate teams deploy independent policy fragments that merge alphabetically"*
  - *Implication*: Enterprise deployments can now split managed policies across files without coordinating on a single monolithic JSON blob.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`sandbox.failIfUnavailable` setting**: When sandbox is enabled but cannot start, Claude Code will now exit with an error rather than silently falling back to running unsandboxed.
  > *"exit with an error when sandbox is enabled but cannot start, instead of running unsandboxed"*
  - *Implication*: Security-conscious environments can now enforce that sandbox is always active and catch misconfiguration at startup.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`disableDeepLinkRegistration` setting**: Prevents the `claude-cli://` protocol handler from being registered on the system.
  - *Implication*: Useful in locked-down enterprise environments or when multiple CLI versions coexist on the same machine.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` env var**: Strips Anthropic and cloud provider credentials from subprocess environments — applies to the Bash tool, hooks, and MCP stdio servers.
  > *"strip Anthropic and cloud provider credentials from subprocess environments (Bash tool, hooks, MCP stdio servers)"*
  - *Implication*: Reduces the credential blast radius when Claude Code spawns external processes.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK` env var**: Disables the non-streaming fallback when streaming fails.
  - *Implication*: Allows controlled environments to reject silent degraded fallback behavior explicitly.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

### New Hook Events

- **`CwdChanged` and `FileChanged` hook events**: Two new reactive hook events enable integrations such as `direnv` to respond to directory and file changes mid-session.
  > *"Added `CwdChanged` and `FileChanged` hook events for reactive environment management (e.g., direnv)"*
  - *Implication*: Hooks can now fire in response to file system and working-directory context changes, not just tool invocations.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

### Deprecations

- **`TaskOutput` tool deprecated**: Replaced by calling `Read` on a background task's output file path directly.
  > *"Deprecated `TaskOutput` tool in favor of using `Read` on the background task's output file path"*
  - *Implication*: Workflows and agents using `TaskOutput` should migrate to `Read`. The tool appears to remain functional for now but should be treated as on the removal path.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

### Keybinding Changes

- **"Stop all background agents" rebound to `Ctrl+X Ctrl+K`**: Previously `Ctrl+F`, which shadowed readline's forward-char binding.
  > *"Changed 'stop all background agents' keybinding from `Ctrl+F` to `Ctrl+X Ctrl+K` to stop shadowing readline forward-char"*
  - *Implication*: Users who relied on `Ctrl+F` for readline navigation will no longer have it intercepted while a background agent runs.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`Ctrl+X Ctrl+E` added as external editor alias**: Matches the standard readline binding for launching an editor; `Ctrl+G` continues to work.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`Ctrl+L` clears screen and forces full redraw**: Documented as a recovery path when `Cmd+K` leaves the UI partially blank. Note: `Ctrl+U` or double-Esc now clears prompt input (previously `Ctrl+L` may have handled both).
  > *"use this to recover when Cmd+K leaves the UI partially blank. Use `Ctrl+U` or double-Esc to clear prompt input."*
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`chat:killAgents` and `chat:fastMode` now rebindable**: Both actions can be remapped via `~/.claude/keybindings.json`.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

### Agent & Plugin Features

- **`initialPrompt` in agent frontmatter**: Agents can declare an `initialPrompt` that is auto-submitted as the first turn.
  - *Implication*: Agents can self-start without requiring a user-supplied opening message, enabling fully autonomous launch flows.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Plugin options (`manifest.userConfig`) exposed externally**: Plugins can prompt for configuration at enable time; values marked `sensitive: true` are stored in the macOS keychain or a protected credentials file on other platforms.
  > *"plugins can prompt for configuration at enable time, with `sensitive: true` values stored in keychain (macOS) or protected credentials file (other platforms)"*
  - *Implication*: Plugins can now manage their own secrets through a platform-native secrets store rather than requiring environment variables.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Duplicate plugin MCP server suppression**: Plugin MCP servers that duplicate an org-managed connector are now suppressed rather than running a redundant second connection.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

### UI & UX Improvements

- **Transcript search**: Press `/` in transcript mode (`Ctrl+O`) to search; use `n`/`N` to step through matches.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Pasted images get positional `[Image #N]` chip**: Images pasted into the prompt insert a labeled chip at the cursor, enabling positional references in the prompt. Claude can also reference the on-disk path of clipboard-pasted images for file operations.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Interrupted prompt input auto-restored**: Interrupting a prompt before any response arrives now automatically restores the input text for editing and resubmission.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`/status` works mid-response**: `/status` no longer queues until the turn finishes — it executes while Claude is actively responding.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`AskUserQuestion` and plan-mode tools disabled under `--channels`**: These interactive tools are now suppressed when `--channels` is active, preventing them from blocking channel-driven sessions.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

### Performance & Limits

- **Non-streaming fallback limits raised**: Token cap 21k → 64k; timeout 120s → 300s (local). Reduces truncated or timed-out fallback responses.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`--bare -p` ~14% faster to API request**: Performance improvement for the SDK scripting pattern.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`claude -p` startup ~600ms faster** with unauthenticated HTTP/SSE MCP servers.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Bedrock SDK cold-start latency improved**: Profile fetch now overlaps with other boot work.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`MEMORY.md` index truncates at 25KB**: Added alongside the existing 200-line cap.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`WebFetch` identifies as `Claude-User`**: Allows site operators to recognize and allowlist Claude Code traffic via `robots.txt`. Peak memory for large pages is also reduced.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Scrollback resets reduced**: In long sessions, scrollback resets drop from once per turn to approximately once per 50 messages.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Linux: `XDG_DATA_HOME` respected** when registering the `claude-cli://` protocol handler.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

### VS Code Integration

- **"Not responding" spinner**: The spinner turns red with "Not responding" when the backend hasn't responded for 60 seconds.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Esc-twice / `/rewind` rewind picker**: A keyboard-navigable rewind picker is now accessible via double-Esc or the `/rewind` slash command.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Fixed session history loading**: Session history now loads correctly when reopening a session via URL or after restart.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Fixed "Fork conversation from here" and rewind actions**: Both were failing silently when the session cache went stale.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

---

## Notable Details

- **`Ctrl+B` behavior corrected**: Previously intercepted readline's backward-char at an idle prompt. It now only fires when a foreground task is actually backgroundable, restoring expected readline navigation.
- **Background subagent visibility after context compaction**: Agents were becoming invisible post-compaction, which could cause **duplicate agents to be spawned** — a particularly dangerous failure mode now fixed.
- **Sandbox piped command fix**: `rg ... | wc -l` and similar piped commands were hanging and returning `0` in sandbox mode on Linux. This affects any automation using shell pipelines inside sandboxed sessions.
- **Startup regression fix**: Claude Code was waiting ~3s for a claude.ai MCP config fetch before proceeding. This was a regression that has been resolved.
- **Voice input freeze resolved**: A 1–8 second UI freeze on startup when voice input was enabled was caused by eagerly loading the native audio module. ALSA library errors corrupting the terminal UI on Linux without audio hardware (Docker, headless, WSL1) are also fixed.
- **`caffeinate` process fix (macOS)**: The `caffeinate` process was not properly terminating when Claude Code exited, which prevented Macs from sleeping. Now fixed.
- **Remote Control improvements**: Sessions now correctly show active rather than Idle status, AI-generated session titles appear within seconds of the first message, and remote sessions no longer require re-login on transient auth errors.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `changelog.md` | Modified | +79 / -0 | Added v2.1.83 release notes (March 25, 2026) |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-25*
