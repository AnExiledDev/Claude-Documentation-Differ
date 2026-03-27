# Claude API Documentation Changes — 2026-03-27

## Summary

This update introduces a new dedicated page documenting Zero Data Retention (ZDR) eligibility and data retention policies across all Claude API features. The changes also add ZDR-status notices to 10+ individual feature pages, expand stop-reason handling guidance with a new section on incomplete tool use under `max_tokens`, and consolidate (removing duplicate content from) the structured outputs and prompt caching pages.

## Significant Changes

### Data Retention & Zero Data Retention (ZDR)

- **New `api-and-data-retention` page**: A comprehensive reference documenting ZDR eligibility and data retention behavior for every Claude API feature and endpoint.
  > "When users use API endpoints with zero data retention (ZDR), customer data submitted through those endpoints is not stored at rest after the API response is returned except where needed to comply with law or combat misuse."
  - *Implication*: Developers building on Claude for enterprise use cases now have a single authoritative reference for understanding which API features can be used within a ZDR arrangement, without needing to check individual feature pages.
  - *Source*: [API and data retention](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention.md)

- **ZDR eligibility table**: The new page includes a full per-feature breakdown with three statuses:
  - **ZDR: Yes** — Messages API, Token Counting, Web Search/Fetch, Memory tool, Compaction, Context Editing, Fast Mode, 1M context window, Adaptive Thinking, Citations, Data Residency, Effort, Extended Thinking, PDF Support, Search Results, Bash/Text Editor/Computer Use tools, Fine-grained tool streaming, Prompt Caching
  - **ZDR: Yes (qualified)** — Structured Outputs (JSON schema cached up to 24 hours); Tool Search (tool catalog metadata retained server-side)
  - **ZDR: No** — Batch Processing (29-day retention), Code Execution (container data up to 30 days), Programmatic Tool Calling, Files API (retained until deleted), Agent Skills, MCP Connector
  > "Features marked 'No' are fundamentally stateful: the Batch API stores your jobs, the Files API stores your files, and code execution runs in persistent containers."
  - *Implication*: Organizations with ZDR contracts now have explicit guidance on which features step outside ZDR scope and what technical data is held for each.
  - *Source*: [API and data retention — ZDR eligibility by feature](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention.md)

- **CORS restriction under ZDR documented**: The new page notes that CORS is not supported for organizations with ZDR arrangements, requiring a backend proxy for browser-based API calls.
  > "Cross-Origin Resource Sharing (CORS) is not supported for organizations with ZDR arrangements. If you need to make API calls from browser-based applications, you must use a backend proxy server."
  - *Implication*: Developers building browser apps under ZDR contracts must route requests through a server-side proxy.
  - *Source*: [API and data retention — Limitations](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention.md)

- **ZDR notices added to individual feature pages**: Ten feature pages now display a note at the top linking to the new data retention reference:
  - Adaptive Thinking, Citations, Context Windows, Data Residency, Effort, Extended Thinking, PDF Support, Search Results — marked ZDR eligible
  - Batch Processing, Files API — marked **not** ZDR eligible, with a link to their per-feature `## Data retention` section
  - *Source (examples)*: [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing.md), [Files API](https://platform.claude.com/docs/en/build-with-claude/files.md), [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **`## Data retention` sections added to feature pages**: Batch Processing, Files API, Prompt Caching, Structured Outputs, and Skills Guide each gained a dedicated `## Data retention` section documenting what is stored and for how long.

### Stop Reason Handling

- **New guidance: Incomplete tool use blocks on `max_tokens` truncation**: The `handling-stop-reasons.md` page gained a new `#### Incomplete tool use blocks` subsection (+227 lines) covering how to detect and recover from a response that is cut off mid-`tool_use` block due to hitting the `max_tokens` limit. Multi-language code examples are provided for Python, TypeScript, C#, Go, Java, PHP, and Ruby.
  > "If Claude's response is cut off due to hitting the `max_tokens` limit, and the truncated response contains an incomplete tool use block, you'll need to retry the request with a higher `max_tokens` value to get the full tool use."
  - *Implication*: Agent and tool-calling applications should check for `stop_reason == "max_tokens"` combined with the last content block being a `tool_use` block, and retry with an increased token budget rather than attempting to process a partial tool call.
  - *Source*: [Handling stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons.md)

### Features Overview

- **ZDR column added to feature tables**: `overview.md` was substantially restructured (+43/-41 lines) to add a **Zero Data Retention (ZDR)** column across all feature tables (Model capabilities, Server-side tools, Client-side tools, Tool infrastructure, Context management, Files and assets). Each row now shows the ZDR eligibility status directly.
  - *Implication*: Developers can now assess ZDR impact for any feature at a glance from the overview page.
  - *Source*: [Features overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

### Content Consolidation

- **Structured outputs page significantly trimmed** (+8/-1077 lines): Sections titled `### Why strict tool use matters for agents`, `### Quick start`, `### How it works`, and `### Common use cases` were removed. The current page retains the core API reference, migration tip for `output_format` → `output_config.format`, SDK examples, and the new `## Data retention` section. A `<Tip>` block was added noting that the `output_format` beta parameter and the old beta header (`structured-outputs-2025-11-13`) continue to work for a transition period.
  > "**Migrating from beta?** The `output_format` parameter has moved to `output_config.format`, and beta headers are no longer required. The old beta header (`structured-outputs-2025-11-13`) and `output_format` parameter will continue working for a transition period."
  - *Implication*: The migration note is now more prominent; the removed sections may have been moved elsewhere or deemed redundant with existing documentation.
  - *Source*: [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **Prompt caching page trimmed** (+32/-488 lines): A large example block (the `# many more tools` section) was removed. The page gained a `## Data retention` section. The core caching reference remains intact.
  - *Source*: [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

## New Pages

- **[api-and-data-retention.md]** — Comprehensive reference for ZDR eligibility and data retention policies across all Claude API features. Includes a per-feature table with endpoint, ZDR status, and retention details; ZDR scope definition; CORS limitation note; and an FAQ covering Claude Code ZDR, Bedrock/Vertex exclusions, and how to request ZDR arrangements. [View](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention.md)

## Notable Details

- **ZDR carve-out for policy violations**: Even under ZDR, Anthropic may retain data for up to 2 years if a session is flagged for Usage Policy violations. This is now explicitly documented in the new data retention page.
- **Dynamic filtering not ZDR-eligible**: Web search and web fetch are ZDR-eligible, but the [dynamic filtering](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool) feature for Opus 4.6 and Sonnet 4.6 is specifically called out as **not** ZDR-eligible (footnote in the ZDR eligibility table).
- **Prompt caching ZDR clarification**: KV cache representations and cryptographic hashes are held in memory for the cache TTL and promptly deleted after expiry — prompts and outputs themselves are not stored. This is now documented at the feature level.
- **Structured outputs ZDR qualified scope**: Only the JSON schema is cached (up to 24 hours since last use); prompts and outputs are not stored. This qualifies for ZDR under the "qualified" designation.
- **`refusal` stop reason note updated**: The `handling-stop-reasons.md` page now references Sonnet 4.5, Opus 4.1, and a support article on understanding Sonnet 4.5's API safety filters in its guidance on handling `refusal` responses.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| api-and-data-retention.md | New | +156 | ZDR eligibility reference for all Claude API features |
| handling-stop-reasons.md | Modified | +227/-4 | Added incomplete tool use detection on max_tokens truncation |
| structured-outputs.md | Modified | +8/-1077 | Added data retention section; removed duplicated content sections |
| prompt-caching.md | Modified | +32/-488 | Added data retention section; removed large tool example block |
| overview.md | Modified | +43/-41 | Added ZDR column to all feature tables |
| skills-guide.md | Modified | +9/-3 | Added data retention section |
| batch-processing.md | Modified | +7/-1 | Added data retention section and ZDR-not-eligible note |
| files.md | Modified | +7/-1 | Added data retention section and ZDR-not-eligible note |
| context-editing.md | Modified | +8/-6 | Minor text updates |
| compaction.md | Modified | +4/-4 | Minor text updates |
| adaptive-thinking.md | Modified | +4/-0 | Added ZDR-eligible note |
| citations.md | Modified | +4/-0 | Added ZDR-eligible note |
| context-windows.md | Modified | +4/-0 | Added ZDR-eligible note |
| data-residency.md | Modified | +4/-0 | Added ZDR-eligible note |
| effort.md | Modified | +4/-0 | Added ZDR-eligible note |
| extended-thinking.md | Modified | +5/-1 | Updated ZDR-eligible note |
| pdf-support.md | Modified | +4/-0 | Added ZDR-eligible note |
| search-results.md | Modified | +4/-0 | Added ZDR-eligible note |
| token-counting.md | Modified | +2/-2 | Minor text update |
| fast-mode.md | Modified | +1/-1 | Minor text update |
| working-with-messages.md | Modified | +1/-1 | Minor text update |

---
*Generated from Claude API documentation changes detected on 2026-03-27*
