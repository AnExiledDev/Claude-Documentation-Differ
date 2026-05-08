# Claude API Documentation Changes — 2026-03-21

## Summary

Twelve pages in the `build-with-claude` section were updated. The most substantive changes are: a new feature availability taxonomy on the overview page, a significant rewrite of the prompt caching cache-lookback explanation, new documentation for Amazon Bedrock's two PDF processing modes, and a re-labeling of fast mode from "research preview" to "beta: research preview". The Java SDK was bumped from `2.15.0` to `2.18.0` across all three platform integrations.

## Significant Changes

### Features Overview

- **New "Feature availability" section**: A formal classification table was added to the features overview page, defining how platform features are categorized throughout the documentation.
  > Features on the Claude Platform are assigned one of the following availability classifications per platform...
  > - **Beta**: Preview features used for gathering feedback and iterating on a less mature use case... Breaking changes are possible with notice...
  > - **Generally available (GA)**: Feature is stable, fully supported, and recommended for production use...
  > - **Deprecated**: Feature is still functional but no longer recommended. A migration path and removal timeline are provided.
  > - **Retired**: Feature is no longer available.
  - *Implication*: The table also introduces a qualifier syntax — "beta: research preview" — for features with tighter availability constraints, which aligns with the fast mode rename described below.
  - *Source*: [Features overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

### Fast Mode

- **"Fast mode" re-labeled to "beta: research preview"**: The page title and all cross-page references changed from `Fast mode (research preview)` to `Fast mode (beta: research preview)`, and the note text was updated accordingly.
  > Fast mode is in beta (research preview). Join the waitlist to request access. Availability is limited while Anthropic gathers feedback.
  - *Implication*: This is a labeling alignment with the newly formalized feature classification system, not a capability change. The `fast-mode-2026-02-01` beta header, pricing, and rate limit behavior are unchanged.
  - *Source*: [Fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode.md), [Usage and Cost API](https://platform.claude.com/docs/en/build-with-claude/usage-cost-api.md)

### Prompt Caching

- **Cache lookback mechanics rewritten for precision**: The explanation of how the system finds cache hits was substantially rewritten to clarify that the lookback finds *prior writes*, not stable content. A new "Common mistake" subsection was added.
  > Cache writes happen only at your breakpoint... The lookback does not find stable content behind your breakpoint and cache it. It finds entries that prior requests already wrote, and writes happen only at breakpoints.
  >
  > **Common mistake: Breakpoint on content that changes every request** — ...The timestamp differs, so the prefix hash at block 6 differs. The lookback walks through blocks 5, 4, 3, 2, and 1, but the system never wrote an entry at any of those positions. No cache hit. You pay for a fresh cache write on every request and never get a read.
  - *Implication*: The prior documentation described the lookback as checking "previous block boundaries" for matches; the new text makes explicit that only positions where prior requests placed a `cache_control` breakpoint can ever be cache hits. Developers who place breakpoints on per-request content (timestamps, user messages) should move them to the end of the stable prefix.
  - *Source*: [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

### PDF Support — Amazon Bedrock

- **Documented two distinct PDF processing modes on Bedrock's Converse API**: New sections explain that full visual PDF understanding on the Bedrock Converse API requires citations to be enabled; without it, the API falls back to text-only extraction.
  > **Important:** To access Claude's full visual PDF understanding capabilities in the Converse API, you must enable citations. Without citations enabled, the API falls back to basic text extraction only.
  >
  > 1. **Converse Document Chat** (Original mode - Text extraction only) — Uses approximately 1,000 tokens for a 3-page PDF. Automatically used when citations are not enabled.
  > 2. **Claude PDF Chat** (New mode - Full visual understanding) — Can understand and analyze charts, graphs, images, and visual layouts. Uses approximately 7,000 tokens for a 3-page PDF. **Requires citations to be enabled** in the Converse API.
  - *Implication*: Developers using Bedrock's Converse API who expect Claude to analyze images or charts in PDFs must explicitly enable citations. The InvokeModel API provides full visual PDF analysis without this requirement.
  - *Source*: [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support.md)

### SDKs

- **Java SDK bumped to `2.18.0`** across all three platform integrations:
  - `anthropic-java-bedrock`: `2.15.0` → `2.18.0`
  - `anthropic-java-vertex`: `2.15.0` → `2.18.0`
  - `anthropic-java-foundry`: `2.15.0` → `2.18.0`
  - *Implication*: Developers using Java on Bedrock, Vertex AI, or Microsoft Foundry should update their Gradle/Maven dependency version.
  - *Source*: [Claude on Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md), [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md), [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md)

## Notable Details

- **Structured outputs on Microsoft Foundry**: Changed from "in public beta" to "in beta". The word "public" was removed, aligning with the new unified Beta classification.
  - *Source*: [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **Extended thinking — Go code example fixed**: A bare `resp, _ := http.DefaultClient.Do(req)` call was replaced with proper error handling (`resp, err := ...; if err != nil { panic(err) }`). No API behavior change.
  - *Source*: [Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

- **Shell code examples made self-contained**: Several pages added `cd "$(mktemp -d)"` setup and file download steps at the top of shell examples, making them runnable without pre-existing local files. Affected pages: PDF support, vision, skills guide. Some shell examples in the skills guide were also marked `nocheck` to indicate they require contextual setup.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| prompt-caching.md | Modified | +24/-18 | Rewrote cache lookback explanation; added "common mistake" example |
| extended-thinking.md | Modified | +24/-21 | Minor wording (present tense); Go error handling fix; section renames |
| skills-guide.md | Modified | +16/-8 | Shell examples marked `nocheck`; one example made self-contained |
| overview.md | Modified | +13/-0 | New "Feature availability" classification table |
| pdf-support.md | Modified | +11/-4 | Amazon Bedrock Converse API PDF modes documented; shell examples updated |
| fast-mode.md | Modified | +2/-2 | Re-labeled as "beta: research preview" |
| claude-in-microsoft-foundry.md | Modified | +2/-2 | Java SDK `2.15.0` → `2.18.0` |
| claude-on-amazon-bedrock.md | Modified | +2/-2 | Java SDK `2.15.0` → `2.18.0` |
| claude-on-vertex-ai.md | Modified | +2/-2 | Java SDK `2.15.0` → `2.18.0` |
| usage-cost-api.md | Modified | +1/-1 | Fast mode section heading: "beta: research preview" |
| structured-outputs.md | Modified | +1/-1 | Foundry availability: "public beta" → "beta" |
| vision.md | Modified | +3/-1 | Files API shell example made self-contained |

---
*Generated from Claude API documentation changes detected on 2026-03-21*
