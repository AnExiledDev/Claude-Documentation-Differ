# Claude API Documentation Changes — 2026-03-31

## Summary

Seven pages in the `build-with-claude` section were updated. The most significant change is the addition of the `output-300k-2026-03-24` beta feature for the Message Batches API, enabling 300k-token outputs for Claude Opus 4.6 and Sonnet 4.6. Separately, documentation for the `context-1m-2025-08-07` beta header (which had provided 1M-token context windows for Sonnet 4.5 and Sonnet 4) has been removed across all platforms, reflecting a narrowing of the 1M context window to Opus 4.6 and Sonnet 4.6 only.

---

## Significant Changes

### Batch Processing

- **New beta: 300k output tokens via `output-300k-2026-03-24` header**: A new beta feature has been documented for the Message Batches API that raises the `max_tokens` cap to 300,000 for Claude Opus 4.6 and Claude Sonnet 4.6. This is a 2–5× increase over the standard per-model maximums (64k–128k).
  > The `output-300k-2026-03-24` beta header raises the `max_tokens` cap to 300,000 for batch requests using Claude Opus 4.6 or Claude Sonnet 4.6. Include the header to generate outputs far longer than the standard limit (64k to 128k depending on model) in a single turn.
  - *Availability*: Message Batches API only — not available on the synchronous Messages API, and not available on Amazon Bedrock, Vertex AI, or Microsoft Foundry.
  - *Pricing*: Standard batch pricing (50% of standard API prices) applies.
  - *Latency*: A single 300k-token generation can take over an hour; the 24-hour batch processing window accommodates this.
  - *Use cases cited*: Book-length drafts, technical documentation, exhaustive structured data extraction, large code-generation scaffolds, and long reasoning chains.
  - *SDK coverage*: Code examples provided for Shell (curl), Python, TypeScript, C#, Go, Java, PHP, and Ruby.
  - *Source*: [Batch Processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing.md)

### Context Windows — 1M Token Beta Removed for Sonnet 4.5 and Sonnet 4

- **`context-1m-2025-08-07` beta header documentation removed**: The previously documented beta path for accessing 1M-token context windows on Claude Sonnet 4.5 and Sonnet 4 has been removed from all platform-specific and general context window documentation. These models are now documented as having a 200k-token context window.

  **Before (context-windows.md):**
  > Claude Sonnet 4.5 and Sonnet 4 require the `context-1m-2025-08-07` beta header for requests beyond 200k tokens (available to organizations in usage tier 4 and those with custom rate limits). Other Claude models have a 200k-token context window.

  **After:**
  > Claude Opus 4.6 and Sonnet 4.6 have a 1M-token context window. Other Claude models, including Claude Sonnet 4.5 and Sonnet 4, have a 200k-token context window.

  - *Implication*: Developers currently relying on the `context-1m-2025-08-07` beta header with Sonnet 4.5 or Sonnet 4 should be aware this capability is no longer documented. The 1M context window is now documented exclusively for Claude Opus 4.6 and Sonnet 4.6.
  - This change is reflected consistently across all four affected pages: the main context-windows guide, Amazon Bedrock, Vertex AI, and Microsoft Foundry platform docs.
  - *Sources*: [Context Windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md), [Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md), [Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md), [Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md)

### Extended Thinking

- **Per-model output token limits clarified, 300k batch reference added**: The note on output token limits in the extended thinking guide was updated to document Sonnet 4.6 and Haiku 4.5 explicitly, and now cross-references the new 300k extended output beta.

  **Before:**
  > Claude Opus 4.6 supports up to 128k output tokens. Earlier models support up to 64k output tokens.

  **After:**
  > Claude Opus 4.6 supports up to 128k output tokens. Claude Sonnet 4.6 and Claude Haiku 4.5 support up to 64k. See the models overview for limits on legacy models. On the Message Batches API, the `output-300k-2026-03-24` beta header raises the output limit to 300k for Opus 4.6 and Sonnet 4.6.

  - *Implication*: Developers now have explicit per-model token ceilings for the current model generation, and a clear pointer to the new batch extended output path for high-volume generation.
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

### Prompt Caching

- **"Long context pricing" removed from stacking modifiers list**: The prompt caching pricing note previously stated that caching multipliers stack with "the Batch API discount, long context pricing, and data residency." The phrase "long context pricing" has been removed.

  **Before:**
  > These multipliers stack with other pricing modifiers such as the Batch API discount, long context pricing, and data residency.

  **After:**
  > These multipliers stack with other pricing modifiers such as the Batch API discount and data residency.

  - *Implication*: Long context pricing is no longer called out as a distinct stacking modifier for prompt caching. This is consistent with the broader removal of the 1M context window beta for Sonnet 4.5/Sonnet 4 — if those models no longer have a documented long context tier, the stacking interaction no longer applies in practice.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

---

## Migration Guidance

- **1M context window on Sonnet 4.5 / Sonnet 4**: If your application passes the `context-1m-2025-08-07` beta header with Claude Sonnet 4.5 or Sonnet 4, review whether this still functions as expected. Documentation no longer describes this capability for these models; you may need to migrate to Claude Opus 4.6 or Sonnet 4.6 for 1M-token context requirements.

- **Extended output in batches**: To use the new 300k output cap, pass `"output-300k-2026-03-24"` in the `betas` array (Python/TypeScript SDKs) or as the `anthropic-beta` header (direct HTTP). Only `claude-opus-4-6` and `claude-sonnet-4-6` support this beta, and only via the Batches API endpoint (`/v1/messages/batches`).

  ```python
  # Python SDK
  message_batch = client.beta.messages.batches.create(
      betas=["output-300k-2026-03-24"],
      requests=[
          Request(
              custom_id="my-request",
              params=MessageCreateParamsNonStreaming(
                  model="claude-opus-4-6",
                  max_tokens=300_000,
                  messages=[{"role": "user", "content": "..."}],
              ),
          ),
      ],
  )
  ```

  ```typescript
  // TypeScript SDK
  const messageBatch = await anthropic.beta.messages.batches.create({
    betas: ["output-300k-2026-03-24"],
    requests: [{
      custom_id: "my-request",
      params: {
        model: "claude-opus-4-6",
        max_tokens: 300000,
        messages: [{ role: "user", content: "..." }]
      }
    }]
  });
  ```

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| batch-processing.md | Modified | +247 / -0 | Added "Extended output (beta)" section documenting the `output-300k-2026-03-24` beta header with full SDK code examples |
| context-windows.md | Modified | +1 / -5 | Removed `context-1m-2025-08-07` beta header docs for Sonnet 4.5 and Sonnet 4; these models now documented at 200k |
| claude-on-amazon-bedrock.md | Modified | +1 / -5 | Same 1M context window beta removal for Sonnet 4.5 and Sonnet 4 on Bedrock |
| claude-on-vertex-ai.md | Modified | +1 / -5 | Same 1M context window beta removal for Sonnet 4.5 and Sonnet 4 on Vertex AI |
| claude-in-microsoft-foundry.md | Modified | +1 / -5 | Same 1M context window beta removal for Sonnet 4.5 on Microsoft Foundry |
| extended-thinking.md | Modified | +1 / -1 | Clarified per-model output token limits; added cross-reference to 300k batch beta |
| prompt-caching.md | Modified | +1 / -1 | Removed "long context pricing" from the list of pricing modifiers that stack with caching multipliers |

---

*Generated from Claude API documentation changes detected on 2026-03-31*
