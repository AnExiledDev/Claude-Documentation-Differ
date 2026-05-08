# Claude API Documentation Changes — 2026-03-19

## Summary

Three pages in the `build-with-claude` section were updated. The most notable change is a **5× increase in Files API storage limits** (100 GB → 500 GB per organization). The compaction documentation revised its message-preservation example from 2 messages to 3, and includes significant C# and Java SDK code improvements. The overview page gained a tip on programmatic capability discovery via the Models API.

---

## Significant Changes

### Files API

- **Storage limit increased from 100 GB to 500 GB per organization**: The per-organization storage quota for the Files API has been multiplied by 5.
  > **Maximum file size:** 500 MB per file
  > **Total storage:** ~~100 GB~~ **500 GB per organization**

  The error documentation was updated in parallel:
  > **Storage limit exceeded (403):** Your organization has reached the **500 GB** storage limit

  - *Implication*: Organizations storing large files (PDFs, media, datasets) via the Files API can now retain substantially more data before hitting quota limits.
  - *Source*: [Files API](https://platform.claude.com/docs/en/build-with-claude/files.md)

### Context Compaction — Preserved Message Count Change

- **`pause_after_compaction` example updated to preserve 3 messages instead of 2**: The documentation example demonstrating manual compaction handling now preserves the **prior exchange + current user message (3 messages)** verbatim rather than the previous "last 2 messages (1 user + 1 assistant turn)".

  > Here's an example that uses `pause_after_compaction` to preserve the **prior exchange and the current user message (three messages total)** verbatim instead of summarizing them.

  The change is reflected consistently across all SDK examples (Python, TypeScript, C#, Go, Java, PHP, Ruby):
  ```python
  # Before
  preserved_messages = messages[-2:] if len(messages) >= 2 else messages
  # After
  preserved_messages = messages[-3:] if len(messages) >= 3 else messages
  ```

  - *Implication*: Developers following the documentation example for manual compaction handling should update their message-slicing logic from `-2` to `-3` to include the current user turn in addition to the prior assistant/user exchange.
  - *Source*: [Context Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction.md)

### Models API — Capability Discovery Tip

- **New tip added to overview: programmatic model capability discovery**: The build-with-claude overview page now surfaces that the Models API returns structured capability metadata.

  > You can discover which capabilities a model supports programmatically. The [Models API](/docs/en/api/models/list) returns `max_input_tokens`, `max_tokens`, and a `capabilities` object for every available model.

  - *Implication*: Developers can query `/v1/models` to dynamically check token limits and feature support rather than hardcoding values per model.
  - *Source*: [Build with Claude Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

---

## Notable Details

### C# SDK Code Quality Improvements (compaction.md)

Multiple C# examples throughout the compaction page were updated from `nocheck`-annotated snippets to fully working code. Key patterns that changed:

- **Collection expressions**: `new[] { "compact-2026-01-12" }` → `["compact-2026-01-12"]` and `Array.Empty<BetaMessageParam>()` → `[]` (C# 12+ collection literals used throughout)
- **Typed stop reason comparison**: `response.StopReason == "compaction"` → `response.StopReason == BetaStopReason.Compaction` (string literal replaced with enum value)
- **Streaming event discrimination**: Raw string type checks (`streamEvent.Type == "content_block_start"`) replaced with discriminated union methods (`streamEvent.TryPickContentBlockStart(out var startEvent)`, `startEvent.ContentBlock.TryPickBetaCompaction(out _)`, etc.)
- **Content block serialization**: `response.Content` assigned directly to `BetaMessageParam.Content` replaced with `.Select(b => new BetaContentBlockParam(b.Json)).ToList()`
- **Text extraction**: `block.Type == "text"` string check replaced with `.OfType<BetaTextBlock>()` LINQ pattern
- **Null safety**: `countResponse.ContextManagement.OriginalInputTokens` → `countResponse.ContextManagement?.OriginalInputTokens` (null-conditional operator added)
- **`nocheck` annotations removed** from C# code blocks (indicating the samples now compile cleanly)

### Java SDK — `nocheck` Annotations Removed

All Java code examples in the compaction page had their `nocheck` fence annotation removed (e.g., `` ```java Java nocheck `` → `` ```java Java ``), indicating those samples are now considered valid/compilable.

### Java Streaming — Null-Safe Content Length

```java
// Before
System.out.println("Compaction complete: " + cd.content().length() + " chars")
// After
System.out.println("Compaction complete: " + cd.content().map(String::length).orElse(0) + " chars")
```

### PHP SDK — Property Name Casing Change

The `pause_after_compaction` property in PHP examples was renamed to `pauseAfterCompaction` (snake_case → camelCase):
```php
// Before
'pause_after_compaction' => true
// After
'pauseAfterCompaction' => true
```
This appears in two PHP examples in the compaction page and may reflect the actual SDK property name.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `build-with-claude/compaction.md` | Modified | +117 / -79 | Message preservation count updated (2→3); C# and Java SDK examples overhauled; PHP property renamed |
| `build-with-claude/files.md` | Modified | +2 / -2 | Storage limit increased from 100 GB to 500 GB per organization |
| `build-with-claude/overview.md` | Modified | +4 / -0 | Added tip about Models API capability discovery (`max_input_tokens`, `max_tokens`, `capabilities`) |

---

*Generated from Claude API documentation changes detected on 2026-03-19*
