# Claude API Documentation Changes — 2026-03-23

## Summary

13 pages in the agents-and-tools documentation section were updated. The changes are predominantly adjustments to `hidelines` directives in code block fences — a presentation-layer change controlling which lines are collapsed by default in the interactive documentation viewer. One substantive change is present: the Java SDK text editor tool example was significantly expanded to include a multi-turn conversation demonstrating tool result handling.

## Significant Changes

### Tools

- **Java Text Editor Tool Example Expanded**: The Java code example for handling text editor tool results was rewritten into a more complete multi-turn conversation. The class was renamed from `TextEditorToolExample` to `TextEditorToolResultExample`, and the example now includes an assistant turn (with a `view` tool use block) and a user turn (with the corresponding `ToolResultBlockParam`) in addition to the initial user message.
  > ```java
  > .addAssistantMessageOfBlockParams(
  >   List.of(
  >     ContentBlockParam.ofText(...),
  >     ContentBlockParam.ofToolUse(
  >       ToolUseBlockParam.builder()
  >         .name("str_replace_based_edit_tool")
  >         .input(... "command": "view", "path": "primes.py" ...)
  >         .build()
  >     )
  >   )
  > )
  > .addUserMessageOfBlockParams(
  >   List.of(ContentBlockParam.ofToolResult(ToolResultBlockParam.builder()...))
  > )
  > ```
  - *Implication*: Developers using the Java SDK now have a complete, working example of the tool-use/tool-result round-trip for the text editor tool, including the imports needed (`ContentBlockParam`, `TextBlockParam`, `ToolResultBlockParam`, `ToolUseBlockParam`).
  - *Source*: [Text Editor Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool.md)

## Notable Details

- **Code block `hidelines` directive normalization**: Across all 13 modified pages, the `hidelines` parameters on fenced code blocks were adjusted. Changes follow a consistent pattern — for example, Python blocks commonly changed from `hidelines={1..4}` or `hidelines={1..5}` to `hidelines={1..2}` (collapsing fewer import lines), TypeScript blocks often went from `hidelines={1..4}` to `hidelines={1..2}` or gained trailing-line collapse directives like `,-3..-1`, and Java blocks shifted from simple top-range hides (e.g., `hidelines={1..9,-1}`) to more precise multi-range specs (e.g., `hidelines={1..5,7..9,-2..}`). These are documentation viewer presentation changes only; no API behavior, SDK methods, or parameters changed.

- **Agent Skills quickstart**: TypeScript and Python code blocks had their `hidelines` directives removed entirely, meaning these examples now show all lines without any pre-collapsed sections. The API calls themselves are unchanged.
  - *Source*: [Agent Skills Quickstart](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| text-editor-tool.md | Modified | +52/-18 | Java example expanded to full multi-turn tool use/result conversation |
| code-execution-tool.md | Modified | +48/-48 | `hidelines` directive adjustments across all SDK code blocks |
| overview.md | Modified | +33/-33 | `hidelines` directive adjustments across all SDK code blocks |
| web-search-tool.md | Modified | +16/-16 | `hidelines` directive adjustments across all SDK code blocks |
| tool-search-tool.md | Modified | +18/-18 | `hidelines` directive adjustments across all SDK code blocks |
| web-fetch-tool.md | Modified | +14/-14 | `hidelines` directive adjustments across all SDK code blocks |
| computer-use-tool.md | Modified | +11/-11 | `hidelines` directive adjustments across all SDK code blocks |
| memory-tool.md | Modified | +7/-7 | `hidelines` directive adjustments across all SDK code blocks |
| mcp-connector.md | Modified | +6/-6 | `hidelines` directive adjustments across all SDK code blocks |
| programmatic-tool-calling.md | Modified | +6/-6 | `hidelines` directive adjustments across all SDK code blocks |
| implement-tool-use.md | Modified | +5/-5 | `hidelines` directive adjustments across all SDK code blocks |
| agent-skills/quickstart.md | Modified | +3/-3 | `hidelines` directives removed from Python and TypeScript examples |
| fine-grained-tool-streaming.md | Modified | +2/-2 | `hidelines` directive adjustments |

---
*Generated from Claude API documentation changes detected on 2026-03-23*
