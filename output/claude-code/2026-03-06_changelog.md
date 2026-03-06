# Claude Code Documentation Changes — 2026-03-06

## Summary

All 8 modified pages reflect a uniform documentation formatting pass: bare code fences (` ``` `) for user-typed prompts and command examples have been replaced with typed, theme-neutral fences (` ```text  theme={null} `), and the `>` REPL-prompt prefix has been stripped from inline examples. No functional content, commands, or behavioral guidance changed.

## Significant Changes

### Documentation Formatting Standardization

- **Code block typing across all pages**: Every example showing a user-typed Claude Code prompt or CLI command was changed from an untyped ` ``` ` fence to ` ```text  theme={null} `. This affects `common-workflows.md`, `how-claude-code-works.md`, `mcp.md`, `jetbrains.md`, `remote-control.md`, `sandboxing.md`, and `troubleshooting.md`.
  > ```text  theme={null}
  > give me an overview of this codebase
  > ```
  - *Implication*: Purely a rendering change. The `theme={null}` attribute disables syntax highlighting for prose prompts, likely to prevent false-positive highlighting of natural-language text that contains code-like tokens.
  - *Source*: [Common Workflows](https://code.claude.com/docs/en/common-workflows.md)

- **Removal of `>` prompt prefix from examples**: All user-prompt examples previously prefixed with `> ` (mimicking a REPL prompt) now appear as plain text within the typed block. Multi-prompt sequences that were combined in a single block are now split into individual blocks.
  > Before: `> /mcp`
  > After: `/mcp` (in its own `text theme={null}` block)
  - *Implication*: Improves copy-paste usability — users no longer need to strip the `>` prefix before entering a command.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

- **MCP examples restructured**: The Sentry, GitHub, and PostgreSQL example sections in `mcp.md` had their numbered bash comments (`# 1. Add the Sentry MCP server`, `# 2. Use /mcp to authenticate`, etc.) removed. Setup commands (bash) and follow-up prompts (text) are now separated into distinct, individually-typed code blocks with plain prose transitions.
  - *Implication*: No change in the actual commands or workflow steps; the Playwright MCP example remains commented out (`{/* ... */}`) as before.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

- **JetBrains `/ide` command split**: The `/ide` command was separated from the preceding `claude` bash block into its own `text theme={null}` block, consistent with the rest of the formatting pass.
  - *Source*: [JetBrains](https://code.claude.com/docs/en/jetbrains.md)

## Notable Details

- **changelog.md star/PR count**: The embedded GitHub repository metadata updated from 74.2k → 74.3k stars and 254 → 255 open pull requests. This is scraped UI state from the GitHub page, not a documentation authoring change.
- **`how-claude-code-works.md` bracket escaping**: The inline narrative `[Claude investigates, tries something]` was changed to `\[Claude investigates, tries something]` and moved outside the code block — a minor Markdown rendering fix to prevent the brackets from being parsed as a link reference.
- **`sandboxing.md`**: Removed the lone `>` prefix from the `/sandbox` command inside a block that was already typed as `text theme={null}`, bringing it in line with the rest of the pass.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| common-workflows.md | Modified | +105 / -102 | Formatting: bare fences → `text theme={null}`, `>` prefix removed across all prompt examples |
| mcp.md | Modified | +76 / -42 | Formatting: prompt examples split into individual typed blocks; numbered bash comments removed |
| how-claude-code-works.md | Modified | +20 / -18 | Formatting: same fence/prefix changes; bracket escaping fix |
| troubleshooting.md | Modified | +6 / -6 | Formatting: error message blocks retyped as `text theme={null}` |
| jetbrains.md | Modified | +4 / -1 | Formatting: `/ide` command separated into its own typed block |
| remote-control.md | Modified | +2 / -2 | Formatting: `/remote-control` command blocks retyped |
| changelog.md | Modified | +2 / -2 | GitHub star count (74.2k→74.3k) and PR count (254→255) updated |
| sandboxing.md | Modified | +1 / -1 | Formatting: `>` prefix removed from `/sandbox` command |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-06*
