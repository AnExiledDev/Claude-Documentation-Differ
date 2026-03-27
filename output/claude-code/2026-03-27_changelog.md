# Claude Code Documentation Changes — 2026-03-27

## Summary

A new interactive context window visualization page was added, and MCP Tool Search behavior was updated from threshold-based to always-on by default. Several pages received cross-reference links to the new visualization, and a `.worktreeinclude` file feature for copying gitignored files into worktrees was documented.

## Significant Changes

### Features

- **New interactive context window visualization**: A new `context-window.md` page provides a step-by-step animated simulation of how Claude Code's context window fills during a real session, showing what loads automatically (system prompt, CLAUDE.md, auto memory, MCP tool names, skill descriptions), what each file read costs, when path-scoped rules fire, and how subagents keep heavy work isolated.
  > "An interactive simulation of how Claude Code's context window fills during a session. See what loads automatically, what each file read costs, and when rules and hooks fire."
  - *Implication*: Developers can now see concrete token counts for each context source and understand exactly what Claude sees vs. what appears in the terminal.
  - *Source*: [Explore the context window](https://code.claude.com/docs/en/context-window.md)

- **`.worktreeinclude` file for copying gitignored files to worktrees**: A new workflow was documented for automatically copying gitignored files (such as `.env`, `.env.local`, `config/secrets.json`) into new git worktrees. Place a `.worktreeinclude` file in the project root using `.gitignore` syntax to specify which files to copy.
  > "Git worktrees are fresh checkouts, so they don't include untracked files like `.env` or `.env.local` from your main repository. To automatically copy these files when Claude creates a worktree, add a `.worktreeinclude` file to your project root."
  > "This applies to worktrees created with `--worktree`, subagent worktrees, and parallel sessions in the desktop app."
  - *Implication*: Eliminates the manual step of copying secrets and environment configs each time a new parallel session or worktree is created.
  - *Source*: [Common workflows](https://code.claude.com/docs/en/common-workflows.md)

### Configuration

- **MCP Tool Search is now always-on by default**: The previous behavior loaded all MCP tool schemas at session start and only deferred them when they exceeded 10% of the context window. Tool search now defers schemas unconditionally — only tool names enter context at startup, with full schemas loaded on demand when Claude uses a specific tool.
  > "Tool search is enabled by default. MCP tools are deferred rather than loaded into context upfront, and Claude uses a search tool to discover relevant ones when a task needs them. Only the tools Claude actually uses enter context."
  > "If you prefer threshold-based loading, set `ENABLE_TOOL_SEARCH=auto` to load schemas upfront when they fit within 10% of the context window and defer only the overflow."
  - *Implication*: Adding more MCP servers now has near-zero context cost at idle. The old opt-in threshold behavior (`ENABLE_TOOL_SEARCH=auto`) is still available for those who prefer it.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

- **Subagent memory limit clarified as 200 lines or 25KB (whichever comes first)**: The memory loading limit for subagents with persistent memory enabled was documented imprecisely as "first 200 lines". The spec now matches the behavior described elsewhere for auto memory.
  > "The subagent's system prompt also includes the first 200 lines or 25KB of `MEMORY.md` in the memory directory, whichever comes first, with instructions to curate `MEMORY.md` if it exceeds that limit."
  - *Implication*: Large MEMORY.md files with short lines may hit the 25KB cap before the 200-line limit; subagents should keep memory files concise to stay within bounds.
  - *Source*: [Create custom subagents](https://code.claude.com/docs/en/sub-agents.md)

## New Pages

- **context-window.md** — Interactive animated visualization of Claude Code's context window filling during a session. Covers all auto-loaded startup content (system prompt, CLAUDE.md, auto memory, MCP tool names, skill descriptions), file read costs, path-scoped rule triggers, hook output, subagent isolation, and the effect of `/compact`. Includes `What the timeline shows` and `Check your own session` sections. [View](https://code.claude.com/docs/en/context-window.md)

## Notable Details

- **MCP context cost table updated**: The features overview table previously read "All tool definitions and schemas / Every request" for MCP servers. It now reads "Tool names; full schemas on demand / Low until a tool is used" — directly reflecting the always-on deferred loading behavior.
- **Context-loading diagram updated**: The `context-loading.svg` image on `features-overview.md` was replaced with a new version; the alt text changed from "CLAUDE.md and MCP load at session start and stay in every request" to "CLAUDE.md loads at session start... MCP tool names load at start with full schemas deferred until use."
- **Cross-reference links added to new context-window page**: Four pages (`best-practices.md`, `features-overview.md`, `how-claude-code-works.md`, `memory.md`, `sub-agents.md`) received added links to the new `/en/context-window` visualization — all in context-management-adjacent sections.
- **Desktop parallel sessions page updated**: A cross-reference to `.worktreeinclude` was added to the desktop parallel sessions section alongside the existing worktree documentation.
- **costs.md MCP section simplified**: The bullet point explaining the `ENABLE_TOOL_SEARCH=auto:<N>` threshold override was removed. The section now just states that MCP tool definitions are deferred by default and recommends disabling unused servers.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| context-window.md | New | +1596 | Interactive context window visualization with animated session timeline |
| common-workflows.md | Modified | +14/-0 | Added "Copy gitignored files to worktrees" section with `.worktreeinclude` |
| features-overview.md | Modified | +5/-5 | Updated MCP context cost table and diagram; added context-window link |
| mcp.md | Modified | +3/-6 | Rewrote Tool Search section: always-on by default, not threshold-based |
| how-claude-code-works.md | Modified | +3/-1 | Updated MCP context description; added context-window link |
| costs.md | Modified | +2/-3 | Updated MCP overhead section for deferred-by-default tool loading |
| sub-agents.md | Modified | +2/-2 | Added context-window link; fixed memory limit to "200 lines or 25KB" |
| desktop.md | Modified | +2/-0 | Added `.worktreeinclude` cross-reference in parallel sessions section |
| memory.md | Modified | +1/-1 | Added context-window visualization link in "Write effective instructions" |
| best-practices.md | Modified | +1/-1 | Added context-window interactive walkthrough link |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-27*
