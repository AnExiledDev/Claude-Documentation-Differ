# Claude Code Documentation Changes — 2026-04-14

## Summary

The dominant change is the introduction of **Routines** — a new documentation page and product concept that supersedes "Cloud scheduled tasks." Routines expand cloud-based automation to support three trigger types: schedule, HTTP API call, and GitHub repository events. Alongside this, three new environment variables were added, and minor clarifications were made to the `/branch` command and plugin SKILL.md authoring guidance.

## Significant Changes

### Features

- **Routines replace Cloud Scheduled Tasks**: The `web-scheduled-tasks` page has been replaced by a new `routines.md` page. The underlying capability expands from schedule-only to three trigger types running on Anthropic-managed cloud infrastructure:
  - **Scheduled**: recurring cadence (hourly, daily, weekdays, weekly; custom cron via CLI with ≥1 hour minimum)
  - **API**: HTTP POST to a per-routine `/fire` endpoint with a bearer token
  - **GitHub events**: react to PR, push, issue, check run, workflow run, and other repository events

  > "A routine is a saved Claude Code configuration: a prompt, one or more repositories, and a set of connectors, packaged once and run automatically. Routines execute on Anthropic-managed cloud infrastructure, so they keep working when your laptop is closed."

  Routines are available on Pro, Max, Team, and Enterprise plans at [claude.ai/code/routines](https://claude.ai/code/routines) or via `/schedule` in the CLI.
  - *Implication*: Teams can now trigger Claude Code cloud sessions directly from CI/CD pipelines, monitoring tools, or any HTTP client — without a schedule. GitHub event triggers enable automated code review, backport automation, and alert triage as first-class features.
  - *Source*: [Routines](https://code.claude.com/docs/en/routines.md)

- **API trigger endpoint (experimental)**: The `/fire` endpoint is live under the `experimental-cc-routine-2026-04-01` beta header. Accepts an optional `text` field to append context (e.g., an alert body) to the routine's configured prompt:

  ```bash
  curl -X POST https://api.anthropic.com/v1/claude_code/routines/<trigger_id>/fire \
    -H "Authorization: Bearer sk-ant-oat01-xxxxx" \
    -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
    -H "Content-Type: application/json" \
    -d '{"text": "Sentry alert SEN-4521 fired in prod. Stack trace attached."}'
  ```

  Returns a JSON body with the new session ID and URL. Breaking changes ship behind new dated beta header versions; the two most recent previous versions remain valid during migration.
  - *Implication*: This endpoint enables alert triage automation (monitoring tool → Claude session → draft PR) and deploy-gate verification (CD pipeline → Claude smoke check → Slack go/no-go) without a standing schedule.
  - *Source*: [Routines](https://code.claude.com/docs/en/routines.md)

- **GitHub event triggers**: 18 event categories are supported (pull requests, reviews, pushes, releases, issues, discussions, check runs, workflow runs, and more). Pull request triggers accept filters on author, title, body, base/head branch, labels, draft status, merge status, and fork origin.

  > "During the research preview, GitHub webhook events are subject to per-routine and per-account hourly caps. Events beyond the limit are dropped until the window resets."

  - *Implication*: GitHub triggers require the Claude GitHub App (not just `/web-setup` CLI token sync). The App must be installed on the target repository; trigger setup prompts for this if it isn't present.
  - *Source*: [Routines](https://code.claude.com/docs/en/routines.md)

- **`/branch` command description updated**: Now explicitly documents the `/resume` return path:

  > "Create a branch of the current conversation at this point. Switches you into the branch and preserves the original, which you can return to with `/resume`. Alias: `/fork`"

  Previously the description omitted how to return to the original conversation after branching.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

### Configuration

- **`CLAUDE_CODE_SKIP_PROMPT_HISTORY`** (new env var): Skips writing prompt history and session transcripts to disk in any mode — interactive or non-interactive. Sessions started with this variable set do not appear in `--resume`, `--continue`, or up-arrow history.

  > "Useful for ephemeral scripted sessions"

  - *Implication*: Previously, suppressing transcript writes required `--no-session-persistence` (non-interactive only) or `persistSession: false` (Agent SDK only). This env var works universally across all modes. The `cleanupPeriodDays` setting docs and `claude-directory.md` have both been updated to lead with this variable as the preferred approach.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_DISABLE_VIRTUAL_SCROLL`** (new env var): Set to `1` to disable virtual scrolling in fullscreen rendering and force every transcript message to render.

  > "Use this if scrolling in fullscreen mode shows blank regions where messages should appear"

  - *Implication*: This is a targeted workaround for a visual rendering bug in fullscreen mode; it is not needed under normal use.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_MAX_CONTEXT_TOKENS`** (new env var): Overrides the context window size Claude Code assumes for the active model.

  > "Only takes effect when `DISABLE_COMPACT` is also set. Use this when routing to a model through `ANTHROPIC_BASE_URL` whose context window does not match the built-in size for its name"

  - *Implication*: Useful for LLM gateway setups where a model served under a familiar name has a different actual context size than the Claude Code built-in default for that name.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

### Plugins

- **SKILL.md `name` frontmatter field removed from authoring example**: The `plugins.md` documentation updated its SKILL.md example and description:

  > Before: "Each `SKILL.md` needs frontmatter with `name` and `description` fields"
  >
  > After: "Each `SKILL.md` contains YAML frontmatter and instructions. Include a `description` so Claude knows when to use the skill"

  The `name` field no longer appears in the example block.
  - *Implication*: The `name` field may no longer be required in SKILL.md frontmatter. New plugins should follow the updated example (description only). Existing plugins with a `name` field are likely unaffected.
  - *Source*: [Plugins](https://code.claude.com/docs/en/plugins.md)

## New Pages

- **[routines.md](https://code.claude.com/docs/en/routines.md)** — Full reference for the Routines feature: creating routines from the web, CLI (`/schedule`), and Desktop app; configuring schedule, API, and GitHub event triggers; managing runs and run history; branch permissions (default: `claude/`-prefix only); connector and environment setup; and daily usage cap details.

## Notable Details

- The `/schedule` CLI command remains the entry point for creating scheduled routines conversationally. API and GitHub event triggers must be added via the web UI at `claude.ai/code/routines` — the CLI cannot currently create or revoke API tokens.
- Routine branch permissions default to `claude/`-prefixed branches only. Enabling **Allow unrestricted branch pushes** per repository is an explicit opt-in.
- Routines are scoped to individual claude.ai accounts (not team/org shared) and draw down subscription usage plus a separate daily run cap viewable at `claude.ai/settings/usage`.
- The Desktop scheduled tasks comparison table updated its "Cloud" column header link from `/en/web-scheduled-tasks` to `/en/routines`; the table structure and content are otherwise identical.
- `common-workflows.md` now points to `claude.ai/code/routines` (previously `claude.ai/code`) in the scheduling comparison table's cloud row.
- The `desktop-scheduled-tasks.md` now mentions API and GitHub event triggers in its recommendation for when to use a remote task over a local desktop task.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| routines.md | New | +331 | Full reference for Routines: schedule, API, and GitHub event triggers on Anthropic cloud |
| desktop-scheduled-tasks.md | Modified | +14/-14 | Updated links from `web-scheduled-tasks` to `routines`; added API/GitHub trigger mention |
| scheduled-tasks.md | Modified | +14/-14 | Updated comparison table and all links from `web-scheduled-tasks` to `routines` |
| env-vars.md | Modified | +3/-0 | Added `CLAUDE_CODE_DISABLE_VIRTUAL_SCROLL`, `CLAUDE_CODE_MAX_CONTEXT_TOKENS`, `CLAUDE_CODE_SKIP_PROMPT_HISTORY` |
| platforms.md | Modified | +7/-7 | Updated scheduling row in remote-work table to link to `routines` |
| remote-control.md | Modified | +7/-7 | Updated scheduling row in remote-work table to link to `routines` |
| common-workflows.md | Modified | +6/-6 | Updated scheduling comparison table to reference Routines and new URL |
| claude-code-on-the-web.md | Modified | +2/-2 | Updated `/schedule` reference and related resources link to `routines` |
| commands.md | Modified | +2/-2 | Clarified `/branch` description (added `/resume`); updated `/schedule` link to `routines` |
| overview.md | Modified | +2/-2 | Updated cloud task references to Routines; noted API and GitHub trigger capability |
| web-quickstart.md | Modified | +2/-2 | Updated `/schedule` reference and related resources to point to `routines` |
| plugins.md | Modified | +1/-2 | Removed `name` field from SKILL.md frontmatter example; updated authoring description |
| claude-directory.md | Modified | +1/-1 | Updated transcript suppression guidance to lead with `CLAUDE_CODE_SKIP_PROMPT_HISTORY` |
| settings.md | Modified | +1/-1 | Updated `cleanupPeriodDays` to reference `CLAUDE_CODE_SKIP_PROMPT_HISTORY` for all modes |
| desktop.md | Modified | +1/-1 | Updated connector note to reference "routines" instead of "scheduled tasks" |
| github-enterprise-server.md | Modified | +1/-1 | Updated "scheduled tasks" to "routines" in remote session workflow description |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-14*
