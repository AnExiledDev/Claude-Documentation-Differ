# Claude API Documentation Changes — 2026-02-19

## Summary

This update adds a Claude Sonnet 4.6 System Card entry to the Resources overview page and applies a uniform wording normalization ("our developer Console" → "the developer Console") across all 63 prompt library pages. No API parameters, endpoints, or SDK behavior changed.

## Significant Changes

### Models

- **Claude Sonnet 4.6 System Card added to Resources overview**: A new card linking to the official Claude Sonnet 4.6 system card has been added to the Model Cards section of the Resources overview, alongside the existing Claude Opus 4.6 entry.
  > `<Card title="Claude Sonnet 4.6 System Card" icon="file" href="https://www.anthropic.com/claude-sonnet-4-6-system-card">Detailed documentation of Claude Sonnet 4.6.</Card>`
  - *Implication*: The system card for Claude Sonnet 4.6 is now accessible directly from the developer platform's Resources page at [anthropic.com/claude-sonnet-4-6-system-card](https://www.anthropic.com/claude-sonnet-4-6-system-card).
  - *Source*: [Resources Overview](https://platform.claude.com/docs/en/resources/overview.md)

## Notable Details

- **Prompt library wording normalization**: All 63 prompt library pages changed "Copy this prompt into **our** developer [Console](/dashboard)" to "Copy this prompt into **the** developer [Console](/dashboard)". This is a style/voice change only — no functional or structural content was altered.
- **Quickstarts card copy update**: The Quickstarts card on the Resources overview changed from "Deployable applications built with **our** API." to "Deployable applications built with **the** API." — same editorial direction as the prompt library change.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `resources/overview.md` | Modified | +5 / -1 | Added Claude Sonnet 4.6 System Card; minor wording update in Quickstarts card |
| `resources/prompt-library/cite-your-sources.md` | Modified | +2 / -2 | Wording normalization ("our" → "the") in two locations |
| 62 other `resources/prompt-library/*.md` files | Modified | +1 / -1 each | Uniform wording normalization: "our developer Console" → "the developer Console" |

---
*Generated from Claude API documentation changes detected on 2026-02-19*
