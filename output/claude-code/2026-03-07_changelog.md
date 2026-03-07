# Claude Code Documentation Changes — 2026-03-07

## Summary

This update introduces session-scoped scheduled tasks as a new Claude Code feature. A new `scheduled-tasks.md` page provides full documentation for the `/loop` skill and underlying cron tools (`CronCreate`, `CronList`, `CronDelete`). Supporting entries were added to `settings.md` (new `CLAUDE_CODE_DISABLE_CRON` flag) and `skills.md` (`/loop` added to bundled skills list). Changes to `overview.md` and `changelog.md` are cosmetic or statistical.

---

## Significant Changes

### Features

- **Session-scoped scheduled tasks via `/loop`**: A new page documents the ability to run prompts automatically on a recurring interval or as a one-time reminder within an active Claude Code session.
  > "Scheduled tasks let Claude re-run a prompt automatically on an interval. Use them to poll a deployment, babysit a PR, check back on a long-running build, or remind yourself to do something later in the session."
  - *Implication*: Developers can automate repetitive monitoring tasks (e.g., watching a CI build, polling a deployment) directly within a Claude Code session without external tooling.
  - *Source*: [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks.md)

- **`/loop` bundled skill**: The `/loop` command accepts an optional interval and a prompt, then schedules a recurring background cron job.
  > "`/loop 5m check if the deployment finished and tell me what happened`"

  Supported interval forms:

  | Form | Example | Parsed interval |
  |:---|:---|:---|
  | Leading token | `/loop 30m check the build` | every 30 minutes |
  | Trailing `every` clause | `/loop check the build every 2 hours` | every 2 hours |
  | No interval | `/loop check the build` | defaults to every 10 minutes |

  Supported units: `s`, `m`, `h`, `d`. Seconds are rounded up to the nearest minute (cron granularity). `/loop` can wrap other skills — e.g., `/loop 20m /review-pr 1234` — firing the inner skill on each interval.
  - *Source*: [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks.md), [Skills](https://code.claude.com/docs/en/skills.md)

- **Underlying cron tools**: Three tools back the scheduling system, accessible directly or via natural-language requests to Claude:

  | Tool | Purpose |
  |:---|:---|
  | `CronCreate` | Schedule a task with a 5-field cron expression, a prompt, and a recurrence flag |
  | `CronList` | List all active tasks with their IDs, schedules, and prompts |
  | `CronDelete` | Cancel a task by its 8-character ID |

  A session can hold up to 50 scheduled tasks. Recurring tasks auto-expire after 3 days.
  - *Source*: [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks.md)

- **One-time reminders**: Natural-language one-shot tasks are supported without `/loop` and delete themselves after firing.
  > "`remind me at 3pm to push the release branch`"
  > "`in 45 minutes, check whether the integration tests passed`"
  - *Source*: [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks.md)

### Configuration

- **`CLAUDE_CODE_DISABLE_CRON` environment variable**: Added to the environment variable reference table.
  > "Set to `1` to disable [scheduled tasks](/en/scheduled-tasks). The `/loop` skill and cron tools become unavailable and any already-scheduled tasks stop firing, including tasks that are already running mid-session"
  - *Implication*: Operators or team environments that want to prevent background scheduled prompts can disable the entire scheduler with a single flag.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

---

## New Pages

- **scheduled-tasks.md** — Full reference for session-scoped scheduled tasks: `/loop` syntax, interval parsing rules, one-time reminders, the `CronCreate`/`CronList`/`CronDelete` tool API, jitter behavior, the 3-day auto-expiry policy, a cron expression reference, the `CLAUDE_CODE_DISABLE_CRON` disable flag, and a limitations section pointing to Desktop and GitHub Actions for durable alternatives. [View](https://code.claude.com/docs/en/scheduled-tasks.md)

---

## Notable Details

- **Jitter on fire times**: The scheduler adds a small deterministic per-task offset to avoid API thundering-herd effects at wall-clock boundaries.
  > "Recurring tasks fire up to 10% of their period late, capped at 15 minutes. [...] One-shot tasks scheduled for the top or bottom of the hour fire up to 90 seconds early."
  The offset is derived from the task ID so it stays consistent. To avoid one-shot jitter, use a non-`:00`/`:30` minute (e.g., `3 9 * * *` instead of `0 9 * * *`).

- **Session-scoped limitations**: Tasks only fire while Claude Code is running and idle; there is no catch-up for missed intervals and no persistence across restarts. The docs explicitly cross-link to [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop.md#schedule-recurring-tasks) and [GitHub Actions](https://code.claude.com/docs/en/github-actions.md) for durable, unattended alternatives.

- **`overview.md` markup cleanup**: Redundant `theme={null}` attributes on code blocks were collapsed from eight repetitions to one per block. No content change — this appears to be a source-template deduplication fix.

- **`changelog.md` stat bump**: The pull request count in the GitHub activity summary changed from 265 to 280. This is a repository activity stat, not a documentation content change.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| scheduled-tasks.md | New | +129 | Full documentation for session-scoped cron scheduling, `/loop`, and cron tools |
| skills.md | Modified | +2 / -0 | Added `/loop` to the bundled skills list with description and link |
| settings.md | Modified | +1 / -0 | Added `CLAUDE_CODE_DISABLE_CRON` environment variable entry |
| overview.md | Modified | +5 / -5 | Deduplicated `theme={null}` attributes on installation code blocks (cosmetic) |
| changelog.md | Modified | +1 / -1 | Updated GitHub PR count stat from 265 to 280 |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-07*
