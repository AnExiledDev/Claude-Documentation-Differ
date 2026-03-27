# Claude API Documentation Changes — 2026-03-27

## Summary

The agents-and-tools documentation section received a major structural overhaul: the monolithic tool-use overview page (~2,400 lines) was split into 13 new focused pages, and all existing tool pages were significantly trimmed. Alongside the restructuring, several API-visible changes are documented: a new `input_examples` field on tool definitions, `strict: true` for grammar-constrained sampling, a beta Tool Runner abstraction in the Python/TypeScript/Ruby SDKs, and ZDR clarifications for `_20260209` server tool versions.

---

## Significant Changes

### Tool Use API — New Parameters and Capabilities

- **`input_examples` field on tool definitions**: Tool definitions now accept an optional `input_examples` array containing schema-validated example input objects. Supported on user-defined and Anthropic-schema client tools; not available on server tools.
  > "Add an optional `input_examples` field to your tool definition with an array of example input objects. Each example must be valid according to the tool's `input_schema`."
  - *Implication*: Particularly useful for complex tools with nested objects, optional parameters, or format-sensitive inputs. Documented with code examples across Python, TypeScript, C#, Go, Java, PHP, and Ruby SDKs.
  - *Source*: [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools.md)

- **`strict: true` for grammar-constrained tool inputs**: Setting `strict: true` on a tool definition uses grammar-constrained sampling to guarantee tool inputs exactly match the declared JSON Schema. Documented as GA, available across all SDKs.
  > "Setting `strict: true` on a tool definition uses grammar-constrained sampling to guarantee Claude's tool inputs match your JSON Schema."
  - *Implication*: Eliminates the need to validate and retry tool calls for type mismatches (e.g., `"2"` instead of `2`). Requires `additionalProperties: false` on the schema. Previously scattered in other docs; now has a dedicated page.
  - *Source*: [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use.md)

- **`allowed_callers` field**: Controls which callers can invoke a tool — `"direct"` (the model itself) and/or `"code_execution_20260120"` (code running inside the code execution sandbox). Documented on the Tool Reference page.
  > "Omitting `\"direct\"` from the array (for example, `\"allowed_callers\": [\"code_execution_20260120\"]`) means the tool is callable only from within code execution."
  - *Implication*: Enables programmatic tool calling from within the code execution sandbox. The response's `tool_use` block includes a `caller` field when this is used.
  - *Source*: [Tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference.md)

- **`defer_loading` property**: Tools marked `defer_loading: true` are excluded from the initial system prompt and loaded on demand when tool search returns a `tool_reference` for them.
  > "Tools with `defer_loading: true` are stripped from the rendered tools section before the cache key is computed. They don't appear in the system-prompt prefix at all."
  - *Implication*: Allows large tool libraries to be added without invalidating an existing prompt cache entry. Preserves both prompt cache and grammar caching when tools load dynamically.
  - *Source*: [Tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference.md)

- **`eager_input_streaming` property**: Per-tool flag to enable fine-grained streaming of tool inputs without JSON validation buffering (user-defined tools only).
  > "Set `eager_input_streaming` to `true` on any user-defined tool where you want fine-grained streaming enabled."
  - *Implication*: Now documented with a dedicated section on accumulating `input_json_delta` events. Previously underdocumented; the page gained +121 lines of new content covering the full delta accumulation pattern.
  - *Source*: [Fine-grained tool streaming](https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming.md)

### Tool Runner SDK (Beta)

- **Tool Runner abstraction in Python, TypeScript, and Ruby SDKs**: A new SDK-level abstraction that handles the agentic loop, error wrapping, and type safety automatically. Available in beta at `client.beta.messages.tool_runner()` (Python/Ruby) and `client.beta.messages.toolRunner()` (TypeScript).
  > "Tool Runner handles the agentic loop, error wrapping, and type safety so you don't have to. Use the manual loop only when you need human-in-the-loop approval, custom logging, or conditional execution."

  **Python**: Use `@beta_tool` decorator (or `@beta_async_tool` for async); call `runner.until_done()` for the final message.

  **TypeScript**: Use `betaZodTool()` (requires Zod ≥3.25.0) for type-safe definitions, or `betaTool()` for JSON Schema-based definitions; `await runner` returns the final message.

  **Ruby**: Use `Anthropic::BaseTool` class with `input_schema` DSL; `runner.run_until_finished` returns all messages.

  > "The tool runner supports automatic compaction, which generates summaries when token usage exceeds a threshold. This allows long-running agentic tasks to continue beyond context window limits."
  - *Implication*: Significantly reduces boilerplate for standard tool use. Supports context compaction for long-running agents. When a tool throws an exception, the runner catches it and returns the error to Claude as `is_error: true` automatically.
  - *Source*: [Tool Runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner.md)

### Server Tools — `pause_turn` and ZDR Handling

- **`pause_turn` stop reason and continuation pattern**: A dedicated page now documents the server-side loop and how to handle `stop_reason: "pause_turn"` from server tools. Code examples in 8 languages show the re-send pattern.
  > "A paused turn means the work isn't finished; re-send the conversation (including the paused response) to let the model continue where it left off."
  - *Implication*: Previously only mentioned inline; now has authoritative documentation and SDK examples for Python, TypeScript, C#, Go, Java, PHP, and Ruby.
  - *Source*: [Server tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools.md)

- **ZDR eligibility and `allowed_callers` for `_20260209` server tools**: The `web_search_20260209` and `web_fetch_20260209` versions are **not** ZDR-eligible by default because they use internal code execution for dynamic filtering. Setting `"allowed_callers": ["direct"]` disables dynamic filtering and restores ZDR eligibility.
  > "To use a `_20260209` server tool with ZDR, disable dynamic filtering by setting `\"allowed_callers\": [\"direct\"]` on the tool."
  - *Implication*: Developers using ZDR must explicitly opt out of dynamic filtering to maintain their ZDR arrangement when upgrading to `_20260209` server tool versions.
  - *Source*: [Server tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools.md)

- **Domain filtering — wildcard and Unicode security notes**: The server tools page now documents that wildcards (`*`) are only valid after the domain part in the path (valid: `example.com/*`; invalid: `*.example.com`). A new warning covers Unicode homograph attack risks in domain allowlists.
  - *Source*: [Server tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools.md)

### Tool Reference and Versioning

- **Unified tool directory**: A new [Tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference.md) page lists all Anthropic-provided tools with their `type` string(s), execution location, and GA/Beta status. Versioning semantics are now formally documented: capability-keyed, model-keyed, variant, and legacy.

  Notable version strings listed:
  | Tool | Active versions |
  |---|---|
  | Web search | `web_search_20260209`, `web_search_20250305` |
  | Web fetch | `web_fetch_20260209`, `web_fetch_20250910` |
  | Code execution | `code_execution_20260120`, `code_execution_20250825` |
  | Text editor | `text_editor_20250728` (Claude 4), `text_editor_20250124` (earlier) |
  | Computer use | `computer_20251124`, `computer_20250124` |

### Prompt Caching with Tools

- **Dedicated prompt caching + tools page**: Documents the full cache invalidation hierarchy for tool-containing requests, including how `defer_loading` preserves the prefix cache and how `strict` mode interacts with grammar construction.
  > "`defer_loading` also acts independently of grammar construction for strict mode. The grammar builds from the full toolset regardless of which tools are deferred, so prompt caching and grammar caching are both preserved when tools load dynamically."
  - *Source*: [Tool use with prompt caching](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching.md)

### Computer Use Tool

- **"Agentic loop" replaces "multi-agent loop"** in terminology. The section previously titled "Understanding the multi-agent loop" is now "Understanding the agentic loop."
- **"Combining with extended thinking"** replaces the earlier section "Enable thinking capability in Claude 4 models and Claude Sonnet 3.7," with the new section framing extended thinking as a general capability rather than a model-specific feature.
- Model compatibility section removed; model support now deferred to the [Tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference.md) page.
- *Source*: [Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

### Text Editor Tool

- **`undo_edit` command removed** from documentation. The model-specific code path distinguishing Claude 4 vs. Sonnet 3.7 behavior for `undo_edit` is no longer documented.
- Model compatibility section removed; deferred to Tool Reference.
- *Source*: [Text editor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool.md)

### Agent Skills — Open-Source Claude API Skill

- **New open-source `claude-api` skill**: Anthropic published an open-source Agent Skill in the [skills repository](https://github.com/anthropics/skills) that provides Claude with current API reference, SDK documentation, and best practices for 8 languages (Python, TypeScript, Java, Go, Ruby, C#, PHP, cURL).
  > "The skill uses progressive disclosure to keep context efficient: Claude loads only the documentation relevant to your project's language and the specific task at hand."
  - *Implication*: The skill is bundled with Claude Code and activates automatically when code imports `anthropic`, `@anthropic-ai/sdk`, or `claude_agent_sdk`. Can be manually installed via `npx skills add` or as a Claude Code plugin.
  - *Source*: [Claude API skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill.md)

- **Open-source Skills section and Data retention** added to Agent Skills overview.
  - *Source*: [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md)

---

## New Pages

- **`how-tool-use-works.md`** — Conceptual overview of the tool-use contract, three execution buckets (user-defined client, Anthropic-schema client, server-executed), the agentic loop, and when to use tools. [View](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works.md)
- **`define-tools.md`** — Schema specification, `input_examples` field, best practices for descriptions and naming, `tool_choice` guidance. [View](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools.md)
- **`handle-tool-calls.md`** — Implementation guide for handling `tool_use` blocks and formatting `tool_result` responses. [View](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls.md)
- **`server-tools.md`** — Shared mechanics for server-executed tools: `server_tool_use` blocks, `pause_turn` continuation, ZDR considerations, domain filtering. [View](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools.md)
- **`strict-tool-use.md`** — Dedicated page for `strict: true` grammar-constrained sampling with full SDK examples. [View](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use.md)
- **`tool-reference.md`** — Directory of all Anthropic-provided tools, their type strings, versioning semantics, and optional tool definition properties (`cache_control`, `strict`, `defer_loading`, `allowed_callers`, `input_examples`, `eager_input_streaming`). [View](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference.md)
- **`tool-runner.md`** — SDK Tool Runner beta for Python (`@beta_tool`), TypeScript (`betaZodTool`/`betaTool`), and Ruby (`Anthropic::BaseTool`). [View](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner.md)
- **`tool-use-with-prompt-caching.md`** — Cache invalidation hierarchy for tool-containing requests, `defer_loading` cache preservation, and per-tool caching considerations. [View](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching.md)
- **`parallel-tool-use.md`** — Guidance for handling multiple concurrent tool calls. [View](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use.md)
- **`manage-tool-context.md`** — Context window management during long tool-use sessions. [View](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context.md)
- **`tool-combinations.md`** — Patterns for combining multiple tools in agentic workflows. [View](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-combinations.md)
- **`build-a-tool-using-agent.md`** — Step-by-step tutorial from a single tool call to production. [View](https://platform.claude.com/docs/en/agents-and-tools/tool-use/build-a-tool-using-agent.md)
- **`troubleshooting-tool-use.md`** — Common tool use failures and diagnostics. [View](https://platform.claude.com/docs/en/agents-and-tools/tool-use/troubleshooting-tool-use.md)
- **`claude-api-skill.md`** — Open-source Agent Skill providing Claude with current API/SDK documentation for 8 programming languages. [View](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill.md)

---

## Notable Details

- **Model compatibility sections removed across multiple tools**: The `bash-tool.md`, `text-editor-tool.md`, `web-search-tool.md`, `web-fetch-tool.md`, and `memory-tool.md` pages all removed their "Supported models" / "Model compatibility" sections. Model support is now centralized in the [Tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference.md) page.
- **Data retention sections added broadly**: `code-execution-tool.md`, `computer-use-tool.md`, `programmatic-tool-calling.md`, `tool-search-tool.md`, `mcp-connector.md`, and `agent-skills/overview.md` all received new "Data retention" sections linking to the ZDR policy page. This appears to be a documentation standardization pass.
- **Tool system prompt token counts updated in overview**: The tool-use overview now includes token counts for several new model variants: Claude Opus 4.6, 4.5, 4.1, 4; Claude Sonnet 4.6, 4.5, 4; Claude Haiku 4.5 — all at 346/313 tokens for `auto/none` and `any/tool` respectively.
- **`_20260209` server tool versions noted as using internal code execution**: The `web_search_20260209` and `web_fetch_20260209` versions "use code execution internally to apply dynamic filters against search results." Including a standalone `code_execution` tool alongside these versions is warned against as it "creates two execution environments, which can confuse the model."

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `tool-use/overview.md` | Modified | +49/-2357 | Stripped to slim intro; content moved to 13 new pages |
| `tool-use/code-execution-tool.md` | Modified | +470/-1424 | Major restructure; removed "Combine operations" section; added Data retention |
| `tool-use/computer-use-tool.md` | Modified | +120/-611 | Agentic loop terminology; extended thinking section; removed model compat |
| `tool-use/tool-search-tool.md` | Modified | +37/-852 | Heavily simplified; added Data retention and Next steps |
| `tool-use/memory-tool.md` | Modified | +20/-358 | Removed model support section; simplified context editing integration |
| `tool-use/programmatic-tool-calling.md` | Modified | +99/-334 | Simplified; added Data retention |
| `tool-use/text-editor-tool.md` | Modified | +78/-232 | Removed `undo_edit` and model compatibility sections |
| `tool-use/fine-grained-tool-streaming.md` | Modified | +121/-3 | New section on accumulating `input_json_delta` deltas; Next steps |
| `tool-use/web-search-tool.md` | Modified | +18/-509 | Removed model support and caching examples; added Next steps |
| `tool-use/bash-tool.md` | Modified | +67/-43 | Updated code examples; removed model compatibility section |
| `tool-use/web-fetch-tool.md` | Modified | +18/-99 | Removed model support and caching examples; added Next steps |
| `mcp-connector.md` | Modified | +40/-34 | Added Data retention section; content updates |
| `agent-skills/overview.md` | Modified | +16/-0 | Added Open-source Skills section and Data retention |
| `tool-use/how-tool-use-works.md` | New | +96 | Conceptual model: three tool execution buckets, agentic loop |
| `tool-use/define-tools.md` | New | ~600 | Tool schemas, `input_examples` field, best practices |
| `tool-use/server-tools.md` | New | ~480 | Server tool mechanics, `pause_turn`, ZDR, domain filtering |
| `tool-use/strict-tool-use.md` | New | ~950 | `strict: true` with full multi-SDK examples |
| `tool-use/tool-runner.md` | New | ~920 | SDK Tool Runner beta (Python, TypeScript, Ruby) |
| `tool-use/tool-reference.md` | New | ~75 | Tool directory, versioning, optional tool definition properties |
| `tool-use/tool-use-with-prompt-caching.md` | New | ~95 | Cache invalidation table, `defer_loading`, per-tool caching |
| `tool-use/handle-tool-calls.md` | New | — | Implementation guide for tool call handling |
| `tool-use/parallel-tool-use.md` | New | — | Parallel tool call patterns |
| `tool-use/manage-tool-context.md` | New | — | Context management for long tool sessions |
| `tool-use/tool-combinations.md` | New | — | Multi-tool workflow patterns |
| `tool-use/build-a-tool-using-agent.md` | New | — | Step-by-step tutorial |
| `tool-use/troubleshooting-tool-use.md` | New | — | Diagnostics and common failures |
| `agent-skills/claude-api-skill.md` | New | ~100 | Claude API open-source skill |

---

*Generated from Claude API documentation changes detected on 2026-03-27*
