# Claude API Documentation Changes — 2026-03-21

## Summary

Five pages in the `about-claude` section received minor wording updates. The most notable changes are: Fast mode's status label was updated from "research preview" to "beta: research preview" across four pages, and the definition of the **Deprecated** model lifecycle stage was reworded to remove the prior claim that deprecated models are unavailable for new customers.

## Significant Changes

### Models

- **Fast mode status relabeled to "beta: research preview"**: The label for Fast mode on Claude Opus 4.6 has been updated from `(research preview)` to `(beta: research preview)` across the What's New, Choosing a Model, and Pricing pages.
  > `### Fast mode (beta: research preview)`
  > `[Fast mode](/docs/en/build-with-claude/fast-mode) (beta: research preview) for Claude Opus 4.6 provides significantly faster output at premium pricing (6x standard rates).`
  - *Implication*: This signals Fast mode has advanced from a pure research preview into a beta stage, suggesting broader availability or increased stability, though it remains early-access. No pricing or behavioral changes were made.
  - *Source*: [What's New — Claude 4.6](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6.md), [Choosing a Model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model.md), [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

### Model Lifecycle

- **"Deprecated" definition revised**: The description of the Deprecated lifecycle stage has been rewritten to remove the previous statement that deprecated models are "no longer available for new customers."
  > Old: `The model is no longer available for new customers but continues to be available for existing users until retirement. Anthropic assigns a retirement date at this point.`
  > New: `The model is still functional but no longer recommended. Anthropic provides a recommended replacement and assigns a retirement date.`
  - *Implication*: The revised wording no longer restricts deprecated models to existing users only — they are described as "still functional." Developers should not rely solely on this definition to determine API availability; always check the specific model's retirement date and recommended replacement listed on the deprecations page.
  - *Source*: [Model Deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations.md)

### MCP Connector

- **"Public beta" simplified to "beta"**: The glossary entry for the MCP connector removed the word "public" from its beta status description, and updated the phrasing from "our [MCP connector documentation]" to "the [MCP connector documentation]."
  > Old: `...is available in public beta.`
  > New: `...is available in beta.`
  - *Implication*: Minor editorial cleanup; no functional change to the MCP connector itself.
  - *Source*: [Glossary](https://platform.claude.com/docs/en/about-claude/glossary.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| about-claude/models/whats-new-claude-4-6.md | Modified | +1/-1 | Fast mode section heading updated to "beta: research preview" |
| about-claude/pricing.md | Modified | +1/-1 | Fast mode pricing description updated to "beta: research preview" |
| about-claude/models/choosing-a-model.md | Modified | +1/-1 | Fast mode reference updated to "beta: research preview" |
| about-claude/model-deprecations.md | Modified | +1/-1 | "Deprecated" lifecycle definition reworded |
| about-claude/glossary.md | Modified | +1/-1 | MCP connector status changed from "public beta" to "beta" |

---
*Generated from Claude API documentation changes detected on 2026-03-21*
