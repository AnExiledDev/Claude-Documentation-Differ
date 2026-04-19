# Claude API Documentation Changes — 2026-04-19

## Summary

All six SDK documentation pages (Python, TypeScript, Go, Java, Ruby, C#) have been updated to document new "Mantle" client classes for Amazon Bedrock, which use the Messages-API endpoint over SSE rather than the legacy `bedrock-runtime` `InvokeModel` path. The Amazon Bedrock documentation URL was also updated from `claude-on-amazon-bedrock` to `claude-in-amazon-bedrock`, with the old URL now preserved as a legacy link.

## Significant Changes

### SDKs — New Amazon Bedrock Mantle Clients

All SDK documentation now introduces a parallel Bedrock client that targets the Messages-API endpoint (SSE streaming) instead of the `InvokeModel` `bedrock-runtime` path. The existing clients are retained for backward compatibility, and the new Mantle clients are recommended for new projects.

- **Python — `AnthropicBedrockMantle`**: A fourth client class is now documented alongside the existing `AnthropicBedrock`, `AnthropicVertex`, and `AnthropicFoundry`.
  > `All four client classes are included in the base anthropic package`
  > `Use AnthropicBedrockMantle for new projects; AnthropicBedrock remains for existing applications using the Bedrock InvokeModel API.`
  - *Implication*: Python projects starting fresh on Bedrock should import `AnthropicBedrockMantle` instead of `AnthropicBedrock`. Both require `pip install anthropic[bedrock]`.
  - *Source*: [Python SDK](https://platform.claude.com/docs/en/api/sdks/python.md)

- **TypeScript — `AnthropicBedrockMantle`**: `@anthropic-ai/bedrock-sdk` now exposes both `AnthropicBedrockMantle` (new) and `AnthropicBedrock` (legacy `bedrock-runtime` path).
  > `npm install @anthropic-ai/bedrock-sdk: Provides AnthropicBedrockMantle client, and AnthropicBedrock for the bedrock-runtime path`
  > `Use AnthropicBedrockMantle for new projects; AnthropicBedrock remains for existing applications using the Bedrock InvokeModel API.`
  - *Implication*: TypeScript consumers should migrate new code to `AnthropicBedrockMantle`; no package change required.
  - *Source*: [TypeScript SDK](https://platform.claude.com/docs/en/api/sdks/typescript.md)

- **Go — `bedrock.NewMantleClient`**: The Go `bedrock` subpackage now provides `bedrock.NewMantleClient` for the Messages-API endpoint (streams over SSE). The existing `bedrock.WithLoadDefaultConfig` / `bedrock.WithConfig` remain for the `bedrock-runtime` path.
  > `Use bedrock.NewMantleClient for the Messages-API Bedrock endpoint (streams over SSE), or bedrock.WithLoadDefaultConfig(ctx) / bedrock.WithConfig(cfg) (bedrock-runtime path). Importing the bedrock package globally registers a decoder for application/vnd.amazon.eventstream with the SDK's streaming layer (through package init()). This applies whether you use the bedrock-runtime WithConfig/WithLoadDefaultConfig path or NewMantleClient.`
  > `Use bedrock.NewMantleClient for new projects; bedrock.WithLoadDefaultConfig/WithConfig remain for existing applications using the Bedrock InvokeModel API.`
  - *Implication*: The `init()` side-effect that registers the `application/vnd.amazon.eventstream` decoder applies to both client paths, so importing the `bedrock` package is sufficient regardless of which client is used.
  - *Source*: [Go SDK](https://platform.claude.com/docs/en/api/sdks/go.md)

- **Java — `BedrockMantleBackend`**: `com.anthropic:anthropic-java-bedrock` now includes `BedrockMantleBackend.fromEnv()` for the Messages-API endpoint alongside the existing `BedrockBackend`.
  > `Use BedrockMantleBackend.fromEnv() for the Messages-API Bedrock endpoint, or BedrockBackend.fromEnv() / BedrockBackend.builder() (bedrock-runtime path).`
  > `Use BedrockMantleBackend for new projects; BedrockBackend remains for existing applications using the Bedrock InvokeModel API.`
  - *Implication*: Pass `BedrockMantleBackend` via `.backend()` on `AnthropicOkHttpClient.builder()` for new Java integrations.
  - *Source*: [Java SDK](https://platform.claude.com/docs/en/api/sdks/java.md)

- **Ruby — `Anthropic::BedrockMantleClient`**: The Ruby SDK adds `Anthropic::BedrockMantleClient`, which requires the `aws-sdk-core` gem (lighter-weight dependency than `aws-sdk-bedrockruntime` required by `Anthropic::BedrockClient`).
  > `Anthropic::BedrockMantleClient, or Anthropic::BedrockClient for the bedrock-runtime path. Anthropic::BedrockMantleClient requires the aws-sdk-core gem; Anthropic::BedrockClient requires the aws-sdk-bedrockruntime gem.`
  > `Use Anthropic::BedrockMantleClient for new projects; Anthropic::BedrockClient remains for existing applications using the Bedrock InvokeModel API.`
  - *Implication*: New Ruby projects on Bedrock can use the lighter `aws-sdk-core` dependency instead of the full `aws-sdk-bedrockruntime`.
  - *Source*: [Ruby SDK](https://platform.claude.com/docs/en/api/sdks/ruby.md)

- **C# — `AnthropicBedrockMantleClient`**: `Anthropic.Bedrock` NuGet package now exposes `AnthropicBedrockMantleClient` (takes an optional `MantleAwsClientOptions` config) alongside the existing `AnthropicBedrockClient` (accepts `AnthropicBedrockCredentialsHelper.FromEnv()` or explicit credentials).
  > `Use AnthropicBedrockMantleClient for the Messages-API Bedrock endpoint, or AnthropicBedrockClient (bedrock-runtime path). AnthropicBedrockMantleClient takes an optional MantleAwsClientOptions config object; AnthropicBedrockClient accepts AnthropicBedrockCredentialsHelper.FromEnv() or explicit credentials.`
  > `Use AnthropicBedrockMantleClient for new projects; AnthropicBedrockClient remains for existing applications using the Bedrock InvokeModel API.`
  - *Implication*: No new NuGet package is needed; `AnthropicBedrockMantleClient` ships in the existing `Anthropic.Bedrock` package.
  - *Source*: [C# SDK](https://platform.claude.com/docs/en/api/sdks/csharp.md)

### Documentation — Amazon Bedrock URL Updated

- **Bedrock docs URL renamed**: The canonical Amazon Bedrock guide URL changed from `claude-on-amazon-bedrock` to `claude-in-amazon-bedrock` across the API overview, client SDKs reference, and all six SDK pages. The old URL is now listed as a legacy link in SDK platform notes.
  > Before: `[Amazon Bedrock](/docs/en/build-with-claude/claude-on-amazon-bedrock)`
  > After: `[Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock)` + `[Amazon Bedrock (legacy)](/docs/en/build-with-claude/claude-on-amazon-bedrock)`
  - *Implication*: Any internal links or bookmarks pointing to `claude-on-amazon-bedrock` may need updating; the legacy link suggests a redirect is still in place but the new URL is canonical.
  - *Source*: [API Overview](https://platform.claude.com/docs/en/api/overview.md), [Client SDKs](https://platform.claude.com/docs/en/api/client-sdks.md)

## Notable Details

- The "Mantle" naming appears consistently across all SDKs, suggesting this is a coordinated platform feature name for the Messages-API Bedrock endpoint (as distinct from the lower-level `InvokeModel` / `bedrock-runtime` interface).
- Go SDK received two minor wording edits unrelated to the Mantle feature: "simply be its zero value" → "be its zero value" and "easily wraps" → "wraps" in the file upload helper description. These are editorial-only changes.
- The Ruby `BedrockMantleClient` dependency on `aws-sdk-core` instead of `aws-sdk-bedrockruntime` is significant: `aws-sdk-core` is a much smaller transitive dependency, indicating Mantle bypasses the lower-level Bedrock runtime interface at the SDK level too.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `sdks/python.md` | Modified | +7/-3 | Added `AnthropicBedrockMantle` client; updated count from 3 to 4 client classes; updated Bedrock doc URL |
| `sdks/go.md` | Modified | +7/-4 | Added `bedrock.NewMantleClient`; expanded Bedrock subpackage docs; updated Bedrock doc URL; minor wording fixes |
| `sdks/java.md` | Modified | +7/-4 | Added `BedrockMantleBackend`; updated Bedrock doc URL |
| `sdks/csharp.md` | Modified | +6/-3 | Added `AnthropicBedrockMantleClient` with `MantleAwsClientOptions`; updated Bedrock doc URL |
| `sdks/typescript.md` | Modified | +5/-2 | Added `AnthropicBedrockMantle` to `@anthropic-ai/bedrock-sdk`; updated Bedrock doc URL |
| `sdks/ruby.md` | Modified | +5/-2 | Added `Anthropic::BedrockMantleClient` with `aws-sdk-core` dependency; updated Bedrock doc URL |
| `api/client-sdks.md` | Modified | +1/-1 | Updated Amazon Bedrock link URL |
| `api/overview.md` | Modified | +1/-1 | Updated Amazon Bedrock link URL |

---
*Generated from Claude API documentation changes detected on 2026-04-19*
