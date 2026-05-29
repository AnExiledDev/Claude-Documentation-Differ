# Claude API Documentation Changes — 2026-05-29

## Summary

Documentation across 22 agents-and-tools pages has been updated to reflect the release of **Claude Opus 4.8** (`claude-opus-4-8`). The new model is added to compatibility tables for the code execution tool, programmatic tool calling, advisor tool, computer use tool, and web search/fetch dynamic filtering. Separately, the MCP connector gains a new "Batch requests" section documenting support for `mcp_servers` in the Message Batches API, and the tool use system prompt token counts table has been revised with corrected per-model values.

## Significant Changes

### Models

- **Claude Opus 4.8 released**: All code examples across agents-and-tools documentation have been updated from `claude-opus-4-7` to `claude-opus-4-8` (in some pages, from `claude-opus-4-6`). The change spans curl, CLI, Python, TypeScript, C#, Go, Java, PHP, and Ruby examples across every tool-use page.
  > `"model": "claude-opus-4-8"`
  - *Implication*: `claude-opus-4-8` is now the recommended model for all agents-and-tools workflows.
  - *Source*: [Tool Use Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md)

- **Code execution tool: Opus 4.8 added to compatibility table**: `claude-opus-4-8` has been added as a supported model for both `code_execution_20250825` and `code_execution_20260120` tool versions.
  > `| Claude Opus 4.8 (claude-opus-4-8) | code_execution_20250825, code_execution_20260120 |`
  - *Implication*: Developers can now use code execution (including REPL state persistence and programmatic tool calling) with Claude Opus 4.8.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

- **Programmatic tool calling: Opus 4.8 added to supported model list**: `claude-opus-4-8` has been added to the models that support `code_execution_20260120` (required for programmatic tool calling).
  > `| Claude Opus 4.8 (claude-opus-4-8) |`
  - *Implication*: Claude Opus 4.8 can now execute tools called from within the code execution sandbox.
  - *Source*: [Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md)

- **Advisor tool: Opus 4.8 added as both executor and advisor model**: The executor/advisor compatibility table has a new row for `Claude Opus 4.8` as an executor (paired with itself as advisor), and Claude Opus 4.8 is now listed as a valid advisor for all existing executor models (Haiku 4.5, Sonnet 4.6, Opus 4.6, Opus 4.7).
  > `| Claude Haiku 4.5 (claude-haiku-4-5-20251001) | Claude Opus 4.8 (claude-opus-4-8), Claude Opus 4.7 (claude-opus-4-7) |`
  > `| Claude Opus 4.8 (claude-opus-4-8) | Claude Opus 4.8 (claude-opus-4-8) |`
  - *Implication*: Claude Opus 4.8 can now serve as the advisor model in advisor-tool setups, and can also act as an executor with itself as advisor.
  - *Source*: [Advisor Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md)

- **Computer use tool: Opus 4.8 added to zoom and high-resolution support**: Claude Opus 4.8 is now listed alongside Opus 4.7 for zoom action support and 2576-pixel high-resolution coordinate handling.
  > `Available in Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6, and Claude Opus 4.5:`
  > `Claude Opus 4.8 and Claude Opus 4.7 support up to 2576 pixels on the long edge, and their coordinates are 1:1 with image pixels (no scale-factor conversion required).`
  - *Implication*: Computer use agents on Opus 4.8 can use the zoom action and do not need to apply coordinate scaling for high-resolution screens.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

- **Web search and web fetch: Opus 4.8 added to dynamic filtering support**: Claude Opus 4.8 is now listed as a supported model for the dynamic filtering capability in `web_search_20260209` and `web_fetch_20260209`.
  > `The latest web search tool version (web_search_20260209) supports dynamic filtering with Claude Opus 4.8, [Claude Mythos Preview], Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6.`
  - *Implication*: Agents using Opus 4.8 can now leverage dynamic filtering to reduce token consumption during web searches and fetches.
  - *Source*: [Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool.md), [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md)

### MCP

- **MCP connector: `mcp_servers` now supported in Message Batches API**: A new "## Batch requests" section documents that `mcp_servers` can be included in batch requests, with the same pricing as regular Messages API requests.
  > `You can include mcp_servers in Message Batches API requests. MCP tool calls through the Batches API are priced the same as those in regular Messages API requests.`
  - *Implication*: Developers can now run large-scale MCP-powered workflows via the Batches API, enabling asynchronous processing of many MCP-tool-using requests at once.
  - *Source*: [MCP Connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md)

### Tool Use

- **Updated tool use system prompt token counts**: The token count reference table in the tool use overview has been revised. Values differ substantially from previous counts across all models. New values per model (auto/none vs. any/tool):
  - `<NextOpus />` (Opus 4.8 placeholder): 290 / 410 tokens
  - Claude Opus 4.7: 675 / 804 tokens (was 346 / 313)
  - Claude Opus 4.6: 497 / 589 tokens (was 346 / 313)
  - Claude Opus 4.5: 496 / 588 tokens (was 346 / 313)
  - Claude Opus 4.1: 313 / 315 tokens (was 346 / 313)
  - Claude Sonnet 4.6: 497 / 589 tokens (was 346 / 313)
  - Claude Sonnet 4.5: 496 / 588 tokens (was 346 / 313)
  - Claude Haiku 4.5: 496 / 588 tokens (was 346 / 313)
  - Claude Haiku 3.5: 264 / 355 tokens (was 264 / 340)
  - *Implication*: Cost estimates for tool-using requests should be recalculated using the new per-model values; previous numbers were inaccurate for most models.
  - *Source*: [Tool Use Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md)

- **Server tools batch documentation expanded**: The batch processing note in the server tools page has been replaced with a more detailed explanation covering agentic loop iteration limits, `pause_turn` continuation behavior, and common use cases.
  > `All server tools support batch processing. In a batch, the agentic loop runs just as it does for synchronous requests, with a higher per-turn iteration limit. If the loop reaches that limit, the response ends with stop_reason: "pause_turn"; you can continue it by submitting a follow-up request with the returned content.`
  > `Common batch workloads for server tools include enriching a dataset or catalog with information pulled from the web, checking a large set of documents against current sources, monitoring a list of pages or topics over time, and running analysis code over many files.`
  - *Implication*: Developers now have clearer guidance on how the agentic loop behaves in batch mode and when to expect `pause_turn` responses.
  - *Source*: [Server Tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools.md)

## Minor Changes

- **[handle-tool-calls.md]**: Example JSON response updated to reflect `claude-opus-4-8` as the model field (+1/-1 lines).

## Notable Details

- The advisor tool reference table updated the description for the `model` parameter: the example model ID changed from `"claude-opus-4-7"` to `"claude-opus-4-8"`, and the `advisor_result` variant description now cites "Claude Opus 4.8" as the example plaintext-returning model.
- In `build-a-tool-using-agent.md`, 15 internal `# Source for <CodeSource> in build-a-tool-using-agent.mdx.` comments were removed from code examples. These were artifact metadata not intended for end-user documentation.
- The `overview.md` token count table uses a `<NextOpus />` placeholder component (not a literal model name) in the new first row, suggesting the table is prepared ahead of full model naming finalization.
- Model references in `build-a-tool-using-agent.md` examples jumped from `claude-opus-4-6` directly to `claude-opus-4-8` (skipping 4.7), indicating the Ring examples were on an older base.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| agent-skills/quickstart.md | Modified | SIGNIFICANT | +39/-39 | Model references updated from `claude-opus-4-7` to `claude-opus-4-8` across all SDK examples |
| mcp-connector.md | Modified | SIGNIFICANT | +19/-15 | New "Batch requests" section; model examples updated to `claude-opus-4-8` |
| mcp-tunnels/overview.md | Modified | SIGNIFICANT | +3/-3 | Model references updated to `claude-opus-4-8` |
| tool-use/advisor-tool.md | Modified | SIGNIFICANT | +21/-20 | Opus 4.8 added to executor/advisor compatibility table; example model updated |
| tool-use/bash-tool.md | Modified | SIGNIFICANT | +9/-9 | Model references updated to `claude-opus-4-8` |
| tool-use/build-a-tool-using-agent.md | Modified | SIGNIFICANT | +27/-47 | Source comments removed; model examples updated from `claude-opus-4-6` to `claude-opus-4-8` |
| tool-use/code-execution-tool.md | Modified | SIGNIFICANT | +54/-53 | Opus 4.8 added to model compatibility table; example model updated |
| tool-use/computer-use-tool.md | Modified | SIGNIFICANT | +13/-13 | Opus 4.8 added to zoom/high-res feature list; example model updated |
| tool-use/define-tools.md | Modified | SIGNIFICANT | +9/-9 | Model references updated to `claude-opus-4-8` |
| tool-use/fine-grained-tool-streaming.md | Modified | SIGNIFICANT | +16/-16 | Model references updated to `claude-opus-4-8` |
| tool-use/handle-tool-calls.md | Modified | MINOR | +1/-1 | Example response model field updated |
| tool-use/memory-tool.md | Modified | SIGNIFICANT | +9/-9 | Model references updated to `claude-opus-4-8` |
| tool-use/overview.md | Modified | SIGNIFICANT | +15/-14 | Tool use system prompt token counts revised for all models; Opus 4.8 row added |
| tool-use/parallel-tool-use.md | Modified | SIGNIFICANT | +14/-14 | Model references updated to `claude-opus-4-8` |
| tool-use/programmatic-tool-calling.md | Modified | SIGNIFICANT | +23/-22 | Opus 4.8 added to supported model table; example model updated |
| tool-use/server-tools.md | Modified | SIGNIFICANT | +17/-15 | Batch documentation expanded with agentic loop details; model updated |
| tool-use/strict-tool-use.md | Modified | SIGNIFICANT | +25/-25 | Model references updated to `claude-opus-4-8` |
| tool-use/text-editor-tool.md | Modified | SIGNIFICANT | +22/-22 | Model references updated to `claude-opus-4-8` |
| tool-use/tool-runner.md | Modified | SIGNIFICANT | +38/-38 | Model references updated to `claude-opus-4-8` across all SDK examples |
| tool-use/tool-search-tool.md | Modified | SIGNIFICANT | +9/-9 | Model references updated to `claude-opus-4-8` |
| tool-use/web-fetch-tool.md | Modified | SIGNIFICANT | +20/-20 | Opus 4.8 added to dynamic filtering support list; example model updated |
| tool-use/web-search-tool.md | Modified | SIGNIFICANT | +21/-19 | Opus 4.8 added to dynamic filtering support list; example model updated |

---
*Generated from Claude API documentation changes detected on 2026-05-29*
