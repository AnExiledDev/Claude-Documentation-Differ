# Claude API Documentation Changes — 2026-03-27

## Summary

Three pages in the "about-claude" section were updated. The largest change (153 additions / 149 deletions) rewrites the Sonnet 4.6 extended-thinking migration guidance to treat adaptive thinking as the primary path rather than an optional alternative, and deprecates `budget_tokens` on Sonnet 4.6. A minor link fix was applied to the "What's new in Claude 4.6" page, and the pricing page was updated to acknowledge 1P data residency options instead of stating the Claude API is unaffected by regional pricing changes.

## Significant Changes

### Models — Migration Guide

- **Adaptive thinking is now the primary migration target for Sonnet 4.6**: The section previously framed adaptive thinking as an optional upgrade to consider after migrating. It now opens the Sonnet 4.6 extended-thinking section with adaptive thinking as the direct replacement for `budget_tokens`, and explicitly deprecates `budget_tokens` on Sonnet 4.6.
  > "If you're using extended thinking with `budget_tokens` on Sonnet 4.5, it is still functional on Sonnet 4.6 but is deprecated. Migrate to adaptive thinking with the effort parameter."
  - *Implication*: Developers migrating from Sonnet 4.5 who planned to keep `budget_tokens` should now plan for an additional migration step. The `budget_tokens` path continues to work but is explicitly marked for removal in a future model release.
  - *Source*: [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **`interleaved-thinking-2025-05-14` beta header scope broadened**: The migration guide previously stated that removing this header applied to Opus 4.6 only, and that Sonnet 4.6 continued to support it with manual extended thinking. The updated text clarifies that adaptive thinking now automatically enables interleaved thinking on **both** Opus 4.6 and Sonnet 4.6, and that manual mode (using the beta header on Sonnet 4.6) is itself deprecated.
  > "Remove interleaved thinking beta header: Adaptive thinking automatically enables interleaved thinking on both Opus 4.6 and Sonnet 4.6. Remove `betas=[\"interleaved-thinking-2025-05-14\"]` from your requests. The header is still functional on Sonnet 4.6 with manual extended thinking, but manual mode is deprecated."
  - *Implication*: The Opus 4.6 migration checklist item previously read "(Opus 4.6 only; Sonnet 4.6 still supports it)". That qualifier is gone — the guidance now applies to both models.
  - *Source*: [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **Code examples updated from beta to GA SDK surface**: All Sonnet 4.6 adaptive thinking code examples were updated to use `client.messages.create` (GA) instead of `client.beta.messages.create`, with `thinking: {type: "adaptive"}` and `max_tokens: 64000` instead of the beta `budget_tokens: 16384` form. SDK-specific changes include:
  - C#: imports moved from `Anthropic.Models.Beta.Messages` to `Anthropic.Models.Messages`; `BetaThinkingConfigEnabled` replaced by `ThinkingConfigAdaptive`; `client.Beta.Messages.Create` replaced by `client.Messages.Create`
  - Go: `client.Beta.Messages.New` replaced by `client.Messages.New`; `BetaThinkingConfigParamOfEnabled` replaced by `ThinkingConfigParamUnion{OfAdaptive: ...}`
  - Java: imports changed from `com.anthropic.models.beta.messages` to `com.anthropic.models.messages`; `BetaThinkingConfigEnabled` replaced by `ThinkingConfigAdaptive`
  - PHP/Ruby: switched from `$client->beta->messages` to `$client->messages`
  - *Implication*: Developers copying code samples will now get GA-surface code that does not require beta headers.
  - *Source*: [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **"Keeping budget_tokens during migration" section added**: A new sub-section explicitly describes the temporary path for developers who cannot immediately migrate away from `budget_tokens`. It recommends a 16k token budget as a reasonable cap and labels this configuration deprecated.
  > "If you need to keep `budget_tokens` temporarily while migrating, a budget around 16k tokens provides headroom for harder problems without risk of runaway token usage. This configuration is deprecated and will be removed in a future model release."
  - *Implication*: The `budget_tokens`-based "chat and non-coding" examples (`effort: "low"`, `max_tokens: 8192`) are now presented under this deprecated path. The recommended effort for the deprecated coding example changed from `low` to `medium`, and `max_tokens` was raised from `8192` to `16384`.
  - *Source*: [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **Sonnet 4.6 migration checklist updated**: The final checklist item changed from a general suggestion to an explicit deprecation notice.
  > "**Recommended:** Migrate from `thinking: {type: \"enabled\", budget_tokens: N}` to `thinking: {type: \"adaptive\"}` with the effort parameter (`budget_tokens` is deprecated and will be removed in a future release)"
  - *Implication*: This makes the migration checklist actionable with a concrete API change rather than a vague recommendation.
  - *Source*: [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

### Models — What's New in Claude 4.6

- **Broken link corrected for "Tool use examples"**: The link target was updated from a non-existent anchor (`implement-tool-use#providing-tool-use-examples`) to the correct page (`define-tools#providing-tool-use-examples`).
  > Previously: `[Tool use examples](/docs/en/agents-and-tools/tool-use/implement-tool-use#providing-tool-use-examples)`
  > Now: `[Tool use examples](/docs/en/agents-and-tools/tool-use/define-tools#providing-tool-use-examples)`
  - *Implication*: The link now resolves correctly. No content change.
  - *Source*: [What's new in Claude 4.6](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6.md)

### Pricing

- **1P data residency options acknowledged**: The statement that the Claude API (1P) is "unaffected" by regional endpoint pricing was replaced with a pointer to the data residency pricing section.
  > Previously: "The Claude API (1P) is global by default and unaffected by this change. The Claude API is global-only (equivalent to the global endpoint offering and pricing from other providers)."
  > Now: "The Claude API (1P) is global by default; for 1P data residency options and pricing, see [Data residency pricing](#data-residency-pricing) below."
  - *Implication*: The prior text implied no regional pricing option existed for the 1P API. The update aligns with the `inference_geo` parameter and the 1.1x data residency multiplier documented elsewhere on the same page.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

## Migration Guidance

**Sonnet 4.6 — `budget_tokens` is now deprecated**: Developers using `thinking: {type: "enabled", budget_tokens: N}` on Sonnet 4.6 should migrate to `thinking: {type: "adaptive"}` combined with the `effort` parameter. The `budget_tokens` path remains functional but will be removed in a future model release. Use the GA SDK surface (`client.messages.create`) rather than the beta surface (`client.beta.messages.create`) when using adaptive thinking.

**Sonnet 4.6 — interleaved thinking beta header deprecated**: Remove `betas=["interleaved-thinking-2025-05-14"]` from Sonnet 4.6 requests that use adaptive thinking. The header is still functional for `thinking: {type: "enabled"}` (the deprecated path) but is no longer needed with adaptive mode.

## Notable Details

- The adaptive thinking section was restructured: previously it appeared as an optional sidebar ("When to try adaptive thinking") after the `budget_tokens` examples. Now it appears first, as the recommended path, with `budget_tokens` moved into a sub-section labeled "Keeping budget_tokens during migration."
- The note about fallback behavior was inverted: previously it said "If you see inconsistent behavior or quality regressions with adaptive thinking, switch to extended thinking with `budget_tokens`." The new note says to try lowering the effort setting or using `max_tokens` as a hard limit first, and notes `budget_tokens` is still functional but deprecated and no longer recommended.
- PHP example output changed from `echo $message;` to `echo $message->content[0]->text;` in the adaptive thinking (GA) example — the reverse change appears in the deprecated `budget_tokens` example.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/about-claude/models/migration-guide.md` | Modified | +153 / -149 | Restructured Sonnet 4.6 thinking migration: adaptive thinking is now primary path; `budget_tokens` deprecated; interleaved thinking header deprecated on both models; code examples moved to GA SDK surface |
| `docs/api/en/about-claude/models/whats-new-claude-4-6.md` | Modified | +1 / -1 | Fixed broken link for "Tool use examples" (`implement-tool-use` → `define-tools`) |
| `docs/api/en/about-claude/pricing.md` | Modified | +1 / -1 | Updated 1P API regional pricing note to point to data residency pricing section instead of stating API is unaffected |
