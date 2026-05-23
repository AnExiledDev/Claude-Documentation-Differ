# Claude Code Documentation Changes — 2026-05-23

## Summary

One page was updated: the Claude Code changelog received version **2.1.149** (released May 22, 2026), adding 29 lines. The release includes 4 new features/enhancements, 4 security/permission-related bug fixes, and 17 additional bug fixes and UX improvements.

## Significant Changes

### Features

- **`/usage` per-category breakdown**: The `/usage` command now displays a detailed breakdown of limit consumption by category — skills, subagents, plugins, and per-MCP-server cost.
  > `/usage` now shows a per-category breakdown of what's driving your limits usage — skills, subagents, plugins, and per-MCP-server cost
  - *Implication*: Users can now identify exactly which category is driving them toward their usage limits, useful for optimizing high-cost workflows.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/diff` keyboard scrolling**: The `/diff` detail view now supports full keyboard navigation.
  > `/diff` detail view can now be scrolled with the keyboard (arrows, `j`/`k`, `PgUp`/`PgDn`, `Space`, `Home`/`End`)
  - *Implication*: Keyboard-driven workflows no longer require mouse interaction to review diff details.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **GFM task list checkbox rendering**: Markdown output now renders GitHub-Flavored Markdown task list syntax as visual checkboxes.
  > Markdown output now renders GFM task list checkboxes (`- [ ] todo` / `- [x] done`) instead of plain bullets
  - *Implication*: Task lists in AI responses and documents are now visually distinct and easier to parse at a glance.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Enterprise: `allowAllClaudeAiMcps` managed setting**: A new enterprise managed setting allows loading all claude.ai cloud MCP connectors in addition to those defined in `managed-mcp.json`.
  > Enterprise: added the `allowAllClaudeAiMcps` managed setting to load claude.ai cloud MCP connectors alongside `managed-mcp.json`
  - *Implication*: Enterprise admins can now grant access to the full suite of claude.ai MCP connectors without enumerating them individually in `managed-mcp.json`.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Security & Permission Fixes

- **PowerShell `cd` permission bypass fixed**: Built-in PowerShell `cd` shorthand functions (`cd..`, `cd\`, `cd~`, `X:`) were silently changing the working directory without triggering permission checks, potentially allowing reads outside the workspace.
  > Fixed a PowerShell permission bypass: built-in `cd` functions (`cd..`, `cd\`, `cd~`, `X:`) changed the working directory undetected, letting a later command read outside the workspace
  - *Implication*: This was a meaningful sandbox escape vector; the fix ensures directory changes via shorthand are tracked the same as explicit `cd` calls.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Git worktree sandbox write allowlist scoped correctly**: The sandbox write allowlist in git worktrees was incorrectly covering the entire main repository root instead of only the shared `.git` directory.
  > Fixed the sandbox write allowlist in git worktrees covering the entire main repository root instead of only the shared `.git` directory (with `hooks/` and `config` denied)
  - *Implication*: Git worktree-based workflows now have tighter sandbox boundaries; `hooks/` and `config` within `.git` are explicitly denied.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **PowerShell prefix/wildcard allow rules fixed**: Allow rules using prefixes or wildcards (e.g., `PowerShell(dotnet.exe build *)`) were not correctly pre-approving native executables and scripts.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`PWD`/`OLDPWD`/`DIRSTACK` stale variable tracking fixed**: The permission parser was trusting stale variable values for these directory-tracking shell variables across `cd`/`pushd`/`popd` calls.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

## Minor Changes

- **changelog.md**: Version 2.1.149 entry added with 25 additional bug fixes and UX improvements including: macOS crash fix for `find` in large directory trees, `/ultraplan` remote session fix, `otelHeadersHelper` space-in-path fix (now reported in `/doctor`), Ctrl+O transcript view tailing fix, `/config` phantom-change fix, `/insights` crash fix, Remote Control session rename sync fix, and `/feedback` pre-compaction conversation inclusion. (+29/-0 lines)

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| changelog.md | Modified | SIGNIFICANT | +29/-0 | Version 2.1.149 release notes: 4 features, 4 security fixes, 17 bug/UX fixes |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-23*
