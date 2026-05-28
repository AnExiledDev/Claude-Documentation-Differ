# Claude Code Documentation Changes — 2026-05-28

## Summary

Documentation was updated to reflect v2.1.153 and v2.1.152 releases. The most significant behavioral change is that `/model` now saves selections as the default for new sessions by default (reversing the v2.1.144 behavior), with a new `s` key for session-only switching and a keybinding rename from `modelPicker:setAsDefault` to `modelPicker:thisSessionOnly`. Two new built-in subagents (`claude-code-guide` and their `statusline-setup` companion) are now documented.

## Significant Changes

### Model Configuration

- **`/model` default behavior reversed in v2.1.153**: The `/model` command now saves the selected model as the default for new sessions by writing to user settings. The picker key for session-only switching changed from `d` to `s`.
  > "As of v2.1.153, `/model` saves your choice as the default for new sessions by writing the `model` field in your user settings. In the picker: `Enter`: switch model and save as your default; `s`: switch model for this session only."
  > "In v2.1.144 through v2.1.152, `/model` applied to the current session only and `d` in the picker saved a default."
  - *Implication*: Users upgrading from v2.1.144–v2.1.152 will find that `/model` selections now persist across sessions; use `s` to switch without persisting.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

- **`opus` alias now resolves to Opus 4.7 on Anthropic API**: The model alias resolution table was updated to reflect that on the Anthropic API and Claude Platform on AWS, `opus` resolves to Opus 4.7 and `sonnet` to Sonnet 4.6, while Bedrock/Vertex/Foundry remain on Opus 4.6 / Sonnet 4.5.
  > "On the Anthropic API and Claude Platform on AWS, `opus` resolves to Opus 4.7 and `sonnet` resolves to Sonnet 4.6. On Bedrock, Vertex, and Foundry, `opus` resolves to Opus 4.6 and `sonnet` resolves to Sonnet 4.5."
  - *Implication*: Anthropic API users relying on the `opus` alias will now get Opus 4.7. Pin with `ANTHROPIC_DEFAULT_OPUS_MODEL` to stay on a specific version.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

### Keybindings

- **`modelPicker:setAsDefault` renamed to `modelPicker:thisSessionOnly`**: The model picker keybinding action was renamed to reflect the inverted default behavior introduced in v2.1.153.
  > "If you customized the `modelPicker:setAsDefault` keybinding, rename it to `modelPicker:thisSessionOnly` in keybindings.json (the `d` action was replaced by `s`)"
  - *Implication*: **Breaking for keybindings customizers**: any `keybindings.json` entry that references `modelPicker:setAsDefault` must be updated to `modelPicker:thisSessionOnly`.
  - *Source*: [Customize keyboard shortcuts](https://code.claude.com/docs/en/keybindings.md)

### Agent View

- **PR column label clarification**: Documentation for the agent view PR column was updated to precisely describe singular vs. plural labeling behavior.
  > "The `PR #N` label … When a session has opened more than one pull request, the label shows a count instead, such as `3 PRs`, colored by the open pull request that most needs attention."
  - *Implication*: The label now actively signals review priority via color when multiple PRs are open; open the peek panel to see them all.
  - *Source*: [Manage multiple agents with agent view](https://code.claude.com/docs/en/agent-view.md)

### Sub-agents

- **New built-in subagents documented**: The sub-agents reference now includes an "Other" tab listing two additional helper agents that are invoked automatically and do not require direct use.
  > "Claude Code includes additional helper agents for specific tasks. These are typically invoked automatically, so you don't need to use them directly."

  | Agent | Model | When used |
  |---|---|---|
  | `statusline-setup` | Sonnet | When you run `/statusline` to configure your status line |
  | `claude-code-guide` | Haiku | When you ask questions about Claude Code features |

  - *Implication*: These agents consume quota like other subagents; `claude-code-guide` (Haiku) answers Claude Code how-to questions in-session.
  - *Source*: [Create custom subagents](https://code.claude.com/docs/en/sub-agents.md)

### Changelog (v2.1.153 and v2.1.152)

- **v2.1.153 (May 28, 2026)** release notes added, covering:
  - `skipLfs` option for `github`/`git` plugin marketplace sources
  - One-time npm global install notice + `/doctor` fix listing
  - Status line scripts now receive `COLUMNS` and `LINES` environment variables
  - `claude agents` dispatch autocomplete now includes native slash commands and bundled skills
  - `/model` saves as default; `s` key for session-only
  - `--strict-mcp-config` behavior fixed for inline `mcpServers` in agent definitions
  - Multiple Windows, background session, MCP, and rendering bug fixes
  - `[VSCode]` fix: Claude Code processes now shut down cleanly when VS Code closes on Windows
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **v2.1.152 (May 27, 2026)** release notes added, covering:
  - `/code-review --fix` applies findings to working tree; `/simplify` now invokes `/code-review --fix`
  - Skills and slash commands can set `disallowed-tools` in frontmatter
  - New `/reload-skills` command and `SessionStart` hook `reloadSkills: true` support
  - `SessionStart` hooks can set session title via `hookSpecificOutput.sessionTitle`
  - New `MessageDisplay` hook event to transform or hide assistant message text
  - `pluginSuggestionMarketplaces` managed setting for org marketplace suggestions
  - Fallback model now activates for the rest of the session (not per-request) when primary model is not found
  - Auto mode no longer requires opt-in consent
  - Vim mode: `/` in NORMAL mode opens reverse history search
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

## Minor Changes

- **[commands.md](https://code.claude.com/docs/en/commands.md)**: Minor update to the commands reference (+1/-1 lines), likely reflecting `/model` behavior or `/code-review` rename from `/simplify`.

- **[env-vars.md](https://code.claude.com/docs/en/env-vars.md)**: Single-line update to the environment variables reference (+1/-1 lines).

- **[monitoring-usage.md](https://code.claude.com/docs/en/monitoring-usage.md)**: One line added (+1/-0); likely documents the new `OTEL_METRICS_INCLUDE_ENTRYPOINT=true` opt-in added in v2.1.152 (session entrypoint as an OTel metric attribute).

- **[settings.md](https://code.claude.com/docs/en/settings.md)**: Two lines added (+2/-0); likely documents the new `pluginSuggestionMarketplaces` managed setting introduced in v2.1.152.

- **[setup.md](https://code.claude.com/docs/en/setup.md)**: Four lines added (+4/-0); minor additions to system requirements or installation instructions.

- **[statusline.md](https://code.claude.com/docs/en/statusline.md)**: Four lines added (+4/-0); documents that status line command scripts now receive `COLUMNS` and `LINES` environment variables (introduced in v2.1.153) so scripts can size output to terminal width.

## Migration Notes

- **`modelPicker:setAsDefault` keybinding rename**: If you have a custom `keybindings.json` entry for `modelPicker:setAsDefault`, rename it to `modelPicker:thisSessionOnly`. The underlying behavior also changed: `Enter` in the model picker now saves the default, while `s` switches for the current session only.

- **`/model` persistence change**: Starting in v2.1.153, selecting a model via `/model` persists it as the default for future sessions. If you previously used `/model` to temporarily switch models, use `s` in the picker or the `--model` flag to keep changes session-local.

## Notable Details

- The v2.1.153 changelog note about `--strict-mcp-config` is worth reading carefully: it no longer strips inline `mcpServers` from explicitly-passed agent definitions (`--agents` / SDK `agents`), and blocked subagent MCP servers now surface a visible warning rather than silently failing.
- The `Agent` tool with `subagent_type: 'claude'` was previously (and incorrectly) running in an undocumented temporary worktree, which could silently discard outputs written to gitignored paths. This is fixed in v2.1.153.
- v2.1.152 introduced `MessageDisplay` hooks — a new hook event class that lets hooks transform or suppress assistant message text at display time, distinct from modifying tool behavior.
- The `claude-code-guide` built-in subagent (Haiku model) answers in-session questions about Claude Code features; its presence in the documented agent list clarifies why Haiku requests appear in telemetry for feature-help queries.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| changelog.md | Modified | SIGNIFICANT | +39/-0 | Added v2.1.153 and v2.1.152 release notes plus earlier versions |
| agent-view.md | Modified | SIGNIFICANT | +10/-10 | Updated PR column label description and related agent view behavior |
| model-config.md | Modified | SIGNIFICANT | +10/-3 | `/model` now saves default; `s` key for session-only; Opus 4.7 alias update |
| keybindings.md | Modified | SIGNIFICANT | +5/-5 | Renamed `modelPicker:setAsDefault` → `modelPicker:thisSessionOnly` |
| sub-agents.md | Modified | SIGNIFICANT | +10/-0 | Added "Other" built-in subagents tab (statusline-setup, claude-code-guide) |
| setup.md | Modified | MINOR | +4/-0 | Minor additions to system requirements or install docs |
| statusline.md | Modified | MINOR | +4/-0 | Documents COLUMNS/LINES env vars passed to status line scripts |
| settings.md | Modified | MINOR | +2/-0 | Minor additions, likely pluginSuggestionMarketplaces managed setting |
| monitoring-usage.md | Modified | MINOR | +1/-0 | Minor addition, likely OTEL_METRICS_INCLUDE_ENTRYPOINT documentation |
| commands.md | Modified | MINOR | +1/-1 | Minor update to commands reference |
| env-vars.md | Modified | MINOR | +1/-1 | Minor update to environment variables reference |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-28*
