# Claude API Documentation Changes — 2026-03-05

## Summary

This update significantly expands multi-language SDK coverage across all agents-and-tools documentation, adding C#, Go, Java, PHP, and Ruby examples to pages that previously showed only Python and TypeScript. Two new tool versions are introduced: `web_search_20260209` and `web_fetch_20260209`, both supporting dynamic content filtering on Claude Opus 4.6 and Sonnet 4.6. The MCP connector example set now covers six languages.

---

## Significant Changes

### Web Search Tool

- **New `web_search_20260209` tool version with dynamic filtering**: A new versioned web search tool is now available for Claude Opus 4.6 and Sonnet 4.6 that enables Claude to write and execute code to post-process query results before they enter the context window.
  > "With the `web_search_20260209` tool version, Claude can write and execute code to post-process query results. Instead of reasoning over full HTML files, Claude dynamically filters search results before loading them into context, keeping only what's relevant and discarding the rest."
  - *Implication*: Dynamic filtering requires the code execution tool to be enabled alongside web search. The previous version `web_search_20250305` remains available without this behavior. The improved version is available on the Claude API and Microsoft Azure; Google Vertex AI only supports the basic version.
  - *Source*: [Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool.md)

### Web Fetch Tool

- **New `web_fetch_20260209` tool version with dynamic filtering**: A new versioned web fetch tool now allows Claude to write and execute code to filter fetched page content before loading it into context, reducing token usage for large documents.
  > "With the `web_fetch_20260209` tool version, Claude can write and execute code to filter the fetched content before loading it into context."
  - *Implication*: Like `web_search_20260209`, this requires the code execution tool. Available on Opus 4.6 and Sonnet 4.6 only. The prior version `web_fetch_20250910` remains available.
  - *Source*: [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md)

### MCP Connector

- **Expanded SDK coverage: Python, C#, Go, Java, PHP, Ruby examples added**: The basic MCP connector code group previously contained only TypeScript and Python examples. It now includes C#, Go, Java, PHP, and Ruby — providing complete multi-language parity.
  > Previously: two-language code group (Python, TypeScript). Now: six-language code group (Python, TypeScript, C#, Go, Java, PHP, Ruby) all demonstrating `mcp-client-2025-11-20` beta usage.
  - *Implication*: Developers using the Go, Java, PHP, Ruby, or C# SDKs now have direct reference implementations for MCP connector integration.
  - *Source*: [MCP Connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md)

### Code Execution Tool

- **C#, Go, Java, PHP, Ruby SDK examples added throughout**: Every major code execution scenario — basic usage, file creation, file upload with the Files API, and persistent container reuse — now includes examples for all six SDK languages.
  - *Implication*: Previously, TypeScript and Python were the only languages with code execution examples. The new additions reduce integration friction for .NET, JVM, PHP, and Ruby ecosystems.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

- **TypeScript Files API call corrected**: The TypeScript file upload example was updated from `anthropic.beta.files.create({ file: createReadStream(...) })` to `client.beta.files.upload({ file: await toFile(createReadStream(...), undefined, { type: "text/csv" }), betas: ["files-api-2025-04-14"] })`.
  > ```diff
  > -  const fileObject = await anthropic.beta.files.create({
  > -    file: createReadStream("data.csv")
  > +  const fileObject = await client.beta.files.upload({
  > +    file: await toFile(createReadStream("data.csv"), undefined, { type: "text/csv" }),
  > +    betas: ["files-api-2025-04-14"]
  >    });
  > ```
  - *Implication*: The `toFile` helper and explicit beta header are required for correct SDK usage with the Files API. The old pattern would fail with current SDK versions.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

- **TypeScript beta header added to container-reuse examples**: The persistent container examples were updated to use `client.beta.messages.create` with `betas: ["code-execution-2025-08-25"]`, replacing bare `anthropic.messages.create` calls.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

### Tool Use Overview and Implement Tool Use

- **C#, Go, Java, PHP, Ruby examples added to core tool use pages**: The tool use overview and implementation guide now include all six SDK languages for the fundamental patterns: defining tools, handling `tool_use` response blocks, building `tool_result` messages, and multi-turn tool loops.
  - *Implication*: These are the most-referenced pages in the tools documentation. Full multi-language coverage significantly lowers the barrier to entry for developers outside the Python/TypeScript ecosystem.
  - *Source*: [Tool Use Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md), [Implement Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use.md)

### Tool Search Tool

- **Substantial content expansion with new handling examples**: The tool search documentation was expanded with new sections showing how to build the full request/response loop: adding the assistant response and tool results back into messages, and extracting `tool_reference` blocks to provide `tool_results`.
  > New sections: "Add assistant response and handle any tool use", "Extract tool_use blocks and provide tool_results"
  - *Implication*: The new sections demonstrate the complete multi-turn interaction pattern required when using deferred tool loading, addressing a gap in the previous documentation.
  - *Source*: [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md)

### Programmatic Tool Calling

- **Substantial content expansion**: The programmatic tool calling page grew by ~778 lines, adding deeper usage guidance and multi-language examples.
  - *Source*: [Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md)

### Computer Use Tool

- **Significant content updates**: The computer use tool page received +588/-118 lines of changes. Content updates reflect current beta versioning and model compatibility.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

### Memory Tool

- **Significant content expansion**: The memory tool page grew by ~371 lines with added usage examples illustrating how Claude interacts with the `/memories` directory across a conversation turn.
  - *Source*: [Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md)

---

## Notable Details

- **TypeScript import style normalized**: Multiple pages changed `import { Anthropic } from "@anthropic-ai/sdk"` to `import Anthropic from "@anthropic-ai/sdk"` (default import). This reflects the preferred SDK import pattern and affects code-execution, overview, and several other pages.

- **Code block annotations added for documentation tooling**: Code examples across agent-skills and bash-tool pages had `nocheck` and `hidelines={...}` directives added to fenced code blocks (e.g., `` ```python nocheck ``, `` ```typescript TypeScript hidelines={1..4} ``). These are documentation rendering hints, not API changes.

- **MCP example URL updated**: The Python MCP connector example URL was changed from `https://mcp.example.com/sse` to `https://example-server.modelcontextprotocol.io/sse`, aligning with the official MCP project domain.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `tool-use/implement-tool-use.md` | Modified | +2032/-204 | C#/Go/Java/PHP/Ruby examples added; new multi-turn tool loop sections |
| `tool-use/code-execution-tool.md` | Modified | +1686/-130 | C#/Go/Java/PHP/Ruby examples added; TypeScript Files API call corrected |
| `tool-use/overview.md` | Modified | +1225/-17 | C#/Go/Java/PHP/Ruby examples added to core tool use intro |
| `tool-use/tool-search-tool.md` | Modified | +960/-9 | Expanded with full agentic loop examples |
| `tool-use/programmatic-tool-calling.md` | Modified | +778/-20 | Significant content expansion and multi-language examples |
| `tool-use/computer-use-tool.md` | Modified | +588/-118 | Content updates and reorganization |
| `tool-use/web-search-tool.md` | Modified | +521/-11 | New `web_search_20260209` tool version with dynamic filtering |
| `tool-use/memory-tool.md` | Modified | +371/-6 | Usage examples and interaction patterns expanded |
| `mcp-connector.md` | Modified | +203/-20 | Added C#, Go, Java, PHP, Ruby SDK examples |
| `tool-use/web-fetch-tool.md` | Modified | +146/-10 | New `web_fetch_20260209` tool version with dynamic filtering |
| `tool-use/text-editor-tool.md` | Modified | +44/-42 | Content reorganization |
| `agent-skills/quickstart.md` | Modified | +9/-5 | Code block annotation changes |
| `agent-skills/best-practices.md` | Modified | +8/-4 | Code block annotation changes |
| `tool-use/bash-tool.md` | Modified | +9/-5 | Code block annotation changes |
| `tool-use/fine-grained-tool-streaming.md` | Modified | +9/-5 | Code block annotation changes |

---

*Generated from Claude API documentation changes detected on 2026-03-05*
