# Claude Code Documentation Changes — 2026-05-27

## Summary

One page was modified: the official changelog received version **2.1.152** (May 27, 2026), adding 36 lines with no deletions. The release is substantive — it introduces new hook events, skill/command capabilities, plugin management improvements, a resilient fallback-model behavior, and a large set of bug fixes.

## Significant Changes

### Skills & Slash Commands

- **`/code-review --fix` applies findings to working tree**: The slash command now patches your working copy after a review run, surfacing reuse, simplification, and efficiency suggestions. `/simplify` has been re-wired to invoke `/code-review --fix`.
  > `/code-review --fix` now applies review findings to your working tree after the review, surfacing reuse, simplification, and efficiency suggestions; `/simplify` now invokes `/code-review --fix`
  - *Implication*: Developers using `/simplify` will now get the full code-review-and-fix pipeline rather than the prior standalone cleanup behavior; update any automation or docs that reference `/simplify` directly.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Skills can now suppress tools via `disallowed-tools` frontmatter**: Skill and slash-command frontmatter accepts a `disallowed-tools` key; listed tools are removed from the model's tool list while the skill is active.
  > Skills and slash commands can now set `disallowed-tools` in frontmatter to remove tools from the model while the skill is active
  - *Implication*: Skill authors can now enforce a restricted tool environment (e.g., read-only mode) without relying on permission rules.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/reload-skills` command added**: Triggers a re-scan of all skill directories in the current session without requiring a restart.
  > Added `/reload-skills` command to re-scan skill directories without restarting the session
  - *Implication*: Useful during plugin or skill development — no session restart needed to pick up newly added skill files.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Hooks

- **`SessionStart` hooks can trigger skill reloads**: Hooks returning `reloadSkills: true` cause Claude Code to re-scan skill directories, making skills installed by the hook available within the same session.
  > `SessionStart` hooks can now return `reloadSkills: true` to re-scan skill directories, making skills installed by the hook available in the same session
  - *Implication*: Enables dynamic skill provisioning workflows — e.g., install a plugin in a `SessionStart` hook and have its skills immediately available.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`SessionStart` hooks can set the session title**: Hooks can now write `hookSpecificOutput.sessionTitle` at startup and on resume.
  > `SessionStart` hooks can now set the session title via `hookSpecificOutput.sessionTitle` on startup and resume
  - *Implication*: Useful for enterprise/automation setups that derive meaningful session labels from project context.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **New `MessageDisplay` hook event**: Hooks can transform or suppress assistant message text at display time.
  > Added a `MessageDisplay` hook event that lets hooks transform or hide assistant message text as it is displayed
  - *Implication*: Enables use cases such as post-processing output for display pipelines, redacting sensitive content, or implementing custom rendering.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Plugins

- **`pluginSuggestionMarketplaces` managed setting**: Admins can now allowlist organization marketplaces whose plugins may appear as context-aware suggestions.
  > Added `pluginSuggestionMarketplaces` managed setting: admins can allowlist org marketplaces whose plugins may be suggested via context-aware tips
  - *Implication*: Enterprises gain control over which plugin suggestions surface to users, preventing third-party marketplace promotions in managed environments.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`claude plugin marketplace remove` gains `--scope` flag**: Accepts `--scope user|project|local`, matching the scope options already available on `marketplace add`, `install`, and `uninstall`.
  > `claude plugin marketplace remove` now accepts `--scope user|project|local` for symmetry with `marketplace add`, `install`, and `uninstall`
  - *Implication*: Enables targeted removal of marketplace registrations at the appropriate settings tier without affecting other scopes.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Model & Session Behavior

- **Fallback model used for the rest of the session on primary model failure**: When the primary model is not found, Claude Code now switches to `--fallback-model` for the remainder of the session rather than failing every subsequent request.
  > Claude Code now switches to your configured `--fallback-model` for the rest of the session when the primary model is not found, instead of failing every request
  - *Implication*: Improves resilience for users who configure a fallback model; sessions no longer brick on transient model availability issues.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Auto mode no longer requires opt-in consent**: The consent gate has been removed.
  > Auto mode no longer requires opt-in consent
  - *Implication*: New users and existing sessions will be able to use auto mode immediately without a confirmation step.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Observability

- **Session entrypoint added as an OpenTelemetry metric attribute**: Emitted as `app.entrypoint`, gated behind `OTEL_METRICS_INCLUDE_ENTRYPOINT=true`.
  > Added the session entrypoint as an OpenTelemetry metric attribute (`app.entrypoint`, opt-in via `OTEL_METRICS_INCLUDE_ENTRYPOINT=true`)
  - *Implication*: Teams collecting OTel metrics can now segment usage by how Claude Code was invoked (CLI, IDE, SDK, etc.).
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

## Minor Changes

- **Vim mode `/` key**: In NORMAL mode, `/` now opens reverse history search (like `Ctrl+R`), matching bash/zsh vi-mode behavior.
- **`/usage` includes large session files**: Files are now scanned with a streaming read, keeping memory usage flat.
- **Thinking summary UX**: Collapsed thinking summaries now stay readable for at least 3 seconds, render as markdown, and cap at 10 lines (`Ctrl+O` shows full thinking).
- **Fullscreen thinking indicator**: The "Thinking for Ns" counter now increments live and retains its value after an interrupt.
- **Workflow tool progress display simplified**: Live agent counts moved to the persistent workflow status row; inline progress display is cleaner.
- **Post-response timer**: Now shows "Waiting for N background agents/workflows to finish" and reports cumulative time when their results are processed.

## Bug Fixes (Notable)

The release resolves 16 bugs. Selected highlights:

- Fixed terminal styling degrading in very long sessions (renderer style pool now recycled).
- Fixed plugin MCP servers with identical commands but different environment variables being incorrectly deduplicated.
- Fixed `/doctor` incorrectly reporting "marketplace not found" / "plugin not found" for stale `enabledPlugins` entries.
- Fixed plugins tracking a git branch silently stopping updates after a plugin registry rebuild.
- Fixed remote MCP servers failing to connect in Claude Code Remote sessions when an egress proxy is enabled.
- Fixed `cache_creation_input_tokens` always reported as 0 when the API returns cache writes only in the nested `cache_creation` breakdown.
- Fixed sessions getting stuck when a model or login switch left stale thinking-block signatures in history (now stripped proactively with a retry safety-net).
- Fixed the PushNotification tool incorrectly reporting "Mobile push not sent (Remote Control inactive)" in SDK-hosted sessions.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| changelog.md | Modified | SIGNIFICANT | +36/-0 | Added version 2.1.152 (May 27, 2026) with new hook events, skill capabilities, plugin management updates, fallback-model resilience, and 16 bug fixes |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-27*
