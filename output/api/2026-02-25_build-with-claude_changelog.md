# Claude API Documentation Changes — 2026-02-25

## Summary

The prompt engineering documentation has been substantially reorganized: the previously scattered technique-specific pages are now consolidated into a single comprehensive reference (`claude-prompting-best-practices.md`), restructured with thematic top-level sections. A new page documents Claude Console prompting tools (prompt generator, templates & variables, prompt improver). Multiple context-management pages received updates introducing the concept of "context rot" and cross-linking a new Anthropic engineering post on effective context engineering.

---

## Significant Changes

### Prompt Engineering Documentation

- **`claude-prompting-best-practices.md` — major restructure and consolidation (+370/-254 lines)**: The guide was reorganized from a loosely ordered list of tips under a flat "Guidance for specific situations" umbrella into clearly delineated top-level sections: **General principles**, **Output and formatting**, **Tool use**, **Thinking and reasoning**, **Agentic systems**, and **Capability-specific tips**. Content is unchanged in substance but is now grouped by concern, making it significantly easier to navigate for task-specific lookup.
  > "This is the single reference for prompt engineering with Claude's latest models... It covers foundational techniques, output control, tool use, thinking, and agentic systems. Jump to the section that matches your situation."
  - *Implication*: The guide is now a self-contained reference rather than an index pointing to separate micro-pages; bookmarks to specific old section anchors may need updating.
  - *Source*: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

- **Section renames — clarity of terminology**: Two foundational sections were renamed to better reflect their intent:
  - "Be explicit with your instructions" → **"Be clear and direct"**
  - "Be vigilant with examples & details" → **"Use examples effectively"**

  Both renames come with expanded content. "Use examples effectively" now includes concrete guidance on few-shot/multishot prompting (3–5 examples recommended, wrapped in `<example>` tags) and guidance on diversity and relevance.
  > "Examples are one of the most reliable ways to steer Claude's output format, tone, and structure. A few well-crafted examples (known as few-shot or multishot prompting) can dramatically improve accuracy and consistency."
  - *Implication*: No API behavior changes; this is authoring guidance for prompt engineers.
  - *Source*: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

- **New sections: "Structure prompts with XML tags", "Give Claude a role", "Long context prompting"**: Three previously absent (or scattered) techniques now appear as explicit subsections under General principles. "Long context prompting" includes a documented finding:
  > "Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs."

  It also provides a multi-document XML template with `<documents>`, `<document index="n">`, `<source>`, and `<document_content>` tags.
  - *Implication*: For applications using 20K+ token inputs, placing the query after the document corpus is now explicitly recommended with quantified uplift.
  - *Source*: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

- **"Thinking sensitivity" section removed; converted to a callout Note**: The standalone section warning that Claude Opus 4.5 is sensitive to the word "think" when extended thinking is disabled has been collapsed into a brief `<Note>` inside the thinking section.
  > "When extended thinking is disabled, Claude Opus 4.5 is particularly sensitive to the word 'think' and its variants. Consider using alternatives like 'consider,' 'evaluate,' or 'reason through' in those cases."
  - *Implication*: The guidance is retained but is now a secondary callout rather than a top-level section. Users scanning for this information should look inside "Thinking and reasoning."
  - *Source*: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

- **Adaptive thinking recommendation added**: A new explicit recommendation was inserted into the "Leverage thinking & interleaved thinking capabilities" section:
  > "In internal evaluations, adaptive thinking reliably drives better performance than extended thinking, and we recommend moving to adaptive thinking to get the most intelligent responses."
  - *Implication*: Anthropic is now explicitly endorsing adaptive thinking (`thinking: {type: "adaptive"}`) over manual extended thinking with `budget_tokens` based on internal benchmark data.
  - *Source*: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

- **"Overthinking" section scope narrowed to Opus 4.6**: The section previously referenced "Claude 4.6 models" broadly. It now explicitly applies to **Claude Opus 4.6**, with updated mitigation advice:
  > "Replace blanket defaults with more targeted instructions. Instead of 'Default to using [tool],' add guidance like 'Use [tool] when it would enhance your understanding of the problem.'"
  - *Source*: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

- **"Migrating away from prefilled responses" — security rationale removed**: The previous version stated prefills "have been a common vector for jailbreaks and other exploits." That language is gone. The new text is neutral:
  > "Starting with Claude 4.6 models, prefilled responses on the last assistant turn are no longer supported. Model intelligence and instruction following has advanced such that most use cases of prefill no longer require it."
  - *Implication*: The migration guidance (use Structured Outputs, system prompt instructions, XML tags, etc.) is unchanged. This is a tone shift, not a behavioral change.
  - *Source*: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

- **"Chain complex prompts" — new section in Agentic systems**: Introduces explicit guidance on when explicit prompt chaining (multi-step API calls) adds value over Claude's internal reasoning:
  > "With adaptive thinking and subagent orchestration, Claude handles most multi-step reasoning internally. Explicit prompt chaining — breaking a task into sequential API calls — is still useful when you need to inspect intermediate outputs or enforce a specific pipeline structure."

  The most recommended pattern is now **self-correction**: generate a draft → review against criteria → refine.
  - *Implication*: Developers building pipelines should consider whether explicit chaining is still necessary vs. relying on adaptive thinking.
  - *Source*: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

- **"Frontend design" section moved**: Previously under the general guidance area; now placed under the new **Capability-specific tips** top-level section. Content is unchanged.

---

### Context Management

- **"Context rot" concept introduced across context docs**: The `context-windows.md` page now names and defines the degradation caused by long contexts:
  > "More context isn't automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as *context rot*. This makes curating what's in context just as important as how much space is available."

  Two specific benchmarks are cited: [MRCR](https://arxiv.org/abs/2501.03276) and [GraphWalks](https://arxiv.org/abs/2412.04360), on which Claude achieves state-of-the-art results.
  - *Implication*: Context quality is now framed as an engineering concern, not just a token budget concern.
  - *Source*: [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md)

- **Compaction rationale expanded**: The `compaction.md` description now explains *why* compaction helps beyond the token cap:
  > "This isn't just about staying under a token cap. As conversations get longer, models struggle to maintain focus across the full history. Compaction keeps the active context focused and performant by replacing stale content with concise summaries."
  - *Source*: [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction.md)

- **Context editing rationale expanded**: The `context-editing.md` description similarly frames the technique as active curation rather than a limit-avoidance mechanism:
  > "Context editing gives you fine-grained runtime control over that curation."
  - *Source*: [Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing.md)

- **New cross-references to "Effective context engineering" blog post**: All three context-management pages (`compaction.md`, `context-editing.md`, `context-windows.md`) now include `<Tip>` callouts linking to [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) on the Anthropic engineering blog.

- **Multi-session agent design tip added to `context-windows.md`**: A new callout under Context Awareness:
  > "For agents that span multiple sessions, design your state artifacts so that context recovery is fast when a new session starts. The [memory tool's multi-session pattern](/docs/en/agents-and-tools/tool-use/memory-tool#multi-session-software-development-pattern) walks through a concrete approach. See also [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)."
  - *Source*: [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md)

---

### Extended Thinking

- **Link to extended thinking tips updated**: `extended-thinking.md` previously linked to a standalone `extended-thinking-tips` page. Both the inline link and the "Next steps" card now point to the new anchor within `claude-prompting-best-practices.md`:
  - Old: `/docs/en/build-with-claude/prompt-engineering/extended-thinking-tips`
  - New: `/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#leverage-thinking-and-interleaved-thinking-capabilities`
  - *Implication*: Any hardcoded links to the old `extended-thinking-tips` page in developer tooling or documentation mirrors may 404 or redirect.
  - *Source*: [Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

---

## New Pages

- **`prompting-tools.md`** — Documents the three Claude Console tools for building and refining prompts: the **Prompt Generator** (creates prompt templates from task descriptions), **Prompt Templates and Variables** (explains `{{double bracket}}` syntax and fixed vs. variable content), and the **Prompt Improver** (4-step enhancement: example identification → initial draft → chain-of-thought refinement → example enhancement). Includes a worked example showing how a bare classification prompt becomes a structured, XML-tagged template with reasoning steps. [View](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools.md)

---

## Notable Details

- **Prompt engineering overview simplified**: `overview.md` dropped the numbered 8-step technique progression (linking to individual pages like `be-clear-and-direct`, `multishot-prompting`, `chain-of-thought`, etc.) and the lengthy "Prompting vs. finetuning" comparison section. The overview now acts as a thin navigation hub pointing to `claude-prompting-best-practices.md` as the primary reference and `prompting-tools` as the Console companion.

- **Overtrigger scope clarified**: The tool overtriggering warning (previously attributed to "Claude Opus 4.5 and Claude 4.6 models") is now consistently scoped to "Claude Opus 4.5 and Claude Opus 4.6" — a minor clarification that disambiguates from Claude Haiku 4.5/Sonnet 4.6.

- **Thinking tips expanded with four new bullets**: The "Leverage thinking & interleaved thinking capabilities" section added:
  1. Prefer general instructions over prescriptive steps ("think thoroughly" often beats a hand-written step-by-step plan)
  2. Multishot examples work with thinking (use `<thinking>` tags in few-shot examples)
  3. Manual CoT as a fallback when thinking is off (use `<thinking>` and `<answer>` tags)
  4. Ask Claude to self-check ("Before you finish, verify your answer against [test criteria]")

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `prompt-engineering/claude-prompting-best-practices.md` | Modified | +370 / -254 | Major restructure into thematic sections; new content on long context, roles, XML, thinking, chaining |
| `prompt-engineering/overview.md` | Modified | +11 / -32 | Simplified to navigation hub; dropped finetuning comparison and step-by-step technique list |
| `context-windows.md` | Modified | +11 / -1 | Introduced "context rot," MRCR/GraphWalks benchmarks, multi-session agent tip |
| `compaction.md` | Modified | +9 / -2 | Expanded rationale; added link to Anthropic engineering blog post |
| `context-editing.md` | Modified | +1 / -1 | Reframed as active curation; added link to Anthropic engineering blog post |
| `extended-thinking.md` | Modified | +2 / -2 | Updated link from standalone tips page to new anchor in best practices doc |
| `prompt-engineering/prompting-tools.md` | New | +216 | Console prompt generator, templates & variables, and prompt improver documentation |

---
*Generated from Claude API documentation changes detected on 2026-02-25*
