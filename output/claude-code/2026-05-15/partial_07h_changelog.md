# Claude Code Documentation Changes — 2026-05-15

## Summary

Four documentation pages were updated in this batch. The most substantive change documents a new `PostToolUse` hook capability: hooks can now inspect per-subagent usage telemetry from completed Agent calls. Minor updates add a `DEBUG` environment variable, pin a minimum version for `/goal`, and expand the `/status` settings explanation.

## Significant Changes

### Hooks

- **`PostToolUse` now exposes subagent usage telemetry in `tool_response`**: When a synchronous Agent tool call completes, the `tool_response` object in a `PostToolUse` hook now carries usage and timing fields alongside the subagent's output.
  > `In PostToolUse, tool_response for a completed Agent call carries the subagent's final text along with usage telemetry. Read these fields to record per-subagent cost from a hook`
  
  The documented fields are:
  | Field | Description |
  |---|---|
  | `status` | `"completed"` (sync) or `"async_launched"` (background) |
  | `agentId` | Identifier for the subagent run |
  | `content` | The subagent's final text blocks |
  | `totalTokens` | Total tokens billed across all turns |
  | `totalDurationMs` | Wall-clock duration of the run |
  | `totalToolUseCount` | Number of tool calls the subagent made |
  | `usage` | Per-type breakdown: `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens` |

  For `run_in_background: true` calls, `tool_response` instead carries `status: "async_launched"`, `agentId`, `description`, `prompt`, and `outputFile` — no usage fields, since the subagent launches asynchronously.
  - *Implication*: Hooks can now implement per-subagent cost tracking, latency monitoring, or audit logging without any additional instrumentation outside the hook itself.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

## Minor Changes

- **[env-vars.md]**: Added new `DEBUG` environment variable (`DEBUG=1` enables debug mode, equivalent to `--debug`; truthy values `1`, `true`, `yes`, `on` are recognized — namespace patterns like `DEBUG=express:*` do not trigger it). Also updated the `CLAUDE_CODE_DEBUG_LOGS_DIR` description to reference `DEBUG` as a third way to enable debug mode alongside `--debug` and `/debug`. (+2/-1 lines)

- **[goal.md]**: Added a version-gate note: `/goal` requires Claude Code **v2.1.139 or later**. (+4/-0 lines)

- **[settings.md]**: Expanded the `/status` "Verify active settings" section with clearer detail: the Status tab now includes a `Setting sources` line listing each loaded configuration layer; a layer only appears when it contributes at least one key. Also clarifies that the Config tab is an editor for UI toggles (theme, verbose output), not a view of `settings.json` contents, and that `Setting sources` shows which sources are loaded, not which layer supplied each individual key. (+3/-1 lines)

## Notable Details

- The `DEBUG` env var addition is careful to avoid false positives: only the four explicit truthy strings (`1`, `true`, `yes`, `on`) activate debug mode, so apps that set `DEBUG=express:*` or similar namespace patterns for other libraries will not inadvertently enable Claude Code debug logging.
- The `/status` Config tab clarification (`not a view of your settings.json contents`) addresses a likely source of user confusion where the Config tab UI and the `settings.json` file appear to serve the same purpose but operate differently.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| hooks.md | Modified | SIGNIFICANT | +14/-0 | Documented `tool_response` usage telemetry fields for `PostToolUse` on Agent calls |
| goal.md | Modified | MINOR | +4/-0 | Added v2.1.139 minimum version requirement note |
| settings.md | Modified | MINOR | +3/-1 | Expanded `/status` description: `Setting sources` line, Config tab clarification |
| env-vars.md | Modified | MINOR | +2/-1 | Added `DEBUG` env var; updated `CLAUDE_CODE_DEBUG_LOGS_DIR` description |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-15*
