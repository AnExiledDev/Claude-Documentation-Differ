# Claude API Documentation Changes — 2026-04-03

## Summary

This update focuses entirely on the Claude Agent SDK. The two headline changes are: (1) the `dontAsk` permission mode is now available in the Python SDK (previously TypeScript-only), and (2) the Python `AssistantMessage` and `ResultMessage` now expose per-step token usage and per-model cost breakdowns, reaching feature parity with TypeScript. Across the board, Python SDK code examples were corrected to use typed dataclasses instead of raw dict access and `message.type` string checks.

---

## Significant Changes

### Permissions

- **`dontAsk` permission mode now available in Python**: The `"TypeScript only"` qualifier has been removed from `dontAsk` across all documentation. The Python `PermissionMode` literal type now includes `"dontAsk"`.
  > `"dontAsk"` — Deny anything not pre-approved instead of prompting
  - *Implication*: Python headless agents can now use `permission_mode="dontAsk"` to hard-deny any tool not in `allowed_tools`, without needing `disallowed_tools` as a workaround. The previous workaround note ("use `disallowed_tools` to explicitly block tools you don't want Claude to attempt") has been removed.
  - *Source*: [permissions.md](https://platform.claude.com/docs/en/agent-sdk/permissions.md), [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md), [agent-loop.md](https://platform.claude.com/docs/en/agent-sdk/agent-loop.md)

- **New `auto` permission mode (TypeScript only)**: A new `"auto"` value has been added to the TypeScript `PermissionMode` type. It uses a model classifier to approve or deny each tool call dynamically.
  > `"auto"` (TypeScript only) — Uses a model classifier to approve or deny each tool call. See [Auto mode](https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode) for availability and behavior
  - *Implication*: Provides a middle ground between `"default"` (manual `canUseTool` callback) and `"bypassPermissions"` (approve all). Availability appears gated; the docs link to a separate page for details. Python does not yet have an equivalent.
  - *Source*: [permissions.md](https://platform.claude.com/docs/en/agent-sdk/permissions.md), [typescript.md](https://platform.claude.com/docs/en/agent-sdk/typescript.md), [quickstart.md](https://platform.claude.com/docs/en/agent-sdk/quickstart.md)

### Python SDK — Cost Tracking Parity

- **`AssistantMessage` gains `usage` and `message_id` fields**: The Python `AssistantMessage` dataclass now exposes per-step token usage (`usage: dict[str, Any] | None`) and a message ID (`message_id: str | None`). Previously these were only available in TypeScript via `message.message.usage` and `message.message.id`.
  > In Python, the `AssistantMessage` dataclass exposes the same data directly via `message.usage` and `message.message_id`. When Claude uses multiple tools in one turn, all messages in that turn share the same ID, so deduplicate by ID to avoid double-counting.
  - *Implication*: Python applications can now track token costs per step without waiting for the final `ResultMessage`.
  - *Source*: [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md), [cost-tracking.md](https://platform.claude.com/docs/en/agent-sdk/cost-tracking.md)

- **`ResultMessage` gains `model_usage` field**: The Python `ResultMessage` now includes `model_usage: dict[str, Any] | None`, providing a per-model cost breakdown matching TypeScript's `modelUsage`. The inner dict keys use **camelCase** because the value is passed through unmodified from the underlying CLI process.
  > The `model_usage` dict maps model names to per-model usage. The inner dict keys use camelCase because the value is passed through unmodified from the underlying CLI process, matching the TypeScript `ModelUsage` type.

  Inner dict keys: `inputTokens`, `outputTokens`, `cacheReadInputTokens`, `cacheCreationInputTokens`, `webSearchRequests`, `costUSD`, `contextWindow`, `maxOutputTokens`.
  - *Implication*: Python agents running multi-model workflows (e.g., with subagents) can now track cost per model without custom aggregation logic.
  - *Source*: [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md), [cost-tracking.md](https://platform.claude.com/docs/en/agent-sdk/cost-tracking.md)

- **Cost tracking section renamed and expanded**: The section "Track detailed usage in TypeScript" is renamed to "Track per-step and per-model usage" and now documents Python equivalents alongside TypeScript examples.
  > The examples in this section use TypeScript field names. In Python, the equivalent fields are `AssistantMessage.usage` and `AssistantMessage.message_id` for per-step usage, and `ResultMessage.model_usage` for per-model breakdowns.
  - *Source*: [cost-tracking.md](https://platform.claude.com/docs/en/agent-sdk/cost-tracking.md)

### TypeScript SDK

- **`SDKCompactBoundaryMessage` is now a distinct type**: The compact boundary event is no longer documented as a subtype of `SDKSystemMessage` in TypeScript — it is a separate `SDKCompactBoundaryMessage` type. In Python it remains a `SystemMessage` with `subtype="compact_boundary"`.
  > In TypeScript, the compact boundary is its own `SDKCompactBoundaryMessage` type rather than a subtype of `SDKSystemMessage`.
  - *Implication*: TypeScript code checking `message.type === "system" && message.subtype === "compact_boundary"` should be updated to check for `SDKCompactBoundaryMessage` instead.
  - *Source*: [agent-loop.md](https://platform.claude.com/docs/en/agent-sdk/agent-loop.md), [streaming-output.md](https://platform.claude.com/docs/en/agent-sdk/streaming-output.md)

- **Structured output result check requires `subtype === "success"`**: All TypeScript examples for `structured_output` now guard with `message.subtype === "success"` in addition to `message.type === "result"`.
  > `if (message.type === "result" && message.subtype === "success" && message.structured_output)`
  - *Implication*: Without the `subtype` check, error result messages (`subtype: "error"`) would previously pass the condition; this narrows the guard to successful completions only. Update any existing code reading `structured_output` that doesn't already include this check.
  - *Source*: [structured-outputs.md](https://platform.claude.com/docs/en/agent-sdk/structured-outputs.md), [typescript-v2-preview.md](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview.md)

- **`total_cost_usd` is no longer nullable in TypeScript**: A TypeScript example changed from `message.total_cost_usd ?? 0` to `message.total_cost_usd`, indicating this field is now guaranteed to be a number on a result message.
  - *Source*: [cost-tracking.md](https://platform.claude.com/docs/en/agent-sdk/cost-tracking.md)

- **Plugin assistant message content access corrected**: TypeScript examples in the plugins page changed `message.content` to `message.message.content` when accessing content on an assistant message, matching the correct nested structure.
  - *Source*: [plugins.md](https://platform.claude.com/docs/en/agent-sdk/plugins.md)

### Python SDK — API Correctness Fixes

Across `slash-commands.md` and `overview.md`, Python examples were updated to use proper typed imports and dataclass-style message handling instead of raw dict/attribute access. Key patterns corrected:

| Before (incorrect) | After (correct) |
|---|---|
| `options={"max_turns": 1}` | `options=ClaudeAgentOptions(max_turns=1)` |
| `message.type == "system"` | `isinstance(message, SystemMessage)` |
| `message.session_id` | `message.data["session_id"]` |
| `message.slash_commands` | `message.data["slash_commands"]` |
| `message.compact_metadata.pre_tokens` | `message.data["compact_metadata"]["pre_tokens"]` |
| `if hasattr(message, "result"):` | `if isinstance(message, ResultMessage):` |
| `message.message` (for assistant content) | iterate `message.content` blocks |

- *Implication*: These are correctness fixes against the actual Python SDK API. Code written against the old examples will need to be updated. The key principle is that `SystemMessage.data` is a dict; session ID and slash commands are stored inside it, not as top-level attributes.
- *Source*: [slash-commands.md](https://platform.claude.com/docs/en/agent-sdk/slash-commands.md), [overview.md](https://platform.claude.com/docs/en/agent-sdk/overview.md)

### MCP Configuration

- **`.mcp.json` is not loaded automatically**: Documentation previously stated the SDK loads `.mcp.json` automatically. This has been corrected: the file is only picked up when `settingSources: ["project"]` (Python: `setting_sources=["project"]`) is explicitly set in options.
  > The SDK does not load filesystem settings by default, so set `settingSources: ["project"]` (Python: `setting_sources=["project"]`) in your options for the file to be picked up.
  - *Implication*: Existing code relying on automatic `.mcp.json` loading will silently fail unless `settingSources` is configured.
  - *Source*: [mcp.md](https://platform.claude.com/docs/en/agent-sdk/mcp.md)

### Hosting

- **Claude Code CLI is now bundled — no separate install required**: The hosting prerequisites previously listed `npm install -g @anthropic-ai/claude-code` as a separate step. This has been removed.
  > Node.js (required by the bundled Claude Code CLI that the SDK spawns; both SDK packages include it, so no separate install is needed)
  - *Implication*: Deployment Dockerfiles and CI scripts that run `npm install -g @anthropic-ai/claude-code` before using the Agent SDK can drop that step.
  - *Source*: [hosting.md](https://platform.claude.com/docs/en/agent-sdk/hosting.md)

### Minor Fixes

- **System prompt TypeScript option corrected**: The `systemPrompt` preset option was documented as `{ preset: "claude_code" }` but the correct form is `{ type: "preset", preset: "claude_code" }`. Fixed in the modifying-system-prompts page.
  - *Source*: [modifying-system-prompts.md](https://platform.claude.com/docs/en/agent-sdk/modifying-system-prompts.md)

- **File checkpointing CLI flag added**: The CLI rewind command now includes the `-p` flag: `claude -p --resume <session-id> --rewind-files <checkpoint-uuid>`.
  - *Source*: [file-checkpointing.md](https://platform.claude.com/docs/en/agent-sdk/file-checkpointing.md)

- **Secure deployment model card URL updated**: The link to the Claude Opus 4.6 system card changed from `assets.anthropic.com/m/64823ba7485345a7/Claude-Opus-4-5-System-Card.pdf` to `www.anthropic.com/claude-opus-4-6-system-card`.
  - *Source*: [secure-deployment.md](https://platform.claude.com/docs/en/agent-sdk/secure-deployment.md)

---

## Migration Guidance

### Python: `dontAsk` permission mode
Previously, the Python workaround for headless permission control was `disallowed_tools`. You can now use the mode directly:
```python
# Before (workaround)
options = ClaudeAgentOptions(
    disallowed_tools=["Bash", "Write"],
    allowed_tools=["Read", "Grep"],
)

# After
options = ClaudeAgentOptions(
    permission_mode="dontAsk",
    allowed_tools=["Read", "Grep"],
)
```

### TypeScript: Structured output result check
```typescript
// Before
if (message.type === "result" && message.structured_output) { ... }

// After
if (message.type === "result" && message.subtype === "success" && message.structured_output) { ... }
```

### Python: Message attribute access
```python
# Before (incorrect)
if message.type == "system" and message.subtype == "init":
    session_id = message.session_id

# After (correct)
if isinstance(message, SystemMessage) and message.subtype == "init":
    session_id = message.data["session_id"]
```

### MCP: Explicit settings source required
```typescript
// Before (assumed automatic loading)
const options = { mcpServers: [] };  // expected .mcp.json to load

// After
const options = {
  settingSources: ["project"],  // Python: setting_sources=["project"]
};
```

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| slash-commands.md | Modified | +31/-29 | Python examples updated to typed imports and `isinstance` checks; `message.data[...]` access pattern |
| python.md | Modified | +17/-0 | Added `dontAsk` to `PermissionMode`; added `message_id` to `AssistantMessage`; added `model_usage` to `ResultMessage` with full field docs |
| cost-tracking.md | Modified | +9/-9 | Renamed section; documented Python per-step and per-model usage parity; removed "Python only has totals" caveat |
| permissions.md | Modified | +4/-9 | `dontAsk` now cross-SDK; added `auto` mode; removed TypeScript-only notes and Python workaround note |
| agent-loop.md | Modified | +4/-3 | `SDKCompactBoundaryMessage` TypeScript type noted; `auto` mode added to permission table |
| overview.md | Modified | +4/-4 | Python example updated to typed `SystemMessage`/`ResultMessage` checks and `message.data` access |
| structured-outputs.md | Modified | +4/-4 | Added `subtype === "success"` guard on result message checks; added explicit type cast |
| quickstart.md | Modified | +2/-1 | `dontAsk` cross-SDK; `auto` mode added to permission table |
| typescript.md | Modified | +2/-1 | Added `"auto"` to `PermissionMode` union type |
| mcp.md | Modified | +2/-2 | Corrected `.mcp.json` loading — now requires explicit `settingSources` |
| plugins.md | Modified | +2/-2 | Fixed `message.content` → `message.message.content` for assistant messages in TypeScript |
| hosting.md | Modified | +1/-2 | Removed separate Claude Code CLI install step; clarified it is bundled |
| streaming-output.md | Modified | +1/-1 | Updated compact boundary description to reflect TypeScript type split |
| modifying-system-prompts.md | Modified | +1/-1 | Fixed `systemPrompt` TypeScript preset option shape |
| typescript-v2-preview.md | Modified | +1/-1 | Added `subtype === "success"` guard on result message |
| file-checkpointing.md | Modified | +1/-1 | Added `-p` flag to CLI rewind command |
| secure-deployment.md | Modified | +1/-1 | Updated Opus 4.6 model card URL |

---
*Generated from Claude Agent SDK documentation changes detected on 2026-04-03*
