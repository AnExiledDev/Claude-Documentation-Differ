# Claude API Documentation Changes — 2026-04-21

## Summary

Claude Haiku 3 (`claude-3-haiku-20240307`) was retired on April 20, 2026. All API requests to this model now return an error. Documentation across model listings, rate limits, platform availability pages, migration guides, and use-case examples has been updated to reflect the retirement and redirect developers to Claude Haiku 4.5.

## Significant Changes

### Models

- **Claude Haiku 3 Retired**: The model status for `claude-3-haiku-20240307` has changed from `Deprecated` to `Retired` effective April 20, 2026. Requests to this model ID now return an error.
  > "We've retired the Claude Haiku 3 model (`claude-3-haiku-20240307`). All requests to this model will now return an error. We recommend upgrading to [Claude Haiku 4.5](/docs/en/about-claude/models/overview#latest-models-comparison)."
  - *Implication*: Any code still referencing `claude-3-haiku-20240307` will fail at runtime. Migrate to `claude-haiku-4-5-20251001`.
  - *Source*: [Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

- **Haiku 3 removed from available models table**: `claude-3-haiku-20240307` has been dropped from the "Available Models" comparison table in the models overview. The table previously listed it alongside Claude Opus 4.6, Sonnet 4.5, Opus 4.5, Opus 4.1, Sonnet 4, and Opus 4; it no longer appears.
  - *Implication*: Developers consulting the overview to discover available model IDs will no longer see Haiku 3 as an option.
  - *Source*: [Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

- **Model deprecations page updated**: The deprecation history entry for Haiku 3 now includes a retirement notice callout, and the model status column reflects `Retired`.
  > "This model was retired April 20, 2026."
  - *Source*: [Model Deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations.md)

### Rate Limits

- **Haiku 3 removed from rate limits tables**: Claude Haiku 3 rows have been removed from all four usage-tier rate limit tables (Free, Build, Scale, and Enterprise tiers). Haiku 3 previously shared limits with Haiku 3.5 (50k–400k TPM depending on tier).
  - *Implication*: Developers no longer need to account for separate Haiku 3 rate limit entries when planning capacity.
  - *Source*: [Rate Limits](https://platform.claude.com/docs/en/api/rate-limits.md)

### Platform Availability

- **Amazon Bedrock**: The Haiku 3 row (`anthropic.claude-3-haiku-20240307-v1:0`) has been removed from the Bedrock model availability table. It was previously listed as deprecated with a retirement date of April 19, 2026.
  - *Source*: [Claude on Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md)

- **Google Vertex AI**: The Haiku 3 entry (`claude-3-haiku@20240307`) has been removed from the Vertex AI model availability table.
  - *Source*: [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

### Prompt Caching

- **Haiku 3 removed from minimum token thresholds**: The prompt caching minimum cacheable token length documentation previously stated "2048 tokens for Claude Haiku 3.5 and Claude Haiku 3." The reference to Haiku 3 has been dropped.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

### Migration Guide

- **"From Haiku 3" migration section removed**: The migration guide previously contained a dedicated code block showing the rename from `claude-3-haiku-20240307` to `claude-haiku-4-5-20251001`. That section has been removed now that the model is retired. The rate limits note has been updated from "Haiku 3.5 and Haiku 3" to just "Haiku 3.5."
  - *Source*: [Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

### Use-Case Guides

- **Content moderation guide updated to Haiku 4.5**: All four code examples in the content moderation guide that previously used `claude-3-haiku-20240307` now reference `claude-haiku-4-5-20251001`. Cost estimates have been updated to reflect Haiku 4.5 pricing ($1.00/$5.00 per MTok input/output vs. the previous $0.25/$1.25 per MTok).
  > "Claude Haiku 4.5 estimated cost: Input token cost: 2,860 MTok * $1.00/MTok = $2,860 / Output token cost: 1,500 MTok * $5.00/MTok = $7,500 / Monthly cost: $2,860 + $7,500 = $10,360"
  - *Implication*: The example monthly cost for moderating 1B posts has risen from ~$2,590 to ~$10,360 — a 4× increase — reflecting the Haiku 4.5 price point.
  - *Source*: [Content Moderation](https://platform.claude.com/docs/en/about-claude/use-case-guides/content-moderation.md)

- **Legal summarization guide updated to Haiku 4.5**: Cost comparison table updated from Haiku 3 ($21.96 for 1,000 documents) to Haiku 4.5 ($87.75) using the new $1.00/$5.00 per MTok pricing.
  - *Source*: [Legal Summarization](https://platform.claude.com/docs/en/about-claude/use-case-guides/legal-summarization.md)

## Migration Guidance

- **Stop using `claude-3-haiku-20240307`**: This model is now retired. All requests will return an error. Migrate to `claude-haiku-4-5-20251001` (API alias: `claude-haiku-4-5`).

  ```python
  # Before (will now error)
  model = "claude-3-haiku-20240307"

  # After
  model = "claude-haiku-4-5-20251001"
  ```

  Note that Haiku 4.5 pricing is $1.00/$5.00 per MTok (input/output), compared to Haiku 3's $0.25/$1.25 per MTok — approximately 4× higher. Review cost estimates accordingly.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| release-notes/overview.md | Modified | +3/-0 | Added April 20, 2026 entry for Haiku 3 retirement |
| about-claude/models/overview.md | Modified | +14/-18 | Removed Haiku 3 column from available models table |
| about-claude/model-deprecations.md | Modified | +5/-1 | Updated Haiku 3 status to Retired; added retirement note callout |
| about-claude/use-case-guides/content-moderation.md | Modified | +9/-9 | Replaced Haiku 3 with Haiku 4.5 in examples and cost estimates |
| about-claude/use-case-guides/legal-summarization.md | Modified | +4/-4 | Replaced Haiku 3 with Haiku 4.5 in cost estimates |
| api/rate-limits.md | Modified | +0/-4 | Removed Haiku 3 from all rate limit tier tables |
| about-claude/models/migration-guide.md | Modified | +1/-5 | Removed "From Haiku 3" migration section |
| build-with-claude/claude-on-amazon-bedrock.md | Modified | +0/-1 | Removed Haiku 3 from Bedrock model availability table |
| build-with-claude/claude-on-vertex-ai.md | Modified | +0/-1 | Removed Haiku 3 from Vertex AI model availability table |
| build-with-claude/prompt-caching.md | Modified | +1/-1 | Removed Haiku 3 from minimum cacheable token length list |

---
*Generated from Claude API documentation changes detected on 2026-04-21*
