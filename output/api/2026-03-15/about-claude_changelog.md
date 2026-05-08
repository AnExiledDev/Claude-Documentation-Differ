# Claude API Documentation Changes — 2026-03-15

## Summary

Four pages in the models and pricing documentation were updated. The most significant change is that Claude Opus 4.6 and Sonnet 4.6 now include the full 1M token context window at standard pricing — the beta requirement and long context premium pricing surcharge have been removed for these models. Accompanying changes update the models overview table and what's-new page to reflect this promotion from beta to GA. A cosmetic normalization also converts token count notations from uppercase "K" to lowercase "k" throughout (e.g., `200K` → `200k`).

---

## Significant Changes

### Models — Context Window & Pricing

- **1M token context window is now standard (non-beta) for Claude Opus 4.6 and Sonnet 4.6**: Both models have had their 1M context window promoted from beta to GA and are now listed with 1M tokens as their default context window. The `context-1m-2025-08-07` beta header is no longer needed for these models.

  > Claude Opus 4.6 and Sonnet 4.6 both support a [1M token context window](/docs/en/build-with-claude/context-windows), extended thinking, and all existing Claude API features.

  - *Implication*: Developers using Opus 4.6 or Sonnet 4.6 no longer need to include the `context-1m-2025-08-07` beta header to access 1M context.
  - *Source*: [What's New — Claude 4.6](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6.md)

- **Long context premium pricing removed for Opus 4.6 and Sonnet 4.6**: These two models are no longer subject to elevated per-token pricing above 200K tokens. Previously, input tokens beyond 200K were charged at $10/MTok (Opus 4.6) or $6/MTok (Sonnet 4.6/4.5/4). The updated pricing page states requests of any size are billed at standard rates.

  > Claude Opus 4.6 and Sonnet 4.6 include the full [1M token context window](/docs/en/build-with-claude/context-windows) at standard pricing. (A 900k-token request is billed at the same per-token rate as a 9k-token request.) Prompt caching and batch processing discounts apply at standard rates across the full context window.

  - *Implication*: Long context workloads on Opus 4.6 and Sonnet 4.6 are now cheaper — no per-token surcharge kicks in above 200K. The 1.1x data residency multiplier is also no longer listed as stacking on top of long context pricing for these models.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

- **Long context beta and premium pricing retained only for Sonnet 4.5 and Sonnet 4**: These older models still require the `context-1m-2025-08-07` beta header and are charged at elevated rates above 200K tokens ($6/$22.50 input/output per MTok). The pricing table has been updated to show only these models in the long context pricing section.

  > For Claude Sonnet 4.5 and Sonnet 4, the 1M token context window is in beta for organizations in [usage tier](/docs/en/api/rate-limits) 4 and organizations with custom rate limits. When the `context-1m-2025-08-07` beta header is included, requests that exceed 200k input tokens are automatically charged at premium long context rates.

  - *Implication*: Developers on Sonnet 4.5 or Sonnet 4 still face the old 200K pricing tier boundary; consider upgrading to Sonnet 4.6 for flat-rate 1M context.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

- **Models overview table updated to reflect 1M as default for Opus/Sonnet 4.6**: The comparison table for current models now lists Opus 4.6 and Sonnet 4.6 with a context window of 1M tokens (no longer `200K / 1M (beta)`). Haiku 4.5 remains at 200K. The footnote explaining the 1M beta requirement for Opus 4.6 and Sonnet 4.6 has been removed.

  > `| **Context window** | 1M tokens | 1M tokens | 200k tokens |`

  The legacy models footnote was also updated to clarify which older models have 200K-only vs. optional 1M context:

  > Claude Opus 4.5, Opus 4.1, Opus 4, Haiku 4.5, and earlier models have a 200k-token context window. Claude Sonnet 4.5 and Sonnet 4 default to 200k but can access a [1M-token context window](/docs/en/build-with-claude/context-windows) by including the `context-1m-2025-08-07` beta header.

  - *Source*: [Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

---

## Notable Details

- **Token count notation normalization**: All token count references across the four modified pages have been changed from uppercase "K" to lowercase "k" (e.g., `200K` → `200k`, `128K` → `128k`, `64K` → `64k`). This is a cosmetic consistency fix with no functional impact.
- **Data residency pricing stack removed**: The bullet noting that the 1.1x data residency multiplier stacks on top of long context pricing was removed from the long context pricing section in `pricing.md`. It is unclear whether this was an intentional policy change or a documentation simplification.
- **Migration guide updated**: The migration guide's reference to "increased output capacity (64K tokens)" was updated to "64k tokens", consistent with the broader notation change.
  - *Source*: [Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `pricing.md` | Modified | +14 / -20 | Removed long context premium pricing for Opus/Sonnet 4.6; limited beta 1M pricing to Sonnet 4.5/4; removed data residency long context stacking note |
| `overview.md` | Modified | +5 / -7 | Updated context window column to show 1M as default for Opus/Sonnet 4.6; removed beta footnote for those models; clarified legacy model footnote |
| `whats-new-claude-4-6.md` | Modified | +3 / -5 | Consolidated context window description; removed beta qualifier for 1M context; section heading casing fix (`128K` → `128k`) |
| `migration-guide.md` | Modified | +1 / -1 | Capitalization fix: `64K` → `64k` |

---

*Generated from Claude API documentation changes detected on 2026-03-15*
