# Claude API Documentation Changes — 2026-03-31

## Summary

Three pages in the "About Claude" section were updated. The most substantive change is the addition of 300k output token support on the Message Batches API for Opus 4.6 and Sonnet 4.6 via a new beta header. The pricing page removed a large section covering legacy long context pricing for Sonnet 4.5 and Sonnet 4, and the models overview page removed documentation of the 1M-token context window option for those same models.

## Significant Changes

### Models

- **300k Output Tokens on Message Batches API**: Opus 4.6 and Sonnet 4.6 now support up to 300k output tokens when using the Message Batches API with the `output-300k-2026-03-24` beta header. This extends well beyond the 128k synchronous limit.
  > "On the Message Batches API, Opus 4.6 and Sonnet 4.6 can generate up to 300k output tokens by using the `output-300k-2026-03-24` beta header."
  - *Implication*: Developers running large batch jobs (e.g., long-form generation, extended thinking) can now request significantly more output per request in batch mode.
  - *Source*: [What's New in Claude 4.6](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6.md)

- **Section Renamed: "128k output tokens" → "Higher output token limits"**: The section heading in the Claude 4.6 release notes was broadened to reflect that output token limits now vary by API surface (128k synchronous, 300k batch), rather than advertising a single fixed limit.
  - *Implication*: The rename signals that the 128k limit is not the ceiling — batch users should consult the section for the full picture.
  - *Source*: [What's New in Claude 4.6](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6.md)

- **Models Overview — New Note on Batch Output Limits**: A callout was added to the models comparison table clarifying that the listed "Max output" values apply to the synchronous Messages API only.
  > "The Max output values above apply to the synchronous Messages API. On the Message Batches API, Opus 4.6 and Sonnet 4.6 support up to 300k output tokens by using the `output-300k-2026-03-24` beta header."
  - *Implication*: Prevents confusion for developers who see 64k/128k in the table but want to use batch for larger outputs.
  - *Source*: [Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

- **Legacy Models Table — 1M Context Window Option Removed for Sonnet 4.5 / Sonnet 4**: The legacy models comparison table previously showed Sonnet 4.5 and Sonnet 4 as supporting either a 200k or 1M context window (via the `context-1m-2025-08-07` beta header). The table now lists all legacy models uniformly at 200k tokens.
  - *Implication*: The 1M context window capability for Sonnet 4.5 and Sonnet 4 is no longer surfaced in the overview table. Developers relying on it should check the dedicated context window documentation.
  - *Source*: [Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

### Pricing

- **Long Context Pricing Section Removed for Sonnet 4.5 and Sonnet 4**: A 38-line section documenting premium long context pricing (input >200k tokens) for Claude Sonnet 4.5 and Sonnet 4 was removed. This included the pricing table, stacking rules, the `usage` object example for determining whether a request was billed at premium rates, and related notes.
  > "For Claude Sonnet 4.5 and Sonnet 4, the 1M token context window is in beta for organizations in usage tier 4 and organizations with custom rate limits. When the `context-1m-2025-08-07` beta header is included, requests that exceed 200k input tokens are automatically charged at premium long context rates"
  - *Implication*: Long context pricing details for these two models are no longer documented in the pricing page. This may reflect that the beta has changed or that pricing has been simplified for those models. Developers who were using the 1M context window on Sonnet 4.5/4 should verify current billing behavior.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

- **Prompt Caching Pricing Modifiers — "Long context pricing" Removed from Stacking List**: The sentence describing what pricing modifiers stack with prompt caching was updated.
  > Before: "These multipliers stack with other pricing modifiers, including the Batch API discount, long context pricing, and data residency."
  > After: "These multipliers stack with other pricing modifiers, including the Batch API discount and data residency."
  - *Implication*: Consistent with the removal of the long context pricing section above; long context pricing is no longer listed as a stacking modifier for prompt caching on Sonnet 4.5/4.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

## Notable Details

- The footnote numbering in the legacy models table was renumbered (superscripts `<sup>2</sup>` and `<sup>3</sup>` became `<sup>1</sup>` and `<sup>2</sup>`) after the footnote about the 1M context window beta was removed.
- The wording in the Claude 4.6 release notes for Opus 4.6 128k support was trimmed slightly: the phrase "doubling the previous 64k limit" was removed, leaving a more neutral statement about the capability.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `about-claude/models/overview.md` | Modified | +8 / -6 | Added batch 300k output note; removed 1M context window from legacy table; renumbered footnotes |
| `about-claude/models/whats-new-claude-4-6.md` | Modified | +4 / -2 | Renamed section to "Higher output token limits"; added 300k batch output documentation |
| `about-claude/pricing.md` | Modified | +1 / -39 | Removed long context pricing section for Sonnet 4.5/4; removed "long context pricing" from prompt caching stacking list |
