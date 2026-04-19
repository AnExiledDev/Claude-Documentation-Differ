# Claude API Documentation Changes — 2026-04-19

## Summary

One minor documentation update was made today: the Managed Agents quickstart guide gained a tip callout directing developers to an interactive onboarding command in Claude Code. No API, SDK, or behavioral changes were made.

## Notable Details

- **Interactive onboarding tip added to Managed Agents quickstart**: A `<Tip>` callout was inserted near the top of the quickstart guide, before the "Core concepts" section:

  > **Prefer an interactive walkthrough?** Run `/claude-api managed-agents-onboard` in the latest version of [Claude Code](https://claude.com/product/claude-code) for a guided setup and interactive question-answering.

  - *Implication*: Developers new to Managed Agents can now use the Claude Code skill `claude-api` to get a guided, in-editor onboarding experience rather than following the static docs. This is the first reference to a managed-agents-specific onboarding command in the quickstart.
  - *Source*: [Managed Agents Quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| managed-agents/quickstart.md | Modified | +4 / -0 | Added `<Tip>` callout for interactive Claude Code onboarding |

---
*Generated from Claude API documentation changes detected on 2026-04-19*
