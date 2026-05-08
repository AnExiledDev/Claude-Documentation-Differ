# Claude Code Documentation Changes — 2026-05-08

## Summary

Six pages were modified in this update (29 additions, 9 deletions). The most notable changes are a restructured commands page with workflow-oriented guidance, significantly expanded telemetry documentation clarifying how permission decisions are attributed across interactive and non-interactive sessions, and a new admin control for disabling routines organization-wide.

## Significant Changes

### Commands & Navigation

- **Commands page restructured with workflow-oriented sections**: The `/commands` page now opens with a new "Commands across a typical workflow" section that organizes commands by phase — first session, during a task, before shipping, between sessions, and when something is wrong — before listing the full command table. The old inline availability note has been promoted to a `<Note>` callout.

  > **First session in a repo.** Run `/init` to generate a starter `CLAUDE.md`, then `/memory` to refine it. Use `/mcp` and `/agents` to set up any servers or subagents the project needs, and `/permissions` to set the approval rules you want.
  >
  > **Before you ship.** `/diff` shows what changed, `/simplify` reviews recent files and applies quality and efficiency fixes, and `/review` or `/security-review` give a deeper read-only pass.
  >
  > **When something is wrong.** `/rewind` rolls code and conversation back to a checkpoint. `/doctor` and `/debug` diagnose install and runtime issues, and `/feedback` reports a bug with session context attached.

  - *Implication*: This section serves as a practical onboarding guide for new users and surfaces lesser-known commands like `/btw`, `/teleport`, and `/remote-control` in context.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

- **`/schedule` description clarified to mention cloud execution context**: The command description now states routines "execute on Anthropic-managed cloud infrastructure."

  > Create, update, list, or run [routines](/en/routines), which execute on Anthropic-managed cloud infrastructure. Claude walks you through the setup conversationally.

  - *Implication*: Makes explicit that routines are not run locally, which matters for security and network access considerations.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

### Monitoring & Telemetry

- **Permission decision `source` field documentation substantially expanded**: The OpenTelemetry `tool_permission_decision` event's `source` values now have precise, session-context-aware definitions distinguishing interactive CLI behavior from Agent SDK and non-interactive `-p` session behavior.

  Key changes:
  - `"config"` now explicitly includes "allow rules in the user's personal settings" and "a session-scoped grant from an earlier prompt in the same interactive CLI session" as contributing sources, with the caveat: *"The event does not indicate which of these sources matched."*
  - `"user_permanent"`: In the interactive CLI, only the initial "Yes, and don't ask again for..." choice emits this value; **subsequent calls matching the saved rule emit `"config"` instead**. In Agent SDK or non-interactive `-p` sessions, both the initial choice and later rule matches emit `"user_permanent"`.
  - `"user_temporary"`: Same split behavior — interactive CLI emits this only for the choice itself, later matches emit `"config"`; Agent SDK / `-p` sessions emit `"user_temporary"` for both the choice and later matches.

  > In the interactive CLI this is emitted only for that choice itself; later calls that match the saved rule emit `"config"` instead. In Agent SDK or non-interactive `-p` sessions, both the initial choice and later rule matches emit `"user_permanent"`.

  - *Implication*: Teams building observability pipelines around permission telemetry need to adjust their logic — the `"config"` source is now a catch-all that includes session-scoped grants and personal allow rules, not just static configuration. Counting `"user_permanent"` events to track rule creation will be accurate in interactive CLI but will overcount in Agent SDK sessions.
  - *Source*: [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage.md)

### Configuration & Administration

- **Team and Enterprise admins can now disable routines organization-wide**: A new paragraph documents a Routines admin toggle.

  > Team and Enterprise admins can disable routines for all members with the Routines toggle at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code). When disabled, existing routines stop running and members cannot create new ones.

  - *Implication*: Admins at organizations with compliance or cost concerns around automated scheduled agents now have a kill switch. Existing routines halt immediately when the toggle is flipped.
  - *Source*: [Routines](https://code.claude.com/docs/en/routines.md)

### Integrations

- **VS Code `claudeProcessWrapper` setting description clarified**: The setting now explains how the bundled binary path is passed and when to use it.

  > Executable used to launch the Claude process. The bundled binary path is passed as an argument when present. Set this to a separately installed `claude` binary if the extension build doesn't include one for your platform.

  - *Implication*: Users on platforms where the extension doesn't bundle a binary (e.g., uncommon Linux architectures) now have clear guidance on how to point the extension at a manually installed `claude` binary.
  - *Source*: [VS Code](https://code.claude.com/docs/en/vs-code.md)

## Notable Details

- **`agent-teams.md`**: The limitation "One team per session" was reworded to "One team at a time" and "starting a new one" changed to "creating a new one." This is a minor clarification — "per session" was slightly misleading since the constraint is about concurrency, not session lifetime.
- **`terminal-config.md`**: The description of tmux's `allow-passthrough` behavior was generalized from "reach iTerm2, Ghostty, or Kitty" to "reach the outer terminal." This removes the implication that only those three terminals support passthrough, making the docs accurate for any compatible terminal emulator.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| commands.md | Modified | +21 / -3 | Added "Commands across a typical workflow" and "All commands" sections; clarified `/schedule` description |
| monitoring-usage.md | Modified | +3 / -3 | Expanded `source` field definitions for `tool_permission_decision` telemetry events |
| routines.md | Modified | +2 / -0 | Added admin toggle documentation for disabling routines org-wide |
| vs-code.md | Modified | +1 / -1 | Clarified `claudeProcessWrapper` setting behavior and use case |
| agent-teams.md | Modified | +1 / -1 | Minor wording: "One team per session" → "One team at a time" |
| terminal-config.md | Modified | +1 / -1 | Generalized terminal names in tmux passthrough description |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-08*
