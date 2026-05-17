# Documentation Diff Report

**Comparing:** `b3d32dba9ed69dbb22c8d30a7016d8147bbdbd33` → `HEAD`
**Generated:** 2026-05-17T01:53:42.886343+00:00

## Summary

- New pages: 0
- Removed pages: 0
- Modified pages: 10

## Modified Pages

### `docs/api/en/agents-and-tools/tool-use/advisor-tool.md`

+13 / -5 lines

### `docs/api/en/agents-and-tools/tool-use/parallel-tool-use.md`

+21 / -2 lines

**New sections:**
- ## Execution semantics

### `docs/api/en/agents-and-tools/tool-use/tool-runner.md`

+1382 / -115 lines

**New sections:**
- ### Taking over message history
- # append_messages() flags state as modified, so the runner skips its
- # automatic append for this iteration. Append the assistant message and
- # tool result yourself, plus any follow-up.
- # When there's no tool call, leave state untouched so the loop exits.
- # Step the runner once. The assistant message and tool result are appended
- # to runner.params[:messages] before next_message returns.
- # Inject a follow-up before continuing. feed_messages takes a splat, not an array.
- # Change parameters in place. Reassigning runner.params[:messages] would tell
- # the runner to skip its automatic append on the next turn.
- ### Automatic context management

**Removed sections:**
- # Optional: inspect the tool response (automatically appended by the runner)
- # Customize the next request
- # Or add additional messages
- # Manual step-by-step control
- # Inject follow-up messages
- # Access current parameters

### `docs/api/en/build-with-claude/claude-in-amazon-bedrock.md`

+2 / -2 lines

### `docs/api/en/build-with-claude/claude-in-microsoft-foundry.md`

+2 / -2 lines

### `docs/api/en/build-with-claude/claude-on-amazon-bedrock-legacy.md`

+2 / -2 lines

### `docs/api/en/build-with-claude/claude-on-vertex-ai.md`

+2 / -2 lines

### `docs/api/en/build-with-claude/claude-platform-on-aws.md`

+2 / -2 lines

### `docs/api/en/get-started.md`

+16 / -11 lines

### `docs/api/en/managed-agents/quickstart.md`

+2 / -2 lines
