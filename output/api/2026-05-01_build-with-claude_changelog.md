# Claude API Documentation Changes — 2026-05-01

## Summary

The primary change is the addition of an official **cache pre-warming** feature to prompt caching, which formalizes `max_tokens: 0` as a supported API mechanism for loading system prompts into cache before user traffic arrives. Accompanying updates note limitations of this feature in adjacent APIs (Message Batches, extended thinking). The search results citation reference documentation was also clarified with more precise field semantics.

---

## Significant Changes

### Prompt Caching — Cache Pre-Warming (`max_tokens: 0`)

- **New `max_tokens: 0` parameter value for cache pre-warming**: Setting `max_tokens: 0` on a `/v1/messages` request triggers the full prefill phase (writing cache at any `cache_control` breakpoints) and returns immediately without generating output. The response contains an empty `content` array, `stop_reason: "max_tokens"`, and a fully populated `usage` block.

  > "Set `max_tokens: 0` in your request. The API runs the full prefill phase (reading your prompt into the model and writing the cache at any `cache_control` breakpoint), then returns immediately without generating any output."

  - *Implication*: Developers can now explicitly warm a shared system-prompt cache before user traffic arrives, eliminating the cache-miss latency penalty on first interactions (TTFT improvement). This is an official replacement for the earlier `max_tokens: 1` workaround.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **Cache write billing applies to pre-warm requests**: A pre-warm call incurs a cache write charge if the prefix is not already cached. Zero output tokens are billed.

  > "A pre-warm request incurs a **cache write** charge if the prefix is not already cached, the same as any other request. Check `usage.cache_creation_input_tokens` in the response to confirm a write occurred. Zero output tokens are billed."

  - *Implication*: Pre-warming is not free — developers should confirm `cache_creation_input_tokens` in the response and account for write costs in their budget. For 5-minute TTL caches, a new pre-warm request must be sent at least every 5 minutes to keep the cache warm.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **Explicit `cache_control` breakpoint placement required**: The `cache_control` breakpoint must be placed on the last shared block (e.g., the system prompt), not on the placeholder user message. Automatic caching is not compatible because it places the breakpoint on the last block (the placeholder), which is not shared with follow-up requests.

  > "Place the `cache_control` breakpoint on the last block that is shared with the follow-up request (typically your system prompt or tool definitions), not on the placeholder user message... This means using an explicit cache breakpoint rather than automatic caching."

  - *Implication*: Developers using automatic caching must switch to explicit `cache_control` placement when implementing cache pre-warming.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **`max_tokens: 0` limitations**: The following combinations are rejected with `invalid_request_error`:
  - `stream: true`
  - Extended thinking (`thinking.type: "enabled"`)
  - Structured outputs (`output_config.format`)
  - `tool_choice` of `{"type": "tool", ...}` or `{"type": "any"}`
  - Message Batches requests

  > "A `max_tokens: 0` request is rejected with an `invalid_request_error` if any of the following are set, since each implies output that a zero-token budget cannot produce."

  - *Implication*: Cache pre-warming is limited to non-streaming, non-thinking, non-structured-output requests, and cannot be used inside a batch job.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **SDK examples added for all supported SDKs**: Full code examples for cache pre-warming are documented for cURL, CLI, Python, TypeScript, C#, Go, Java, PHP, and Ruby.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

### Message Batches — `max_tokens: 0` Restriction

- **`max_tokens: 0` (cache pre-warming) explicitly disallowed in batches**: The batch-processing limitations section now states that each batched request must have `max_tokens` of at least `1`.

  > "Each batched request must have `max_tokens` of at least `1`. `max_tokens: 0` (cache pre-warming) is not supported inside a batch, since an ephemeral cache entry written during batch processing would likely expire before the follow-up request runs."

  - *Implication*: Developers must not include pre-warm requests inside a Message Batch payload. Pre-warming targets TTFT, which does not apply to batch processing.
  - *Source*: [Batch Processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing.md)

### Extended Thinking — Incompatibility with `max_tokens: 0`

- **Extended thinking cannot be combined with `max_tokens: 0`**: The `budget_tokens` constraint requires `budget_tokens < max_tokens`, which is impossible when `max_tokens` is `0`.

  > "Because `budget_tokens` must be less than `max_tokens`, extended thinking cannot be combined with `max_tokens: 0` (cache pre-warming)."

  - *Implication*: Clarifies a constraint that was previously implicit. No behavioral change.
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

### Search Results — Citation Field Semantics Clarified

- **`cited_text` field clarified**: The description now explicitly states that `cited_text` contains the full concatenated text of all cited blocks and is **not** counted toward output tokens.

  > "`cited_text` | string | The full text of the cited block(s), concatenated. Equals the contents of `content[start_block_index:end_block_index]` joined together. Not counted toward output tokens."

  - *Implication*: Developers who were budgeting output tokens and including `cited_text` length should note that it does not contribute to output token costs.
  - *Source*: [Search Results](https://platform.claude.com/docs/en/build-with-claude/search-results.md)

- **`end_block_index` semantics clarified as exclusive**: The field is now documented as an exclusive end index (Python-slice semantics), and is guaranteed to be greater than `start_block_index`.

  > "`end_block_index` | integer | Exclusive end index of the cited block range in the search result's `content` array. Always greater than `start_block_index`."

  - *Implication*: Developers parsing citation ranges should treat `end_block_index` as exclusive — i.e., `content[start_block_index:end_block_index]`.
  - *Source*: [Search Results](https://platform.claude.com/docs/en/build-with-claude/search-results.md)

- **`search_result_index` ordering clarified**: Now explicitly documented as the 0-based index among all `search_result` blocks in the request, in the order they appear across all messages and tool results (not just within a single message).

  > "`search_result_index` | integer | 0-based index of the cited search result among all `search_result` blocks in the request, in the order they appear (across all messages and tool results)."

  - *Source*: [Search Results](https://platform.claude.com/docs/en/build-with-claude/search-results.md)

- **Added concrete JSON example for multiple content block citations**: The documentation now includes a full example showing what a citation object looks like when citing a specific content block within a multi-block search result.
  - *Source*: [Search Results](https://platform.claude.com/docs/en/build-with-claude/search-results.md)

- **Block-level citation granularity guidance added**: Documentation now explicitly states that Claude cites whole blocks, not substrings within a block, and advises splitting content into smaller blocks for finer citation boundaries.

  > "The text block is the minimal citable unit: Claude cites whole blocks, not substrings within a block. To get finer-grained citations, split your search result content into smaller blocks."

  - *Source*: [Search Results](https://platform.claude.com/docs/en/build-with-claude/search-results.md)

---

## Migration Guidance

### Replacing the `max_tokens: 1` Cache Warm-Up Workaround

If your application uses `max_tokens: 1` requests to pre-warm the prompt cache, migrate to `max_tokens: 0`:

```python
# Before (max_tokens: 1 workaround — produces a single-token reply to discard)
prewarm = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1,
    system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
    messages=[{"role": "user", "content": "warmup"}],
)
# Discard prewarm.content[0].text

# After (max_tokens: 0 — no output, no output token cost, unambiguous intent)
prewarm = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=0,
    system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
    messages=[{"role": "user", "content": "warmup"}],
)
# prewarm.content == [], prewarm.stop_reason == "max_tokens"
```

> "The `max_tokens: 0` approach is preferred: no output is produced, so there is no single-token reply to discard, no output tokens are billed, and the intent of the request is unambiguous."

---

## Notable Details

- The placeholder user message content for a pre-warm request can be any non-whitespace string (examples use `"warmup"`). Its content is read during prefill but never answered.
- The example pre-warm API response shows `usage.cache_creation.ephemeral_5m_input_tokens: 5120`, confirming that standard 5-minute ephemeral TTL is used by default.
- The citations warning about "all-or-nothing" behavior had a trailing sentence removed: the original advised disabling citations for all results if some must be disabled; the updated version omits this prescriptive guidance (the all-or-nothing constraint itself remains).
- The search-results "Key benefits" list formatting changed from ` - **Term** - description` to ` - **Term:** description` (dash separators replaced with colons). This is a cosmetic documentation style change.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| prompt-caching.md | Modified | +346 / -0 | Added full "Pre-warming the cache" section: `max_tokens: 0` feature, how-it-works, usage pattern, limitations, migration from `max_tokens: 1`, code examples for 9 SDKs |
| search-results.md | Modified | +42 / -41 | Clarified `cited_text`, `end_block_index` (exclusive), and `search_result_index` semantics; added multi-block citation JSON example; minor list formatting changes |
| batch-processing.md | Modified | +1 / -0 | Added limitation note: `max_tokens: 0` (cache pre-warming) not allowed in batch requests |
| extended-thinking.md | Modified | +1 / -1 | Noted that extended thinking cannot be combined with `max_tokens: 0` |

---

*Generated from Claude API documentation changes detected on 2026-05-01*
