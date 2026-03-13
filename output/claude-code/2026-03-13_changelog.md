# Claude Code Documentation Changes — 2026-03-13

## Summary

Three new dedicated reference pages were added — for built-in commands, environment variables, and tools — and their previously embedded content was removed from `settings.md`, `interactive-mode.md`, and `cli-reference.md`. The model configuration page was updated to document the `opus[1m]` alias alongside the existing `sonnet[1m]` alias, and the hooks reference gained a new `once` field for one-shot hook handlers scoped to skills.

## Significant Changes

### New Reference Pages (Content Reorganization)

The most significant structural change is the extraction of previously embedded reference content into three standalone pages. Cross-links across 22 modified pages have been updated to point to these new locations.

- **Built-in Commands Reference**: The full `/`-command table was moved from `interactive-mode.md` into its own dedicated page. It now lists 60+ commands with descriptions, including platform/plan/environment-gated visibility notes, MCP prompt commands (`/mcp__<server>__<prompt>`), and links to skills and CLI reference.
  > "Type `/` in Claude Code to see all available commands, or type `/` followed by any letters to filter. Not all commands are visible to every user. Some depend on your platform, plan, or environment."
  - *Implication*: Bookmarks or deep links to `interactive-mode.md#built-in-commands` will need updating. The `interactive-mode.md` page now redirects to this new page for the command list.
  - *Source*: [Built-in commands](https://code.claude.com/docs/en/commands.md)

- **Environment Variables Reference**: All environment variables that control Claude Code behavior have been extracted from `settings.md` and other pages into a single comprehensive reference. Variables can be set in the shell before launching `claude` or configured under the `env` key in `settings.json`.
  > "Claude Code supports the following environment variables to control its behavior. Set them in your shell before launching `claude`, or configure them in `settings.json` under the `env` key to apply them to every session or roll them out across your team."
  - *Implication*: The `settings.md` page lost ~200 lines of env var content. Developers looking for variables like `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`, `CLAUDE_CODE_EFFORT_LEVEL`, `CLAUDE_ENV_FILE`, or `CLAUDE_CODE_DISABLE_AUTO_MEMORY` should consult this dedicated page.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **Tools Reference**: The complete list of Claude Code's internal tools has been moved from `settings.md` into a dedicated page. Each tool entry includes its description, whether it requires user permission, and a link to relevant docs. The page also covers Bash tool persistence behavior and how to reference `CLAUDE_ENV_FILE` for environment variable persistence.
  > "The tool names below are the exact strings you use in permission rules, subagent tool lists, and hook matchers."
  - *Implication*: The `Bash tool behavior` and `Extending tools with hooks` sections have been removed from `settings.md`. Developers configuring `PreToolUse` hooks, subagent tool restrictions, or permission rules should reference this page. The `LSP` tool (code intelligence via language servers) and `ToolSearch` (deferred tool loading) are explicitly listed here.
  - *Source*: [Tools reference](https://code.claude.com/docs/en/tools-reference.md)

### Model Configuration

- **`opus[1m]` alias added to documentation**: The model configuration page now explicitly documents the `opus[1m]` alias alongside `sonnet[1m]`. The section previously titled "Use the sonnet[1m] alias" has been renamed "Use the opus[1m] or sonnet[1m] alias" and the model alias table has been updated.
  > ```
  > # Use the opus[1m] or sonnet[1m] alias
  > /model opus[1m]
  > /model sonnet[1m]
  >
  > # Or append [1m] to a full model name
  > /model claude-opus-4-6[1m]
  > ```
  - *Implication*: Developers on Max, Team, and Enterprise plans can now use `/model opus[1m]` to explicitly request Opus 4.6 with 1M context. Both `opus[1m]` and `sonnet[1m]` are now first-class documented aliases.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

### Hooks

- **New `once` field for hook handlers**: A `once` boolean field was added to the hook handler common fields table. When `true`, the hook runs only once per session and is then automatically removed. This applies to skills only, not agents.
  > "`once` — If `true`, runs only once per session then is removed. Skills only, not agents. See Hooks in skills and agents"
  - *Implication*: Enables single-use initialization logic in skill-scoped hooks — useful for one-time setup checks or setup gates that should fire exactly once.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

### Memory

- **`autoMemoryDirectory` policy restriction clarified**: The `memory.md` page was updated to explicitly state that `autoMemoryDirectory` is not accepted from project settings (`.claude/settings.json`), preventing a shared project from redirecting auto memory writes to sensitive or unexpected locations. The setting is accepted from policy, local, and user settings only.
  > "This setting is accepted from policy, local, and user settings. It is not accepted from project settings (`.claude/settings.json`) to prevent a shared project from redirecting auto memory writes to sensitive locations."
  - *Implication*: Teams deploying shared project configurations cannot redirect auto memory storage via project-level settings. Use user or managed policy settings if redirection is needed.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

### CLI Reference

- **`Agents flag format` section removed**: The standalone subsection documenting the `--agents` JSON flag format has been removed. The format information is now integrated directly into the `--agents` flag description in the main flags table, which still fully documents the JSON structure and all supported frontmatter fields.
  - *Implication*: No functional change; the reference is more consolidated.
  - *Source*: [CLI reference](https://code.claude.com/docs/en/cli-reference.md)

## New Pages

- **[commands.md](https://code.claude.com/docs/en/commands.md)** — Complete reference table of all built-in `/` commands, platform/plan gating notes, MCP prompt commands, and links to skills and CLI reference. Extracted from `interactive-mode.md`.
- **[env-vars.md](https://code.claude.com/docs/en/env-vars.md)** — Comprehensive reference for all environment variables controlling Claude Code behavior. Extracted from `settings.md` and scattered inline content across other pages.
- **[tools-reference.md](https://code.claude.com/docs/en/tools-reference.md)** — Full list of Claude Code tools with permission requirements and Bash tool persistence notes. Extracted from the "Bash tool behavior" section in `settings.md`.

## Notable Details

- The `interactive-mode.md` page lost its "### MCP prompts" section as part of the -73 line reduction. MCP prompt commands are now documented in `commands.md`. The page is now focused on keyboard shortcuts, vim mode, background bash, prompt suggestions, and `/btw` side questions.
- The `settings.md` page dropped a net ~200 lines. Removed sections: `### Bash tool behavior`, `### Extending tools with hooks`, and multiple env var code examples. The page is now tighter and focused on settings scopes, configuration files, and permission/hook settings schema.
- 15+ pages had a single cross-reference line changed from `/en/interactive-mode#built-in-commands` to `/en/commands`, confirming the breadth of the reorganization across the docs site.
- The `sub-agents.md` page (+10/-6) updated its tools section to reference the new `tools-reference.md` page: `"Subagents can use any of Claude Code's internal tools"` now links directly there.
- The `skills.md` page (+11/-13) similarly updated its reference to built-in commands: `"For built-in commands like /help and /compact, see the built-in commands reference /en/commands"`.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| commands.md | New | +87 | Complete built-in commands reference (extracted from interactive-mode.md) |
| env-vars.md | New | large | Complete environment variables reference (extracted from settings.md) |
| tools-reference.md | New | +59 | Complete tools reference with permission requirements (extracted from settings.md) |
| settings.md | Modified | +12/-213 | Removed Bash tool behavior, env vars, and hooks-extension content; links out to dedicated pages |
| interactive-mode.md | Modified | +4/-73 | Removed MCP prompts section and full commands table; now links to commands.md |
| cli-reference.md | Modified | +9/-70 | Removed standalone "Agents flag format" section; format now inline in --agents description |
| model-config.md | Modified | +21/-12 | Added opus[1m] alias to table and code examples; renamed section heading |
| sub-agents.md | Modified | +10/-6 | Updated tools reference link to tools-reference.md |
| skills.md | Modified | +11/-13 | Updated commands reference link to commands.md; clarification updates |
| common-workflows.md | Modified | +10/-10 | Link/wording updates |
| vs-code.md | Modified | +7/-7 | Updated cross-reference links to commands.md |
| third-party-integrations.md | Modified | +6/-6 | Link/wording updates |
| hooks.md | Modified | +4/-0 | Added `once` field to hook handler common fields table |
| memory.md | Modified | +3/-1 | Added policy restriction note for autoMemoryDirectory |
| desktop.md | Modified | +3/-3 | Link updates |
| google-vertex-ai.md | Modified | +2/-4 | Minor content cleanup |
| setup.md | Modified | +2/-2 | Link updates |
| checkpointing.md | Modified | +1/-1 | Updated link from interactive-mode#built-in-commands to /en/commands |
| desktop-quickstart.md | Modified | +1/-1 | Link update |
| fast-mode.md | Modified | +1/-1 | Link update |
| headless.md | Modified | +1/-1 | Link update |
| how-claude-code-works.md | Modified | +1/-1 | Link update |
| network-config.md | Modified | +1/-1 | Link update |
| scheduled-tasks.md | Modified | +1/-1 | Link update |
| troubleshooting.md | Modified | +1/-1 | Link update |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-13*
