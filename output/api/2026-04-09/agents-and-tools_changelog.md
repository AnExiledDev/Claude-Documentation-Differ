# Claude API Documentation Changes — 2026-04-09

## Summary

This update adds pervasive `ant` CLI examples across all agents-and-tools documentation pages, introduces Claude Mythos Preview (linked to `anthropic.com/glasswing`) as a supported model for web search, web fetch, tool search, and code execution, and removes all cross-references to the Agent SDK from the Agent Skills section. A new `output_file_too_large` error code was documented for the bash tool in code execution.

---

## Significant Changes

### Claude Mythos Preview — New Model Added to Multiple Tools

- **Web Search dynamic filtering now includes Mythos Preview**: The "Dynamic filtering" section (previously titled "Dynamic filtering with Opus 4.6 and Sonnet 4.6") was renamed to simply "Dynamic filtering" to reflect expanded model support.
  > `The latest web search tool version (web_search_20260209) supports dynamic filtering with Claude Mythos Preview, Claude Opus 4.6, and Claude Sonnet 4.6.`
  - *Platform note*: Mythos Preview web search is available on the Claude API, Microsoft Foundry, and Google Vertex AI — but **not** Amazon Bedrock.
  - *Source*: [Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool.md)

- **Web Fetch dynamic filtering now includes Mythos Preview**: Same section rename and model expansion.
  > `For Claude Mythos Preview, web fetch is supported on the Claude API and Microsoft Foundry only. It is not available for Mythos Preview on Amazon Bedrock or Google Vertex AI.`
  - *Platform note*: More restrictive availability than web search — no Vertex AI support for Mythos Preview web fetch.
  - *Source*: [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md)

- **Code Execution now documents Mythos Preview availability**:
  > `For Claude Mythos Preview, code execution is supported on the Claude API and Microsoft Foundry only. It is not available for Mythos Preview on Amazon Bedrock or Google Vertex AI.`
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

- **Tool Search model support expanded to include Mythos Preview**:
  > `Model support: Claude Mythos Preview, Sonnet 4.0+, Opus 4.0+ only (no Haiku)`
  - *Source*: [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md)

### `ant` CLI Tool — Added to All Tool Documentation

A new `ant` CLI tool has been added as a code example tab alongside Shell (curl), Python, and TypeScript across all tool documentation pages. This appears to be a first-party CLI for interacting with the Anthropic API. Coverage includes:

- **Bash Tool**: `ant messages create --tool '{type: bash_20250124, name: bash}' --message '...'`
- **Code Execution Tool**: `ant messages create --tool '{type: code_execution_20250825, name: code_execution}'` plus file upload/download workflows using `ant beta:files upload` and `ant beta:files download`
- **Computer Use Tool**: `ant beta:messages create --beta computer-use-2025-11-24` with YAML heredoc syntax
- **Fine-grained Tool Streaming**: `ant messages create --stream --transform usage` with `eager_input_streaming: true` in tool spec
- **Memory Tool**: `ant messages create` with YAML heredoc
- **MCP Connector**: `ant beta:messages create --beta mcp-client-2025-11-20` with YAML heredoc
- **Programmatic Tool Calling**: Multi-turn conversation examples using `ant messages create` with inline YAML
- **Text Editor Tool**: Initial request and full multi-turn conversation example in YAML format
- **Tool Search Tool**: `ant messages create` with `defer_loading: true` on tools
- **Web Fetch Tool**: `ant messages create` with YAML, plus `ant messages create --tool '{type: web_fetch_20250910, name: web_fetch, max_uses: 5}'`
- **Web Search Tool**: `ant messages create` with YAML and inline `--tool` flag syntax
- **Agent Skills Quickstart**: `ant beta:skills list --source anthropic`, `ant beta:messages create --beta code-execution-2025-08-25 --beta skills-2025-10-02`, and `ant beta:files download --file-id "$FILE_ID" --output ...`

The CLI uses both inline flags (`--tool '{type: ..., name: ...}'`, `--message '{role: ..., content: ...}'`) and YAML heredoc syntax (`<<'YAML' ... YAML`) for complex requests. A `--transform` flag supports JQ-style field extraction from responses.

- *Implication*: Developers can now test all tools from the CLI without writing Python or constructing curl commands.
- *Sources*: All pages under [agents-and-tools/tool-use/](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md)

### Code Execution Tool — Model Compatibility Simplified

- **Per-model table removed**: The explicit table listing each model and its tool version was replaced with a single statement.
  > `The code execution tool is available on all supported Claude models using tool version code_execution_20250825.`
  - *Implication*: Developers no longer need to cross-reference a table; all current models are supported under the same tool version.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

### Code Execution Tool — New Error Code

- **`output_file_too_large` added for bash commands**: A new error code was added to the error reference table.
  > `| bash | output_file_too_large | Command output exceeded the maximum size |`
  - *Implication*: Applications handling code execution results should catch this error type when bash commands produce large stdout/stderr.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

### Agent Skills — Agent SDK Cross-References Removed

References to the Claude Agent SDK were removed from three Agent Skills pages:

- **`overview.md`**: Removed the "Claude Agent SDK" section that described how Skills work with filesystem-based configuration in the SDK, including `allowed_tools` configuration and automatic discovery.
  > Removed: `The Claude Agent SDK supports custom Skills through filesystem-based configuration... Skills in the Agent SDK are then automatically discovered when the SDK runs.`

- **`best-practices.md`**: Removed the "Use Skills in the Agent SDK" card linking to `/docs/en/agent-sdk/skills`.

- **`enterprise.md`**: Removed the "Securely deploying AI agents" card linking to `/docs/en/agent-sdk/secure-deployment`.

- **`quickstart.md`**: Removed "Use Skills in the Agent SDK" navigation card from the "Next steps" section.

- *Implication*: The Agent SDK Skills integration is no longer surfaced in the Skills documentation. Developers using the SDK should check the SDK documentation directly.
- *Sources*: [Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md), [Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md), [Enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise.md), [Quickstart](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart.md)

### MCP Connector — Agent SDK Reference Removed from Note

- A note clarifying when to use `mcp_servers` vs. client-side helpers was revised to remove a reference to the Agent SDK.
  > Before: `If you're using the Agent SDK, MCP connections are managed automatically.`
  > After: This clause was removed. The note now only references the base SDK client-side helpers.
  - *Source*: [MCP Connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md)

### Agent Skills Quickstart — CLI Example Added for `--transform` File ID Extraction

- A new CLI variant was added for extracting `file_id` from code execution results using the `--transform` flag with a GJSON path expression:
  > `FILE_ID=$(ant beta:messages create --beta code-execution-2025-08-25 --beta skills-2025-10-02 --transform 'content.#.content.content.#.file_id|@flatten|0' ...)`
  - *Implication*: The `--transform` flag supports structured data extraction from API responses in the CLI, reducing the need for `jq` post-processing.
  - *Source*: [Agent Skills Quickstart](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart.md)

---

## Notable Details

- **Code example ordering changed**: Several pages (bash-tool, overview, quickstart) reordered code tabs to place Shell/CLI examples before Python/TypeScript. This is a documentation style change with no API impact.
- **JSON/SSE response blocks relabeled**: Code blocks showing API response payloads were updated from bare ` ```json ` to ` ```json Output ` throughout code-execution-tool, text-editor-tool, web-fetch-tool, web-search-tool, and programmatic-tool-calling. This is a display hint for the documentation renderer.
- **`ant beta:skills list` uses `--source anthropic`**: The CLI flag for listing Anthropic-managed skills uses `--source anthropic`, matching the `?source=anthropic` query parameter in the REST API.
- **Container reuse via `--container` flag**: The code execution CLI examples show `ant messages create --container "$CONTAINER_ID"` as the mechanism for persisting state across requests, mirroring the `container` field in the Messages API.
- **`defaultLanguage="CLI"` on some CodeGroup blocks**: The Agent Skills quickstart sets `<CodeGroup defaultLanguage="CLI">`, suggesting CLI is now the preferred default tab for new examples in this section.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| agent-skills/quickstart.md | Modified | +205/-97 | Added CLI examples throughout; reordered code tabs to CLI-first |
| tool-use/text-editor-tool.md | Modified | +114/-3 | Added CLI examples for all operations; labeled JSON blocks as Output |
| tool-use/code-execution-tool.md | Modified | +89/-19 | Simplified model compatibility; added Mythos Preview note; new error code; CLI examples |
| tool-use/programmatic-tool-calling.md | Modified | +69/-2 | Added CLI examples for request and tool-result turn; labeled JSON as Output |
| tool-use/web-fetch-tool.md | Modified | +34/-7 | Added Mythos Preview; renamed dynamic filtering section; CLI examples |
| tool-use/web-search-tool.md | Modified | +32/-5 | Added Mythos Preview; renamed dynamic filtering section; CLI examples |
| tool-use/memory-tool.md | Modified | +29/-0 | Added CLI example |
| tool-use/fine-grained-tool-streaming.md | Modified | +27/-0 | Added CLI example with eager_input_streaming |
| tool-use/bash-tool.md | Modified | +25/-17 | Added CLI example; reordered code tabs |
| tool-use/computer-use-tool.md | Modified | +20/-0 | Added CLI example |
| tool-use/overview.md | Modified | +21/-13 | Added Shell and CLI examples; reordered tabs |
| mcp-connector.md | Modified | +19/-1 | Added CLI example; removed Agent SDK reference from note |
| tool-use/tool-search-tool.md | Modified | +39/-1 | Added Mythos Preview to model support; CLI example |
| agent-skills/overview.md | Modified | +0/-17 | Removed Claude Agent SDK section and SDK navigation card |
| agent-skills/best-practices.md | Modified | +0/-7 | Removed "Use Skills in the Agent SDK" navigation card |
| agent-skills/enterprise.md | Modified | +0/-7 | Removed "Securely deploying AI agents" navigation card |

---
*Generated from Claude API documentation changes detected on 2026-04-09*
