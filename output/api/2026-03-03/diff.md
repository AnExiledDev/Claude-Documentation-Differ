# Documentation Diff Report

**Comparing:** `98f6750a2d409877fa602fea27da8e40e7d86b1f` → `HEAD`
**Generated:** 2026-03-03T01:11:16.397841+00:00

## Summary

- New pages: 0
- Removed pages: 0
- Modified pages: 59

## Modified Pages

### `docs/api/en/about-claude/models/migration-guide.md`

+2 / -2 lines

**New sections:**
- ## Get help

**Removed sections:**
- ## Need help?

### `docs/api/en/about-claude/models/whats-new-claude-4-6.md`

+1 / -1 lines

### `docs/api/en/about-claude/use-case-guides/customer-support-chat.md`

+24 / -24 lines

### `docs/api/en/about-claude/use-case-guides/legal-summarization.md`

+10 / -10 lines

### `docs/api/en/about-claude/use-case-guides/ticket-routing.md`

+4 / -4 lines

### `docs/api/en/agent-sdk/file-checkpointing.md`

+6 / -53 lines

### `docs/api/en/agent-sdk/migration-guide.md`

+6 / -6 lines

**New sections:**
- # BEFORE (claude-code-sdk)
- # AFTER (claude-agent-sdk)

**Removed sections:**
- # BEFORE (v0.0.x)
- # AFTER (v0.1.0)

### `docs/api/en/agent-sdk/stop-reasons.md`

+47 / -71 lines

**New sections:**
- # Handle stop reasons
- ## Read stop_reason
- ## Detect refusals
- ## Read stop_reason in Python

**Removed sections:**
- # Handling stop reasons
- ## Reading stop_reason
- # stop_reason might be "end_turn" or "tool_use"
- # depending on what the model was doing when the limit hit
- ## Detecting refusals

### `docs/api/en/agent-sdk/typescript.md`

+5 / -5 lines

### `docs/api/en/agents-and-tools/agent-skills/best-practices.md`

+73 / -73 lines

### `docs/api/en/agents-and-tools/agent-skills/quickstart.md`

+11 / -11 lines

**New sections:**
- ## Agent Skills overview

**Removed sections:**
- ## What are Agent Skills?

### `docs/api/en/agents-and-tools/mcp-connector.md`

+1 / -1 lines

### `docs/api/en/agents-and-tools/tool-use/bash-tool.md`

+9 / -9 lines

### `docs/api/en/agents-and-tools/tool-use/code-execution-tool.md`

+1 / -1 lines

### `docs/api/en/agents-and-tools/tool-use/computer-use-tool.md`

+7 / -7 lines

### `docs/api/en/agents-and-tools/tool-use/fine-grained-tool-streaming.md`

+1 / -1 lines

### `docs/api/en/agents-and-tools/tool-use/implement-tool-use.md`

+1 / -1 lines

### `docs/api/en/agents-and-tools/tool-use/memory-tool.md`

+1 / -1 lines

### `docs/api/en/agents-and-tools/tool-use/overview.md`

+2 / -2 lines

### `docs/api/en/agents-and-tools/tool-use/programmatic-tool-calling.md`

+22 / -22 lines

### `docs/api/en/agents-and-tools/tool-use/text-editor-tool.md`

+13 / -13 lines

### `docs/api/en/agents-and-tools/tool-use/tool-search-tool.md`

+17 / -17 lines

### `docs/api/en/agents-and-tools/tool-use/web-fetch-tool.md`

+6 / -6 lines

### `docs/api/en/agents-and-tools/tool-use/web-search-tool.md`

+4 / -4 lines

### `docs/api/en/api/errors.md`

+1 / -1 lines

### `docs/api/en/api/openai-sdk.md`

+5 / -5 lines

**New sections:**
- ### System / developer message hoisting
- ## Detailed OpenAI compatible API support

**Removed sections:**
- ### System / Developer message hoisting
- ## Detailed OpenAI Compatible API Support

### `docs/api/en/api/sdks/csharp.md`

+3 / -3 lines

### `docs/api/en/api/sdks/go.md`

+2 / -2 lines

### `docs/api/en/api/sdks/java.md`

+5 / -5 lines

### `docs/api/en/api/sdks/php.md`

+1 / -1 lines

### `docs/api/en/api/sdks/python.md`

+3 / -3 lines

### `docs/api/en/api/sdks/ruby.md`

+2 / -2 lines

### `docs/api/en/api/sdks/typescript.md`

+3 / -3 lines

### `docs/api/en/build-with-claude/adaptive-thinking.md`

+2 / -2 lines

### `docs/api/en/build-with-claude/batch-processing.md`

+4 / -4 lines

### `docs/api/en/build-with-claude/citations.md`

+4 / -4 lines

### `docs/api/en/build-with-claude/claude-in-microsoft-foundry.md`

+24 / -24 lines

### `docs/api/en/build-with-claude/claude-on-amazon-bedrock.md`

+5 / -5 lines

**New sections:**
- ### PDF support on Bedrock

**Removed sections:**
- ### PDF Support on Bedrock

### `docs/api/en/build-with-claude/claude-on-vertex-ai.md`

+6 / -6 lines

**New sections:**
- ### Model availability

**Removed sections:**
- ### Model Availability

### `docs/api/en/build-with-claude/compaction.md`

+1 / -1 lines

### `docs/api/en/build-with-claude/context-editing.md`

+1 / -1 lines

### `docs/api/en/build-with-claude/context-windows.md`

+8 / -4 lines

### `docs/api/en/build-with-claude/data-residency.md`

+11 / -11 lines

### `docs/api/en/build-with-claude/effort.md`

+9 / -9 lines

**New sections:**
- ## When to adjust the effort parameter

**Removed sections:**
- ## When should I adjust the effort parameter?

### `docs/api/en/build-with-claude/embeddings.md`

+1 / -1 lines

### `docs/api/en/build-with-claude/extended-thinking.md`

+1 / -1 lines

### `docs/api/en/build-with-claude/fast-mode.md`

+6 / -6 lines

### `docs/api/en/build-with-claude/files.md`

+1 / -1 lines

### `docs/api/en/build-with-claude/handling-stop-reasons.md`

+1 / -1 lines

**New sections:**
- ## The stop_reason field

**Removed sections:**
- ## What is stop_reason?

### `docs/api/en/build-with-claude/pdf-support.md`

+2 / -2 lines

### `docs/api/en/build-with-claude/prompt-caching.md`

+1 / -1 lines

### `docs/api/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md`

+10 / -10 lines

### `docs/api/en/build-with-claude/search-results.md`

+8 / -8 lines

### `docs/api/en/build-with-claude/skills-guide.md`

+12 / -12 lines

### `docs/api/en/build-with-claude/streaming.md`

+3 / -3 lines

### `docs/api/en/build-with-claude/structured-outputs.md`

+9 / -9 lines

### `docs/api/en/build-with-claude/vision.md`

+6 / -6 lines

**New sections:**
- ### Basics and limits

**Removed sections:**
- ### Basics and Limits

### `docs/api/en/build-with-claude/zero-data-retention.md`

+2 / -1 lines

### `docs/api/en/test-and-evaluate/develop-tests.md`

+16 / -16 lines
