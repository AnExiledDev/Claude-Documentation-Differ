# Claude Code Documentation Changes — 2026-03-26

## Summary

15 pages were modified in this update with no pages added or removed (+275/-151 lines total). The most substantial changes are: a new `TaskCreated` hook event for agent team workflows, a new PR auto-fix feature for Claude Code on the web, and a new `CLAUDE_STREAM_IDLE_TIMEOUT_MS` environment variable. Additional changes include a new `chat:newline` keybinding action, a `paths` field for skill auto-activation scoping, MCP tool description size limits, and three new Remote Control troubleshooting entries.

---

## Significant Changes

### Hooks

- **New `TaskCreated` hook event**: A new lifecycle hook fires when a task is being created via the `TaskCreate` tool in agent team workflows. Like `TaskCompleted`, it supports exit code 2 to block creation (with stderr fed back to the model as feedback) and `{"continue": false, "stopReason": "..."}` to stop the teammate entirely.

  > Runs when a task is being created via the `TaskCreate` tool. Use this to enforce naming conventions, require task descriptions, or prevent certain tasks from being created.

  The hook receives `task_id`, `task_subject`, and optionally `task_description`, `teammate_name`, and `team_name`. It supports all four hook types (`command`, `http`, `prompt`, `agent`) and does not support matchers — it fires on every occurrence.

  ```json
  {
    "hook_event_name": "TaskCreated",
    "task_id": "task-001",
    "task_subject": "Implement user authentication",
    "task_description": "Add login and signup endpoints",
    "teammate_name": "implementer",
    "team_name": "my-project"
  }
  ```

  Decision control example — block tasks whose subjects don't follow a required format:

  ```bash
  #!/bin/bash
  INPUT=$(cat)
  TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

  if [[ ! "$TASK_SUBJECT" =~ ^\[TICKET-[0-9]+\] ]]; then
    echo "Task subject must start with a ticket number, e.g. '[TICKET-123] Add feature'" >&2
    exit 2
  fi
  ```

  - *Implication*: Teams can now gate task creation with the same hook machinery used for task completion — useful for enforcing ticket-number prefixes, required descriptions, or policy checks before work begins.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md), [hooks-guide.md](https://code.claude.com/docs/en/hooks-guide.md), [agent-teams.md](https://code.claude.com/docs/en/agent-teams.md), [plugins-reference.md](https://code.claude.com/docs/en/plugins-reference.md)

- **`TaskCreated` added to decision control and matcher tables**: The matcher reference tables now include `TaskCreated` in the "no matcher support" row alongside `TeammateIdle` and `TaskCompleted`. It also appears in the "exit code or `continue: false`" decision pattern group and in the exit-code-2 effects table.

  > `TeammateIdle`, `TaskCreated`, `TaskCompleted` — Exit code 2 blocks the action with stderr feedback. JSON `{"continue": false, "stopReason": "..."}` also stops the teammate entirely.

  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md)

- **Hook lifecycle diagram updated**: The lifecycle SVG was replaced with a new version that includes `TaskCreated` inside the agentic loop alongside `TaskCompleted`. The diagram height increased from 1100px to 1155px to accommodate the new event.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md)

---

### Web Features

- **New Auto-fix pull requests feature**: Claude Code on the web can now watch a PR and automatically respond to CI failures and review comments. The Claude GitHub App subscribes to GitHub activity on the PR; when a check fails or a reviewer comments, Claude investigates and pushes a fix if one is clear.

  > Claude can watch a pull request and automatically respond to CI failures and review comments. Claude subscribes to GitHub activity on the PR, and when a check fails or a reviewer leaves a comment, Claude investigates and pushes a fix if one is clear.

  Three ways to enable auto-fix:
  - **PRs created in Claude Code on the web**: open the CI status bar and select **Auto-fix**
  - **From the mobile app**: tell Claude to auto-fix the PR
  - **Any existing PR**: paste the PR URL into a session

  Claude's response behavior is tiered by confidence level:
  - **Clear fixes**: Claude makes the change, pushes it, and explains in the session
  - **Ambiguous requests**: Claude asks before acting
  - **Duplicate or no-action events**: Claude notes the event and moves on

  > Claude may reply to review comment threads on GitHub as part of resolving them. These replies are posted using your GitHub account, so they appear under your username, but each reply is labeled as coming from Claude Code so reviewers know it was written by the agent and not by you directly.

  - *Implication*: Enables a partially automated CI/CD loop where Claude monitors and repairs PRs without manual re-engagement, while preserving human oversight for ambiguous or architectural decisions.
  - *Source*: [claude-code-on-the-web.md](https://code.claude.com/docs/en/claude-code-on-the-web.md)

---

### Environment Variables

- **New `CLAUDE_STREAM_IDLE_TIMEOUT_MS`**: Controls how long the streaming idle watchdog waits before closing a stalled connection.

  > Timeout in milliseconds before the streaming idle watchdog closes a stalled connection. Default: `90000` (90 seconds). Increase this value if long-running tools or slow networks cause premature timeout errors.

  - *Implication*: Users hitting unexpected timeout errors on slow networks or with long-running tool invocations can now tune this threshold without patching code.
  - *Source*: [env-vars.md](https://code.claude.com/docs/en/env-vars.md)

---

### Keybindings

- **New `chat:newline` action**: A new keybinding action (unbound by default) inserts a newline into the chat input without submitting the message.

  > `chat:newline` — (unbound) — Insert a newline without submitting

  - *Implication*: Users can bind this to a preferred key (e.g., `Shift+Enter`) to compose multiline messages more naturally.
  - *Source*: [keybindings.md](https://code.claude.com/docs/en/keybindings.md)

- **Chord unbinding documentation added**: New documentation explains how to unbind chord prefixes to free them for single-key use. All chords sharing a prefix must be unbound before the prefix key becomes available as a standalone binding. A note clarifies partial unbinding still enters chord-wait mode.

  ```json
  {
    "bindings": [
      {
        "context": "Chat",
        "bindings": {
          "ctrl+x ctrl+k": null,
          "ctrl+x ctrl+e": null,
          "ctrl+x": "chat:newline"
        }
      }
    ]
  }
  ```

  > If you unbind some but not all chords on a prefix, pressing the prefix still enters chord-wait mode for the remaining bindings.

  - *Source*: [keybindings.md](https://code.claude.com/docs/en/keybindings.md)

---

### Skills

- **New `paths` field for skill auto-activation scoping**: Skills now support a `paths` field with glob patterns that control when the skill is automatically activated based on the files being worked on.

  > Glob patterns that limit when this skill is activated. Accepts a comma-separated string or a YAML list. When set, Claude loads the skill automatically only when working with files matching the patterns. Uses the same format as path-specific rules.

  - *Implication*: Skills can be scoped to specific parts of a repository (e.g., `src/frontend/**` for a frontend-focused skill), avoiding unnecessary context loading when working in unrelated directories.
  - *Source*: [skills.md](https://code.claude.com/docs/en/skills.md)

---

### MCP

- **Local configuration takes precedence over claude.ai connectors**: Clarification added that when a server is configured both locally and through a claude.ai connector, the local configuration wins and the connector entry is skipped entirely.

  > If a server is configured both locally and through a claude.ai connector, the local configuration takes precedence and the connector entry is skipped.

  - *Source*: [mcp.md](https://code.claude.com/docs/en/mcp.md)

- **Tool description and server instruction size limit documented**: Claude Code truncates both tool descriptions and server instructions at 2KB each. The documentation advises keeping descriptions concise and front-loading critical details.

  > Claude Code truncates tool descriptions and server instructions at 2KB each. Keep them concise to avoid truncation, and put critical details near the start.

  - *Implication*: MCP server authors — especially those generating descriptions from OpenAPI specs — should audit description lengths and reorganize content to ensure critical information appears within the first 2KB.
  - *Source*: [mcp.md](https://code.claude.com/docs/en/mcp.md)

---

### Remote Control Troubleshooting

Three new error message entries were added to the Remote Control troubleshooting section:

- **"Remote Control requires a claude.ai subscription"**: Not authenticated with a claude.ai account. Fix: run `claude auth login` (unset `ANTHROPIC_API_KEY` first if set in the environment).
- **"Remote Control requires a full-scope login token"**: Authenticated with a long-lived token from `claude setup-token` or `CLAUDE_CODE_OAUTH_TOKEN` — these are inference-only and cannot establish Remote Control sessions. Fix: run `claude auth login` to get a full-scope session token.
- **"Unable to determine your organization for Remote Control eligibility"**: Stale or incomplete cached account information. Fix: run `claude auth login` to refresh.

  - *Implication*: These messages were presumably already surfaced in the CLI; the documentation now provides concrete resolution steps for each.
  - *Source*: [remote-control.md](https://code.claude.com/docs/en/remote-control.md)

---

### Permissions (Managed Settings)

- **New `allowedChannelPlugins` managed setting**: Administrators can now specify an allowlist of channel plugins permitted to push messages. When set, this replaces the default Anthropic allowlist. Requires `channelsEnabled: true`.

  > Allowlist of channel plugins that may push messages. Replaces the default Anthropic allowlist when set. Requires `channelsEnabled: true`. See Restrict which channel plugins can run.

  - *Source*: [permissions.md](https://code.claude.com/docs/en/permissions.md)

---

## Notable Details

- **MEMORY.md load limit now includes a size cap**: The auto memory load threshold changed from "first 200 lines" to "first 200 lines or 25KB, whichever comes first." This is documented in both `memory.md` and `how-claude-code-works.md`. Repositories with wide or dense MEMORY.md content (long lines, log-style entries) may now see fewer lines loaded at session start than before.
  - *Source*: [memory.md](https://code.claude.com/docs/en/memory.md)

- **`Ctrl+U` description clarified**: The shortcut was described as "Delete entire line" and is now "Delete from cursor to line start" with an added note: "Repeat to clear across lines in multiline input." This is a documentation correction for existing behavior.
  - *Source*: [interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md)

- **`setup.md` code block formatting cleanup**: Duplicate `theme={null}` attributes were removed from all install command blocks (e.g., `theme={null} theme={null} theme={null} theme={null}` → `theme={null}`). No content change.
  - *Source*: [setup.md](https://code.claude.com/docs/en/setup.md)

- **`ENABLE_CLAUDEAI_MCP_SERVERS` anchor link fixed**: The link in the env vars table was corrected from `#use-mcp-servers-from-claudeai` to `#use-mcp-servers-from-claude-ai`.
  - *Source*: [env-vars.md](https://code.claude.com/docs/en/env-vars.md)

- **`TaskCompleted` section moved earlier in `hooks.md`**: `TaskCompleted` was previously documented after `TeammateIdle` near the end of the hook events section. It now appears alongside the new `TaskCreated` section, grouped before `Stop`. The content itself is unchanged; only the position shifted.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| hooks.md | Modified | +135/-77 | New `TaskCreated` hook event with full input schema, decision control docs, and code examples; `TaskCompleted` section relocated earlier in reference |
| claude-code-on-the-web.md | Modified | +25/-1 | New "Auto-fix pull requests" section with behavior details and activation methods |
| keybindings.md | Modified | +33/-13 | New `chat:newline` action; chord unbinding documentation added |
| hooks-guide.md | Modified | +18/-17 | `TaskCreated` added to event table and matcher reference table |
| skills.md | Modified | +15/-14 | New `paths` field for glob-based skill auto-activation scoping |
| remote-control.md | Modified | +12/-0 | Three new troubleshooting entries for subscription, token scope, and org eligibility errors |
| permissions.md | Modified | +10/-9 | New `allowedChannelPlugins` managed setting |
| interactive-mode.md | Modified | +8/-8 | `Ctrl+U` description clarified for multiline context |
| mcp.md | Modified | +4/-0 | Local config precedence over connectors; 2KB tool description truncation limit documented |
| memory.md | Modified | +3/-3 | MEMORY.md load threshold updated to 200 lines or 25KB, whichever comes first |
| agent-teams.md | Modified | +2/-1 | `TaskCreated` hook referenced in quality gates section |
| env-vars.md | Modified | +2/-1 | New `CLAUDE_STREAM_IDLE_TIMEOUT_MS`; anchor link fix for `ENABLE_CLAUDEAI_MCP_SERVERS` |
| plugins-reference.md | Modified | +2/-1 | `TaskCreated` added to plugin hook event table |
| how-claude-code-works.md | Modified | +1/-1 | MEMORY.md load limit description updated to match new 25KB cap |
| setup.md | Modified | +5/-5 | Code block `theme` attribute deduplication (formatting only) |

---

*Generated from Claude Code CLI documentation changes detected on 2026-03-26*
