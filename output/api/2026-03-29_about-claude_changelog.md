# Claude API Documentation Changes — 2026-03-29

## Summary

Two pages were updated in the "About Claude" section. The `whats-new-claude-4-6.md` page expanded the scope of the `thinking: {type: "enabled"}` deprecation to explicitly include Sonnet 4.6 alongside Opus 4.6, and updated guidance on the `interleaved-thinking-2025-05-14` beta header for Sonnet 4.6. The `pricing.md` page received a set of minor formatting corrections, changing colon placement inside bold list labels from `**Label**:` to `**Label:**`.

## Significant Changes

### Models

- **Deprecation scope expanded to Sonnet 4.6**: The `thinking: {type: "enabled", budget_tokens: N}` deprecation notice, previously stated for Opus 4.6 only, now explicitly covers Sonnet 4.6 as well, and links to the feature availability reference page.
  > `thinking: {type: "enabled", budget_tokens: N}` is [**deprecated**](/docs/en/build-with-claude/overview#feature-availability) on Opus 4.6 and Sonnet 4.6. It is still functional but no longer recommended and will be removed in a future model release. Migrate to `thinking: {type: "adaptive"}` with the [effort parameter](/docs/en/build-with-claude/effort).
  - *Implication*: Developers using `budget_tokens` on Sonnet 4.6 should now plan migration to `thinking: {type: "adaptive"}` — previously the page only flagged Opus 4.6.
  - *Source*: [What's new in Claude 4.6](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6.md)

- **Interleaved thinking guidance clarified for Sonnet 4.6**: The previous note stating Sonnet 4.6 "continues to support" the `interleaved-thinking-2025-05-14` beta header alongside `thinking: {type: "enabled"}` as an equal option has been replaced with language that explicitly marks manual mode as deprecated on Sonnet 4.6.
  > On **Sonnet 4.6**, the `interleaved-thinking-2025-05-14` beta header is still functional for use with manual extended thinking (`thinking: {type: "enabled"}`), but manual mode is deprecated. Adaptive thinking is the recommended path and automatically enables interleaved thinking.
  - *Implication*: Sonnet 4.6 users relying on the beta header with manual extended thinking should migrate to adaptive thinking; the header is still accepted but the underlying mode it enables (`type: "enabled"`) is now deprecated.
  - *Source*: [What's new in Claude 4.6](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6.md)

## Notable Details

- **Pricing page formatting corrections**: Multiple bold list-item labels in `pricing.md` were updated from `**Label**:` (colon outside bold span) to `**Label:**` (colon inside bold span). Affected sections include the third-party platform regional endpoint note, cost optimization strategies, rate limits tier list, and billing summary. These are purely cosmetic and carry no semantic change.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

- **Billing phrasing simplified**: Two billing bullet points were reworded for brevity:
  - "Billing is calculated monthly based on actual usage" → "Billing is based on actual monthly usage"
  - "Payments are processed in USD" → "All payments are in USD"
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/about-claude/models/whats-new-claude-4-6.md` | Modified | +2 / -2 | Extended `budget_tokens` deprecation to Sonnet 4.6; updated interleaved thinking guidance for Sonnet 4.6 |
| `docs/api/en/about-claude/pricing.md` | Modified | +14 / -14 | Formatting fixes (colon placement in bold labels); minor billing phrasing simplifications |
