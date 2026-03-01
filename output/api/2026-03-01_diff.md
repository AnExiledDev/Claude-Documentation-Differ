# Documentation Diff Report

**Comparing:** `8a5d34c5c398e02c99a35d611d065ffe8ff54696` → `HEAD`
**Generated:** 2026-03-01T01:15:20.347780+00:00

## Summary

- New pages: 0
- Removed pages: 0
- Modified pages: 8

## Modified Pages

### `docs/api/en/agent-sdk/hooks.md`

+333 / -342 lines

**New sections:**
- ## How hooks work
- # Register the hook for PreToolUse events
- # The matcher filters to only Write and Edit tool calls
- # Filter for assistant and result messages
- ### Callback functions
- #### Inputs
- #### Outputs
- #### Asynchronous output
- # Start a background task, then return immediately
- ## Examples
- ### Modify tool input
- ### Add context and block a tool
- # Top-level field: inject guidance into the conversation
- # hookSpecificOutput: block the operation
- ### Auto-approve specific tools
- ### Chain multiple hooks
- ### Filter with regex matchers
- ### Track subagent activity
- # Log subagent details when it finishes
- ### Make HTTP requests from hooks
- # Only fire after a tool completes (PostToolUse), not before
- # Run the blocking HTTP call in a thread to avoid blocking the event loop
- # Log the error but don't raise. A failed webhook shouldn't stop the agent
- ### Forward notifications to Slack
- # Run the blocking HTTP call in a thread to avoid blocking the event loop
- # Return empty object. Notification hooks don't modify agent behavior
- # Register the hook for Notification events (no matcher needed)
- ## Fix common issues
- ### Session hooks not available in Python
- ## Related resources

**Removed sections:**
- # Register the hook for PreToolUse events
- # The matcher filters to only Write and Edit tool calls
- ## Common use cases
- ### Callback function inputs
- ### Input data
- ### Callback outputs
- # Top-level field: inject guidance into the conversation
- # hookSpecificOutput: block the operation
- #### Permission decision flow
- #### Block a tool
- #### Modify tool input
- #### Add a system message
- #### Auto-approve specific tools
- ## Handle advanced scenarios
- ### Chaining multiple hooks
- ### Tool-specific matchers with regex
- ### Tracking subagent activity
- ### Async operations in hooks
- ### Sending notifications (TypeScript only)
- ## Fix common issues
- ### Session hooks not available
- ## Learn more

### `docs/api/en/agent-sdk/python.md`

+5 / -3 lines

### `docs/api/en/agent-sdk/skills.md`

+1 / -1 lines

### `docs/api/en/agent-sdk/typescript.md`

+168 / -124 lines

**New sections:**
- ### `Query` object
- ### `AgentInfo`

**Removed sections:**
- ### `Query`

### `docs/api/en/build-with-claude/prompt-caching.md`

+4 / -4 lines

### `docs/api/en/build-with-claude/prompt-engineering/prompting-tools.md`

+1 / -1 lines

### `docs/api/en/build-with-claude/structured-outputs.md`

+12 / -12 lines

### `docs/api/en/build-with-claude/zero-data-retention.md`

+9 / -5 lines
