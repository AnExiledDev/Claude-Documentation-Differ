# Claude API Documentation Changes — 2026-02-19

## Summary

This update primarily documents the launch of **Claude Sonnet 4.6** across the full platform surface: it gains adaptive thinking, the effort parameter, interleaved thinking, the 1M-token context window (beta), structured outputs GA support, prompt caching, batch pricing, and availability on Bedrock, Vertex AI, and Microsoft Foundry. Concurrently, the structured outputs documentation was substantially expanded with per-SDK usage tabs, new schema complexity limits, and graduation of the Go, Ruby, and C# SDK examples from beta APIs to GA. ZDR (Zero Data Retention) eligibility tables were also updated to reflect the status of several features.

---

## Significant Changes

### Models — Claude Sonnet 4.6 Rollout

**Claude Sonnet 4.6 added across all major features**: Sonnet 4.6 (`claude-sonnet-4-6`) is now documented as a supported model for adaptive thinking, the effort parameter, interleaved thinking, compaction, context editing, context awareness, structured outputs (GA), prompt caching, batch processing, search results, and the 1M-token context window beta.

- *Implication*: Developers previously using Sonnet 4.5 with extended thinking should plan migration; `thinking.type: "enabled"` with `budget_tokens` is now **deprecated** on Sonnet 4.6 (as it already was on Opus 4.6). Prefilling on the last assistant turn is also deprecated on Sonnet 4.6.
- *Source*: [Adaptive Thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md), [Effort](https://platform.claude.com/docs/en/build-with-claude/effort.md), [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

---

### Adaptive Thinking

- **Sonnet 4.6 added as supported model**: Adaptive thinking (`thinking: {type: "adaptive"}`) is now available on both Claude Opus 4.6 and Claude Sonnet 4.6.

  > `thinking.type: "enabled"` and `budget_tokens` are **deprecated** on Opus 4.6 and Sonnet 4.6 and will be removed in a future model release. Use `thinking.type: "adaptive"` with the `effort` parameter instead. If you are already using extended thinking with `budget_tokens`, it continues to work and no immediate changes are required.

  - *Implication*: Migrate Sonnet 4.6 workloads from `type: "enabled"` to `type: "adaptive"` where applicable. Manual `budget_tokens` continues to be supported in the interim.
  - *Source*: [Adaptive Thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md)

- **Softened performance claim**: The documentation previously stated adaptive thinking "reliably drives better performance." It now reads "can drive better performance for many workloads, especially bimodal tasks and long-horizon agentic workflows," and explicitly notes that extended thinking with `budget_tokens` remains fully supported for workloads requiring predictable latency and precise cost control.

- **Interleaved thinking behavior clarified by model**:
  - **Opus 4.6 adaptive mode**: Interleaved thinking is automatic. The `interleaved-thinking-2025-05-14` beta header is **deprecated** on Opus 4.6 and is safely ignored if included.
  - **Sonnet 4.6 manual mode**: Interleaved thinking is supported via the `interleaved-thinking-2025-05-14` beta header.
  - **Opus 4.6 manual mode**: Interleaved thinking is **not available**. Use adaptive mode for workflows that require thinking between tool calls on Opus 4.6.

  > Adaptive mode: Interleaved thinking is automatically enabled on both Opus 4.6 and Sonnet 4.6. Manual mode on Sonnet 4.6: Interleaved thinking is supported via the `interleaved-thinking-2025-05-14` beta header. Manual mode on Opus 4.6: Interleaved thinking is not available.

  - *Source*: [Adaptive Thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md)

---

### Effort Parameter

- **Sonnet 4.6 now supported**: The effort parameter previously applied only to Opus 4.6 and Opus 4.5; Sonnet 4.6 is now included.

- **New guidance for Sonnet 4.6 effort levels**:

  > Sonnet 4.6 defaults to `high` effort. Explicitly set effort when using Sonnet 4.6 to avoid unexpected latency:
  > - **Medium effort** (recommended default): Best balance of speed, cost, and performance for most applications. Suitable for agentic coding, tool-heavy workflows, and code generation.
  > - **Low effort**: For high-volume or latency-sensitive workloads.
  > - **High effort**: For tasks requiring maximum intelligence from Sonnet 4.6.

  - *Implication*: Without an explicit `effort` setting, Sonnet 4.6 defaults to `high`, which may be unexpectedly slow for some workloads. Set `effort: "medium"` as a safe default unless your use case requires deeper reasoning.
  - *Source*: [Effort](https://platform.claude.com/docs/en/build-with-claude/effort.md)

- **Sonnet 4.6 and thinking modes**: Sonnet 4.6 supports both adaptive thinking (effort controls thinking depth) and manual thinking with interleaved mode. Opus 4.5 and other Claude 4 models use manual `budget_tokens`.

---

### Structured Outputs — Major Expansion

The structured outputs page received the largest update in this diff (+687/-104 lines). Key changes:

- **Sonnet 4.6 added to GA list**: Structured outputs are now generally available on Claude Opus 4.6, **Claude Sonnet 4.6**, Claude Sonnet 4.5, Claude Opus 4.5, and Claude Haiku 4.5 on the Claude API and Amazon Bedrock.

- **ZDR note added**:

  > Prompts and responses using structured outputs are processed with Zero Data Retention (ZDR). However, the JSON schema itself is temporarily cached for up to 24 hours for optimization purposes. No prompt or response data is retained.

- **Beta graduation in Go, Ruby, C# SDKs**: Examples updated from beta API calls (e.g., `client.Beta.Messages.New`, `client.beta.messages.create`, `"structured-outputs-2025-11-13"` header) to stable GA APIs. Old beta parameter `output_format` migrated to `output_config.format`.

  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **New: Schema complexity limits** replace the old generic "Schema validation errors" section:

  | Limit | Value | Description |
  |-------|-------|-------------|
  | Strict tools per request | 20 | Maximum tools with `strict: true` |
  | Optional parameters | 24 | Total optional parameters across all strict schemas |
  | Parameters with union types | 16 | Total `anyOf` or type-array parameters across all strict schemas |

  > Beyond the explicit limits above, there are additional internal limits on the compiled grammar size. When these limits are exceeded, you'll receive a 400 error with "Schema is too complex for compilation." The API also enforces a **compilation timeout of 180 seconds**.

  - *Implication*: The optional-parameter and union-type limits apply across the total request, not per tool. Four strict tools with 6 optional parameters each would hit the 24-parameter limit even though no single tool appears large.
  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **Python SDK**: Removed `transform_schema()` requirement. `client.messages.parse()` with a Pydantic model now works directly without manually transforming the schema.

- **TypeScript SDK**: Updated to use `client.messages.parse()` instead of `client.messages.create()` for native schema integration with Zod; `response.parsed_output` returns typed output.

- **Java SDK**: Method renamed from `outputConfig(Class<T>)` to `outputFormat(Class<T>)`. Access parsed results via `response.output(Class<T>)`. Moved from `client.beta().messages()` to `client.messages()`. New documentation for Jackson/Swagger annotations (`@JsonPropertyDescription`, `@JsonIgnore`, `@Schema`) and schema streaming via `BetaMessageAccumulator`.

- **New SDK examples added** for Go, Ruby (with `ArrayOf`, `EnumOf`, `UnionOf`), C#, and PHP demonstrating `output_config` usage across all seven SDKs.

---

### Platform Integrations

#### Amazon Bedrock

- **Claude Sonnet 4.6 added** to model availability table (`anthropic.claude-sonnet-4-6`), available in global, us, eu, jp regions (not apac).
- **C# SDK added**: New `Anthropic.Bedrock` package supports Bedrock. Install with `dotnet add package Anthropic.Bedrock`.
- **Ruby SDK added**: New `aws-sdk-bedrockruntime` gem integration for Bedrock via `Anthropic::BedrockClient`.
- **Bearer token authentication** documented as a new authentication option for corporate environments, avoiding AWS credentials management. Supported in C#, Go, and Java SDKs (not Python, TypeScript, Ruby). Set `AWS_BEARER_TOKEN_BEDROCK` environment variable for automatic detection.

  > Bearer token authentication is supported in the C#, Go, and Java SDKs. The Python, TypeScript, and Ruby SDKs use AWS SigV4 signing only.

- **PHP SDK exclusion noted**:

  > The PHP SDK does not currently support Amazon Bedrock.

- *Source*: [Claude on Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md)

#### Google Vertex AI

- **Claude Sonnet 4.6 added** to model availability table (`claude-sonnet-4-6`).
- **Ruby SDK added** (`gem "anthropic"` + `gem "googleauth"`). Use via `Anthropic::VertexClient.new(region:, project_id:)`.
- **PHP SDK exclusion noted**:

  > The PHP SDK does not currently support Google Vertex AI.

- *Source*: [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

#### Microsoft Foundry

- **Java SDK added** (`com.anthropic:anthropic-java-foundry:2.14.0`). Both API key and bearer token (Entra ID) authentication patterns documented.
- **Claude Sonnet 4.6 added** to Foundry model table.
- **SDK support matrix clarified**:

  > Foundry is supported by the C#, Java, Python, and TypeScript SDKs. The Go, PHP, and Ruby SDKs do not currently support Microsoft Foundry.

- *Source*: [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md)

---

### Context Windows

- **Sonnet 4.6 added to 1M token context window beta**: Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5, and Sonnet 4 now all support the 1M-token context window (in beta for usage tier 4+, enabled with `context-1m-2025-08-07` header).

- **Context awareness now includes Sonnet 4.6**: The section "Context awareness in Claude Sonnet 4.5 and Haiku 4.5" has been renamed to include Sonnet 4.6.

  - *Source*: [Context Windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md)

---

### Prompt Caching

- **Sonnet 4.6 added** with minimum cacheable prompt length of **1024 tokens** (same as Sonnet 4.5).
- **Pricing** for Sonnet 4.6: $3/MTok base, $3.75/MTok 25% write premium, $6/MTok 100% write premium, $0.30/MTok cache read, $15/MTok output.
- **ZDR clarification added**:

  > Prompt caching stores KV cache representations and cryptographic hashes of cached content, but does not store the raw text of prompts or responses. This may be suitable for customers who require ZDR-type data retention commitments.

- *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

---

### Batch Processing

- **Sonnet 4.6 pricing added**: $1.50/MTok input, $7.50/MTok output (50% discount on standard API prices, same as Sonnet 4.5).
- **ZDR note added**: Batch processing is explicitly flagged as **not** covered by Zero Data Retention.

  > This feature is **not** covered by Zero Data Retention (ZDR) arrangements. Data is retained according to the feature's standard retention policy.

- *Source*: [Batch Processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing.md)

---

### Zero Data Retention (ZDR)

The ZDR eligibility tables were significantly updated:

**Newly added as ZDR-eligible** (data not stored after response):
- Web Search, Web Fetch, Memory Tool (client-side)
- Client-side Tool Search
- Context Management (compaction) — moved from "Not ZDR-eligible" to "ZDR-eligible"

**Newly documented as NOT ZDR-eligible**:
- Code Execution tool: container data retained up to 30 days
- Programmatic Tool Calling: built on code execution, same 30-day retention
- Server-side Tool Search: tool catalog data retained per standard policy

**ZDR notes added** to individual feature pages:
- Batch Processing: not ZDR-eligible
- Files API (beta): not ZDR-eligible
- Context Editing (beta): not ZDR-eligible
- Skills Guide (beta): not ZDR-eligible
- Token Counting: ZDR-eligible
- Working with Messages (Messages API): ZDR-eligible
- Structured Outputs: ZDR-eligible (schema cached up to 24 hours for optimization)

- *Source*: [Zero Data Retention](https://platform.claude.com/docs/en/build-with-claude/zero-data-retention.md)

---

### Compaction

- **Sonnet 4.6 added** as a supported model for compaction (beta, requires `compact-2026-01-12` header).
- **ZDR note added**: Compaction is ZDR-eligible.
- *Source*: [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction.md)

---

### Prompt Engineering Best Practices

- **New migration section: Sonnet 4.5 → Sonnet 4.6**. Detailed guidance added including:
  - Recommended effort settings by use case (medium for most, low for latency-sensitive, high for maximum intelligence)
  - Recommended max output token budget of 64k at medium/high effort
  - Code examples for non-thinking, extended thinking, and adaptive thinking paths
  - Guidance on when to prefer adaptive thinking (autonomous agents, computer use, bimodal workloads)

  > Claude Sonnet 4.6 defaults to an effort level of `high`, in contrast to Claude Sonnet 4.5 which had no effort parameter. Consider adjusting the effort parameter as you migrate from Claude Sonnet 4.5 to Claude Sonnet 4.6. If not explicitly set, you may experience higher latency with the default effort level.

- **Overthinking guidance updated for all Claude 4.6 models**: Now covers both Sonnet 4.6 and Opus 4.6. Key additions:
  - Remove anti-laziness prompts ("be thorough", "think carefully", "do not be lazy")
  - Remove explicit think tool instructions
  - Use effort as the primary control lever

  New sample prompt for reducing over-deliberation:
  > Prioritize execution over deliberation. Choose one approach and start producing output immediately. Do not compare alternatives or plan the entire solution before writing.

- **Prefilling deprecation now applies to all Claude 4.6 models** (not just Opus 4.6):

  > Starting with Claude 4.6 models, prefilled responses on the last assistant turn are no longer supported. Prefills have been a common vector for jailbreaks and other exploits.

- *Source*: [Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

---

### Tool Availability Status Changes (Overview)

Several tools moved from beta to GA status in the platform availability table:

| Tool | Previous Status | New Status |
|------|----------------|------------|
| Code Execution | Beta on Claude API + Azure | GA on Claude API + Azure; description updated to note "free when used with web search or web fetch" |
| Memory | Beta on all platforms | GA on Claude API, Bedrock, Vertex AI, Azure |
| Web Fetch | Beta on Claude API + Azure | GA on Claude API + Azure |
| Programmatic Tool Calling | Beta on Claude API + Azure | GA on Claude API + Azure |
| Tool Search | Beta on all platforms | GA on Claude API, Bedrock, Vertex AI, Azure |

- *Source*: [Build with Claude Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

---

### Citations

- **Removed Sonnet 3.7 warning**: The specific warning advising users to add explicit citation instructions when using Claude Sonnet 3.7 (e.g., "Use citations to back up your answer.") has been removed from the citations documentation.
- *Source*: [Citations](https://platform.claude.com/docs/en/build-with-claude/citations.md)

---

### Streaming Error Recovery

- Documentation reorganized into two sections with explicit version targeting:
  - **Claude 4.5 and earlier**: Resume streaming from where it was interrupted using a continuation request.
  - **Claude 4.6**: Add a user message instructing the model to continue: "Your previous response was interrupted and ended with [previous_response]. Continue from where you left off."

- *Source*: [Streaming](https://platform.claude.com/docs/en/build-with-claude/streaming.md)

---

### Search Results

- **Sonnet 4.6 added** to supported models list.
- *Source*: [Search Results](https://platform.claude.com/docs/en/build-with-claude/search-results.md)

---

### Context Editing

- **Sonnet 4.6 added** to supported models list.
- **ZDR note added**: Context editing is a beta feature and is not covered by ZDR.
- *Source*: [Context Editing](https://platform.claude.com/docs/en/build-with-claude/context-editing.md)

---

## Notable Details

- **Prompt caching and ZDR**: The new ZDR note on prompt caching clarifies that only cryptographic hashes and compiled KV cache representations (not raw prompt text) are stored — potentially making prompt caching compatible with ZDR commitments. Developers operating under ZDR contracts should consult Anthropic to confirm.

- **Structured outputs and ZDR**: Schemas are cached up to 24 hours even under ZDR. This is a non-obvious exception to the "no data retained" guarantee that deserves attention in privacy-sensitive applications.

- **Compaction is now ZDR-eligible**: Previously listed as "Not ZDR-eligible" due to beta status, compaction's eligibility clarification reflects its graduation in the ZDR documentation even while it remains behind the `compact-2026-01-12` beta header.

- **Java SDK structured outputs API change**: The `outputConfig(Class<T>)` method was renamed to `outputFormat(Class<T>)`. The beta namespace (`client.beta().messages()`) is replaced with the stable namespace (`client.messages()`). Update any Java code calling the old method name.

- **Interleaved thinking beta header deprecated on Opus 4.6**: The `interleaved-thinking-2025-05-14` header is explicitly marked deprecated and safely ignored on Opus 4.6. On Sonnet 4.6 in manual mode, the header is still required. On third-party platforms (Bedrock, Vertex AI), passing the header to unsupported models causes a request failure.

- **`effort: "max"` remains Opus 4.6 only**: Despite Sonnet 4.6 gaining adaptive thinking and effort parameter support, the `max` effort level is still restricted to Opus 4.6. Requests using `max` on Sonnet 4.6 will return an error.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| structured-outputs.md | Modified | +687/-104 | Sonnet 4.6 GA, beta graduation for Go/Ruby/C#, schema complexity limits, per-SDK tabs |
| claude-on-amazon-bedrock.md | Modified | +220/-2 | Sonnet 4.6 model, C# + Ruby SDK support, bearer token auth, Sonnet 4.6 model ID |
| prompt-engineering/claude-prompting-best-practices.md | Modified | +109/-24 | Sonnet 4.5→4.6 migration guide, updated 4.6 overthinking guidance |
| claude-in-microsoft-foundry.md | Modified | +131/-4 | Java SDK support, Sonnet 4.6, SDK compatibility note |
| claude-on-vertex-ai.md | Modified | +66/-2 | Ruby SDK support, Sonnet 4.6, PHP note |
| extended-thinking.md | Modified | +52/-51 | Sonnet 4.6 added, interleaved thinking per-model clarification, example model updates |
| adaptive-thinking.md | Modified | +16/-8 | Sonnet 4.6 added, softened performance claims, interleaved thinking clarified |
| effort.md | Modified | +18/-9 | Sonnet 4.6 added, recommended effort levels section |
| streaming.md | Modified | +16/-12 | Error recovery split into Claude 4.5 and Claude 4.6 sections |
| prompt-caching.md | Modified | +8/-2 | Sonnet 4.6 pricing + support, ZDR clarification |
| zero-data-retention.md | Modified | +8/-2 | Updated ZDR-eligible/non-eligible tables for multiple features |
| batch-processing.md | Modified | +12/-7 | Sonnet 4.6 pricing, ZDR exclusion note |
| embeddings.md | Modified | +11/-11 | Link text and prose improvements (no functional changes) |
| prompt-engineering/chain-prompts.md | Modified | +11/-11 | Heading style change (#### → **bold**) only |
| extended-thinking-tips.md | Modified | +10/-10 | Wording/voice improvements (no functional changes) |
| skills-guide.md | Modified | +10/-6 | ZDR note added |
| compaction.md | Modified | +5/-0 | Sonnet 4.6 added, ZDR eligibility noted |
| context-editing.md | Modified | +5/-0 | Sonnet 4.6 added, ZDR note |
| context-windows.md | Modified | +4/-4 | Sonnet 4.6 added to 1M context window and context awareness |
| files.md | Modified | +4/-0 | ZDR exclusion note (beta feature) |
| overview.md | Modified | +5/-5 | Tool availability status changes (beta → GA) |
| token-counting.md | Modified | +9/-4 | ZDR eligibility noted, model update in examples |
| working-with-messages.md | Modified | +9/-5 | ZDR note, Sonnet 4.6 prefill deprecation |
| search-results.md | Modified | +1/-0 | Sonnet 4.6 added |
| citations.md | Modified | +4/-11 | Removed Sonnet 3.7 citation warning |
| prompt-engineering/prompt-improver.md | Modified | +5/-5 | Title wording only |
| prompt-engineering/prompt-generator.md | Modified | +5/-5 | Link/prose improvements only |
| multilingual-support.md | Modified | +2/-2 | Prose improvements only |
| administration-api.md | Modified | +1/-1 | Link text improvement only |

---
*Generated from Claude API documentation changes detected on 2026-02-19*
