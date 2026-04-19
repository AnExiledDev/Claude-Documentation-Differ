# Claude API Documentation Changes — 2026-04-19

## Summary

A new "Claude in Amazon Bedrock" integration has been fully documented, replacing what was previously labeled a "research preview." The prior InvokeModel/Converse-based Bedrock integration is now formally designated as legacy. Cross-references across multiple documentation pages have been updated accordingly.

## Significant Changes

### Amazon Bedrock — New Messages API Integration

- **New `claude-in-amazon-bedrock` page**: Documents the new AWS-managed Bedrock endpoint that exposes the Messages API directly at `/anthropic/v1/messages` with SSE streaming — the same request shape used in Anthropic's first-party API.
  > "This guide walks you through setting up and making API calls to Claude in Amazon Bedrock. Claude in Amazon Bedrock runs on AWS-managed infrastructure with zero operator access (Anthropic personnel have no access to the inference infrastructure), letting you build sensitive applications entirely inside the AWS security boundary while using the same Messages API shape you use with Anthropic's first-party API."
  - *Implication*: Developers can now use familiar Anthropic SDK patterns (streaming via SSE, same request body) when targeting Bedrock, rather than using AWS event-stream encoding and ARN model identifiers.
  - *Source*: [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock.md)

- **New endpoint URL pattern**: `https://bedrock-mantle.{region}.api.aws/anthropic/v1/messages`
  - Global endpoint available for Claude Opus 4.7 and Claude Haiku 4.5; Claude Mythos Preview is regional-only (`us-east-1`).
  - Regional endpoints carry a 10% pricing premium over global endpoints.

- **Three new authentication paths** documented:
  1. **Bedrock service role** (recommended): AWS-managed keys via IAM PassRole
  2. **IAM assumed roles**: Identity-federated access, 12-hour maximum session
  3. **Bearer tokens**: Short-term access without IAM roles (12-hour maximum), passed via `x-api-key` header

- **New SDK client classes** (BedrockMantle variants) across all supported SDKs:
  | Language | Install | Client class |
  |----------|---------|--------------|
  | Python | `pip install "anthropic[bedrock]"` | `AnthropicBedrockMantle` |
  | TypeScript | `npm install @anthropic-ai/bedrock-sdk` | `AnthropicBedrockMantle` |
  | C# | `dotnet add package Anthropic.Bedrock` | `AnthropicBedrockMantleClient` |
  | Go | `go get github.com/anthropics/anthropic-sdk-go/bedrock` | `bedrock.NewMantleClient` |
  | Java | `anthropic-java-bedrock:2.20.0` | `BedrockMantleBackend` |
  | PHP | `anthropic-ai/sdk` + `aws/aws-sdk-php` | `Anthropic\Bedrock\MantleClient` |
  | Ruby | `anthropic` + `aws-sdk-core` gems | `Anthropic::BedrockMantleClient` |

  - *Implication*: SigV4 signing requires the dedicated BedrockMantle client. The standard `Anthropic` client can also be used by pointing `base_url` at the Bedrock endpoint, but that path supports bearer-token authentication only.

- **Available models on the new endpoint**:
  | Model | Model ID | Access |
  |-------|----------|--------|
  | Claude Opus 4.7 | `anthropic.claude-opus-4-7` | Open |
  | Claude Haiku 4.5 | `anthropic.claude-haiku-4-5` | Open |
  | Claude Mythos Preview | `anthropic.claude-mythos-preview` | Invitation only (Project Glasswing) |

- **Feature availability** on the new endpoint — supported: Messages API, prompt caching, extended thinking, tool use (client-defined), citations, structured outputs. Not supported: Anthropic-defined tools (Web Search, Web Fetch, Remote MCP, Memory, Files API, Computer Use, Skills, Code Execution), Claude Managed Agents, Message Batches API, `/v1/users` endpoint.

- **Quotas**: Default 2 million input TPM; can be raised to 4 million without additional Anthropic approval. RPM limits are enforced by AWS (contact AWS support for adjustments).

- **Zero data retention (ZDR)** available on request via AWS support.

### Amazon Bedrock — Legacy Integration Relabeled

- **`claude-on-amazon-bedrock.md` renamed to "Claude on Amazon Bedrock (legacy)"**: The InvokeModel/Converse API integration is now officially designated as legacy. The page description updated from "Anthropic's Claude models are now generally available through Amazon Bedrock" to "The legacy Amazon Bedrock integration for Claude models, using InvokeModel and Converse APIs with ARN-versioned model identifiers."
  > "This page covers the legacy Amazon Bedrock integration: the `InvokeModel` and `Converse` APIs with ARN-versioned model identifiers and AWS event-stream encoding. For models available on the Messages-API Bedrock endpoint, see [Claude in Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock)."
  - *Implication*: Developers should plan to migrate to the new Messages-API endpoint for new integrations.
  - *Source*: [Claude on Amazon Bedrock (legacy)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md)

- **Claude Opus 4.7 note updated** in the legacy page: Removed language stating Opus 4.7 was only available "in research preview." Updated to clarify it is now reachable through `InvokeModel` on `bedrock-runtime`, served by the same infrastructure as the new Messages API endpoint. Opus 4.7 remains absent from the legacy ARN model table because it has no ARN-versioned model ID.

### Structured Outputs — Bedrock Availability Update

- **Claude Mythos Preview and Claude Opus 4.7 now listed for Bedrock**: The structured outputs availability note was updated to reflect that both models are available via the new Messages-API Bedrock endpoint. Previously, Claude Opus 4.7 was listed as "in research preview" on Bedrock; Claude Mythos Preview was not mentioned for Bedrock at all.
  > "Claude Opus 4.7 and Claude Mythos Preview are available through [Claude in Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock) (the Messages-API Bedrock endpoint)."
  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

### Link Updates (Cross-Reference Cleanup)

The following pages had internal links updated from `/claude-on-amazon-bedrock` to `/claude-in-amazon-bedrock`:

- **adaptive-thinking.md**: Thinking signature cross-platform compatibility note
- **extended-thinking.md**: Two references — interleaved thinking platform note and signature compatibility note
- **claude-on-vertex-ai.md**: "Claude is also available through..." footer reference

## New Pages

- **claude-in-amazon-bedrock.md** — Full guide for the new Messages API–based Amazon Bedrock integration: authentication (service role, IAM assumed roles, bearer tokens), SDK installation across 7 languages, first-request examples, supported models and features, regional availability table (26 AWS regions), quotas, ZDR, observability, and support contact. [View](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock.md)

## Notable Details

- The new Bedrock integration introduces **"Claude Mythos Preview"** — a model requiring an invitation through [Project Glasswing](https://anthropic.com/glasswing). This is the first documentation reference to this model name; access requires a dedicated AWS account allowlisted by the Bedrock Marketplace team (typically processed within 24 hours).
- The endpoint uses the service name `bedrock-mantle` in both the URL hostname and SigV4 signing: `aws:amz:{region}:bedrock-mantle`. Developers using raw cURL with `--aws-sigv4` must use this service name.
- The `ant` CLI does not support the new Amazon Bedrock endpoint — only cURL or SDKs work.
- The support contact for the new integration is **bedrock-ant-eap@amazon.com**, suggesting the "Early Access Preview" (EAP) program designation persists internally even as the public documentation drops the "research preview" label.
- CloudWatch and CloudTrail observability is built in; Anthropic recommends a 30-day minimum log retention.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| claude-in-amazon-bedrock.md | New | +417 | Full guide for new Messages API–based Bedrock integration |
| claude-on-amazon-bedrock.md | Modified | +9/-7 | Relabeled as "legacy"; updated Claude Opus 4.7 and research preview references |
| extended-thinking.md | Modified | +2/-2 | Updated two links from `claude-on-amazon-bedrock` to `claude-in-amazon-bedrock` |
| adaptive-thinking.md | Modified | +1/-1 | Updated link from `claude-on-amazon-bedrock` to `claude-in-amazon-bedrock` |
| claude-on-vertex-ai.md | Modified | +1/-1 | Updated Bedrock cross-reference link |
| structured-outputs.md | Modified | +1/-1 | Updated Bedrock availability note for Claude Opus 4.7 and Claude Mythos Preview |

---
*Generated from Claude API documentation changes detected on 2026-04-19*
