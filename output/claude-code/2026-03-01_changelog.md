# Claude Code Documentation Changes — 2026-03-01

## Summary

14 pages were modified across the Claude Code documentation, with the largest change being a significant reorganization of the memory/CLAUDE.md reference page. A new HTTP hook type was added to the hooks guide, two built-in bundled skills (`/simplify` and `/batch`) are now documented, and the `Task` tool used in subagent spawning was officially renamed to `Agent` as of version 2.1.63.

## Significant Changes

### Memory & CLAUDE.md

- **Memory documentation overhauled**: The page was retitled from "Manage Claude's memory" to "How Claude remembers your project" and restructured around two core concepts — CLAUDE.md files (user-written) and auto memory (Claude-written). A new comparison table leads the page to help developers choose the right mechanism.
  > "Claude Code has two complementary memory systems. Both are loaded at the start of every conversation. Claude treats them as context, not enforced configuration. The more specific and concise your instructions, the more consistently Claude follows them."
  - *Implication*: Developers should review the new scope table for CLAUDE.md file locations (Managed policy, Project, User, Local) and note that each scope now includes Windows paths explicitly (e.g., `C:\Program Files\ClaudeCode\CLAUDE.md`).
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

- **Auto memory controls now documented**: The `autoMemoryEnabled` setting and `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` environment variable are documented for toggling auto memory on or off.
  > "Auto memory is on by default. To toggle it, open `/memory` in a session and use the auto memory toggle, or set `autoMemoryEnabled` in your project settings: `{ \"autoMemoryEnabled\": false }`. To disable auto memory via environment variable, set `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`."
  - *Implication*: Teams that want to prevent Claude from accumulating session notes can now disable auto memory via settings file or environment variable — both are now first-class supported mechanisms.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

- **MEMORY.md 200-line loading limit clarified**: The auto memory entrypoint file `MEMORY.md` is loaded only up to 200 lines at session start. Content beyond line 200 is not loaded; Claude is expected to keep `MEMORY.md` concise by offloading detail into topic files.
  > "The first 200 lines of `MEMORY.md` are loaded at the start of every conversation. Content beyond line 200 is not loaded at session start. Claude keeps `MEMORY.md` concise by moving detailed notes into separate topic files."
  - *Implication*: This limit applies only to `MEMORY.md`, not to CLAUDE.md files (which load in full). Developers building workflows that rely on auto memory should be aware of what Claude will and won't see at startup.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

- **New troubleshooting section**: Four common failure modes are now documented with debugging steps: instructions not being followed, unclear what auto memory saved, CLAUDE.md files growing too large, and instructions seeming lost after `/compact`.
  > "CLAUDE.md is context, not enforcement. Claude reads it and tries to follow it, but there's no guarantee of strict compliance, especially for vague or conflicting instructions."
  - *Implication*: The troubleshooting guidance explicitly addresses the `/compact` concern — CLAUDE.md is re-injected from disk after compaction, so only in-conversation instructions (not written to CLAUDE.md) are lost.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

- **CLAUDE.md from `--add-dir` directories disabled by default**: When using `--add-dir` to give Claude access to additional directories, CLAUDE.md files from those directories are not loaded unless `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` is set.
  > "To also load CLAUDE.md files from additional directories, including `CLAUDE.md`, `.claude/CLAUDE.md`, and `.claude/rules/*.md`, set the `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` environment variable."
  - *Implication*: This is opt-in behavior. Developers using `--add-dir` for shared config directories will need to set this env var if they want shared CLAUDE.md files to take effect.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

### Hooks

- **HTTP hook type now documented**: The hooks guide adds a new `## HTTP hooks` section documenting `"type": "http"` as a hook handler type. This allows hook events to be POSTed to a URL instead of running a local shell command.
  > "`\"type\": \"http\"`: POST event data to a URL. See HTTP hooks."
  - *Implication*: This enables integrating Claude Code's hook lifecycle with remote services (e.g., logging endpoints, approval systems, webhook receivers) without needing a local script. The hook type sits alongside `command`, `prompt`, and `agent` types.
  - *Source*: [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)

### Skills

- **Two bundled skills now documented**: Claude Code ships with two built-in skills that are available in every session without configuration.

  - **`/simplify`**: Reviews recently changed files for code reuse, quality, and efficiency issues, then fixes them. Spawns three parallel review agents (code reuse, code quality, efficiency), aggregates findings, and applies fixes. Accepts optional text to focus on specific concerns.
  - **`/batch <instruction>`**: Orchestrates large-scale codebase changes in parallel. Researches the codebase, decomposes work into 5–30 independent units, presents a plan for approval, then spawns one background agent per unit in an isolated git worktree. Each agent implements its unit, runs tests, and opens a pull request. Requires a git repository.

  > "Claude Code ships with two built-in skills available in every session: `/simplify` ... `/batch <instruction>`..."
  - *Implication*: `/batch` in particular represents a significant capability — automated parallel codebase-wide changes with per-unit PR creation. It requires git and uses worktree isolation per unit.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

### Subagents & Permissions

- **`Task` tool renamed to `Agent` (v2.1.63)**: The internal tool used to spawn subagents was renamed from `Task` to `Agent`. Permission rules, subagent `tools` field values, and CLI flag syntax now use `Agent(agent_type)` instead of `Task(agent_type)`.
  > "In version 2.1.63, the Task tool was renamed to Agent. Existing `Task(...)` references in settings and agent definitions still work as aliases."
  - *Implication*: Existing configurations using `Task(Explore)` or `Task(my-agent)` continue to work without changes. New configurations should use `Agent(Explore)` etc. The permissions page now documents `Agent (subagents)` as a tool-specific rule category.
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md), [Permissions](https://code.claude.com/docs/en/permissions.md)

### Features Overview

- **New CLAUDE.md vs Rules vs Skills comparison tab**: The features overview page added a three-way comparison tab clarifying when to use each instruction storage mechanism.
  > "Use CLAUDE.md for instructions every session needs: build commands, test conventions, project architecture. Use rules to keep CLAUDE.md focused. Rules with `paths` frontmatter only load when Claude works with matching files, saving context. Use skills for content Claude only needs sometimes, like API documentation or a deployment checklist you trigger with `/<name>`."
  - *Implication*: This is a practical decision guide for teams building out their CLAUDE.md/rules/skills architecture.
  - *Source*: [Features Overview](https://code.claude.com/docs/en/features-overview.md)

## Notable Details

- **Effective instructions guidance added**: The memory page now gives specific CLAUDE.md authoring advice — target under 200 lines, use markdown structure, prefer concrete rules ("Use 2-space indentation") over vague ones ("Format code properly"), and audit for conflicting instructions across nested files. This 200-line target differs from the skills page's 500-line tip for `SKILL.md`, reflecting different loading semantics.

- **`claudeMdExcludes` setting documented more prominently**: The setting now has its own subsection with a concrete JSON example for monorepo users wanting to skip unrelated teams' CLAUDE.md files. It supports glob patterns matched against absolute paths and can be set at any settings layer (user, project, local, or managed policy). Managed policy CLAUDE.md files cannot be excluded.

- **Subagent auto memory scopes**: The memory page now cross-references subagent-specific memory (`/en/sub-agents#enable-persistent-memory`) as a related resource, confirming subagents can maintain their own auto memory directories separate from the main session.

- **`/batch` requires git**: The bundled `/batch` skill requires a git repository because it creates one isolated git worktree per unit of work. This is a runtime requirement, not just a recommendation.

- **VS Code minimum version**: The VS Code extension page reflects VS Code 1.98.0 as the minimum required version (minor version bump reflected in the diff).

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| memory.md | Modified | +198/-172 | Major reorganization: new title, CLAUDE.md vs auto memory comparison, scope table, auto memory controls, troubleshoot section |
| hooks-guide.md | Modified | +45/-2 | New `## HTTP hooks` section; documents `"type": "http"` hook handler alongside command/prompt/agent types |
| features-overview.md | Modified | +19/-3 | New CLAUDE.md vs Rules vs Skills comparison tab; updated context cost table |
| skills.md | Modified | +9/-1 | New `## Bundled skills` section documenting `/simplify` and `/batch` built-in skills |
| sub-agents.md | Modified | +10/-8 | Documents Task→Agent rename in v2.1.63; backward-compatible alias noted |
| permissions.md | Modified | +6/-6 | `Task (subagents)` section renamed to `Agent (subagents)`; syntax updated to `Agent(AgentName)` |
| mcp.md | Modified | +8/-1 | Minor additions to MCP server documentation |
| interactive-mode.md | Modified | +31/-31 | Table reformatting; equivalent additions and deletions indicate structural reorganization |
| cli-reference.md | Modified | +10/-10 | Updated `--agents` flag table: `Task(agent_type)` reference changed to `Agent(agent_type)` |
| hooks.md | Modified | +5/-5 | Minor reference/wording updates |
| how-claude-code-works.md | Modified | +3/-0 | Small content additions |
| overview.md | Modified | +3/-2 | Minor content updates |
| settings.md | Modified | +3/-2 | Minor content updates |
| vs-code.md | Modified | +1/-1 | VS Code minimum version update |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-01*
