# Claude Code Documentation Changes — 2026-02-20

## Summary

This update introduces two major features: a `--worktree` CLI flag that automates git worktree creation for isolated parallel sessions, and a new `ConfigChange` hook event that lets scripts audit or block configuration file changes during a session. Supporting changes add `background` and `isolation` frontmatter fields for subagent definitions, a `settings.json` default-settings capability for plugins, and a new `CLAUDE_CODE_SIMPLE` environment variable for minimal-tooling mode. Several pages were updated to reflect the worktree flag and cross-reference the new hook.

---

## Significant Changes

### Features

- **New `--worktree` / `-w` CLI flag**: Starts Claude in an automatically created git worktree at `<repo>/.claude/worktrees/<name>`. The name becomes both the directory and the branch name (`worktree-<name>`). If no name is given, one is auto-generated (e.g., `bright-running-fox`). On session exit, the worktree is removed automatically if no changes were made; if changes exist, Claude prompts to keep or discard.

  > `| --worktree, -w | Start Claude in an isolated git worktree at <repo>/.claude/worktrees/<name>. If no name is given, one is auto-generated | claude -w feature-auth |`

  - *Implication*: Eliminates the multi-step manual workflow of `git worktree add` + `cd` + `claude`. Lifecycle cleanup is now managed by Claude Code itself.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **New `ConfigChange` hook event**: Fires when any configuration file (user settings, project settings, local settings, policy settings, or skill files) changes during a running session. Hooks can log changes or block them from taking effect by returning `{"decision": "block"}` or exiting with code 2. Note that `policy_settings` changes cannot be blocked — hooks fire but blocking decisions are ignored, ensuring enterprise-managed settings always apply.

  > `ConfigChange hooks fire for changes to settings files, managed policy settings, and skill files. The source field in the input tells you which type of configuration changed, and the optional file_path field provides the path to the changed file.`

  The matcher filters on `source` values: `user_settings`, `project_settings`, `local_settings`, `policy_settings`, or `skills`. The hook input includes `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`, `source`, and optionally `file_path`.

  - *Implication*: Teams can now enforce configuration governance without MDM enrollment: log who changed what and when, or prevent unauthorized settings changes from applying to an active session.
  - *Source*: [Hooks Reference](https://code.claude.com/docs/en/hooks.md)

- **New `CLAUDE_CODE_SIMPLE` environment variable**: Setting `CLAUDE_CODE_SIMPLE=1` runs Claude with a minimal system prompt and only the Bash, file read, and file edit tools. MCP tools, attachments, hooks, and CLAUDE.md files are all disabled.

  > `Set to 1 to run with a minimal system prompt and only the Bash, file read, and file edit tools. Disables MCP tools, attachments, hooks, and CLAUDE.md files`

  - *Implication*: Useful for embedding Claude in restricted scripting environments or auditing scenarios where a fully-featured session is undesirable.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **New `Ctrl+F` keyboard shortcut**: Kills all background agents. Press twice within 3 seconds to confirm.

  > `| Ctrl+F | Kill all background agents. Press twice within 3 seconds to confirm | Background agent control |`

  - *Implication*: Provides a keyboard-accessible way to terminate background agents without leaving the interactive session.
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

### Configuration

- **New subagent frontmatter fields — `background` and `isolation`**: Two new optional fields are available in subagent YAML frontmatter.

  - `background: true` — Always runs the subagent as a background task (default: `false`).
  - `isolation: worktree` — Runs the subagent in a temporary git worktree, giving it an isolated copy of the repository. The worktree is cleaned up automatically if no changes are made.

  > `| background | No | Set to true to always run this subagent as a background task. Default: false |`
  > `| isolation | No | Set to worktree to run the subagent in a temporary git worktree, giving it an isolated copy of the repository. The worktree is automatically cleaned up if the subagent makes no changes |`

  - *Implication*: Subagent definitions can now declare isolation and execution mode directly in their frontmatter, removing the need to manually orchestrate worktrees for agent tasks.
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

- **Plugin `settings.json` for shipping default configuration**: Plugins can now include a `settings.json` file at the plugin root. Currently only the `agent` key is supported, which activates a plugin-defined custom agent as the main thread. Settings from `settings.json` take priority over `settings` declared in `plugin.json`. Unknown keys are silently ignored.

  > `Setting agent activates one of the plugin's custom agents as the main thread, applying its system prompt, tool restrictions, and model. This lets a plugin change how Claude Code behaves by default when enabled.`

  The `settings.json` file is now listed in both the plugin directory structure diagram and the file locations reference table in the plugins reference page, with the note that only `agent` settings are currently supported.

  - *Implication*: Plugin authors can now deliver opinionated defaults (including switching the active agent) that activate automatically when a user enables the plugin.
  - *Source*: [Plugins](https://code.claude.com/docs/en/plugins.md), [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

- **`disableAllHooks` now documented as respecting the managed settings hierarchy**: The documentation now explicitly states that `disableAllHooks` set in user, project, or local settings cannot disable hooks configured through managed policy settings. Only `disableAllHooks` at the managed settings level can disable managed hooks.

  > `The disableAllHooks setting respects the managed settings hierarchy. If an administrator has configured hooks through managed policy settings, disableAllHooks set in user, project, or local settings cannot disable those managed hooks.`

  - *Implication*: Enterprise administrators can rely on policy-level hooks remaining active even if individual users or projects set `disableAllHooks`.
  - *Source*: [Hooks Reference](https://code.claude.com/docs/en/hooks.md)

### Hooks Guide: New "Audit configuration changes" Example

A new practical example was added to the hooks guide showing how to use `ConfigChange` to append each settings change to an audit log file using `jq`. The example hooks into all configuration sources with an empty matcher and produces a log line containing `timestamp`, `source`, and `file_path`. The guide also notes that blocking (exit code 2 or `{"decision": "block"}`) prevents the change from taking effect, and links to the full reference.

> `"command": "jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> ~/claude-config-audit.log"`

- *Source*: [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)

### Worktree Workflow Documentation Rewrite

The git worktrees section in common-workflows.md was substantially restructured. The previous step-by-step guide using raw `git worktree` commands was replaced with content that leads with the `--worktree` flag as the primary workflow. A new "Manage worktrees manually" subsection preserves the `git worktree` command examples for users who need custom worktree locations or need to check out specific existing branches.

New cleanup behavior is documented: on exit with no changes, the worktree and branch are removed automatically. With changes or commits present, Claude prompts the user to keep or remove.

A new tip was added recommending users add `.claude/worktrees/` to `.gitignore` to prevent worktree contents from appearing as untracked files in the main repository.

- *Source*: [Common Workflows](https://code.claude.com/docs/en/common-workflows.md)

### Cross-Reference Updates

- **Security page**: Added `ConfigChange` hooks as a recommended team security practice alongside OpenTelemetry monitoring.
  - *Source*: [Security](https://code.claude.com/docs/en/security.md)

- **Server-managed settings page**: Added a note directing users to `ConfigChange` hooks for detecting runtime configuration changes as a complement to MDM-based enforcement.
  - *Source*: [Server-Managed Settings](https://code.claude.com/docs/en/server-managed-settings.md)

- **Desktop comparison table**: The "Session isolation" row was updated from "manual via git worktrees" to the `--worktree` flag link.
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

- **VS Code page**: The worktrees section was updated to show `claude -w feature-auth` instead of the manual `git worktree add` + `cd` sequence.
  - *Source*: [VS Code](https://code.claude.com/docs/en/vs-code.md)

---

## Notable Details

- The hooks lifecycle diagram image CDN URL was updated (new token `xcAz1d2i2To-I_QJ` replaces `TBPmHzr19mDCuhZi`). This is a CDN asset rotation with no content change.
- `ConfigChange` was added to three tables in hooks.md: the event summary table, the matcher reference table (with `configuration source` as the filtered field), and the exit-code-2 blockability table. The blockability entry includes the parenthetical caveat `(except policy_settings)`.
- `ConfigChange` was also added to the JSON decision-pattern table alongside `UserPromptSubmit`, `PostToolUse`, etc., using the top-level `decision` pattern with `"block"` and `reason` fields.
- The `--worktree` flag entry in the CLI reference table links directly to the worktree anchor in common-workflows.md (`/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees`).
- The hooks guide's event table at the bottom of "How hooks work" now lists `ConfigChange` between `TaskCompleted` and `PreCompact`.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| cli-reference.md | Modified | +1/-0 | Added `--worktree` / `-w` flag |
| common-workflows.md | Modified | +48/-51 | Rewrote git worktrees section to lead with `--worktree` flag; added cleanup and manual management subsections |
| desktop.md | Modified | +1/-1 | Updated session isolation row to reference `--worktree` flag |
| hooks-guide.md | Modified | +28/-0 | Added "Audit configuration changes" example using new `ConfigChange` event |
| hooks.md | Modified | +107/-33 | Added full `ConfigChange` hook event documentation including input schema, decision control, matcher values, and blockability table entries |
| interactive-mode.md | Modified | +18/-17 | Added `Ctrl+F` shortcut for killing background agents |
| plugins-reference.md | Modified | +11/-9 | Added `settings.json` to plugin directory structure and file locations table |
| plugins.md | Modified | +15/-0 | Added "Ship default settings with your plugin" section documenting `settings.json` |
| security.md | Modified | +1/-0 | Added `ConfigChange` hooks to team security recommendations |
| server-managed-settings.md | Modified | +2/-0 | Added cross-reference to `ConfigChange` hooks for runtime change detection |
| settings.md | Modified | +1/-0 | Added `CLAUDE_CODE_SIMPLE` environment variable |
| sub-agents.md | Modified | +2/-0 | Added `background` and `isolation` frontmatter fields |
| vs-code.md | Modified | +3/-9 | Updated worktrees section to use `--worktree` flag instead of manual git commands |

---

*Generated from Claude Code CLI documentation changes detected on 2026-02-20*
