# Claude API Documentation Changes — 2026-04-25

## Summary

Two new release note entries were added covering the Rate Limits API launch (April 24) and the Managed Agents Memory feature reaching public beta (April 23). Ancillary documentation — the quickstart guide, intro page, and pricing page — was updated to reflect Claude Opus 4.7 as the current default model in examples and descriptions.

## Significant Changes

### API

- **Rate Limits API launched**: A new programmatic API endpoint allows organization administrators to query the rate limits configured for their organization and workspaces.
  > "We've released the [Rate Limits API](/docs/en/build-with-claude/rate-limits-api), allowing administrators to programmatically query the rate limits configured for their organization and workspaces."
  - *Implication*: Teams can now automate rate limit monitoring and build tooling that dynamically adjusts request rates based on current configured limits, without manual Console inspection.
  - *Source*: [Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

### Managed Agents

- **Memory for Claude Managed Agents in public beta**: The Memory feature for Managed Agents has graduated from limited access to public beta. No new beta header is required — it is now covered under the existing `managed-agents-2026-04-01` header.
  > "**Memory** for Claude Managed Agents is now in public beta under the standard `managed-agents-2026-04-01` header. See [Using agent memory](/docs/en/managed-agents/memory) for the full integration guide."
  - *Implication*: All users with Managed Agents access can now enable persistent memory for agent sessions without requesting separate access. The integration guide is available at `/docs/en/managed-agents/memory`.
  - *Source*: [Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

### Models

- **Claude Opus 4.7 promoted to default in documentation examples**: The quickstart guide, intro page, and pricing page were each updated with one-line model-name changes to reference `claude-opus-4-7` instead of `claude-opus-4-6` in code examples and the featured model description.
  - *Implication*: New developers following the quickstart will use Opus 4.7 out of the box. Note that Opus 4.7 uses a new tokenizer (up to 35% more tokens for the same text) and includes API breaking changes versus 4.6; review the [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide) before upgrading.
  - *Source*: [Get Started](https://platform.claude.com/docs/en/get-started.md), [Intro](https://platform.claude.com/docs/en/intro.md), [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| release-notes/overview.md | Modified | +6/-0 | Added April 24 (Rate Limits API) and April 23 (Managed Agents Memory beta) entries |
| get-started.md | Modified | +2/-2 | Updated model in quickstart code examples to `claude-opus-4-7` |
| intro.md | Modified | +1/-1 | Updated featured model description to Claude Opus 4.7 |
| about-claude/pricing.md | Modified | +1/-1 | Updated data residency pricing note to include Claude Opus 4.7 |

---
*Generated from Claude API documentation changes detected on 2026-04-25*
