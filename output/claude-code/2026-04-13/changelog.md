# Claude Code Documentation Changes — 2026-04-13

## Summary

Ten documentation pages were updated in this diff, covering a new `/team-onboarding` command, a new `asyncRewake` hook field, a `viewMode` settings key, expanded Vertex AI region support, clarified permission-hook interaction semantics, and telemetry improvements for trace spans. No pages were added or removed.

## Significant Changes

### Features

- **New `/team-onboarding` command**: Generates a team onboarding guide from your Claude Code usage history.
  > `/team-onboarding` — Generate a team onboarding guide from your Claude Code usage history. Claude analyzes your sessions, commands, and MCP server usage from the past 30 days and produces a markdown guide a teammate can paste as a first message to get set up quickly
  - *Implication*: Teams can now auto-generate context-rich onboarding documents without manual curation of their Claude Code setup.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

- **Session resume accepts custom names**: `claude --resume` now accepts a custom session name in addition to a session ID.
  > Sessions created by `claude -p` or SDK invocations do not appear in the picker, but you can still resume one by passing its session ID or custom name to `claude --resume <session-id-or-name>`. Custom names set with `--name` or `/rename` are accepted in addition to session IDs.
  - *Implication*: If you've named sessions with `--name` or `/rename`, you can now reference them directly instead of looking up opaque session IDs.
  - *Source*: [Common Workflows](https://code.claude.com/docs/en/common-workflows.md)

- **Ultraplan auto-creates cloud environments**: Ultraplan no longer requires a pre-existing cloud environment — it creates one automatically on first launch.
  > If you don't have a cloud environment yet, ultraplan creates one automatically when it first launches.
  - *Implication*: New users can invoke ultraplan without first running `/web-setup` manually.
  - *Source*: [Ultraplan](https://code.claude.com/docs/en/ultraplan.md)

- **New `viewMode` setting**: Controls the default transcript view mode on startup without relying on the sticky Ctrl+O toggle.
  > `viewMode` — Default transcript view mode on startup: `"default"`, `"verbose"`, or `"focus"`. Overrides the sticky Ctrl+O selection when set
  - *Implication*: Teams using managed settings can now enforce a consistent transcript view across all users (e.g., always `"verbose"` for audit purposes).
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Hooks

- **New `asyncRewake` hook field**: A new option for command hooks that runs asynchronously but can wake Claude immediately on failure.
  > `asyncRewake` — If `true`, runs in the background and wakes Claude on exit code 2. Implies `async`. The hook's stderr, or stdout if stderr is empty, is shown to Claude as a system reminder so it can react to a long-running background failure
  - *Implication*: Hooks can now monitor long-running background processes and surface failures to Claude mid-session without blocking the initial tool call. Previously, async hook output only appeared on the next user interaction.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

- **Clarified `PreToolUse` permission interaction**: The documentation now explicitly states that deny/ask rules are evaluated regardless of what a `PreToolUse` hook returns — not just when the hook returns `"allow"`.
  > Hook decisions do not bypass permission rules. Deny and ask rules are evaluated regardless of what a PreToolUse hook returns, so a matching deny rule blocks the call and a matching ask rule still prompts even when the hook returned `"allow"` or `"ask"`.
  - *Implication*: A hook returning `"allow"` does not suppress `ask`-type permission rules; users will still be prompted. This clarification matters for anyone building hooks intended to fully pre-approve tool calls.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md), [Hooks](https://code.claude.com/docs/en/hooks.md)

### Model Configuration

- **`ANTHROPIC_CUSTOM_MODEL_OPTION` gains capability suffix support**: The `_NAME`, `_DESCRIPTION`, and `_SUPPORTED_CAPABILITIES` environment variable suffixes now apply to `ANTHROPIC_CUSTOM_MODEL_OPTION` in addition to the default Sonnet and Haiku models.
  > The same `_NAME`, `_DESCRIPTION`, and `_SUPPORTED_CAPABILITIES` suffixes are available for `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`, and `ANTHROPIC_CUSTOM_MODEL_OPTION`.
  - *Implication*: Custom model entries in the `/model` picker can now declare supported capabilities (e.g., extended thinking, effort levels) so Claude Code enables the correct features for gateway-specific or non-standard model deployments.
  - *Source*: [Model Configuration](https://code.claude.com/docs/en/model-config.md)

- **New `ANTHROPIC_CUSTOM_MODEL_OPTION_SUPPORTED_CAPABILITIES` env var**: Documents the capability declaration variable for custom model picker entries.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **New Vertex AI region overrides for Opus 4.5 and 4.6**: Two new environment variables allow per-model region pinning for Claude Opus on Vertex AI.
  > `VERTEX_REGION_CLAUDE_4_5_OPUS` — Override region for Claude Opus 4.5 when using Vertex AI
  > `VERTEX_REGION_CLAUDE_4_6_OPUS` — Override region for Claude Opus 4.6 when using Vertex AI
  - *Implication*: Vertex AI deployments can now pin Opus 4.5 and 4.6 to specific regions, consistent with existing Sonnet region controls.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

### Telemetry / Monitoring

- **`OTEL_LOG_TOOL_DETAILS` now covers trace span attributes**: The variable's scope was expanded — it now populates `tool_input` and related attributes on trace spans in addition to `tool_result` log events.
  > When enabled, `tool_result` events include a `tool_parameters` attribute with Bash commands, MCP server and tool names, and skill names, plus a `tool_input` attribute with file paths, URLs, search patterns, and other arguments. Trace spans include the same `tool_input` attribute and input-derived attributes such as `file_path`.
  - *Implication*: Observability pipelines using distributed tracing now get tool input details natively on spans without needing to cross-reference log events. Operators should review their trace redaction rules accordingly.
  - *Source*: [Monitoring & Usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **Tracing section now lists `OTEL_LOG_TOOL_DETAILS` as required for tool input in spans**: Updated to reflect that three variables are needed to fully unlock span content.
  > Spans redact user prompt text, tool input details, and tool content by default. Set `OTEL_LOG_USER_PROMPTS=1`, `OTEL_LOG_TOOL_DETAILS=1`, and `OTEL_LOG_TOOL_CONTENT=1` to include them.
  - *Implication*: Previously the docs only listed `OTEL_LOG_USER_PROMPTS` and `OTEL_LOG_TOOL_CONTENT` for span enrichment; `OTEL_LOG_TOOL_DETAILS` was omitted.
  - *Source*: [Monitoring & Usage](https://code.claude.com/docs/en/monitoring-usage.md)

### Troubleshooting

- **Web quickstart troubleshooting error updated**: The "No cloud environment available" troubleshooting entry was expanded to cover "Could not create a cloud environment" and explains the automatic-creation behavior added in recent CLI versions.
  > Remote-session features create a default cloud environment automatically if you don't have one. If you see "Could not create a cloud environment", automatic creation failed. If you see "No cloud environment available", your CLI predates automatic creation. In either case, run `/web-setup` in the Claude Code CLI to create one manually.
  - *Implication*: The two error messages now have distinct meaning: "Could not create" means auto-creation failed; "No cloud environment available" means the CLI is older than v2.1.100 and lacks auto-creation support.
  - *Source*: [Web Quickstart](https://code.claude.com/docs/en/web-quickstart.md)

## Notable Details

- The `OTEL_LOG_TOOL_DETAILS` description in `env-vars.md` was updated from "include MCP server names and tool details in telemetry" to "include tool input arguments, MCP server names, and tool details in OpenTelemetry traces and logs" — the word "traces" being new, consistent with the span attribute expansion in `monitoring-usage.md`.
- The `asyncRewake` async hooks constraint is documented inline in the async hooks section: `asyncRewake` hooks that exit with code 2 are the **only** exception to the rule that async hook output waits until the next user interaction.
- The hooks `permissionDecision` table entry was subtly corrected: the old wording "Deny and ask rules still apply when a hook returns `"allow"`" implied `ask` rules only triggered on `"allow"` returns. The new wording clarifies that rules fire unconditionally.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| commands.md | Modified | +1/-0 | Added `/team-onboarding` command |
| common-workflows.md | Modified | +1/-1 | `--resume` now accepts session name in addition to ID |
| env-vars.md | Modified | +4/-1 | New `ANTHROPIC_CUSTOM_MODEL_OPTION_SUPPORTED_CAPABILITIES`; two new Vertex Opus region vars; clarified `OTEL_LOG_TOOL_DETAILS` |
| hooks.md | Modified | +13/-12 | New `asyncRewake` field; clarified `permissionDecision` rule evaluation |
| model-config.md | Modified | +1/-1 | `_SUPPORTED_CAPABILITIES` suffixes now documented for `ANTHROPIC_CUSTOM_MODEL_OPTION` |
| monitoring-usage.md | Modified | +23/-23 | `OTEL_LOG_TOOL_DETAILS` now covers trace spans; tracing section updated; table reformatted |
| permissions.md | Modified | +1/-1 | Clarified that hook decisions don't bypass ask rules |
| settings.md | Modified | +1/-0 | New `viewMode` setting for default transcript view |
| ultraplan.md | Modified | +1/-1 | Auto-creates cloud environment on first launch |
| web-quickstart.md | Modified | +2/-2 | Expanded cloud environment troubleshooting for auto-creation errors |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-13*
