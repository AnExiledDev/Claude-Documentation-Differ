# Claude API Documentation Changes — 2026-04-17

## Summary

Documentation across the entire agents-and-tools section was updated to reflect Claude Opus 4.7 as the new primary recommended model, replacing Claude Opus 4.6 in all code examples. The most substantive changes introduce Managed Agents (beta) support in the `claude-api` skill, add a `/claude-api migrate` subcommand for automating model migrations, document Claude Opus 4.7's expanded computer use capabilities (higher resolution support), and simplify the Tool Search Tool's ZDR policy while extending its model support to Haiku 4.5+.

---

## Significant Changes

### Models

- **Claude Opus 4.7 added as the default example model**: All code samples across 15 documentation pages now reference `claude-opus-4-7` (and typed SDK constants like `Model.ClaudeOpus4_7`, `anthropic.ModelClaudeOpus4_7`, `Model.CLAUDE_OPUS_4_7`) instead of `claude-opus-4-6`. This affects every SDK language (Python, TypeScript, Go, Java, Ruby, C#, PHP, cURL/CLI).
  - *Implication*: Developers copying examples will now target Opus 4.7 by default; existing Opus 4.6 code is not broken.
  - *Source*: [Tool Use Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md) and all tool pages

- **Tool use system prompt token count documented for Claude Opus 4.7**: The tool use overview's compatibility table now includes a row for Claude Opus 4.7 — 346 tokens for `auto`/`none` tool choice, 313 tokens for `any`/`tool`.
  > `| Claude Opus 4.7 | auto, none<hr />any, tool | 346 tokens<hr />313 tokens |`
  - *Implication*: Developers budgeting tokens for tool-enabled prompts can now account for Opus 4.7's overhead, which is identical to Opus 4.6.
  - *Source*: [Tool Use Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md)

### Agent Skills — Managed Agents (Beta)

- **`claude-api` skill expanded to cover Claude Managed Agents**: The skill now documents two distinct Anthropic surfaces — the Messages API and Claude Managed Agents (beta). This is the largest single change in this update (+85/−29 lines).

  > The `claude-api` skill is an open-source Agent Skill that provides Claude with detailed, up-to-date reference material for building applications on two Anthropic surfaces:
  > - **Messages API** — the primary surface for single requests, streaming chat, tool use, batch processing, prompt caching, structured outputs, and custom agent loops.
  > - **Claude Managed Agents (beta)** — a first-party surface for server-managed stateful agents with Anthropic-hosted tool execution, persistent agent configs, and per-session containers.

  - *Implication*: The skill now routes third-party deployments (Bedrock, Vertex AI, Foundry) to Messages API + tool use, since Managed Agents is first-party only.
  - *Source*: [Claude API Skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill.md)

- **Language support table updated — "Agent SDK" column replaced with "Managed Agents (beta)"**: Java, Go, Ruby, PHP, and cURL now have Managed Agents beta support. C# remains unsupported for Managed Agents.

  | Language   | Messages API SDK | Tool runner | Managed Agents |
  |------------|------------------|-------------|----------------|
  | Python     | Yes              | Yes (beta)  | Yes (beta)     |
  | TypeScript | Yes              | Yes (beta)  | Yes (beta)     |
  | Java       | Yes              | No          | Yes (beta)     |
  | Go         | Yes              | No          | Yes (beta)     |
  | Ruby       | Yes              | Yes (beta)  | Yes (beta)     |
  | C#         | Yes              | No          | No             |
  | PHP        | Yes              | No          | Yes (beta)     |
  | cURL       | Yes              | N/A         | Yes (beta)     |

  - *Source*: [Claude API Skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill.md)

- **New `managed-agents-2026-04-01` beta header documented**: The Managed Agents beta requires this header, which the SDK sets automatically for all `client.beta.agents.*`, `client.beta.environments.*`, `client.beta.sessions.*`, and `client.beta.vaults.*` calls.
  - *Implication*: Developers building Managed Agents do not need to set this header manually when using a supported SDK.
  - *Source*: [Claude API Skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill.md)

- **New "Setting up a Managed Agent" section with `/claude-api managed-agents-onboard` subcommand**:
  > The skill runs an interview that walks you through the Managed Agents mental model (Agent configs versus Sessions), templates an agent config, configures environments and tools, sets up the session loop, and emits runnable code for your language. The skill also covers the mandatory **Agent (once) → Session (every run)** flow — `model`, `system`, and `tools` live on the agent, never on the session, and agents should be created once and referenced by ID.
  - *Implication*: New adopters of Managed Agents can use this subcommand to scaffold a working agent from scratch via an interactive interview.
  - *Source*: [Claude API Skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill.md)

### Model Migration Tooling

- **New "Migrating to a newer Claude model" section with `/claude-api migrate` subcommand**: The `claude-api` skill can now automate codebase-wide model migrations. The command accepts an optional scope to avoid a scope-confirmation prompt.

  ```text
  /claude-api migrate this project to claude-opus-4-7
  /claude-api migrate everything under src/ to claude-opus-4-7
  ```

  The skill handles:
  > - **Model ID swaps**, including typed SDK constants across all supported languages
  > - **Breaking parameter changes**, such as removing `temperature`, `top_p`, and `top_k` for Claude Opus 4.7, and converting `thinking: {type: "enabled", budget_tokens: N}` to `thinking: {type: "adaptive"}`
  > - **Prefill replacement**, converting assistant-message prefill patterns to structured outputs where applicable
  > - **Beta header cleanup**, removing headers that are GA on the target model (e.g., `effort-2025-11-24`, `fine-grained-tool-streaming-2025-05-14`, `interleaved-thinking-2025-05-14`)
  > - **Effort calibration**, recommending an `output_config.effort` starting point (e.g., `xhigh` for coding/agentic use cases on Claude Opus 4.7)

  - *Implication*: Migrating a codebase from Opus 4.6 to 4.7 involves several breaking parameter changes; this tooling automates the mechanical parts and flags items requiring manual verification.
  - *Source*: [Claude API Skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill.md)

### Computer Use Tool

- **Claude Opus 4.7 added to `computer-use-2025-11-24` beta support**: The beta note now lists Claude Opus 4.7 alongside Opus 4.6, Sonnet 4.6, and Opus 4.5 as supported models.

- **New coordinate resolution note for Claude Opus 4.7**:
  > Claude Opus 4.7 supports up to 2576 pixels on the long edge, and its coordinates are 1:1 with image pixels (no scale-factor conversion required). The 1568-pixel guidance below applies to earlier models.
  - *Implication*: The coordinate transformation logic described in the "Handle coordinate scaling for higher resolutions" section is not required when using Opus 4.7; developers should branch on model version if supporting both.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

### Advisor Tool

- **Claude Opus 4.7 added as a valid executor/advisor pair**: The model compatibility table now includes a row for Opus 4.7 as both executor and advisor.
  > `| Claude Opus 4.7 (claude-opus-4-7) | Claude Opus 4.7 (claude-opus-4-7) |`
  - *Implication*: Developers can now use `claude-opus-4-7` as the `model` field value in the `advisor_20260301` tool definition; examples across all SDKs have been updated accordingly.
  - *Source*: [Advisor Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md)

### Tool Search Tool

- **"Data retention" section removed; ZDR note simplified**: The previous section stated that server-side tool search indexes and stores tool catalog data beyond the API response. This has been replaced with a simpler statement:
  > This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
  - *Implication*: The old language implied the tool search tool was *not* fully ZDR-eligible for the server-side variant. The updated language removes that distinction — organizations with ZDR arrangements can treat the feature as fully ZDR-eligible.
  - *Source*: [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md)

- **Haiku 4.5+ added to supported model list**: The model support limit previously stated "no Haiku." It now reads:
  > **Model support:** Claude Mythos Preview, Sonnet 4.0+, Opus 4.0+, Haiku 4.5+
  - *Implication*: The tool search tool can now be used with Claude Haiku 4.5 and later, expanding cost-sensitive use cases.
  - *Source*: [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md)

### Web Search and Web Fetch Tools

- **Claude Opus 4.7 added to dynamic filtering support**: Both the `web_search_20260209` and `web_fetch_20260209` tool versions now list Claude Opus 4.7 alongside Claude Mythos Preview, Opus 4.6, and Sonnet 4.6 as models that support dynamic filtering.
  - *Implication*: Dynamic filtering (code-based pre-filtering of search results/fetched content before it enters the context window) is available for Opus 4.7 users.
  - *Source*: [Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool.md), [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md)

### Code Execution and Programmatic Tool Calling

- **Claude Opus 4.7 added to supported models**: Both the code execution tool and programmatic tool calling documentation now include `claude-opus-4-7` in their model support tables.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md), [Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md)

---

## Notable Details

- **Code block label change: "Shell" → "cURL"**: Every curl-based code example across all 15 modified pages has had its language label changed from `Shell` to `cURL`. This is a display/rendering change with no impact on the API.

- **Automatic activation triggers expanded for the `claude-api` skill**: The skill now activates not only on SDK import detection, but also when a user "asks Claude to help build, debug, or optimize something with the Claude API, an Anthropic SDK, or Managed Agents" or modifies Claude features in a file. The previous trigger `claude_agent_sdk` import has been removed.

- **Agent SDK card removed from "Related documentation"**: The `claude-api-skill.md` page no longer links to `/docs/en/agent-sdk/overview` in its related resources section. This appears to reflect the shift from a separate "Agent SDK" concept to "Managed Agents."

- **Progressive disclosure updated to cover surface selection**: The skill now uses the surface (Messages API vs. Managed Agents) as an additional dimension when deciding which documentation to load, alongside language and feature task.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| agent-skills/claude-api-skill.md | Modified | +85/−29 | Added Managed Agents beta coverage, `/claude-api migrate`, `/claude-api managed-agents-onboard`, updated language support table |
| tool-use/code-execution-tool.md | Modified | +48/−47 | Added Claude Opus 4.7 to model support table; model ID bumps in examples |
| tool-use/text-editor-tool.md | Modified | +27/−26 | Model ID bumps in examples; Shell→cURL label |
| agent-skills/quickstart.md | Modified | +25/−25 | Model ID bumps; Shell→cURL label; nocheck flags added to CLI blocks |
| tool-use/web-fetch-tool.md | Modified | +22/−22 | Added Opus 4.7 to dynamic filtering support; model ID bumps |
| tool-use/web-search-tool.md | Modified | +21/−21 | Added Opus 4.7 to dynamic filtering support; model ID bumps |
| tool-use/advisor-tool.md | Modified | +19/−18 | Added Opus 4.7 as valid executor/advisor; model ID bumps |
| tool-use/programmatic-tool-calling.md | Modified | +19/−18 | Added Claude Opus 4.7 to model support; model ID bumps |
| mcp-connector.md | Modified | +16/−16 | Model ID bumps across all SDK examples |
| tool-use/computer-use-tool.md | Modified | +18/−14 | Added Opus 4.7 to beta support; added 2576px resolution note |
| tool-use/memory-tool.md | Modified | +10/−10 | Model ID bumps; Shell→cURL label |
| tool-use/tool-search-tool.md | Modified | +12/−18 | Removed Data retention section; added Haiku 4.5+ support; ZDR note simplified |
| tool-use/overview.md | Modified | +6/−5 | Added Opus 4.7 to token count table; model ID bumps |
| tool-use/fine-grained-tool-streaming.md | Modified | +7/−7 | Model ID bumps; Shell→cURL label |
| tool-use/bash-tool.md | Modified | +4/−4 | Model ID bumps; Shell→cURL label |

---

*Generated from Claude API documentation changes detected on 2026-04-17*
