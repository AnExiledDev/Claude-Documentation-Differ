# Claude API Documentation Changes — 2026-02-25

## Summary

One documentation page was updated with two internal link fixes. Both links now point to anchor sections within a consolidated `claude-prompting-best-practices` page, indicating that previously separate prompt engineering guides (`system-prompts` and `chain-prompts`) have been merged into a single reference page.

## Notable Details

- **Prompt engineering docs consolidation**: Two internal links in the customer support chat guide were updated to reflect restructured documentation. The standalone pages for system prompts and chain prompts appear to have been merged into a unified `claude-prompting-best-practices` page with named anchors:
  - `/docs/en/build-with-claude/prompt-engineering/system-prompts` → `/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role`
  - `/docs/en/build-with-claude/prompt-engineering/chain-prompts` → `/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#chain-complex-prompts`
  - *Implication*: Developers following links from the customer support guide will now land at the correct anchored sections of the consolidated best practices page. No API behavior changed.
  - *Source*: [Customer Support Chat Guide](https://platform.claude.com/docs/en/about-claude/use-case-guides/customer-support-chat.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `about-claude/use-case-guides/customer-support-chat.md` | Modified | +2/-2 | Updated two internal prompt engineering links to point to consolidated best practices page |

---
*Generated from Claude API documentation changes detected on 2026-02-25*
