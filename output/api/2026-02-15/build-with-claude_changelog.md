# Claude API Documentation Changes — 2026-02-15

## Summary
This update focuses on editorial improvements and organizational changes to the "Build with Claude" documentation. The most significant change is a restructuring of the features overview page with new categorical sections to better organize capabilities. Minor wording refinements improve clarity throughout documentation on adaptive thinking, extended thinking, prompt caching, and error recovery for streaming.

## Significant Changes

### Documentation Organization

- **Features Overview Restructure**: The overview page now organizes features into six distinct categories instead of the previous two-section layout
  > New sections: "Model capabilities", "Server-side tools", "Client-side tools", "Tool infrastructure", "Context management", and "Files & assets"
  - *Implication*: Developers can more easily navigate and understand the relationship between different Claude capabilities
  - *Source*: [Features overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

### Streaming Error Recovery

- **Claude Opus 4.6 Error Recovery Change**: Error recovery behavior differs for Opus 4.6 compared to earlier models
  > "For Claude Opus 4.6, you should add a user message that instructs the model to continue from where it left off. For example: `Your previous response was interrupted and ended with [previous_response]. Continue from where you left off.`"
  - *Implication*: When recovering from interrupted streaming requests on Opus 4.6, developers must explicitly instruct the model to continue rather than relying on the previous approach of providing a partial assistant response
  - *Source*: [Streaming](https://platform.claude.com/docs/en/build-with-claude/streaming.md)

## Notable Details

### Terminology Standardization

Multiple pages received consistent wording updates replacing abbreviations with full forms:
- "e.g." → "for example" (in embeddings.md, compaction.md, extended-thinking.md, prompt-caching.md)
- "i.e." → "that is" (in context-windows.md, prompt-caching.md)

### Code Block Language Tags

Several code blocks received explicit language annotations for better syntax highlighting:
- Plain text blocks now marked as `text` (adaptive-thinking.md, compaction.md, embeddings.md, extended-thinking.md, prompt-caching.md, prompt-templates-and-variables.md)
- XML examples marked as `xml` (context-windows.md)

### Adaptive Thinking Wording

Minor rephrasing in adaptive-thinking.md changes "decide" to "determine" for consistency:
- "Claude decides when and how much to think" → "Claude determines when and how much to use extended thinking"

### Prompt Caching Language

Wording updates improve clarity in prompt-caching.md:
- Recommendation language shifted from "we recommend" to directive form
- Example: "we recommend moving to adaptive thinking" → "Move to adaptive thinking"

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| overview.md | Modified | +44/-17 | Restructured into six categorical sections |
| extended-thinking.md | Modified | +11/-11 | Code block annotations and terminology standardization |
| prompt-caching.md | Modified | +7/-7 | Terminology standardization (e.g./i.e.) |
| adaptive-thinking.md | Modified | +7/-7 | Wording refinements and code block annotations |
| streaming.md | Modified | +6/-1 | Added Opus 4.6-specific error recovery guidance |
| embeddings.md | Modified | +4/-4 | Terminology standardization and directive language |
| context-windows.md | Modified | +3/-3 | XML code block annotation and terminology |
| compaction.md | Modified | +2/-2 | Terminology standardization |
| prompt-templates-and-variables.md | Modified | +1/-1 | Code block annotation |

---
*Generated from Claude API documentation changes detected on 2026-02-15*
