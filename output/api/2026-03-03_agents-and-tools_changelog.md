# Claude API Documentation Changes — 2026-03-03

## Summary

Fifteen pages in the Agents and Tools section received a uniform formatting pass. The dominant change is a punctuation style standardisation: bold inline labels previously written as `**Label**:` (colon outside the closing `**`) are now written as `**Label:**` (colon inside). Alongside this, several sentences were reworded from passive or deferential voice to direct, imperative voice (e.g., "Please reach out" → "Reach out"), and a handful of minor prose and typo fixes were applied.

## Significant Changes

### Agent Skills

- **Section rename in quickstart — "What are Agent Skills?" → "Agent Skills overview"**: The introductory section in the quickstart page was renamed.
  > Before: `## What are Agent Skills?`
  > After: `## Agent Skills overview`
  - *Implication*: Any documentation links or anchor refs pointing to `#what-are-agent-skills` will now resolve to `#agent-skills-overview`. Update any hardcoded deep links.
  - *Source*: [Agent Skills Quickstart](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart.md)

- **Best practices — pervasive bold-label punctuation standardisation**: All bold labels across the best-practices page had their trailing colon moved inside the closing `**` markers (73 additions / 73 deletions). Example:
  > `-**Default assumption**: Claude is already very smart`
  > `+**Default assumption:** Claude is already very smart`
  - *Implication*: Purely cosmetic; no content was changed.
  - *Source*: [Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)

- **Best practices — minor prose change in iterative development description**: One sentence was updated from future tense to present tense.
  > `-Simply ask Claude to create a Skill and it will generate properly structured SKILL.md content`
  > `+Simply ask Claude to create a Skill and it generates properly structured SKILL.md content`
  - *Implication*: No functional change.
  - *Source*: [Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)

### Tools

- **Computer use tool — "currently in beta" phrasing simplified**: The beta status note dropped "currently".
  > `-Computer use is currently in beta and requires a beta header`
  > `+Computer use is in beta and requires a beta header`
  - *Implication*: No functional change.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

- **Computer use tool — typo fix in reference implementation description**: A missing word was inserted.
  > `-It includes all of the components needed have Claude use a computer.`
  > `+It includes all of the components needed to have Claude use a computer.`
  - *Implication*: Corrects a grammatical error only.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

- **Implement tool use — image alt text added**: The `tool_choice` diagram image now has a descriptive alt attribute.
  > `-![Image](/docs/images/tool_choice.png)`
  > `+![Diagram showing the four tool_choice options: auto, any, tool, and none](/docs/images/tool_choice.png)`
  - *Implication*: Accessibility improvement; no functional API change.
  - *Source*: [Implement Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use.md)

- **Web fetch tool — capitalisation fix**: "Javascript" corrected to "JavaScript".
  > `-The web fetch tool currently does not support web sites dynamically rendered via Javascript.`
  > `+The web fetch tool currently does not support web sites dynamically rendered via JavaScript.`
  - *Implication*: No functional change.
  - *Source*: [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md)

- **Web search tool — Console name clarified**: The reference to "Console" in the admin setup note was expanded to "Claude Console".
  > `-Your organization's administrator must enable web search in Console`
  > `+Your organization's administrator must enable web search in the Claude Console`
  - *Implication*: Clarifies the product name; no functional change.
  - *Source*: [Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool.md)

### Feedback Call-to-Actions

- **"Please" removed from feedback prompts across multiple pages**: Several Note and Tip components on the code execution, computer use, memory, web fetch, and tool search pages had "Please" removed from their feedback form links.
  > `-Please reach out through the feedback form to share your feedback on this feature.`
  > `+Reach out through the feedback form to share your feedback on this feature.`
  - *Implication*: Purely editorial; links and destinations unchanged.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md), [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md), [Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md), [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md), [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md)

## Notable Details

- The MCP connector deprecation notice was lightly reworded from "Please migrate to `mcp-client-2025-11-20`" to "Migrate to `mcp-client-2025-11-20`" — the deprecated version identifier and migration guide link are unchanged.
- The fine-grained tool streaming warning about `max_tokens` changed "You will generally have to" to "You generally have to" — same meaning, slightly less formal.
- The programmatic tool calling page updated several descriptions from future/passive constructions ("will receive", "Claude's code will receive") to present active tense ("receives", "Claude's code receives") — no semantic change to the API behaviour described.
- The tool search tool's feedback note changed from linking to "our feedback form" to linking to "the feedback form" — same URL destination.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| agent-skills/best-practices.md | Modified | +73 / -73 | Bold label colon style standardised throughout; one sentence tense change |
| agent-skills/quickstart.md | Modified | +11 / -11 | Section renamed "What are Agent Skills?" → "Agent Skills overview"; bold label punctuation |
| mcp-connector.md | Modified | +1 / -1 | "Please migrate" → "Migrate" in deprecation notice |
| tool-use/bash-tool.md | Modified | +9 / -9 | Bold label punctuation in use cases and limitations |
| tool-use/code-execution-tool.md | Modified | +1 / -1 | "Please reach out" → "Reach out" in feedback note |
| tool-use/computer-use-tool.md | Modified | +7 / -7 | Removed "currently" from beta note; "Please" removed; typo fix; bold label punctuation |
| tool-use/fine-grained-tool-streaming.md | Modified | +1 / -1 | "will generally have to" → "generally have to" in max_tokens warning |
| tool-use/implement-tool-use.md | Modified | +1 / -1 | Added descriptive alt text to tool_choice diagram image |
| tool-use/memory-tool.md | Modified | +1 / -1 | "Please reach out" → "Reach out" in feedback note |
| tool-use/overview.md | Modified | +2 / -2 | "Please continue" → "Continue" in courses tip |
| tool-use/programmatic-tool-calling.md | Modified | +22 / -22 | Bold label punctuation; passive-to-active voice; "will" removed from present-tense descriptions |
| tool-use/text-editor-tool.md | Modified | +13 / -13 | Bold label punctuation; future tense → present tense in tool behaviour descriptions |
| tool-use/tool-search-tool.md | Modified | +17 / -17 | Bold label punctuation; feedback note reworded; troubleshooting cause/fix label punctuation |
| tool-use/web-fetch-tool.md | Modified | +6 / -6 | Feedback note reworded; "Javascript" → "JavaScript"; passive-to-active rewording |
| tool-use/web-search-tool.md | Modified | +4 / -4 | "Console" → "Claude Console"; passive-to-active voice in error descriptions |
