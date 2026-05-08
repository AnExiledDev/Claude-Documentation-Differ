# Claude API Documentation Changes — 2026-03-07

## Summary

This update focuses on two areas: expanded Zero Data Retention (ZDR) guidance for the new `_20260209` versions of the web search and web fetch tools, and C# SDK API corrections across several tool-use examples. Model references in implement-tool-use examples were also updated from `claude-3-7-sonnet-latest` to `claude-opus-4-6`.

---

## Significant Changes

### Tools — Web Search & Web Fetch: ZDR Eligibility Clarified for `_20260209` Versions

- **ZDR split between tool versions**: Both the web search and web fetch tools now carry expanded ZDR notes distinguishing between the older and newer tool versions.

  For web search:
  > The basic web search tool (`web_search_20250305`) is eligible for Zero Data Retention (ZDR).
  > The `web_search_20260209` version with dynamic filtering is **not** ZDR-eligible by default because dynamic filtering relies on code execution internally.

  For web fetch:
  > The basic web fetch tool (`web_fetch_20250910`) is eligible for Zero Data Retention (ZDR).
  > The `web_fetch_20260209` version with dynamic filtering is **not** ZDR-eligible by default because dynamic filtering relies on code execution internally.

  - *Implication*: Organizations with ZDR arrangements that upgrade to `_20260209` tool versions will lose ZDR coverage unless they explicitly opt out of dynamic filtering.

- **ZDR opt-out via `allowed_callers`**: Both pages now document how to use `_20260209` tools with ZDR by disabling dynamic filtering:

  ```json
  {
    "type": "web_search_20260209",
    "name": "web_search",
    "allowed_callers": ["direct"]
  }
  ```

  > This restricts the tool to direct invocation only, bypassing the internal code execution step.

  - *Implication*: `"allowed_callers": ["direct"]` is a new tool-level parameter that controls whether dynamic filtering (code execution) is invoked. Setting it to `["direct"]` restores ZDR eligibility but forfeits the token-reduction benefit of dynamic filtering.
  - *Source*: [Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool.md), [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md)

- **Web fetch ZDR caveat for third-party sites**: An additional note was added specific to web fetch:

  > While our native web fetch tool is ZDR-eligible, website publishers may retain any parameters passed to the URL if Claude fetches content from their site.

  - *Implication*: ZDR eligibility applies to Anthropic's data handling only; URL parameters sent to external sites are subject to those sites' own retention policies.
  - *Source*: [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md)

### Tools — Web Search & Web Fetch: SDK Examples Added for `_20260209` Versions

- **C#, Go, Java, PHP, and Ruby examples added** for both `web_search_20260209` and `web_fetch_20260209` dynamic-filtering tool versions. Previously only Shell, Python, and TypeScript examples existed for these newer tool versions. All new examples use `claude-opus-4-6` as the model.
  - *Source*: [Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool.md), [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md)

### SDKs — C# API Corrections Across Tool-Use Examples

Several C# code examples were updated to reflect current SDK API shapes:

- **`TryPickToolUse()` replaces LINQ `.Where(block => block.Type == "tool_use")`** in `implement-tool-use.md`:

  ```csharp
  // Before
  var toolUses = response.Content.Where(block => block.Type == "tool_use").ToList();

  // After
  var toolUses = new List<ToolUseBlock>();
  foreach (var block in response.Content)
  {
      if (block.TryPickToolUse(out var toolUse))
      {
          toolUses.Add(toolUse);
      }
  }
  ```

- **`.Id` renamed to `.ID`** on tool use blocks (`ToolUseID = toolUse.ID`), and on container references (`response1.Container!.ID`). The null-forgiving operator (`!`) was also added to the container access.

- **`TryPickText()` replaces direct `.Content[0].Text` access**:

  ```csharp
  // Before
  Console.WriteLine($"\nClaude's response:\n{finalResponse.Content[0].Text}");

  // After
  finalResponse.Content[0].TryPickText(out var text);
  Console.WriteLine($"\nClaude's response:\n{text?.Text}");
  ```

- **Assistant message content serialization updated** to use `.Select(block => new ContentBlockParam(block.Json)).ToList()` rather than passing `response.Content` directly. This applies in both `implement-tool-use.md` and the C# web-search-pause-turn example.

- **`CodeExecutionTool20260120` constructor** now used directly instead of wrapping a generic `Tool` object in `programmatic-tool-calling.md`:

  ```csharp
  // Before
  new ToolUnion(new Tool()
  {
      Type = "code_execution_20260120",
      Name = "code_execution",
      InputSchema = new InputSchema(),
  }),

  // After
  new CodeExecutionTool20260120(),
  ```

- **`ToolUseBlock.Input` in `overview.md`** changed from `JsonSerializer.SerializeToElement(new { ... })` to a `Dictionary<string, JsonElement>` for per-field serialization.

  - *Implication*: These are breaking API changes in the C# SDK. Developers using the Anthropic C# SDK should audit code that accesses `.Id`, `.Text`, or `.Content` on response blocks directly.
  - *Source*: [Implement Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use.md), [Tool Use Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md), [Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md)

### Tools — Model Reference Updated to `claude-opus-4-6`

- **`claude-3-7-sonnet-latest` replaced by `claude-opus-4-6`** in all SDK examples within `implement-tool-use.md` (Python, TypeScript, C#, Go, Java, PHP, Ruby). This affects the web-search pause-turn examples.
  - *Implication*: The recommended model for web search pause-turn examples is now `claude-opus-4-6`.
  - *Source*: [Implement Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use.md)

### ZDR Wording Standardized Across All Tool Pages

The phrase "covered by Zero Data Retention (ZDR) arrangements" was replaced with "eligible for Zero Data Retention (ZDR)" across six pages: MCP connector, code execution tool, computer use tool, memory tool, programmatic tool calling, and web fetch tool. The substance of the ZDR statements is unchanged; this is a terminology alignment.

---

## Notable Details

- **`cache_control` placement fix in web-search prompt caching example** (`web-search-tool.md`): `cache_control` was moved from the top-level message object into a content block within the `content` array. This corrects the structure to match the actual API schema, where `cache_control` must be a property of a content block, not the message itself.

- **Shell `nocheck` marker added** to curl examples in `mcp-connector.md`, `text-editor-tool.md`, and `tool-search-tool.md` (e.g., ` ```bash Shell nocheck`). This instructs documentation tooling to skip validation of those shell snippets.

- **`jq` pipe removed** from the fine-grained tool streaming Shell example: `}' | jq '.usage'` was simplified to `}'`. This is a documentation cleanup — the example no longer filters to only the usage field.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| web-search-tool.md | Modified | +147/-3 | Expanded ZDR note for `_20260209`; added C#/Go/Java/PHP/Ruby examples; fixed `cache_control` placement |
| web-fetch-tool.md | Modified | +143/-2 | Expanded ZDR note for `_20260209` with `allowed_callers`; added C#/Go/Java/PHP/Ruby examples |
| implement-tool-use.md | Modified | +28/-19 | C# SDK API updates (`TryPickToolUse`, `.ID`, content serialization); model updated to `claude-opus-4-6` |
| overview.md | Modified | +6/-2 | C# `ToolUseBlock.Input` changed to `Dictionary<string, JsonElement>` |
| programmatic-tool-calling.md | Modified | +2/-7 | C# simplified to `new CodeExecutionTool20260120()`; ZDR wording |
| mcp-connector.md | Modified | +3/-2 | ZDR wording; Shell `nocheck` |
| tool-search-tool.md | Modified | +2/-1 | Shell `nocheck` |
| code-execution-tool.md | Modified | +2/-2 | ZDR wording; C# `.Container!.ID` null-safe fix |
| computer-use-tool.md | Modified | +1/-1 | ZDR wording |
| memory-tool.md | Modified | +1/-1 | ZDR wording |
| text-editor-tool.md | Modified | +1/-1 | Shell `nocheck` |
| fine-grained-tool-streaming.md | Modified | +1/-1 | Removed `| jq '.usage'` from Shell example |

---

*Generated from Claude API documentation changes detected on 2026-03-07*
