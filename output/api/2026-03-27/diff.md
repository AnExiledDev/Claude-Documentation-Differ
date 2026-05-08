# Documentation Diff Report

**Comparing:** `5eac94428c9cb2ccd083f6340823fde26410dc99` → `HEAD`
**Generated:** 2026-03-27T01:07:52.436343+00:00

## Summary

- New pages: 15
- Removed pages: 0
- Modified pages: 38

## New Pages

- `docs/api/en/agents-and-tools/agent-skills/claude-api-skill.md`
- `docs/api/en/agents-and-tools/tool-use/build-a-tool-using-agent.md`
- `docs/api/en/agents-and-tools/tool-use/define-tools.md`
- `docs/api/en/agents-and-tools/tool-use/handle-tool-calls.md`
- `docs/api/en/agents-and-tools/tool-use/how-tool-use-works.md`
- `docs/api/en/agents-and-tools/tool-use/manage-tool-context.md`
- `docs/api/en/agents-and-tools/tool-use/parallel-tool-use.md`
- `docs/api/en/agents-and-tools/tool-use/server-tools.md`
- `docs/api/en/agents-and-tools/tool-use/strict-tool-use.md`
- `docs/api/en/agents-and-tools/tool-use/tool-combinations.md`
- `docs/api/en/agents-and-tools/tool-use/tool-reference.md`
- `docs/api/en/agents-and-tools/tool-use/tool-runner.md`
- `docs/api/en/agents-and-tools/tool-use/tool-use-with-prompt-caching.md`
- `docs/api/en/agents-and-tools/tool-use/troubleshooting-tool-use.md`
- `docs/api/en/build-with-claude/api-and-data-retention.md`

## Modified Pages

### `docs/api/en/about-claude/models/migration-guide.md`

+153 / -149 lines

### `docs/api/en/about-claude/models/whats-new-claude-4-6.md`

+1 / -1 lines

### `docs/api/en/about-claude/pricing.md`

+1 / -1 lines

### `docs/api/en/agents-and-tools/agent-skills/overview.md`

+16 / -0 lines

**New sections:**
- ### Open-source Skills
- ## Data retention

### `docs/api/en/agents-and-tools/mcp-connector.md`

+40 / -34 lines

**New sections:**
- ## Data retention

### `docs/api/en/agents-and-tools/tool-use/bash-tool.md`

+67 / -43 lines

**New sections:**
- # Send command to bash
- # Capture output with timeout
- # Allow only commands from an explicit allowlist
- # Reject shell operators that would chain additional commands

**Removed sections:**
- ## Model compatibility
- # User request
- # Claude's tool uses:
- # 1. Install package
- # 2. Create script
- # 3. Run script
- # Send command to bash
- # Capture output with timeout
- # Block dangerous commands
- # Add more validation as needed

### `docs/api/en/agents-and-tools/tool-use/code-execution-tool.md`

+470 / -1424 lines

**New sections:**
- ### Upload and analyze your own files
- #### Upload and analyze files
- # First, upload a file
- # Then use the file_id with code execution
- # Upload a file
- # Use the file_id with code execution
- # Upload a file
- # Use the file_id with code execution
- #### Retrieve generated files
- # Initialize the client
- # Request code execution that creates files
- # Extract file IDs from the response
- # concrete-typed list: List[BashCodeExecutionOutputBlock]
- # Download the created files
- # concrete-typed list: BashCodeExecutionOutputBlock
- ## Data retention

**Removed sections:**
- ### Execute Bash commands
- ### Create and edit files directly
- ### Upload and analyze your own files
- #### Upload and analyze files
- # First, upload a file
- # Then use the file_id with code execution
- # Upload a file
- # Use the file_id with code execution
- # Upload a file
- # Use the file_id with code execution
- #### Retrieve generated files
- # Initialize the client
- # Request code execution that creates files
- # Extract file IDs from the response
- # Download the created files
- ### Combine operations
- # First, upload a file
- # Extract file_id (using jq)
- # Then use it with code execution
- # Upload a file
- # Use it with code execution
- # Claude might:
- # 1. Use bash to check file size and preview data
- # 2. Use text_editor to write Python code to analyze the CSV and create visualizations
- # 3. Use bash to run the Python code
- # 4. Use text_editor to create a README.md with findings
- # 5. Use bash to organize files into a report directory
- # Enable programmatic calling for your tools

### `docs/api/en/agents-and-tools/tool-use/computer-use-tool.md`

+120 / -611 lines

**New sections:**
- ### Understanding the agentic loop
- ### Combining with extended thinking
- ## Data retention

**Removed sections:**
- ## Model compatibility
- ### Understanding the multi-agent loop
- ### Enable thinking capability in Claude 4 models and Claude Sonnet 3.7

### `docs/api/en/agents-and-tools/tool-use/fine-grained-tool-streaming.md`

+121 / -3 lines

**New sections:**
- ## Accumulating tool input deltas
- ## Next steps

### `docs/api/en/agents-and-tools/tool-use/memory-tool.md`

+20 / -358 lines

**New sections:**
- ## Context editing integration
- ## Next steps

**Removed sections:**
- ## Supported models
- ## Using with Context Editing
- ### How they work together
- ### Example workflow
- ### Configuration
- # Your other tools

### `docs/api/en/agents-and-tools/tool-use/overview.md`

+49 / -2357 lines

**New sections:**
- ## How tool use works
- ## Tool use examples
- ## Next steps
- ### Choose your path

**Removed sections:**
- ## How tool use works
- ### Client tools
- ### Server tools
- ## Using MCP tools with Claude
- ### Converting MCP tools to Claude format
- ## Tool use examples
- ## Next Steps

### `docs/api/en/agents-and-tools/tool-use/programmatic-tool-calling.md`

+99 / -334 lines

**New sections:**
- # Process results programmatically
- ## Data retention

**Removed sections:**
- # async wrapper omitted for clarity
- # Process results programmatically
- # async wrapper omitted for clarity
- # async wrapper omitted for clarity
- # async wrapper omitted for clarity
- # Provide error information in the tool result

### `docs/api/en/agents-and-tools/tool-use/text-editor-tool.md`

+78 / -232 lines

**Removed sections:**
- ## Model compatibility
- #### undo_edit
- # Check if it's a Claude 4 model
- # Restore from backup for Claude 3.7

### `docs/api/en/agents-and-tools/tool-use/tool-search-tool.md`

+37 / -852 lines

**New sections:**
- ## Data retention
- ## Next steps

**Removed sections:**
- # First request with tool search
- # Add Claude's response to conversation
- # Second request with cache breakpoint
- # Add assistant response and handle any tool use
- # Extract tool_use blocks and provide tool_results

### `docs/api/en/agents-and-tools/tool-use/web-fetch-tool.md`

+18 / -99 lines

**New sections:**
- ## Next steps

**Removed sections:**
- ## Supported models
- # First request with web fetch
- # Add Claude's response to conversation
- # Second request with cache breakpoint
- # The second response benefits from cached fetch results

### `docs/api/en/agents-and-tools/tool-use/web-search-tool.md`

+18 / -509 lines

**New sections:**
- ## Next steps

**Removed sections:**
- ## Supported models
- # First request with web search and cache breakpoint
- # Add Claude's response to the conversation
- # Second request with cache breakpoint after the search results
- # The second response will benefit from cached search results
- # while still being able to perform new searches if needed

### `docs/api/en/api/sdks/ruby.md`

+1 / -1 lines

### `docs/api/en/build-with-claude/adaptive-thinking.md`

+4 / -0 lines

### `docs/api/en/build-with-claude/batch-processing.md`

+7 / -1 lines

**New sections:**
- ## Data retention

### `docs/api/en/build-with-claude/citations.md`

+4 / -0 lines

### `docs/api/en/build-with-claude/compaction.md`

+4 / -4 lines

### `docs/api/en/build-with-claude/context-editing.md`

+8 / -6 lines

### `docs/api/en/build-with-claude/context-windows.md`

+4 / -0 lines

### `docs/api/en/build-with-claude/data-residency.md`

+4 / -0 lines

### `docs/api/en/build-with-claude/effort.md`

+4 / -0 lines

### `docs/api/en/build-with-claude/extended-thinking.md`

+5 / -1 lines

### `docs/api/en/build-with-claude/fast-mode.md`

+1 / -1 lines

### `docs/api/en/build-with-claude/files.md`

+7 / -1 lines

**New sections:**
- ## Data retention

### `docs/api/en/build-with-claude/handling-stop-reasons.md`

+227 / -4 lines

**New sections:**
- #### Incomplete tool use blocks
- # Check if response was truncated during tool use
- # Check if the last content block is an incomplete tool_use
- # Send the request with higher max_tokens

### `docs/api/en/build-with-claude/overview.md`

+43 / -41 lines

### `docs/api/en/build-with-claude/pdf-support.md`

+4 / -0 lines

### `docs/api/en/build-with-claude/prompt-caching.md`

+32 / -488 lines

**New sections:**
- ## Data retention

**Removed sections:**
- # many more tools

### `docs/api/en/build-with-claude/search-results.md`

+4 / -0 lines

### `docs/api/en/build-with-claude/skills-guide.md`

+9 / -3 lines

**New sections:**
- ## Data retention

### `docs/api/en/build-with-claude/structured-outputs.md`

+8 / -1077 lines

**New sections:**
- ## Data retention

**Removed sections:**
- ### Why strict tool use matters for agents
- ### Quick start
- ### How it works
- ### Common use cases

### `docs/api/en/build-with-claude/token-counting.md`

+2 / -2 lines

### `docs/api/en/build-with-claude/working-with-messages.md`

+1 / -1 lines

### `docs/api/en/release-notes/overview.md`

+3 / -3 lines
