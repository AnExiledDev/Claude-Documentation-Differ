# Claude API Documentation Changes — 2026-04-11

## Summary

This update introduces the Advisor Tool (`advisor_20260301`), a new beta tool type that delegates to a configurable Claude model sub-instance within a message request. The Java SDK has been bumped from 2.20.0 to 2.22.0 with a major Managed Agents API documentation expansion (+27,000 lines), including 3 new agent endpoint pages. The `advisor-tool-2026-03-01` beta header has been added across all SDK references and REST API endpoints.

---

## Significant Changes

### Beta API — Advisor Tool

- **New tool type `BetaAdvisorTool20260301`**: A new built-in beta tool that invokes a secondary Claude model inference as part of message processing. Enabled via the `"advisor-tool-2026-03-01"` beta header.

  The tool definition accepts:
  > `BetaAdvisorTool20260301 = object { model, name, type, allowed_callers, cache_control, caching, defer_loading, max_uses, strict }`
  - `name`: always `"advisor"`
  - `type`: always `"advisor_20260301"`
  - `model`: the Claude model to use for the advisor sub-inference (supports `"claude-mythos-preview"`, `"claude-opus-4-6"`, `"claude-sonnet-4-6"`, and more)
  - `allowed_callers`: restricts which contexts can invoke the tool — `"direct"`, `"code_execution_20250825"`, or `"code_execution_20260120"`
  - `caching`: optional `BetaCacheControlEphemeral` to cache the advisor's own prompt prefix (5m or 1h TTL)
  - `defer_loading`: if `true`, excludes the tool from the initial system prompt and only loads it when referenced via tool search
  - `max_uses`: maximum number of invocations allowed per request
  - `strict`: enables schema validation on tool names and inputs

  - *Implication*: Enables delegating sub-tasks to a separately-configured Claude model within a single message, with optional caching of the advisor's context for efficiency in multi-turn use.
  - *Source*: [Beta API Reference](https://platform.claude.com/docs/en/api/beta.md)

- **New response block `BetaAdvisorToolResultBlock`**: The advisor returns one of three result content variants:

  > - `BetaAdvisorResultBlock { text, type: "advisor_result" }` — plain text result
  > - `BetaAdvisorRedactedResultBlock { encrypted_content, type: "advisor_redacted_result" }` — opaque blob containing the advisor's output; must be round-tripped verbatim; do not inspect or modify
  > - `BetaAdvisorToolResultError { error_code, type: "advisor_tool_result_error" }` — error codes include: `max_uses_exceeded`, `prompt_too_long`, `too_many_requests`, `overloaded`, `unavailable`, `execution_time_exceeded`

  - *Implication*: The `advisor_redacted_result` variant is for privacy-filtered contexts (analogous to encrypted code execution results); callers must store and re-submit the blob opaquely.
  - *Source*: [Beta Messages](https://platform.claude.com/docs/en/api/beta/messages.md)

- **New usage type `BetaAdvisorMessageIterationUsage`**: Token usage per advisor sub-inference is now tracked separately in the message usage response:

  > Token usage for an advisor sub-inference iteration.
  > Fields: `cache_creation`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `input_tokens`, `output_tokens`, `model`, `type: "advisor_message"`

  - *Implication*: Developers can attribute token costs to each advisor call individually, including which model was used and whether cache was hit.
  - *Source*: [Beta Messages](https://platform.claude.com/docs/en/api/beta/messages.md)

- **`"advisor-tool-2026-03-01"` beta header added to all endpoints** across REST API and all SDK references (Python, TypeScript, Go, Java, Ruby, C#). The `AnthropicBeta` enum count incremented from 18 to 19 members.

### Models

- **New model `"claude-mythos-preview"`** referenced in the Advisor Tool's model parameter:
  > "New class of intelligence, strongest in coding and cybersecurity"

  This model identifier appears in `BetaAdvisorTool20260301.model` and `BetaAdvisorMessageIterationUsage.model`. It is not currently listed in the Managed Agents model enum.

- **`claude-opus-4-6` description updated** in Java SDK and related references:
  - Before: `"Most intelligent model for building agents and coding"`
  - After: `"Frontier intelligence for long-running agents and coding"`

### Java SDK — Major Managed Agents Documentation Expansion

- **Java SDK updated: `2.20.0` → `2.22.0`**. The installation instructions in the Java SDK reference page now specify version 2.22.0.
  - *Source*: [Java SDK](https://platform.claude.com/docs/en/api/sdks/java.md)

- **3 new Java SDK beta agent pages** added:
  - `java/beta/agents.md` — overview of Agents CRUD operations with create/list/retrieve/update/archive/versions
  - `java/beta/agents/create.md` — `POST /v1/agents` with full `AgentCreateParams` type including `model`, `name`, `system`, `tools`, `mcpServers`, `skills`, `metadata`, `description`
  - `java/beta/agents/update.md` — `POST /v1/agents/{agent_id}` with optimistic concurrency via `version` field

- **Java `java/beta.md` comprehensive expansion (+27,238 lines)**: Now documents the full Managed Agents API surface for Java, matching other SDKs. Newly documented sections include:
  - **Agents** (create, list, retrieve, update, archive, versions) — `BetaManagedAgentsAgent` type with toolset configs, MCP server configs, custom tools, skills
  - **Environments** (create, list, retrieve, update, delete, archive) — `BetaEnvironment`, `BetaCloudConfig`, `BetaLimitedNetwork`, `BetaPackages`
  - **Sessions** (full CRUD + archive) and **Events** (list, send, stream) — extensive event types: `BetaManagedAgentsAgentMessageEvent`, `BetaManagedAgentsAgentCustomToolUseEvent`, `BetaManagedAgentsAgentMCPToolUseEvent`, session lifecycle events, retry status types
  - **Resources** (add, list, retrieve, update, delete) — `BetaManagedAgentsFileResource`, `BetaManagedAgentsGitHubRepositoryResource`
  - **Vaults** (full CRUD + archive) and **Credentials** (full CRUD + archive) — MCP OAuth, Static Bearer, Token Endpoint auth types
  - **Files** (upload, list, download, retrieve metadata)
  - **Skills**

- **`BetaRefusalStopDetails` added to Java beta message response**: New optional field on `BetaMessage`:
  > `Optional<BetaRefusalStopDetails> stopDetails` — Structured information about a refusal.
  > - `category`: `CYBER("cyber")` or `BIO("bio")` — policy category that triggered the refusal; null when not mapped
  > - `explanation`: Human-readable explanation; not guaranteed to be stable; null when unavailable
  > - `type`: always `"refusal"`

  - *Implication*: Java SDK users can now programmatically inspect why a message was refused, including which safety policy applied.
  - *Source*: [Java Beta Messages](https://platform.claude.com/docs/en/api/java/beta/agents.md)

### Agent Toolset Types

- **`BetaManagedAgentsAgentToolset20260401`** (toolset type `"agent_toolset_20260401"`) introduced as the versioned built-in agent toolset configuration, supporting individual tool enable/disable and permission policies (`always_allow` or `always_ask`) for: `bash`, `edit`, `read`, `write`, `glob`, `grep`, `web_fetch`, `web_search`.

### Environments API — Cookie Parameters Removed

- **`sessionKey` cookie parameter removed** from all Environments API endpoint documentation (create, list, retrieve, update, delete, archive). This was a `### Cookie Parameters` section containing `sessionKey: optional string` that has been dropped from all six environments endpoints.
  - *Implication*: The session key cookie is no longer a documented parameter for environment management calls. Developers relying on cookie-based auth for environments should verify their integration.
  - *Source*: [Beta Environments](https://platform.claude.com/docs/en/api/beta/environments.md)

### Code Execution Tool Types — Documentation Reordering

- **`BetaBashCodeExecutionToolResultErrorParam`** now lists `"output_file_too_large"` as a valid error code alongside `"invalid_tool_input"`, `"unavailable"`, `"too_many_requests"`, and `"execution_time_exceeded"`.

- **Tool result block ordering in request body** has changed. `BetaAdvisorToolResultBlockParam` is now the first listed tool result type in the `BetaToolResultBlockParam` union, followed by `BetaCodeExecutionToolResultBlockParam`, `BetaBashCodeExecutionToolResultBlockParam`, `BetaTextEditorCodeExecutionToolResultBlockParam`, `BetaToolSearchToolResultBlockParam`, and `BetaMCPToolUseBlockParam`. This is a documentation organization change; no API behavior change implied.

- **Tool name enumeration** now includes `"advisor"` as the first listed built-in tool name value (alongside `"web_search"`, `"web_fetch"`, `"code_execution"`, etc.).

---

## New Pages

- **`en_api_java_beta_agents.md`** — Java SDK: Agents API overview with create/list/retrieve/update/archive/versions operations. [View](https://platform.claude.com/docs/en/api/java/beta/agents.md)
- **`en_api_java_beta_agents_create.md`** — Java SDK: `POST /v1/agents` with full `AgentCreateParams` parameter reference. [View](https://platform.claude.com/docs/en/api/java/beta/agents/create.md)
- **`en_api_java_beta_agents_update.md`** — Java SDK: `POST /v1/agents/{agent_id}` with `AgentUpdateParams` including optimistic concurrency `version` field. [View](https://platform.claude.com/docs/en/api/java/beta/agents/update.md)

---

## Notable Details

- The **`BetaAdvisorTool20260301` replaces `BetaToolSearchToolBm25_20251119`** in the primary position within the tool definitions list in the beta messages documentation. `BetaToolSearchToolBm25_20251119` is still present but now listed after the advisor tool type. This ordering shift suggests the advisor tool is intended as the primary advanced tool entry point.

- The **`BetaAdvisorRedactedResultBlock`** contains `encrypted_content` described as: *"Opaque blob containing the advisor's output. Round-trip verbatim; do not inspect or modify."* This mirrors the pattern used by encrypted code execution results (`BetaEncryptedCodeExecutionResultBlockParam`), indicating the advisor results in certain contexts will be filtered/encrypted before being returned to the caller.

- The **`caching` field on `BetaAdvisorTool20260301`** is distinct from the standard `cache_control` field. The description reads: *"When set, each advisor call writes a cache entry at the given TTL so subsequent calls in the same conversation read the stable prefix. When omitted, the advisor prompt is not cached."* This enables per-advisor-call prompt caching independently of the outer message's cache control.

- **`BetaAdvisorMessageIterationUsage`** appears in the message usage array alongside the main usage, meaning a single top-level API call can produce multiple usage entries when the advisor tool fires. Billing attribution for advisor calls uses the advisor model's pricing.

- The Java SDK's `agent.model` field accepts either a plain model string or a `BetaManagedAgentsModelConfigParams` object that adds a `speed` field (`"standard"` or `"fast"`). The `"fast"` mode *"provides significantly faster output token generation at premium pricing"* and is validated at agent creation time.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `java/beta.md` | Modified | +27,238 / -683 | Comprehensive Managed Agents API expansion for Java SDK |
| `java/beta/messages.md` | Modified | +4,567 / -1,263 | Advisor Tool + new domain types for Java SDK |
| `typescript/beta.md` | Modified | +4,613 / -1,017 | Advisor Tool + type additions for TypeScript SDK |
| `beta/messages.md` | Modified | +4,513 / -949 | Advisor Tool types, usage tracking, `advisor-tool-2026-03-01` header |
| `go/beta.md` | Modified | +4,536 / -864 | Advisor Tool + type additions for Go SDK |
| `python/beta.md` | Modified | +4,355 / -360 | Advisor Tool + type additions for Python SDK |
| `ruby/beta.md` | Modified | +4,341 / -669 | Advisor Tool + type additions for Ruby SDK |
| `csharp/beta.md` | Modified | +3,793 / -617 | Advisor Tool + type additions for C# SDK |
| `beta.md` | Modified | +4,335 / -687 | Advisor Tool types, `advisor-tool-2026-03-01` header |
| `cli/beta.md` | Modified | +2,802 / -257 | Advisor Tool + type additions for CLI |
| `python/beta/messages.md` | Modified | +4,211 / -324 | Advisor Tool types for Python SDK |
| `go/beta/messages.md` | Modified | +4,183 / -619 | Advisor Tool types for Go SDK |
| `typescript/beta/messages.md` | Modified | +4,190 / -702 | Advisor Tool types for TypeScript SDK |
| `ruby/beta/messages.md` | Modified | +4,230 / -666 | Advisor Tool types for Ruby SDK |
| `csharp/beta/messages.md` | Modified | +3,211 / -141 | Advisor Tool types for C# SDK |
| `sdks/java.md` | Modified | +84 / -81 | Java SDK version bump 2.20.0 → 2.22.0 |
| `java/beta/agents.md` | **New** | +3,746 | Java Agents API overview |
| `java/beta/agents/create.md` | **New** | +648 | Java Agents create endpoint |
| `java/beta/agents/update.md` | **New** | +726 | Java Agents update endpoint |
| `beta/messages/create.md` | Modified | +402 / -3 | `advisor-tool-2026-03-01` header + Advisor tool types |
| `beta/messages/count_tokens.md` | Modified | +236 / -3 | `advisor-tool-2026-03-01` header added |
| `beta/messages/batches/create.md` | Modified | +235 / -2 | `advisor-tool-2026-03-01` header added |
| `beta/environments.md` | Modified | +12 / -24 | Cookie Parameters sections removed |
| `beta/sessions.md` | Modified | +43 / -15 | Sessions listing updates |
| `beta/vaults.md` | Modified | +38 / -14 | Vaults listing updates |
| `java/messages.md` | Modified | +72 / -0 | Model section added to Java non-beta messages |

---
*Generated from Claude API documentation changes detected on 2026-04-11*
