# Claude Code Documentation Changes — 2026-03-07

## Summary

Five documentation pages were updated in this batch. The two largest changes document new capabilities: scheduled recurring tasks in the Desktop app, and setup scripts for Claude Code on the web cloud environments. The official changelog also records version 2.1.71, a significant release covering new commands, bug fixes, and performance improvements.

## Significant Changes

### Features

#### Scheduled Recurring Tasks (Desktop)

The Desktop app now supports scheduled tasks that run Claude automatically on a recurring basis. This is a substantial new feature with its own dedicated section in the Desktop reference, covering frequency options, missed-run behavior, permission handling, and management UI.

> Scheduled tasks start a new local session automatically at a time and frequency you choose. Use them for recurring work like daily code reviews, dependency update checks, or morning briefings that pull from your calendar and inbox.

Key details:
- **Frequency options**: Manual (on-demand), Hourly, Daily, Weekdays, or Weekly via the UI. Custom intervals (e.g., every 6 hours, first of each month) can be set by asking Claude in natural language.
- **Missed-run catch-up**: On wake, Desktop checks the last seven days and fires exactly one catch-up run for the most recently missed time; older misses are discarded.
- **Permission handling**: Each task has its own permission mode. Runs stall at permission prompts in Ask mode until approved. Use **Run now** after setup to pre-approve tools via "always allow."
- **Storage on disk**: Task prompts live at `~/.claude/scheduled-tasks/<task-name>/SKILL.md` (YAML frontmatter for name/description, prompt as body). Editable directly; changes take effect on next run.
- **Worktree isolation**: Optional — toggle in the prompt input to give each run its own Git worktree.

> Tasks only run while the desktop app is running and your computer is awake. If your computer sleeps through a scheduled time, the run is skipped. To prevent idle-sleep, enable **Keep computer awake** in Settings under **Desktop app → General**.

- *Implication*: Developers can now automate recurring code review, dependency audits, or data-pull briefings without external cron jobs or CI pipelines, directly from the Desktop app.
- *Source*: [Desktop Reference](https://code.claude.com/docs/en/desktop.md)

---

#### Setup Scripts for Claude Code on the Web

Cloud environments now support a **setup script** field — a Bash script that runs before Claude Code launches on each new session. This replaces the prior workaround of using `SessionStart` hooks for cloud-only initialization.

> A setup script is a Bash script that runs when a new cloud session starts, before Claude Code launches. Use setup scripts to install dependencies, configure tools, or prepare anything the cloud environment needs that isn't in the default image.

Key details:
- Scripts run **as root on Ubuntu 24.04**; `apt install` and most language package managers work without sudo.
- Scripts run only on **new sessions** — skipped when resuming an existing session.
- A non-zero exit code **fails the session**; append `|| true` to non-critical commands.
- Configured in the **environment settings dialog** (both "Add environment" and "Edit environment" flows now expose this field).
- Network access applies: scripts that install packages require the default network access level (which allows npm, PyPI, RubyGems, crates.io, etc.).

The documentation now distinguishes setup scripts from `SessionStart` hooks with a comparison table:

| | Setup scripts | SessionStart hooks |
|---|---|---|
| Attached to | The cloud environment | Your repository |
| Configured in | Cloud environment UI | `.claude/settings.json` in your repo |
| Runs | Before Claude Code launches, on new sessions only | After Claude Code launches, on every session including resumed |
| Scope | Cloud environments only | Both local and cloud |

> Use a setup script to install things the cloud needs but your laptop already has, like a language runtime or CLI tool. Use a SessionStart hook for project setup that should run everywhere, cloud and local, like `npm install`.

- *Implication*: Teams can now install cloud-specific tooling (e.g., `gh` CLI) without modifying repo-level hooks, keeping environment-specific and project-wide setup concerns cleanly separated.
- *Source*: [Claude Code on the Web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

---

### Version Release — v2.1.71

The official changelog documents v2.1.71. Notable items:

**New commands and features:**
- **`/loop` command**: Runs a prompt or slash command on a recurring interval (e.g., `/loop 5m check the deploy`).
- **Cron scheduling tools**: For recurring prompts within a session.
- **`voice:pushToTalk` keybinding**: Voice activation key is now rebindable in `keybindings.json` (default: space). Modifier+letter combos (e.g., `meta+k`) are explicitly noted as having zero typing interference.
- **Bash auto-approval allowlist expanded**: Added `fmt`, `comm`, `cmp`, `numfmt`, `expr`, `test`, `printf`, `getconf`, `seq`, `tsort`, and `pr`.

**Bug fixes (selected):**
- Fixed stdin freeze in long-running sessions where keystrokes stop being processed.
- Fixed a 5–8 second startup freeze for users with voice mode enabled (CoreAudio initialization blocked the main thread after system wake).
- Fixed startup UI freeze when many claude.ai proxy connectors refresh an expired OAuth token simultaneously.
- Fixed forked conversations (`/fork`) sharing the same plan file, causing edits in one fork to overwrite the other.
- Fixed false-positive permission prompts for compound bash commands containing heredoc commit messages.
- Fixed plugin installations being lost when running multiple Claude Code instances.
- Fixed `/plugin marketplace add owner/repo@ref` incorrectly parsing `@` — previously only `#` worked as a ref separator.
- Fixed duplicate entries in `/permissions` Workspace tab when the same directory is added with and without a trailing slash.
- Fixed `--print` hanging forever when team agents are configured (exit loop no longer waits on long-lived `in_process_teammate` tasks).
- Fixed background agent completion notifications missing the output file path.
- Fixed Chrome extension auto-detection getting permanently stuck on "not installed" after running on a machine without local Chrome.

**Improvements:**
- `/plugin uninstall` now disables project-scoped plugins in `.claude/settings.local.json` instead of `.claude/settings.json`, so changes don't affect teammates.
- Plugin-provided MCP server deduplication: servers duplicating a manually-configured server (same command/URL) are skipped; suppressions shown in `/plugin` menu.
- `/debug` now toggles debug logging on mid-session (debug logs are no longer written by default).
- Bridge session reconnection completes within seconds after laptop wake (previously up to 10 minutes).
- Startup time improved by deferring native image processor loading to first use.
- Removed startup notification noise for unauthenticated org-registered claude.ai connectors.

- *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

## Notable Details

- **Desktop capabilities list now hyperlinked**: The bullet list of Desktop features in `desktop.md` was updated to link each capability to its section anchor. This is a usability improvement but also signals that scheduled tasks are now considered a first-class Desktop capability on par with diff review, live preview, and PR monitoring.
- **Desktop quickstart updated**: The quickstart intro sentence now includes "scheduled tasks" in its feature summary, and a new "Put Claude on a schedule" next-step suggestion was added at the end of the walkthrough.
- **Overview page**: The Desktop app tab description now mentions "schedule recurring tasks." The code block `theme` attribute changes appear to be a documentation tooling artifact (repeated `theme={null}` attributes) with no user-facing effect.
- **Dependency management guidance revised**: The web docs previously directed users to `SessionStart` hooks as the sole workaround for custom dependencies. That section now positions setup scripts as the primary path and hooks as the secondary option for cases that also need to run locally.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `en/desktop.md` | Modified | +75 / -7 | Added full "Schedule recurring tasks" section (6 subsections); updated capabilities list with anchors and scheduled tasks entry; added CLI comparison row |
| `en/claude-code-on-the-web.md` | Modified | +57 / -7 | Added "Setup scripts" and "Setup scripts vs. SessionStart hooks" sections; updated environment setup flow descriptions and best practices |
| `en/changelog.md` | Modified | +31 / -2 | Added v2.1.71 release entry; minor GitHub star/PR count updates |
| `en/desktop-quickstart.md` | Modified | +3 / -1 | Added "scheduled tasks" to intro feature list; added scheduled tasks next-step suggestion |
| `en/overview.md` | Modified | +6 / -6 | Added "schedule recurring tasks" to Desktop tab description; code block theme attribute reformatting (tooling artifact) |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-07*
