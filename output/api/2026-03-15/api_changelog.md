# Claude API Documentation Changes — 2026-03-15

## Summary

Three API documentation pages were updated. The most significant change is to the rate limits page, which gains a new section on spend limit management and removes the "Long context rate limits" section (previously a beta feature tied to the `context-1m-2025-08-07` header). Priority Tier capacity burndown multipliers in the service tiers docs were also narrowed to specific model versions.

---

## Significant Changes

### Rate Limits

- **New "Increasing your spend limits" section**: Documentation now distinguishes between two kinds of spend limits: a customer-controlled limit (adjustable via **Settings > Limits > Change Limit** in the Console) and a tier-enforced ceiling. Guidance is provided for each.

  > Your organization has two kinds of spend limits: a customer-set limit you control directly, and a tier-enforced ceiling set by your usage tier. Each has a different process for increasing it.

  > When you need a limit higher than your tier's ceiling (Tier 4's ceiling is $200,000 per month), click **Contact Sales** on the Limits page.

  > Monthly Invoicing removes the monthly spend cap entirely and uses Net-30 payment terms by default.

  - *Implication*: Developers and teams seeking to raise spend limits above Tier 4's $200,000/month ceiling now have explicit documentation on the path (Contact Sales → email follow-up → tier upgrade, or Monthly Invoicing for uncapped access).
  - *Source*: [Rate Limits](https://platform.claude.com/docs/en/api/rate-limits.md)

- **"Long context rate limits" section removed**: The dedicated rate limit table for long-context requests (>200K tokens) using the `context-1m-2025-08-07` beta header has been removed from the rate limits page. This section previously documented Tier 4 limits of 1,000,000 ITPM / 200,000 OTPM for Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5, and Sonnet 4.

  - *Implication*: The separate long-context rate limit tier appears to have been retired or folded into standard limits. Developers relying on the `context-1m-2025-08-07` beta header for 1M token context should verify current behavior against their current tier limits.
  - *Source*: [Rate Limits](https://platform.claude.com/docs/en/api/rate-limits.md)

### Service Tiers — Priority Tier Capacity Burndown

- **Long-context multipliers scoped to specific models**: The 2× input / 1.5× output token burndown for long-context requests (>200K input tokens) is now explicitly limited to **Claude Sonnet 4.5 and Sonnet 4**. Previously, the rule applied to all models.

  > For [long-context](/docs/en/build-with-claude/context-windows) (>200k input tokens) requests on Claude Sonnet 4.5 and Sonnet 4, input tokens are 2 tokens per token

  > For [long-context](/docs/en/build-with-claude/context-windows) (>200k input tokens) requests on Claude Sonnet 4.5 and Sonnet 4, output tokens are 1.5 tokens per token

  - *Implication*: Long-context requests on Claude Opus 4.6 and newer models no longer carry the 2× / 1.5× Priority Tier surcharge. This reduces the effective cost of long-context usage for those models under Priority Tier.
  - *Source*: [Service Tiers](https://platform.claude.com/docs/en/api/service-tiers.md)

- **US-only inference multiplier scoped to Opus 4.6 and newer**: The 1.1× input/output burndown for `inference_geo: "us"` requests is now explicitly limited to **Claude Opus 4.6 and newer models**. Previously, the rule was stated without a model restriction.

  > For [US-only inference](/docs/en/build-with-claude/data-residency) (`inference_geo: "us"`) requests on Claude Opus 4.6 and newer models, input tokens are 1.1 tokens per token

  - *Implication*: The stacking multiplier note has been updated accordingly — the combination of long-context + US-only inference now applies per-model rather than universally. Developers should re-check their Priority Tier capacity math if they use `inference_geo: "us"` with older models.
  - *Source*: [Service Tiers](https://platform.claude.com/docs/en/api/service-tiers.md)

### API Overview

- **Third-party platform request size limits documented**: A new note clarifies that Vertex AI and Amazon Bedrock impose their own, lower request size limits beyond Anthropic's own API limits.

  > Third-party platforms have their own request size limits: Vertex AI limits requests to 30 MB, and Amazon Bedrock limits requests to 20 MB. Consult your platform's documentation for current values.

  - *Implication*: Developers using Claude through Vertex AI or Amazon Bedrock who are close to request size limits should account for the tighter platform-specific caps (30 MB and 20 MB respectively) rather than the Anthropic API ceiling.
  - *Source*: [API Overview](https://platform.claude.com/docs/en/api/overview.md)

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/api/rate-limits.md` | Modified | +35 / -32 | Added spend limit management guidance; removed long context rate limits section |
| `docs/api/en/api/service-tiers.md` | Modified | +5 / -5 | Scoped long-context and US-only inference Priority Tier multipliers to specific model versions |
| `docs/api/en/api/overview.md` | Modified | +4 / -0 | Added note on Vertex AI (30 MB) and Amazon Bedrock (20 MB) request size limits |

---

*Generated from Claude API documentation changes detected on 2026-03-15*
