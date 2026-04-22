# Claude Code Documentation Changes — 2026-04-22

## Summary

This update documents v2.1.117 (released April 22, 2026) alongside significant documentation additions: a new dedicated configuration debugging guide, a new `UserPromptExpansion` hook event, expanded OpenTelemetry traces documentation, cross-marketplace plugin dependency support, and the WebFetch domain safety check disclosure. 25 pages were modified and one new page was added.

## Significant Changes

### Hooks

- **New `UserPromptExpansion` hook event**: Added a new hook lifecycle event that fires when a user-typed slash command expands into a prompt before it reaches Claude. The hook can block the expansion, inject context, or log which commands users invoke.
  > `UserPromptExpansion` fires on that direct path. This event covers the path `PreToolUse` does not: a `PreToolUse` hook matching the `Skill` tool fires only when Claude calls the tool, but typing `/skillname` directly bypasses `PreToolUse`.
  - *Implication*: Enables enforcement of slash-command policies that were previously unenforced — for example, blocking `/deploy` unless an approval file exists, without relying on `PreToolUse`.
  - Matcher: filters on `command_name`; leave empty to catch every prompt-type slash command.
  - Input fields: `expansion_type` (`slash_command` or `mcp_prompt`), `command_name`, `command_args`, `command_source`, original `prompt` string.
  - Decision control: returns top-level `decision: "block"`, `reason`, or `additionalContext`.
  - Exit code 2 blocks the expansion; exit 0 allows it and passes stdout to Claude as context.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **`CwdChanged` and `FileChanged` hooks no longer restricted to `command` type**: The documentation previously stated "Only `type: \"command\"` hooks are supported" for these events. That restriction has been removed, implying `http`, `prompt`, and `agent` hook types are now also supported.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

### Configuration Debugging

- **New `debug-your-config` guide**: A dedicated troubleshooting page for configuration problems (CLAUDE.md not loading, hooks not firing, MCP servers not connecting, etc.) has been extracted from the `.claude` directory reference into its own page.
  > When Claude ignores an instruction or a feature you configured doesn't appear, the cause is usually that the file didn't load, it loaded from a different location than you expected, or another file overrode it.
  - Covers: `/context`, `/memory`, `/skills`, `/agents`, `/hooks`, `/mcp`, `/permissions`, `/doctor`, `/status`
  - Includes a symptom → cause → fix lookup table covering 14 common scenarios including hook matcher errors, MCP approval dismissal, and `~/.claude.json` vs `~/.claude/settings.json` confusion.
  - The equivalent content has been removed from `claude-directory.md` and replaced with a link to this new page.
  - *Source*: [Debug your configuration](https://code.claude.com/docs/en/debug-your-config.md)

### Monitoring / OpenTelemetry

- **Expanded traces (beta) documentation — span hierarchy and attributes**: The monitoring page gained comprehensive reference tables for every span type in the distributed tracing system.
  > Each user prompt starts a `claude_code.interaction` root span. API calls, tool calls, and hook executions are recorded as its children. Tool spans have two child spans of their own: one for the time spent waiting on a permission decision and one for the execution itself.
  - Span types documented: `claude_code.interaction`, `claude_code.llm_request`, `claude_code.tool`, `claude_code.tool.blocked_on_user`, `claude_code.tool.execution`, `claude_code.hook`
  - The `claude_code.hook` span requires additional flags (`ENABLE_BETA_TRACING_DETAILED=1`, `BETA_TRACING_ENDPOINT`) and is gated for interactive CLI sessions but ungated for Agent SDK / `-p` sessions.
  - *Source*: [Monitoring](https://code.claude.com/docs/en/monitoring-usage.md)

- **New OTel event types documented**: Ten new event sections added covering permission mode changes, auth events, MCP server connections, internal errors, API retries exhausted, hook execution start/complete, and compaction events.
  - *Source*: [Monitoring](https://code.claude.com/docs/en/monitoring-usage.md)

- **`OTEL_LOG_RAW_API_BODIES` now accepts `file:<dir>` mode**: The environment variable description was updated to document a new value format.
  > Set to `1` for inline bodies truncated at 60 KB, or `file:<dir>` to write untruncated bodies to disk and emit a `body_ref` path instead.
  - *Implication*: Enterprise users needing full (untruncated) API request/response bodies for audit purposes can now write them to disk, avoiding the 60 KB inline truncation.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **`OTEL_LOG_TOOL_DETAILS` now explicitly covers raw error strings**: The description was updated to include "raw error strings on tool failures" among the data gated by this flag.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

### New Environment Variable

- **`CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT`**: New env var that applies the minimal system prompt and collapsed tool descriptions from simple mode (`CLAUDE_CODE_SIMPLE`) without disabling the full tool set, hooks, MCP servers, or CLAUDE.md discovery.
  > Set to `1` to use the minimal system prompt and collapsed tool descriptions from `CLAUDE_CODE_SIMPLE` without the other simple-mode changes. The full tool set, hooks, MCP servers, and CLAUDE.md discovery remain enabled.
  - *Implication*: Useful for reducing system prompt token consumption without sacrificing agent capabilities — a middle ground between bare mode and full mode.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

### Data Usage

- **WebFetch domain safety check documented**: A new section explains that the WebFetch tool performs a hostname pre-flight check against Anthropic's safety blocklist before each fetch, regardless of which model provider is in use.
  > Before fetching a URL, the WebFetch tool sends the requested hostname to `api.anthropic.com` to check it against a safety blocklist maintained by Anthropic. Only the hostname is sent, not the full URL, path, or page contents.
  - The check runs even when `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` is set; it has its own opt-out: `skipWebFetchPreflight: true` in settings.
  - Added to the "Default behaviors by API provider" table as a row that is on-by-default across all providers.
  - *Implication*: Organizations with network policies blocking `api.anthropic.com` will find WebFetch requests fail unless they allowlist the domain or disable the preflight. Consider pairing `skipWebFetchPreflight: true` with `WebFetch` permission rules.
  - *Source*: [Data usage](https://code.claude.com/docs/en/data-usage.md)

### Plugins

- **Cross-marketplace plugin dependencies**: Plugin authors can now declare a dependency that lives in a different marketplace by specifying a `marketplace` field in the dependency object.
  > By default, Claude Code refuses to auto-install a dependency that lives in a different marketplace than the plugin declaring it. To allow it, the maintainer of the root marketplace adds the target marketplace name to `allowCrossMarketplaceDependenciesOn` in `marketplace.json`.
  - The allowlist is one-directional: only the root marketplace's list is consulted; trust does not chain through intermediate marketplaces.
  - *Source*: [Constrain plugin dependency versions](https://code.claude.com/docs/en/plugin-dependencies.md)

- **Plugin marketplace `Optional fields` section renamed**: The section previously called "Optional metadata" is now "Optional fields" in the marketplace reference. Content appears equivalent; this is a structural rename.
  - *Source*: [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

### Troubleshooting

- **Version check URL updated from Google Cloud Storage to Anthropic's domain**: The error section previously titled `` `Failed to fetch version from storage.googleapis.com` `` is now titled `` `Failed to fetch version from downloads.claude.ai` ``. The installer now downloads from `downloads.claude.ai` rather than Google Cloud Storage.
  - The troubleshooting steps for checking network connectivity also update the `curl` verification command to target `downloads.claude.ai`.
  - *Implication*: Organizations with allow-lists for Claude Code downloads need to permit `downloads.claude.ai` instead of (or in addition to) `storage.googleapis.com`.
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

### MCP

- **Connector configuration URL updated**: The URL for configuring cloud MCP servers in Claude.ai has changed from `claude.ai/settings/connectors` to `claude.ai/customize/connectors`.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

### Release Notes (v2.1.117 — April 22, 2026)

The changelog page gained the v2.1.117 entry. Notable items from the release:

- **Native binary on macOS/Linux**: `Glob` and `Grep` tools replaced by embedded `bfs` and `ugrep` via the Bash tool — faster searches without a separate tool round-trip (Windows and npm builds unchanged)
- **Default effort bumped to `high` for Pro/Max on Opus 4.6 and Sonnet 4.6** (was `medium`)
- **Forked subagents enabled externally** via `CLAUDE_CODE_FORK_SUBAGENT=1`
- **Agent frontmatter `mcpServers` now loaded** for main-thread `--agent` sessions
- **OTel additions**: `user_prompt` events include `command_name` and `command_source` for slash commands; cost/token/API events include `effort` attribute; custom/MCP command names redacted unless `OTEL_LOG_TOOL_DETAILS=1`
- **`/model` persistence**: selections now persist across restarts even when the project pins a different model
- **Plugin install improvements**: reinstalling an already-installed plugin now resolves missing dependencies; dependency errors include install hints; `blockedMarketplaces` and `strictKnownMarketplaces` enforced on all install operations
- **Opus 4.7 context window fix**: `/context` percentages were inflated because Claude Code computed against a 200K window instead of Opus 4.7's native 1M
- *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

## Notable Details

- **Interactive mode task list reduced to 5**: The task list display was cut from "up to 10 tasks at a time" to "up to 5 tasks at a time" in the interactive mode docs.
- **Session recap docs simplified**: The mention of `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` env var override was removed from the interactive mode documentation on session recaps.
- **Quickstart streamlined**: The quickstart page had 113 lines removed (net -112 lines). The interactive install configurator component remains; the removed content was likely duplicated prose now residing elsewhere.
- **`/resume` behavior for stale sessions**: v2.1.117 adds an offer to summarize stale, large sessions before re-reading them, matching `--resume` behavior. The changelog is the primary source; no docs page was added yet.
- **`cleanupPeriodDays` scope expanded**: Now also sweeps `~/.claude/tasks/`, `~/.claude/shell-snapshots/`, and `~/.claude/backups/` in addition to existing paths.

## New Pages

- **[debug-your-config.md](https://code.claude.com/docs/en/debug-your-config.md)** — Dedicated guide for diagnosing configuration problems: why CLAUDE.md, settings, hooks, MCP servers, or skills aren't taking effect. Covers inspection commands (`/context`, `/memory`, `/hooks`, `/mcp`, `/doctor`, `/status`) and a 14-row symptom → cause → fix table. Replaces the troubleshooting content previously embedded in `claude-directory.md`.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| debug-your-config.md | New | +96 | New configuration debugging guide |
| monitoring-usage.md | Modified | +305/-38 | Span hierarchy, span attributes, 10 new event type sections for traces beta |
| hooks.md | Modified | +125/-73 | New `UserPromptExpansion` event with full input/output schema; CwdChanged/FileChanged hook type restriction removed |
| quickstart.md | Modified | +1/-113 | Significant content reduction; install configurator retained |
| plugins-reference.md | Modified | +59/-33 | Updated hook event tables and component path documentation |
| hooks-guide.md | Modified | +31/-29 | `UserPromptExpansion` added to event table and matcher reference |
| plugin-dependencies.md | Modified | +33/-6 | New "Depend on a plugin from another marketplace" section with `allowCrossMarketplaceDependenciesOn` |
| changelog.md | Modified | +31/-0 | v2.1.117 release notes added |
| claude-directory.md | Modified | +1/-35 | Troubleshooting table and "Check what loaded" section removed; replaced with link to new debug guide |
| data-usage.md | Modified | +15/-8 | WebFetch domain safety check disclosed; new table row and dedicated section added |
| troubleshooting.md | Modified | +9/-9 | Download server updated from `storage.googleapis.com` to `downloads.claude.ai` |
| plugin-marketplaces.md | Modified | +8/-7 | "Optional metadata" section renamed to "Optional fields" |
| settings.md | Modified | +6/-4 | Minor updates |
| permissions.md | Modified | +5/-3 | Minor updates |
| skills.md | Modified | +5/-2 | Minor updates |
| network-config.md | Modified | +5/-3 | Minor updates |
| env-vars.md | Modified | +3/-2 | New `CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT`; updated `OTEL_LOG_RAW_API_BODIES` and `OTEL_LOG_TOOL_DETAILS` descriptions |
| sub-agents.md | Modified | +4/-2 | Minor updates |
| interactive-mode.md | Modified | +2/-2 | Task list display reduced to 5; recap env var reference removed |
| sandboxing.md | Modified | +2/-2 | Minor updates |
| overview.md | Modified | +1/-8 | Net reduction; minor structural change |
| memory.md | Modified | +1/-0 | Added link to new debug-your-config guide |
| common-workflows.md | Modified | +1/-1 | Thinking spinner description updated to "inline progress hints" |
| mcp.md | Modified | +1/-1 | Connector URL updated from `/settings/connectors` to `/customize/connectors` |
| setup.md | Modified | +1/-1 | Minor update |
| terminal-config.md | Modified | +1/-1 | Minor update |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-22*
