# Claude API Documentation Changes - February 7, 2026

## TL;DR

Major SDK documentation overhaul with 7 new dedicated SDK pages (Python, TypeScript, Java, Go, Ruby, C#, PHP), expanded code examples across all SDKs for batch processing, files API, structured outputs, and platform integrations (Bedrock, Vertex AI). The documentation now provides comprehensive multi-language support with SDK-specific features and best practices.

## SDK Documentation Restructure

The most significant change is a complete reorganization of SDK documentation from a single page to dedicated pages for each language.

### New SDK Pages

Seven new dedicated SDK documentation pages were added, each with comprehensive SDK-specific features:

- **[Python SDK](/docs/en/api/sdks/python.md)**: Sync/async client support, Pydantic integration, platform extras (`anthropic[bedrock]`, `anthropic[vertex]`)
- **[TypeScript SDK](/docs/en/api/sdks/typescript.md)**: Node.js, Deno, Bun, and browser support
- **[Java SDK](/docs/en/api/sdks/java.md)**: Builder pattern, CompletableFuture async, structured outputs with annotations
- **[Go SDK](/docs/en/api/sdks/go.md)**: Context-based cancellation, functional options
- **[Ruby SDK](/docs/en/api/sdks/ruby.md)**: Sorbet types, streaming helpers
- **[C# SDK](/docs/en/api/sdks/csharp.md)**: .NET Standard 2.0+, **IChatClient integration**
- **[PHP SDK](/docs/en/api/sdks/php.md)**: Value objects, builder pattern

The main [Client SDKs page](/docs/en/api/client-sdks.md) now serves as a landing page with quick installation, quick start examples, and platform support matrix.

### SDK Version Updates

- **Java SDK**: Updated from `2.10.0` to `2.11.1`
- **Go SDK**: Version `v1.19.0` noted in documentation
- **Python**: Now requires 3.9+ (previously 3.8+)
- **C# SDK**: Major version jump - now at v10+ (official SDK, replacing community `tryAGI.Anthropic`)

> **C# Breaking Change**: The `Anthropic` package is now the official Anthropic SDK for C#. Package versions 3.X and below were previously used for the tryAGI community-built SDK, which has moved to `tryAGI.Anthropic`. If you need to continue using the former client in your project, update your package reference to `tryAGI.Anthropic`.

## New SDK Features

### C# IChatClient Integration

The C# SDK now implements Microsoft's `IChatClient` interface from `Microsoft.Extensions.AI.Abstractions`, enabling integration with MCP (Model Context Protocol) tools:

```csharp
using Anthropic;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;

IChatClient chatClient = client.AsIChatClient("claude-opus-4-6")
    .AsBuilder()
    .UseFunctionInvocation()
    .Build();

// Using McpClient from the MCP C# SDK
McpClient learningServer = await McpClient.CreateAsync(
    new HttpClientTransport(new() { Endpoint = new("https://learn.microsoft.com/api/mcp") }));

ChatOptions options = new() { Tools = [.. await learningServer.ListToolsAsync()] };

Console.WriteLine(await chatClient.GetResponseAsync("Tell me about IChatClient", options));
```

This is a significant integration point for .NET developers working with AI orchestration frameworks.

### Java Structured Outputs

The Java SDK documentation now highlights class-based structured outputs with the `outputConfig()` method:

```java
class ContactInfo {
    public String name;
    public String email;
    public String planInterest;
}

StructuredMessageCreateParams<ContactInfo> createParams = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_6)
    .outputConfig(ContactInfo.class)
    .addUserMessage("...")
    .build();
```

The SDK automatically generates JSON schemas from Java classes, with support for annotations and local schema validation.

## Multi-Language Code Examples

All major feature documentation pages now include code examples for **all 7 SDKs**. This is a massive expansion from the previous Python/TypeScript-only examples.

### Batch Processing

Added code examples for Go, Ruby, C#, and PHP to the [batch processing documentation](/docs/en/build-with-claude/batch-processing.md). All SDKs now have parity for batch API usage.

### Files API

Comprehensive multi-language examples added for:
- File upload (7 languages)
- Using files in messages (7 languages)

Each SDK shows idiomatic patterns:
- **Java**: `Path.of()` for file handling
- **Go**: `os.Open()` with deferred cleanup
- **Ruby**: `File.open()` with binary mode
- **C#**: `File.OpenRead()` for async streams
- **PHP**: `fopen()` with resource handles

### Structured Outputs

The [structured outputs documentation](/docs/en/build-with-claude/structured-outputs.md) now includes examples for all SDKs, with a new section on SDK-specific helpers:

> #### Using native schema definitions
>
> Instead of writing raw JSON schemas, you can use familiar schema definition tools in your language. Each SDK provides class-based or library-based schema support:
>
> - **Python**: Pydantic models
> - **TypeScript**: Zod schemas
> - **Java**: Plain Java classes with annotation support
> - **Ruby**: `Anthropic::BaseModel` classes

Previously titled "Using Pydantic and Zod", this section now acknowledges the multi-language nature of the SDK ecosystem.

### Vision API

Added Go code examples to the [vision documentation](/docs/en/build-with-claude/vision.md), including both base64-encoded images and URL-based images.

## Platform Integration Updates

### Amazon Bedrock

Enhanced [Bedrock documentation](/docs/en/build-with-claude/claude-on-amazon-bedrock.md) with:
- Java and Go installation instructions and code examples
- Support for both global and regional (CRIS) endpoints across all SDKs
- Updated Maven/Gradle dependencies for Java Bedrock integration (`anthropic-java-bedrock:2.13.0`)

Example showing regional endpoint usage:

```java
// Using US regional endpoint (CRIS)
var message = client.messages().create(MessageCreateParams.builder()
    .model("us.anthropic.claude-opus-4-6-v1")  // Regional prefix
    .maxTokens(256)
    .addUserMessage("Hello, world")
    .build());
```

### Google Vertex AI

The [Vertex AI documentation](/docs/en/build-with-claude/claude-on-vertex-ai.md) now includes:
- Java and Go setup instructions with platform-specific backends
- Maven dependency: `anthropic-java-vertex:2.13.0`
- Examples of using Google Cloud credentials with both global and regional endpoints
- Cross-reference to Amazon Bedrock and Microsoft Foundry

Currently, the Vertex backend **does not support the Anthropic Batch API**.

## Documentation Style Updates

Several subtle documentation improvements worth noting:

### Recommendation Language Softening

The documentation has been updated to use less prescriptive language:

- Vision: "we recommend resizing" → "resize" (more direct)
- Vision: "we recommend an image-then-text structure" → "prefer an image-then-text structure"
- Vision: "our API" → "the API" (less possessive)

This suggests a shift toward more neutral, developer-friendly documentation tone.

### Citation Example Update

Minor model update in the [citations documentation](/docs/en/build-with-claude/citations.md):
- Changed from `Model.CLAUDE_SONNET_4_20250514` to `Model.CLAUDE_OPUS_4_6` in the Java example

This indicates that examples are being standardized to use Claude Opus 4.6 as the default model across documentation.

## Platform Support Matrix

The reorganized SDK documentation now includes a clear platform support table:

| Platform | Description |
|----------|-------------|
| Claude API | Connect directly to Claude API endpoints |
| Amazon Bedrock | Use Claude through AWS |
| Google Vertex AI | Use Claude through Google Cloud |
| Microsoft Foundry | Use Claude through Microsoft Azure |

All SDKs support multiple deployment options, with platform-specific setup instructions on individual SDK pages.

## Beta Features Access

All SDK pages now document how to access beta features through the `beta` namespace, with consistent examples across languages:

```python
# Python
message = client.beta.messages.create(
    betas=["feature-name"]
)
```

```java
// Java
client.beta().messages().create(params);
```

```go
// Go
client.Beta.Messages.New(ctx, params)
```

The documentation emphasizes that beta features are available across all SDKs with consistent patterns.

## Hidden Gems

### Jackson Compatibility Checking (Java)

The Java SDK documentation reveals a Jackson version compatibility checker that throws exceptions at runtime if an incompatible version is detected:

> The SDK depends on Jackson for JSON serialization/deserialization. It is compatible with version 2.13.4 or higher, but depends on version 2.18.2 by default.
>
> The SDK throws an exception if it detects an incompatible Jackson version at runtime (e.g. if the default version was overridden in your Maven or Gradle config).

This can be disabled via `checkJacksonVersionCompatibility`, though it's not recommended.

### ProGuard/R8 Support (Java)

The Java SDK ships with ProGuard/R8 keep rules for mobile development:

> Although the SDK uses reflection, it is still usable with ProGuard and R8 because `anthropic-java-core` is published with a configuration file containing keep rules.

### PHP Named Parameters

PHP SDK requires named parameters for optional arguments:

> This library uses named parameters to specify optional arguments. Parameters with a default value must be set by name.

This is a modern PHP 8.1+ pattern that improves API clarity.

### C# Response Validation

The C# SDK includes optional upfront response validation:

```csharp
// Validate response structure immediately
var message = await client.Messages.Create(parameters);
message.Validate();

// Or configure globally
AnthropicClient client = new() { ResponseValidation = true };
```

By default, the SDK only throws `AnthropicInvalidDataException` when you directly access properties, but you can opt into eager validation.

## SDK-Specific Error Handling

Each SDK now documents its exception hierarchy:

**C#**:
- `AnthropicApiException` base class with HTTP status-specific subclasses
- `AnthropicSseException` for streaming errors
- `AnthropicInvalidDataException` for malformed responses

**PHP**:
- `APIException` base class
- Status-specific exceptions (400 → `BadRequestException`, 429 → `RateLimitException`, etc.)
- `APIConnectionException` for network errors
- `APITimeoutException` for timeouts

**Java**:
- Unchecked exceptions only (explicitly avoided checked exceptions due to "widely considered a mistake")
- FAQ section explaining the design decision

## Requirements Summary

Updated minimum version requirements across SDKs:

| SDK | Minimum Version | Notes |
|-----|-----------------|-------|
| Python | 3.9+ | Previously 3.8+ |
| TypeScript | 4.9+ (Node.js 20+) | |
| Java | 8+ | |
| Go | 1.22+ | |
| Ruby | 3.2.0+ | |
| C# | .NET Standard 2.0 | Wide compatibility |
| PHP | 8.1.0+ | |

## Technical Details

### Auto-Pagination

Both C# and PHP SDKs document auto-pagination support:

**C#**:
```csharp
var page = await client.Beta.Messages.Batches.List(parameters);
await foreach (var item in page.Paginate())
{
    Console.WriteLine(item);
}
```

**PHP**:
```php
foreach ($page->pagingEachItem() as $item) {
    var_dump($item->id);
}
```

### Retries Configuration

All SDKs default to **2 retries** with exponential backoff for:
- Connection errors
- 408 Request Timeout
- 409 Conflict
- 429 Rate Limit
- 5xx Internal Server errors

Retries are configurable per-client or per-request.

### Timeouts

Most SDKs default to **10 minutes** for request timeouts (C# specifically documented). This is quite generous and designed for long-running operations like batch processing.

## Documentation Organization

The reorganization creates a clear information hierarchy:

1. **Main SDK page**: Quick start, installation, platform support overview
2. **Individual SDK pages**: Deep dives into SDK-specific features, error handling, advanced usage
3. **Feature pages**: Multi-language code examples for each API feature

This structure makes it much easier to find language-specific information while maintaining cross-SDK consistency in the feature documentation.

## Additional Resources

All new SDK pages link to:
- GitHub repositories
- Language-specific package registries (NuGet, Packagist, Javadocs, etc.)
- API reference
- Streaming guide
- Tool use guide (where relevant)

---

*Generated from Claude API documentation changes detected on February 7, 2026*
