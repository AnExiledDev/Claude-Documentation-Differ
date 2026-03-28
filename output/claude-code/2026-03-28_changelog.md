# Claude Code Documentation Changes — 2026-03-28

## Summary

Four pages were updated, driven primarily by the v2.1.86 release (March 27, 2026). The release adds a new `--tmux` CLI flag, moves `teammateMode` from project settings to global config, and documents a large batch of bug fixes and performance improvements.

## Significant Changes

### Features

- **New `--tmux` CLI flag**: A new flag `--tmux` has been added, requiring `--worktree`, that creates a tmux session for the isolated worktree. Supports iTerm2 native panes by default or traditional tmux via `--tmux=classic`.
  > `--tmux` — Create a tmux session for the worktree. Requires `--worktree`. Uses iTerm2 native panes when available; pass `--tmux=classic` for traditional tmux
  - *Implication*: Developers using worktrees for parallel sessions can now launch directly into a tmux/iTerm2 split in a single command, e.g. `claude -w feature-auth --tmux`.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **Session ID header for API proxies**: v2.1.86 adds `X-Claude-Code-Session-Id` to all outbound API requests.
  > Added `X-Claude-Code-Session-Id` header to API requests so proxies can aggregate requests by session without parsing the body
  - *Implication*: Proxy and gateway operators can now group and trace all requests belonging to a single Claude Code session using this header, without body inspection.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **VCS directory exclusions extended**: `.jj` (Jujutsu) and `.sl` (Sapling) metadata directories added to exclusion lists.
  > Added `.jj` and `.sl` to VCS directory exclusion lists so Grep and file autocomplete don't descend into Jujutsu or Sapling metadata
  - *Implication*: Users of alternative VCS tools will no longer see noise from metadata directories in search results or file autocomplete.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Read tool compaction**: The Read tool now uses a compact line-number format and deduplicates unchanged re-reads.
  > Read tool now uses compact line-number format and deduplicates unchanged re-reads, reducing token usage
  - *Implication*: Measurable token savings in sessions that read files multiple times; particularly beneficial in long agentic runs.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Reduced token overhead for `@`-file mentions**: Raw file content is no longer JSON-escaped when mentioned with `@`.
  > Reduced token overhead when mentioning files with `@` — raw string content no longer JSON-escaped
  - *Implication*: Smaller context window consumption per `@`-mention, especially noticeable with large files.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Prompt cache hit rate improvement for hosted providers**: Dynamic content removed from tool descriptions for Bedrock, Vertex, and Foundry.
  > Improved prompt cache hit rate for Bedrock, Vertex, and Foundry users by removing dynamic content from tool descriptions
  - *Implication*: Users on Bedrock, Vertex, or Foundry should see improved cache utilization and potentially reduced costs.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Configuration

- **`teammateMode` moved to global config**: The `teammateMode` setting has been relocated from the project settings table to the **Global config settings** table (stored in `~/.claude.json`, not `settings.json`). The anchor link for how to configure it also changed from `#set-up-agent-teams` to `#choose-a-display-mode`.
  > These settings are stored in `~/.claude.json` rather than `settings.json`. Adding them to `settings.json` will trigger a schema validation error.
  - *Implication*: If `teammateMode` was previously set in `settings.json`, it will now trigger a schema validation error. It must be moved to `~/.claude.json`.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **Agent teams doc link updated**: The agent-teams page now directs users to configure `teammateMode` in their **global config** at `~/.claude.json` via a more specific anchor (`#global-config-settings`), replacing the previously generic link to `/en/settings`.
  > To override, set `teammateMode` in your [global config](/en/settings#global-config-settings) at `~/.claude.json`
  - *Implication*: Clarifies the exact config file and location, reducing misconfiguration risk.
  - *Source*: [Agent Teams](https://code.claude.com/docs/en/agent-teams.md)

### Bug Fixes (v2.1.86)

Notable fixes documented in the changelog:

- **`--resume` regression fixed**: Sessions created before v2.1.85 were failing with `"tool_use ids were found without tool_result blocks"`.
- **File access outside project root**: Write/Edit/Read failing on files like `~/.claude/CLAUDE.md` when conditional skills or rules were configured.
- **Windows config corruption**: Unnecessary config disk writes on every skill invocation caused performance issues and corruption on Windows.
- **Memory crash on `/feedback`**: Potential OOM crash on very long sessions with large transcript files.
- **`--bare` mode MCP tools**: `--bare` mode was dropping MCP tools in interactive sessions and silently discarding enqueued mid-turn messages.
- **OAuth URL copy**: The `c` shortcut was copying only ~20 characters of the OAuth login URL instead of the full URL.
- **Masked input token leak**: OAuth code paste was leaking the start of the token when wrapping across narrow terminals.
- **Marketplace plugin permissions**: Official marketplace plugin scripts were failing with "Permission denied" on macOS/Linux since v2.1.83.
- **Multi-instance model statusline**: Statusline was showing another session's model when running multiple Claude Code instances and using `/model` in one.
- **`/plugin` uninstall dialog**: Pressing `n` now correctly uninstalls while preserving the data directory (previously inverted).
- **`ultrathink` hint linger**: Hint was not cleared after deleting the keyword.
- **Memory growth in long sessions**: Markdown/highlight render caches were retaining full content strings.
- **macOS keychain stalls**: Startup event-loop stalls reduced by extending keychain cache from 5s to 30s when many claude.ai MCP connectors are configured.
- **[VSCode] "Not responding" false positive**: Extension was incorrectly showing "Not responding" during long-running operations.
- **[VSCode] Max plan model reset**: Extension was defaulting Max plan users back to Sonnet after OAuth token refresh (8 hours post-login).

### UI/UX Changes (v2.1.86)

- **Memory filenames now interactive**: Filenames in the "Saved N memories" notice now highlight on hover and open on click.
- **`/skills` listing capped at 250 chars**: Skill descriptions are truncated in the listing to reduce context usage.
- **`/skills` sorted alphabetically**: The skills menu now sorts entries alphabetically for easier scanning.
- **Auto mode plan message updated**: "temporarily unavailable" is now "unavailable for your plan" when disabled by plan restrictions.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +29/−0 | Added v2.1.86 release entry (March 27, 2026) |
| settings.md | Modified | +8/−8 | Moved `teammateMode` from project settings to global config table; updated section anchor |
| cli-reference.md | Modified | +1/−0 | Added `--tmux` flag (requires `--worktree`) |
| agent-teams.md | Modified | +1/−1 | Updated `teammateMode` config link to `#global-config-settings` at `~/.claude.json` |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-28*
