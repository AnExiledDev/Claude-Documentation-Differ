# Claude API Documentation Changes — 2026-03-11

## Summary

Seven pages in the `build-with-claude` section were updated. The most notable changes are SDK-level fixes to the Files API upload interface (Go, Java, and Ruby all received revised method signatures), a data residency note removing Microsoft Foundry from the list of platforms with independent regional pricing, and extended thinking prompt-caching examples doubling their sample text size from 5,000 to 10,000 characters. The remaining changes are documentation hygiene: code-block label standardization, hardcoded IDs replaced by variables, and placeholder strings replaced with realistic example content.

---

## Significant Changes

### Files API — SDK Upload Interface Updates

The Files API documentation (`files.md`) was substantially rewritten (+252/-494 lines). The core API is unchanged, but three SDKs received revised upload signatures that developers should adopt:

- **Go SDK** — File upload now uses the `anthropic.File()` helper to attach MIME type information:

  > ```go
  > // Before
  > anthropic.BetaFileUploadParams{
  >     File:  file,   // raw *os.File, no MIME type
  >     Betas: ...
  > }
  >
  > // After
  > anthropic.BetaFileUploadParams{
  >     File:  anthropic.File(f, "document.pdf", "application/pdf"),
  >     Betas: ...
  > }
  > ```

  - *Implication*: The previous pattern passed a bare `*os.File` without an explicit MIME type or filename; the new helper makes those explicit. Existing code using the old form may need updating if the Go SDK enforces this.
  - *Source*: [Files API](https://platform.claude.com/docs/en/build-with-claude/files.md)

- **Java SDK** — File upload now uses `MultipartField.<InputStream>builder()` with explicit `.value()`, `.filename()`, and `.contentType()` fields, replacing the simpler `Path.of(...)` shorthand:

  > ```java
  > // Before
  > FileUploadParams.builder()
  >     .file(Path.of("/path/to/document.pdf"))
  >     .build()
  >
  > // After
  > FileUploadParams.builder()
  >     .file(MultipartField.<InputStream>builder()
  >         .value(Files.newInputStream(Path.of("/path/to/document.pdf")))
  >         .filename("document.pdf")
  >         .contentType("application/pdf")
  >         .build())
  >     .build()
  > ```

  - *Implication*: The new form requires an explicit `InputStream`, filename, and content type. This change gives callers full control over the multipart upload but is more verbose.
  - *Source*: [Files API](https://platform.claude.com/docs/en/build-with-claude/files.md)

- **Ruby SDK** — File upload now uses `Anthropic::FilePart.new(Pathname(...), content_type: ...)` instead of passing a raw `File.open(...)` handle:

  > ```ruby
  > # Before
  > client.beta.files.upload(
  >   file: File.open("/path/to/document.pdf", "rb")
  > )
  >
  > # After
  > client.beta.files.upload(
  >   file: Anthropic::FilePart.new(
  >     Pathname("/path/to/document.pdf"),
  >     content_type: "application/pdf"
  >   )
  > )
  > ```

  - *Implication*: The new `Anthropic::FilePart` wrapper attaches content type metadata to the upload. Code using `File.open` directly may need migration.
  - *Source*: [Files API](https://platform.claude.com/docs/en/build-with-claude/files.md)

Additionally, all Files API code examples now use variables (`file_id`, `$FILE_ID`, `fileId`) for file identifiers instead of hardcoded example IDs (previously `file_011CNha8iCJcU1wXNR6q4V8w`), making the snippets more immediately usable.

---

### Data Residency — Microsoft Foundry Removed from Third-Party Pricing Note

The data residency page was updated to remove Microsoft Foundry from the list of third-party platforms that have their own independent regional pricing:

> **Before:** "This pricing applies to the Claude API (1P) only. Third-party platforms (AWS Bedrock, Google Vertex AI, **Microsoft Foundry**) have their own regional pricing."
>
> **After:** "This pricing applies to the Claude API (1P) only. Third-party platforms (AWS Bedrock, Google Vertex AI) have their own regional pricing."

- *Implication*: It is not stated whether this reflects a change in Foundry's pricing model, or that Foundry now follows standard Claude API data residency pricing. Developers using Microsoft Foundry with data residency requirements should consult Foundry's documentation directly.
- *Source*: [Data Residency](https://platform.claude.com/docs/en/build-with-claude/data-residency.md)

---

### Extended Thinking — Prompt Caching Example Text Size Doubled

The extended thinking page updated its prompt-caching code examples (in both the system-prompt caching and message-history caching sections) to use 10,000 characters of sample text instead of 5,000:

> ```python
> # Before
> LARGE_TEXT = book_content[:5000]
>
> # After
> LARGE_TEXT = book_content[:10000]
> ```

This change is applied consistently across all SDK examples (Python, TypeScript, C#, Go, Java, PHP, Ruby) in two separate prompt-caching example sections.

- *Implication*: The updated size better ensures the example content exceeds the prompt caching minimum token threshold, making the caching examples more reliable as runnable demonstrations.
- *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

---

## Notable Details

- **Code block label standardization**: `cURL` renamed to `Shell` in code block identifiers across `context-editing.md`, `context-windows.md`, and `fast-mode.md`. This is a display/renderer change with no functional impact.

- **`fast-mode.md` response example expanded**: The JSON response example for the "checking which speed was used" section was expanded from a placeholder (`...`) to show the full response object including `content`, `model`, `stop_reason`, and `stop_sequence`. The previously abbreviated fields are now hidden via a `hidelines` directive, keeping the rendered output focused on the `usage.speed` field while preserving the complete example in source.

- **`structured-outputs.md` placeholder strings replaced**: Example code that used placeholder `"..."` for message content was updated with realistic strings (e.g., `"Extract contact info: John Smith, john@example.com, interested in the Pro plan"`, `"Invoice #12345, Date: 2024-01-15, Total: $500.00"`, `"Search for flights to Tokyo departing June 1, 2026"`). No schema or parameter changes were made.

- **Files API example boilerplate reduced**: SDK examples in `files.md` that previously included full program scaffolding (package declarations, import blocks, class wrappers) were trimmed to context-relevant snippets. The `nocheck` annotation was also removed from several examples, suggesting the code is now considered directly executable.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `files.md` | Modified | +252 / -494 | SDK upload interface updates (Go, Java, Ruby); code examples refactored to use variables and trimmed boilerplate |
| `structured-outputs.md` | Modified | +50 / -29 | Placeholder `"..."` strings replaced with realistic example content across all SDK examples |
| `extended-thinking.md` | Modified | +16 / -16 | Prompt caching sample text size increased from 5,000 to 10,000 characters across all SDKs |
| `fast-mode.md` | Modified | +5 / -2 | JSON response example expanded from placeholder to full object |
| `context-editing.md` | Modified | +4 / -4 | Code block labels renamed from `cURL` to `Shell` |
| `context-windows.md` | Modified | +1 / -1 | Code block label renamed from `cURL` to `Shell` |
| `data-residency.md` | Modified | +1 / -1 | Microsoft Foundry removed from third-party regional pricing note |

---

*Generated from Claude API documentation changes detected on 2026-03-11*
