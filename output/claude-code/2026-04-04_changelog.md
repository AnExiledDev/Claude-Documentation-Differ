# Claude Code Documentation Changes — 2026-04-04

## Summary

Two new pages were added: `ultraplan.md` (a research-preview feature for cloud-based plan drafting with browser review) and `desktop-scheduled-tasks.md` (scheduled tasks for the Desktop app extracted from the main `desktop.md` page into its own dedicated reference). The `permission-modes.md` page received the most substantive rewrite: the available modes table was restructured, a new `acceptEdits` section and a `Protected paths` section were added, and several subsections covering `plan` mode and `auto` mode internals were reorganized into collapsible accordions.

## Significant Changes

### Features

- **Ultraplan (research preview)**: A new workflow that offloads plan drafting to a Claude Code on the web session. From the CLI, run `/ultraplan <prompt>` or include the word `ultraplan` in any message. Claude generates the plan in the cloud while your terminal stays free. You then open the plan in your browser to leave inline comments, react to sections, and choose to execute on the web or send the plan back to your terminal.
  > "Ultraplan hands a planning task from your local CLI to a Claude Code on the web session running in plan mode. Claude drafts the plan in the cloud while you keep working in your terminal."
  - *Implication*: Requires a Claude Code on the web account and a GitHub repository. Starting an ultraplan session disconnects any active Remote Control session.
  - *Source*: [ultraplan.md](https://code.claude.com/docs/en/ultraplan.md)

- **`/ultraplan` slash command added**: The commands reference now lists `/ultraplan <prompt>` as a top-level slash command alongside `/upgrade`, `/usage`, and others.
  > "Draft a plan in an ultraplan session, review it in your browser, then execute remotely or send it back to your terminal"
  - *Implication*: The command is available in all CLI sessions; it opens a confirmation dialog before launching the cloud session.
  - *Source*: [commands.md](https://code.claude.com/docs/en/commands.md)

### Configuration

- **Permission modes page restructured**: `permission-modes.md` was substantially rewritten. The introductory "Available modes" table is now shown at the top of the page (before the switching instructions), and a new dedicated section `## Auto-approve file edits with acceptEdits mode` was added. Details on `plan` mode's use cases and worked examples were trimmed to a shorter description. The auto mode deep-dive subsections ("How actions are evaluated", "How auto mode handles subagents", "Cost and latency") were moved into collapsible accordions. The "Compare permission approaches" comparison table and the "Customize permissions further" section were removed.
  > "Each mode makes a different tradeoff between convenience and oversight. The table below shows what Claude can do without a permission prompt in each mode."
  - *Implication*: The new layout puts the modes table before any setup instructions, making it faster to identify the right mode at a glance.
  - *Source*: [permission-modes.md](https://code.claude.com/docs/en/permission-modes.md)

- **Protected paths now explicitly documented**: A new `## Protected paths` section in `permission-modes.md` lists every directory and file that is never auto-approved across all modes. The list was previously scattered across mode descriptions. New additions compared to the old inline list: `.claude/worktrees` is now carved out of the `.claude` protected directory, and specific protected files are enumerated for the first time (`.gitconfig`, `.gitmodules`, `.bashrc`, `.bash_profile`, `.zshrc`, `.zprofile`, `.profile`, `.ripgreprc`, `.mcp.json`, `.claude.json`).
  > "Protected files: `.gitconfig`, `.gitmodules`, `.bashrc`, `.bash_profile`, `.zshrc`, `.zprofile`, `.profile`, `.ripgreprc`, `.mcp.json`, `.claude.json`"
  - *Implication*: Shell config and dotfiles are now explicitly called out as protected, which was not stated before.
  - *Source*: [permission-modes.md](https://code.claude.com/docs/en/permission-modes.md)

- **Auto mode requirements clarified**: The auto mode section now presents its requirements as a structured list rather than prose, and explicitly states that auto mode is not available on Pro or Max plans (previously only said "Team, Enterprise, and API"). A minimum version requirement (`Claude Code v2.1.83 or later`) was added. The requirement note that `claudeCode.initialPermissionMode` cannot be set to `auto` is now documented in the VS Code section.
  > "Plan: Team, Enterprise, or API. Not available on Pro or Max."
  - *Implication*: Pro and Max users may have been unclear on auto mode availability; this is now explicit.
  - *Source*: [permission-modes.md](https://code.claude.com/docs/en/permission-modes.md)

- **VS Code `initialPermissionMode` setting no longer lists `auto`**: The extension settings table changed `initialPermissionMode` accepted values from `default`, `plan`, `acceptEdits`, `auto`, or `bypassPermissions` to `default`, `plan`, `acceptEdits`, or `bypassPermissions`. A note was added that to start in auto mode by default, `defaultMode` must be set in `settings.json` instead.
  - *Implication*: Auto mode cannot be set as the startup default through the VS Code extension setting; it must be configured in Claude Code's own settings file.
  - *Source*: [vs-code.md](https://code.claude.com/docs/en/vs-code.md)

- **`--permission-mode acceptEdits` example added to headless docs**: The non-interactive mode page now documents passing `--permission-mode acceptEdits` with `-p`, and clarifies that `dontAsk` denies anything not in `permissions.allow` rules.
  > "To set a baseline for the whole session instead of listing individual tools, pass a permission mode. `dontAsk` denies anything not in your `permissions.allow` rules, which is useful for locked-down CI runs."
  - *Implication*: Developers running scripted/CI workloads now have an explicit example for both `acceptEdits` and `dontAsk` in the headless reference.
  - *Source*: [headless.md](https://code.claude.com/docs/en/headless.md)

### Agent Teams and Sub-agents

- **Teammate subagent inheritance clarified**: The behavior when a teammate uses a subagent definition was corrected. Previously the docs said the teammate "inherits that subagent's system prompt, tools, and model." Now: the definition's body is "appended to the teammate's system prompt as additional instructions rather than replacing it." Team coordination tools (`SendMessage`, task management) are always available even when `tools` restricts other tools. The `skills` and `mcpServers` frontmatter fields do not apply when running as a teammate.
  > "The teammate honors that definition's `tools` allowlist and `model`, and the definition's body is appended to the teammate's system prompt as additional instructions rather than replacing it."
  - *Implication*: This is a behavior clarification, not a change — but it corrects a potentially misleading description of how system prompts compose.
  - *Source*: [agent-teams.md](https://code.claude.com/docs/en/agent-teams.md)

- **Teammate naming documented**: A new paragraph explains that the lead assigns each teammate a name at spawn time, and any teammate can message any other by that name. To get predictable names for later prompts, the lead must be told what to call each teammate in the spawn instruction.
  - *Implication*: Useful for workflows that reference specific teammates by name in follow-up messages.
  - *Source*: [agent-teams.md](https://code.claude.com/docs/en/agent-teams.md)

### Scheduled Tasks

- **Desktop scheduled tasks extracted to dedicated page**: All content from the `## Schedule recurring tasks` section of `desktop.md` (+96 removed lines) was moved verbatim into the new `desktop-scheduled-tasks.md` page. All cross-links across the documentation (in `overview.md`, `common-workflows.md`, `scheduled-tasks.md`, `web-scheduled-tasks.md`, `platforms.md`, `remote-control.md`, `desktop-quickstart.md`) were updated from `/en/desktop#schedule-recurring-tasks` to `/en/desktop-scheduled-tasks`.
  - *Implication*: Direct links to the old anchor (`desktop#schedule-recurring-tasks`) will no longer resolve; the canonical URL is now the standalone page.
  - *Source*: [desktop-scheduled-tasks.md](https://code.claude.com/docs/en/desktop-scheduled-tasks.md)

### Legal and Compliance

- **OAuth authentication scope expanded**: The legal-and-compliance page updated its description of OAuth authentication. The previous wording limited OAuth to "Free, Pro, and Max plans" and explicitly prohibited use with the Agent SDK. The new wording covers "Free, Pro, Max, Team, and Enterprise subscription plans" and removes the explicit Agent SDK prohibition, instead directing users to a support article about logging in.
  > "OAuth authentication is intended exclusively for purchasers of Claude Free, Pro, Max, Team, and Enterprise subscription plans and is designed to support ordinary use of Claude Code and other native Anthropic applications."
  - *Implication*: Team and Enterprise plans are now explicitly included in the OAuth scope; the blanket prohibition on Agent SDK use via OAuth was removed from this page.
  - *Source*: [legal-and-compliance.md](https://code.claude.com/docs/en/legal-and-compliance.md)

### Integrations

- **Remote Control and Ultraplan mutual exclusion documented**: The Remote Control limitations section now explicitly states that starting an ultraplan session disconnects any active Remote Control session, because both features occupy the `claude.ai/code` interface and only one can be connected at a time.
  - *Source*: [remote-control.md](https://code.claude.com/docs/en/remote-control.md)

- **Claude Code on the web cross-linked to ultraplan**: A new paragraph in the web docs references ultraplan as an option for drafting and reviewing plans in a web session.
  - *Source*: [claude-code-on-the-web.md](https://code.claude.com/docs/en/claude-code-on-the-web.md)

## New Pages

- **[desktop-scheduled-tasks.md](https://code.claude.com/docs/en/desktop-scheduled-tasks.md)** — Full reference for scheduling recurring tasks in the Claude Code Desktop app, covering task creation, frequency options, missed-run catch-up behavior, per-task permission modes, and task management. Content was split out from `desktop.md`.

- **[ultraplan.md](https://code.claude.com/docs/en/ultraplan.md)** — Documents the ultraplan research-preview feature: launching a cloud planning session from the CLI via `/ultraplan`, monitoring plan status, reviewing and commenting on the plan in the browser, and choosing to execute on the web or send the plan back to the terminal. [View](https://code.claude.com/docs/en/ultraplan.md)

## Notable Details

- The `Shift+Tab` cycle in the CLI no longer includes `auto` in the default description. Previously the docs showed the cycle as `default → acceptEdits → plan → auto`; now it is documented as `default → acceptEdits → plan`, with `auto` only appearing after `--enable-auto-mode` opt-in.
- `bypassPermissions` is now explicitly documented as requiring a restart with an enabling flag; you cannot enter it from a running session that was not started with one.
- The VS Code mode selector label "Ask permissions" was renamed to "Ask before edits" and "Auto accept edits" to "Edit automatically" in the UI label table within `permission-modes.md`.
- The `plan` mode description removed worked examples (OAuth2 migration prompt and follow-up questions) that previously appeared as illustrative text; the section is now shorter and procedural.
- `plan` mode approval dialog now includes "Refine with Ultraplan" as a fourth option alongside the existing three approve options.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| desktop-scheduled-tasks.md | New | +109 | Dedicated page for Desktop app scheduled tasks (split from desktop.md) |
| ultraplan.md | New | +83 | New research-preview feature: cloud plan drafting with browser review |
| permission-modes.md | Modified | +144/-151 | Major restructure: new modes table at top, acceptEdits section, Protected paths section, auto mode requirements list, accordions for internals |
| desktop.md | Modified | +3/-96 | Removed scheduled tasks section (moved to desktop-scheduled-tasks.md); updated links |
| agent-teams.md | Modified | +9/-1 | Clarified subagent-as-teammate system prompt behavior; added teammate naming docs |
| vs-code.md | Modified | +15/-15 | Updated `initialPermissionMode` accepted values (removed `auto`); updated auto mode requirements description |
| web-scheduled-tasks.md | Modified | +13/-13 | Updated links to desktop-scheduled-tasks.md throughout comparison tables |
| scheduled-tasks.md | Modified | +14/-14 | Updated links to desktop-scheduled-tasks.md throughout |
| remote-control.md | Modified | +9/-7 | Added ultraplan mutual-exclusion limitation; updated scheduled tasks links |
| headless.md | Modified | +6/-0 | Added `--permission-mode acceptEdits` example for non-interactive runs |
| overview.md | Modified | +12/-12 | Updated desktop scheduled tasks link; reformatted integrations table |
| common-workflows.md | Modified | +6/-6 | Updated desktop scheduled tasks link in scheduling options table |
| claude-code-on-the-web.md | Modified | +2/-0 | Added ultraplan cross-reference |
| commands.md | Modified | +1/-0 | Added `/ultraplan` to slash commands table |
| legal-and-compliance.md | Modified | +1/-1 | Expanded OAuth scope to Team/Enterprise; softened Agent SDK prohibition |
| platforms.md | Modified | +7/-7 | Updated scheduled tasks link in remote work comparison table |
| desktop-quickstart.md | Modified | +1/-1 | Updated scheduled tasks link |
| sub-agents.md | Modified | +1/-1 | Clarified subagent-as-teammate system prompt composition behavior |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-04*
