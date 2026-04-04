# Claude Code Documentation Changes — 2026-04-04

## Summary

Version 2.1.92 was released on April 4, 2026, adding enterprise policy controls, an interactive Bedrock setup wizard, per-model cost breakdowns, and an interactive `/release-notes` version picker, along with eleven bug fixes. The environment variables reference dropped `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS` and corrected the `CLAUDE_CODE_TMPDIR` documentation to reflect platform-specific temp path behavior.

## Significant Changes

### Features

- **`forceRemoteSettingsRefresh` policy setting**: A new managed policy option blocks CLI startup until remote managed settings are freshly fetched, exiting if the fetch fails (fail-closed behavior).
  > "when set, the CLI blocks startup until remote managed settings are freshly fetched, and exits if the fetch fails (fail-closed)"
  - *Implication*: Enterprise admins can enforce that all clients always run with up-to-date remote policy — clients cannot start with stale or cached settings.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Interactive Bedrock setup wizard**: A guided onboarding flow for AWS Bedrock is now accessible from the login screen when selecting "3rd-party platform".
  > "guides you through AWS authentication, region configuration, credential verification, and model pinning"
  - *Implication*: Users setting up Bedrock no longer need to manually configure AWS credentials and model settings; the wizard handles the full configuration flow interactively.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Per-model and cache-hit cost breakdown in `/cost`**: Subscription users now see a more detailed breakdown in the `/cost` command, including per-model and cache-hit statistics.
  - *Implication*: Easier to audit token spend across models and understand caching efficiency during a session.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/release-notes` is now an interactive version picker**: Previously a static display; now allows navigating release notes by version interactively.
  - *Implication*: Users can browse historical release notes without leaving the CLI.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Remote Control session name prefix uses hostname**: Session names now default to the machine hostname as a prefix (e.g., `myhost-graceful-unicorn`), overridable with `--remote-control-session-name-prefix`.
  - *Implication*: Easier to identify which machine a remote session belongs to when managing multiple machines.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Prompt cache expiry hint for Pro users**: When returning to a session after the prompt cache has expired, Pro users now see a footer hint showing roughly how many tokens the next turn will send uncached.
  - *Implication*: Helps users make informed decisions about continuing a session versus starting fresh to control token costs.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Performance

- **Write tool diff speed improvement (~60% faster for large files)**: Diff computation for the Write tool is significantly faster on files containing tabs, `&`, or `$` characters.
  - *Implication*: Noticeably faster feedback when Claude applies edits to large files with these common characters.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Linux sandbox `apply-seccomp` helper restored**: Ships the `apply-seccomp` helper in both npm and native builds, restoring unix-socket blocking for sandboxed commands.
  - *Implication*: Linux users on both npm-installed and native builds now have consistent sandboxing behavior.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Removed Commands

- **`/tag` command removed**: The `/tag` command has been removed with no replacement documented.
  - *Implication*: Any workflows using `/tag` will need to be updated.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/vim` command removed**: Vim mode toggle is now accessible exclusively through `/config` → Editor mode.
  > "toggle vim mode via `/config` → Editor mode"
  - *Implication*: The shortcut is gone; vim mode is still available but requires navigating the config menu.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Bug Fixes

- **tmux subagent spawning**: Subagents no longer permanently fail with "Could not determine pane count" after tmux windows are killed or renumbered during a long-running session.
- **Stop hook `ok:false` handling**: Prompt-type Stop hooks no longer incorrectly fail when the small fast model returns `ok:false`; `preventContinuation:true` semantics restored for non-Stop prompt-type hooks.
- **Tool input validation**: Fixed failures when streaming emits array/object fields as JSON-encoded strings.
- **Extended thinking whitespace text block**: Fixed an API 400 error that could occur when extended thinking produced a whitespace-only text block alongside real content.
- **Feedback survey accidental submissions**: Fixed unintended survey submissions from auto-pilot keypresses and consecutive-prompt digit collisions.
- **Fullscreen "esc to interrupt" hint**: The misleading hint no longer appears alongside "esc to clear" when a text selection exists in fullscreen mode during processing.
- **Homebrew update prompts**: Update prompts now correctly reference the cask's release channel (`claude-code` → stable, `claude-code@latest` → latest).
- **`ctrl+e` in multiline prompts**: Fixed `ctrl+e` jumping to the end of the next line when the cursor was already at the end of the current line.
- **Duplicate message when scrolling**: Fixed an issue where the same message could appear at two positions when scrolling up in fullscreen mode (affects iTerm2, Ghostty, and other terminals with DEC 2026 support).
- **Idle-return token hint**: The "/clear to save X tokens" hint now correctly shows the current context size instead of cumulative session tokens.
- **Plugin MCP servers stuck connecting**: Fixed plugin MCP servers getting stuck in "connecting" on session start when they duplicate a claude.ai connector that is unauthenticated.

### Configuration / Environment Variables

- **`CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS` removed**: This variable, which allowed fast mode when the organization status check failed due to a network error (e.g., a corporate proxy blocking the status endpoint), has been removed from the documentation.
  - *Implication*: Users who relied on this variable to work around corporate proxy issues will need to find an alternative approach.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_TMPDIR` platform behavior corrected**: The temp path suffix and default directory are now documented as platform-specific.
  > "Claude Code appends `/claude-{uid}/` (Unix) or `/claude/` (Windows) to this path. Default: `/tmp` on macOS, `os.tmpdir()` on Linux/Windows"
  - *Implication*: On Unix, the temp directory is now user-scoped (`/claude-{uid}/`) rather than shared (`/claude/`), which matters for security on multi-user systems. The previous docs incorrectly grouped Linux with macOS for the default path.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

## Notable Details

- The `CLAUDE_CODE_TMPDIR` change corrects a meaningful inaccuracy: the old docs described a single Unix/macOS default of `/tmp` with a shared `/claude/` suffix. The updated docs separate macOS (`/tmp`) from Linux (`os.tmpdir()`) and switch the Unix suffix to the user-scoped `/claude-{uid}/`. This affects multi-user Linux environments.
- The removal of `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS` with no documented replacement is notable for teams operating behind corporate proxies that block the organization status endpoint.
- Version 2.1.92 is a large release with 22 changelog bullet points — 11 of which are bug fixes — suggesting a stabilization pass following recent feature work.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +24/-0 | Added 2.1.92 release notes |
| env-vars.md | Modified | +1/-2 | Removed `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS`; corrected `CLAUDE_CODE_TMPDIR` platform details |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-04*
