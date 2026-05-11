# Claude API Documentation Changes — 2026-05-11

## Summary

Sixteen pages in the `build-with-claude` section were updated. The most significant developer-facing changes are a new prefill restriction warning for four model families, a clarification that manual extended thinking is blocked on Claude Opus 4.7 specifically (not all future models), and the addition of Claude Mythos Preview to the server-side compaction beta. Code samples across C#, Java, TypeScript, Go, and PHP were updated to use modern idioms.

---

## Significant Changes

### Models & Feature Availability

- **Compaction beta now includes Claude Mythos Preview**: The list of models eligible for server-side compaction was extended.
  > "It is currently available in beta for Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6."
  - *Implication*: Developers using Claude Mythos Preview can now opt into automatic context condensation for long-running conversations.
  - *Source*: [context-windows.md](https://platform.claude.com/docs/en/build-with-claude/context-windows.md)

- **Manual extended thinking restriction scoped to Claude Opus 4.7 specifically**: The prior wording said "Claude Opus 4.7 and later models"; the updated docs now say only "Claude Opus 4.7." Claude Mythos Preview explicitly accepts `thinking: {type: "enabled", budget_tokens: N}` in addition to adaptive thinking.
  > "Manual extended thinking (`thinking: {type: \"enabled\", budget_tokens: N}`) is supported on all current Claude models **except Claude Opus 4.7**, where it is no longer accepted and returns a 400 error."
  - *Implication*: Future models are no longer pre-emptively excluded; each model's support is now documented explicitly. Claude Mythos Preview uses adaptive thinking by default but also accepts the manual budget syntax.
  - *Source*: [extended-thinking.md](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

### API Behavior Changes

- **Prefill now explicitly unsupported on four model families**: A new `<Warning>` block was added to the prefill section of the working-with-messages guide, formalizing behavior that was not previously called out.
  > "Prefilling is not supported on [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6. Requests using prefill with these models return a 400 error. Use [structured outputs](/docs/en/build-with-claude/structured-outputs) or system prompt instructions instead."
  - *Implication*: Any code that uses the `assistant` role pre-fill technique must migrate to structured outputs or system prompt guidance when targeting these models. The migration guide linked from the warning covers the patterns.
  - *Source*: [working-with-messages.md](https://platform.claude.com/docs/en/build-with-claude/working-with-messages.md)

- **Non-streaming max_tokens ceiling clarified for Python SDK**: The example ceiling in the `max_tokens` section was changed from 64,000 to 20,000, with an explanatory comment.
  > "max_tokens=20000,  # Python SDK requires streaming for max_tokens above ~21k (Opus 4.7 supports 128k with streaming)"
  - *Implication*: Non-streaming requests through the Python SDK are effectively capped near 21k output tokens; streaming must be enabled to reach the 128k output token ceiling on Opus 4.7.
  - *Source*: [handling-stop-reasons.md](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons.md)

- **`max_tokens` now required in `pause_turn` continuation examples**: Two Python examples that handle `pause_turn` stop reasons were updated to include an explicit `max_tokens` argument that was previously absent.
  - *Implication*: Omitting `max_tokens` in continuation requests was technically incorrect; the updated examples reflect that the parameter is required.
  - *Source*: [handling-stop-reasons.md](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons.md)

- **Streaming extended thinking description clarified**: The description of the streaming + extended thinking example now notes the `display: "summarized"` setting specifically.
  > "This request enables extended thinking with streaming. The `display: \"summarized\"` setting streams a condensed summary of Claude's reasoning rather than the full chain of thought."
  - *Implication*: Clarifies that the example in the docs does not stream raw thinking tokens; developers wanting full thinking content need to use a different `display` value.
  - *Source*: [streaming.md](https://platform.claude.com/docs/en/build-with-claude/streaming.md)

### Python SDK

- **Error handling updated from `APIError` to `APIStatusError`**: The fast mode fallback example replaces catching `InternalServerError` + `OverloadedError` with a broader `APIStatusError` guard that re-raises on non-5xx status codes.

  ```python
  # Before
  except (
      anthropic.InternalServerError,
      anthropic.OverloadedError,
      anthropic.APIConnectionError,
  ):
  
  # After
  except (
      anthropic.APIStatusError,
      anthropic.APIConnectionError,
  ) as error:
      if isinstance(error, anthropic.APIStatusError) and error.status_code < 500:
          raise
  ```
  - *Implication*: `OverloadedError` is no longer caught as a distinct type; only 5xx `APIStatusError` instances trigger the fallback retry. Developers with custom fallback logic should audit their error handling.
  - *Source*: [fast-mode.md](https://platform.claude.com/docs/en/build-with-claude/fast-mode.md)

- **`model_dump_json()` replaced with `print(response)`**: The search results example was simplified.
  ```python
  # Before
  print(response.model_dump_json(indent=2))
  # After
  print(response)
  ```
  - *Source*: [search-results.md](https://platform.claude.com/docs/en/build-with-claude/search-results.md)

### C# SDK

- **Top-level statements pattern adopted across all C# examples**: All C# snippets previously wrapped in `class Program { static async Task Main(string[] args) { ... } }` were rewritten to use top-level statements (C# 9+). Corresponding `using System;`, `using System.Threading.Tasks;`, and class wrapper lines were removed.
  - *Implication*: The examples are now more concise and directly runnable as `.cs` files or in interactive environments. No API surface change.
  - Affected pages: `extended-thinking.md`, `batch-processing.md`, `context-editing.md`, `fast-mode.md`, `handling-stop-reasons.md`, `pdf-support.md`, `vision.md`, `working-with-messages.md`

- **C# LINQ chain improved in Microsoft Foundry examples**: The pattern for extracting text content from `response.Content` was updated to use `.OfType<TextBlock>()` instead of `.Where(c => c.Value is TextBlock).Select(c => (c.Value as TextBlock)!.Text)`.
  ```csharp
  // Before
  .Where(c => c.Value is TextBlock)
  .Select(c => (c.Value as TextBlock)!.Text)
  
  // After
  .Select(block => block.Value)
  .OfType<TextBlock>()
  .Select(textBlock => textBlock.Text)
  ```
  - *Source*: [claude-in-microsoft-foundry.md](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md)

- **`ToolUseID` → `ID` property rename in C# extended thinking tool use example**: The property used to construct a `ToolResultBlockParam` was updated.
  ```csharp
  // Before
  ToolUseID = toolUseBlock?.Id ?? "",
  // After
  ToolUseID = toolUseBlock?.ID ?? "",
  ```
  - *Implication*: This reflects a property naming correction in the C# SDK; code using the old `.Id` property may need updating.
  - *Source*: [extended-thinking.md](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

### Java SDK

- **All Java examples updated to JDK 21 compact source file style**: `public class X { public static void main(String[] args) { } }` wrappers have been replaced with `void main() { }` (Java 21 implicit class feature). `System.out.println` → `IO.println` and `System.out.print` → `IO.print`.
  - *Implication*: The examples now target JDK 21+ compact source files (JEP 445). Code copied into a standard Java project still compiles but would need to be wrapped in a class.
  - Affected pages: `extended-thinking.md`, `fast-mode.md`, `claude-in-microsoft-foundry.md`, `claude-on-vertex-ai.md`

- **`IO.println` added in a return branch that previously had no output**: The Vertex AI and Skills Guide Go examples now print the response rather than silently ignoring it.
  - *Source*: [skills-guide.md](https://platform.claude.com/docs/en/build-with-claude/skills-guide.md), [claude-on-vertex-ai.md](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

### Go SDK

- **Typed model constants replace string literals**: Multiple extended thinking examples updated from `anthropic.Model("claude-sonnet-4-6")` to `anthropic.ModelClaudeSonnet4_6` (and the same pattern for other models).
  - *Implication*: String-based model constants still work but are not idiomatic; the typed constants are safer against typos.
  - *Source*: [extended-thinking.md](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

- **`Usage.RawJSON()` replaces `%+v` format verb**: Go examples printing usage statistics now call `.RawJSON()` to produce clean JSON output instead of the Go struct default formatting.
  ```go
  // Before
  fmt.Printf("First response usage: %+v\n", response1.Usage)
  // After
  fmt.Printf("First response usage: %s\n", response1.Usage.RawJSON())
  ```
  - *Source*: [extended-thinking.md](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

### TypeScript SDK

- **`async function main()` wrappers removed**: TypeScript examples previously wrapped in `async function main() { ... } main();` are now written as top-level `await` expressions (ESM top-level await).
  - Affected pages: `extended-thinking.md`, `pdf-support.md`, `vision.md`, `context-editing.md`

### Documentation Clarifications

- **Context editing thinking-block defaults reformatted as a table**: Previously described in a single dense paragraph, the per-model-class defaults for `clear_thinking_20251015` are now presented as a markdown table.

  | Model class | Keep all prior thinking | Keep only the last turn's thinking |
  |---|---|---|
  | Opus | Claude Opus 4.5 and later | Claude Opus 4.1 and earlier |
  | Sonnet | Claude Sonnet 4.6 and later | Claude Sonnet 4.5 and earlier |
  | Haiku | (none) | All models through Claude Haiku 4.5 |

  - *Source*: [context-editing.md](https://platform.claude.com/docs/en/build-with-claude/context-editing.md)

- **Amazon Bedrock PDF visual analysis requires citations**: The PDF support page retains and clarifies that enabling citations is required to unlock full visual PDF analysis through the Converse API; without it, Bedrock falls back to text-only extraction.
  - *Source*: [pdf-support.md](https://platform.claude.com/docs/en/build-with-claude/pdf-support.md)

- **Entra ID clarified as "formerly Azure Active Directory"**: A minor precision edit in the Microsoft Foundry provisioning steps.
  - *Source*: [claude-in-microsoft-foundry.md](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md)

- **Structured outputs Java example**: `@Schema(minimum = "1")` annotation removed from the `pageCount` field in the article schema example, aligning the sample with the documented constraint that `minimum` is not supported by the structured outputs feature.
  - *Source*: [structured-outputs.md](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **Skills guide `extract_file_ids` Python example simplified**: The `hasattr(file, "file_id")` guard was removed; the function now directly calls `file.file_id`, reflecting that all items in the concrete-typed list expose this attribute.
  - *Source*: [skills-guide.md](https://platform.claude.com/docs/en/build-with-claude/skills-guide.md)

---

## Notable Details

- The PHP examples on `vision.md` and `batch-processing.md` changed from `print_r($batch)` / `print_r($message)` to `echo $batch->id` / `echo $message->content[0]->text`, returning only the relevant field rather than the full object dump.
- Vertex AI docs now say "Vertex AI offers three endpoint types" instead of "Google Vertex AI offers three endpoint types" — a minor branding correction.
- Node.js file read comment in `pdf-support.md` updated from `import fs from "fs"` pattern to `import { readFile } from "node:fs/promises"`, preferring the `node:` protocol and promise-based API.
- Many heading changes from Title Case to sentence case across `skills-guide.md`, `streaming.md`, `vision.md`, and `pdf-support.md` are cosmetic and do not affect content.
- Widespread replacement of `e.g.,` with "for example" and `via` with "through" across structured outputs and other pages — editorial standardization.

---

## Changes by Page

| Page | Lines Added | Lines Removed | Summary |
|------|-------------|---------------|---------|
| extended-thinking.md | +747 | -802 | Model restriction scoped to Opus 4.7 only; Java/C#/Go/TS code modernization throughout |
| working-with-messages.md | +94 | -126 | New prefill restriction warning; C# top-level statements |
| batch-processing.md | +90 | -122 | C# top-level statements; PHP output style fix |
| vision.md | +86 | -98 | Section heading renamed; TS/PHP code modernization |
| fast-mode.md | +62 | -66 | Python error handling updated; Java void main() style |
| pdf-support.md | +56 | -64 | Heading case change; TS async wrapper removed |
| claude-in-microsoft-foundry.md | +51 | -45 | C# LINQ pattern improved; Java void main(); Entra ID note |
| structured-outputs.md | +50 | -43 | @Schema minimum annotation removed; wording standardization |
| claude-on-vertex-ai.md | +45 | -37 | Java void main(); branding fix |
| context-editing.md | +38 | -38 | Thinking defaults table; TS async wrapper removed |
| skills-guide.md | +31 | -21 | extract_file_ids simplified; heading case normalization |
| handling-stop-reasons.md | +21 | -28 | max_tokens ceiling corrected; APIStatusError; C# top-level |
| streaming.md | +4 | -4 | Heading case; display: summarized description added |
| context-windows.md | +1 | -1 | Mythos Preview added to compaction beta list |
| search-results.md | +1 | -1 | model_dump_json() → print() |
| claude-in-amazon-bedrock.md | +1 | -1 | Go hidelines annotation expanded |

---
*Generated from Claude API documentation changes detected on 2026-05-11*
