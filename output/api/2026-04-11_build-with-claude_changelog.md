# Claude API Documentation Changes — 2026-04-11

## Summary

A new research preview page documents a second Amazon Bedrock integration that exposes the Messages API directly at `/anthropic/v1/messages` with AWS-native authentication. The structured outputs page received a substantial overhaul covering new TypeScript and PHP SDK helper patterns, updated Java SDK idioms, and C# API surface changes. Smaller updates add the Advisor tool to platform overview tables and tighten the `custom_id` validation spec for batch requests.

---

## Significant Changes

### New: Claude in Amazon Bedrock (Research Preview)

- **New Bedrock endpoint with Messages API shape**: A second Bedrock integration is documented, distinct from the existing `InvokeModel`/`Converse` path. The new endpoint exposes the Messages API at `https://bedrock-mantle.{region}.api.aws/anthropic/v1/messages` with standard SSE streaming.
  > "This guide walks you through setting up and making API calls to Claude in Amazon Bedrock. Claude in Amazon Bedrock runs on AWS-managed infrastructure with zero operator access (Anthropic personnel have no access to the inference infrastructure)."
  - *Implication*: Developers can now use the same request/response shape as the first-party API, including prompt caching, extended thinking, tool use, citations, and structured outputs, entirely inside the AWS security boundary.
  - *Source*: [Claude in Amazon Bedrock (research preview)](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock-research-preview.md)

- **Three authentication paths**: Bedrock service role (recommended), IAM assumed roles (12-hour max), and bearer tokens (12-hour max, least preferred). SigV4 signing requires the dedicated `AnthropicBedrockMantle` client; the standard `Anthropic` client can be pointed at the new base URL but supports bearer tokens only.

- **New dedicated SDK clients**: Each SDK gets a new Bedrock Mantle client class.

  | SDK | Package / Import | Client class |
  |-----|-----------------|--------------|
  | Python | `anthropic[bedrock]` | `AnthropicBedrockMantle` |
  | TypeScript | `@anthropic-ai/bedrock-sdk` | `AnthropicBedrockMantle` |
  | C# | `Anthropic.Bedrock` | `AnthropicBedrockMantleClient` |
  | Go | `github.com/anthropics/anthropic-sdk-go/bedrock` | `bedrock.NewMantleClient()` |
  | Java | `com.anthropic:anthropic-java-bedrock:2.20.0` | `BedrockMantleBackend.fromEnv()` |
  | PHP | `anthropic-ai/sdk` + `aws/aws-sdk-php` | `MantleClient` |
  | Ruby | `anthropic` + `aws-sdk-core` gems | `Anthropic::BedrockMantleClient` |

- **Supported models in research preview**:

  | Model | Model ID |
  |-------|----------|
  | Claude Mythos Preview | `anthropic.claude-mythos-preview` |
  | Claude Haiku 4.5 | `anthropic.claude-haiku-4-5` |

- **Region and quota**: Available in `us-east-1` only. Default quota is 2 million input TPM; up to 4 million TPM available without additional Anthropic approval. Requires account allowlisting via your Anthropic account executive.

- **Features not supported on this endpoint**: Anthropic-defined tools (Web Search, Web Fetch, Remote MCP, Memory, Files API, Computer Use, Skills, Code Execution), Claude Managed Agents, Message Batches API, and `/v1/users`.

---

### Structured Outputs — SDK Updates

The structured outputs page was significantly revised (+756/−518 lines) across multiple SDK sections.

- **TypeScript: New `jsonSchemaOutputFormat()` helper**: A new path for structured outputs without Zod. Accepts a raw JSON Schema object and integrates with `client.messages.parse()`. For inline schema literals declared with `as const`, the inferred TypeScript type of `parsed_output` matches the schema structure at compile time.
  > "The `jsonSchemaOutputFormat()` helper accepts a JSON Schema object and integrates it with `parse()` without requiring Zod. Zod is an optional peer dependency you install separately; `jsonSchemaOutputFormat()` works out of the box because the SDK bundles `json-schema-to-ts` directly."
  > "For **inline schema literals** (declared with `as const` in your source), you also get compile-time type inference... For **imported or generated schemas** (from a JSON file or OpenAPI codegen), the helper still sends the schema and parses the response, but the inferred type is `unknown`."
  - Import path: `@anthropic-ai/sdk/helpers/json-schema`
  - Supports `{ transform: false }` option to send the schema unchanged without the SDK's normalization pass.
  - *Implication*: Developers can get type-safe structured outputs in TypeScript without adding Zod as a dependency.
  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **PHP: Class-based schema derivation replaces raw JSON schemas**: The PHP SDK now supports a `StructuredOutputModel` interface (plus `StructuredOutputModelTrait`) that derives a JSON Schema from native PHP 8 property types. The `$message->parsedOutput()` method returns a typed class instance.
  > "Define a PHP class implementing `StructuredOutputModel` (using `StructuredOutputModelTrait`) and pass the class name to `outputConfig: ['format' => MyClass::class]`. The SDK derives a JSON schema from your native PHP 8 property types and returns a typed instance via `$message->parsedOutput()`."
  - Constraints can be added via the `#[Constrained]` attribute (e.g., `description`, `minimum`, `maximum`, `format`, `itemClass`, `minItems`).
  - Raw JSON schema via `OutputConfig::with()` remains available as a fallback for schemas PHP type hints cannot express.
  - *Implication*: PHP developers can now use class-based schema definition instead of manually building JSON schema arrays.
  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **Java SDK: Class requirements and API changes**:
  - Schema classes must be declared as top-level classes or `static` nested classes. Non-static inner classes cannot be instantiated by Jackson Databind.
    > "Declare your schema classes as top-level classes or `static` nested classes. This requirement comes from the Jackson Databind library (`com.fasterxml.jackson.databind`), which the SDK uses to deserialize JSON responses into your class instances and cannot instantiate non-static inner classes."
  - Result access changed: `response.content().get(0).asText().text()` → `response.content().stream().flatMap(block -> block.text().stream()).findFirst().orElseThrow().text()`
  - Streaming: `BetaMessageAccumulator` renamed to `MessageAccumulator`; `BetaMessage` renamed to `Message` in the streaming accumulation flow.
  - New documentation sections: **Composition and inheritance** (composition yields nested JSON; inheritance yields flat JSON) and **Defining schemas without a Java class** using the `JsonOutputFormat.Schema` builder.
  - Examples updated to JDK 25 compact source file syntax (`void main()` instead of `public class Foo { public static void main(String[] args) {} }`).
  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **C# SDK: `TryPickText()` replaces direct cast**: Content block access changed from `(response.Content.First().Value as TextBlock)!.Text` to `response.Content[0].TryPickText(out var textBlock)`. Model string literals replaced by typed constants (e.g., `Model.ClaudeOpus4_6`).
  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **Go SDK**: `map[string]interface{}` replaced with `map[string]any` (idiomatic Go since 1.18).

- **Cross-SDK clarification on `output_format` backward compatibility**:
  > "The Python SDK's `client.messages.parse()` still accepts `output_format` as a convenience parameter and translates it to `output_config.format` internally. Other SDKs require `output_config` directly."
  - *Implication*: Only the Python SDK maintains the `output_format` compatibility alias; other SDK users must use `output_config`.

---

### New Tool: Advisor Tool

- **Advisor tool added to platform overview and ZDR tables**: The Advisor tool is now listed in the server-side built-in tools table on the overview page and in the API/data retention ZDR eligibility table.
  > "Pair a faster executor model with a higher-intelligence advisor model that provides strategic guidance mid-generation for long-horizon agentic workloads."
  - ZDR: eligible. HIPAA: not eligible. Availability: Claude API (beta).
  - *Implication*: The Advisor tool is now an officially documented beta server-side tool available via `/v1/messages` with the `advisor` tool type.
  - *Source*: [Build with Claude Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md), [API and Data Retention](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention.md)

---

### Batch Processing — `custom_id` Validation Constraints

- **`custom_id` format requirement now explicit**: The documentation previously described `custom_id` only as "unique." It now specifies the full validation rule.
  > "A unique `custom_id` for identifying the Messages request. Must be 1 to 64 characters and contain only alphanumeric characters, hyphens, and underscores (matching `^[a-zA-Z0-9_-]{1,64}$`)."
  - *Implication*: Callers using `custom_id` values with spaces, dots, slashes, or other special characters may already be receiving validation errors; this documents the constraint explicitly.
  - *Source*: [Batch Processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing.md)

---

### Amazon Bedrock Cross-Reference Fixes

- **`claude-on-amazon-bedrock.md`**: The existing Bedrock integration is no longer labeled "legacy." The note now reads "the Amazon Bedrock integration available today" and links to the new research preview page for the Messages API path.
  - *Source*: [Claude on Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md)

- **`claude-on-vertex-ai.md`**: Fixed a broken cross-platform link that was pointing to the non-existent `/docs/en/build-with-claude/claude-in-amazon-bedrock` path; corrected to `/docs/en/build-with-claude/claude-on-amazon-bedrock`.
  - *Source*: [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

---

## New Pages

- **`claude-in-amazon-bedrock-research-preview.md`** — Full setup guide for the new AWS-managed Messages API endpoint in Amazon Bedrock. Covers prerequisites, three authentication paths (service role, IAM assumed roles, bearer tokens), SDK installation, first-request examples in 7 languages, supported models, feature availability, quotas, data retention, and observability. [View](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock-research-preview.md)

---

## Notable Details

- The new Bedrock endpoint uses standard SSE streaming, unlike the `InvokeModel` AWS event-stream encoding used by the existing integration. This means existing streaming code written for the first-party API can be reused with minimal changes.
- The research preview model `anthropic.claude-mythos-preview` corresponds to [Project Glasswing](https://anthropic.com/glasswing). The model ID carries an `anthropic.` provider prefix per the new Bedrock naming convention.
- The Java SDK structured outputs streaming accumulator rename from `BetaMessageAccumulator` → `MessageAccumulator` (and `BetaMessage` → `Message`) indicates the Java streaming accumulation API has moved out of beta.
- PHP's `#[Constrained]` attribute distinguishes between API-enforced constraints (sent in the JSON schema wire format) and SDK-validated constraints (stripped from the wire schema, appended to description text, and validated client-side against the response).

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `claude-in-amazon-bedrock-research-preview.md` | New | +381 | Research preview guide for Messages API on Bedrock with AWS-native auth |
| `structured-outputs.md` | Modified | +756/−518 | New TS `jsonSchemaOutputFormat()` helper; PHP class-based schema derivation; Java static class requirement, streaming rename, composition/inheritance docs; C# `TryPickText()` |
| `overview.md` | Modified | +1/−0 | Added Advisor tool to built-in tools table |
| `api-and-data-retention.md` | Modified | +1/−0 | Added Advisor tool to ZDR/HIPAA eligibility table |
| `batch-processing.md` | Modified | +1/−1 | Explicit `custom_id` character set and length constraints |
| `claude-on-amazon-bedrock.md` | Modified | +1/−1 | Updated note to remove "legacy" label; link to new research preview page |
| `claude-on-vertex-ai.md` | Modified | +1/−1 | Fixed cross-platform Bedrock link |
| `compaction.md` | Modified | +3/−1 | Code formatting only (template literal line break) |
| `context-editing.md` | Modified | +3/−1 | Code formatting only (template expression line break) |

---

*Generated from Claude API documentation changes detected on 2026-04-11*
