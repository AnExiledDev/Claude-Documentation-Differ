# Claude Code Documentation Changes — 2026-04-03

## Summary

13 pages were modified across this update. The most significant changes document `CLAUDE.local.md` as a new first-class memory scope for personal, unversioned project instructions, and add a new mechanism for MCP server authors to override per-tool result size limits. Computer use documentation was updated throughout to reflect Windows support in the Desktop app.

## Significant Changes

### Memory / CLAUDE.md

- **New `CLAUDE.local.md` scope**: A new local memory file type has been added, sitting alongside `CLAUDE.md` at the project root for personal, gitignored project-specific instructions. The settings scopes table, memory reference table, and `/memory` command documentation all reflect this addition.
  > "Local instructions — `./CLAUDE.local.md` — Personal project-specific preferences; add to `.gitignore` — Your sandbox URLs, preferred test data — Just you (current project)"
  - *Implication*: Developers can now store personal project preferences (e.g., local URLs, preferred test fixtures) without polluting the shared `CLAUDE.md`. Running `/init` and choosing the personal option automatically gitignores the file.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

- **Load order clarified**: `CLAUDE.local.md` is appended after `CLAUDE.md` within each directory, so personal notes take precedence when instructions conflict.
  > "All discovered files are concatenated into context rather than overriding each other. Within each directory, `CLAUDE.local.md` is appended after `CLAUDE.md`, so when instructions conflict, your personal notes are the last thing Claude reads at that level."
  - *Implication*: Predictable override behavior — personal local files always win at the same directory level.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

- **`CLAUDE.local.md` not loaded from additional directories**: Files in directories added via `--add-dir` / `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` are excluded from local file loading.
  > "`CLAUDE.local.md` files in additional directories are not loaded."
  - *Implication*: Avoids unintentionally pulling in personal notes from shared or auxiliary config directories.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

- **Settings scopes table updated**: `CLAUDE.md` row now shows `CLAUDE.local.md` as the local scope.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **Best practices updated**: `CLAUDE.local.md` is now listed as a distinct location alongside `CLAUDE.md` files.
  > "**Project root (`./CLAUDE.local.md`)**: personal project-specific notes; add this file to your `.gitignore` so it isn't shared with your team"
  - *Source*: [Best Practices](https://code.claude.com/docs/en/best-practices.md)

- **Desktop docs updated**: The shared-config section now mentions both `CLAUDE.md` and `CLAUDE.local.md`.
  > "**CLAUDE.md** and `CLAUDE.local.md` files in your project are used by both"
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

### MCP

- **Per-tool result size override**: MCP server authors can now annotate individual tools with `_meta["anthropic/maxResultSizeChars"]` in the `tools/list` response to allow results larger than the default limit, up to a hard ceiling of 500,000 characters. This replaces the previous section titled "Set a higher limit for MCP tool outputs" with a more structured "Override result size per tool" subsection.
  > "If you're building an MCP server, you can allow individual tools to return results larger than the default limit by setting `_meta["anthropic/maxResultSizeChars"]` in the tool's `tools/list` response entry. Claude Code uses this value as the maximum result size for that tool, up to a hard ceiling of 500,000 characters."
  - *Implication*: Useful for tools that return inherently large outputs such as database schemas or full file trees. Without this annotation, oversized results are persisted to disk and replaced with a file reference in the conversation.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

### Computer Use

- **Windows support in Desktop**: Computer use in the Desktop app now supports Windows in addition to macOS. Multiple places in the docs were updated to reflect this.
  > "Computer use is a research preview on macOS and Windows that requires a Pro or Max plan."
  - *Implication*: Windows users on Pro or Max plans can now use computer use via the Desktop app. The CLI remains macOS-only for computer use.
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

- **Windows-specific setup instructions added**: The enable flow now distinguishes macOS (requires Accessibility + Screen Recording permissions) from Windows (toggle takes effect immediately, no extra permissions needed).
  > "On Windows, the toggle takes effect immediately and setup is complete. On macOS, continue to the next step."
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

- **CLI computer use page updated**: Clarified that the CLI surface is macOS-only, and directs Windows users to the Desktop app.
  > "You're on macOS. Computer use in the CLI is not available on Linux or Windows. On Windows, use computer use in Desktop instead."
  - *Source*: [Computer Use](https://code.claude.com/docs/en/computer-use.md)

### Plugins

- **`bin/` directory added as a plugin component**: Plugins can now ship executables under a `bin/` directory. These executables are added to the Bash tool's `PATH` and are invokable as bare commands while the plugin is enabled.
  > "Executables — `bin/` — Executables added to the Bash tool's `PATH`. Files here are invokable as bare commands in any Bash tool call while the plugin is enabled"
  - *Implication*: Plugin authors can bundle custom CLI tools alongside their plugin without requiring separate installation or absolute paths.
  - *Source*: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md), [Plugins](https://code.claude.com/docs/en/plugins.md)

### Permissions / Sandboxing

- **Auto-allow mode behavior clarified**: The description of sandbox auto-allow mode now explicitly states that `ask` rules only apply to commands that fall back to the regular permission flow, not to sandboxed commands.
  > "Explicit deny rules are always respected. Ask rules apply only to commands that fall back to the regular permission flow."
  - *Implication*: Developers relying on `ask: Bash(*)` rules should be aware those prompts are suppressed for sandboxed commands when `autoAllowBashIfSandboxed: true` (the default).
  - *Source*: [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)

- **`autoAllowBashIfSandboxed` behavior documented in permissions**: Added a note that when sandboxing is enabled with `autoAllowBashIfSandboxed: true`, sandboxed Bash commands bypass per-command prompts even when `ask: Bash(*)` is set.
  > "When sandboxing is enabled with `autoAllowBashIfSandboxed: true`, which is the default, sandboxed Bash commands run without prompting even if your permissions include `ask: Bash(*)`. The sandbox boundary substitutes for the per-command prompt."
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

### Settings

- **`disableDeepLinkRegistration` updated**: The `q` parameter of `claude-cli://open?q=` deep links now supports multi-line prompts using URL-encoded newlines (`%0A`).
  > "The `q` parameter supports multi-line prompts using URL-encoded newlines (`%0A`)."
  - *Implication*: External tools can now pass multi-line prompts via deep links.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Changelog (v2.1.91)

- Version 2.1.91 was added to the official changelog, dated April 2, 2026. Key items:
  - MCP tool result persistence override via `_meta["anthropic/maxResultSizeChars"]` (up to 500K)
  - New `disableSkillShellExecution` setting to disable inline shell execution in skills, custom slash commands, and plugin commands
  - Multi-line prompts now supported in `claude-cli://open?q=` deep links
  - Plugins can ship executables under `bin/` invokable as bare commands from the Bash tool
  - Fixed transcript chain breaks on `--resume` that could lose conversation history
  - Fixed `cmd+delete` not deleting to start of line on iTerm2, kitty, WezTerm, Ghostty, and Windows Terminal
  - Fixed plan mode in remote sessions losing track of the plan file after a container restart
  - Fixed JSON schema validation for `permissions.defaultMode: "auto"` in settings.json
  - Edit tool now uses shorter `old_string` anchors, reducing output tokens
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

## New Pages

None.

## Removed Pages

None.

## Notable Details

- The `platforms.md` comparison table now specifies that CLI computer use requires macOS (Pro and Max), distinguishing it from the Desktop app which supports both macOS and Windows.
- The `sandboxing.md` page removed the macOS qualifier from the computer use boundary description, reflecting the new cross-platform scope.
- The `desktop.md` app permission warning now uses platform-neutral language: "terminals, Finder or File Explorer, and System Settings or Settings" instead of macOS-specific app names.
- The Amazon Bedrock resources section gained a link to the [Bedrock token burndown and quotas](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-token-burndown.html) page.
- The worktree-aware guidance for `CLAUDE.local.md` notes that a gitignored file only exists in the worktree where it was created; to share personal instructions across worktrees, importing from `~/.claude/CLAUDE.md` is recommended instead.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `memory.md` | Modified | +18 / -11 | Added `CLAUDE.local.md` scope, updated load order explanation, `/memory` command, and debug tips |
| `mcp.md` | Modified | +17 / -2 | Added per-tool result size override via `_meta["anthropic/maxResultSizeChars"]`; restructured section |
| `desktop.md` | Modified | +11 / -11 | Extended computer use to Windows; updated setup steps and app permission language |
| `plugins-reference.md` | Modified | +15 / -12 | Added `bin/` directory as a plugin component for bundled executables |
| `changelog.md` | Modified | +16 / -0 | Added v2.1.91 release entry |
| `computer-use.md` | Modified | +4 / -3 | Clarified CLI is macOS-only; directs Windows users to Desktop; updated comparison table |
| `permissions.md` | Modified | +2 / -0 | Documented `autoAllowBashIfSandboxed` interaction with `ask` rules |
| `sandboxing.md` | Modified | +2 / -2 | Clarified `ask` rule behavior in auto-allow sandbox mode; removed macOS qualifier from computer use |
| `settings.md` | Modified | +2 / -2 | Added `CLAUDE.local.md` to scopes table; noted multi-line deep link support |
| `best-practices.md` | Modified | +1 / -0 | Added `CLAUDE.local.md` to list of CLAUDE.md file locations |
| `plugins.md` | Modified | +1 / -0 | Added `bin/` directory to plugin component table |
| `platforms.md` | Modified | +1 / -1 | Specified CLI computer use is macOS-only in the platform comparison table |
| `amazon-bedrock.md` | Modified | +1 / -0 | Added link to Bedrock token burndown and quotas documentation |
