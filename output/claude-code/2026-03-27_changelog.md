# Claude Code Documentation Changes — 2026-03-27

## Summary

This update adds a new interactive `.claude` directory explorer page, documents the `2.1.85` release with 25+ fixes and improvements, expands the Code Review page with a new "Check run output" section, and clarifies that `OTEL_LOG_TOOL_DETAILS=1` is now required to emit `tool_parameters` for all tool types (including Bash) in OpenTelemetry `tool_result` events.

## Significant Changes

### Features

- **Code Review: Check run output section**: A new `### Check run output` section documents the **Claude Code Review** check run that appears alongside CI checks on GitHub PRs. It describes the structured findings summary, per-line annotations in the Files changed tab, and a machine-readable severity footer that CI workflows can parse to gate merges.
  > "The check run always completes with a neutral conclusion so it never blocks merging through branch protection rules. If you want to gate merges on Code Review findings, read the severity breakdown from the check run output in your own CI. The last line of the Details text is a machine-readable comment your workflow can parse with `gh` and jq:"
  > ```bash
  > gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID \
  >   --jq '.output.text | split("bughunter-severity: ")[1] | split(" -->")[0] | fromjson'
  > ```
  - *Implication*: Teams that want to enforce merge gates based on Code Review severity can now do so by parsing the `bughunter-severity` JSON object. The `normal` key holds the count of Important (red) findings; a non-zero value signals a bug worth fixing before merge.
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

- **v2.1.85 release notes added**: The changelog page received 33 new lines covering the March 26, 2026 release. Key items include:
  - `CLAUDE_CODE_MCP_SERVER_NAME` and `CLAUDE_CODE_MCP_SERVER_URL` env vars in MCP `headersHelper` scripts, enabling one helper to serve multiple servers
  - Conditional `if` field for hooks using permission rule syntax (e.g., `Bash(git *)`) to filter when hooks run, reducing process spawning overhead
  - Timestamp markers in transcripts when scheduled tasks (`/loop`, `CronCreate`) fire
  - Deep link queries (`claude-cli://open?q=…`) now support up to 5,000 characters
  - MCP OAuth now follows RFC 9728 Protected Resource Metadata discovery
  - Plugins blocked by organization policy (`managed-settings.json`) can no longer be installed, enabled, or seen in marketplace views
  - PreToolUse hooks can satisfy `AskUserQuestion` by returning `updatedInput` alongside `permissionDecision: "allow"`, enabling headless integrations
  - `tool_parameters` in OpenTelemetry `tool_result` events are now gated behind `OTEL_LOG_TOOL_DETAILS=1`
  - Scroll performance improved by replacing WASM yoga-layout with pure TypeScript in large transcripts
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Monitoring / Observability

- **`OTEL_LOG_TOOL_DETAILS` now gates `tool_parameters` for all tools**: Previously, `tool_parameters` was described as always present for Bash tools, with only MCP and Skill sub-fields conditionally gated. The documentation now consistently puts the entire `tool_parameters` field behind `OTEL_LOG_TOOL_DETAILS=1` for all tool types.
  > Before: `` `tool_parameters`: JSON string containing tool-specific parameters (when available) ``
  > After: `` `tool_parameters` (when `OTEL_LOG_TOOL_DETAILS=1`): JSON string containing tool-specific parameters ``
  - *Implication*: If your telemetry pipeline relies on `tool_parameters` (including Bash command details) appearing in `tool_result` events without setting `OTEL_LOG_TOOL_DETAILS=1`, that data will no longer be present. Set the env var explicitly to retain it.
  - *Source*: [Monitoring](https://code.claude.com/docs/en/monitoring-usage.md)

- **`OTEL_LOG_TOOL_DETAILS` description expanded in config reference table**: The variable's description was updated to be more precise about what it gates.
  > Before: "Enable logging of tool input arguments, MCP server/tool names, and skill names in tool events"
  > After: "Enable logging of tool parameters (bash commands, MCP server/tool names, skill names) and tool input arguments in tool events"
  - *Implication*: The updated wording makes explicit that bash commands are part of `tool_parameters`, not only MCP and skill identifiers.
  - *Source*: [Monitoring](https://code.claude.com/docs/en/monitoring-usage.md)

- **Security and privacy section rewritten**: The privacy note was consolidated to cover both `tool_parameters` and `tool_input` together under `OTEL_LOG_TOOL_DETAILS=1`.
  > Before: Two separate bullets — one for Bash commands/file paths in `tool_parameters`, one for tool input arguments behind the flag.
  > After: "Tool input arguments and parameters are not logged by default. To include them, set `OTEL_LOG_TOOL_DETAILS=1`. When enabled, tool_result events include a `tool_parameters` attribute (bash commands, MCP server/tool names, skill names) and a `tool_input` attribute (file paths, URLs, search patterns, and other arguments)."
  - *Implication*: Both potentially sensitive attributes are now described together, making the privacy posture and the single flag that controls them easier to understand.
  - *Source*: [Monitoring](https://code.claude.com/docs/en/monitoring-usage.md)

## New Pages

- **claude-directory.md** — An interactive explorer for the `.claude` directory structure covering both project-level (`.claude/`) and global (`~/.claude/`) files. Documents `CLAUDE.md`, `settings.json`, `settings.local.json`, `.mcp.json`, `rules/`, `skills/`, `commands/`, `agents/`, `output-styles/`, `agent-memory/`, `keybindings.json`, and auto memory under `~/.claude/projects/`. Each entry includes load timing, tips, and inline examples. [View](https://code.claude.com/docs/en/claude-directory.md)

## Notable Details

- The `tool_input` field description in the `tool_result` event was simplified: the explicit "over 512 characters" per-value truncation threshold was removed in favor of "long strings truncated," while the overall ~4 K payload cap remains.
- The `@claude review once` command is now documented more prominently in the Code Review page — it starts a single review without subscribing the PR to future push-triggered reviews, useful for long-running PRs with frequent pushes.
- The `claude-directory.md` page embeds a full React component (`ClaudeExplorer`) rendered as JSX source rather than plain markdown — it is an interactive UI component, not a static doc page.
- Total tracked documentation pages increased from 71 to 72 with the addition of `claude-directory.md`.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| claude-directory.md | New | +1432 / -0 | Interactive explorer for `.claude` directory covering all project and global config files |
| changelog.md | Modified | +33 / -0 | Added v2.1.85 release notes (25+ fixes and improvements, March 26 2026) |
| code-review.md | Modified | +37 / -7 | New "Check run output" section: check run details, annotations, and machine-readable severity JSON |
| monitoring-usage.md | Modified | +26 / -26 | `tool_parameters` now gated behind `OTEL_LOG_TOOL_DETAILS=1` for all tools; config table and privacy section updated |
