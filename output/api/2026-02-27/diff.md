# Documentation Diff Report

**Comparing:** `4e005d57cf8eea7207c8eee09ddbd05b75db0502` → `HEAD`
**Generated:** 2026-02-27T01:11:30.475683+00:00

## Summary

- New pages: 0
- Removed pages: 0
- Modified pages: 123

## Modified Pages

### `docs/api/en/agent-sdk/cost-tracking.md`

+123 / -289 lines

**New sections:**
- # Track cost and usage
- ## Understand token usage
- ## Get the total cost of a query
- ## Track detailed usage in TypeScript
- ### Track per-step usage
- ### Break down usage per model
- ## Accumulate costs across multiple calls
- # Track cumulative cost across multiple query() calls
- ## Handle errors, caching, and token discrepancies
- ### Resolve output token discrepancies
- ### Track costs on failed conversations
- ### Track cache tokens
- ## Related documentation

**Removed sections:**
- # Tracking Costs and Usage
- # SDK Cost Tracking
- ## Understanding Token Usage
- ### Key Concepts
- ## Usage Reporting Structure
- ### Single vs Parallel Tool Use
- # Example: Tracking usage in a conversation
- # Process messages as they arrive
- ### Message Flow Example
- ## Important Usage Rules
- ### 1. Same ID = Same Usage
- ### 2. Charge Once Per Step
- ### 3. Result Message Contains Cumulative Usage
- ### 4. Per-Model Usage Breakdown
- ## Implementation: Cost Tracking System
- # Process messages as they arrive
- # Capture the final result message
- # Only process assistant messages with usage
- # Skip if already processed this message ID
- # Mark as processed and record usage
- # Implement your pricing calculation
- # Usage
- ## Handling Edge Cases
- ### Output Token Discrepancies
- ### Cache Token Tracking
- ## Best Practices
- ## Usage Fields Reference
- ## Example: Building a Billing Dashboard
- ## Related Documentation

### `docs/api/en/agent-sdk/custom-tools.md`

+101 / -51 lines

### `docs/api/en/agent-sdk/hooks.md`

+1 / -3 lines

### `docs/api/en/agent-sdk/mcp.md`

+91 / -75 lines

### `docs/api/en/agent-sdk/migration-guide.md`

+7 / -7 lines

### `docs/api/en/agent-sdk/modifying-system-prompts.md`

+3 / -11 lines

### `docs/api/en/agent-sdk/plugins.md`

+3 / -9 lines

### `docs/api/en/agent-sdk/python.md`

+422 / -82 lines

**New sections:**
- ## Choosing between `query()` and `ClaudeSDKClient`
- ### Quick comparison
- ### When to use `query()` (new session each time)
- ### When to use `ClaudeSDKClient` (continuous conversation)
- #### Input schema options
- # Follow-up question - the session retains the previous context
- ### `Transport`
- # Expected dict shape for output_format
- #### Why use setting_sources
- ### `PermissionRuleValue`
- ### `ToolsPreset`
- ### `ThinkingConfig`
- ### `AssistantMessageError`
- ### `PostToolUseFailureHookInput`
- ### `NotificationHookInput`
- ### `SubagentStartHookInput`
- ### `PermissionRequestHookInput`
- #### `HookSpecificOutput`
- # Send message - the session retains all previous messages
- # Add a timestamp as additional context for Claude to see
- # The model is requesting to run this command outside the sandbox
- # Required: dummy hook keeps the stream open for can_use_tool

**Removed sections:**
- ## Choosing Between `query()` and `ClaudeSDKClient`
- ### Quick Comparison
- ### When to Use `query()` (New Session Each Time)
- ### When to Use `ClaudeSDKClient` (Continuous Conversation)
- #### Input Schema Options
- # Follow-up question - Claude remembers the previous context
- #### Why use setting_sources?
- # Send message - Claude remembers all previous messages in this session
- # Add timestamp to all prompts
- # Check if we've received the final result
- # The model wants to run this command outside the sandbox
- # Return True to allow, False to deny

### `docs/api/en/agent-sdk/quickstart.md`

+22 / -16 lines

### `docs/api/en/agent-sdk/streaming-output.md`

+1 / -1 lines

### `docs/api/en/agent-sdk/streaming-vs-single-mode.md`

+1 / -1 lines

### `docs/api/en/agent-sdk/structured-outputs.md`

+16 / -13 lines

### `docs/api/en/agent-sdk/subagents.md`

+4 / -2 lines

### `docs/api/en/agent-sdk/todo-tracking.md`

+6 / -6 lines

### `docs/api/en/agent-sdk/typescript-v2-preview.md`

+27 / -24 lines

**New sections:**
- ### SDKSession interface

**Removed sections:**
- ### Session interface

### `docs/api/en/agent-sdk/typescript.md`

+1032 / -651 lines

**New sections:**
- ### `listSessions()`
- #### Parameters
- #### Return type: `SDKSessionInfo`
- #### Example
- ### `SDKControlInitializeResponse`
- ### `AgentMcpServerSpec`
- #### Why use settingSources
- #### `McpClaudeAIProxyServerConfig`
- #### `SetupHookInput`
- #### `TeammateIdleHookInput`
- #### `TaskCompletedHookInput`
- #### `ConfigChangeHookInput`
- #### `WorktreeCreateHookInput`
- #### `WorktreeRemoveHookInput`
- ### `ToolInputSchemas`
- ### TaskOutput
- ### TaskStop
- ### Config
- ### EnterWorktree
- ### `ToolOutputSchemas`
- ### TaskStop
- ### Config
- ### EnterWorktree
- ### `McpServerStatusConfig`
- ### `ThinkingConfig`
- ### `SpawnedProcess`
- ### `SpawnOptions`
- ### `McpSetServersResult`
- ### `RewindFilesResult`
- ### `SDKStatusMessage`
- ### `SDKTaskNotificationMessage`
- ### `SDKToolUseSummaryMessage`
- ### `SDKHookStartedMessage`
- ### `SDKHookProgressMessage`
- ### `SDKHookResponseMessage`
- ### `SDKToolProgressMessage`
- ### `SDKAuthStatusMessage`
- ### `SDKTaskStartedMessage`
- ### `SDKTaskProgressMessage`
- ### `SDKFilesPersistedEvent`
- ### `SDKRateLimitEvent`
- ### `SDKPromptSuggestionMessage`
- ### `SandboxNetworkConfig`
- ### `SandboxFilesystemConfig`

**Removed sections:**
- #### Why use settingSources?
- ### `ToolInput`
- ### BashOutput
- ### KillBash
- ### `ToolOutput`
- ### BashOutput
- ### KillBash
- ### `NetworkSandboxSettings`
- ### `SandboxIgnoreViolations`

### `docs/api/en/agent-sdk/user-input.md`

+5 / -2 lines

### `docs/api/en/agents-and-tools/agent-skills/quickstart.md`

+48 / -32 lines

### `docs/api/en/agents-and-tools/mcp-connector.md`

+7 / -3 lines

### `docs/api/en/agents-and-tools/tool-use/bash-tool.md`

+6 / -2 lines

### `docs/api/en/agents-and-tools/tool-use/code-execution-tool.md`

+189 / -147 lines

### `docs/api/en/agents-and-tools/tool-use/computer-use-tool.md`

+44 / -14 lines

### `docs/api/en/agents-and-tools/tool-use/fine-grained-tool-streaming.md`

+25 / -21 lines

### `docs/api/en/agents-and-tools/tool-use/implement-tool-use.md`

+65 / -48 lines

### `docs/api/en/agents-and-tools/tool-use/memory-tool.md`

+12 / -7 lines

### `docs/api/en/agents-and-tools/tool-use/overview.md`

+23 / -19 lines

### `docs/api/en/agents-and-tools/tool-use/programmatic-tool-calling.md`

+54 / -23 lines

**New sections:**
- # ...

### `docs/api/en/agents-and-tools/tool-use/text-editor-tool.md`

+8 / -3 lines

### `docs/api/en/agents-and-tools/tool-use/tool-search-tool.md`

+3 / -5 lines

### `docs/api/en/agents-and-tools/tool-use/web-fetch-tool.md`

+10 / -8 lines

### `docs/api/en/agents-and-tools/tool-use/web-search-tool.md`

+8 / -6 lines

### `docs/api/en/api/beta-headers.md`

+1 / -3 lines

### `docs/api/en/api/client-sdks.md`

+1 / -3 lines

### `docs/api/en/api/errors.md`

+1 / -3 lines

### `docs/api/en/api/openai-sdk.md`

+2 / -7 lines

### `docs/api/en/api/sdks/typescript.md`

+31 / -10 lines

### `docs/api/en/build-with-claude/adaptive-thinking.md`

+12 / -8 lines

### `docs/api/en/build-with-claude/batch-processing.md`

+62 / -66 lines

### `docs/api/en/build-with-claude/citations.md`

+3 / -2 lines

### `docs/api/en/build-with-claude/claude-in-microsoft-foundry.md`

+1 / -4 lines

### `docs/api/en/build-with-claude/compaction.md`

+18 / -23 lines

### `docs/api/en/build-with-claude/context-editing.md`

+103 / -69 lines

### `docs/api/en/build-with-claude/context-windows.md`

+1 / -3 lines

### `docs/api/en/build-with-claude/data-residency.md`

+6 / -4 lines

### `docs/api/en/build-with-claude/effort.md`

+6 / -4 lines

### `docs/api/en/build-with-claude/embeddings.md`

+2 / -3 lines

### `docs/api/en/build-with-claude/extended-thinking.md`

+65 / -57 lines

### `docs/api/en/build-with-claude/fast-mode.md`

+6 / -4 lines

### `docs/api/en/build-with-claude/files.md`

+18 / -18 lines

### `docs/api/en/build-with-claude/pdf-support.md`

+8 / -6 lines

### `docs/api/en/build-with-claude/prompt-caching.md`

+30 / -21 lines

### `docs/api/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md`

+3 / -3 lines

### `docs/api/en/build-with-claude/search-results.md`

+10 / -8 lines

### `docs/api/en/build-with-claude/skills-guide.md`

+76 / -89 lines

### `docs/api/en/build-with-claude/streaming.md`

+123 / -16 lines

### `docs/api/en/build-with-claude/structured-outputs.md`

+93 / -45 lines

**New sections:**
- ### Property ordering

### `docs/api/en/build-with-claude/token-counting.md`

+31 / -24 lines

### `docs/api/en/build-with-claude/vision.md`

+9 / -6 lines

### `docs/api/en/build-with-claude/working-with-messages.md`

+22 / -20 lines

### `docs/api/en/get-started.md`

+36 / -33 lines

### `docs/api/en/resources/prompt-library/adaptive-editor.md`

+3 / -6 lines

### `docs/api/en/resources/prompt-library/airport-code-analyst.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/alien-anthropologist.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/alliteration-alchemist.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/babels-broadcasts.md`

+0 / -3 lines

### `docs/api/en/resources/prompt-library/brand-builder.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/career-coach.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/cite-your-sources.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/code-clarifier.md`

+9 / -9 lines

### `docs/api/en/resources/prompt-library/code-consultant.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/corporate-clairvoyant.md`

+0 / -3 lines

### `docs/api/en/resources/prompt-library/csv-converter.md`

+9 / -9 lines

### `docs/api/en/resources/prompt-library/culinary-creator.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/data-organizer.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/direction-decoder.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/dream-interpreter.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/efficiency-estimator.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/email-extractor.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/emoji-encoder.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/ethical-dilemma-navigator.md`

+6 / -5 lines

### `docs/api/en/resources/prompt-library/excel-formula-expert.md`

+10 / -14 lines

### `docs/api/en/resources/prompt-library/function-fabricator.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/futuristic-fashion-advisor.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/git-gud.md`

+0 / -3 lines

### `docs/api/en/resources/prompt-library/google-apps-scripter.md`

+0 / -3 lines

### `docs/api/en/resources/prompt-library/grading-guru.md`

+0 / -3 lines

### `docs/api/en/resources/prompt-library/grammar-genie.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/hal-the-humorous-helper.md`

+6 / -5 lines

### `docs/api/en/resources/prompt-library/idiom-illuminator.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/interview-question-crafter.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/latex-legend.md`

+9 / -9 lines

### `docs/api/en/resources/prompt-library/lesson-planner.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/master-moderator.md`

+0 / -3 lines

### `docs/api/en/resources/prompt-library/meeting-scribe.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/memo-maestro.md`

+9 / -9 lines

### `docs/api/en/resources/prompt-library/mindfulness-mentor.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/mood-colorizer.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/motivational-muse.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/neologism-creator.md`

+0 / -3 lines

### `docs/api/en/resources/prompt-library/perspectives-ponderer.md`

+0 / -3 lines

### `docs/api/en/resources/prompt-library/philosophical-musings.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/pii-purifier.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/polyglot-superpowers.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/portmanteau-poet.md`

+9 / -12 lines

### `docs/api/en/resources/prompt-library/product-naming-pro.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/prose-polisher.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/pun-dit.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/python-bug-buster.md`

+9 / -6 lines

### `docs/api/en/resources/prompt-library/review-classifier.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/riddle-me-this.md`

+0 / -3 lines

### `docs/api/en/resources/prompt-library/sci-fi-scenario-simulator.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/second-grade-simplifier.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/simile-savant.md`

+0 / -3 lines

### `docs/api/en/resources/prompt-library/socratic-sage.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/spreadsheet-sorcerer.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/sql-sorcerer.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/storytelling-sidekick.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/time-travel-consultant.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/tongue-twister.md`

+0 / -3 lines

### `docs/api/en/resources/prompt-library/trivia-generator.md`

+0 / -3 lines

### `docs/api/en/resources/prompt-library/tweet-tone-detector.md`

+6 / -6 lines

### `docs/api/en/resources/prompt-library/vr-fitness-innovator.md`

+0 / -3 lines

### `docs/api/en/resources/prompt-library/website-wizard.md`

+9 / -10 lines
