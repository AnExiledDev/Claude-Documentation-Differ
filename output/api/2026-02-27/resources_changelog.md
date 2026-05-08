# Claude API Documentation Changes — 2026-02-27

## Summary

All 63 modified pages are confined to the prompt library under `resources/prompt-library/`. The changes are purely cosmetic code formatting adjustments in TypeScript code examples — no API parameters, model names, system prompt content, or functional documentation changed.

## Notable Details

- **TypeScript code formatting sweep**: Two mechanical reformatting changes were applied across all affected prompt library pages:

  1. Long `system:` property values in TypeScript `messages.create()` calls were reformatted from inline assignment to a line-broken style:

     Before:
     ```typescript
     system: "Your task is to analyze the provided text...",
     ```
     After:
     ```typescript
     system:
       "Your task is to analyze the provided text...",
     ```

  2. Trailing blank lines after `console.log(msg);` within TypeScript code blocks were removed, bringing the closing triple-backtick directly after the last statement.

- **Quote style normalization** (subset of pages): In TypeScript examples where the string literal contained double-quote characters, the surrounding quotes were changed from escaped double quotes to single quotes. For example, in `adaptive-editor.md`:

  Before: `text: "...Canis is the Latin word meaning \"dog\"..."`

  After: `text: '...Canis is the Latin word meaning "dog"...'`

  This affects `adaptive-editor.md` and a small number of other pages with embedded quotes in user message strings.

- No Python, AWS Bedrock Python, or Vertex AI Python code blocks were modified in substance. The TypeScript-only scope of these changes is consistent across all 63 pages.

- No model IDs, `max_tokens`, `temperature`, `system` prompt text, or API endpoint references changed.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| [adaptive-editor.md](https://platform.claude.com/docs/en/resources/prompt-library/adaptive-editor.md) | modified | +3 / -6 | TS formatting: quote style change + trailing blank line removal (3 blocks) |
| [airport-code-analyst.md](https://platform.claude.com/docs/en/resources/prompt-library/airport-code-analyst.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [alien-anthropologist.md](https://platform.claude.com/docs/en/resources/prompt-library/alien-anthropologist.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [alliteration-alchemist.md](https://platform.claude.com/docs/en/resources/prompt-library/alliteration-alchemist.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [babels-broadcasts.md](https://platform.claude.com/docs/en/resources/prompt-library/babels-broadcasts.md) | modified | +0 / -3 | TS formatting: trailing blank line removal only (3 blocks) |
| [brand-builder.md](https://platform.claude.com/docs/en/resources/prompt-library/brand-builder.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [career-coach.md](https://platform.claude.com/docs/en/resources/prompt-library/career-coach.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [cite-your-sources.md](https://platform.claude.com/docs/en/resources/prompt-library/cite-your-sources.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [code-clarifier.md](https://platform.claude.com/docs/en/resources/prompt-library/code-clarifier.md) | modified | +9 / -9 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [code-consultant.md](https://platform.claude.com/docs/en/resources/prompt-library/code-consultant.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [corporate-clairvoyant.md](https://platform.claude.com/docs/en/resources/prompt-library/corporate-clairvoyant.md) | modified | +0 / -3 | TS formatting: trailing blank line removal only (3 blocks) |
| [csv-converter.md](https://platform.claude.com/docs/en/resources/prompt-library/csv-converter.md) | modified | +9 / -9 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [culinary-creator.md](https://platform.claude.com/docs/en/resources/prompt-library/culinary-creator.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [data-organizer.md](https://platform.claude.com/docs/en/resources/prompt-library/data-organizer.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [direction-decoder.md](https://platform.claude.com/docs/en/resources/prompt-library/direction-decoder.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [dream-interpreter.md](https://platform.claude.com/docs/en/resources/prompt-library/dream-interpreter.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [efficiency-estimator.md](https://platform.claude.com/docs/en/resources/prompt-library/efficiency-estimator.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [email-extractor.md](https://platform.claude.com/docs/en/resources/prompt-library/email-extractor.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [emoji-encoder.md](https://platform.claude.com/docs/en/resources/prompt-library/emoji-encoder.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [ethical-dilemma-navigator.md](https://platform.claude.com/docs/en/resources/prompt-library/ethical-dilemma-navigator.md) | modified | +6 / -5 | TS formatting: system string line-wrap + trailing blank line removal |
| [excel-formula-expert.md](https://platform.claude.com/docs/en/resources/prompt-library/excel-formula-expert.md) | modified | +10 / -14 | TS formatting: system string line-wrap + quote style change |
| [function-fabricator.md](https://platform.claude.com/docs/en/resources/prompt-library/function-fabricator.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [futuristic-fashion-advisor.md](https://platform.claude.com/docs/en/resources/prompt-library/futuristic-fashion-advisor.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [git-gud.md](https://platform.claude.com/docs/en/resources/prompt-library/git-gud.md) | modified | +0 / -3 | TS formatting: trailing blank line removal only (3 blocks) |
| [google-apps-scripter.md](https://platform.claude.com/docs/en/resources/prompt-library/google-apps-scripter.md) | modified | +0 / -3 | TS formatting: trailing blank line removal only (3 blocks) |
| [grading-guru.md](https://platform.claude.com/docs/en/resources/prompt-library/grading-guru.md) | modified | +0 / -3 | TS formatting: trailing blank line removal only (3 blocks) |
| [grammar-genie.md](https://platform.claude.com/docs/en/resources/prompt-library/grammar-genie.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [hal-the-humorous-helper.md](https://platform.claude.com/docs/en/resources/prompt-library/hal-the-humorous-helper.md) | modified | +6 / -5 | TS formatting: system string line-wrap + trailing blank line removal |
| [idiom-illuminator.md](https://platform.claude.com/docs/en/resources/prompt-library/idiom-illuminator.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [interview-question-crafter.md](https://platform.claude.com/docs/en/resources/prompt-library/interview-question-crafter.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [latex-legend.md](https://platform.claude.com/docs/en/resources/prompt-library/latex-legend.md) | modified | +9 / -9 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [lesson-planner.md](https://platform.claude.com/docs/en/resources/prompt-library/lesson-planner.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [master-moderator.md](https://platform.claude.com/docs/en/resources/prompt-library/master-moderator.md) | modified | +0 / -3 | TS formatting: trailing blank line removal only (3 blocks) |
| [meeting-scribe.md](https://platform.claude.com/docs/en/resources/prompt-library/meeting-scribe.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [memo-maestro.md](https://platform.claude.com/docs/en/resources/prompt-library/memo-maestro.md) | modified | +9 / -9 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [mindfulness-mentor.md](https://platform.claude.com/docs/en/resources/prompt-library/mindfulness-mentor.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [mood-colorizer.md](https://platform.claude.com/docs/en/resources/prompt-library/mood-colorizer.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [motivational-muse.md](https://platform.claude.com/docs/en/resources/prompt-library/motivational-muse.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [neologism-creator.md](https://platform.claude.com/docs/en/resources/prompt-library/neologism-creator.md) | modified | +0 / -3 | TS formatting: trailing blank line removal only (3 blocks) |
| [perspectives-ponderer.md](https://platform.claude.com/docs/en/resources/prompt-library/perspectives-ponderer.md) | modified | +0 / -3 | TS formatting: trailing blank line removal only (3 blocks) |
| [philosophical-musings.md](https://platform.claude.com/docs/en/resources/prompt-library/philosophical-musings.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [pii-purifier.md](https://platform.claude.com/docs/en/resources/prompt-library/pii-purifier.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [polyglot-superpowers.md](https://platform.claude.com/docs/en/resources/prompt-library/polyglot-superpowers.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [portmanteau-poet.md](https://platform.claude.com/docs/en/resources/prompt-library/portmanteau-poet.md) | modified | +9 / -12 | TS formatting: system string line-wrap + trailing blank line removal |
| [product-naming-pro.md](https://platform.claude.com/docs/en/resources/prompt-library/product-naming-pro.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [prose-polisher.md](https://platform.claude.com/docs/en/resources/prompt-library/prose-polisher.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [pun-dit.md](https://platform.claude.com/docs/en/resources/prompt-library/pun-dit.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [python-bug-buster.md](https://platform.claude.com/docs/en/resources/prompt-library/python-bug-buster.md) | modified | +9 / -6 | TS formatting: system string line-wrap + user text string reformatting |
| [review-classifier.md](https://platform.claude.com/docs/en/resources/prompt-library/review-classifier.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [riddle-me-this.md](https://platform.claude.com/docs/en/resources/prompt-library/riddle-me-this.md) | modified | +0 / -3 | TS formatting: trailing blank line removal only (3 blocks) |
| [sci-fi-scenario-simulator.md](https://platform.claude.com/docs/en/resources/prompt-library/sci-fi-scenario-simulator.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [second-grade-simplifier.md](https://platform.claude.com/docs/en/resources/prompt-library/second-grade-simplifier.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [simile-savant.md](https://platform.claude.com/docs/en/resources/prompt-library/simile-savant.md) | modified | +0 / -3 | TS formatting: trailing blank line removal only (3 blocks) |
| [socratic-sage.md](https://platform.claude.com/docs/en/resources/prompt-library/socratic-sage.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [spreadsheet-sorcerer.md](https://platform.claude.com/docs/en/resources/prompt-library/spreadsheet-sorcerer.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [sql-sorcerer.md](https://platform.claude.com/docs/en/resources/prompt-library/sql-sorcerer.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [storytelling-sidekick.md](https://platform.claude.com/docs/en/resources/prompt-library/storytelling-sidekick.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [time-travel-consultant.md](https://platform.claude.com/docs/en/resources/prompt-library/time-travel-consultant.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [tongue-twister.md](https://platform.claude.com/docs/en/resources/prompt-library/tongue-twister.md) | modified | +0 / -3 | TS formatting: trailing blank line removal only (3 blocks) |
| [trivia-generator.md](https://platform.claude.com/docs/en/resources/prompt-library/trivia-generator.md) | modified | +0 / -3 | TS formatting: trailing blank line removal only (3 blocks) |
| [tweet-tone-detector.md](https://platform.claude.com/docs/en/resources/prompt-library/tweet-tone-detector.md) | modified | +6 / -6 | TS formatting: system string line-wrap + trailing blank line removal (3 blocks) |
| [vr-fitness-innovator.md](https://platform.claude.com/docs/en/resources/prompt-library/vr-fitness-innovator.md) | modified | +0 / -3 | TS formatting: trailing blank line removal only (3 blocks) |
| [website-wizard.md](https://platform.claude.com/docs/en/resources/prompt-library/website-wizard.md) | modified | +9 / -10 | TS formatting: system string line-wrap + trailing blank line removal |

---
*Generated from Claude API documentation changes detected on 2026-02-27*
