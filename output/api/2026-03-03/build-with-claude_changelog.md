# Claude API Documentation Changes — 2026-03-03

## Summary

25 pages in the `build-with-claude` section received documentation edits totaling 138 additions and 133 deletions. The changes are primarily stylistic: a broad pass converting bold inline labels from `**Label**:` format to `**Label:**` format, and removing future-tense constructions ("will return", "will be") in favor of present-tense equivalents ("returns", "is"). One substantive content addition was made to the Zero Data Retention page, adding the 1M Token Context Window to the list of ZDR-eligible features.

## Significant Changes

### Zero Data Retention

- **1M Token Context Window added to ZDR-eligible features**: The 1M token context window feature has been explicitly listed as Zero Data Retention eligible.
  > `| 1M Token Context Window | /v1/messages (with anthropic-beta: context-1m-2025-08-07) | Extended context processing uses the standard Messages API. ZDR applies even though this feature is in beta. |`
  - *Implication*: Organizations with ZDR arrangements can now confirm that 1M token context window requests do not store data after the API response is returned, even while the feature remains in beta.
  - *Source*: [Zero Data Retention](https://platform.claude.com/docs/en/build-with-claude/zero-data-retention.md)

### Context Windows

- **ZDR eligibility note added to 1M token context window section**: A new `<Note>` block was added to the 1M token context window documentation.
  > `This feature is Zero Data Retention (ZDR) eligible. When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.`
  - *Implication*: Developers using the 1M context window now have in-context confirmation that ZDR applies to this beta feature.
  - *Source*: [Context Windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md)

- **"Currently in beta" phrasing removed**: The phrase "currently in beta" was revised to simply "in beta" in the 1M token context window note.
  > Before: `The 1M token context window is currently in beta for organizations in usage tier 4...`
  > After: `The 1M token context window is in beta for organizations in usage tier 4...`
  - *Implication*: No behavioral change; editorial consistency.
  - *Source*: [Context Windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md)

- **"pdfs" capitalized to "PDFs"**: The multimodal considerations bullet now uses the correct capitalization.
  > After: `When processing large numbers of images or PDFs, be aware that the files can vary in token usage.`
  - *Source*: [Context Windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md)

### Effort Parameter

- **Section heading changed from question to declarative form**: The heading `## When should I adjust the effort parameter?` was renamed to `## When to adjust the effort parameter`.
  - *Implication*: No content change; heading style now matches the rest of the documentation.
  - *Source*: [Effort](https://platform.claude.com/docs/en/build-with-claude/effort.md)

- **`max` effort error language clarified**: The description of the `max` effort level now uses present tense consistently.
  > Before: `Requests using max on other models will return an error.`
  > After: `Requests using max on other models return an error.`
  - *Source*: [Effort](https://platform.claude.com/docs/en/build-with-claude/effort.md)

### Handling Stop Reasons

- **Section heading reworded to be declarative**: `## What is stop_reason?` was renamed to `## The stop_reason field`.
  - *Implication*: No content change; aligns with declarative heading conventions used elsewhere.
  - *Source*: [Handling Stop Reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons.md)

### Fast Mode

- **Attribution changed from first-person to third-party**: A note about feedback gathering was updated to remove first-person "we".
  > Before: `Availability is limited while we gather feedback.`
  > After: `Availability is limited while Anthropic gathers feedback.`
  - *Source*: [Fast Mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode.md)

### Extended Thinking (Documentation Typo Fix)

- **Typo "documention" corrected to "documentation"**: A link to the Streaming Messages page contained a misspelling.
  > Before: `For more documention on streaming via the Messages API...`
  > After: `For more documentation on streaming via the Messages API...`
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

### Prompt Engineering Best Practices

- **Recommendation language softened for adaptive thinking**: A recommendation to use adaptive thinking was changed from prescriptive to advisory.
  > Before: `...we recommend moving to adaptive thinking to get the most intelligent responses.`
  > After: `...Consider moving to adaptive thinking to get the most intelligent responses.`
  - *Implication*: The guidance is now framed as a suggestion rather than a direct recommendation.
  - *Source*: [Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

- **Vision performance guidance reattributed**: The description of the image crop technique was updated to use third-person attribution.
  > Before: `One technique we've found effective... We've seen consistent uplift... We've put together a cookbook...`
  > After: `One technique that has proven effective... Testing has shown consistent uplift... Anthropic has created a cookbook...`
  - *Source*: [Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

### Amazon Bedrock

- **Section heading capitalization normalized**: `### PDF Support on Bedrock` was changed to `### PDF support on Bedrock` (lowercase "support").
  - *Implication*: No content change.
  - *Source*: [Claude on Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md)

- **"Currently in beta" phrasing removed for 1M context window**: Updated to remove "currently" for editorial consistency.
  > Before: `The 1M token context window is currently in beta.`
  > After: `The 1M token context window is in beta.`
  - *Source*: [Claude on Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md)

### Google Vertex AI

- **Section heading capitalization normalized**: `### Model Availability` was changed to `### Model availability` (lowercase "availability").
  - *Implication*: No content change.
  - *Source*: [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

- **Grammar fix in introduction sentence**: Removed a duplicate "have" from the guide's prerequisite note.
  > Before: `Note that this guide assumes you have already have a GCP project...`
  > After: `Note that this guide assumes you already have a GCP project...`
  - *Source*: [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

- **Subject-verb agreement fix**: A code example description was corrected for subject-verb agreement.
  > Before: `The following examples shows how to generate text...`
  > After: `The following examples show how to generate text...`
  - *Source*: [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

### Structured Outputs

- **"Currently in public beta" shortened**: The Microsoft Foundry status note was trimmed.
  > Before: `Structured outputs remain in public beta on Microsoft Foundry.`
  > After: `Structured outputs are in public beta on Microsoft Foundry.`
  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **First request latency description clarified**: Passive construction replaced with active voice.
  > Before: `there will be additional latency while the grammar is compiled`
  > After: `there is additional latency while the grammar compiles`
  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

### Zero Data Retention — Minor Edit

- **Semicolon replaces comma in "Programmatic Tool Calling" note**: A minor punctuation correction in the Not ZDR-eligible table.
  > Before: `Built on code execution—uses sandbox containers that retain user data.`
  > After: `Built on code execution; uses sandbox containers that retain user data.`
  - *Source*: [Zero Data Retention](https://platform.claude.com/docs/en/build-with-claude/zero-data-retention.md)

## Notable Details

- **Beta feature language standardized**: Across multiple pages (compaction, context-editing, Files API, fast mode, structured outputs), the phrase "currently in beta" was shortened to simply "in beta." This appears to be an editorial decision to avoid implying these features may be leaving beta imminently. Affected pages: `compaction.md`, `context-editing.md`, `files.md`, `fast-mode.md`, `structured-outputs.md`.

- **Bold list item punctuation normalized**: Throughout many pages, bold terms in bullet lists used `**Label**:` (colon outside bold) and were changed to `**Label:**` (colon inside bold). This was a broad formatting pass affecting: `claude-in-microsoft-foundry.md`, `claude-on-amazon-bedrock.md`, `claude-on-vertex-ai.md`, `data-residency.md`, `effort.md`, `fast-mode.md`, `prompt-engineering/claude-prompting-best-practices.md`, `search-results.md`, `skills-guide.md`, `structured-outputs.md`.

- **Prompt caching FAQ updated**: Attribution of the cache improvement work changed from first-person to third-person.
  > Before: `We're considering ways to improve these cache hit rates...`
  > After: `Anthropic is considering ways to improve these cache hit rates...`
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| adaptive-thinking.md | Modified | +2 / -2 | Present-tense verb corrections in behavior descriptions |
| batch-processing.md | Modified | +4 / -4 | Present-tense verb corrections ("will be able" → "can", "will be" → "are") |
| citations.md | Modified | +4 / -4 | Present-tense verb corrections; removed "Please" from feedback tip |
| claude-in-microsoft-foundry.md | Modified | +24 / -24 | Bold label punctuation pass (`**Label**:` → `**Label:**`); present-tense corrections |
| claude-on-amazon-bedrock.md | Modified | +5 / -5 | Section heading case normalization; "currently in beta" → "in beta"; bold label punctuation |
| claude-on-vertex-ai.md | Modified | +6 / -6 | Section heading case normalization; grammar fixes; bold label punctuation |
| compaction.md | Modified | +1 / -1 | "currently in beta" → "in beta" |
| context-editing.md | Modified | +1 / -1 | "currently in beta" → "in beta" |
| context-windows.md | Modified | +8 / -4 | Added ZDR eligibility note for 1M context window; "currently in beta" → "in beta"; "pdfs" → "PDFs"; present-tense corrections |
| data-residency.md | Modified | +11 / -11 | Bold label punctuation pass throughout |
| effort.md | Modified | +9 / -9 | Section heading reworded; bold label punctuation pass; present-tense corrections |
| embeddings.md | Modified | +1 / -1 | Removed "Please" from FAQ answer |
| extended-thinking.md | Modified | +1 / -1 | Typo fix: "documention" → "documentation" |
| fast-mode.md | Modified | +6 / -6 | "currently in beta" → "in beta"; attribution change from "we" to "Anthropic"; bold label punctuation |
| files.md | Modified | +1 / -1 | "currently in beta" → "in beta"; removed "Please" from feedback note |
| handling-stop-reasons.md | Modified | +1 / -1 | Section heading renamed from question to declarative form |
| pdf-support.md | Modified | +2 / -2 | Removed "Please note" phrasing; bold label punctuation in note |
| prompt-caching.md | Modified | +1 / -1 | Attribution changed from "We're" to "Anthropic is" |
| prompt-engineering/claude-prompting-best-practices.md | Modified | +10 / -10 | Bold label punctuation pass; recommendation language softened; vision attribution updated |
| search-results.md | Modified | +8 / -8 | Present-tense corrections; bold label punctuation pass |
| skills-guide.md | Modified | +12 / -12 | Bold label punctuation pass; present-tense corrections |
| streaming.md | Modified | +3 / -3 | Present-tense verb corrections |
| structured-outputs.md | Modified | +9 / -9 | "currently in public beta" shortened; present-tense corrections; bold label punctuation |
| vision.md | Modified | +6 / -6 | Section heading case normalization; present-tense corrections ("will be" → "is/are") |
| zero-data-retention.md | Modified | +2 / -1 | Added 1M Token Context Window as ZDR-eligible; punctuation fix in table |
