# Claude API Documentation Changes — 2026-03-29

## Summary

One page was modified in the agents-and-tools section. The change is a minor clarification in the tool use overview, improving the description of how client tools return results to the caller. No pages were added or removed.

## Significant Changes

### Tools

- **Client tool response clarification**: The description of how client tool calls are returned was updated to explicitly name the `stop_reason` field and mention the possibility of multiple `tool_use` blocks.
  > Before: "Claude returns a `tool_use` block, your code executes the operation, and you send back a `tool_result`."
  >
  > After: "Claude responds with `stop_reason: "tool_use"` and one or more `tool_use` blocks, your code executes the operation, and you send back a `tool_result`."
  - *Implication*: Developers handling tool calls programmatically should be aware that `stop_reason` is the correct signal to check for a pending tool call, and that a single response may contain multiple `tool_use` blocks requiring sequential or parallel execution.
  - *Source*: [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/agents-and-tools/tool-use/overview.md` | Modified | +1 / -1 | Clarified client tool response structure: added `stop_reason: "tool_use"` and noted multiple `tool_use` blocks are possible |
