# Claude API Documentation Changes — 2026-02-27

## Summary

14 pages in the agents-and-tools documentation section were updated with code formatting improvements. The changes are entirely presentational: inline JSON objects and arrays were expanded to multi-line form, comments were moved from inside code blocks to prose labels above them, and streaming event examples were reclassified from `json` to `sse` code fences. No API behavior, parameters, or feature availability changed.

## Notable Details

### Code Sample Formatting Standardization

All 14 modified pages received the same style of reformatting. The pattern is consistent across every file:

- **Inline object and array literals expanded to multi-line**: Single-line `messages: [{...}]` and `tools: [{...}]` patterns were replaced with multi-line equivalents. This affects JavaScript/TypeScript examples across the tool-use documentation.
  > Before: `messages: [{ role: "user", content: "..." }]`
  > After: `messages: [\n  {\n    role: "user",\n    content: "..."\n  }\n]`
  - *Implication*: No functional change; copy-paste behavior is identical. The expanded form is more readable for developers scanning examples.

- **In-block comments converted to prose headings**: Code blocks that used `// Comment text` as section labels inside a single code fence were split into separate fenced blocks, with the comment text moved to a prose line preceding each block. This applies to `bash-tool.md`, `computer-use-tool.md`, `text-editor-tool.md`, and `programmatic-tool-calling.md`.
  > Before (single block with inline comments):
  > ```json
  > // Take a screenshot
  > { "action": "screenshot" }
  > // Click at position
  > { "action": "left_click", "coordinate": [500, 300] }
  > ```
  > After (separate labeled blocks):
  > ```
  > Take a screenshot:
  > ```json
  > { "action": "screenshot" }
  > ```
  > Click at position:
  > ```json
  > { "action": "left_click", "coordinate": [500, 300] }
  > ```
  - *Implication*: Rendering in documentation portals that syntax-highlight code blocks will now show cleaner examples without comment text mixed into JSON.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md), [Bash Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool.md), [Text Editor Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool.md), [Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md)

- **Streaming event examples reclassified to `sse` code fence**: Three pages that show streaming output switched their code fence language from `json` to `sse`.
  - *Implication*: Documentation renderers that support SSE syntax highlighting will display these blocks more accurately.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md), [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md), [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md), [Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool.md)

- **Code execution tool response examples wrapped in arrays**: The bash command response and file operation response JSON examples in `code-execution-tool.md` were restructured. Previously shown as adjacent bare JSON objects, they are now presented as elements inside a `[...]` array with `hidelines={1,-1}` directives (which hide the array wrapper in rendered output but clarify the structural relationship).
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

- **MCP connector examples updated**: Two `messages: [...]` placeholders in deprecated `mcp-client-2025-04-04` migration examples were expanded from `[...]` shorthand to multi-line with a `// ...` comment, consistent with the style used elsewhere.
  - *Source*: [MCP Connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md)

- **Trailing comma removed from MCP toolset example**: The `mcp_server_name` field in a minimal `mcp_toolset` JSON snippet had a trailing comma removed, making it valid JSON.
  > Before: `"mcp_server_name": "google-calendar-mcp",`
  > After: `"mcp_server_name": "google-calendar-mcp"`
  - *Source*: [MCP Connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md)

- **`thinking` parameter example restructured**: The computer use tool's example of enabling extended thinking was wrapped in a containing object and given a `hidelines={1,-1}` directive, matching the pattern used for other partial-request snippets.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| agent-skills/quickstart.md | modified | +48 / -32 | Multi-line expansion of `messages` and `tools` arrays in 4 JavaScript code examples |
| mcp-connector.md | modified | +7 / -3 | Expanded `messages` placeholder to multi-line; removed trailing comma from `mcp_toolset` example |
| tool-use/bash-tool.md | modified | +6 / -2 | Split single code block with comments into two labeled blocks |
| tool-use/code-execution-tool.md | modified | +189 / -147 | Multi-line array expansion throughout; response examples wrapped in arrays with `hidelines`; streaming fence changed to `sse` |
| tool-use/computer-use-tool.md | modified | +44 / -14 | Split action examples into individual labeled blocks; `thinking` parameter example restructured |
| tool-use/fine-grained-tool-streaming.md | modified | +25 / -21 | Multi-line expansion of `tools` and `messages` arrays in JavaScript example |
| tool-use/implement-tool-use.md | modified | +65 / -48 | Multi-line expansion of `messages` and `tools` arrays; minor inline formatting cleanup |
| tool-use/memory-tool.md | modified | +12 / -7 | Multi-line expansion of `tools` array; `messages` placeholder expanded |
| tool-use/overview.md | modified | +23 / -19 | Multi-line expansion of `tools` and `messages` arrays |
| tool-use/programmatic-tool-calling.md | modified | +54 / -23 | Multi-line expansion throughout; invalid/valid code examples split into separate labeled blocks |
| tool-use/text-editor-tool.md | modified | +8 / -3 | Split `view` command examples into individual labeled blocks |
| tool-use/tool-search-tool.md | modified | +3 / -5 | Streaming fence changed to `sse`; `tool_reference` content collapsed to one line |
| tool-use/web-fetch-tool.md | modified | +10 / -8 | Multi-line expansion of `tools` array; `citations` object spacing; streaming fence changed to `sse` |
| tool-use/web-search-tool.md | modified | +8 / -6 | Multi-line expansion of `tools` array; streaming fence changed to `sse` |
