# Documentation Diff Report

**Comparing:** `4aa266400dde1a9f1bc9a77ff3d065c04b46c785` → `HEAD`
**Generated:** 2026-03-05T01:10:09.577346+00:00

## Summary

- New pages: 0
- Removed pages: 0
- Modified pages: 168

## Modified Pages

### `docs/api/en/about-claude/models/migration-guide.md`

+729 / -69 lines

**New sections:**
- #### If you're using extended thinking

**Removed sections:**
- #### If you're using extended thinking

### `docs/api/en/about-claude/models/whats-new-claude-4-6.md`

+3 / -3 lines

### `docs/api/en/about-claude/pricing.md`

+29 / -11 lines

**New sections:**
- ### Prompt caching

### `docs/api/en/about-claude/use-case-guides/content-moderation.md`

+4 / -4 lines

### `docs/api/en/about-claude/use-case-guides/customer-support-chat.md`

+3 / -3 lines

### `docs/api/en/about-claude/use-case-guides/legal-summarization.md`

+3 / -3 lines

### `docs/api/en/about-claude/use-case-guides/ticket-routing.md`

+4 / -3 lines

### `docs/api/en/agent-sdk/overview.md`

+4 / -5 lines

### `docs/api/en/agent-sdk/permissions.md`

+50 / -9 lines

**New sections:**
- ## Allow and deny rules
- #### Don't ask mode (`dontAsk`, TypeScript only)

### `docs/api/en/agent-sdk/python.md`

+2 / -2 lines

### `docs/api/en/agent-sdk/quickstart.md`

+3 / -2 lines

### `docs/api/en/agent-sdk/skills.md`

+4 / -4 lines

### `docs/api/en/agent-sdk/typescript.md`

+2 / -2 lines

### `docs/api/en/agents-and-tools/agent-skills/best-practices.md`

+8 / -4 lines

### `docs/api/en/agents-and-tools/agent-skills/quickstart.md`

+9 / -5 lines

### `docs/api/en/agents-and-tools/mcp-connector.md`

+203 / -20 lines

### `docs/api/en/agents-and-tools/tool-use/bash-tool.md`

+9 / -5 lines

### `docs/api/en/agents-and-tools/tool-use/code-execution-tool.md`

+1686 / -130 lines

**New sections:**
- # Upload a file
- # Use the file_id with code execution
- # Use it with code execution
- # Claude might:
- # 1. Use bash to check file size and preview data
- # 2. Use text_editor to write Python code to analyze the CSV and create visualizations
- # 3. Use bash to run the Python code
- # 4. Use text_editor to create a README.md with findings
- # 5. Use bash to organize files into a report directory
- # First request: Create a file with a random number
- # Extract container ID from the response (using jq)
- # Second request: Reuse the container to read the file

**Removed sections:**
- # Use it with code execution
- # Claude might:
- # 1. Use bash to check file size and preview data
- # 2. Use text_editor to write Python code to analyze the CSV and create visualizations
- # 3. Use bash to run the Python code
- # 4. Use text_editor to create a README.md with findings
- # 5. Use bash to organize files into a report directory
- # First request: Create a file with a random number
- # Extract container ID from the response (using jq)
- # Second request: Reuse the container to read the file

### `docs/api/en/agents-and-tools/tool-use/computer-use-tool.md`

+588 / -118 lines

### `docs/api/en/agents-and-tools/tool-use/fine-grained-tool-streaming.md`

+9 / -5 lines

### `docs/api/en/agents-and-tools/tool-use/implement-tool-use.md`

+2032 / -204 lines

**New sections:**
- # Extract tool use blocks from response
- # Build tool results with actual IDs

### `docs/api/en/agents-and-tools/tool-use/memory-tool.md`

+371 / -6 lines

### `docs/api/en/agents-and-tools/tool-use/overview.md`

+1225 / -17 lines

### `docs/api/en/agents-and-tools/tool-use/programmatic-tool-calling.md`

+778 / -20 lines

**Removed sections:**
- # ...

### `docs/api/en/agents-and-tools/tool-use/text-editor-tool.md`

+44 / -42 lines

### `docs/api/en/agents-and-tools/tool-use/tool-search-tool.md`

+960 / -9 lines

**New sections:**
- # Add assistant response and handle any tool use
- # Extract tool_use blocks and provide tool_results

### `docs/api/en/agents-and-tools/tool-use/web-fetch-tool.md`

+146 / -10 lines

### `docs/api/en/agents-and-tools/tool-use/web-search-tool.md`

+521 / -11 lines

### `docs/api/en/api/beta-headers.md`

+1 / -1 lines

### `docs/api/en/api/beta.md`

+253 / -561 lines

### `docs/api/en/api/beta/messages.md`

+253 / -561 lines

### `docs/api/en/api/beta/messages/batches.md`

+115 / -255 lines

### `docs/api/en/api/beta/messages/batches/create.md`

+23 / -51 lines

### `docs/api/en/api/beta/messages/batches/results.md`

+23 / -51 lines

### `docs/api/en/api/beta/messages/count_tokens.md`

+23 / -51 lines

### `docs/api/en/api/beta/messages/create.md`

+46 / -102 lines

### `docs/api/en/api/client-sdks.md`

+117 / -88 lines

### `docs/api/en/api/completions.md`

+69 / -153 lines

### `docs/api/en/api/completions/create.md`

+46 / -102 lines

### `docs/api/en/api/csharp/beta.md`

+198 / -450 lines

### `docs/api/en/api/csharp/beta/messages.md`

+198 / -450 lines

### `docs/api/en/api/csharp/beta/messages/batches.md`

+110 / -250 lines

### `docs/api/en/api/csharp/beta/messages/batches/create.md`

+22 / -50 lines

### `docs/api/en/api/csharp/beta/messages/batches/results.md`

+22 / -50 lines

### `docs/api/en/api/csharp/beta/messages/create.md`

+22 / -50 lines

### `docs/api/en/api/csharp/messages.md`

+198 / -450 lines

### `docs/api/en/api/csharp/messages/batches.md`

+110 / -250 lines

### `docs/api/en/api/csharp/messages/batches/create.md`

+22 / -50 lines

### `docs/api/en/api/csharp/messages/batches/results.md`

+22 / -50 lines

### `docs/api/en/api/csharp/messages/create.md`

+22 / -50 lines

### `docs/api/en/api/errors.md`

+3 / -2 lines

### `docs/api/en/api/go/beta.md`

+203 / -452 lines

### `docs/api/en/api/go/beta/messages.md`

+203 / -452 lines

### `docs/api/en/api/go/beta/messages/batches.md`

+115 / -252 lines

### `docs/api/en/api/go/beta/messages/batches/create.md`

+22 / -50 lines

### `docs/api/en/api/go/beta/messages/batches/results.md`

+27 / -52 lines

### `docs/api/en/api/go/beta/messages/create.md`

+22 / -50 lines

### `docs/api/en/api/go/completions.md`

+44 / -100 lines

### `docs/api/en/api/go/completions/create.md`

+22 / -50 lines

### `docs/api/en/api/go/messages.md`

+225 / -502 lines

### `docs/api/en/api/go/messages/batches.md`

+115 / -252 lines

### `docs/api/en/api/go/messages/batches/create.md`

+22 / -50 lines

### `docs/api/en/api/go/messages/batches/results.md`

+27 / -52 lines

### `docs/api/en/api/go/messages/create.md`

+22 / -50 lines

### `docs/api/en/api/java/beta.md`

+198 / -450 lines

### `docs/api/en/api/java/beta/messages.md`

+198 / -450 lines

### `docs/api/en/api/java/beta/messages/batches.md`

+110 / -250 lines

### `docs/api/en/api/java/beta/messages/batches/create.md`

+22 / -50 lines

### `docs/api/en/api/java/beta/messages/batches/results.md`

+22 / -50 lines

### `docs/api/en/api/java/beta/messages/create.md`

+22 / -50 lines

### `docs/api/en/api/java/completions.md`

+44 / -100 lines

### `docs/api/en/api/java/completions/create.md`

+22 / -50 lines

### `docs/api/en/api/java/messages.md`

+198 / -450 lines

### `docs/api/en/api/java/messages/batches.md`

+110 / -250 lines

### `docs/api/en/api/java/messages/batches/create.md`

+22 / -50 lines

### `docs/api/en/api/java/messages/batches/results.md`

+22 / -50 lines

### `docs/api/en/api/java/messages/create.md`

+22 / -50 lines

### `docs/api/en/api/messages.md`

+277 / -613 lines

### `docs/api/en/api/messages/batches.md`

+115 / -255 lines

### `docs/api/en/api/messages/batches/create.md`

+23 / -51 lines

### `docs/api/en/api/messages/batches/results.md`

+23 / -51 lines

### `docs/api/en/api/messages/count_tokens.md`

+23 / -51 lines

### `docs/api/en/api/messages/create.md`

+46 / -102 lines

### `docs/api/en/api/openai-sdk.md`

+23 / -6 lines

### `docs/api/en/api/python/beta.md`

+391 / -776 lines

### `docs/api/en/api/python/beta/messages.md`

+391 / -776 lines

### `docs/api/en/api/python/beta/messages/batches.md`

+178 / -353 lines

### `docs/api/en/api/python/beta/messages/batches/create.md`

+35 / -70 lines

### `docs/api/en/api/python/beta/messages/batches/results.md`

+38 / -73 lines

### `docs/api/en/api/python/beta/messages/count_tokens.md`

+35 / -70 lines

### `docs/api/en/api/python/beta/messages/create.md`

+73 / -143 lines

### `docs/api/en/api/python/completions.md`

+108 / -213 lines

### `docs/api/en/api/python/completions/create.md`

+73 / -143 lines

### `docs/api/en/api/python/messages.md`

+427 / -847 lines

### `docs/api/en/api/python/messages/batches.md`

+178 / -353 lines

### `docs/api/en/api/python/messages/batches/create.md`

+35 / -70 lines

### `docs/api/en/api/python/messages/batches/results.md`

+38 / -73 lines

### `docs/api/en/api/python/messages/count_tokens.md`

+35 / -70 lines

### `docs/api/en/api/python/messages/create.md`

+73 / -143 lines

### `docs/api/en/api/ruby/beta.md`

+254 / -564 lines

### `docs/api/en/api/ruby/beta/messages.md`

+254 / -564 lines

### `docs/api/en/api/ruby/beta/messages/batches.md`

+115 / -255 lines

### `docs/api/en/api/ruby/beta/messages/batches/create.md`

+23 / -51 lines

### `docs/api/en/api/ruby/beta/messages/batches/results.md`

+23 / -51 lines

### `docs/api/en/api/ruby/beta/messages/count_tokens.md`

+23 / -51 lines

### `docs/api/en/api/ruby/beta/messages/create.md`

+47 / -105 lines

### `docs/api/en/api/ruby/completions.md`

+70 / -156 lines

### `docs/api/en/api/ruby/completions/create.md`

+47 / -105 lines

### `docs/api/en/api/ruby/messages.md`

+278 / -616 lines

### `docs/api/en/api/ruby/messages/batches.md`

+115 / -255 lines

### `docs/api/en/api/ruby/messages/batches/create.md`

+23 / -51 lines

### `docs/api/en/api/ruby/messages/batches/results.md`

+23 / -51 lines

### `docs/api/en/api/ruby/messages/count_tokens.md`

+23 / -51 lines

### `docs/api/en/api/ruby/messages/create.md`

+47 / -105 lines

### `docs/api/en/api/sdks/csharp.md`

+14 / -14 lines

### `docs/api/en/api/sdks/go.md`

+186 / -149 lines

**Removed sections:**
- ## Streaming

### `docs/api/en/api/sdks/java.md`

+49 / -49 lines

### `docs/api/en/api/sdks/php.md`

+12 / -4 lines

### `docs/api/en/api/sdks/python.md`

+29 / -20 lines

### `docs/api/en/api/sdks/ruby.md`

+18 / -6 lines

### `docs/api/en/api/sdks/typescript.md`

+28 / -25 lines

### `docs/api/en/api/typescript/beta.md`

+256 / -564 lines

### `docs/api/en/api/typescript/beta/messages.md`

+256 / -564 lines

### `docs/api/en/api/typescript/beta/messages/batches.md`

+115 / -255 lines

### `docs/api/en/api/typescript/beta/messages/batches/create.md`

+23 / -51 lines

### `docs/api/en/api/typescript/beta/messages/batches/results.md`

+23 / -51 lines

### `docs/api/en/api/typescript/beta/messages/count_tokens.md`

+23 / -51 lines

### `docs/api/en/api/typescript/beta/messages/create.md`

+49 / -105 lines

### `docs/api/en/api/typescript/completions.md`

+72 / -156 lines

### `docs/api/en/api/typescript/completions/create.md`

+49 / -105 lines

### `docs/api/en/api/typescript/messages.md`

+280 / -616 lines

### `docs/api/en/api/typescript/messages/batches.md`

+115 / -255 lines

### `docs/api/en/api/typescript/messages/batches/create.md`

+23 / -51 lines

### `docs/api/en/api/typescript/messages/batches/results.md`

+23 / -51 lines

### `docs/api/en/api/typescript/messages/count_tokens.md`

+23 / -51 lines

### `docs/api/en/api/typescript/messages/create.md`

+49 / -105 lines

### `docs/api/en/build-with-claude/adaptive-thinking.md`

+506 / -70 lines

**Removed sections:**
- ### Thinking redaction

### `docs/api/en/build-with-claude/batch-processing.md`

+827 / -169 lines

**New sections:**
- ### Listing all Message Batches
- # Automatically fetches more pages as needed.
- # Automatically fetches more pages as needed

**Removed sections:**
- ### Listing all Message Batches
- # Automatically fetches more pages as needed.

### `docs/api/en/build-with-claude/citations.md`

+37 / -36 lines

### `docs/api/en/build-with-claude/claude-in-microsoft-foundry.md`

+177 / -84 lines

**New sections:**
- # Get Azure Entra ID token
- # Make request with token. Replace {resource} with your resource name

**Removed sections:**
- # Get Azure Entra ID token
- # Make request with token. Replace {resource} with your resource name

### `docs/api/en/build-with-claude/claude-on-amazon-bedrock.md`

+362 / -131 lines

### `docs/api/en/build-with-claude/claude-on-vertex-ai.md`

+285 / -107 lines

### `docs/api/en/build-with-claude/compaction.md`

+2246 / -62 lines

**New sections:**
- # Append the response (including any compaction block) to continue the conversation
- #### Maximizing cache hits with system prompts

**Removed sections:**
- #### Maximizing cache hits with system prompts

### `docs/api/en/build-with-claude/context-editing.md`

+1622 / -27 lines

**New sections:**
- # ...
- # ...
- # ...
- # The SDK logs compaction events when verbose logging is enabled.
- # You'll see messages like:
- # Token usage 105000 has exceeded the threshold of 100000. Performing compaction.
- # Compaction complete. New token usage: 2500

### `docs/api/en/build-with-claude/context-windows.md`

+118 / -3 lines

### `docs/api/en/build-with-claude/data-residency.md`

+5 / -2 lines

### `docs/api/en/build-with-claude/effort.md`

+149 / -19 lines

### `docs/api/en/build-with-claude/embeddings.md`

+6 / -5 lines

### `docs/api/en/build-with-claude/extended-thinking.md`

+2124 / -287 lines

**New sections:**
- ### Preserving thinking blocks
- # Fetch book content
- # First request - establish cache
- # Second request - same thinking parameters (cache hit expected)
- # Third request - different thinking parameters (cache miss for messages)

**Removed sections:**
- ### Preserving thinking blocks
- ### Thinking redaction
- # Using a special prompt that triggers redacted thinking (for demonstration purposes only)
- # Identify redacted thinking blocks
- # These blocks are still usable in subsequent requests
- # Extract all blocks (both redacted and non-redacted)
- # When passing to subsequent requests, include all blocks without modification
- # This preserves the integrity of Claude's reasoning

### `docs/api/en/build-with-claude/fast-mode.md`

+133 / -42 lines

### `docs/api/en/build-with-claude/files.md`

+725 / -177 lines

**New sections:**
- # Example: Reading a text file

### `docs/api/en/build-with-claude/handling-stop-reasons.md`

+62 / -16 lines

### `docs/api/en/build-with-claude/multilingual-support.md`

+1 / -4 lines

### `docs/api/en/build-with-claude/pdf-support.md`

+86 / -52 lines

### `docs/api/en/build-with-claude/prompt-caching.md`

+1246 / -22 lines

### `docs/api/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md`

+5 / -5 lines

### `docs/api/en/build-with-claude/prompt-engineering/prompting-tools.md`

+0 / -3 lines

### `docs/api/en/build-with-claude/search-results.md`

+826 / -53 lines

### `docs/api/en/build-with-claude/skills-guide.md`

+3782 / -386 lines

**New sections:**
- ### Downloading Generated Files
- # Step 1: Use a Skill to create a file
- # Step 2: Extract file_id from response (using jq)
- # Step 3: Get filename from metadata
- # Step 4: Download the file using Files API
- # Step 1: Use a Skill to create a file
- # Step 2: Extract file IDs from the response
- # Step 3: Download the file using Files API
- # Step 4: Save to disk
- # Get file metadata
- # List all files
- # Delete a file
- # Get file metadata
- # List all files
- # Delete a file
- # Initial request
- # Check stop_reason and handle pause_turn in a loop
- # Continue with same container
- ### Using Multiple Skills
- # Option 1: Using a zip file
- # Option 2: Using individual files
- # List all Skills
- # List only custom Skills
- # Delete all versions first, then delete the Skill
- # Step 1: Delete all versions
- # Step 2: Delete the Skill
- # Create a new version
- # Use specific version
- # Use latest version
- # Create a new version
- # Create custom DCF analysis Skill
- # Use with Excel to create financial model
- # Create custom DCF analysis Skill
- # Use with Excel to create financial model
- # First request creates cache
- # Adding/removing Skills breaks cache

**Removed sections:**
- ### Downloading Generated Files
- # Step 1: Use a Skill to create a file
- # Step 2: Extract file_id from response (using jq)
- # Step 3: Get filename from metadata
- # Step 4: Download the file using Files API
- # Get file metadata
- # List all files
- # Delete a file
- # Initial request
- # Check stop_reason and handle pause_turn in a loop
- # Continue with same container
- ### Using Multiple Skills
- # Delete all versions first, then delete the Skill
- # Create a new version
- # Create custom DCF analysis Skill
- # Use with Excel to create financial model

### `docs/api/en/build-with-claude/streaming.md`

+947 / -44 lines

### `docs/api/en/build-with-claude/structured-outputs.md`

+2216 / -428 lines

**New sections:**
- #### SDK-specific methods
- # JSON outputs: structured response format
- # Strict tool use: guaranteed tool parameters

**Removed sections:**
- #### SDK-specific methods

### `docs/api/en/build-with-claude/token-counting.md`

+806 / -62 lines

### `docs/api/en/build-with-claude/vision.md`

+125 / -85 lines

### `docs/api/en/build-with-claude/working-with-messages.md`

+706 / -7 lines

**New sections:**
- # Option 1: Base64-encoded image
- # Option 2: URL-referenced image

### `docs/api/en/get-started.md`

+25 / -24 lines

### `docs/api/en/resources/overview.md`

+0 / -4 lines

### `docs/api/en/test-and-evaluate/develop-tests.md`

+2 / -0 lines

### `docs/api/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md`

+206 / -2 lines
