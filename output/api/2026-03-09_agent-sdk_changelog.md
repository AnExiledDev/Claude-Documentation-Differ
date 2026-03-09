# Claude API Documentation Changes — 2026-03-09

## Summary

All 10 changes in this batch affect the Agent SDK documentation exclusively. The most significant changes are: the subagent orchestration tool has been renamed from `Task` to `Agent` across the SDK (with backward-compatibility guidance for older SDK versions), and two new session-history functions — `list_sessions()` / `listSessions()` and `get_session_messages()` / `getSessionMessages()` — have been added to both the Python and TypeScript SDKs. A new `ToolConfig` type was also documented for TypeScript, and the user-input guide received expanded coverage of option preview formatting.

---

## Significant Changes

### Agent SDK — `Task` Tool Renamed to `Agent`

- **`Task` orchestration tool renamed to `Agent`**: The built-in tool used to spawn subagents has been renamed from `Task` to `Agent` in current SDK releases. All documentation, code examples, and `allowedTools` arrays have been updated to use `"Agent"` instead of `"Task"`.

  > `Agent tool is required for subagent invocation`
  > `allowed_tools=["Read", "Grep", "Glob", "Agent"]`

  Backward-compatibility note added explicitly in the subagents guide:

  > The tool name was renamed from `"Task"` to `"Agent"` in Claude Code v2.1.63. Current SDK releases emit `"Agent"` in `tool_use` blocks but still use `"Task"` in the `system:init` tools list and in `result.permission_denials[].tool_name`. Checking both values in `block.name` ensures compatibility across SDK versions.

  - *Implication*: Any code checking `block.name === "Task"` to detect subagent invocations should be updated to also match `"Agent"`. The subagents page now provides a detection pattern that matches both names for cross-version compatibility.
  - *Source*: [Subagents](https://platform.claude.com/docs/en/agent-sdk/subagents.md), [Agent Loop](https://platform.claude.com/docs/en/agent-sdk/agent-loop.md), [Claude Code Features](https://platform.claude.com/docs/en/agent-sdk/claude-code-features.md), [Overview](https://platform.claude.com/docs/en/agent-sdk/overview.md), [MCP](https://platform.claude.com/docs/en/agent-sdk/mcp.md), [Sessions](https://platform.claude.com/docs/en/agent-sdk/sessions.md)

---

### Python SDK — New Session History Functions

- **`list_sessions()` added**: New synchronous function to discover past sessions with metadata, filterable by project directory.

  ```python
  def list_sessions(
      directory: str | None = None,
      limit: int | None = None,
      include_worktrees: bool = True
  ) -> list[SDKSessionInfo]
  ```

  Returns `SDKSessionInfo` objects with fields: `session_id`, `summary`, `last_modified`, `file_size`, `custom_title`, `first_prompt`, `git_branch`, `cwd`. Results are sorted by `last_modified` descending (newest first). Omitting `directory` searches across all projects.

  - *Implication*: Enables programmatic session discovery for workflows that resume, audit, or replay past agent sessions.
  - *Source*: [Python SDK Reference](https://platform.claude.com/docs/en/agent-sdk/python.md)

- **`get_session_messages()` added**: New synchronous function to read user and assistant messages from a past session transcript.

  ```python
  def get_session_messages(
      session_id: str,
      directory: str | None = None,
      limit: int | None = None,
      offset: int = 0
  ) -> list[SessionMessage]
  ```

  Returns `SessionMessage` objects with fields: `type` (`"user"` | `"assistant"`), `uuid`, `session_id`, `message` (raw content), `parent_tool_use_id`.

  - *Implication*: Allows reading full conversation history from saved sessions, useful for auditing, replaying, or displaying past agent runs.
  - *Source*: [Python SDK Reference](https://platform.claude.com/docs/en/agent-sdk/python.md)

- **New message types documented**: Several new Python type definitions were added to the SDK reference: `McpServerStatus`, `TaskStartedMessage`, `TaskUsage`, `TaskProgressMessage`, `TaskNotificationMessage`, and `Agent` (replacing the previously documented `Task` type).

  - *Source*: [Python SDK Reference](https://platform.claude.com/docs/en/agent-sdk/python.md)

---

### TypeScript SDK — New Session Function and `ToolConfig` Type

- **`getSessionMessages()` added**: New async function to read messages from a past session, complementing the existing `listSessions()`.

  ```typescript
  function getSessionMessages(
    sessionId: string,
    options?: GetSessionMessagesOptions
  ): Promise<SessionMessage[]>;
  ```

  Options: `dir` (project directory), `limit`, `offset`. Returns `SessionMessage[]` with fields: `type`, `uuid`, `session_id`, `message`, `parent_tool_use_id`.

  - *Implication*: Pairs with `listSessions()` to provide full read access to session history from TypeScript applications.
  - *Source*: [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

- **`ToolConfig` type documented**: A new `ToolConfig` type has been added to the TypeScript SDK reference, accessible via the `toolConfig` option on `Options`. This provides configuration for built-in tool behavior.

  - *Implication*: Developers can now configure how built-in tools behave at a per-query level.
  - *Source*: [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

- **`Agent` type replaces `Task` type**: The `Task` message/tool type entries in the TypeScript SDK reference have been replaced with `Agent` (appearing twice in the type documentation, reflecting both tool-use and result contexts).

  - *Source*: [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

---

### Subagents Guide — Backward-Compatible Detection Pattern

- **Detection code updated to match both `"Task"` and `"Agent"` tool names**: All detection examples now check `block.name in ("Task", "Agent")` (Python) or `block.name === "Task" || block.name === "Agent"` (TypeScript) to handle both old and current SDK versions.

  > Check for subagent invocation. Match both names: older SDK versions emitted "Task", current versions emit "Agent".

  - *Implication*: This is the recommended pattern going forward; code that only checks `"Task"` will miss invocations on current SDK versions, and code that only checks `"Agent"` will miss invocations on older SDK versions (pre-v2.1.63).
  - *Source*: [Subagents](https://platform.claude.com/docs/en/agent-sdk/subagents.md)

---

### User Input Guide — Option Previews (TypeScript)

- **New "Option previews" section added for TypeScript**: The user-input guide gained a new subsection (`#### Option previews (TypeScript)`) with approximately 45 lines of new content covering how to display option previews when presenting `AskUserQuestion` choices to users in TypeScript.

  - *Implication*: Provides concrete TypeScript patterns for richer UI rendering of Claude's clarifying question options, beyond simple text display.
  - *Source*: [User Input](https://platform.claude.com/docs/en/agent-sdk/user-input.md)

---

### Hooks Guide — Minor Wording Updates

- **Small clarification to hook documentation**: The hooks guide received minor wording changes (+7/-5 lines) with no section additions or removals. No API-visible changes.
  - *Source*: [Hooks](https://platform.claude.com/docs/en/agent-sdk/hooks.md)

---

## Migration Guidance

### `Task` → `Agent` Tool Rename

All `allowedTools` arrays that include `"Task"` for subagent invocation should be updated to `"Agent"`:

```python
# Before (SDK < v2.1.63)
allowed_tools=["Read", "Grep", "Glob", "Task"]

# After (current SDK)
allowed_tools=["Read", "Grep", "Glob", "Agent"]
```

```typescript
// Before
allowedTools: ["Read", "Grep", "Glob", "Task"]

// After
allowedTools: ["Read", "Grep", "Glob", "Agent"]
```

For detection code that needs to support both old and new SDK versions:

```python
# Compatible detection pattern
if getattr(block, "type", None) == "tool_use" and block.name in ("Task", "Agent"):
    print(f"Subagent invoked: {block.input.get('subagent_type')}")
```

```typescript
// Compatible detection pattern
if (block.type === "tool_use" && (block.name === "Task" || block.name === "Agent")) {
  console.log(`Subagent invoked: ${block.input.subagent_type}`);
}
```

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `agent-sdk/python.md` | Modified | +221/-3 | New `list_sessions()`, `get_session_messages()` functions; new `McpServerStatus`, `TaskStartedMessage`, `TaskUsage`, `TaskProgressMessage`, `TaskNotificationMessage`, `Agent` types; `Task` type removed |
| `agent-sdk/typescript.md` | Modified | +81/-13 | New `getSessionMessages()` function; new `ToolConfig` type; `Agent` type replaces `Task` type (×2) |
| `agent-sdk/subagents.md` | Modified | +40/-31 | All references to `Task` tool updated to `Agent`; backward-compatible detection pattern added |
| `agent-sdk/user-input.md` | Modified | +45/-3 | New "Option previews (TypeScript)" section |
| `agent-sdk/hooks.md` | Modified | +7/-5 | Minor wording clarifications |
| `agent-sdk/overview.md` | Modified | +3/-3 | `Task` → `Agent` tool reference updated |
| `agent-sdk/agent-loop.md` | Modified | +1/-1 | Orchestration tools table: `Task` → `Agent` |
| `agent-sdk/claude-code-features.md` | Modified | +1/-1 | `allowedTools: ["Task"]` → `allowedTools: ["Agent"]` in feature table |
| `agent-sdk/mcp.md` | Modified | +1/-1 | `Task` → `Agent` reference updated |
| `agent-sdk/sessions.md` | Modified | +1/-1 | `Task` → `Agent` reference updated |

---

*Generated from Claude API documentation changes detected on 2026-03-09*
