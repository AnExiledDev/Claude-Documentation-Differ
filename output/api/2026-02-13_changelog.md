# Claude API Documentation Changes - February 13, 2026

## TL;DR

Major SDK expansion with **42 new C# documentation pages** covering the complete Claude API surface. The `output_format` parameter is now deprecated in favor of `output_config.format` for structured outputs. Fast mode is officially documented as a beta feature for high-throughput inference. Adaptive thinking replaces the previous extended thinking configuration in Claude Opus 4.6.

## SDK Updates

### **C# SDK - Full Documentation Launch** 🎉

The C# SDK now has complete, production-ready documentation across all major API modules:

**New documentation pages (42 total):**
- Messages API (create, count tokens)
- Models API (list, retrieve)
- Files API (upload, download, delete, list, retrieve metadata)
- Batch Processing API (create, cancel, delete, list, results, retrieve)
- Skills API (create, delete, list, retrieve, version management)

> The C# SDK provides type-safe classes for all requests and responses with async support via `CancellationToken` parameters.

**Key C# SDK Features:**
- Readonly collections using `IReadOnlyList<T>` for immutability
- Comprehensive error handling with specific exception types (`BetaApiError`, `BetaAuthenticationError`, `BetaRateLimitError`, etc.)
- Support for rich content types (text, images, PDFs, documents)
- Cursor-based pagination across list endpoints
- Full beta feature access via header configuration

**Beta features available in C#:**
- Message batches, prompt caching, computer use, PDF support
- Token counting, token-efficient tools, output 128k
- Files API, MCP client support, code execution
- Extended cache TTL, 1M context window, skills
- Fast mode (2026-02-01)

### Python SDK - Enhanced Documentation

Significant documentation improvements across Python SDK examples:
- More concise code samples with improved formatting
- Updated batch processing examples with clearer type hints
- Enhanced structured outputs documentation
- Better error handling patterns

### SDK Example Cleanup

**Removed:** Over 1,000 lines of redundant "Example" sections across all SDK docs (Go, Java, Ruby, TypeScript), streamlining documentation for better readability.

## API Changes

### **Structured Outputs - Parameter Migration**

The `output_format` parameter is now officially deprecated:

```python
# Before (deprecated)
response = client.messages.create(
    output_format={"type": "json_schema", "schema": {...}},
    # ...
)

# After (recommended)
response = client.messages.create(
    output_config={"format": {"type": "json_schema", "schema": {...}}},
    # ...
)
```

> Body param: Deprecated: Use `output_config.format` instead. See [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

**Why this matters:** The new `output_config` parameter provides a more extensible structure for controlling output behavior, including the new `effort` parameter for Opus 4.6.

### **Fast Mode - Now Documented** ⚡

Fast mode is now officially documented as a beta feature for high-throughput inference:

```python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    speed="fast",  # New parameter
    betas=["fast-mode-2026-02-01"],
    messages=[{"role": "user", "content": "Refactor this module..."}],
)
```

> Body param: The inference speed mode for this request. `"fast"` enables high output-tokens-per-second inference.

**Model descriptions updated:**
- Claude Haiku 4.5: "Fastest and most compact model for near-instant responsiveness"
- Claude Sonnet 4: "Hybrid model, capable of near-instant responses and extended thinking"

### **Message Turns - Automatic Combining**

New documentation clarifies automatic message turn combining:

> Our models are trained to operate on alternating `user` and `assistant` conversational turns. When creating a new `Message`, you specify the prior conversational turns with the `messages` parameter, and the model then generates the next `Message` in the conversation. Consecutive `user` or `assistant` turns in your request will be combined into a single turn.

**Developer impact:** You no longer need to manually merge consecutive messages from the same role—Claude does this automatically.

## Model Updates

### **Claude Opus 4.6 - Adaptive Thinking**

Adaptive thinking replaces the previous extended thinking configuration:

```python
# Before (Claude Opus 4.5)
response = client.beta.messages.create(
    model="claude-opus-4-5",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 32000},
    betas=["interleaved-thinking-2025-05-14"],
    messages=[...],
)

# After (Claude Opus 4.6)
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},  # Simplified
    output_config={"effort": "high"},  # New parameter
    messages=[...],
)
```

**Breaking changes in Opus 4.6:**
- Cannot use `temperature` and `top_p` simultaneously (choose one)
- Text editor tool updated: `text_editor_20250124` → `text_editor_20250728`
- Tool name changed: `str_replace_editor` → `str_replace_based_edit_tool`

### **Extended Thinking Model Descriptions**

Model documentation now explicitly mentions thinking capabilities:

- Claude Opus 4.6: "High-performance model with extended thinking"
- Claude Sonnet 4.5: "High-performance model with extended thinking"
- Claude Opus 4.1: "High-performance model with early extended thinking"

> Configuration for enabling Claude's extended thinking. See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

## Beta Headers

### **Web Fetch Beta Header Removed**

The `anthropic-beta: web-fetch-2025-09-10` header has been removed from documentation examples, suggesting web fetch may have graduated from beta or changed implementation.

### **Active Beta Features**

Updated list of beta features accessible via the `betas` option:
- `fast-mode-2026-02-01` (new)
- `interleaved-thinking-2025-05-14`
- `prompt-caching-2024-07-31`
- `computer-use-2025-01-24`
- `pdf-support-2024-09-25`
- `token-counting-2024-11-01`
- `message-batches-2024-09-24`
- And 10+ more...

## Documentation Improvements

### **Use Case Guides - Code Quality**

Extensive cleanup of use case guide examples:
- **Content moderation:** Improved Python formatting, better list comprehensions
- **Customer support chat:** Enhanced prompt examples with clearer structure
- **Legal summarization:** Updated code samples with modern Python syntax
- **Ticket routing:** Added evaluation best practices

### **Prompt Library - Consistency**

All 50+ prompt library examples updated with:
- Consistent code formatting across Python examples
- Proper use of environment variable defaults: `# defaults to os.environ.get("ANTHROPIC_API_KEY")`
- Better inline comments and documentation
- Standardized import statements

### **Agent SDK Documentation**

Major overhaul of Agent SDK docs with:
- Enhanced Python and TypeScript v2 preview examples
- Improved documentation of cost tracking, custom tools, file checkpointing
- Better MCP (Model Context Protocol) integration guidance
- Clearer migration guides and hosting instructions

### **Tool Use Documentation**

Comprehensive updates to tool use guides:
- Bash tool, code execution, computer use tool refreshed
- Fine-grained tool streaming documentation enhanced
- Memory tool simplified (16 lines removed, clearer examples)
- Text editor, web fetch, and web search tools updated

## Migration Guidance

### **Sonnet 4.5 Migration**

```python
# From Sonnet 4
model = "claude-sonnet-4-20250514"      # Before
model = "claude-sonnet-4-5-20250929"    # After

# From Sonnet 3.7
model = "claude-3-7-sonnet-20250219"    # Before
model = "claude-sonnet-4-5-20250929"    # After
```

**Pricing:** Sonnet 4.5 is $3 per million input tokens, $15 per million output tokens.

### **Haiku 4.5 Migration**

```python
# From Haiku 3.5
model = "claude-3-5-haiku-20241022"     # Before
model = "claude-haiku-4-5-20251001"     # After
```

**Note:** Haiku 4.5 has separate rate limits from Haiku 3.5. Review the [rate limits documentation](/docs/en/api/rate-limits).

## Deprecations & Breaking Changes

### **Model Retirements**

Updated deprecation timeline table with consistent formatting. No new model retirements announced in this update.

**Accessing usage audit:**
- Path updated: Go to [Usage](/usage) page (previously `/settings/usage`)
- Export CSV to review usage by API key and model

### **Text Editor Tool Update**

If using the text editor tool, update to the latest version:

```python
# Before
tools = [{"type": "text_editor_20250124", "name": "str_replace_editor"}]

# After
tools = [{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}]
```

See [Text editor tool documentation](/docs/en/agents-and-tools/tool-use/text-editor-tool) for migration details.

## Technical Details

### **Output Config Parameter Structure**

The new `output_config` parameter supports multiple configuration options:

```python
output_config = {
    "format": {  # Replaces output_format
        "type": "json_schema",
        "schema": {...}
    },
    "effort": "high"  # New in Opus 4.6
}
```

### **Thinking Configuration Evolution**

The thinking parameter has evolved from explicit budget control to adaptive mode:

**Opus 4.5 style (interleaved thinking):**
```python
thinking = {
    "type": "enabled",
    "budget_tokens": 32000
}
```

**Opus 4.6 style (adaptive thinking):**
```python
thinking = {
    "type": "adaptive"  # Auto-manages thinking budget
}
```

### **Fast Mode Requirements**

To use fast mode:
1. Set `speed="fast"` parameter
2. Include `betas=["fast-mode-2026-02-01"]`
3. Compatible with all Claude 4.x models
4. Optimizes for output tokens per second, not latency

### **Batch Processing Limits**

Message batches documentation confirms:
- Batches can process for up to 24 hours
- Custom IDs supported for matching results to requests
- Results retrievable after completion
- Cancelation available for in-progress batches

## Hidden Gems

### **Consecutive Message Turn Combining**

The automatic combining of consecutive user or assistant messages is a subtle but powerful feature that reduces API complexity. Previously undocumented, this behavior is now explicitly called out across SDK docs.

### **C# SDK Production Ready**

The addition of 42 comprehensive C# documentation pages suggests the C# SDK has reached production maturity. This is significant for .NET developers who previously had limited official guidance.

### **Skills API Versioning**

The Skills API now supports full version management (create, list, retrieve, delete versions), indicating a mature API ready for production use with proper version control workflows.

### **Extended Cache TTL Options**

Documentation now shows cache control with two TTL options:
- 5 minutes (short-term caching)
- 1 hour (longer-term caching)

This wasn't prominently featured in previous docs.

### **Citation Types Expanded**

The citation system now supports 5 distinct location types:
- Character locations
- Page locations
- Content block locations
- Web search result locations
- Search result locations

This suggests enhanced document processing and search result integration capabilities.

## New Documentation Pages

All 42 new pages are for the **C# SDK**:

**Beta namespace:**
- Files: delete, download, list, retrieve_metadata
- Messages: count_tokens, create
- Message Batches: cancel, create, delete, list, results, retrieve
- Models: list, retrieve
- Skills: create, delete, list, retrieve
- Skill Versions: create, delete, list, retrieve

**Standard namespace:**
- Messages: count_tokens, create
- Message Batches: cancel, create, delete, list, results, retrieve
- Models: list, retrieve

These pages provide complete API reference documentation with request/response schemas, parameter descriptions, and C#-specific type information.

---

*Generated from Claude API documentation changes detected on February 13, 2026*
