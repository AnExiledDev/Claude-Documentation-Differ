# Claude API Documentation Changes — 2026-03-07

## Summary

This update focuses on expanding SDK code coverage across the documentation. Fast mode, vision, and prompt caching pages all gained C#, Go, Java, PHP, and Ruby examples where previously only a subset of SDKs were covered. The Java SDK for structured outputs has a breaking API rename (`outputFormat()` → `outputConfig()`), and C# streaming for extended thinking migrated to a new type-safe event API.

---

## Significant Changes

### Fast Mode — New SDK Examples (C#, Java, PHP, Ruby)

- **Expanded language coverage**: The fast mode documentation now includes complete code examples for C#, Java, PHP, and Ruby across all three major sections: basic usage, checking the speed field in the response, and the rate-limit fallback pattern.
  > `Speed = Speed.Fast, Betas = ["fast-mode-2026-02-01"]` (C# example added)
  > `.speed(MessageCreateParams.Speed.FAST).addBeta(AnthropicBeta.FAST_MODE_2026_02_01)` (Java example added)
  - *Implication*: Developers using C#, Java, PHP, or Ruby can now find complete fast mode examples without adapting from another language's pattern.
  - *Source*: [Fast Mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode.md)

- **JSON response example moved**: The JSON response snippet showing `"speed": "fast"` in the `usage` object was relocated from the basic usage section to the "Checking which speed was used" section, improving document flow.

### Vision — Expanded SDK Coverage and Files API Guidance

- **New SDK examples for base64, URL, and Files API image inputs**: C#, Go, PHP, and Ruby code examples were added to all three image input methods (base64-encoded, URL-based, Files API upload). Previously the vision page only covered Shell, Python, TypeScript, and Java for most sections.
  - *Implication*: All major supported SDKs now have first-class vision examples.
  - *Source*: [Vision](https://platform.claude.com/docs/en/build-with-claude/vision.md)

- **New guidance on Files API for multi-turn conversations**: A new `<Tip>` callout was added to the Files API image section explaining why referencing images by `file_id` reduces request size in agentic workflows.
  > "In multi-turn conversations and agentic workflows, each request resends the full conversation history. If images are base64-encoded, the full image bytes are included in the payload on every turn, which can significantly increase request size and latency as the conversation grows. Uploading images to the Files API and referencing them by `file_id` keeps request payloads small regardless of how many images accumulate in the conversation history."
  - *Implication*: Developers building multi-image, multi-turn agents should prefer the Files API over base64 for latency and throughput reasons.
  - *Source*: [Vision](https://platform.claude.com/docs/en/build-with-claude/vision.md)

### Structured Outputs — Java SDK API Rename

- **`outputFormat()` renamed to `outputConfig()`**: All Java SDK examples for structured outputs have been updated to use `.outputConfig(Class<T>)` instead of `.outputFormat(Class<T>)` for schema derivation.
  > Before: `.outputFormat(ContactInfo.class)`
  > After: `.outputConfig(ContactInfo.class)`
  - *Implication*: Java developers using the structured outputs helpers must update their code to use `outputConfig()`.
  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **`response.output()` accessor removed**: The Java response parsing method `response.output(Class<T>)` is replaced with `response.content().get(0).asText().text()`.
  > Before: `ContactInfo contact = response.output(ContactInfo.class);`
  > After: `ContactInfo contact = response.content().get(0).asText().text();`
  - *Implication*: Existing Java code using `response.output()` will break and must be updated.
  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **C# `InputSchema` constructor signature changed**: The C# `InputSchema` initializer was updated from object-initializer syntax with `Properties` and `Required` members to a constructor accepting a `Dictionary<string, JsonElement>`, and all C# strict tool examples now explicitly include `["additionalProperties"] = JsonSerializer.SerializeToElement(false)`.
  - *Implication*: C# developers using strict tool schemas need to update `InputSchema` construction to the dictionary-based pattern shown in the docs.
  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

### Prompt Caching — New SDK Examples (C#, Go, Ruby)

- **Automatic caching examples expanded**: The automatic caching section now includes C#, Go, and Ruby examples alongside the existing Shell, Python, TypeScript, Java, and PHP examples.
  > `CacheControl = new CacheControlEphemeral()` (C# example added)
  > `CacheControl: anthropic.NewCacheControlEphemeralParam()` (Go example added)
  - *Implication*: Developers in C#, Go, and Ruby can now use automatic caching without translating from another language's example.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

### Extended Thinking — C# SDK Type-Safe Streaming API

- **Streaming event handling updated to type-safe methods**: The C# extended thinking streaming example was updated from string-based type checks (e.g., `streamEvent.Type == "content_block_start"`) to typed dispatch methods.
  > Before: `if (streamEvent.Type == "content_block_delta") { if (streamEvent.Delta?.Type == "thinking_delta") { Console.Write(streamEvent.Delta.Thinking); } }`
  > After: `else if (streamEvent.TryPickContentBlockDelta(out var blockDelta)) { if (blockDelta.Delta.TryPickThinking(out var thinkingDelta)) { Console.Write(thinkingDelta.Thinking); } }`
  - *Implication*: C# developers should migrate extended thinking streaming code to the `TryPick*` method pattern, which is type-safe and avoids string comparisons.
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

### Overview — Memory Tool Reclassified; Compaction Availability Expanded

- **Memory tool moved to client-side tools section**: The Memory tool was moved from the "Server tools" table to the "Client-side tools" table in the build-with-claude overview.
  - *Implication*: This reflects that the Memory tool operates client-side (you control data retention), not server-side.
  - *Source*: [Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

- **Compaction availability expanded**: Compaction (`compact-2026-01-12`) is now listed as available on Amazon Bedrock (beta), Google Vertex AI (beta), and Microsoft Azure AI (beta), in addition to the Claude API (beta).
  - *Implication*: Third-party platform users can now use server-side context compaction where available.
  - *Source*: [Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

### Handling Stop Reasons — Output Token Ceiling Clarified

- **`max_tokens` comment updated to reflect streaming ceiling**: Python examples using `max_tokens=64000` for `model_context_window_exceeded` handling had their inline comment updated.
  > Before: `max_tokens=64000,  # Model's maximum output tokens`
  > After: `max_tokens=64000,  # Practical non-streaming ceiling (Opus 4.6 supports 128K with streaming)`
  - *Implication*: Claude Opus 4.6 supports up to 128K output tokens when streaming; 64K is the practical non-streaming ceiling. Developers using streaming may increase `max_tokens` beyond 64K.
  - *Source*: [Handling Stop Reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons.md)

### Zero Data Retention — Section Renamed

- **"Fully ZDR-eligible" renamed to "ZDR-eligible"**: The section heading in the ZDR eligibility table was simplified from `### Fully ZDR-eligible` to `### ZDR-eligible`.
  - *Implication*: No functional change; this is editorial. The list of ZDR-eligible features is unchanged.
  - *Source*: [Zero Data Retention](https://platform.claude.com/docs/en/build-with-claude/zero-data-retention.md)

---

## Migration Guidance

### Java SDK — Structured Outputs

The Java SDK's structured output helper API was renamed. Update all call sites:

```java
// Before
StructuredMessageCreateParams<ContactInfo> params = MessageCreateParams.builder()
    .outputFormat(ContactInfo.class)
    .build();
ContactInfo contact = response.output(ContactInfo.class);

// After
StructuredMessageCreateParams<ContactInfo> params = MessageCreateParams.builder()
    .outputConfig(ContactInfo.class)
    .build();
ContactInfo contact = response.content().get(0).asText().text();
```

### C# SDK — Strict Tool InputSchema

The `InputSchema` constructor pattern for strict tools was updated:

```csharp
// Before
InputSchema = new InputSchema()
{
    Properties = new Dictionary<string, JsonElement>
    {
        ["location"] = JsonSerializer.SerializeToElement(new { type = "string" }),
    },
    Required = ["location"],
},

// After
InputSchema = new InputSchema(new Dictionary<string, JsonElement>
{
    ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
    {
        ["location"] = new { type = "string" },
    }),
    ["required"] = JsonSerializer.SerializeToElement(new[] { "location" }),
    ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
}),
```

---

## Notable Details

- **ZDR eligibility language standardized**: Across multiple pages (`batch-processing`, `context-editing`, `context-windows`, `fast-mode`, `files`, `skills-guide`, `token-counting`, `working-with-messages`), the phrasing was changed from "covered by ZDR arrangements" or "ZDR eligible" to the consistent form "eligible for ZDR". This is editorial only; no eligibility changed.

- **Bedrock/Vertex/Azure code examples marked `nocheck`**: Several code examples in `claude-on-amazon-bedrock.md`, `claude-on-vertex-ai.md`, and `claude-in-microsoft-foundry.md` had `nocheck` added to their code block annotations, indicating they are not run as executable test code (likely because they require platform-specific credentials).

- **Compaction PHP bug fix**: The PHP compaction example had `messages: []` (empty array) corrected to `messages: [['role' => 'user', 'content' => 'Hello, Claude']]`. An empty messages array would produce an API validation error.

- **Prompt caching tool example cleanup**: A `# many more tools` placeholder comment was removed from the JSON caching example, making the example more complete and accurate.

- **Token counting shell examples improved**: Shell examples for counting tokens with images and PDFs were updated to use heredoc syntax (`<<EOF`) and `-s` flag on curl, fixing variable interpolation issues in the original inline JSON string.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| vision.md | Modified | +446/-24 | Added C#, Go, PHP, Ruby SDK examples for all image input methods; new Files API tip for multi-turn conversations |
| fast-mode.md | Modified | +311/-13 | Added C#, Java, PHP, Ruby examples for basic usage, speed checking, and rate-limit fallback |
| structured-outputs.md | Modified | +75/-64 | Java `outputFormat()` → `outputConfig()` rename; C# `InputSchema` constructor updated; added `additionalProperties: false` |
| prompt-caching.md | Modified | +108/-9 | Added C#, Go, Ruby automatic caching examples; removed placeholder comment; editorial wording |
| token-counting.md | Modified | +36/-29 | Shell example improved (heredoc syntax, `-s` flag); ZDR wording normalized |
| batch-processing.md | Modified | +41/-15 | Shell polling/cancel examples improved; C# `System` parameter type updated; ZDR wording normalized |
| claude-on-amazon-bedrock.md | Modified | +17/-9 | Code examples marked `nocheck` |
| extended-thinking.md | Modified | +10/-10 | C# streaming updated to type-safe `TryPick*` dispatch methods |
| zero-data-retention.md | Modified | +6/-6 | Section renamed "ZDR-eligible" (was "Fully ZDR-eligible") |
| prompt-engineering/claude-prompting-best-practices.md | Modified | +6/-6 | Minor punctuation normalization; Python `nocheck` flags corrected |
| skills-guide.md | Modified | +5/-6 | ZDR wording normalized; PHP example marked `nocheck`; Python `nocheck` corrected |
| handling-stop-reasons.md | Modified | +5/-5 | `max_tokens` comment updated to note 128K streaming ceiling for Opus 4.6 |
| overview.md | Modified | +2/-2 | Memory tool moved to client-side section; compaction availability expanded |
| context-editing.md | Modified | +3/-3 | ZDR wording normalized; placeholder JSON updated |
| files.md | Modified | +3/-3 | ZDR wording normalized; shell example updated |
| working-with-messages.md | Modified | +3/-3 | Minor wording/code updates |
| claude-in-microsoft-foundry.md | Modified | +4/-2 | Shell examples marked `nocheck` |
| compaction.md | Modified | +1/-1 | PHP bug fix: empty `messages: []` → valid message array |
| context-windows.md | Modified | +1/-1 | ZDR wording normalized |
| claude-on-vertex-ai.md | Modified | +2/-1 | Shell example marked `nocheck` |

---
*Generated from Claude API documentation changes detected on 2026-03-07*
