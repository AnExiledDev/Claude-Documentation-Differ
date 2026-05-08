# Documentation Diff Report

**Comparing:** `HEAD~1` → `HEAD`
**Generated:** 2026-02-11T01:01:21.949944+00:00

## Summary

- New pages: 0
- Removed pages: 0
- Modified pages: 3

## Modified Pages

### `docs/api/en/agents-and-tools/tool-use/overview.md`

+11 / -2 lines

### `docs/api/en/build-with-claude/compaction.md`

+54 / -3 lines

**New sections:**
- #### Maximizing cache hits with system prompts

### `docs/api/en/build-with-claude/handling-stop-reasons.md`

+34 / -14 lines

**New sections:**
- # Continue the conversation by sending the response back
- # Claude finished processing - return the final response
- # pause_turn: add the assistant's response and continue
- # pause_turn: replace the full message list to maintain alternating roles
- # Reached max continuations - return the last response

**Removed sections:**
- # Continue the conversation
