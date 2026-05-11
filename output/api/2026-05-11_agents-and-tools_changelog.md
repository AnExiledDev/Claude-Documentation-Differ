# Claude API Documentation Changes — 2026-05-11

## Summary

Nine pages in the agents-and-tools section were updated, with changes spanning tool use documentation, the MCP connector, and SDK code examples. The most substantive changes are a documentation correction to the tool search error response type, improved safety in tool runner code examples, and a clearer explanation of how strict tool use works mechanically. All Java and C# code samples were modernized to use language-level top-level statement patterns.

## Significant Changes

### Tool Use

- **Strict mode documentation clarifies grammar-constrained sampling**: The description of `strict: true` was rewritten to explicitly name the underlying technique.
  > Previously: "uses grammar-constrained sampling to guarantee Claude's tool inputs match your JSON Schema"
  > Now: "guarantees Claude's tool inputs match your JSON Schema by constraining the model's token sampling to schema-valid outputs (a technique called grammar-constrained sampling)"
  - *Implication*: Developers now have the correct terminology to understand and explain strict mode behavior. The reordering puts the guarantee first (the outcome) and the mechanism second (how it works).
  - *Source*: [Strict Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use.md)

- **Tool search error response type corrected**: The error response JSON example in the troubleshooting section had the wrong `type` field.
  > Before: `"type": "tool_result"`
  > After: `"type": "tool_search_tool_result"`
  - *Implication*: This was a documentation bug. Developers parsing tool search error responses should use `tool_search_tool_result` as the type discriminator, not the generic `tool_result`.
  - *Source*: [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md)

- **Tool runner final-message examples made safer**: Code examples for accessing the final message content were changed from direct index access to safe iteration over content blocks.

  Python (before):
  ```python
  print(final_message.content[0].text)
  ```
  Python (after):
  ```python
  for block in final_message.content:
      if block.type == "text":
          print(block.text)
  ```
  TypeScript (before):
  ```typescript
  console.log(finalMessage.content[0].text);
  ```
  TypeScript (after):
  ```typescript
  for (const block of finalMessage.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```
  - *Implication*: The old pattern would throw if the first content block wasn't a text block (e.g., when tool use blocks appear). The new pattern correctly handles multimodal or mixed-type responses.
  - *Source*: [Tool Runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner.md)

- **Ruby tool runner adds Array type guard**: When iterating over tool results to add `cache_control`, the Ruby example now checks `tool_results_message[:content].is_a?(Array)` before calling `.each`.
  - *Implication*: Prevents a runtime `NoMethodError` if the content field is a string rather than an array, which can happen when tool results have non-array content formats.
  - *Source*: [Tool Runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner.md)

- **Handle tool calls adds cross-reference link**: The phrase "client or server tool" now links to the tool use overview page.
  - *Source*: [Handle Tool Calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls.md)

### MCP Connector

- **MCP connector TypeScript example renamed variable for clarity**: The `runner` variable returned from `toolRunner()` was renamed to `finalMessage` in the "Use with npm MCP client" example, with an added `console.log(finalMessage)` call. Similarly, a `console.log(response)` was added to the "Use MCP prompts" example.
  - *Implication*: The old code silently discarded the runner result. The rename better reflects that the awaited value is the final message, not an ongoing runner.
  - *Source*: [MCP Connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md)

- **MCP connector section headings reformatted**: Section headings changed from dash separators to colons (e.g., "Allowlist - Enable only specific tools" → "Allowlist: enable only specific tools", "MCP Tool Use Block" → "MCP tool use block").
  - *Implication*: Purely editorial; no API behavior change. Internal links/anchors using the old heading format may be affected.
  - *Source*: [MCP Connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md)

### SDK Code Examples — Cross-SDK Modernization

Java and C# examples across multiple pages were updated to use modern language patterns:

- **Java examples now use `void main()` (Java 21+ JEP 445)**: All Java samples dropped the `public class X { public static void main(String[] args) { ... } }` wrapper in favor of top-level `void main()` instance methods. Output calls changed from `System.out.println()` to `IO.println()`. Affected pages: MCP Connector, Web Search Tool, Web Fetch Tool, Tool Search Tool.

  Before:
  ```java
  public class WebSearchExample {
      public static void main(String[] args) {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();
          // ...
          System.out.println(response);
      }
  }
  ```
  After:
  ```java
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();
      // ...
      IO.println(response);
  }
  ```

- **C# examples now use top-level statements (C# 9+)**: All C# samples dropped the `class Program { static async Task Main(string[] args) { ... } }` wrapper. C# examples for the Web Fetch Tool also removed the explicit `ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")` assignment, relying on the default environment variable lookup (`AnthropicClient client = new()`). Affected pages: Strict Tool Use, Tool Search Tool, Web Fetch Tool, Web Search Tool.

- **TypeScript examples drop `async function main()` wrapper**: TypeScript samples now use top-level `await` directly rather than defining and calling a `main()` function. Affected pages: Tool Search Tool, Web Search Tool. The Web Search Tool TypeScript sample also removed the `nocheck` compiler directive from its language hint.

- **Ruby examples expose more setup code**: Multiple Ruby examples in the Tool Runner page updated `hidelines` directives to show more lines, including `require "anthropic"` and client initialization (`client = Anthropic::Client.new`), making the examples more self-contained.

## Notable Details

- The tool search tool documentation replaced "invoking" with "calling" throughout (e.g., "`server_tool_use`: Indicates Claude is calling the tool search tool"), suggesting a terminology standardization effort.
- The tool search FAQ troubleshooting example for the tool search tool definition removed an inline code comment (`// No defer_loading here`), replacing it with a clean JSON object. A separate incomplete schema snippet (`// complete schema`) was replaced with `"type": "object"` as a concrete minimal example.
- Multiple pages replaced `e.g.,` with `for example,` — consistent with a style guide update.
- The MCP connector OAuth section wording changed: "as well as refreshing the token as needed" → "and to refresh the token as needed" — a minor grammatical tightening.
- The fine-grained tool streaming tip changed "the manual pattern above" to "the preceding manual pattern" — consistent with a documentation style convention avoiding directional references.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| mcp-connector.md | Modified | +38 / -35 | Java SDK modernization; section heading reformatting; TypeScript example renamed variable; editorial prose cleanup |
| tool-search-tool.md | Modified | +160 / -175 | TypeScript/C#/Java code modernization; error response type corrected; "invoking" → "calling" terminology; inline comment cleanup |
| web-search-tool.md | Modified | +64 / -88 | TypeScript/C#/Java code modernization; TypeScript removed `nocheck` flag |
| web-fetch-tool.md | Modified | +51 / -76 | C#/Java code modernization; C# removed explicit API key lookup; added missing `print(response)` in Python example |
| strict-tool-use.md | Modified | +66 / -78 | C# code modernization; strict mode description clarified to name grammar-constrained sampling |
| tool-runner.md | Modified | +40 / -14 | Safer content access in Python/TypeScript final message examples; Ruby Array type guard; Ruby examples expose more setup lines |
| fine-grained-tool-streaming.md | Modified | +1 / -1 | Editorial: "above" → "preceding" |
| handle-tool-calls.md | Modified | +1 / -1 | Added hyperlink from "client or server tool" to overview page |
| parallel-tool-use.md | Modified | +1 / -1 | C# code block added `hidelines` attribute to hide boilerplate |

---
*Generated from Claude API documentation changes detected on 2026-05-11*
