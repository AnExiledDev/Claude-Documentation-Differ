# Documentation Diff Report

**Comparing:** `cb463ef578030af41d08f4c09da86f0ec4c81424` → `HEAD`
**Generated:** 2026-03-09T01:09:06.321305+00:00

## Summary

- New pages: 0
- Removed pages: 0
- Modified pages: 11

## Modified Pages

### `docs/api/en/agent-sdk/agent-loop.md`

+1 / -1 lines

### `docs/api/en/agent-sdk/claude-code-features.md`

+1 / -1 lines

### `docs/api/en/agent-sdk/hooks.md`

+7 / -5 lines

### `docs/api/en/agent-sdk/mcp.md`

+1 / -1 lines

### `docs/api/en/agent-sdk/overview.md`

+3 / -3 lines

### `docs/api/en/agent-sdk/python.md`

+221 / -3 lines

**New sections:**
- ### `list_sessions()`
- #### Parameters
- #### Return type: `SDKSessionInfo`
- #### Example
- ### `get_session_messages()`
- #### Parameters
- #### Return type: `SessionMessage`
- #### Example
- ### `McpServerStatus`
- ### `TaskStartedMessage`
- ### `TaskUsage`
- ### `TaskProgressMessage`
- ### `TaskNotificationMessage`
- ### Agent

**Removed sections:**
- ### Task

### `docs/api/en/agent-sdk/sessions.md`

+1 / -1 lines

### `docs/api/en/agent-sdk/subagents.md`

+40 / -31 lines

**New sections:**
- # Agent tool is required for subagent invocation
- # Check for subagent invocation. Match both names: older SDK
- # versions emitted "Task", current versions emit "Agent".
- # Search message content for the agentId (appears in Agent tool results)

**Removed sections:**
- # Task tool is required for subagent invocation
- # Check for subagent invocation in message content
- # Search message content for the agentId (appears in Task tool results)

### `docs/api/en/agent-sdk/typescript.md`

+81 / -13 lines

**New sections:**
- ### `getSessionMessages()`
- #### Parameters
- #### Return type: `SessionMessage`
- #### Example
- ### `ToolConfig`
- ### Agent
- ### Agent

**Removed sections:**
- ### Task
- ### Task

### `docs/api/en/agent-sdk/user-input.md`

+45 / -3 lines

**New sections:**
- #### Option previews (TypeScript)

### `docs/api/en/build-with-claude/extended-thinking.md`

+2 / -2 lines

**New sections:**
- # Let's pretend this is what we get back

**Removed sections:**
- # let's pretend this is what we get back
