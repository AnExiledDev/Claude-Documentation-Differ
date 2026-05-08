# Claude API Documentation Changes — 2026-02-19

## Summary

Several server-side tools have graduated from beta, removing the need for beta headers and `client.beta.messages` calls: code execution, memory, programmatic tool calling, tool search, tool use examples (`input_examples`), and web fetch. Concurrently, new tool versions for web search (`web_search_20260209`) and web fetch (`web_fetch_20260209`) introduce **dynamic filtering** — Claude writes and executes code to process fetched content before it reaches the context window. Claude Sonnet 4.6 is added as a supported model across code execution, web search, web fetch, computer use, memory, and programmatic tool calling.

---

## Significant Changes

### Tools Graduating from Beta

Multiple tools that previously required beta headers and `client.beta.messages.create` have been promoted to the stable API. The `client.messages.create` method and standard (non-beta) path should now be used for all of these:

| Feature | Old beta header (removed) | New call path |
|---|---|---|
| Code execution | `code-execution-2025-08-25` | `client.messages.create` |
| Memory tool | `context-management-2025-06-27` | `client.messages.create` |
| Programmatic tool calling | `advanced-tool-use-2025-11-20` | `client.messages.create` |
| Tool search tool | `advanced-tool-use-2025-11-20` | `client.messages.create` |
| Tool use examples (`input_examples`) | `advanced-tool-use-2025-11-20` | `client.messages.create` |
| Web fetch tool | `web-fetch-2025-09-10` | `client.messages.create` |

- *Implication*: Any code using `client.beta.messages.create` with these beta headers should be updated to `client.messages.create` without the `betas` list. The beta headers are no longer required and can be removed from requests.
- *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md), [Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md), [Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md), [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md), [Implement Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use.md), [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md)

---

### Web Search — Dynamic Filtering with `web_search_20260209`

- **New tool version `web_search_20260209`**: A new version of the web search tool is available for Claude Opus 4.6 and Sonnet 4.6. Claude can write and execute code to post-process query results before they reach the context window, keeping only relevant content and discarding the rest. The previous version (`web_search_20250305`) remains available.

  > "With the `web_search_20260209` tool version, Claude can write and execute code to post-process query results. Instead of reasoning over full HTML files, Claude dynamically filters search results before loading them into context, keeping only what's relevant and discarding the rest."

  > "Dynamic filtering is particularly effective for: Searching through technical documentation, Literature review and citation verification, Technical research, Response grounding and verification"

  - *Implication*: Dynamic filtering requires the code execution tool to be enabled alongside web search. Available on the Claude API and Microsoft Azure; on Google Vertex AI, only the basic web search tool (without dynamic filtering) is available.
  - *Source*: [Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool.md)

```python
# Enable dynamic filtering — use the new tool version
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Search for current AAPL and GOOGL prices..."}],
    tools=[{"type": "web_search_20260209", "name": "web_search"}],
)
```

---

### Web Fetch — Dynamic Filtering with `web_fetch_20260209`

- **New tool version `web_fetch_20260209`**: A parallel update to the web fetch tool enables Claude Opus 4.6 and Sonnet 4.6 to filter fetched web page and PDF content before it reaches the context window. The previous version (`web_fetch_20250910`) remains available.

  > "The latest web fetch tool version (`web_fetch_20260209`) supports **dynamic filtering** with Claude Opus 4.6 and Sonnet 4.6. Claude can write and execute code to filter fetched content before it reaches the context window, keeping only relevant information and discarding the rest. This reduces token consumption while maintaining response quality."

  - *Implication*: As with web search, dynamic filtering requires the code execution tool. Available on the Claude API and Microsoft Azure.
  - *Source*: [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md)

---

### Code Execution — Free with Web Search/Fetch, New Pricing Transparency

- **Code execution is free when combined with web search or web fetch**: When `web_search_20260209` or `web_fetch_20260209` is included in a request, code execution incurs no additional charges beyond standard input/output token costs.

  > "**Code execution is free when used with web search or web fetch.** When `web_search_20260209` or `web_fetch_20260209` is included in your request, there are no additional charges for code execution tool calls beyond the standard input and output token costs. Standard code execution charges apply when these tools are not included."

- **Usage tracking in response**: Code execution usage is now surfaced in the API response under `usage.server_tool_use.code_execution_requests`:

  ```json
  "usage": {
    "input_tokens": 105,
    "output_tokens": 239,
    "server_tool_use": {
      "code_execution_requests": 1
    }
  }
  ```

- **Platform availability**: A new section documents where code execution is available:
  > "Code execution is available on: Claude API (Anthropic), Microsoft Azure AI Foundry. Code execution is not currently available on Amazon Bedrock or Google Vertex AI."

- **Files API combo simplified**: When using the Files API with code execution, only the `files-api-2025-04-14` beta header is needed. The `code-execution-2025-08-25` header is no longer required in the combination.

- **Upgrade instructions simplified**: The upgrade from the old tool version no longer includes a step to update the beta header — only the tool type (`code_execution_20250522` → `code_execution_20250825`) needs to change.

- *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

---

### Claude Sonnet 4.6 — Expanded Tool Support

Claude Sonnet 4.6 (`claude-sonnet-4-6`) has been added as a supported model across multiple tools and features:

- **Code execution tool** (`code_execution_20250825`)
- **Web search tool** (both `web_search_20250305` and `web_search_20260209`)
- **Web fetch tool** (both `web_fetch_20250910` and `web_fetch_20260209`)
- **Computer use tool** — uses the newer `computer_20251124` tool version with `computer-use-2025-11-24` beta header (same as Opus 4.6 and Opus 4.5)
- **Memory tool** (`memory_20250818`)
- **Programmatic tool calling** (`code_execution_20250825`)
- **Tool system prompt tokens**: Added to the token count table (346 tokens for `auto`/`none`, 313 tokens for `any`/`tool`)
- **Parallel tool use**: Added to the list of models that excel at parallel tool use with minimal prompting

  > "Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5, Opus 4.5, Opus 4.1, and Sonnet 4: Excel at parallel tool use with minimal prompting"

- *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md), [Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool.md), [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md), [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md), [Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md), [Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md), [Tool Use Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md)

---

### Computer Use — Sonnet 4.6 Upgraded to Newer Tool Version

- **Sonnet 4.6 uses `computer_20251124`**: Previously, only Opus 4.6 and Opus 4.5 supported the `computer_20251124` tool version (with `computer-use-2025-11-24` beta header) which includes the zoom action for screen region inspection. Sonnet 4.6 now also uses this newer version.

  > "`computer-use-2025-11-24` for Claude Opus 4.6, Claude Sonnet 4.6, Claude Opus 4.5"

  > "Claude Opus 4.6, Claude Sonnet 4.6, and Claude Opus 4.5 introduce the `computer_20251124` tool version with new capabilities including the zoom action for detailed screen region inspection."

- **ZDR exclusion noted**: A new note clarifies that computer use is **not** covered by Zero Data Retention arrangements.
- **Beta flag logic updated**: The reference implementation's `sampling_loop` now uses `computer-use-2025-11-24` when the tool version string contains `20251124`.
- *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

---

### ZDR (Zero Data Retention) Eligibility Clarifications

Several features had their ZDR status explicitly documented:

| Feature | ZDR Status |
|---|---|
| Web search tool | ✅ ZDR eligible |
| Web fetch tool | ✅ ZDR eligible |
| Memory tool | ✅ ZDR eligible |
| Tool search (custom client-side) | ✅ ZDR eligible |
| Code execution tool | ❌ Not covered by ZDR |
| Programmatic tool calling | ❌ Not covered by ZDR |
| Tool search (server-side) | ❌ Not covered by ZDR |
| Computer use | ❌ Not covered by ZDR |
| MCP connector | ❌ Not covered by ZDR |

- *Implication*: Developers with ZDR arrangements should audit which tools they use. Server-side code execution, programmatic tool calling, and server-side tool search will retain data per their standard retention policies even under ZDR.
- *Source*: [Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool.md), [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md), [Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md), [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md), [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md), [Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md), [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md), [MCP Connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md)

---

### Memory Tool — Beta Graduation and ZDR Eligibility

- **No longer requires beta header**: The `context-management-2025-06-27` header has been removed from all memory tool examples. Setup is now a two-step process (add the tool, implement handlers) rather than three steps.
- **ZDR eligible**: The memory tool is now documented as ZDR eligible (the previous note only mentioned beta status).
- **Sonnet 4.6 added** to the supported models list.
- *Source*: [Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md)

---

### Tool Use Examples (`input_examples`) — Beta Label Removed

- **`input_examples` is no longer beta**: The field was previously documented as `(Optional, beta)` and required the `advanced-tool-use-2025-11-20` beta header. It is now `(Optional)` with no special header needed.

  > "`input_examples` | (Optional) An array of example input objects to help Claude understand how to use the tool."

- *Implication*: Developers using `input_examples` should remove the `advanced-tool-use-2025-11-20` beta header and switch from `client.beta.messages.create` to `client.messages.create`.
- *Source*: [Implement Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use.md)

---

### MCP Connector — Model and ZDR Updates

- **Model reference updated in examples**: Code snippets previously showed `claude-sonnet-4-5`; all examples now reference `claude-sonnet-4-6`.
- **ZDR exclusion noted**: A new note clarifies that the MCP connector is **not** covered by ZDR arrangements.
- *Source*: [MCP Connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md)

---

## Migration Guidance

### Remove Beta Headers for Graduated Tools

For any of the following features, update your code to remove beta headers and switch from `beta.messages` to `messages`:

```python
# Before (code execution)
response = client.beta.messages.create(
    model="claude-opus-4-6",
    betas=["code-execution-2025-08-25"],
    ...
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)

# After
response = client.messages.create(
    model="claude-opus-4-6",
    ...
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

```python
# Before (memory tool)
response = client.beta.messages.create(
    model="claude-opus-4-6",
    betas=["context-management-2025-06-27"],
    tools=[{"type": "memory_20250818", "name": "memory"}],
    ...
)

# After
response = client.messages.create(
    model="claude-opus-4-6",
    tools=[{"type": "memory_20250818", "name": "memory"}],
    ...
)
```

```python
# Before (programmatic tool calling / tool search / input_examples)
response = client.beta.messages.create(
    model="claude-opus-4-6",
    betas=["advanced-tool-use-2025-11-20"],
    ...
)

# After
response = client.messages.create(
    model="claude-opus-4-6",
    ...
)
```

```python
# Before (web fetch)
response = client.beta.messages.create(
    model="claude-opus-4-6",
    betas=["web-fetch-2025-09-10"],
    tools=[{"type": "web_fetch_20250910", "name": "web_fetch"}],
    ...
)

# After
response = client.messages.create(
    model="claude-opus-4-6",
    tools=[{"type": "web_fetch_20250910", "name": "web_fetch"}],  # or web_fetch_20260209 for dynamic filtering
    ...
)
```

### Upgrade Web Search/Fetch to Enable Dynamic Filtering

To use dynamic filtering (available on Opus 4.6 and Sonnet 4.6 only), change the tool type:

```python
# Dynamic filtering — web search
tools=[{"type": "web_search_20260209", "name": "web_search"}]
# Also include code execution tool to enable filtering
tools=[
    {"type": "web_search_20260209", "name": "web_search"},
    {"type": "code_execution_20250825", "name": "code_execution"},
]

# Dynamic filtering — web fetch
tools=[{"type": "web_fetch_20260209", "name": "web_fetch"}]
```

### Update Files API + Code Execution Requests

Previously required two beta headers; now only one is needed:

```bash
# Before
--header "anthropic-beta: code-execution-2025-08-25,files-api-2025-04-14"

# After
--header "anthropic-beta: files-api-2025-04-14"
```

### Update Computer Use for Sonnet 4.6

If using Sonnet 4.6 with computer use, switch to the newer tool version:

```python
# Sonnet 4.6 now uses computer_20251124, not computer_20250124
betas=["computer-use-2025-11-24"]
tools=[{
    "type": "computer_20251124",   # was computer_20250124
    "name": "computer",
    ...
}]
```

---

## Notable Details

- **Programmatic tool calling error message updated**: The `missing_beta_header` error description changed from "PTC beta header not provided" to "Required beta header not provided", reflecting that the PTC-specific beta header is no longer needed.
- **Tool search + MCP no longer needs `advanced-tool-use-2025-11-20`**: When combining tool search with the MCP connector, only the `mcp-client-2025-11-20` header is needed — `advanced-tool-use-2025-11-20` has been removed from the combination.
- **"Anthropic API" consistently renamed to "Claude API"**: Several references to "Anthropic API" in agent skills and platform documentation have been updated to "Claude API". Similarly, "Anthropic API key" is now "Claude API key" in the quickstart guide.
- **Agent Skills best practices**: The recommendation to use gerund form for skill names softened from "We recommend" to "Consider using", and "We do not currently provide a built-in way to run evaluations" became "There is not currently a built-in way."
- **Code execution in Batches API**: The documentation notes that code execution tool can be included in Messages Batches API requests.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| web-fetch-tool.md | Modified | +96 / -14 | New `web_fetch_20260209` tool version with dynamic filtering; beta graduation; Sonnet 4.6 support; ZDR eligible |
| web-search-tool.md | Modified | +89 / -1 | New `web_search_20260209` tool version with dynamic filtering; Sonnet 4.6 support; ZDR eligible |
| code-execution-tool.md | Modified | +64 / -61 | Beta graduation (no more `code-execution-2025-08-25` header); free with web search/fetch; Sonnet 4.6; platform availability section; usage tracking |
| computer-use-tool.md | Modified | +35 / -29 | Sonnet 4.6 now uses `computer_20251124`; ZDR exclusion noted; beta flag logic updated |
| implement-tool-use.md | Modified | +16 / -27 | `input_examples` beta label removed; `advanced-tool-use-2025-11-20` removed; Sonnet 4.6 in parallel tool use list |
| memory-tool.md | Modified | +15 / -18 | Beta graduation; ZDR eligible; Sonnet 4.6 support; setup simplified to 2 steps |
| web-search-tool.md | Modified | +89 / -1 | Dynamic filtering with `web_search_20260209`; ZDR note; Sonnet 4.6 |
| tool-search-tool.md | Modified | +11 / -20 | Beta graduation; ZDR status differentiated (server-side not ZDR, client-side ZDR eligible) |
| overview.md | Modified | +9 / -8 | Sonnet 4.6 added to tool system prompt token count table |
| mcp-connector.md | Modified | +7 / -3 | Model examples updated to Sonnet 4.6; ZDR exclusion noted |
| programmatic-tool-calling.md | Modified | +14 / -26 | Beta graduation; Sonnet 4.6 support; ZDR exclusion noted |
| agent-skills/best-practices.md | Modified | +5 / -5 | Minor wording changes; "Anthropic API" → "Claude API" |
| agent-skills/quickstart.md | Modified | +3 / -3 | Minor wording changes; "Anthropic API key" → "Claude API key" |

---

*Generated from Claude API documentation changes detected on 2026-02-19*
