# Claude Code Documentation Changes — 2026-02-21

## Summary

Eight documentation pages were updated in this batch. The most significant changes introduce two new hook events — `WorktreeCreate` and `WorktreeRemove` — that allow custom worktree lifecycle logic for non-git version control systems. Supporting changes document subagent worktree isolation, a new `claude agents` CLI command, a new `CLAUDE_CODE_DISABLE_1M_CONTEXT` environment variable, and clarifications to hook type support and model configuration.

## Significant Changes

### Hooks

- **New `WorktreeCreate` hook event**: A new hook event fires when a worktree is created via `--worktree` or `isolation: "worktree"`. When configured, it replaces the default git worktree behavior entirely, enabling support for non-git version control systems.
  > "When you run `claude --worktree` or a subagent uses `isolation: "worktree"`, Claude Code creates an isolated working copy using `git worktree`. If you configure a WorktreeCreate hook, it replaces the default git behavior, letting you use a different version control system like SVN, Perforce, or Mercurial."
  > "The hook must print the absolute path to the created worktree directory on stdout. Claude Code uses this path as the working directory for the isolated session."
  - *Implication*: Teams using SVN, Perforce, Mercurial, or other non-git VCS can now use worktree isolation. Any non-zero exit code fails worktree creation. Only `type: "command"` hooks are supported.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **New `WorktreeRemove` hook event**: A cleanup counterpart to `WorktreeCreate`. Fires when a worktree is removed — either at session exit or when a subagent with `isolation: "worktree"` finishes.
  > "For git-based worktrees, Claude handles cleanup automatically with `git worktree remove`. If you configured a WorktreeCreate hook for a non-git version control system, pair it with a WorktreeRemove hook to handle cleanup. Without one, the worktree directory is left on disk."
  > "Claude Code passes the path that WorktreeCreate printed on stdout as `worktree_path` in the hook input."
  - *Implication*: Without a paired `WorktreeRemove` hook, directories created by a custom `WorktreeCreate` hook are not cleaned up automatically. Hook failures are logged in debug mode only; removal cannot be blocked.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **Hook type support table clarified**: The documentation now explicitly lists which events support all three hook types (`command`, `prompt`, `agent`) versus which are restricted to `type: "command"` only.
  > "Events that only support `type: \"command\"` hooks: ConfigChange, Notification, PreCompact, SessionEnd, SessionStart, SubagentStart, TeammateIdle, WorktreeCreate, WorktreeRemove"
  - *Implication*: `WorktreeCreate` and `WorktreeRemove` do not support prompt-based or agent-based hooks.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **Decision control table updated for `WorktreeCreate`**: The JSON output decision control reference now includes `WorktreeCreate` with its unique decision pattern.
  > "WorktreeCreate: stdout path — Hook prints absolute path to created worktree. Non-zero exit fails creation"
  > "WorktreeRemove, Notification, SessionEnd, PreCompact: None — No decision control. Used for side effects like logging or cleanup"
  - *Implication*: `WorktreeCreate` uses a distinct pattern from all other events: the hook communicates the result via stdout (the worktree path), not via a JSON decision field.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **`ConfigChange` matcher support added to hooks guide**: The matcher table in the hooks guide now includes `ConfigChange` as an event that supports matcher filtering by configuration source.
  > "ConfigChange | configuration source | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`"
  - *Implication*: This corrects an omission that previously existed in the guide's matcher table (it was already in the reference page); both pages now agree.
  - *Source*: [Automate workflows with hooks](https://code.claude.com/docs/en/hooks-guide.md)

- **`SessionStart` source values updated in hooks guide**: The hooks guide example text was updated to add `clear` as a valid `SessionStart` source value.
  > "`SessionStart` hooks get the `source` (startup, resume, clear, compact)"
  - *Source*: [Automate workflows with hooks](https://code.claude.com/docs/en/hooks-guide.md)

### Worktrees and Parallel Workflows

- **Subagent worktree isolation documented**: A new subsection in the common workflows page explains how subagents can use worktree isolation to avoid conflicts when working in parallel.
  > "Subagents can also use worktree isolation to work in parallel without conflicts. Ask Claude to 'use worktrees for your agents' or configure it in a custom subagent by adding `isolation: worktree` to the agent's frontmatter. Each subagent gets its own worktree that is automatically cleaned up when the subagent finishes without changes."
  - *Implication*: This enables multi-agent parallelism at the filesystem level without manual coordination.
  - *Source*: [Common workflows](https://code.claude.com/docs/en/common-workflows.md)

- **Non-git version control workflow documented**: A new subsection explains how to extend worktree isolation to non-git VCS by configuring hooks.
  > "Worktree isolation works with git by default. For other version control systems like SVN, Perforce, or Mercurial, configure WorktreeCreate and WorktreeRemove hooks to provide custom worktree creation and cleanup logic. When configured, these hooks replace the default git behavior when you use `--worktree`."
  - *Source*: [Common workflows](https://code.claude.com/docs/en/common-workflows.md)

### CLI

- **New `claude agents` command**: A new CLI command lists all configured subagents without starting an interactive session.
  > "`claude agents` | List all configured subagents, grouped by source | `claude agents`"
  - *Implication*: Useful for quickly auditing which subagents are available and which are overridden by higher-priority definitions, without entering an interactive session.
  - *Source*: [CLI reference](https://code.claude.com/docs/en/cli-reference.md)

- **`--worktree` flag moved in CLI flags table**: The `--worktree` / `-w` flag was repositioned in the CLI flags table to maintain alphabetical order (moved from between `--resume` and `--session-id` to after `--version`). No change to the flag behavior or description.
  - *Source*: [CLI reference](https://code.claude.com/docs/en/cli-reference.md)

### Configuration and Environment Variables

- **New `CLAUDE_CODE_DISABLE_1M_CONTEXT` environment variable**: A new variable allows administrators to disable 1M context window support entirely.
  > "Set to `1` to disable 1M context window support. When set, 1M model variants are unavailable in the model picker. Useful for enterprise environments with compliance requirements"
  - *Implication*: Enterprise deployments that need to restrict usage to standard context windows can now do so via environment variable.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **Environment variable table re-sorted alphabetically**: Multiple environment variable rows were reordered in the settings table to restore strict alphabetical order. No descriptions changed.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Model Configuration

- **Default model inline table removed, replaced with link**: The table showing default models by subscription tier (Opus 4.6 for Max/Team/Pro, Sonnet 4.5 for pay-as-you-go) was removed in favor of a link to the relevant anchor section.
  > "It always remains available and represents the system's runtime default [based on the user's subscription tier](#default-model-setting)."
  - *Implication*: The specific model names per tier are no longer shown inline; readers must follow the anchor link to see current defaults.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

- **Example updated from Sonnet 4.5 to Sonnet 4.6**: The `availableModels` configuration example was updated to reference Sonnet 4.6.
  > "This example ensures all users run Sonnet 4.6 and can only choose between Sonnet and Haiku"
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

- **`CLAUDE_CODE_DISABLE_1M_CONTEXT` documented on model config page**: Added alongside the existing 1M context description.
  > "To disable 1M context entirely, set `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. This removes 1M model variants from the model picker. See environment variables."
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

### Sub-agents

- **`claude agents` command cross-referenced**: The sub-agents page now documents the CLI command as an alternative to the interactive `/agents` menu.
  > "To list all configured subagents from the command line without starting an interactive session, run `claude agents`. This shows agents grouped by source and indicates which are overridden by higher-priority definitions."
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

## Notable Details

- **`WorktreeCreate` is blocking; `WorktreeRemove` is not**: Unlike most hook events, `WorktreeCreate` treats any non-zero exit code as a failure (not just exit code 2). `WorktreeRemove` failures are silent by default — logged only in debug mode.
- **Hooks lifecycle diagram updated**: The `hooks-lifecycle.svg` image was replaced with a new version. Its alt text now explicitly mentions `WorktreeCreate` and `WorktreeRemove` as "standalone setup and teardown events," reflecting that they sit outside the main agentic loop.
- **Six events now explicitly listed as matcher-ignorant**: The note previously named only `UserPromptSubmit` and `Stop` as events that silently ignore the `matcher` field. It now names all six: `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, and `WorktreeRemove`.
- **Overview page changes are formatting-only**: The `overview.md` changes fix duplicated `theme={null}` attributes in code block tags (e.g., `theme={null} theme={null}` corrected to `theme={null}`). No content changed.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| [hooks.md](https://code.claude.com/docs/en/hooks.md) | Modified | +153 / -38 | Added `WorktreeCreate` and `WorktreeRemove` events with full schemas, examples, and decision control documentation; updated all relevant tables; clarified hook type support by event |
| [hooks-guide.md](https://code.claude.com/docs/en/hooks-guide.md) | Modified | +31 / -28 | Added `WorktreeCreate`/`WorktreeRemove` to event and matcher tables; added `ConfigChange` matcher row; updated `SessionStart` source list to include `clear` |
| [common-workflows.md](https://code.claude.com/docs/en/common-workflows.md) | Modified | +8 / -0 | Added "Subagent worktrees" and "Non-git version control" subsections under the worktrees section |
| [settings.md](https://code.claude.com/docs/en/settings.md) | Modified | +11 / -10 | Added `CLAUDE_CODE_DISABLE_1M_CONTEXT`; re-sorted environment variable table alphabetically |
| [model-config.md](https://code.claude.com/docs/en/model-config.md) | Modified | +4 / -7 | Removed inline default model table; added link to anchor; updated Sonnet example to 4.6; added `CLAUDE_CODE_DISABLE_1M_CONTEXT` note |
| [cli-reference.md](https://code.claude.com/docs/en/cli-reference.md) | Modified | +13 / -12 | Added `claude agents` command; repositioned `--worktree` flag alphabetically in flags table |
| [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md) | Modified | +2 / -0 | Documented `claude agents` CLI command as alternative to interactive `/agents` |
| [overview.md](https://code.claude.com/docs/en/overview.md) | Modified | +5 / -5 | Formatting only: removed duplicate `theme={null}` attributes from code block tags |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-21*
