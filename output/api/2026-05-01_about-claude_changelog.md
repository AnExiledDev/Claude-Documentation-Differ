# Claude API Documentation Changes — 2026-05-01

## Summary

One line was removed from the Claude Managed Agents pricing documentation. The "Long context premium" row has been dropped from the table of Messages API modifiers that do not apply to Claude Managed Agents sessions, implying that long context pricing may now apply to those sessions.

## Significant Changes

### Pricing — Claude Managed Agents

- **Long context premium exclusion removed for Managed Agents**: The pricing page previously listed the long context premium as a modifier that does *not* apply to Claude Managed Agents sessions, with the rationale that "Context window is managed by the runtime." That row has been deleted.

  > ~~`| [Long context premium](#long-context-pricing) | Context window is managed by the runtime. |`~~

  The remaining non-applicable modifiers are now: Batch API discount, Fast mode premium, Data residency multiplier, and Third-party platform pricing.

  - *Implication*: Developers using Claude Managed Agents with large context windows should review the [long context premium pricing](https://platform.claude.com/docs/en/about-claude/pricing.md#long-context-pricing) to understand whether and how it now affects their session costs.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| about-claude/pricing.md | Modified | +0/-1 | Removed "Long context premium" from Managed Agents non-applicable modifiers table |

---
*Generated from Claude API documentation changes detected on 2026-05-01*
