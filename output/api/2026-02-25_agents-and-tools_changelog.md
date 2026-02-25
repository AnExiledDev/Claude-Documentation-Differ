# Claude API Documentation Changes — 2026-02-25

## Summary

Seven pages in the agents-and-tools/tool-use section received substantive additions focused on long-running agent patterns and multi-session workflows. The most significant additions are: a new multi-session software development pattern in the memory tool docs, a git-based checkpointing guide in the bash tool docs, and expanded best-practice guidance on tool design, error messages, and scaling tool libraries with tool search.

## Significant Changes

### Memory Tool

- **Multi-session software development pattern**: A new top-level section documents a structured pattern for agents that span multiple sessions. The pattern divides work into three phases: an initializer session that creates memory artifacts (progress log, feature checklist, startup script reference), subsequent sessions that read those artifacts to recover state, and end-of-session updates that write back progress before closing.
  > "For long-running software projects that span multiple agent sessions, memory files need to be bootstrapped deliberately, not just written ad hoc as work progresses. The pattern below turns memory into a structured recovery mechanism, so each new session can pick up exactly where the last one left off."
  - *Implication*: Developers building multi-session coding agents now have an explicit, documented pattern for session continuity using the memory tool rather than ad hoc file writes.
  - *Source*: [Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md)

- **Just-in-time context retrieval framing**: The memory tool introduction now explicitly positions the tool as the primitive for just-in-time context retrieval, with a cross-reference to the [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) engineering post.
  > "This is the key primitive for just-in-time context retrieval: rather than loading all relevant information upfront, agents store what they learn in memory and pull it back on demand."
  - *Implication*: Clarifies the intended use pattern for the memory tool in agentic workflows — load what is needed when it is needed, not everything upfront.
  - *Source*: [Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md)

### Bash Tool

- **Git-based checkpointing guidance**: A new subsection under the bash tool's best practices describes using git as a structured state recovery mechanism in long-running agent workflows — not merely for version control.
  > "Git serves as a structured recovery mechanism in long-running agent workflows, not just a way to save changes:
  > - **Capture a baseline:** Before any agent work begins, commit the current state.
  > - **Commit per feature:** Each completed feature gets its own commit. These serve as rollback points if something goes wrong later.
  > - **Reconstruct state at session start:** Read `git log` alongside a progress file to understand what has already been done and what comes next.
  > - **Revert on failure:** If work goes sideways, `git checkout` reverts to the last good commit instead of trying to debug a broken state."
  - *Implication*: Directly complements the memory tool's multi-session pattern; together they form a complete recovery strategy for long-running coding agents.
  - *Source*: [Bash Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool.md)

- **Terminal-Bench 2.0 benchmark reference**: The opening description now cites Terminal-Bench 2.0 as evidence for the bash tool's effectiveness.
  > "On [Terminal-Bench 2.0](https://github.com/terminal-bench/terminal-bench), a benchmark that evaluates real-world terminal tasks using shell-only validation, Claude shows strong performance gains with access to a persistent bash session."
  - *Source*: [Bash Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool.md)

### Tool Design Best Practices (implement-tool-use.md)

Three new bullet points were added to the tool design guidelines:

- **Consolidate related operations into fewer tools**: Documentation now advises grouping related actions into a single tool with an `action` parameter rather than creating per-action tools (e.g., a single `pr` tool with an `action` field instead of separate `create_pr`, `review_pr`, `merge_pr` tools).
  > "Rather than creating a separate tool for every action (`create_pr`, `review_pr`, `merge_pr`), group them into a single tool with an `action` parameter. Fewer, more capable tools reduce selection ambiguity."
  - *Implication*: Directly addresses tool selection accuracy degradation at scale; also aligns with the tool search guidance about namespacing.
  - *Source*: [Implement Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use.md)

- **Meaningful namespacing in tool names**: New guidance recommends prefixing tool names by service (e.g., `github_list_prs`, `slack_send_message`) to make tool selection unambiguous as libraries grow, with a specific callout that this is especially important when using tool search.
  - *Source*: [Implement Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use.md)

- **Return only high-signal information from tools**: New guidance advises returning semantic, stable identifiers (slugs or UUIDs) rather than opaque internal references, and including only the fields Claude needs for its next reasoning step.
  > "Bloated responses waste context and make it harder for Claude to extract what matters."
  - *Source*: [Implement Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use.md)

- **Instructive error messages tip**: A new callout in the error handling section advises developers to write error messages that include what went wrong and what Claude should try next.
  > "Write instructive error messages. Instead of generic errors like `\"failed\"`, include what went wrong and what Claude should try next, e.g., `\"Rate limit exceeded. Retry after 60 seconds.\"` This gives Claude the context it needs to recover or adapt without guessing."
  - *Source*: [Implement Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use.md)

### Tool Search Tool

- **Quantified context cost figures**: The tool search overview now includes concrete token-cost figures to justify the tool's purpose.
  > "A typical multi-server setup (GitHub, Slack, Sentry, Grafana, Splunk) can consume ~55K tokens in definitions before Claude does any actual work. Tool search typically reduces this by over 85%, loading only the 3–5 tools Claude actually needs for a given request."
  - *Implication*: The original description used relative language ("massive portions"); the update gives developers concrete numbers to evaluate when tool search is worth adopting.
  - *Source*: [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md)

- **Namespacing added to best practices**: The optimization tips section now explicitly recommends prefixing tool names by service or resource (e.g., `github_`, `slack_`) so search queries naturally surface the right tool group.
  - *Source*: [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md)

### Programmatic Tool Calling

- **Concrete multi-tool workflow example and benchmark references**: The page introduction was expanded with a worked example (budget compliance across 20 employees: 20 round-trips vs. a single script) and references to BrowseComp and DeepSearchQA benchmarks.
  > "The difference compounds fast in real workflows. Consider checking budget compliance across 20 employees: the traditional approach requires 20 separate model round-trips, pulling thousands of expense line items into the context along the way. With programmatic tool calling, a single script runs all 20 lookups, filters the results, and returns only the employees who exceeded their limits."
  - *Source*: [Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md)

### Computer Use Tool

- **Multi-session verification tip**: A new callout advises running end-to-end verification at the start of each session for agents that span multiple sessions, noting that browser-based checks catch regressions from prior sessions that code-level review misses.
  > "For agents that span multiple sessions, run end-to-end verification at the start of each session, not only after implementation."
  - *Implication*: Reinforces the multi-session agent pattern documented across the bash and memory tool pages.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

- **WebArena benchmark reference**: The opening description now cites WebArena state-of-the-art results for Claude on autonomous web navigation.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

### Tool Use Overview

- **Benchmark references and "tool contract" framing**: The page introduction was expanded to frame tool use as defining a contract between developer and model, and now cites LAB-Bench FigQA and SWE-bench to support the value of tool access.
  > "Each tool defines a contract: you specify what operations are available and what they return; Claude decides when and how to call them."
  - *Source*: [Tool Use Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md)

- **Advanced tool use tip added to Next Steps**: A new callout in the "Next Steps" section links to the [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) engineering post and describes when to consider tool search and programmatic tool calling.
  > "Once your tool workflows grow beyond a handful of tools, explore [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) to learn how tool search and programmatic tool calling scale tool orchestration to hundreds of tools without blowing up your context window."
  - *Source*: [Tool Use Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md)

## Notable Details

- **Cross-doc pattern coherence**: The multi-session agent pattern is distributed deliberately across three pages: memory tool (session state management), bash tool (git-based recovery), and computer use tool (end-of-session verification). Developers implementing long-running agents should read all three together.
- **Consistent external engineering post references**: Six of the seven modified pages now link to one or more Anthropic engineering posts ([Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use), [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)). These posts appear to be newly published companion material for this documentation update.
- **Namespacing consistency**: The namespacing recommendation (prefix tool names by service) appears independently in both `implement-tool-use.md` and `tool-search-tool.md`, reinforcing it as a cross-cutting design principle rather than a single-tool optimization.
- **Tool search description change**: The original framing called the two challenges "critical"; the updated text removes that adjective and uses more precise language ("compounds quickly", "degrades significantly"), a shift toward concrete specificity over emphasis.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| memory-tool.md | Modified | +23/-1 | New multi-session software development pattern section (3 subsections); just-in-time retrieval framing added to intro |
| implement-tool-use.md | Modified | +11/-0 | Three new tool design best practices; two new tip callouts (tool design post, instructive error messages) |
| programmatic-tool-calling.md | Modified | +7/-1 | Expanded intro with concrete example and benchmark citations; new tip linking to Advanced tool use post |
| bash-tool.md | Modified | +10/-1 | New git-based checkpointing subsection; Terminal-Bench 2.0 benchmark added to intro |
| tool-search-tool.md | Modified | +10/-5 | Quantified token cost figures (~55K → 85% reduction); namespacing tip added; minor wording tightened |
| computer-use-tool.md | Modified | +9/-1 | New multi-session verification tip; WebArena benchmark added to intro |
| overview.md | Modified | +5/-1 | Tool contract framing and benchmark citations added to intro; Advanced tool use tip in Next Steps |

---
*Generated from Claude API documentation changes detected on 2026-02-25*
