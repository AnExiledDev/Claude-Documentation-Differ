# Claude API Documentation Changes — 2026-03-03

## Summary

Five pages in the "About Claude" section received minor editorial edits. All changes are wording and punctuation corrections with no substantive impact on API behavior, model capabilities, or developer-facing guidance. No new pages were added and no pages were removed.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| [migration-guide.md](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md) | Modified | +2 / -2 | Section heading renamed from "Need help?" to "Get help"; one punctuation fix |
| [whats-new-claude-4-6.md](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6.md) | Modified | +1 / -1 | Minor phrasing correction in adaptive thinking description |
| [customer-support-chat.md](https://platform.claude.com/docs/en/about-claude/use-case-guides/customer-support-chat.md) | Modified | +24 / -24 | Punctuation normalization (bold label colons) and first-person-plural removal throughout |
| [legal-summarization.md](https://platform.claude.com/docs/en/about-claude/use-case-guides/legal-summarization.md) | Modified | +10 / -10 | First-person-plural removal and minor phrasing fixes |
| [ticket-routing.md](https://platform.claude.com/docs/en/about-claude/use-case-guides/ticket-routing.md) | Modified | +4 / -4 | Minor verb tense and phrasing fixes |

## Notable Details

- **Section heading rename in migration guide**: The final section of the model migration guide was renamed from `## Need help?` to `## Get help`. The linked resources and content beneath it are unchanged. Developers who anchor-link directly to `#need-help` will need to update those links to `#get-help`.

- **Punctuation normalization across use-case guides**: Bold labels in the customer support chat guide that previously used `**Label**:` (colon outside bold) were updated to `**Label:**` (colon inside bold). This is a formatting consistency fix only.

- **First-person plural removal**: Phrases like "our example," "we will," "we decided," and "our implementation" were replaced with neutral phrasing ("the example," "start with," "the code outputs," "this implementation") across the customer support, legal summarization, and ticket routing guides. This is a documentation style standardization.

- **Adaptive thinking phrasing fix** in `whats-new-claude-4-6.md`: "Claude will almost always think" was changed to "Claude almost always thinks." No change to the described behavior or the deprecation status of `thinking: {type: "enabled"}` and `budget_tokens`.
