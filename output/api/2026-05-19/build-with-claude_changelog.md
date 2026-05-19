# Claude API Documentation Changes — 2026-05-19

## Summary

A new beta feature, Cache diagnostics, has been added to help developers identify why prompt cache misses occur by comparing consecutive requests. Separately, workspace-level inference geography controls (`allowed_inference_geos` and `default_inference_geo`) are now documented as available on Claude Platform on AWS — reversing previous documentation that stated they were not. A new compaction limitation was also documented regarding tool-calling failures during summarization.

## Significant Changes

### Prompt Caching

- **New: Cache Diagnostics (Beta)**: A new beta API capability allows developers to diagnose prompt cache misses by having the API compare consecutive requests and identify the exact point of divergence (model, system prompt, tools, or message history).
  > "Pass the `id` of your previous response, and the API compares the two requests and tells you where they diverged (the model, the system prompt, the tools, or the message history) so you can fix the root cause instead of guessing."
  - *How to use*: Include beta header `cache-diagnosis-2026-04-07` in requests, and pass `diagnostics: {"previous_message_id": <previous_response_id>}` in the request body. The first turn passes `null` as `previous_message_id` to opt in.
  - *Response shape*: The response gains a `diagnostics` field. When a divergence is found, it contains `cache_miss_reason` with a `type` field indicating the divergence location.
  - *Cache miss reason types*: `model_changed`, `system_changed`, `tools_changed`, `messages_changed`, `previous_message_not_found`, `unavailable`. The `*_changed` types also carry a `cache_missed_input_tokens` estimate.
  - *Streaming*: In streaming responses, `diagnostics` appears on the `message_start` event.
  - *Constraints*: Claude API only — not available on Amazon Bedrock or Vertex AI. Fingerprints are scoped to the same organization and workspace, expire after a short time, and contain only hashes and token counts (no raw prompt content). ZDR eligible.
  - *SDK support*: Code examples provided for cURL, CLI, Python, TypeScript, C#, Go, Java, PHP, and Ruby.
  - *Implication*: Developers can now programmatically detect the root cause of unexpected cache misses rather than relying solely on `usage.cache_read_input_tokens` dropping to zero.
  - *Source*: [Cache diagnostics](https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics.md)

- **Prompt caching troubleshooting now references Cache diagnostics**: The troubleshooting section of the prompt caching page gained a tip block and a bullet point pointing to the new Cache diagnostics feature.
  > "[Cache diagnostics](/docs/en/build-with-claude/cache-diagnostics) (beta) has the API compare consecutive requests and report exactly where the prompt prefix diverged, which automatically handles many of the steps in this list."
  - *Implication*: Developers following the troubleshooting guide are now directed to the new diagnostic tool as a first-line resource.
  - *Source*: [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

### Claude Platform on AWS

- **Workspace-level inference geography controls now available**: Previous documentation stated that `allowed_inference_geos` and `default_inference_geo` were *not* available on Claude Platform on AWS. This has been reversed — they are now documented as available.
  > "Workspace-level inference geography controls (`allowed_inference_geos` and `default_inference_geo`) are also available on Claude Platform on AWS. See [Workspace-level restrictions](/docs/en/manage-claude/data-residency#workspace-level-restrictions)."

  The prior text read: "Workspace-level inference geography controls...are **not** available on Claude Platform on AWS. Set `inference_geo` on each request instead."

  Additionally, the default behavior when `inference_geo` is omitted has changed:
  > "If you omit `inference_geo`, the request uses the workspace's `default_inference_geo` if one is configured, otherwise `global`."
  - *Implication*: Operators using Claude Platform on AWS can now configure inference geography at the workspace level rather than requiring it on every individual request. The prior restriction no longer applies.
  - *Source*: [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws.md)

### Compaction

- **New limitation: tool-call failure during compaction summarization**: The compaction limitations section now documents a failure mode where, when `tools` are defined in the request, the model may call a tool during the internal summarization step instead of producing a text summary.
  > "When your request includes `tools`, the model occasionally calls a tool during the internal summarization step instead of writing a summary. When this occurs, the response contains a `compaction` block with `content: null`."

  The recommended mitigation is to set the `instructions` parameter with an explicit instruction:
  ```text
  Summarize the transcript inside <summary></summary> tags. Include relevant information in the summary for continuing the task in the next context window. Do not call any tools while writing this summary; respond with text only.
  ```
  - *Implication*: Developers using compaction alongside tool definitions should add explicit `instructions` to prevent silent summarization failures (observable as `compaction.content: null` in the response).
  - *Source*: [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction.md)

## New Pages

- **cache-diagnostics.md** — Full documentation for the Cache diagnostics beta feature, including API usage, request/response format, all cache miss reason types, streaming support, multi-turn conversation threading, diagnostics-vs-usage interpretation matrix, limitations, and data retention details. [View](https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics.md)

## Notable Details

- The cache diagnostics beta header is `cache-diagnosis-2026-04-07`. Developers must include this on every turn of a conversation for diagnostics to function — omitting it on any turn will prevent fingerprint storage and break the comparison chain.
- The `diagnostics` field has four distinct states: absent (no header), `null` (no divergence or first turn), `{"cache_miss_reason": null}` (comparison pending), or `{"cache_miss_reason": {...}}` (divergence found). The pending state can occur when prefill is very fast.
- Cache diagnostics reports only the **first** point of divergence. Fixing one cause may reveal a second divergence on the next turn.
- The AWS inference geography change removes a bullet from the "not currently available" list in the Claude Platform on AWS page, indicating a feature graduation rather than a documentation correction.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| cache-diagnostics.md | New | SIGNIFICANT | +1400/-0 | New beta feature documentation for diagnosing prompt cache misses |
| claude-platform-on-aws.md | Modified | SIGNIFICANT | +3/-4 | Workspace-level inference geo controls now available; default behavior updated |
| compaction.md | Modified | SIGNIFICANT | +5/-0 | New limitation: tools may trigger tool call instead of summary during compaction |
| prompt-caching.md | Modified | SIGNIFICANT | +5/-0 | Troubleshooting section updated to reference new cache diagnostics feature |

---
*Generated from Claude API documentation changes detected on 2026-05-19*
