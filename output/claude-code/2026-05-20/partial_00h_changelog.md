# Claude Code Documentation Changes — 2026-05-20

## Summary

Claude Code v2.1.145 was released on May 19, 2026, adding scripting support for live agent sessions, OTEL span improvements, and numerous bug fixes. Documentation was also updated to clarify how settings file edits take effect at runtime and how bare tool deny rules differ from scoped ones — including their impact on the prompt cache.

## Significant Changes

### Release: v2.1.145 (May 19, 2026)

- **`claude agents --json`**: New flag lists live Claude sessions as JSON, designed for scripting use cases such as tmux-resurrect integration, status bars, and session pickers.
  > `Added 'claude agents --json' to list live Claude sessions as JSON for scripting (tmux-resurrect, status bars, session pickers)`
  - *Implication*: Developers can now programmatically query active agent sessions from shell scripts or external tools.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **OTEL span improvements**: `agent_id` and `parent_agent_id` attributes added to `claude_code.tool` spans, and background subagent spans now nest correctly under the dispatching Agent tool span.
  > `Added 'agent_id' and 'parent_agent_id' attributes to 'claude_code.tool' OTEL spans, and fixed trace parenting so background subagent spans nest under the dispatching Agent tool span`
  - *Implication*: Observability tooling gains proper parent–child trace structure for multi-agent sessions.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Status line JSON includes GitHub context**: The status line JSON input now includes GitHub repo and PR information when detected.
  - *Implication*: Custom status line integrations can surface PR state without additional shell queries.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Plugin discovery previews**: The `/plugin` Discover and Browse screens now show a plugin's commands, agents, skills, hooks, and MCP/LSP servers before installation.
  - *Implication*: Users can evaluate a plugin's surface area before committing to installing it.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Stop/SubagentStop hooks gain `background_tasks` and `session_crons` fields**: Hook input for Stop and SubagentStop events now includes these fields.
  - *Implication*: Hook scripts can inspect active background tasks and scheduled crons at session-end time.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Read tool partial-file fallback**: The Read tool now returns a truncated first page with a "PARTIAL view" notice instead of a hard error when a whole-file read exceeds the token limit.
  - *Implication*: Large file reads no longer abort; partial content is returned with an explicit notice rather than an error.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

**Bug fixes in v2.1.145:**
- Fixed a permission-prompt bypass where bare variable assignments to non-allowlisted environment variables in Bash commands were auto-approved
- Fixed MCP prompt slash commands showing raw server validation errors when a required argument is omitted — the error now names the missing argument and shows expected usage
- Fixed the spinner and elapsed-time display freezing until a keypress after a terminal resize or refocus
- Fixed the cross-project resume hint failing in default Windows PowerShell 5.1 — Windows now uses `;` as the command separator
- Fixed voice push-to-talk not working in the agent view's reply pane
- Fixed task lists rendering in random order when several tasks are created at once
- Fixed stale "Failed to install Anthropic marketplace" banner showing when the marketplace is already installed
- Fixed the PR badge in the footer not updating immediately after `gh pr create` and other PR-state-changing commands run in-session
- Fixed Agent Teams teammates with non-ASCII names failing every API call due to invalid header encoding
- Fixed `/review` using a deprecated `projectCards` GraphQL query that errored on repos with Classic Projects
- Fixed `claude plugin validate` not flagging `skills:` entries that point at a file instead of a directory
- Fixed an infinite loop where a skill using `context: fork` could repeatedly re-invoke itself

### Configuration

- **Settings: Live reload behavior documented**: A new "When edits take effect" section was added to the settings documentation, explaining that Claude Code watches settings files and applies most changes to the running session without a restart.
  > `Claude Code watches your settings files and reloads them when they change, so edits to most keys apply to the running session without a restart. This includes 'permissions', 'hooks', and credential helpers like 'apiKeyHelper'.`
  
  Two keys are **not** hot-reloaded and require a restart:
  - `model` — use `/model` to switch mid-session
  - `outputStyle` — part of the system prompt, rebuilt on `/clear` or restart
  - *Implication*: Developers can update permissions and hooks on-the-fly; the `ConfigChange` hook fires for each detected change.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Permissions & Prompt Caching

- **Bare tool deny rules vs. scoped deny rules — behavior clarified**: The permissions documentation now distinguishes between a bare tool name deny rule and a scoped one.
  > `A bare tool name like 'Bash' removes the tool from Claude's context entirely, so Claude never sees it. A scoped rule like 'Bash(rm *)' leaves the tool available and blocks matching calls when Claude attempts them.`
  - *Implication*: Using `Bash` (or `Bash(*)`) as a deny rule is more restrictive than `Bash(rm *)` — the tool is invisible to the model entirely, not just blocked on matching calls.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

- **Denying an entire tool invalidates the prompt cache**: A new section in the prompt-caching docs explains why bare tool deny rules bust the cache.
  > `Adding a bare tool name like 'Bash' or 'WebFetch' as a deny rule removes that tool from Claude's context entirely. Tool definitions sit in the system prompt layer, so adding or removing one of these rules mid-session invalidates the cache the same way an MCP server connecting or disconnecting does.`
  
  Scoped deny rules (`Bash(rm *)`) and all allow/ask rules do **not** affect the cache — only bare tool name removals do.
  - *Implication*: Users who add bare tool deny rules mid-session should expect a cache miss on the next turn.
  - *Source*: [Prompt Caching](https://code.claude.com/docs/en/prompt-caching.md)

## Minor Changes

- **`routines.md`**: Added a minimum CLI version requirement note — `/schedule` requires v2.1.81 or newer; older installs should run `claude update`. (+1/-0)
- **`permissions.md`**: Added a clarifying sentence that `Bash(*)` as a deny rule also removes the tool from Claude's context, consistent with the bare `Bash` form. (+3/-1)

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| changelog.md | Modified | SIGNIFICANT | +23/-2 | Added v2.1.145 release notes; removed 2 bug fix bullets from v2.1.144 |
| settings.md | Modified | SIGNIFICANT | +9/-0 | New "When edits take effect" section documenting live reload behavior |
| prompt-caching.md | Modified | SIGNIFICANT | +7/-0 | New "Denying an entire tool" section explaining cache invalidation from bare deny rules |
| permissions.md | Modified | MINOR | +3/-1 | Clarified bare vs scoped deny rule behavior |
| routines.md | Modified | MINOR | +1/-0 | Added min-version 2.1.81 note for `/schedule` |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-20*
