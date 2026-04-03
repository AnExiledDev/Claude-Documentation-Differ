# Claude Code Documentation Changes — 2026-04-03

## Summary

Five pages were modified in this update. The dominant change is a large expansion of plugin marketplace CLI documentation, introducing four new non-interactive `claude plugin marketplace` subcommands for scripting and automation. Smaller updates clarify orphaned worktree auto-cleanup behavior, fix the `excludedCommands` sandbox syntax, and link `cleanupPeriodDays` to worktree lifecycle management.

## Significant Changes

### Features

- **New `claude plugin marketplace` CLI subcommands**: The plugin marketplace system now exposes four non-interactive subcommands — `add`, `list`, `remove`, and `update` — for use in scripts and CI/CD pipelines.
  > "Claude Code provides non-interactive `claude plugin marketplace` subcommands for scripting and automation. These are equivalent to the `/plugin marketplace` commands available inside an interactive session."
  - `add` accepts GitHub `owner/repo` shorthand, git URLs, direct `marketplace.json` URLs, or local paths; supports `--scope` (`user`, `project`, or `local`) and `--sparse` for monorepo checkouts.
  - `list` accepts `--json` for machine-readable output.
  - `remove` (alias `rm`) uninstalls all plugins from the marketplace on removal — use `update` instead to refresh without losing installed plugins.
  - `update [name]` refreshes one or all marketplaces; seed-managed entries are silently skipped.
  - *Implication*: Teams can now manage marketplaces entirely from scripts without launching an interactive Claude Code session.
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

- **`CLAUDE_CODE_PLUGIN_CACHE_DIR` environment variable for seed directory builds**: Documentation now describes an alternative approach that avoids a post-install copy step when pre-populating container images.
  > "To skip the copy step, set `CLAUDE_CODE_PLUGIN_CACHE_DIR` to your target seed path during the build so plugins install directly there:"
  ```bash
  CLAUDE_CODE_PLUGIN_CACHE_DIR=/opt/claude-seed claude plugin marketplace add your-org/plugins
  CLAUDE_CODE_PLUGIN_CACHE_DIR=/opt/claude-seed claude plugin install my-tool@your-plugins
  ```
  - *Implication*: Container image builds can install plugins directly to the intended seed path, removing the manual copy step previously required.
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

- **Automatic cleanup of orphaned subagent worktrees at startup**: Claude Code now removes subagent worktrees left behind by crashes or interrupted parallel runs once they exceed the `cleanupPeriodDays` age threshold.
  > "Subagent worktrees orphaned by a crash or an interrupted parallel run are removed automatically at startup once they are older than your `cleanupPeriodDays` setting, provided they have no modifications to tracked files and no unpushed commits. Untracked files (new files never staged with `git add`) are not checked and do not prevent removal. Worktrees you create with `--worktree` are never removed by this sweep."
  - *Implication*: Developers running parallel agents no longer need to manually prune stale worktrees after crashes; user-created `--worktree` worktrees are explicitly protected from this sweep.
  - *Source*: [Common Workflows](https://code.claude.com/docs/en/common-workflows.md)

### Configuration

- **`cleanupPeriodDays` now governs worktree cleanup age**: The setting description was updated to document its dual role — it controls both session transcript deletion and the age cutoff for orphaned subagent worktree removal.
  > "Also controls the age cutoff for automatic removal of orphaned subagent worktrees at startup."
  - *Implication*: Administrators tuning `cleanupPeriodDays` for session retention should be aware this value also affects how long stale worktrees persist before auto-removal.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`excludedCommands` sandbox syntax corrected to glob patterns**: The documented example for excluding Docker from sandboxing changed from `"docker"` to `"docker *"`, indicating that exclusions require glob-style matching.
  > "Consider specifying `docker *` in `excludedCommands` to force it to run outside of the sandbox."

  The `excludedCommands` settings reference example was also updated:
  > Previous: `["git", "docker"]` → Now: `["docker *"]`
  - *Implication*: Existing configurations using bare command names like `"docker"` without a glob may not correctly exclude all invocations of that command. The `"git"` entry was also dropped from the example, suggesting it no longer requires exclusion.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md) · [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)

- **Seed marketplace mutations now explicitly blocked**: A new bullet was added to the seed directory behavior documentation.
  > "**Mutation is blocked**: running `/plugin marketplace remove` or `/plugin marketplace update` against a seed-managed marketplace fails with guidance to ask your administrator to update the seed image."
  - *Implication*: This clarifies expected error behavior when operators or users attempt to modify seed-provided marketplaces, directing them to the admin workflow instead.
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

### Notable Details

- **Relative path resolution wording clarified**: The note in the plugin sources table was updated from "Must start with `./`" to "Must start with `./`. Resolved relative to the marketplace root, not the `.claude-plugin/` directory" — making the path resolution rule explicit in the table itself rather than only in the prose below.
- **`../` restriction reworded**: "Do not use `../` to climb out of `.claude-plugin/`" was changed to "Do not use `../` to reference paths outside the marketplace root." This is a more accurate description since `.claude-plugin/` is a subdirectory of the marketplace root, not the root itself.
- **`setup.md` code block cosmetic fix**: Duplicate `theme={null}` attributes were deduplicated in all installation code blocks (e.g., `theme={null} theme={null} theme={null}` → `theme={null}`). No functional content change.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| plugin-marketplaces.md | Modified | +128 / -9 | New CLI subcommand reference for `add`, `list`, `remove`, `update`; `CLAUDE_CODE_PLUGIN_CACHE_DIR` env var; seed mutation block behavior; relative path note clarification |
| common-workflows.md | Modified | +2 / -0 | Documents automatic orphaned subagent worktree cleanup at startup |
| settings.md | Modified | +3 / -3 | `cleanupPeriodDays` links to worktree cleanup; `excludedCommands` example updated to glob syntax |
| sandboxing.md | Modified | +1 / -1 | `excludedCommands` Docker example corrected from `"docker"` to `"docker *"` |
| setup.md | Modified | +5 / -5 | Cosmetic deduplication of `theme={null}` attributes in install code blocks |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-03*
