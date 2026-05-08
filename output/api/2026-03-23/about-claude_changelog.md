# Claude API Documentation Changes — 2026-03-23

## Summary

Four documentation pages were updated with minor formatting adjustments to code snippet display directives (`hidelines` parameters). One bullet point in the ticket-routing guide was slightly reworded. No API-visible changes, new parameters, or behavioral changes are present in this update.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| about-claude/models/migration-guide.md | Modified | +21/-21 | Adjusted `hidelines` ranges on Go, Java, PHP, Ruby, and TypeScript code examples across multiple sections |
| about-claude/use-case-guides/content-moderation.md | Modified | +4/-4 | Normalized `hidelines` ranges on four Python code examples |
| about-claude/use-case-guides/ticket-routing.md | Modified | +3/-3 | Adjusted `hidelines` on two Python examples; simplified one bullet point |
| about-claude/use-case-guides/legal-summarization.md | Modified | +2/-2 | Adjusted `hidelines` ranges on two Python code examples |

## Notable Details

- All changes affect `hidelines={...}` directives embedded in fenced code block metadata (e.g., ` ```go Go hidelines={1..13,-1}` → ` ```go Go hidelines={1..11,-1}`). These control which lines are collapsed/hidden in the documentation viewer and have no effect on the code itself.
- The ticket-routing guide removed the phrase "Imports the Anthropic library and" from a bullet point describing a code snippet, reflecting that the import statement is now hidden from view by the updated `hidelines` directive.
- Sources: [Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md) · [Content Moderation](https://platform.claude.com/docs/en/about-claude/use-case-guides/content-moderation.md) · [Legal Summarization](https://platform.claude.com/docs/en/about-claude/use-case-guides/legal-summarization.md) · [Ticket Routing](https://platform.claude.com/docs/en/about-claude/use-case-guides/ticket-routing.md)

---
*Generated from Claude API documentation changes detected on 2026-03-23*
