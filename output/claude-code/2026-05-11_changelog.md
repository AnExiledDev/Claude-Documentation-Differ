# Claude Code Documentation Changes — 2026-05-11

## Summary

This update introduces **Agent View**, a new terminal UI for dispatching and monitoring multiple background Claude Code sessions from a single screen. The feature ships as a 292-line new documentation page, five new CLI subcommands, a new `--bg` flag, two new in-session slash commands, a new environment variable, a new managed setting, and supporting cross-references across ten existing pages.

## Significant Changes

### Features

- **Agent View (`claude agents`)**: A full-screen terminal dashboard for running and managing parallel background sessions. Previously `claude agents` only listed configured subagents; it now opens an interactive TUI showing every background session's state, activity summary, and PR/CI status. Requires Claude Code v2.1.139 or later. When output is piped, the old behavior (listing subagents) is preserved.
  > Dispatch and manage many Claude Code sessions from one screen. Agent view shows what every session is doing and which ones need your input.
  - *Implication*: Developers can run independent tasks (bug fix, PR review, test investigation) concurrently and step in only when a session needs input, without managing separate terminals or reading scrollback.
  - *Source*: [Agent View](https://code.claude.com/docs/en/agent-view.md)

- **New `--bg` CLI flag**: Starts a session immediately in the background and returns the terminal to the caller, printing the session ID and a set of management commands. Can be combined with `--agent` to run a specific subagent.
  > `--bg` — Start the session as a background agent and return immediately. Prints the session ID and management commands. Combine with `--agent` to run a specific subagent.
  - *Implication*: Background sessions can be scripted from the shell without opening agent view first; useful for CI scripts and automation.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **New in-session commands `/background` (`/bg`) and `/stop`**: `/background [prompt]` detaches the current conversation to run as a background agent, freeing the terminal (an optional final instruction can be passed before detaching). `/stop` terminates the current background session while keeping the transcript and any worktree intact.
  > `/background [prompt]` — Detach the current session to run as a background agent and free this terminal. Pass a prompt to send one more instruction before detaching. Monitor the session with `claude agents`. Alias: `/bg`
  - *Implication*: An interactive session mid-conversation can be handed off to the background without starting over.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

### New CLI Subcommands for Session Management

Five new shell-level subcommands manage background sessions by their short ID:

| Command | Purpose |
|---|---|
| `claude attach <id>` | Attach to a background session in this terminal |
| `claude logs <id>` | Print recent output from a background session |
| `claude stop <id>` | Stop a session (also accepts `claude kill`) |
| `claude respawn <id>` | Restart a stopped session with its conversation intact; `--all` restarts every stopped session |
| `claude rm <id>` | Remove a session from the list |

- *Implication*: All session lifecycle operations are now scriptable from the shell without opening the TUI.
- *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

### Configuration

- **New `disableAgentView` setting and `CLAUDE_CODE_DISABLE_AGENT_VIEW` env var**: Disables `claude agents`, `--bg`, `/background`, and the on-demand supervisor process. The setting and env var are equivalent; administrators can enforce it organization-wide via managed settings. Also added to the admin setup capabilities table.
  > Set to `true` to turn off background agents and agent view: `claude agents`, `--bg`, `/background`, and the on-demand supervisor. Typically set in managed settings. Equivalent to setting `CLAUDE_CODE_DISABLE_AGENT_VIEW` to `1`.
  - *Implication*: Orgs that want to restrict parallel background execution have a single control that covers all entry points (TUI, flag, and in-session command).
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md), [Environment Variables](https://code.claude.com/docs/en/env-vars.md), [Admin Setup](https://code.claude.com/docs/en/admin-setup.md)

### Terminology Clarifications

- **`Ctrl+X Ctrl+K` scope tightened**: The keyboard shortcut description was changed from "Kill all background agents" to "Kill all running background subagents **in this session**." The same update was applied to the `chat:killAgents` entry in the keybindings reference.
  - *Implication*: Clarifies that this shortcut affects subagents spawned within the current session — not background sessions managed by the supervisor (those are stopped via `claude stop <id>` or `/stop`).
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md), [Keybindings](https://code.claude.com/docs/en/keybindings.md)

- **Subagent vs. background agent distinction formalized**: The note in the sub-agents page was rewritten to distinguish three parallelism models clearly:
  > Subagents work within a single session. To run many independent sessions in parallel and monitor them from one place, see background agents. For sessions that communicate with each other, see agent teams.
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

- **`claude agents` pipe behavior documented**: Piping the output of `claude agents` (e.g. `claude agents | cat`) produces the old listing behavior — subagents grouped by source. Without piping, agent view opens interactively.
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

### Glossary

- **New "Turn" entry**: Defines a turn as one complete Claude response within a session — starting when the user sends a message, ending when Claude finishes responding (including any tool calls in between). Notes that stop hooks fire at the end of each turn.
  > One complete response from Claude within a session. A turn begins when you send a message and ends when Claude finishes responding, with any number of tool calls in between. Stop hooks fire at the end of each turn.
  - *Source*: [Glossary](https://code.claude.com/docs/en/glossary.md)

## New Pages

- **[agent-view.md](https://code.claude.com/docs/en/agent-view.md)** — Full reference for Agent View: quick start walkthrough, session state icons (animated/yellow/dimmed/green/red/grey), peek and reply panel, keyboard shortcuts, dispatching from agent view/shell/inside a session, worktree isolation for parallel file edits, supervisor process internals with file paths, shell management commands, troubleshooting, and known limitations. 292 lines.

## Notable Details

- **Supervisor process model**: Background sessions are hosted by a per-user supervisor process, separate from any terminal. It auto-starts on first background session or `claude agents` open. It watches the Claude Code binary on disk and restarts into new versions automatically after auto-update. Session state persists at `~/.claude/jobs/<id>/state.json`; the supervisor log is at `~/.claude/daemon.log`.
- **Worktree auto-isolation for dispatched sessions**: Sessions dispatched from agent view are blocked from writing files until they move into an isolated git worktree under `.claude/worktrees/`. Deleting a session deletes its worktree — the docs warn to merge or push changes before deleting.
- **Row summaries use Haiku-class model**: Each row in agent view shows a one-line summary generated by a Haiku-class model call, billed under normal data usage terms.
- **`←` arrow becomes universal navigation**: Once agent view has been used, pressing `←` on an empty prompt from *any* Claude Code session opens agent view with the current session pre-selected — not only from sessions attached via agent view.
- **`/batch` wording updated**: "background agent" changed to "background subagent" in the `/batch` skill description, consistent with the new terminology split between subagents (in-session) and background agents (supervisor-managed).
- **Cross-references added across docs**: The overview page's agent teams accordion, the common-workflows parallel worktrees section, and the sub-agents note block all gained links to the new agent view page.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| agent-view.md | New | +292 | Full Agent View feature documentation |
| interactive-mode.md | Modified | +19/-19 | Keyboard shortcut table reformatted; `Ctrl+X Ctrl+K` scoped to in-session subagents |
| cli-reference.md | Modified | +7/-1 | Added `attach`, `logs`, `stop`, `respawn`, `rm` subcommands; `--bg` flag; updated `agents` description |
| commands.md | Modified | +3/-1 | Added `/background` and `/stop` commands; updated `/batch` to say "subagent" |
| glossary.md | Modified | +6/-0 | Added "Turn" definition |
| sub-agents.md | Modified | +2/-2 | Clarified subagent vs. background agent vs. agent team; updated `claude agents` pipe note |
| settings.md | Modified | +1/-0 | Added `disableAgentView` setting |
| env-vars.md | Modified | +1/-0 | Added `CLAUDE_CODE_DISABLE_AGENT_VIEW` variable |
| admin-setup.md | Modified | +1/-0 | Added `disableAgentView` to managed settings table |
| common-workflows.md | Modified | +1/-1 | Added cross-reference to background agents from parallel worktrees section |
| overview.md | Modified | +1/-1 | Added background agents mention in agent teams accordion |
| keybindings.md | Modified | +1/-1 | Updated `chat:killAgents` description to clarify in-session scope |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-11*
