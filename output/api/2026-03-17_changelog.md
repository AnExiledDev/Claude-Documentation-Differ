# Claude API Documentation Changes — 2026-03-17

## Summary

The primary change is the launch of `display: "omitted"` on the thinking configuration, which allows streaming applications to skip receiving thinking token content while preserving the encrypted `signature` needed for multi-turn continuity. Supporting this release are documentation updates to rate limits (new Monthly Spend Limit column), errors (new HTTP 402 code), streaming event shapes, and clarifications around PDF and image size limits.

---

## Significant Changes

### Extended Thinking — New `display` Field

- **`thinking.display` parameter controls thinking content visibility**: A new `display` field has been added to the thinking configuration object. It accepts two values:

  > `"summarized"` (default): Thinking blocks contain summarized thinking text.
  > `"omitted"`: Thinking blocks are returned with an empty `thinking` field. The `signature` field still carries the encrypted full thinking for multi-turn continuity.

  - *Implication*: Automated pipelines and latency-sensitive applications that never surface thinking content to users can now set `display: "omitted"` to reduce time-to-first-text-token during streaming. The server skips streaming thinking tokens entirely and delivers only the signature. **Billing is unchanged** — you are still charged for full thinking tokens regardless of `display` value.
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md), [Adaptive Thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md)

- **Pricing table updated for `display: "omitted"`**: Documentation now explicitly covers the token billing breakdown for omitted thinking:

  > When using `display: "omitted"`:
  > - **Input tokens:** Tokens in your original request (same as summarized)
  > - **Output tokens (billed):** The original thinking tokens that Claude generated internally (same as summarized)
  > - **Output tokens (visible):** Zero thinking tokens (the `thinking` field is empty)

  - *Implication*: Visible token counts will show zero thinking tokens, but the billed count reflects the full internal reasoning. Developers should not rely on visible token counts to estimate costs when using `display: "omitted"`.

- **Summarized thinking clarified as the default**: The documentation now explicitly states:

  > This is the default behavior when the `display` field on the thinking configuration is unset or set to `"summarized"`.

- **Disabled thinking can now be set explicitly**: The comparison table for thinking modes was updated:

  > **Disabled** | Omit `thinking` parameter **or pass `{type: "disabled"}`** | All models

  - *Implication*: Developers can now explicitly pass `{type: "disabled"}` instead of omitting the parameter, which may make intent clearer in code.

- **SDK support status for `display`**: The `display` field is not yet in any SDK's type definitions:

  > No SDK currently includes `display` in its type definitions. The Python SDK forwards unrecognized dict keys to the API at runtime; passing `display` in the thinking dict works transparently. The TypeScript SDK requires a type assertion. The C#, Go, Java, PHP, and Ruby SDKs require a direct HTTP request until native support lands.

  - *Implication*: Python developers can use the field today without code changes. TypeScript developers must cast with `as unknown as Anthropic.MessageCreateParamsNonStreaming`. For C#, Go, Java, PHP, and Ruby, a raw HTTP call is required for now.

  For adaptive thinking, the syntax is:
  ```python
  thinking = {"type": "adaptive", "display": "omitted"}
  ```

### Streaming — Thinking Block Shape Change

- **`content_block_start` for thinking blocks now includes `signature`**: The example SSE event for a thinking block start was updated:

  > Before: `{"type": "content_block_start", "index": 0, "content_block": {"type": "thinking", "thinking": ""}}`
  > After: `{"type": "content_block_start", "index": 0, "content_block": {"type": "thinking", "thinking": "", "signature": ""}}`

  - *Implication*: Applications parsing raw SSE events should expect a `signature` field (initially empty string) in the opening `content_block_start` for thinking blocks. This is additive but parsers relying on exact shape matching should be updated.
  - *Source*: [Streaming](https://platform.claude.com/docs/en/build-with-claude/streaming.md), [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

- **`display: "omitted"` streaming event sequence documented**: When omitted, no `thinking_delta` events are emitted. The sequence is:
  1. `content_block_start` (thinking block opens)
  2. Single `content_block_delta` with `signature_delta`
  3. `content_block_stop`
  4. Text content block begins streaming immediately after

  - *Source*: [Streaming](https://platform.claude.com/docs/en/build-with-claude/streaming.md)

### API Errors — New HTTP 402 Billing Error

- **New `402 billing_error` status code documented**:

  > `402 - billing_error`: There's an issue with your billing or payment information. Check your payment details in the [Console](https://platform.claude.com).

  - *Implication*: Applications handling API errors should add a case for HTTP 402, distinct from the existing `401 authentication_error`. This may surface when accounts have payment issues.
  - *Source*: [Errors](https://platform.claude.com/docs/en/api/errors.md)

### Rate Limits — Monthly Spend Limits Added

- **New "Monthly Spend Limit" column in the usage tiers table**: The rate limits documentation now documents per-tier monthly spending caps:

  | Usage Tier | Credit Purchase | Max Credit Purchase | Monthly Spend Limit |
  |---|---|---|---|
  | Tier 1 | $5 | $100 | $100 |
  | Tier 2 | $40 | $500 | $500 |
  | Tier 3 | $200 | $1,000 | $1,000 |
  | Tier 4 | $400 | $200,000 | $200,000 |
  | Monthly Invoicing | N/A | N/A | No limit |

  > **Monthly Spend Limit** is the maximum you can spend on the API each calendar month at that tier.

  - *Implication*: Developers on lower tiers now have a documented hard ceiling on monthly API spend, not just per-transaction purchase limits. Monthly Invoicing customers have no limit.
  - *Source*: [Rate Limits](https://platform.claude.com/docs/en/api/rate-limits.md)

### PDF and Vision — Large File Failure Clarifications

- **PDF support tip updated**: The previous tip mentioned splitting documents when context window fills. It now adds:

  > Requests with large PDFs can also fail before reaching the page limit, even when using the Files API. Try splitting the document into sections; for large files, since each page is processed as an image, downsampling embedded images can also help.

  - *Implication*: Using the Files API does not guarantee requests will stay under limits for very large PDFs. Pre-processing documents to reduce embedded image resolution is now explicitly recommended.
  - *Source*: [PDF Support](https://platform.claude.com/docs/en/build-with-claude/pdf-support.md)

- **Vision limits clarified for many large images**: A new note was added to the vision basics section:

  > Even when using the Files API, requests with many large images can fail before reaching the 600-image count. Reduce image dimensions or file sizes (for example, by downsampling) before uploading.

  - *Implication*: The 600-image limit is a count ceiling, not a size ceiling. Developers hitting failures at lower counts with large images should pre-scale images before upload.
  - *Source*: [Vision](https://platform.claude.com/docs/en/build-with-claude/vision.md)

---

## Notable Details

- The `signature` field behavior is consistent across both `display` values: `"summarized"` and `"omitted"` produce the same `signature`. Switching `display` values between conversation turns is supported without breaking multi-turn state.
- `display` is invalid when `thinking.type` is `"disabled"`. Setting it on a disabled thinking config will return an error.
- The `signature` field description had a minor wording simplification: "it exists solely for verification purposes" was removed. The field description now reads: "an opaque field and should not be interpreted or parsed."
- The vision docs updated the image-over-text placement tip to cross-link to the [long-context prompting best practices page](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#long-context-prompting), connecting the image ordering guidance to the existing document-query placement principle.
- PDF support intro text changed "You can now ask Claude..." to "You can ask Claude..." — the "now" removal signals PDF support is considered a stable, established feature rather than a recent launch.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| extended-thinking.md | Modified | +434 / -8 | New "Controlling thinking display" section with `display` field docs and multi-SDK code examples |
| adaptive-thinking.md | Modified | +43 / -8 | New "Controlling thinking display" section mirroring extended thinking; disabled mode wording update; pricing table for omitted thinking |
| rate-limits.md | Modified | +8 / -0 | Added Monthly Spend Limit column and values for all tiers |
| vision.md | Modified | +9 / -10 | Clarification that large images can fail before 600-image limit even with Files API; wording improvements |
| release-notes/overview.md | Modified | +3 / -0 | Added March 16, 2026 entry for `display` field launch |
| streaming.md | Modified | +3 / -1 | Documented `display: "omitted"` streaming behavior; updated `content_block_start` shape to include `signature` |
| pdf-support.md | Modified | +3 / -3 | Updated tip to cover pre-limit failures and image downsampling; minor wording fixes |
| errors.md | Modified | +1 / -0 | Added HTTP 402 `billing_error` |

---

*Generated from Claude API documentation changes detected on 2026-03-17*
