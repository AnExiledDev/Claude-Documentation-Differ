# Claude API Documentation Changes — 2026-05-13

## Summary

This update primarily documents expanded platform availability across the agents-and-tools surface: Claude Platform on AWS and Microsoft Foundry are now explicitly listed as supported platforms for code execution, programmatic tool calling, web search, web fetch, agent skills, and the MCP connector. Several smaller documentation fixes accompany this, including a clarification that `tool_result` `content` is optional, a correction to how deferred tool loading works internally, and C# code example modernization to top-level statements.

## Significant Changes

### Platform Availability Expansion

Multiple features now explicitly support **Claude Platform on AWS** and **Microsoft Foundry**, replacing vague prior wording that listed only "Claude API" or "Microsoft Azure AI Foundry".

- **Code Execution Tool**: Platform list updated to include Claude Platform on AWS and Microsoft Foundry with documentation links. Vertex AI replaces "Google Vertex AI" throughout.
  > `- **[Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws)**`
  > `- **[Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry)**`
  - *Implication*: Developers using Claude Platform on AWS can now confirm code execution is officially supported.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

- **Programmatic Tool Calling**: Platform scope expanded; Amazon Bedrock and Vertex AI explicitly excluded.
  > `Programmatic tool calling is available on the Claude API, [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws), and [Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry). It is not currently available on Amazon Bedrock or Vertex AI.`
  - *Implication*: The `missing_beta_header` error table entry was removed simultaneously, reflecting that this feature is not available on Bedrock/Vertex.
  - *Source*: [Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md)

- **Web Search Tool**: Claude Platform on AWS added to the dynamic filtering support list; notably, web search for Claude Mythos Preview is explicitly **not** available on Claude Platform on AWS.
  > `The web search tool (with and without dynamic filtering) is available on the Claude API, [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws), and [Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry). On Vertex AI, only the basic web search tool (without dynamic filtering) is available. Web search is not available on Amazon Bedrock.`
  - *Implication*: Developers on Claude Platform on AWS can use dynamic filtering web search; those using Mythos Preview cannot.
  - *Source*: [Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool.md)

- **Web Fetch Tool**: Platform list expanded to include Claude Platform on AWS; "Microsoft Azure" corrected to "Microsoft Foundry".
  > `The web fetch tool (with and without dynamic filtering) is available on the Claude API, [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws), and [Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry). It is not available on Amazon Bedrock or Vertex AI.`
  - *Source*: [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md)

- **Advisor Tool**: Now available on Claude Platform on AWS in beta; explicitly unavailable on Amazon Bedrock, Vertex AI, and Microsoft Foundry.
  > `The advisor tool is available in beta on the Claude API and on [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws). It is not currently available on Amazon Bedrock, Vertex AI, or Microsoft Foundry.`
  - *Source*: [Advisor Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md)

- **MCP Connector**: Platform scope clarified — previously stated "not supported on Amazon Bedrock and Google Vertex AI"; now states availability positively on the Claude API, Claude Platform on AWS, and Microsoft Foundry.
  > `The MCP connector is available on the Claude API, [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws), and [Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry). It is not currently available on Amazon Bedrock or Vertex AI.`
  - *Source*: [MCP Connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md)

- **Fine-Grained Tool Streaming**: Platform support now expressed as an explicit list with links rather than the previous "all platforms" shorthand.
  > `Fine-grained tool streaming is supported on the Claude API, [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws), [Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock), [Vertex AI](/docs/en/build-with-claude/claude-on-vertex-ai), and [Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry).`
  - *Source*: [Fine-Grained Tool Streaming](https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming.md)

### Agent Skills

- **Agent Skills available on Claude Platform on AWS and Microsoft Foundry**: Pre-built and custom Skills now officially extend to both platforms, with a new note making inheritance explicit.
  > `Claude Platform on AWS and Microsoft Foundry inherit the same Skills behavior as the Claude API in all following sections.`
  > `**Pre-built Agent Skills** are available on claude.ai, the Claude API, [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws), and [Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry).`
  - *Implication*: Custom Skills can also be uploaded through the Skills API on these new platforms.
  - *Source*: [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md)

- **Custom Skills sharing scope renamed**: "organization-wide" replaced with "workspace-wide" for Claude API custom Skills.
  > `Custom Skills are shared workspace-wide; all workspace members can access them.`
  - *Implication*: This is likely a terminology alignment, not a behavior change, but developers using the API should use "workspace" terminology when referencing skill sharing scope.
  - *Source*: [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md)

### Tool Use Behavior Clarifications

- **`tool_result` `content` is optional**: The `content` field in `tool_result` blocks is now explicitly labeled as `(optional)`.
  > `- \`content\` (optional): The result of the tool, as a string...`
  - *Implication*: Developers can omit `content` when returning tool results — for example, when only setting `is_error: true`.
  - *Source*: [Handle Tool Calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls.md)

- **Deferred tool loading mechanism clarified**: The internal behavior of `defer_loading` is now described more precisely, explaining that the API appends a `tool_reference` block and then expands it before passing to Claude.
  > `When the model discovers a deferred tool through tool search, the API appends a \`tool_reference\` block inline in the conversation, then expands it into the full tool definition before passing it to Claude. The prefix is untouched, so prompt caching is preserved.`
  - *Implication*: This clarifies that the prompt cache prefix is never invalidated by deferred tool discovery.
  - *Source*: [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md)

- **Tool search searches argument names/descriptions**: The troubleshooting section now clarifies that the tool search regex matches against tool name, description, argument names, and argument descriptions — not just name and description.
  > `**Cause:** Tool name, description, argument names, or argument descriptions don't match the regex pattern`
  - *Source*: [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md)

- **Tool Search on Claude Platform on AWS**: New note added clarifying that server-side tool search works identically on Claude Platform on AWS as on the Claude API (no InvokeModel/Converse distinction).
  > `On [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws), server-side tool search works identically to the Claude API. Claude Platform on AWS uses the Anthropic Messages API directly, so there is no InvokeModel or Converse distinction.`
  - *Source*: [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md)

### Advisor Tool — Priority Tier Link Added

- **Priority Tier now linked**: The advisor tool documentation now links "Priority Tier" to its dedicated documentation page.
  > `**[Priority Tier](/docs/en/api/service-tiers)** is honored for each model. Priority Tier on the executor model does not extend to the advisor; you need Priority Tier on the advisor model specifically.`
  - *Source*: [Advisor Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md)

### Code Execution Tool — Files API Beta Header Fix

- **Retrieve generated files example corrected**: The TypeScript code example for retrieving files generated during code execution removed `"code-execution-2025-08-25"` from the `betas` array, leaving only `"files-api-2025-04-14"`.
  > `betas: ["files-api-2025-04-14"],`
  - *Implication*: Developers retrieving generated files only need the Files API beta header, not the code execution beta header.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

## Minor Changes

- **agent-skills/quickstart.md**: CLI code example updated — `--format yaml` replaced with `--raw-output` flag (+1/-1)
- **handle-tool-calls.md**: `content` field in `tool_result` explicitly marked as `(optional)` (+1/-1)
- **tool-runner.md**: `max_tokens` in streaming example corrected from `1000` to `1024` (+1/-1)
- **server-tools.md**: ZDR link updated from `/zero-data-retention` to `/manage-claude/api-and-data-retention`; "the Console" → "Claude Console" (+3/-3)
- **parallel-tool-use.md**: TypeScript example improved with ✓/✗ status indicators and an else branch for the no-parallel-tools case; reference to deprecated models simplified (+9/-5)
- **strict-tool-use.md**: C# code example modernized to top-level statements (removing wrapping class/Main boilerplate); PHP examples fixed to output results (+27/-36)
- **mcp-connector.md**: Minor punctuation and wording cleanup throughout; `cache_control` description now links to prompt caching docs; "MCP Connector" → "MCP connector" in data retention section (+13/-13)
- **web-search-tool.md**: `tool_use_id` example value corrected from `servertoolu_a93jad` to `srvtoolu_a93jad` (+3/-3)
- **fine-grained-tool-streaming.md**: Chunk numbering in example corrected (Chunk 8→7, Chunk 9→8); "generally available" simplified to "available" (+5/-5)
- **code-execution-tool.md**: CLI examples updated (`--format yaml` → `--raw-output`); "Retrieve generated files" section promoted from `####` to `###` heading level (+14/-13)

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| agent-skills/overview.md | Modified | SIGNIFICANT | +20/-16 | Platform expansion (AWS, Foundry); "workspace-wide" terminology; claude.ai capitalization |
| tool-use/strict-tool-use.md | Modified | SIGNIFICANT | +27/-36 | C# example refactored to top-level statements; PHP output fixes |
| tool-use/programmatic-tool-calling.md | Modified | SIGNIFICANT | +16/-17 | Platform expansion (AWS, Foundry); removed Bedrock/Vertex beta-header error entry |
| tool-use/code-execution-tool.md | Modified | SIGNIFICANT | +14/-13 | Platform expansion; Files API beta array fix; heading promotion |
| tool-use/parallel-tool-use.md | Modified | SIGNIFICANT | +9/-5 | TypeScript example improved with status indicators; deprecated model note simplified |
| tool-use/tool-search-tool.md | Modified | SIGNIFICANT | +13/-10 | AWS note added; defer_loading mechanism clarified; regex scope expanded |
| mcp-connector.md | Modified | SIGNIFICANT | +13/-13 | Platform availability clarified; punctuation/link cleanup |
| tool-use/fine-grained-tool-streaming.md | Modified | SIGNIFICANT | +5/-5 | Platform list with links; chunk numbering fix |
| tool-use/advisor-tool.md | Modified | SIGNIFICANT | +4/-4 | Platform expansion (AWS); Priority Tier link added |
| tool-use/web-fetch-tool.md | Modified | SIGNIFICANT | +3/-3 | Platform expansion (AWS, Foundry); Vertex AI naming update |
| tool-use/web-search-tool.md | Modified | SIGNIFICANT | +3/-3 | Platform expansion; Mythos Preview exclusion on AWS; tool_use_id fix |
| tool-use/server-tools.md | Modified | SIGNIFICANT | +3/-3 | ZDR link and console name updates |
| agent-skills/quickstart.md | Modified | MINOR | +1/-1 | CLI flag: `--format yaml` → `--raw-output` |
| tool-use/handle-tool-calls.md | Modified | MINOR | +1/-1 | `content` field marked optional in tool_result |
| tool-use/tool-runner.md | Modified | MINOR | +1/-1 | `max_tokens` corrected to 1024 in streaming example |

---
*Generated from Claude API documentation changes detected on 2026-05-13*
