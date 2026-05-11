# Claude API Documentation Changes — 2026-05-11

## Summary

One documentation page was updated with a minor clarification. The change expands the described recovery options when handling a `stop_reason: refusal` in streaming responses, explicitly listing "clear the conversation history entirely" as a valid reset strategy alongside removing or rephrasing the offending turn. No API behavior, parameters, or endpoints changed.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| [handle-streaming-refusals.md](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md) | Modified | +1/-1 | Expanded context-reset guidance to include three recovery options |

## Notable Details

- **Streaming refusal recovery options clarified**: The "Reset context after refusal" section previously described resetting by "removing or updating the turn that was refused." The updated text explicitly enumerates three options:

  > You can remove or rephrase the turn that triggered the refusal, or clear the conversation history entirely.

  This is a documentation clarification only — the underlying API behavior is unchanged. Developers who were already clearing full conversation history (rather than surgically removing the offending turn) can now see that approach is explicitly supported.
  - *Source*: [Handle Streaming Refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md)

---
*Generated from Claude API documentation changes detected on 2026-05-11*
