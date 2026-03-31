# Claude Code Documentation Changes — 2026-03-31

## Summary

A new page covering GitHub Enterprise Server (GHES) support was added, along with CLI version 2.1.88 release notes. Several existing pages were updated to reflect that auto mode is now generally available on Team, Enterprise, and API plans (removing previous "rolling out shortly" language), and the web setup flow gained a terminal-based `/web-setup` command.

## Significant Changes

### GitHub Enterprise Server Support (New Page)

- **New GHES documentation**: A dedicated page explains how to connect Claude Code to self-hosted GitHub Enterprise Server instances for web sessions, code review, and plugin marketplaces.
  > "GitHub Enterprise Server (GHES) support lets your organization use Claude Code with repositories hosted on your self-managed GitHub instance instead of github.com. Once an admin connects your GHES instance, developers can run web sessions, get automated code reviews, and install plugins from internal marketplaces without any per-repository configuration."
  - *Implication*: Teams and Enterprise plan customers with self-hosted GitHub can now use Claude Code on the web and Code Review without migrating to github.com.
  - *Source*: [GitHub Enterprise Server](https://code.claude.com/docs/en/github-enterprise-server.md)

### Auto Mode Plan Availability

- **Auto mode now generally available on Enterprise and API plans**: Multiple pages previously described auto mode as available on "Team plans, with Enterprise and API support rolling out shortly." That language has been replaced with "Team, Enterprise, and API plans" throughout.
  > "Auto mode is available on Team, Enterprise, and API plans. On Team and Enterprise, an admin must enable it in Claude Code admin settings before users can turn it on."
  - *Implication*: Enterprise and API customers no longer need to wait; auto mode is live for all three plan types.
  - *Source*: [Permission Modes](https://code.claude.com/docs/en/permission-modes.md), [CLI Reference](https://code.claude.com/docs/en/cli-reference.md), [Desktop](https://code.claude.com/docs/en/desktop.md), [VS Code](https://code.claude.com/docs/en/vs-code.md)

### Auto Mode Prompt Injection Defense (Expanded Description)

- **Auto mode classifier description now includes prompt injection defense details**: The permission-modes page expanded the description of how the auto mode classifier protects against hostile content.
  > "It blocks actions that escalate beyond the task scope, target infrastructure the classifier doesn't recognize as trusted, or appear to be driven by prompt injection: hostile instructions embedded in a file, web page, or tool result that attempt to redirect Claude toward actions you never asked for. The defense is layered: a server-side probe scans incoming tool results and flags suspicious content before Claude reads it, while the classifier itself is never shown tool results, so injected instructions cannot influence its approval decisions."
  - *Implication*: The documentation now links to an [engineering deep dive](https://www.anthropic.com/engineering/claude-code-auto-mode) alongside the existing announcement post.
  - *Source*: [Permission Modes](https://code.claude.com/docs/en/permission-modes.md)

### Web Setup — Terminal Path Added

- **`/web-setup` command documented**: The "Getting started" section of Claude Code on the web now has two subsections: "From the browser" (existing flow) and "From the terminal" (new).
  > "Run `/web-setup` inside Claude Code to connect GitHub using your local `gh` CLI credentials. The command syncs your `gh auth token` to Claude Code on the web, creates a default cloud environment, and opens claude.ai/code in your browser when it finishes."
  - *Implication*: Developers already authenticated with the `gh` CLI can set up web sessions without going through the browser GitHub App flow; admins can disable this with a toggle at claude.ai/admin-settings/claude-code.
  - *Source*: [Claude Code on the Web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

### Model Configuration — Pinning the Default Model

- **Clarified that `model` setting is an initial selection, not enforcement**: The model-config page now explains that users can bypass a `model` setting by choosing "Default" in the picker, and adds `ANTHROPIC_DEFAULT_SONNET_MODEL` / `ANTHROPIC_DEFAULT_OPUS_MODEL` / `ANTHROPIC_DEFAULT_HAIKU_MODEL` env vars to the recommended control pattern.
  > "The `model` setting is an initial selection, not enforcement. It sets which model is active when a session starts, but users can still open `/model` and pick Default, which resolves to the system default for their tier regardless of what `model` is set to."
  - *Implication*: Organizations that need to pin a specific model version must also set the corresponding `ANTHROPIC_DEFAULT_*` env var, or users can silently get the latest release instead.
  - *Source*: [Model Configuration](https://code.claude.com/docs/en/model-config.md)

### Version 2.1.88 Release

- **CLI 2.1.88 changelog entry added**: The changelog page records 30+ fixes and improvements for the March 30, 2026 release. Key items include:
  - New `CLAUDE_CODE_NO_FLICKER=1` env var for flicker-free alt-screen rendering
  - New `PermissionDenied` hook that fires after auto mode classifier denials, supporting `{retry: true}`
  - Named subagents added to `@` mention typeahead suggestions
  - `showThinkingSummaries: true` setting required to restore thinking summaries (now off by default in interactive sessions)
  - Fixed prompt cache misses in long sessions from changing tool schema bytes
  - Fixed `StructuredOutput` schema cache bug causing ~50% failure rate in multi-schema workflows
  - Fixed PreToolUse/PostToolUse hooks not providing `file_path` as absolute path for Write/Edit/Read tools
  - Multiple Windows, CJK/emoji, and rendering fixes
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Scheduled Tasks — Minimum Cron Interval Clarified

- **Scheduled tasks now document a 1-hour minimum interval**: The web-scheduled-tasks page previously told users to "set a specific schedule" via `/schedule update`; it now adds that the minimum interval is 1 hour and that sub-hourly expressions (e.g., `*/30 * * * *`) are rejected.
  - *Source*: [Web Scheduled Tasks](https://code.claude.com/docs/en/web-scheduled-tasks.md)

## New Pages

- **github-enterprise-server.md** — Full admin and developer guide for connecting Claude Code to self-hosted GitHub Enterprise Server instances, including setup steps, GitHub App permissions, GHES plugin marketplace configuration, and troubleshooting. [View](https://code.claude.com/docs/en/github-enterprise-server.md)

## Notable Details

- The `claude-code-on-the-web.md` limitations section now notes that self-hosted GitHub Enterprise Server instances are supported for Teams and Enterprise plans, removing a previous implicit restriction to github.com only.
- `network-config.md` added a note that GHES instances behind a firewall must allowlist Anthropic API IP addresses for clone and review operations to work.
- `plugin-marketplaces.md` updated the `hostPattern` description to explicitly recommend this approach for GHES or self-hosted GitLab instances.
- `code-review.md` added a cross-reference to the new GHES page for repositories on self-hosted GitHub instances.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| github-enterprise-server.md | New | +188 | GHES admin setup, developer workflow, plugin marketplace config, and troubleshooting |
| changelog.md | Modified | +44/-0 | Added v2.1.88 release entry |
| claude-code-on-the-web.md | Modified | +17/-1 | Added "From the terminal" `/web-setup` section; GHES noted in limitations |
| model-config.md | Modified | +14/-6 | Clarified model setting enforcement; added env vars for pinning Default resolution |
| permission-modes.md | Modified | +4/-4 | Auto mode available on Enterprise/API (no longer "rolling out"); expanded classifier description |
| vs-code.md | Modified | +15/-15 | Updated auto mode plan requirement wording (table reformatting only) |
| desktop.md | Modified | +7/-7 | Updated auto mode plan requirement in permission modes table |
| cli-reference.md | Modified | +1/-1 | Updated `--enable-auto-mode` plan requirement |
| network-config.md | Modified | +2/-0 | Added GHES firewall allowlist note |
| code-review.md | Modified | +1/-1 | Added GHES cross-reference |
| plugin-marketplaces.md | Modified | +1/-1 | Added GHES recommendation to hostPattern description |
| web-scheduled-tasks.md | Modified | +1/-1 | Added 1-hour minimum interval and rejection of sub-hourly cron expressions |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-31*
