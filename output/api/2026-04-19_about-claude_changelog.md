# Claude API Documentation Changes — 2026-04-19

## Summary

Two pages were updated with minor link corrections reflecting a structural change to AWS Bedrock documentation. Claude Opus 4.7 on AWS Bedrock has graduated from research preview to a production Messages-API endpoint, and the pricing page now distinguishes between the new and legacy Bedrock integration paths.

## Significant Changes

### Models

- **Claude Opus 4.7 on AWS Bedrock — Research Preview Removed**: Footnote 3 in the models overview was updated to remove the "research preview" designation and point to the new production Bedrock integration page.
  > Before: *"Claude Opus 4.7 on AWS is available through [Claude in Amazon Bedrock] …, currently in research preview."*
  >
  > After: *"Claude Opus 4.7 on AWS is available through [Claude in Amazon Bedrock] (the Messages-API Bedrock endpoint)."*
  - *Implication*: Opus 4.7 is now considered generally available on Bedrock via the Messages-API endpoint. The research preview URL (`claude-in-amazon-bedrock-research-preview`) has been replaced with the production path (`claude-in-amazon-bedrock`).
  - *Source*: [Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

### Pricing

- **AWS Bedrock Regional Pricing — Two Integration Paths Documented**: The pricing note on regional/global endpoint premiums now distinguishes between the new and legacy Bedrock integrations.
  > Before: *"[AWS Bedrock global vs regional endpoints](/docs/en/build-with-claude/claude-on-amazon-bedrock#global-vs-regional-endpoints)"*
  >
  > After: *"[AWS Bedrock global vs regional endpoints](/docs/en/build-with-claude/claude-in-amazon-bedrock#regions) for Opus 4.7, Haiku 4.5, and newer models, or [the legacy integration](/docs/en/build-with-claude/claude-on-amazon-bedrock#global-vs-regional-endpoints) for all other models on Bedrock"*
  - *Implication*: Developers using Opus 4.7 or Haiku 4.5 on Bedrock should use the new `claude-in-amazon-bedrock` integration for regional endpoint configuration. Older models continue to use the legacy `claude-on-amazon-bedrock` path.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

- **AWS Bedrock link in Third-Party Pricing section updated**: The inline link under "Third-party platform pricing" was corrected from the legacy `claude-on-amazon-bedrock` path to the new `claude-in-amazon-bedrock` path.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

## Notable Details

- The Bedrock integration split (`claude-in-amazon-bedrock` vs. `claude-on-amazon-bedrock`) signals a dual-path architecture on AWS: a newer Messages-API endpoint used by Opus 4.7 and Haiku 4.5+, and a legacy endpoint covering earlier models. Developers integrating newer models should reference the new endpoint docs, particularly for regional pricing and endpoint selection.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `about-claude/models/overview.md` | Modified | +1/-1 | Opus 4.7 Bedrock footnote updated: research preview removed, link updated to production endpoint |
| `about-claude/pricing.md` | Modified | +2/-2 | AWS Bedrock links updated to distinguish new vs. legacy integration paths |

---
*Generated from Claude API documentation changes detected on 2026-04-19*
