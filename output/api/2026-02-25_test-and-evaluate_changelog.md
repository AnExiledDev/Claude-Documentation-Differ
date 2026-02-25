# Claude API Documentation Changes — 2026-02-25

## Summary

Four pages in the "Test and Evaluate" section received minor link updates. All changes involve redirecting internal cross-references from old individual prompt engineering pages to a consolidated `claude-prompting-best-practices` page or the updated `prompting-tools` page. No content, examples, or behavioral guidance changed.

## Significant Changes

### Documentation Links / Internal Navigation

- **Prompt Generator Link Update (eval-tool)**: The link to the prompt generator was updated from the old `/prompt-engineering/prompt-generator` path to `/prompt-engineering/prompting-tools`.
  > The Console offers a built-in [prompt generator](/docs/en/build-with-claude/prompt-engineering/prompting-tools) powered by Claude Opus 4.1
  - *Implication*: Developers following the link from the Evaluation tool page will now land on the consolidated prompting tools page rather than the previous standalone prompt generator page.
  - *Source*: [eval-tool.md](https://platform.claude.com/docs/en/test-and-evaluate/eval-tool.md)

- **System Prompts Link Consolidation (increase-consistency)**: The link under "Use system prompts to set the role" was updated from `/prompt-engineering/system-prompts` to `/prompt-engineering/claude-prompting-best-practices#give-claude-a-role`.
  > Use [system prompts](/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role) to define Claude's role and personality.
  - *Implication*: The cross-reference now points directly to the relevant anchor within the consolidated best practices page instead of a dedicated system prompts page.
  - *Source*: [increase-consistency.md](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency.md)

- **"Be Clear and Direct" Links Consolidated (reduce-latency)**: Two links referencing `/prompt-engineering/be-clear-and-direct` were updated to `/prompt-engineering/claude-prompting-best-practices#be-clear-and-direct`. This affects both the "Be clear but concise" bullet and the "Ask for shorter responses" bullet.
  > [claude lacks context](/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#be-clear-and-direct) on your use case
  > ask Claude to [curb its chattiness](/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#be-clear-and-direct)
  - *Implication*: Both latency-reduction tips now link to anchored sections of the unified best practices page rather than a standalone page.
  - *Source*: [reduce-latency.md](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency.md)

- **System Prompts Link Consolidation (reduce-prompt-leak)**: The link referencing the most effective way to use system prompts was updated from `/prompt-engineering/system-prompts` to `/prompt-engineering/claude-prompting-best-practices#give-claude-a-role`.
  > Notice that this system prompt is still predominantly a role prompt, which is the [most effective way to use system prompts](/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role).
  - *Implication*: Cross-reference now points to the anchor section on role prompting within the consolidated best practices page.
  - *Source*: [reduce-prompt-leak.md](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-prompt-leak.md)

## Notable Details

All four changes are purely navigational — links that previously pointed to standalone prompt engineering topic pages (`/system-prompts`, `/be-clear-and-direct`, `/prompt-generator`) have been redirected to sections within a unified `claude-prompting-best-practices` page. This reflects an ongoing consolidation of the prompt engineering documentation structure. No new guidance, warnings, or code examples were added or removed.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| [eval-tool.md](https://platform.claude.com/docs/en/test-and-evaluate/eval-tool.md) | Modified | +1 / -1 | Prompt generator link updated to `/prompting-tools` |
| [increase-consistency.md](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency.md) | Modified | +1 / -1 | System prompts link updated to `claude-prompting-best-practices#give-claude-a-role` |
| [reduce-latency.md](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency.md) | Modified | +2 / -2 | Two "be-clear-and-direct" links updated to `claude-prompting-best-practices#be-clear-and-direct` |
| [reduce-prompt-leak.md](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-prompt-leak.md) | Modified | +1 / -1 | System prompts link updated to `claude-prompting-best-practices#give-claude-a-role` |
