# Claude API Documentation Changes — 2026-03-29

## Summary

The Agent SDK documentation received substantial additions across both the Python and TypeScript SDK reference pages. Three new session-management functions (`get_session_info` / `getSessionInfo`, `rename_session` / `renameSession`, `tag_session` / `tagSession`) were documented in both SDKs, along with new fields on `SDKSessionInfo`. The `ClaudeSDKClient` MCP methods were replaced with a revised API, and two new event types (`RateLimitEvent`, `RateLimitInfo`) were added to the Python message stream model.

## Significant Changes

### Session Management

- **New `get_session_info()` / `getSessionInfo()` functions**: Both SDKs now document a function to read metadata for a single session by ID without scanning the full project directory, returning `SDKSessionInfo | None` (Python) or `SDKSessionInfo | undefined` (TypeScript).
  > "Reads metadata for a single session by ID without scanning the full project directory. Synchronous; returns immediately."
  - *Implication*: Efficient single-session lookup when you already hold a session ID, avoiding a full directory scan.
  - *Source*: [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md), [typescript.md](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

- **New `rename_session()` / `renameSession()` functions**: Both SDKs now document a function to assign a custom title to a session. Repeated calls are safe; the most recent title wins. Python raises `ValueError` on empty title or invalid UUID and `FileNotFoundError` if the session is missing.
  > "Renames a session by appending a custom-title entry. Repeated calls are safe; the most recent title wins."
  - *Implication*: Enables programmatic session labeling for display in custom session pickers or UIs.
  - *Source*: [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md), [typescript.md](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

- **New `tag_session()` / `tagSession()` functions**: Both SDKs now document a function to attach a string tag to a session, or clear it by passing `None` / `null`. Tags are Unicode-sanitized before storing (Python).
  > "Tags a session. Pass `None` to clear the tag. Repeated calls are safe; the most recent tag wins."
  - *Implication*: Tags can be used to group or filter sessions (e.g., `"needs-review"`) across subsequent `list_sessions()` calls.
  - *Source*: [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md), [typescript.md](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

- **New fields on `SDKSessionInfo`**: Both SDKs added `tag` and `createdAt` / `created_at` fields to the session info return type. The `fileSize` / `file_size` field was also updated to be nullable.
  > Python: `tag: str | None` — User-set session tag (see `tag_session()`); `created_at: int | None` — Session creation time in milliseconds since epoch.
  > TypeScript: `fileSize: number | undefined` — Only populated for local JSONL storage; `createdAt: number | undefined` — Creation time in milliseconds since epoch, from the first entry's timestamp.
  - *Implication*: `fileSize` / `file_size` can now be `None` / `undefined` for remote storage backends, which is a behavioral change from the prior strict `int` / `number` type.
  - *Source*: [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md), [typescript.md](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

### MCP Client Methods

- **`ClaudeSDKClient` MCP methods replaced**: The `add_mcp_server()` and `remove_mcp_server()` methods have been removed and replaced with `reconnect_mcp_server()`, `toggle_mcp_server()`, and `stop_task()`. The return type of `get_mcp_status()` changed from `list[McpServerStatus]` to `McpStatusResponse`.
  > "`reconnect_mcp_server(server_name)` — Retry connecting to an MCP server that failed or was disconnected"
  > "`toggle_mcp_server(server_name, enabled)` — Enable or disable an MCP server mid-session. Disabling removes its tools"
  > "`stop_task(task_id)` — Stop a running background task. A `TaskNotificationMessage` with status `"stopped"` follows in the message stream"
  - *Implication*: Code calling `add_mcp_server()` or `remove_mcp_server()` will break; the new methods provide finer-grained MCP lifecycle control.
  - *Source*: [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md)

- **New `McpStatusResponse` and `McpServerStatusConfig` types**: `get_mcp_status()` now returns `McpStatusResponse` (a TypedDict with an `mcpServers` key) rather than a bare list. `McpServerStatusConfig` is a new union type covering all MCP transport variants plus a `claudeai-proxy` variant for servers proxied through claude.ai.
  > "`McpStatusResponse` — Response from `ClaudeSDKClient.get_mcp_status()`. Wraps the list of server statuses under the `mcpServers` key."
  - *Implication*: Callers must update to access `response.mcpServers` instead of iterating the response directly.
  - *Source*: [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md)

### Rate Limiting

- **New `RateLimitEvent` and `RateLimitInfo` types (Python)**: The `Message` union now includes `RateLimitEvent`, which fires when rate limit status changes. `RateLimitInfo` carries status (`"allowed"`, `"allowed_warning"`, `"rejected"`), reset timestamps, utilization fraction, and overage fields.
  > "Emitted when rate limit status changes (for example, from `"allowed"` to `"allowed_warning"`). Use this to warn users before they hit a hard limit, or to back off when status is `"rejected"`."
  - *Implication*: Applications can now react to rate limit warnings proactively by handling `RateLimitEvent` in the message stream.
  - *Source*: [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md)

### AgentDefinition (Subagents)

- **New fields on `AgentDefinition`**: Three new optional fields were added: `skills` (list of skill names), `memory` (memory source: `"user"`, `"project"`, or `"local"`), and `mcpServers` (MCP servers available to the agent by name or inline config).
  > "`skills` — List of skill names available to this agent; `memory` — Memory source for this agent: `"user"`, `"project"`, or `"local"`; `mcpServers` — MCP servers available to this agent."
  - *Implication*: Subagents can now be given isolated skill sets, memory scopes, and MCP server access without inheriting everything from the parent.
  - *Source*: [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md), [subagents.md](https://platform.claude.com/docs/en/agent-sdk/subagents.md)

- **`AgentDefinition.skills` availability corrected**: The subagents page previously stated skills were available to subagents in "TypeScript only"; this qualifier has been removed, reflecting Python support as well.
  > Before: "Skills (unless listed in `AgentDefinition.skills`, TypeScript only)"
  > After: "Skills (unless listed in `AgentDefinition.skills`)"
  - *Implication*: Python SDK users can now pass `skills` to `AgentDefinition` to grant subagents specific skill access.
  - *Source*: [subagents.md](https://platform.claude.com/docs/en/agent-sdk/subagents.md)

### AssistantMessage

- **New `usage` field on `AssistantMessage`**: Per-message token usage is now exposed directly on `AssistantMessage` in addition to the existing `ResultMessage.usage`.
  > "`usage: dict[str, Any] | None` — Per-message token usage (same keys as `ResultMessage.usage`)"
  - *Implication*: Developers can track token consumption at the individual assistant message level, not just at turn end.
  - *Source*: [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md)

## Migration Guidance

**Breaking changes requiring code updates:**

1. `ClaudeSDKClient.get_mcp_status()` return type changed from `list[McpServerStatus]` to `McpStatusResponse`. Update callers to use `response.mcpServers` to access the list.
2. `ClaudeSDKClient.add_mcp_server()` and `remove_mcp_server()` are removed. Replace with `reconnect_mcp_server()`, `toggle_mcp_server()`, or `stop_task()` as appropriate.
3. `SDKSessionInfo.file_size` (Python) is now `int | None`; `SDKSessionInfo.fileSize` (TypeScript) is now `number | undefined`. Null-check before use.

## Notable Details

- The skills file path pattern in the overview feature table changed from `.claude/skills/SKILL.md` to `.claude/skills/*/SKILL.md`, indicating skills are now organized in subdirectories.
- The sessions overview page added a paragraph cross-linking to the new session mutation functions (`get_session_info`, `rename_session`, `tag_session`) in both SDKs.
- "Claude platform" was capitalized to "Claude Platform" in the overview comparison table section.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| [overview.md](https://platform.claude.com/docs/en/agent-sdk/overview.md) | Modified | +2 / -2 | Skills path updated to subdirectory pattern; "Claude Platform" capitalization fix |
| [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md) | Modified | +212 / -12 | New session management functions, updated `ClaudeSDKClient` MCP methods, new `RateLimitEvent`/`RateLimitInfo` types, `AgentDefinition` new fields, `AssistantMessage.usage`, updated `McpServerStatus.config` type |
| [typescript.md](https://platform.claude.com/docs/en/agent-sdk/typescript.md) | Modified | +63 / -1 | New session management functions (`getSessionInfo`, `renameSession`, `tagSession`), new `SDKSessionInfo` fields |
| [sessions.md](https://platform.claude.com/docs/en/agent-sdk/sessions.md) | Modified | +2 / -0 | Added paragraph cross-linking new session mutation functions in both SDKs |
| [subagents.md](https://platform.claude.com/docs/en/agent-sdk/subagents.md) | Modified | +4 / -1 | New `AgentDefinition` fields (`skills`, `memory`, `mcpServers`); removed "TypeScript only" qualifier for `skills` |
