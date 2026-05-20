# Claude Code Documentation Changes — 2026-05-20

## Summary

Fifteen pages were modified in this update, with no pages added or removed (+169/-51 lines total). The most substantive changes introduce three new bundled skills for running and verifying apps directly (`/run`, `/verify`, `/run-skill-generator`), expand plugin install-preview detail with version-gated metadata, and add repository identity fields to the status line data schema. Hooks and CLI reference documentation also received significant content updates.

## Significant Changes

### Features: New Bundled Skills

- **`/run`, `/verify`, and `/run-skill-generator` skills added**: Three new bundled skills are now documented that let Claude launch and test the running app — not just tests — to confirm a code change works.

  > `/run` — Launch and drive your app to see a change working
  >
  > `/verify` — Build and run your app to confirm a code change does what it should, without falling back to tests or type checks
  >
  > `/run-skill-generator` — Teach `/run` and `/verify` how to build and launch your project

  These skills infer launch behavior from project files (`README`, `package.json`, `Makefile`) for standard setups, but `/run-skill-generator` records a per-project recipe in `.claude/skills/run-<name>/` for projects that need databases, env files, or non-standard builds.

  - *Implication*: Developers can now verify changes against the live application without leaving Claude Code. Run `/run-skill-generator` once per project; subsequent `/run` and `/verify` calls follow the recorded recipe.
  - *Source*: [Extend Claude with skills](https://code.claude.com/docs/en/skills.md), [Commands](https://code.claude.com/docs/en/commands.md)

  > All three skills require Claude Code v2.1.145 or later.

### Configuration: Plugin Install Detail Pane

- **Version-gated metadata now shown before plugin install**: The plugin detail pane in `/plugin` Discover now surfaces three new items, each tied to a minimum version:

  > - A **Context cost** estimate so you can see how many tokens the plugin will add to your context window every turn (v2.1.143 and later)
  > - The plugin's **Last updated** date (v2.1.144 and later)
  > - A **Will install** section listing the plugin's commands, agents, skills, hooks, and MCP and LSP servers, so you can review exactly what it adds before installing (v2.1.145 and later)

  - *Implication*: Users can inspect a plugin's full footprint — context cost, freshness, and component inventory — before committing to install. This enables more informed plugin management in large projects.
  - *Source*: [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins.md)

### Configuration: Status Line New Data Fields

- **Repository identity and git worktree fields added to status line schema**: The `statusline` Available Data table now includes `workspace.repo.host`, `workspace.repo.owner`, `workspace.repo.name`, and `workspace.git_worktree`.

  > `workspace.repo.host`, `workspace.repo.owner`, `workspace.repo.name` — Repository identity parsed from the `origin` remote, for example `"github.com"`, `"anthropics"`, `"claude-code"`. Absent outside a git repository or when no `origin` remote is configured.
  >
  > `workspace.git_worktree` — Git worktree name when the current directory is inside a linked worktree created with `git worktree add`. Absent in the main working tree. Populated for any git worktree, unlike `worktree.*` which applies only to `--worktree` sessions.

  - *Implication*: Status line scripts can now display the current repository and distinguish between linked git worktrees and regular directories, useful for monorepo and multi-project setups.
  - *Source*: [Customize your status line](https://code.claude.com/docs/en/statusline.md)

### Configuration: Hooks Documentation Expanded

- **Hooks reference received significant new content (+51/-3 lines)**: The hooks reference page was substantially updated. The lifecycle diagram alt text now enumerates a comprehensive event set including `UserPromptExpansion`, `PermissionDenied`, `PostToolBatch`, `SubagentStart/Stop`, `TaskCreated/Completed`, `TeammateIdle`, `PreCompact/PostCompact`, `Elicitation/ElicitationResult`, `WorktreeCreate/Remove`, `InstructionsLoaded`, `CwdChanged`, and `FileChanged` — events documented individually in the events table.

  Notable event descriptions:

  > `PermissionDenied` — When a tool call is denied by the auto mode classifier. Return `{retry: true}` to tell the model it may retry the denied tool call.
  >
  > `UserPromptExpansion` — When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion.
  >
  > `InstructionsLoaded` — When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session.

  - *Implication*: Hook authors now have documentation for the full event surface, including expansion, permission denial retry logic, and lifecycle events for compact and elicitation flows.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

### Reference: CLI Flags Documentation Reformulated

- **CLI reference received equivalent-volume reformulation (+28/-28 lines)**: The CLI reference saw significant line-for-line rewrites, likely improving description precision for several flags. Version references were updated (e.g., `--resume` notes background sessions appear in the picker marked with `bg` as of v2.1.144). The `--effort` flag now lists all valid levels: `low`, `medium`, `high`, `xhigh`, `max`.

  - *Implication*: Developers relying on the CLI reference for flag descriptions will find more precise and up-to-date text. No flags were added or removed in this update.
  - *Source*: [CLI reference](https://code.claude.com/docs/en/cli-reference.md)

### Reference: Plugins Reference — Unrecognized Fields Section

- **New section "Unrecognized fields" added to plugins reference (+25 lines)**: The plugins reference gained a new subsection documenting how Claude Code handles unknown or unrecognized fields in plugin configuration schemas.
  - *Implication*: Plugin authors have explicit guidance on forward/backward compatibility when fields are unrecognized by older or newer versions.
  - *Source*: [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md)

## Minor Changes

- **agent-view.md**: Minor content addition (+3/-0 lines). Likely a note or clarification in the agent view documentation.
- **commands.md**: Added `/run`, `/run-skill-generator`, and `/verify` to the all-commands table (+3/-0 lines).
- **env-vars.md**: Small reformulation of an environment variable description (+2/-2 lines).
- **fullscreen.md**: Single-line addition (+1/-0 lines).
- **interactive-mode.md**: Minor rewording (+1/-2 lines).
- **monitoring-usage.md**: Updated monitoring documentation (+11/-9 lines); likely revised telemetry variable descriptions.
- **output-styles.md**: Minor rewording (+2/-2 lines).
- **permission-modes.md**: Single-line substitution (+1/-1 lines).
- **tools-reference.md**: Single-line substitution (+1/-1 lines).

## Notable Details

- The `/run`, `/verify`, and `/run-skill-generator` skills are gated to **v2.1.145+** per inline version comments in both `skills.md` and `commands.md`. Users on earlier versions will not see these commands.
- The discover-plugins.md version gates span three consecutive releases (v2.1.143 → 2.1.144 → 2.1.145), indicating each piece of the install-detail feature was shipped incrementally.
- The `workspace.git_worktree` field is explicitly noted as distinct from `worktree.*` fields: it fires for any `git worktree add` linked worktree, while `worktree.*` fields only populate for `--worktree` sessions. This distinction matters for status line scripts used in monorepo environments.
- The `PermissionDenied` hook event supports `{retry: true}` as a return value, enabling hook authors to build retry-on-denial workflows for auto mode.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| hooks.md | Modified | SIGNIFICANT | +51/-3 | Expanded hook events documentation and lifecycle diagram |
| cli-reference.md | Modified | SIGNIFICANT | +28/-28 | Reformulated flag descriptions and version references |
| plugins-reference.md | Modified | SIGNIFICANT | +25/-0 | New "Unrecognized fields" section |
| skills.md | Modified | SIGNIFICANT | +18/-0 | New "Run and verify your app" section with `/run`, `/verify`, `/run-skill-generator` |
| statusline.md | Modified | SIGNIFICANT | +16/-1 | Added `workspace.repo.*` and `workspace.git_worktree` data fields |
| monitoring-usage.md | Modified | SIGNIFICANT | +11/-9 | Revised telemetry variable documentation |
| discover-plugins.md | Modified | SIGNIFICANT | +6/-2 | Plugin detail pane now shows context cost, last updated, and "Will install" (v2.1.143–2.1.145) |
| commands.md | Modified | MINOR | +3/-0 | Added `/run`, `/run-skill-generator`, `/verify` commands |
| agent-view.md | Modified | MINOR | +3/-0 | Minor addition |
| env-vars.md | Modified | MINOR | +2/-2 | Minor variable description update |
| output-styles.md | Modified | MINOR | +2/-2 | Minor rewording |
| fullscreen.md | Modified | MINOR | +1/-0 | Single-line addition |
| interactive-mode.md | Modified | MINOR | +1/-2 | Minor rewording |
| permission-modes.md | Modified | MINOR | +1/-1 | Minor rewording |
| tools-reference.md | Modified | MINOR | +1/-1 | Minor rewording |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-20*
