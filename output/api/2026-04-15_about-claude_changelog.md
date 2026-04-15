# Claude API Documentation Changes — 2026-04-15

## Summary

Anthropic deprecated `claude-sonnet-4-20250514` and `claude-opus-4-20250514` on April 14, 2026, with a retirement date of June 15, 2026. Documentation across the model deprecations page, models overview, migration guide, and pricing page has been updated to reflect this status change. Recommended replacements are `claude-sonnet-4-6` and `claude-opus-4-6`.

## Significant Changes

### Model Deprecations

- **Claude Sonnet 4 and Claude Opus 4 (original releases) deprecated**: `claude-sonnet-4-20250514` and `claude-opus-4-20250514` have moved from Active to Deprecated status, effective April 14, 2026. Both will be retired on June 15, 2026.

  > On April 14, 2026, Anthropic notified developers using Claude Sonnet 4 and Claude Opus 4 models of their upcoming retirement on the Claude API.
  >
  > | Retirement Date | Deprecated Model | Recommended Replacement |
  > |:----------------|:-----------------|:------------------------|
  > | June 15, 2026 | `claude-sonnet-4-20250514` | `claude-sonnet-4-6` |
  > | June 15, 2026 | `claude-opus-4-20250514` | `claude-opus-4-6` |

  - *Implication*: Developers using these model IDs directly must migrate to `claude-sonnet-4-6` or `claude-opus-4-6` before June 15, 2026. Callers using the alias forms (`claude-sonnet-4-0`, `claude-opus-4-0`) should verify their alias routing.
  - *Source*: [Model Deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations.md)

- **Models overview warning updated**: The legacy models comparison table now labels Claude Sonnet 4 and Claude Opus 4 as "(deprecated)", and the warning callout has been expanded to include both models alongside the existing Claude Haiku 3 deprecation notice.

  > Claude Sonnet 4 (`claude-sonnet-4-20250514`) and Claude Opus 4 (`claude-opus-4-20250514`) are deprecated and will be retired on June 15, 2026. Migrate to Claude Sonnet 4.6 and Claude Opus 4.6 respectively before the retirement date.

  - *Implication*: Developers scanning the models overview page will now see a prominent warning. Claude Haiku 3 retirement (April 19, 2026) is also still prominently displayed.
  - *Source*: [Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

- **Migration guide updated**: The migration path description for moving from "Claude 4.1 or earlier to Claude 4.6" now explicitly labels Sonnet 4 as deprecated in the text.

  > If you're migrating from Opus 4.1, Sonnet 4 (deprecated), or earlier models directly to Claude 4.6...

  - *Implication*: No behavior change — purely a documentation clarification to guide developers to the correct migration path.
  - *Source*: [Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **Pricing page updated**: The scope note for the tiered pricing structure (introduced with Claude Sonnet 4.5 and Haiku 4.5) now labels the earlier models as deprecated.

  > Earlier models (Claude Sonnet 4 (deprecated), Opus 4 (deprecated), and prior releases) retain their existing pricing.

  - *Implication*: No pricing changes — the labeling update clarifies that these models continue on legacy pricing until retirement.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

## Migration Guidance

- **Migrate off `claude-sonnet-4-20250514` by June 15, 2026**: Replace with `claude-sonnet-4-6`.
- **Migrate off `claude-opus-4-20250514` by June 15, 2026**: Replace with `claude-opus-4-6`.
- **Migrate off `claude-3-haiku-20240307` by April 19, 2026**: Replace with `claude-haiku-4-5` (separate, earlier deadline).

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| model-deprecations.md | Modified | +11/-2 | Added deprecation entry for claude-sonnet-4-20250514 and claude-opus-4-20250514; updated status to Deprecated with June 15, 2026 retirement |
| models/overview.md | Modified | +6/-2 | Added "(deprecated)" labels to Sonnet 4 and Opus 4 in comparison table; expanded warning callout |
| models/migration-guide.md | Modified | +1/-1 | Added "(deprecated)" qualifier to Sonnet 4 reference in migration path text |
| pricing.md | Modified | +1/-1 | Added "(deprecated)" labels to Sonnet 4 and Opus 4 in pricing scope note |

---
*Generated from Claude API documentation changes detected on 2026-04-15*
