# Claude API Documentation Changes — 2026-02-27

## Summary

This update delivers a large expansion of the TypeScript and Python Agent SDK reference documentation, adding dozens of new types, API surface, and hook events. The changes include a new `listSessions()` function (TypeScript), a custom `Transport` abstraction (Python), six new lifecycle hook events, a sandbox default change, and a significant restructuring of the cost-tracking guide. The V2 TypeScript preview renames `Session` to `SDKSession` and aligns return types with the V1 SDK.

---

## Significant Changes

### TypeScript SDK — `query()` Options Expanded

Several new options are now documented on the `Options` type:

- **`agent`** (`string`) — Designates an agent name for the main thread. Must be defined in the `agents` option or in settings.
- **`debug`** / **`debugFile`** — Enable debug mode or redirect debug logs to a file path. `debugFile` implicitly enables debug mode.
- **`effort`** (`'low' | 'medium' | 'high' | 'max'`, default `'high'`) — Controls thinking depth via adaptive thinking.
- **`persistSession`** (`boolean`, default `true`) — When `false`, disables session persistence to disk; sessions cannot be resumed later.
- **`promptSuggestions`** (`boolean`, default `false`) — Emits a `prompt_suggestion` message after each turn with a predicted next user prompt.
- **`sessionId`** (`string`) — Lets callers supply a specific UUID for the session instead of auto-generating one.
- **`spawnClaudeCodeProcess`** (`(options: SpawnOptions) => SpawnedProcess`) — Custom function to spawn the Claude Code process; enables running it in VMs, containers, or remote environments.
- **`thinking`** ([`ThinkingConfig`](#thinkingconfig)) — Replaces deprecated `maxThinkingTokens`. Supports `adaptive`, `enabled` (with `budget_tokens`), and `disabled` variants.
- **`env`** type changed from `Dict<string>` to `Record<string, string | undefined>`. Documentation now notes: set `CLAUDE_AGENT_SDK_CLIENT_APP` to identify your app in the `User-Agent` header.

  > `maxThinkingTokens` | `number` | `undefined` | _Deprecated:_ Use `thinking` instead. Maximum tokens for thinking process

  - *Implication*: Callers using `maxThinkingTokens` should migrate to `thinking`. The deprecated field still works but is no longer the canonical API.
  - *Source*: [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

### TypeScript SDK — New `listSessions()` Function

A new top-level export `listSessions()` discovers past sessions with lightweight metadata.

```typescript
function listSessions(options?: ListSessionsOptions): Promise<SDKSessionInfo[]>
```

| Parameter | Description |
|:----------|:------------|
| `options.dir` | Filter to sessions for this project directory (and git worktrees). Omit for all projects. |
| `options.limit` | Maximum number of sessions to return. |

Returns `SDKSessionInfo[]` with fields: `sessionId`, `summary`, `lastModified`, `fileSize`, `customTitle`, `firstPrompt`, `gitBranch`, `cwd`.

> Discovers and lists past sessions with light metadata. Filter by project directory or list sessions across all projects.

- *Implication*: Enables SDK applications to enumerate resumable sessions programmatically, useful for building session pickers or dashboards.
- *Source*: [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

### TypeScript SDK — `Query` Interface Expanded

The `Query` object returned by `query()` now documents several new methods:

| New Method | Description |
|:-----------|:------------|
| `initializationResult()` | Returns `SDKControlInitializeResponse` with commands, output styles, models, and account info. |
| `reconnectMcpServer(serverName)` | Reconnect a specific MCP server by name. |
| `toggleMcpServer(serverName, enabled)` | Enable or disable an MCP server by name. |
| `setMcpServers(servers)` | Dynamically replace the full set of MCP servers for the session. Returns `McpSetServersResult` with added/removed counts and errors. |
| `streamInput(stream)` | Stream input messages for multi-turn conversations. |
| `stopTask(taskId)` | Stop a running background task by ID. |
| `close()` | Forcefully terminate the underlying process and clean up resources. |

Additionally, `rewindFiles()` gains an optional `{ dryRun?: boolean }` second parameter and now returns `RewindFilesResult` instead of `void`. `setMaxThinkingTokens()` is now marked deprecated.

- *Implication*: Callers that need fine-grained session control (dynamic MCP reconfiguration, background task management, or dry-run file rewind previews) can now do so without restarting the session.
- *Source*: [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

### TypeScript SDK — New and Expanded Hook Events

Six new `HookEvent` values are now documented:

```typescript
type HookEvent =
  // ...existing events...
  | "Setup"          // Fires on init or maintenance
  | "TeammateIdle"   // Fires when a teammate agent is idle
  | "TaskCompleted"  // Fires when a background task completes
  | "ConfigChange"   // Fires when settings files change
  | "WorktreeCreate" // Fires when a git worktree is created
  | "WorktreeRemove" // Fires when a git worktree is removed
```

Corresponding typed input structures `SetupHookInput`, `TeammateIdleHookInput`, `TaskCompletedHookInput`, `ConfigChangeHookInput`, `WorktreeCreateHookInput`, and `WorktreeRemoveHookInput` are also documented.

`HookCallbackMatcher` gains a new optional `timeout?: number` field (in seconds) applied to all hooks in the matcher.

Existing hook inputs are expanded:
- `PreToolUseHookInput`, `PostToolUseHookInput`, `PostToolUseFailureHookInput` — all now include `tool_use_id: string`.
- `NotificationHookInput` — adds `notification_type: string`.
- `StopHookInput` — adds `last_assistant_message?: string`.
- `SubagentStopHookInput` — adds `agent_id`, `agent_transcript_path`, `agent_type`, `last_assistant_message?`.
- `SessionStartHookInput` — adds `agent_type?`, `model?`.

`SyncHookJSONOutput` is expanded to cover `PostToolUseFailure`, `Notification`, `SubagentStart`, and `Setup` hook-specific outputs. `PostToolUse` output gains `updatedMCPToolOutput`. The `PermissionRequest` output now accepts a full structured `decision` object with either `allow` or `deny` behavior.

- *Implication*: Hooks can now observe and react to worktree lifecycle events, configuration file changes, teammate availability, and completed background tasks—enabling richer automation and orchestration scenarios.
- *Source*: [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

### TypeScript SDK — `AgentDefinition` Expanded

```typescript
type AgentDefinition = {
  description: string;
  tools?: string[];
  disallowedTools?: string[];   // NEW
  prompt: string;
  model?: "sonnet" | "opus" | "haiku" | "inherit";
  mcpServers?: AgentMcpServerSpec[];              // NEW
  skills?: string[];                              // NEW
  maxTurns?: number;                              // NEW
  criticalSystemReminder_EXPERIMENTAL?: string;   // NEW
}
```

The new `AgentMcpServerSpec` type allows subagents to inherit MCP servers by name from the parent's config, or to define inline server configurations.

- *Implication*: Subagent definitions are now significantly richer—they can be given their own MCP servers, skills, turn caps, and explicit tool denylists.
- *Source*: [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

### TypeScript SDK — `PermissionMode`, `CanUseTool`, and `PermissionResult` Changes

- **New `PermissionMode`**: `'dontAsk'` — does not prompt for permissions; denies if not pre-approved.
- **`CanUseTool` input type**: changed from `ToolInput` to `Record<string, unknown>`.
- **`CanUseTool` options** gain three new fields: `blockedPath` (path that triggered the request), `decisionReason` (why permission was triggered), `toolUseID` (unique ID for this call), and `agentID` (the calling subagent, if any).
- **`PermissionResult` `allow`**: `updatedInput` is now optional; adds optional `toolUseID`.
- **`PermissionResult` `deny`**: adds optional `toolUseID`.

  - *Source*: [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

### TypeScript SDK — `SDKMessage` Union Expanded

Twelve new message types added to the `SDKMessage` discriminated union:

> `SDKStatusMessage`, `SDKTaskNotificationMessage`, `SDKToolUseSummaryMessage`, `SDKHookStartedMessage`, `SDKHookProgressMessage`, `SDKHookResponseMessage`, `SDKToolProgressMessage`, `SDKAuthStatusMessage`, `SDKTaskStartedMessage`, `SDKTaskProgressMessage`, `SDKFilesPersistedEvent`, `SDKRateLimitEvent`, `SDKPromptSuggestionMessage`

Additional changes to existing message types:
- **`SDKAssistantMessage`**: `message` field renamed from `APIAssistantMessage` to `BetaMessage`; adds `error?: SDKAssistantMessageError` (`'authentication_failed' | 'billing_error' | 'rate_limit' | 'invalid_request' | 'server_error' | 'unknown'`).
- **`SDKResultMessage`**: adds `stop_reason: string | null` on both `success` and `error` subtypes.
- **`SDKSystemMessage`**: adds `agents?`, `betas?`, `claude_code_version`, `skills`, `plugins` fields.
- **`SDKUserMessage` / `SDKUserMessageReplay`**: `message` field renamed from `APIUserMessage` to `MessageParam`; adds `isSynthetic?`, `tool_use_result?`; replay adds `isReplay: true`.
- **`SDKPartialAssistantMessage`**: `event` field renamed from `RawMessageStreamEvent` to `BetaRawMessageStreamEvent`.

  - *Implication*: Applications iterating the message stream will receive rate-limit events, auth status, hook lifecycle messages, and prompt suggestions as first-class stream messages. Discriminated-union type narrowing must account for the new variants.
  - *Source*: [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

### TypeScript SDK — `tool()` Function: Zod 4 Support and Annotations

```typescript
function tool<Schema extends AnyZodRawShape>(
  name: string,
  description: string,
  inputSchema: Schema,
  handler: (args: InferShape<Schema>, extra: unknown) => Promise<CallToolResult>,
  extras?: { annotations?: ToolAnnotations }   // NEW
): SdkMcpToolDefinition<Schema>
```

The schema parameter type changed from `ZodRawShape` to `AnyZodRawShape` to support both Zod 3 and Zod 4. A new `extras` parameter allows supplying MCP tool annotations (`readOnly`, `destructive`, `openWorld`).

  - *Source*: [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

### TypeScript SDK — `ToolInputSchemas` Replaces `ToolInput`

The `ToolInput` union type is renamed to `ToolInputSchemas` and is now explicitly exported from `@anthropic-ai/claude-agent-sdk`. The set of members changed:

- **Added**: `TaskOutputInput`, `ConfigInput`, `EnterWorktreeInput`, `ExitPlanModeInput`
- **Removed**: `BashOutputInput`, `KillBash`

A matching `ToolOutputSchemas` union is also now documented, similarly restructured.

  - *Source*: [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

### TypeScript SDK — New MCP Server Type: `McpClaudeAIProxyServerConfig`

```typescript
type McpClaudeAIProxyServerConfig = {
  type: "claudeai-proxy";
  url: string;
  id: string;
}
```

A new MCP server configuration variant for routing through a Claude AI proxy. No further documentation is provided beyond the type definition.

  - *Source*: [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

### TypeScript SDK — Sandbox Default Changes

Two `SandboxSettings` defaults have changed:

| Property | Old Default | New Default |
|:---------|:-----------|:-----------|
| `autoAllowBashIfSandboxed` | `false` | `true` |
| `allowUnsandboxedCommands` | `false` | `true` |

  - *Implication*: Applications that create sandboxed sessions and relied on these being `false` by default will need to explicitly set them to `false` to preserve the previous behavior.
  - *Source*: [Python SDK Reference](https://platform.claude.com/docs/en/agent-sdk/python.md)

---

### Python SDK — New `transport` Parameter on `query()` and `ClaudeSDKClient`

```python
async def query(
    *,
    prompt: str | AsyncIterable[dict[str, Any]],
    options: ClaudeAgentOptions | None = None,
    transport: Transport | None = None   # NEW
) -> AsyncIterator[Message]
```

`ClaudeSDKClient.__init__` also accepts a `transport` parameter. The `Transport` abstract base class is now documented:

```python
class Transport(ABC):
    async def connect(self) -> None: ...
    async def write(self, data: str) -> None: ...
    def read_messages(self) -> AsyncIterator[dict[str, Any]]: ...
    async def close(self) -> None: ...
    def is_ready(self) -> bool: ...
    async def end_input(self) -> None: ...
```

> This is a low-level internal API. The interface may change in future releases.

  - *Implication*: Custom transports enable running Claude Code in remote environments (VMs, containers) by replacing the default subprocess channel. Treat this as an internal API subject to change.
  - *Source*: [Python SDK Reference](https://platform.claude.com/docs/en/agent-sdk/python.md)

### Python SDK — Hooks and Custom Tools Now Available in `query()`

Previously documented as unsupported in `query()`, both Hooks and Custom Tools now show ✅ in the feature comparison table:

| Feature | Before | After |
|:--------|:-------|:------|
| **Hooks** | ❌ Not supported in `query()` | ✅ Supported |
| **Custom Tools** | ❌ Not supported in `query()` | ✅ Supported |

  - *Implication*: Applications using `query()` for one-off tasks can now attach hooks and custom tools without switching to `ClaudeSDKClient`.
  - *Source*: [Python SDK Reference](https://platform.claude.com/docs/en/agent-sdk/python.md)

### Python SDK — `ClaudeSDKClient` New Methods

| New Method | Description |
|:-----------|:------------|
| `set_permission_mode(mode)` | Change the permission mode for the current session. |
| `set_model(model)` | Change the model; pass `None` to reset to default. |
| `get_mcp_status()` | Get the status of all configured MCP servers. |
| `get_server_info()` | Get server information including session ID and capabilities. |

  - *Source*: [Python SDK Reference](https://platform.claude.com/docs/en/agent-sdk/python.md)

### Python SDK — `ClaudeAgentOptions` Expanded

New fields added to `ClaudeAgentOptions`:

| Field | Type | Description |
|:------|:-----|:------------|
| `sandbox` | `SandboxSettings \| None` | Configure sandbox behavior programmatically. |
| `plugins` | `list[SdkPluginConfig]` | Load custom plugins. |
| `thinking` | `ThinkingConfig \| None` | Controls extended thinking (replaces deprecated `max_thinking_tokens`). |
| `effort` | `Literal["low", "medium", "high", "max"] \| None` | Effort level for thinking depth. |
| `enable_file_checkpointing` | `bool` | Enable file change tracking for rewind. |

`max_thinking_tokens` is now marked `# Deprecated: use thinking instead`.

`output_format` type changed from `OutputFormat` (a `TypedDict`) to `dict[str, Any]`. The expected shape is documented as `{"type": "json_schema", "schema": {...}}`.

  - *Source*: [Python SDK Reference](https://platform.claude.com/docs/en/agent-sdk/python.md)

### Python SDK — New Hook Events and Typed Hook Inputs

New `HookEvent` values for Python (note: Python's hook event set was previously a subset of TypeScript's):

```python
HookEvent = Literal[
    "PreToolUse", "PostToolUse",
    "PostToolUseFailure",   # NEW
    "UserPromptSubmit", "Stop", "SubagentStop", "PreCompact",
    "Notification",         # NEW
    "SubagentStart",        # NEW
    "PermissionRequest",    # NEW
]
```

The `HookCallback` signature is now strongly typed:
```python
# Before
HookCallback = Callable[[dict[str, Any], str | None, HookContext], Awaitable[dict[str, Any]]]

# After
HookCallback = Callable[[HookInput, str | None, HookContext], Awaitable[HookJSONOutput]]
```

`HookContext` changed from `@dataclass` to `TypedDict`. New hook input types documented: `PostToolUseFailureHookInput`, `NotificationHookInput`, `SubagentStartHookInput`, `PermissionRequestHookInput`. `hookSpecificOutput` is now a typed `HookSpecificOutput` discriminated union rather than a plain `dict[str, Any]`.

  - *Source*: [Python SDK Reference](https://platform.claude.com/docs/en/agent-sdk/python.md)

### Python SDK — Message Types Expanded

- **`UserMessage`**: gains `uuid: str | None`, `parent_tool_use_id: str | None`, `tool_use_result: dict[str, Any] | None`.
- **`AssistantMessage`**: gains `parent_tool_use_id: str | None` and `error: AssistantMessageError | None`.
- **`AssistantMessageError`**: new type — `Literal["authentication_failed", "billing_error", "rate_limit", "invalid_request", "server_error", "unknown"]`.
- **`ResultMessage.usage`**: now documented with specific keys: `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`.

  - *Source*: [Python SDK Reference](https://platform.claude.com/docs/en/agent-sdk/python.md)

### Python SDK — `can_use_tool` Signature Change

The callback signature changes from returning `bool` to returning a typed result object:

```python
# Before
async def can_use_tool(tool: str, input: dict) -> bool:
    return is_command_authorized(input.get("command"))

# After
async def can_use_tool(
    tool: str, input: dict, context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    if is_command_authorized(input.get("command")):
        return PermissionResultAllow()
    return PermissionResultDeny(message="Command not authorized for unsandboxed execution")
```

`ToolPermissionContext` is now a documented type. Import via `from claude_agent_sdk.types import ToolPermissionContext`.

  - *Implication*: Existing `can_use_tool` callbacks returning `bool` will need to be updated to return `PermissionResultAllow()` / `PermissionResultDeny(message=...)`.
  - *Source*: [Python SDK Reference](https://platform.claude.com/docs/en/agent-sdk/python.md)

### Python SDK — `tool()` Decorator: Annotations Support

```python
def tool(
    name: str,
    description: str,
    input_schema: type | dict[str, Any],
    annotations: ToolAnnotations | None = None   # NEW
) -> ...
```

`ToolAnnotations` is imported from `mcp.types` and supports hints like `readOnlyHint`, `destructiveHint`, `openWorldHint`.

  - *Source*: [Python SDK Reference](https://platform.claude.com/docs/en/agent-sdk/python.md)

---

### TypeScript V2 Preview — `Session` Renamed to `SDKSession`

The `Session` interface in the V2 preview is renamed to `SDKSession`:

```typescript
// Before
interface Session {
  send(message: string): Promise<void>;
  stream(): AsyncGenerator<SDKMessage>;
  close(): void;
}

// After
interface SDKSession {
  readonly sessionId: string;                      // NEW
  send(message: string | SDKUserMessage): Promise<void>;  // string | SDKUserMessage
  stream(): AsyncGenerator<SDKMessage, void>;      // explicit void
  close(): void;
}
```

Return types for `unstable_v2_createSession()` and `unstable_v2_resumeSession()` updated to `SDKSession`. `unstable_v2_prompt()` now returns `Promise<SDKResultMessage>` instead of `Promise<Result>`.

Code examples updated to guard on `result.subtype === "success"` before accessing `result.result`.

  - *Source*: [TypeScript V2 Preview](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview.md)

The V2 preview description corrects `send()`/`receive()` to `send()`/`stream()` in the banner note on the V1 TypeScript reference.

---

### Cost Tracking — Page Restructured and Simplified

The cost-tracking page (`cost-tracking.md`, +123/-289 lines) was significantly rewritten. Old content included a class-based `CostTracker` with manual deduplication logic and a billing dashboard example. New content focuses on minimal, idiomatic `for await` patterns:

```typescript
// New pattern: get total cost from result message
for await (const message of query({ prompt: "Summarize this project" })) {
  if (message.type === "result") {
    console.log(`Total cost: $${message.total_cost_usd}`);
  }
}
```

Key clarifications added:
- Python SDK does **not** expose per-step token usage on individual assistant messages; only TypeScript does.
- The SDK automatically uses prompt caching — no configuration required.
- Both success and error result messages include `usage` and `total_cost_usd`.
- `UserPromptSubmit` hook `hookSpecificOutput.updatedPrompt` changed to `hookSpecificOutput.additionalContext`.

  - *Source*: [Cost Tracking](https://platform.claude.com/docs/en/agent-sdk/cost-tracking.md)

---

## Migration Guidance

### `can_use_tool` callback in Python

Callbacks returning `bool` must be updated:

```python
# Before
async def can_use_tool(tool: str, input: dict) -> bool:
    return True  # or False

# After
from claude_agent_sdk import PermissionResultAllow, PermissionResultDeny
from claude_agent_sdk.types import ToolPermissionContext

async def can_use_tool(
    tool: str, input: dict, context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    return PermissionResultAllow()  # or PermissionResultDeny(message="reason")
```

### `maxThinkingTokens` → `thinking` (TypeScript and Python)

```typescript
// Before (TypeScript)
options: { maxThinkingTokens: 8000 }

// After (TypeScript)
options: { thinking: { type: "enabled", budget_tokens: 8000 } }
```

```python
# Before (Python)
ClaudeAgentOptions(max_thinking_tokens=8000)

# After (Python)
ClaudeAgentOptions(thinking={"type": "enabled", "budget_tokens": 8000})
```

### `ToolInput` → `ToolInputSchemas` (TypeScript)

Any code importing `ToolInput` from `@anthropic-ai/claude-agent-sdk` should update to `ToolInputSchemas`. `BashOutputInput` and `KillBash` have been removed from the union; `TaskOutputInput`, `ConfigInput`, `EnterWorktreeInput`, and `ExitPlanModeInput` are added.

### Sandbox behavior defaults (Python and TypeScript)

If your application relies on `autoAllowBashIfSandboxed: false` or `allowUnsandboxedCommands: false`, these must now be explicitly set:

```python
ClaudeAgentOptions(sandbox={
    "enabled": True,
    "autoAllowBashIfSandboxed": False,  # must be explicit now
    "allowUnsandboxedCommands": False,  # must be explicit now
})
```

### V2 Preview `Session` → `SDKSession`

Any code referring to the `Session` type should update to `SDKSession`. The `send()` method now accepts `string | SDKUserMessage`. Check `result.subtype === "success"` before accessing `.result` on `unstable_v2_prompt()` return values.

---

## Notable Details

- `UserPromptSubmit` hook output: `updatedPrompt` has been replaced with `additionalContext`. Applications using `updatedPrompt` to inject context into prompts need to update their hook output.
- `StreamEvent` import path now explicitly documented: `from claude_agent_sdk.types import StreamEvent`.
- `CLINotFoundError` message in Python updated to suggest `pip install --force-reinstall claude-agent-sdk` instead of an npm install command.
- TypeScript `env` option documentation now notes `CLAUDE_AGENT_SDK_CLIENT_APP` as a recognized environment variable to identify the calling application in the `User-Agent` header.
- `SDKSystemMessage` now exposes `claude_code_version` — useful for logging and debugging version mismatches.
- MCP code examples across `mcp.md` and `quickstart.md` now use `hidelines={1,-1}` to wrap bare object literals in `const _ = {...}` for syntactic validity, with the wrapper hidden in rendered output.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|:-----|:-----|:-------------|:--------|
| typescript.md | Modified | +1032 / -651 | `listSessions()`, expanded `Query` interface, new Options, new hook events, new message types, renamed types |
| python.md | Modified | +422 / -82 | `Transport` type, hooks/tools in `query()`, new `ClaudeSDKClient` methods, expanded `ClaudeAgentOptions`, typed hooks |
| cost-tracking.md | Modified | +123 / -289 | Page restructured to simpler streaming examples; Python/TypeScript granularity differences documented |
| custom-tools.md | Modified | +101 / -51 | Code formatting only (array/object literal style) |
| mcp.md | Modified | +91 / -75 | TypeScript code examples wrapped for syntactic validity with `hidelines` |
| typescript-v2-preview.md | Modified | +27 / -24 | `Session` → `SDKSession`, new `sessionId` property, `send()` accepts `SDKUserMessage` |
| quickstart.md | Modified | +22 / -16 | TypeScript code examples reformatted with `hidelines` |
| structured-outputs.md | Modified | +16 / -13 | Code formatting only |
| migration-guide.md | Modified | +7 / -7 | JSON before/after labels moved outside code blocks |
| subagents.md | Modified | +4 / -2 | Code formatting only |
| user-input.md | Modified | +5 / -2 | Minor clarifications |
| todo-tracking.md | Modified | +6 / -6 | Arrow function formatting |
| modifying-system-prompts.md | Modified | +3 / -11 | Code formatting only |
| plugins.md | Modified | +3 / -9 | Code formatting only |
| streaming-output.md | Modified | +1 / -1 | Semicolon fix |
| streaming-vs-single-mode.md | Modified | +1 / -1 | Arrow function formatting |
| hooks.md | Modified | +1 / -3 | Minor formatting |

---

*Generated from Claude API documentation changes detected on 2026-02-27*
