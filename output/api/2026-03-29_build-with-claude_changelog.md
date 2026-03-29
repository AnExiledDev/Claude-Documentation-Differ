# Claude API Documentation Changes — 2026-03-29

## Summary

This update expands the deprecation of `thinking.type: "enabled"` with `budget_tokens` to cover both Claude Sonnet 4.6 and Claude Opus 4.6 (previously only Opus 4.6 was explicitly called out). Adaptive thinking is now positioned as the primary and recommended approach for both models, with `budget_tokens` explicitly marked as a migration-only path. Prompt caching documentation was also improved with clearer guidance on silent cache misses.

---

## Significant Changes

### Extended Thinking / Adaptive Thinking

- **`budget_tokens` deprecation extended to Claude Sonnet 4.6**: Previously, docs warned that `thinking.type: "enabled"` with `budget_tokens` was deprecated only on Opus 4.6. The deprecation now explicitly covers Sonnet 4.6 as well, and links to the feature availability reference.
  > `` `budget_tokens` is [**deprecated**](/docs/en/build-with-claude/overview#feature-availability) on Claude Opus 4.6 and Claude Sonnet 4.6 and will be removed in a future model release. Use [adaptive thinking](/docs/en/build-with-claude/adaptive-thinking) with the [effort parameter](/docs/en/build-with-claude/effort) to control thinking depth instead. ``
  - *Implication*: Developers using `thinking.type: "enabled"` with `budget_tokens` on Sonnet 4.6 should begin planning migration to `thinking.type: "adaptive"` with the `effort` parameter. The feature remains functional but is no longer recommended.
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

- **Interleaved thinking beta header deprecated on Sonnet 4.6**: The `interleaved-thinking-2025-05-14` beta header with manual extended thinking on Sonnet 4.6 is now deprecated. Adaptive thinking automatically enables interleaved thinking and is the recommended path.
  > `Claude Sonnet 4.6: Interleaved thinking is automatically enabled when using adaptive thinking (recommended). The interleaved-thinking-2025-05-14 beta header with manual extended thinking (thinking: {type: "enabled"}) is still functional but deprecated.`
  - *Implication*: Sonnet 4.6 users relying on the `interleaved-thinking-2025-05-14` header should migrate to adaptive mode. For other Claude 4 models (Opus 4.5, Opus 4.1, Opus 4, Sonnet 4.5, Sonnet 4), the header continues to be the supported mechanism.
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

- **Adaptive thinking deprecation language strengthened**: The tip callout on the adaptive thinking page no longer frames `budget_tokens` as a valid alternative for latency-sensitive workloads. It is now explicitly deprecated and "no longer recommended."
  > `If your workload requires predictable latency or precise control over thinking costs, extended thinking with budget_tokens is still functional on these models but is deprecated and no longer recommended. See the warning below.`
  - *Implication*: The previous framing suggested `budget_tokens` remained appropriate for certain workloads; that guidance is retracted. Effort parameter tuning or `max_tokens` limits are now the recommended cost-control tools.
  - *Source*: [Adaptive Thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md)

### Prompting Best Practices — Restructured Thinking Migration Guidance

- **"When to try adaptive thinking" section removed; adaptive thinking becomes the default**: The best practices guide for Sonnet 4.6 was restructured. Previously, extended thinking with `budget_tokens` was presented as the default path with a "when to try adaptive" opt-in section. The structure is now inverted: adaptive thinking is presented first and as primary, with `budget_tokens` covered under a "Keeping budget_tokens during migration" subsection.

  New primary code example for Sonnet 4.6:
  ```python
  client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=64000,
      thinking={"type": "adaptive"},
      output_config={"effort": "high"},
      messages=[{"role": "user", "content": "..."}],
  )
  ```
  Recommended effort levels by workload:
  - **Multi-step agents, coding, computer use**: start at `high`, scale down to `medium` if latency or token usage is a concern
  - **Chat, content generation, classification**: `low` effort with the option to increase to `medium` for more depth

  - *Implication*: Developers migrating from Sonnet 4.5 to Sonnet 4.6 should target adaptive thinking as the migration destination, not a like-for-like `budget_tokens` port. The docs now explicitly state the Sonnet 4.5 `budget_tokens` path "is still functional on Claude Sonnet 4.6 but is deprecated."
  - *Source*: [Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

### Prompt Caching — Silent Failure Guidance

- **Clarified behavior when prompt falls below cache minimum**: The docs now explicitly state that sub-minimum caching attempts fail silently (no error), and describe how to detect the failure.
  > `Any requests to cache fewer than this number of tokens will be processed without caching, and no error is returned. To verify whether a prompt was cached, check the response usage fields: if both cache_creation_input_tokens and cache_read_input_tokens are 0, the prompt was not cached (likely because it did not meet the minimum length requirement).`
  - *Implication*: Developers debugging unexpected cache misses should check both `cache_creation_input_tokens` and `cache_read_input_tokens` in the response. The troubleshooting section now mirrors this guidance with a note that "length-based caching failures are silent."
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **New guidance: expand cached content to reach the minimum threshold**: A new tip recommends padding cached content to hit the minimum when close to the threshold.
  > `If your prompt falls just short of the minimum for the model you are using, expanding the cached content to reach the threshold is often worthwhile. Cache reads cost significantly less than uncached input tokens, so reaching the minimum can reduce costs for frequently reused prompts.`
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

### Fast Mode

- **Pricing clarification for requests over 200k tokens**: Fast mode pricing is confirmed to be 6x standard Opus rates across the full context window, including for requests that exceed 200k input tokens.
  > `Fast mode is priced at 6x standard Opus rates across the full context window, including requests over 200k input tokens.`
  - *Implication*: Removes ambiguity about whether pricing changes at the 200k token boundary; it does not.
  - *Source*: [Fast Mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode.md)

### Compaction

- **Token usage response example updated with clarification**: The example JSON was updated to reflect smaller token values, and a new sentence clarifies the relationship between top-level fields and the `iterations` array.
  > `The top-level input_tokens and output_tokens match the message iteration exactly in this example because there is only one non-compaction iteration.`
  - *Implication*: Helps developers correctly interpret compaction responses; top-level token counts reflect non-compaction iterations only, not the compaction step itself.
  - *Source*: [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction.md)

- **Cookbook link updated to specific recipe**: The "Next steps" card now links directly to the session memory compaction cookbook (`/cookbook/misc-session-memory-compaction`) rather than the generic cookbook landing page.
  - *Source*: [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction.md)

---

## Migration Guidance

- **Sonnet 4.6 — Migrate from `budget_tokens` to adaptive thinking**:
  ```python
  # Before (deprecated, still functional)
  client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=16384,
      thinking={"type": "enabled", "budget_tokens": 16384},
      output_config={"effort": "medium"},
      messages=[{"role": "user", "content": "..."}],
  )

  # After (recommended)
  client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=64000,
      thinking={"type": "adaptive"},
      output_config={"effort": "high"},
      messages=[{"role": "user", "content": "..."}],
  )
  ```

- **Sonnet 4.6 — Remove `interleaved-thinking-2025-05-14` beta header**: If using the beta header for interleaved thinking on Sonnet 4.6, switch to adaptive mode, which enables interleaved thinking automatically with no beta header required.

---

## Notable Details

- The deprecation warning for `budget_tokens` on both Opus 4.6 and Sonnet 4.6 now links to `/docs/en/build-with-claude/overview#feature-availability` — a signal that this is a tracked, versioned deprecation with an expected removal timeline tied to future model releases.
- The `api-and-data-retention.md` section heading was renamed from "Our approach to data retention" to "Anthropic's approach to data retention." This is a cosmetic change but updates an internal cross-reference link anchor from `#our-approach-to-data-retention` to `#anthropics-approach-to-data-retention`.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| prompt-engineering/claude-prompting-best-practices.md | Modified | +25/-25 | Restructured Sonnet 4.6 thinking guidance; adaptive thinking is now primary, budget_tokens covered as deprecated migration path |
| extended-thinking.md | Modified | +6/-6 | Deprecation scope extended to Sonnet 4.6; interleaved beta header deprecated on Sonnet 4.6 |
| compaction.md | Modified | +5/-5 | Token usage example clarified; cookbook link updated to specific recipe |
| adaptive-thinking.md | Modified | +4/-4 | Deprecation language strengthened; budget_tokens framed as no longer recommended |
| prompt-caching.md | Modified | +4/-2 | Silent failure behavior documented; new tip on expanding prompts to reach cache minimum |
| api-and-data-retention.md | Modified | +2/-2 | Section heading renamed from "Our approach" to "Anthropic's approach" |
| effort.md | Modified | +1/-1 | Sonnet 4.6 description updated to reflect adaptive thinking as primary; manual mode deprecated |
| fast-mode.md | Modified | +1/-1 | Pricing clarified to explicitly include requests over 200k input tokens |

---
*Generated from Claude API documentation changes detected on 2026-03-29*
