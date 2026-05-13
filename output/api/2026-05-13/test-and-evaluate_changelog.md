# Claude API Documentation Changes — 2026-05-13

## Summary

One page was updated in the test-and-evaluate section: the streaming refusals guide. The changes update code examples across multiple languages to use `claude-opus-4-7` (replacing `claude-sonnet-4-6` in C# and Go), refactor the Java example to use modern Java syntax (top-level `void main()` instead of a class wrapper), and make minor code quality improvements.

## Significant Changes

### Streaming Refusals — Code Example Updates

- **Model updated in C# example**: The C# `MessageCreateParams` now uses `Model.ClaudeOpus4_7` instead of `Model.ClaudeSonnet4_6`.
  > ```csharp
  > Model = Model.ClaudeOpus4_7,
  > ```
  - *Implication*: Developers copying the C# example will now use Opus 4.7 as the reference model. Existing code targeting `ClaudeSonnet4_6` is unaffected but should be reviewed for intentionality.
  - *Source*: [Handle Streaming Refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md)

- **Go example uses typed constant instead of string literal**: The Go example switches from `anthropic.Model("claude-opus-4-7")` to the typed constant `anthropic.ModelClaudeOpus4_7`.
  > ```go
  > Model: anthropic.ModelClaudeOpus4_7,
  > ```
  - *Implication*: This is the idiomatic SDK usage — the typed constant provides compile-time safety over a raw string. Developers should prefer the constant form.
  - *Source*: [Handle Streaming Refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md)

- **Java example refactored to modern Java (JEP 445 unnamed classes / instance main methods)**: The Java example was rewritten from a `public class RefusalHandling` with `public static void main` and `private static` helpers to a top-level `void main()` and `void resetConversation()` without a class wrapper. The model constant changes from `Model.CLAUDE_SONNET_4_6` to `Model.CLAUDE_OPUS_4_7`, and the reset message changes from `System.out.println` to `IO.println`.
  > ```java
  > void main() {
  >     ...
  >     .model(Model.CLAUDE_OPUS_4_7)
  > ```
  - *Implication*: The new Java style uses JEP 445 (Java 21+ preview / Java 23+ standard). Developers on older Java versions will need to wrap the code in a class. The switch from `System.out.println` to `IO.println` reflects the new implicit class I/O API.
  - *Source*: [Handle Streaming Refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md)

- **Python refusal check simplified**: The `hasattr` guard was removed from the event type check.
  > ```python
  > # Before
  > if hasattr(event, "type") and event.type == "message_delta":
  > # After
  > if event.type == "message_delta":
  > ```
  - *Implication*: The SDK now guarantees the `type` attribute exists on all stream events, so the defensive `hasattr` check is no longer necessary. This makes the code cleaner and consistent with other language examples.
  - *Source*: [Handle Streaming Refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md)

- **cURL example `max_tokens` increased**: The bash example raises `max_tokens` from `256` to `1024`.
  - *Implication*: The example now matches the token limit used across all other language examples, ensuring consistency in the documentation.
  - *Source*: [Handle Streaming Refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md)

- **Java hidden lines annotation updated**: The Java code block header changed from `hidelines={1..5,9..12,14..15,37..38,-1}` to `hidelines={1..5,9..10}`, reflecting the reduced import/boilerplate footprint of the refactored example.
  - *Implication*: Fewer lines are collapsed by default in the rendered documentation, matching the shorter example.
  - *Source*: [Handle Streaming Refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md)

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| [handle-streaming-refusals.md](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md) | modified | SIGNIFICANT | +30 / -32 | Model updates (Sonnet 4.6 → Opus 4.7 in C#/Java), Go typed constant, Java modern syntax refactor, Python `hasattr` removal, cURL `max_tokens` bump |
