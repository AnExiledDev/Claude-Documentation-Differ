# Claude API Documentation Changes — 2026-03-31

## Summary

One page was modified in this update. The service tiers documentation was updated to remove long-context token burndown rate rules that previously applied to Claude Sonnet 4.5 and Sonnet 4. The corresponding explanatory note was also simplified to remove the long-context reference.

## Significant Changes

### API — Service Tiers

- **Removed long-context Priority Tier burndown rates for Claude Sonnet 4.5 and Sonnet 4**: Two bullet points specifying elevated token burndown rates for requests exceeding 200k input tokens on Claude Sonnet 4.5 and Sonnet 4 were removed from the Priority Tier capacity counting rules. The removed rules stated that input tokens counted as 2 tokens per token and output tokens as 1.5 tokens per token for those long-context requests. These lines no longer appear under either the **Input Tokens** or **Output Tokens** sections.

  Previously included (now removed):
  > - For [long-context] (>200k input tokens) requests on Claude Sonnet 4.5 and Sonnet 4, input tokens are 2 tokens per token
  > - For [long-context] (>200k input tokens) requests on Claude Sonnet 4.5 and Sonnet 4, output tokens are 1.5 tokens per token

  - *Implication*: Developers using Claude Sonnet 4.5 or Sonnet 4 with long-context requests (>200k input tokens) should note that the documentation no longer distinguishes a higher burndown rate for those requests. Priority Tier capacity accounting for those models now follows the standard "all other tokens are 1 token per token" rule, unless the US-only inference multiplier applies.
  - *Source*: [Service Tiers](https://platform.claude.com/docs/en/api/service-tiers.md)

- **Simplified burndown rate explanatory note**: The `<Note>` block explaining burndown rates was shortened to remove the sentence that cited the Sonnet 4.5 / Sonnet 4 long-context example.

  Previous note (truncated portion removed):
  > For Claude Sonnet 4.5 and Sonnet 4, long-context requests (>200k input tokens) draw down input tokens at 2 tokens per token and output tokens at 1.5 tokens per token.

  - *Implication*: The note now only references the US-only inference example, consistent with the removal of the long-context rules above.
  - *Source*: [Service Tiers](https://platform.claude.com/docs/en/api/service-tiers.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/api/service-tiers.md` | Modified | +1 / -3 | Removed long-context (>200k token) Priority Tier burndown rate rules for Claude Sonnet 4.5 and Sonnet 4; simplified explanatory note |
