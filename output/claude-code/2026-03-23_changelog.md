# Claude Code Documentation Changes — 2026-03-23

## Summary

This update introduces **Cloud Scheduled Tasks**, a new scheduling tier that runs Claude prompts on Anthropic-managed infrastructure — persisting across computer restarts and sleep. Documentation across six pages was updated to integrate this feature and clearly differentiate the three available scheduling options: cloud, desktop-local, and session-scoped `/loop`.

## Significant Changes

### Features

#### Cloud Scheduled Tasks (new)

A new scheduling mode allows tasks to run on Anthropic infrastructure rather than the user's local machine. Tasks keep running even when the computer is off.

> "A scheduled task runs a prompt on a recurring cadence using Anthropic-managed infrastructure. Tasks keep working even when your computer is off."

Key characteristics:
- **Availability**: All Claude Code on the web users — Pro, Max, Team, and Enterprise
- **Entry points**: Web UI at `claude.ai/code/scheduled`, Desktop app Schedule page (New task → New remote task), or CLI via `/schedule`
- **Repository model**: Each run clones the repo fresh from the default branch; Claude pushes to `claude/`-prefixed branches by default. Unrestricted branch pushes can be enabled per-repository
- **Environments**: Tasks use [cloud environments](https://code.claude.com/docs/en/claude-code-on-the-web.md) that configure network access, environment variables, and setup scripts
- **Connectors**: All connected MCP connectors are included by default; individual ones can be removed at task creation time
- **Run output**: Each run produces a full session in the session list, viewable and continuable like any other session

> "Scheduled tasks are available to all Claude Code on the web users, including Pro, Max, Team, and Enterprise."

- *Implication*: Teams no longer need a machine to stay on or a CI pipeline to run recurring automated work like PR reviews, dependency audits, or nightly CI failure analysis.
- *Source*: [Schedule tasks on the web](https://code.claude.com/docs/en/web-scheduled-tasks.md)

---

#### `/schedule` CLI Command (new)

A new slash command was added to create, update, list, and run cloud scheduled tasks conversationally from within any CLI session.

> `| /schedule [description] | Create, update, list, or run Cloud scheduled tasks. Claude walks you through the setup conversationally |`

Supported sub-operations include `/schedule list`, `/schedule update`, and `/schedule run`. Custom cron intervals (not available in the web UI picker) can be set via `/schedule update`.

- *Implication*: Developers can create and manage cloud scheduled tasks without leaving the CLI or navigating the web UI.
- *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

---

#### Scheduling Options Comparison Table (new, cross-page)

A standardized comparison table (rendered via a shared `scheduling-comparison.mdx` snippet) now appears on three pages: `scheduled-tasks.md`, `desktop.md`, and `web-scheduled-tasks.md`.

> | Option | Where it runs | Best for |
> | :--- | :--- | :--- |
> | Cloud scheduled tasks | Anthropic-managed infrastructure | Tasks that should run even when your computer is off |
> | Desktop scheduled tasks | Your machine, via the desktop app | Tasks that need direct access to local files, tools, or uncommitted changes |
> | GitHub Actions | Your CI pipeline | Tasks tied to repo events or cron schedules that should live alongside workflow config |
> | `/loop` | The current CLI session | Quick polling while a session is open |

- *Implication*: Makes the scheduling decision explicit for new users encountering any of the three scheduling surfaces.
- *Source*: [Common Workflows](https://code.claude.com/docs/en/common-workflows.md)

---

### Configuration & Desktop

#### Desktop Scheduled Tasks: Local vs. Remote Distinction

The Desktop scheduled tasks section was restructured to distinguish between **local tasks** (run on your machine) and **remote tasks** (run on Anthropic cloud infrastructure). Both kinds appear in the same task grid in the Desktop app.

> "The Schedule page supports two kinds of tasks:
> * **Local tasks**: run on your machine. They have direct access to your local files and tools, but the desktop app must be open and your computer awake for them to run.
> * **Remote tasks**: run on Anthropic-managed cloud infrastructure. They keep running even when your computer is off, but work against a fresh clone of your repository rather than your local checkout."

UI flow updated: the **New task** button now opens a picker — choose **New local task** or **New remote task**.

> "To create a local scheduled task, click **Schedule** in the sidebar, click **New task**, and choose **New local task**."

Existing documentation about local task behavior (worktree toggle, missed runs, keep-awake setting) was preserved and scoped explicitly to local tasks.

- *Implication*: Existing local task workflows are unchanged; the UI now surfaces remote task creation as a peer option.
- *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

---

#### Desktop: Connector Note for Remote Sessions Updated

The connector availability note in Desktop docs was updated to reflect that remote sessions configure connectors at task creation time, rather than through the `+` button during a session.

> "The **+** button is not available in remote sessions, but [scheduled tasks](/en/web-scheduled-tasks) configure connectors at task creation time."

- *Implication*: Clarifies that connector access in remote/scheduled contexts is set up upfront, not mid-session.
- *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

---

#### Session-Scoped Scheduling (`/loop`) — Updated References

The `/loop` (session-scoped) scheduled tasks page updated its "durable scheduling" fallback language to include cloud scheduled tasks as a third option alongside Desktop and GitHub Actions.

Previous wording:
> "For durable scheduling that survives restarts and runs without an active terminal session, see Desktop scheduled tasks or GitHub Actions."

Updated to:
> "For durable scheduling that survives restarts, use Cloud or Desktop scheduled tasks, or GitHub Actions."

The "Three-day expiry" section similarly now mentions cloud tasks as an alternative alongside Desktop.

- *Implication*: `/loop` documentation now correctly positions the full set of persistent scheduling alternatives.
- *Source*: [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks.md)

---

## New Pages

- **web-scheduled-tasks.md** — Full guide to cloud scheduled tasks: creation steps (web, Desktop, CLI), frequency options (Hourly/Daily/Weekdays/Weekly, custom via `/schedule update`), repository and branch permissions, connector and environment configuration, task management, and run interaction. [View](https://code.claude.com/docs/en/web-scheduled-tasks.md)

## Notable Details

- Cloud tasks run against a **fresh clone** of the repository on each run, not a local checkout. Prompts that rely on uncommitted changes or local tool state should use Desktop local tasks instead.
- Branch push restrictions on cloud tasks default to `claude/`-prefixed branches only. This is a deliberate safety boundary to prevent accidental writes to `main` or other protected branches. Per-repository override is available.
- The `/schedule` command accepts an inline description (`/schedule daily PR review at 9am`), allowing quick task creation without entering a guided conversational flow.
- Frequency presets in the web UI cover Hourly, Daily, Weekdays, and Weekly. Custom intervals (e.g., every 2 hours, first of each month) require using `/schedule update` from the CLI to set an arbitrary cron expression.
- The `overview.md` page cleaned up redundant `theme={null}` attributes on code blocks (e.g., `theme={null}` repeated 8 times per block collapsed to a single instance). No user-facing impact.
- The overview integrations table gained a new row: "Run Claude on a recurring schedule → Cloud scheduled tasks or Desktop scheduled tasks", making the feature discoverable from the top-level overview page.
- Total documentation page count increased from 67 to 68 (metadata.json updated).

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| web-scheduled-tasks.md | New | +138 | Full guide to cloud scheduled tasks |
| desktop.md | Modified | +18/-7 | Added local vs. remote task distinction; new "Compare scheduling options" subsection |
| overview.md | Modified | +24/-15 | Added scheduling accordion; added row to integrations table; cleaned up redundant theme attrs |
| common-workflows.md | Modified | +19/-0 | Added "Run Claude on a schedule" section with scheduling options comparison table |
| scheduled-tasks.md | Modified | +11/-3 | Added "Compare scheduling options" section; updated durable scheduling references to include cloud |
| claude-code-on-the-web.md | Modified | +4/-0 | Added "Schedule recurring tasks" section linking to web-scheduled-tasks |
| commands.md | Modified | +1/-0 | Added `/schedule [description]` command entry |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-23*
