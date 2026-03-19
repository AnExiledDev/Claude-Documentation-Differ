# Claude API Documentation Changes — 2026-03-19

## Summary

One documentation page was modified with 4 lines added and no deletions. The change adds a tip to the models overview page directing developers to the Models API for programmatic querying of model capabilities and token limits.

## Significant Changes

### Models

- **New tip: Query model capabilities via the Models API**: A callout was added to the models overview page noting that developers can programmatically retrieve model capabilities and token limits using the Models API.
  > You can query model capabilities and token limits programmatically with the [Models API](/docs/en/api/models/list). The response includes `max_input_tokens`, `max_tokens`, and a `capabilities` object for every available model.
  - *Implication*: Developers can now be explicitly pointed to the `GET /v1/models` endpoint to dynamically inspect per-model limits and capabilities rather than hardcoding values from the docs. The mention of a `capabilities` object warrants attention for those building model-agnostic logic.
  - *Source*: [Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| about-claude/models/overview.md | Modified | +4/-0 | Added tip callout pointing to Models API for programmatic capability/token-limit queries |

---
*Generated from Claude API documentation changes detected on 2026-03-19*
