# Claude API Documentation Changes — 2026-03-15

## Summary

Four documentation pages were modified with no new or removed pages. The primary change is the addition of a March 13, 2026 release note entry documenting that the 1M token context window reached general availability for Claude Opus 4.6 and Sonnet 4.6, along with associated rate limit and media limit changes. The remaining three page edits are minor (2–3 lines each).

## Significant Changes

### Context Window & Limits

- **1M Token Context Window Now GA for Opus 4.6 and Sonnet 4.6**: The 1M token context window is generally available at standard pricing for these two models, with no beta header required. Requests over 200k tokens work automatically. The feature remains in beta for Claude Sonnet 4.5 and Sonnet 4.
  > "The 1M token context window is now generally available for Claude Opus 4.6 and Sonnet 4.6 at standard pricing. Requests over 200k tokens work automatically for these models with no beta header required. The 1M token context window remains in beta for Claude Sonnet 4.5 and Sonnet 4."
  - *Implication*: Developers using Opus 4.6 or Sonnet 4.6 can drop any `anthropic-beta` header previously required for 1M context requests. No code changes needed — requests over 200k tokens will automatically route to the extended context window.
  - *Source*: [Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

- **Dedicated 1M Rate Limits Removed**: Anthropic has removed the separate rate limit tier that previously applied to 1M-context requests. Standard account rate limits now apply uniformly across all context lengths.
  > "We've removed the dedicated 1M rate limits for all supported models. Your standard account limits now apply across every context length."
  - *Implication*: Developers no longer need to track or request separate quota for long-context workloads; however, high-volume long-context usage will now count directly against existing rate limits, which may require limit increase requests for heavily loaded applications.
  - *Source*: [Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

- **Media Limit Raised from 100 to 600 per Request**: When using the 1M token context window, the per-request limit for images and PDF pages has increased sixfold.
  > "We've raised the media limit from 100 to 600 images or PDF pages per request when using the 1M token context window."
  - *Implication*: Long-context document analysis workflows (e.g., large PDF corpora or multi-image tasks) can now include substantially more media without splitting requests.
  - *Source*: [Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

## Notable Details

- The `web-fetch-tool.md` and `tool-search-tool.md` pages each received minor edits (+3/−3 and +2/−2 lines respectively). Based on the diff magnitude, these are likely small wording or example code adjustments rather than API-visible behavior changes.
- The `reduce-hallucinations.md` page had a single-line change (+1/−1), consistent with a minor copy fix.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| release-notes/overview.md | Modified | +10/−5 | Added March 13, 2026 section: 1M context GA, rate limit removal, media limit increase |
| agents-and-tools/tool-use/web-fetch-tool.md | Modified | +3/−3 | Minor documentation update |
| agents-and-tools/tool-use/tool-search-tool.md | Modified | +2/−2 | Minor documentation update |
| test-and-evaluate/strengthen-guardrails/reduce-hallucinations.md | Modified | +1/−1 | Minor copy fix |

---
*Generated from Claude API documentation changes detected on 2026-03-15*
