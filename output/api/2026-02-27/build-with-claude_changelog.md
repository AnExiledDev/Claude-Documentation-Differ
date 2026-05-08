# Claude API Documentation Changes — 2026-02-27

## Summary

23 pages in the `build-with-claude` section were updated. The substantive changes include: new Java, Go, and Ruby streaming examples added to the streaming documentation; a new "Property ordering" section added to structured outputs; and a cache minimum token threshold update for Claude Sonnet 4.6 in prompt caching. The remainder of changes are TypeScript/JavaScript code formatting normalization across many pages (array literal style, line-length wrapping).

---

## Significant Changes

### Streaming

- **New Java, Go, and Ruby streaming examples**: The streaming documentation now includes complete code examples for Java, Go, and Ruby SDKs demonstrating streaming with the `web_search` tool (`WebSearchTool20250305`). Previously, only Python and TypeScript examples were shown for the web-search streaming section.

  Java example uses `client.messages().createStreaming(params)` with the OkHttp client:
  ```java
  try (var streamResponse = client.messages().createStreaming(params)) {
      streamResponse.stream().forEach(event -> {
          event.contentBlockDelta().ifPresent(deltaEvent ->
              deltaEvent.delta().text().ifPresent(td ->
                  System.out.print(td.text())
              )
          );
      });
  }
  ```
  Go uses `client.Messages.NewStreaming(...)` with event-type switching. Ruby uses `client.messages.stream(...).text.each`.

  - *Implication*: Java, Go, and Ruby developers now have first-class streaming reference examples directly in the docs.
  - *Source*: [Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming.md)

- **SSE code blocks re-labeled**: All streaming event examples that were tagged as ` ```json ` blocks have been re-tagged as ` ```sse `. This affects the `streaming.md`, `extended-thinking.md`, and `citations.md` pages. Affected blocks include: error events, text deltas, input JSON deltas, thinking deltas, signature deltas, and full streaming response examples.

  > Before: ` ```json Example error `
  > After: ` ```sse Example error `

  - *Implication*: Syntax highlighters and documentation renderers that understand SSE formatting will now display these blocks correctly rather than attempting JSON highlighting on SSE event data.
  - *Source*: [Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming.md)

### Structured Outputs

- **New "Property ordering" section**: A new section documents how properties are ordered in structured output responses. Required properties appear first (in schema order), followed by optional properties (in schema order), regardless of their position in the original schema definition.

  > When using structured outputs, properties in objects maintain their defined ordering from your schema, with one important caveat: **required properties appear first, followed by optional properties**.

  Example: for a schema with `["notes", "name", "email", "age"]` where `name` and `email` are required, the output will order: `name`, `email`, `notes`, `age`.

  > If property order in the output is important to your application, ensure all properties are marked as required, or account for this reordering in your parsing logic.

  - *Implication*: Applications that depend on specific JSON property ordering in structured output responses must either mark all properties as `required` or handle this reordering in their parsing logic.
  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

### Prompt Caching

- **Claude Sonnet 4.6 minimum cacheable token threshold raised to 2048**: The cache limitations table was updated to split `Claude Sonnet 4.6` out from `Claude Sonnet 4.5` with a higher minimum.

  > Before: `1024 tokens for Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.1, ...`
  > After:
  > - `2048 tokens for Claude Sonnet 4.6`
  > - `1024 tokens for Claude Sonnet 4.5, Claude Opus 4.1, ...`

  - *Implication*: Prompts shorter than 2048 tokens will not be cached when using `claude-sonnet-4-6`. Applications designed around the previous 1024-token threshold for Sonnet 4.6 may need to revisit their caching strategy.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **Extended cache TTL example simplified**: The `cache_control` snippet for the 1-hour extended cache duration was updated to show only `"ttl": "1h"` rather than `"5m" | "1h"` union notation. The example now uses concrete token values instead of ellipsis placeholders in the usage response block.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

### Context Editing

- **Example JSON configurations split into separate blocks**: Two inline-commented code blocks in the `clear_thinking_20251015` configuration section were split into separate, properly labeled JSON blocks. Comments like `// Keep thinking blocks from the last 3 assistant turns` were moved outside the JSON block as prose headings.

  - *Implication*: The examples are now valid JSON (comments are not valid JSON) and will render correctly in documentation viewers that validate JSON syntax.
  - *Source*: [Context Editing](https://platform.claude.com/docs/en/build-with-claude/context-editing.md)

---

## Notable Details

- **Broad TypeScript array-literal formatting normalization**: Across at least 15 pages, TypeScript/JavaScript code examples were reformatted to use multi-line array syntax (`messages: [\n  { ... }\n]`) instead of inline object-in-array syntax (`messages: [{ ... }]`) for single-element arrays. This is consistent formatting only — no API behavior changes.

- **`hidelines` directives added to TypeScript snippets in `context-editing.md`**: Several TypeScript code blocks in the compaction/context-editing section gained `hidelines={1,-1}` annotations (e.g., ` ```typescript TypeScript hidelines={1,7..9,-1} `). These are rendering directives that hide wrapper boilerplate code in the UI, not API changes.

- **Batch processing `.jsonl` code block label corrected**: A code fence for JSONL output was changed from ` ```json .jsonl file ` to ` ```jsonl .jsonl file `, matching its actual format.
  - *Source*: [Batch Processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing.md)

- **Prompt caching auto-cache table clarified**: The auto-cache behavior table was updated to use a cleaner `User(N)` / `Asst(N)` turn numbering notation (with `<br/>` line breaks for readability) replacing the previous single-line `User:A + Asst:B + User:C` format.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| streaming.md | Modified | +123 / -16 | Added Java, Go, Ruby streaming examples; re-labeled SSE code blocks |
| context-editing.md | Modified | +103 / -69 | Formatting; split inline-commented JSON into separate blocks; hidelines annotations |
| structured-outputs.md | Modified | +93 / -45 | New "Property ordering" section; code formatting |
| skills-guide.md | Modified | +76 / -89 | Code formatting (array/object style) |
| extended-thinking.md | Modified | +65 / -57 | Code formatting; SSE block re-labeling |
| batch-processing.md | Modified | +62 / -66 | Code formatting; `.jsonl` language tag fix |
| prompt-caching.md | Modified | +30 / -21 | Sonnet 4.6 min cache tokens raised to 2048; table/example updates |
| token-counting.md | Modified | +31 / -24 | Code formatting |
| working-with-messages.md | Modified | +22 / -20 | Code formatting |
| compaction.md | Modified | +18 / -23 | Code formatting |
| files.md | Modified | +18 / -18 | Code formatting |
| adaptive-thinking.md | Modified | +12 / -8 | Code formatting |
| search-results.md | Modified | +10 / -8 | Code formatting |
| vision.md | Modified | +9 / -6 | Code formatting |
| pdf-support.md | Modified | +8 / -6 | Code formatting |
| data-residency.md | Modified | +6 / -4 | Code formatting |
| effort.md | Modified | +6 / -4 | Code formatting |
| fast-mode.md | Modified | +6 / -4 | Code formatting |
| citations.md | Modified | +3 / -2 | SSE code block re-labeling |
| prompt-engineering/claude-prompting-best-practices.md | Modified | +3 / -3 | Code formatting |
| embeddings.md | Modified | +2 / -3 | Minor formatting |
| claude-in-microsoft-foundry.md | Modified | +1 / -4 | Code formatting |
| context-windows.md | Modified | +1 / -3 | Code formatting |

---
*Generated from Claude API documentation changes detected on 2026-02-27*
