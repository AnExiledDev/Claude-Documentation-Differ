# Documentation Diff Report

**Comparing:** `49920206b8fd6aeed1c134d9cfcc463ede7a288a` → `HEAD`
**Generated:** 2026-03-07T01:07:06.008675+00:00

## Summary

- New pages: 2
- Removed pages: 0
- Modified pages: 42

## New Pages

- `docs/api/en/agent-sdk/agent-loop.md`
- `docs/api/en/agent-sdk/claude-code-features.md`

## Modified Pages

### `docs/api/en/about-claude/models/migration-guide.md`

+14 / -13 lines

### `docs/api/en/about-claude/models/whats-new-claude-4-6.md`

+2 / -2 lines

### `docs/api/en/agent-sdk/python.md`

+2 / -1 lines

### `docs/api/en/agent-sdk/sessions.md`

+249 / -169 lines

**New sections:**
- # Work with sessions
- ## Choose an approach
- ### Continue, resume, and fork
- ## Automatic session management
- ### Python: `ClaudeSDKClient`
- # First query: client captures the session ID internally
- # Second query: automatically continues the same session
- ### TypeScript: `continue: true`
- ## Use session options with `query()`
- ### Capture the session ID
- ### Resume by ID
- # Earlier session analyzed the code; now build on that analysis
- ### Fork to explore alternatives
- # Fork: branch from session_id into a new session
- # Original session is untouched; resuming it continues the JWT thread
- ## Resume across hosts
- ## Related resources

**Removed sections:**
- # Session Management
- # Session Management
- ## How Sessions Work
- ### Getting the Session ID
- # The first message is a system init message with the session ID
- # You can save this ID for later resumption
- # Process other messages...
- # Later, you can use the saved session_id to resume
- ## Resuming Sessions
- # Resume a previous session using its ID
- # The conversation continues with full context from the previous session
- ## Forking Sessions
- ### When to Fork a Session
- ### Forking vs Continuing
- ### Example: Forking a Session
- # First, capture the session ID
- # Fork the session to try a different approach
- # This will be a different session ID
- # The original session remains unchanged and can still be resumed

### `docs/api/en/agent-sdk/subagents.md`

+21 / -6 lines

**New sections:**
- ### Context isolation
- ## What subagents inherit

**Removed sections:**
- ### Context management

### `docs/api/en/agent-sdk/typescript.md`

+2 / -2 lines

### `docs/api/en/agents-and-tools/mcp-connector.md`

+3 / -2 lines

### `docs/api/en/agents-and-tools/tool-use/code-execution-tool.md`

+2 / -2 lines

### `docs/api/en/agents-and-tools/tool-use/computer-use-tool.md`

+1 / -1 lines

### `docs/api/en/agents-and-tools/tool-use/fine-grained-tool-streaming.md`

+1 / -1 lines

### `docs/api/en/agents-and-tools/tool-use/implement-tool-use.md`

+28 / -19 lines

### `docs/api/en/agents-and-tools/tool-use/memory-tool.md`

+1 / -1 lines

### `docs/api/en/agents-and-tools/tool-use/overview.md`

+6 / -2 lines

### `docs/api/en/agents-and-tools/tool-use/programmatic-tool-calling.md`

+2 / -7 lines

### `docs/api/en/agents-and-tools/tool-use/text-editor-tool.md`

+1 / -1 lines

### `docs/api/en/agents-and-tools/tool-use/tool-search-tool.md`

+2 / -1 lines

### `docs/api/en/agents-and-tools/tool-use/web-fetch-tool.md`

+143 / -2 lines

### `docs/api/en/agents-and-tools/tool-use/web-search-tool.md`

+147 / -3 lines

### `docs/api/en/api/errors.md`

+1 / -2 lines

### `docs/api/en/api/sdks/csharp.md`

+4 / -1 lines

### `docs/api/en/api/sdks/ruby.md`

+14 / -8 lines

### `docs/api/en/api/sdks/typescript.md`

+1 / -5 lines

### `docs/api/en/build-with-claude/batch-processing.md`

+41 / -15 lines

### `docs/api/en/build-with-claude/claude-in-microsoft-foundry.md`

+4 / -2 lines

### `docs/api/en/build-with-claude/claude-on-amazon-bedrock.md`

+17 / -9 lines

### `docs/api/en/build-with-claude/claude-on-vertex-ai.md`

+2 / -1 lines

### `docs/api/en/build-with-claude/compaction.md`

+1 / -1 lines

### `docs/api/en/build-with-claude/context-editing.md`

+3 / -3 lines

### `docs/api/en/build-with-claude/context-windows.md`

+1 / -1 lines

### `docs/api/en/build-with-claude/extended-thinking.md`

+10 / -10 lines

### `docs/api/en/build-with-claude/fast-mode.md`

+311 / -13 lines

### `docs/api/en/build-with-claude/files.md`

+3 / -3 lines

### `docs/api/en/build-with-claude/handling-stop-reasons.md`

+5 / -5 lines

### `docs/api/en/build-with-claude/overview.md`

+2 / -2 lines

### `docs/api/en/build-with-claude/prompt-caching.md`

+108 / -9 lines

**Removed sections:**
- # many more tools

### `docs/api/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md`

+6 / -6 lines

### `docs/api/en/build-with-claude/skills-guide.md`

+5 / -6 lines

### `docs/api/en/build-with-claude/structured-outputs.md`

+75 / -64 lines

### `docs/api/en/build-with-claude/token-counting.md`

+36 / -29 lines

### `docs/api/en/build-with-claude/vision.md`

+446 / -24 lines

**New sections:**
- # Upload the image file
- # Use the uploaded file in a message

### `docs/api/en/build-with-claude/working-with-messages.md`

+3 / -3 lines

### `docs/api/en/build-with-claude/zero-data-retention.md`

+6 / -6 lines

**New sections:**
- ### ZDR-eligible

**Removed sections:**
- ### Fully ZDR-eligible
