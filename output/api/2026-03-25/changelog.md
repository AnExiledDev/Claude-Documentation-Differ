# Claude API Documentation Changes — 2026-03-25

## Summary

This update is focused entirely on the Claude Agent SDK. A new dedicated page documents the Tool Search feature for scaling agents to large tool catalogs. The custom tools guide was substantially rewritten, removing the previous requirement for streaming input mode and adding coverage of tool annotations, image/resource returns, and error handling patterns. Python and TypeScript SDK references gained `ToolAnnotations` documentation.

## Significant Changes

### Agent SDK — Tool Search (New Feature Page)

- **New `tool-search` reference page**: Documents how the Agent SDK dynamically discovers and loads tools on demand, enabling agents to work with catalogs of up to 10,000 tools without loading all definitions into context upfront.

  > "Tool search enables your agent to work with hundreds or thousands of tools by dynamically discovering and loading them on demand. Instead of loading all tool definitions into the context window upfront, the agent searches your tool catalog and loads only the tools it needs."

  Key details:
  - **Enabled by default** — tool definitions are withheld from context; the agent receives a summary and searches as needed.
  - **Model requirement** — requires Claude Sonnet 4 or later, or Claude Opus 4 or later. Haiku models are explicitly excluded.
  - **Search results** — returns 3–5 most relevant tools per search query; adds one round-trip the first time a tool is discovered.
  - **Maximum catalog size** — 10,000 tools.
  - *Implication*: Developers with large tool sets no longer need to manage context window pressure from tool definitions manually; tool search is active out of the box.
  - *Source*: [Tool search](https://platform.claude.com/docs/en/agent-sdk/tool-search.md)

- **`ENABLE_TOOL_SEARCH` environment variable**: Controls tool search behavior via the `env` option on `query()`.

  | Value | Behavior |
  |:------|:---------|
  | (unset) or `true` | Tool search always on (default) |
  | `auto` | Activates when tool definitions exceed 10% of context window |
  | `auto:N` | Activates at a custom percentage threshold (e.g., `auto:5` = 5%) |
  | `false` | Off — all tool definitions loaded into context every turn |

  > "With fewer than ~10 tools, loading everything upfront is typically faster."

  - *Implication*: The `auto` and `auto:N` modes let developers tune the crossover point between full upfront loading and on-demand search.
  - *Source*: [Tool search — Configure tool search](https://platform.claude.com/docs/en/agent-sdk/tool-search.md)

### Agent SDK — Custom Tools (Major Rewrite)

- **Streaming input no longer required for custom MCP tools**: The previous documentation stated custom MCP tools required streaming input mode (async generator for `prompt`). The rewritten guide uses a plain string `prompt` with `query()`, removing that constraint.

  Old approach (removed):
  ```python
  # Previously required streaming input mode
  async with ClaudeSDKClient(options=options) as client:
      await client.query("What's the weather?")
  ```
  New approach:
  ```python
  async for message in query(
      prompt="What's the temperature in San Francisco?",
      options=options,
  ):
      ...
  ```
  - *Implication*: Custom tool integrations no longer require `ClaudeSDKClient` or async generators; `query()` with a string prompt works.
  - *Source*: [Give Claude custom tools](https://platform.claude.com/docs/en/agent-sdk/custom-tools.md)

- **Tool annotations documented**: New `### Add tool annotations` section covering the `ToolAnnotations` type for both Python and TypeScript.

  | Field | Default | Meaning |
  |:------|:--------|:--------|
  | `readOnlyHint` | `false` | Tool does not modify environment; enables parallel calls with other read-only tools |
  | `destructiveHint` | `true` | Tool may perform destructive updates (informational) |
  | `idempotentHint` | `false` | Repeated calls with same args have no additional effect (informational) |
  | `openWorldHint` | `true` | Tool reaches external systems (informational) |

  > "Annotations are metadata, not enforcement. A tool marked `readOnlyHint: true` can still write to disk if that's what the handler does. Keep the annotation accurate to the handler."

  - *Implication*: Setting `readOnlyHint: true` is the mechanism for enabling Claude to batch read-only tool calls in parallel.
  - *Source*: [Give Claude custom tools — Add tool annotations](https://platform.claude.com/docs/en/agent-sdk/custom-tools.md)

- **Error handling patterns clarified**: New `## Handle errors` section explicitly documents how uncaught exceptions terminate the agent loop, while returning `isError: true` in the content lets Claude respond to the failure and continue.

  > "Handler throws an uncaught exception → Agent loop stops. Claude never sees the error, and the `query` call fails."
  > "Handler catches the error and returns `isError: true` → Agent loop continues. Claude sees the error as data and can retry, try a different tool, or explain the failure."

  - *Implication*: Developers should wrap handler logic in `try/except` / `try/catch` and return `isError: true` to keep the agent loop alive on failures.
  - *Source*: [Give Claude custom tools — Handle errors](https://platform.claude.com/docs/en/agent-sdk/custom-tools.md)

- **Returning images and resources**: New `## Return images and resources` section documents how tool handlers can return `image` and `resource` blocks alongside `text` in the `content` array.

  > "An image block carries the image bytes inline, encoded as base64. There is no URL field. To return an image that lives at a URL, fetch it in the handler, read the response bytes, and base64-encode them before returning."

  Image block fields: `type: "image"`, `data` (raw base64, no `data:image/...;base64,` prefix), `mimeType` (required, e.g., `image/png`).
  - *Implication*: Tools can now feed visual data directly to Claude for processing without separate API calls.
  - *Source*: [Give Claude custom tools — Return images and resources](https://platform.claude.com/docs/en/agent-sdk/custom-tools.md)

- **`tools` vs `allowedTools` distinction clarified**: New table explaining the two separate layers of tool control.

  | Option | Layer | Effect |
  |:-------|:------|:-------|
  | `tools: ["Read", "Grep"]` | Availability | Only listed built-ins in Claude's context; MCP tools unaffected |
  | `tools: []` | Availability | All built-ins removed; Claude can only use MCP tools |
  | `allowedTools` | Permission | Listed tools run without prompt; unlisted tools go through permission flow |
  | `disallowedTools` | Permission | Calls denied, but tool stays visible in context |

  > "To limit which built-ins Claude can use, prefer `tools` over disallowed tools. Omitting a tool from `tools` removes it from context so Claude never attempts it."

  - *Source*: [Give Claude custom tools — Configure allowed tools](https://platform.claude.com/docs/en/agent-sdk/custom-tools.md)

### Agent SDK — Python SDK Reference

- **`ToolAnnotations` type documented**: New `#### ToolAnnotations` section in the `tool()` decorator reference. Re-exported from `mcp.types` (also importable as `from claude_agent_sdk import ToolAnnotations`). Documents all five fields with types, defaults, and descriptions.
  - *Source*: [Agent SDK reference - Python](https://platform.claude.com/docs/en/agent-sdk/python.md)

- **Interrupt handling example updated**: The `ClaudeSDKClient` interrupt example now explicitly shows draining the interrupted task's messages before issuing a new query, and notes that interrupted tasks produce `ResultMessage` with `subtype == "error_during_execution"`.
  - *Source*: [Agent SDK reference - Python](https://platform.claude.com/docs/en/agent-sdk/python.md)

### Agent SDK — TypeScript SDK Reference

- **`ToolAnnotations` type documented**: New `#### ToolAnnotations` section in the `tool()` function reference. Re-exported from `@modelcontextprotocol/sdk/types.js`. Documents all five fields with types, defaults, and descriptions.
  - *Source*: [Agent SDK reference - TypeScript](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

- **`SDKLocalCommandOutputMessage` type documented**: New `### SDKLocalCommandOutputMessage` section added to the TypeScript SDK reference.
  - *Source*: [Agent SDK reference - TypeScript](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

### Agent SDK — MCP Page Simplified

- **Tool search content moved to dedicated page**: Three sections were removed from `mcp.md` — "Alternative: Change the permission mode", "How it works" (tool search internals), and "Configure tool search". The page now contains a brief `## MCP tool search` section that links to the new `tool-search.md` page.
  - *Implication*: Tool search configuration is now consolidated in its own page; developers should consult `tool-search.md` for `ENABLE_TOOL_SEARCH` options.
  - *Source*: [Connect to external tools with MCP](https://platform.claude.com/docs/en/agent-sdk/mcp.md)

### Context Editing — Multi-SDK Code Examples Added

- **Expanded SDK coverage in context editing examples**: The `context-editing.md` page was substantially restructured (+183 / −384 lines). Code examples for the `context_management` API now include C#, Go, Java, PHP, and Ruby in addition to the previously covered Shell, Python, and TypeScript.
  - *Implication*: Developers using the C#, Go, Java, PHP, and Ruby Anthropic SDKs can now reference native-language examples for `clear_tool_uses_20250919` and `clear_thinking_20251015` strategies directly in the documentation.
  - *Source*: [Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing.md)

## New Pages

- **[tool-search.md]** — Dedicated reference for the Agent SDK's tool search feature: how it works, the `ENABLE_TOOL_SEARCH` environment variable and its modes, optimization tips for tool naming and descriptions, limits (10,000 tool max, 3–5 results per search), and model support requirements. [View](https://platform.claude.com/docs/en/agent-sdk/tool-search.md)

## Notable Details

- The Python custom tools examples switched from `aiohttp` to `httpx` as the HTTP client library throughout `custom-tools.md`. This is an example-level change, not an API requirement.
- The `auto` threshold in `ENABLE_TOOL_SEARCH` is 10% of the model's context window by default. The `auto:N` variant accepts integer percentages (e.g., `auto:5`). Lower values activate tool search sooner.
- Tool search is documented as applying to both remote MCP servers and in-process SDK MCP servers built with `createSdkMcpServer` / `create_sdk_mcp_server`.
- The context editing page now explicitly notes that beta features (including context editing) are **not** eligible for Zero Data Retention (ZDR).

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| agent-sdk/tool-search.md | New | +129 | New page: tool search for scaling to large tool catalogs |
| agent-sdk/custom-tools.md | Modified | +586 / -613 | Major rewrite: removes streaming requirement, adds annotations, images, error handling |
| build-with-claude/context-editing.md | Modified | +183 / -384 | Multi-SDK examples added (C#, Go, Java, PHP, Ruby); page condensed |
| agent-sdk/python.md | Modified | +66 / -5 | ToolAnnotations type documented; interrupt handling updated |
| agent-sdk/typescript.md | Modified | +46 / -3 | ToolAnnotations and SDKLocalCommandOutputMessage types documented |
| agent-sdk/mcp.md | Modified | +8 / -67 | Tool search sections removed; now links to tool-search.md |
| agent-sdk/user-input.md | Modified | +8 / -6 | Minor wording refinements |

---
*Generated from Claude API documentation changes detected on 2026-03-25*
