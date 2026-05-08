# Claude API Documentation Changes - February 6, 2026

## TL;DR

This is a **major documentation refresh** representing what appears to be a complete rebuild of the Claude API documentation site. The documentation now includes 493 new pages covering Claude 4.6 models, a comprehensive Agent SDK, new Admin APIs for organization management, Skills API for custom agent capabilities, MCP connector for remote tool integration, and extensive guides for prompt engineering, testing, and enterprise features.

## 🚀 Major New Features

### Claude 4.6 Models

New model family with significant capabilities and breaking changes:

- **`claude-opus-4-6`**: Latest and most intelligent model, "world's best model for coding, enterprise agents, and professional work"
- **`claude-sonnet-4-5-20250929`**: Best combination of speed and intelligence for everyday tasks
- **`claude-haiku-4-5-20251001`**: Near-frontier performance with lightning-fast speed and extended thinking at economical pricing

> Claude Opus 4.6 is a near drop-in replacement for Claude 4.5, with a few breaking changes to be aware of.

**Key capabilities:**
- 200K context window (with 1M token beta option)
- 128K max output tokens
- Adaptive thinking mode (replaces extended thinking)
- Enhanced tool use with new versions

### Claude Agent SDK

Comprehensive new SDK for building AI agents with Claude:

> The Claude Agent SDK provides detailed token usage information for each interaction with Claude.

**Available in Python and TypeScript** with features including:
- File checkpointing for undo/redo operations
- Hooks system for intercepting and controlling agent behavior
- Custom tools via MCP protocol integration
- Session management and resumption
- Subagent spawning for parallel tasks
- Todo tracking and structured outputs
- Skills integration
- Cost tracking and usage analytics

Hooks example showing security control:
```python
async def protect_env_files(input_data, tool_use_id, context):
    file_path = input_data['tool_input'].get('file_path', '')
    if file_path.endswith('.env'):
        return {
            'hookSpecificOutput': {
                'permissionDecision': 'deny',
                'permissionDecisionReason': 'Cannot modify .env files'
            }
        }
    return {}
```

### MCP Connector (Public Beta)

Connect to remote MCP servers directly from the Messages API:

> The MCP connector is a feature that allows API users to connect to MCP servers directly from the Messages API without building an MCP client.

- No separate MCP client needed
- OAuth authentication support via `authorization_token` parameter
- Seamless integration with MCP-compatible tools and services
- **Not supported on Amazon Bedrock and Google Vertex**

### Skills API

New API for creating and managing agent skills:

- **Skills API endpoints**: `POST /v1/skills`, `GET /v1/skills`
- Workspace-scoped distribution
- Version management for custom skills
- Pre-built Anthropic-managed skills (e.g., `pptx`, `xlsx`)
- Requires `skills-2025-10-02` beta header

> Use pre-built Agent Skills by referencing their `skill_id` (e.g., `pptx`, `xlsx`), or create and upload your own via the Skills API.

### Admin API

Comprehensive API for programmatic organization management:

> **The Admin API is unavailable for individual accounts.** Only organization members with the admin role can use the Admin API.

**Requires special Admin API key** (starting with `sk-ant-admin...`)

**Capabilities:**
- Organization management (`/v1/organizations/*`)
- User and member management
- Workspace management (create, archive, update)
- API key management (list, retrieve, update - cannot create new keys)
- Invitations management
- Usage and cost reporting
- Claude Code analytics

**New reporting endpoints:**
- `/v1/admin/usage_report` - Messages API usage
- `/v1/admin/usage_report/claude_code` - Claude Code analytics
- `/v1/admin/cost_report` - Cost data

> The Claude Code Analytics Admin API provides programmatic access to daily aggregated usage metrics for Claude Code users.

## 🔥 Breaking Changes

### Claude 4.6 Breaking Changes

1. **Prefill removal** (CRITICAL):
   > Prefilling assistant messages returns a 400 error on Claude 4.6 models.

   **Migration:** Use structured outputs, system prompt instructions, or `output_config.format` instead.

2. **Tool parameter quoting changes**:
   > Claude 4.6 models may produce slightly different JSON string escaping in tool call arguments.

   **Impact:** If parsing tool call `input` as raw strings, verify parsing logic. Standard JSON parsers handle this automatically.

3. **Sampling parameters** (when migrating from Claude 3.x):
   > Use only `temperature` OR `top_p`, not both.

   Previously both could be used together; Claude 4+ models will error if both are provided.

4. **Tool version updates required** (from Claude 3.x):
   - Text editor: Use `text_editor_20250728` and `str_replace_based_edit_tool`
   - Code execution: Upgrade to `code_execution_20250825`
   - Remove any code using the `undo_edit` command

5. **New stop reasons to handle**:
   - `refusal` - When Claude refuses a request
   - `model_context_window_exceeded` - When hitting context limit (vs `max_tokens` limit)

6. **Trailing newlines preserved**:
   > Claude 4.5+ models preserve trailing newlines in tool call string parameters that were previously stripped.

## 📝 API Changes

### Adaptive Thinking (Replaces Extended Thinking)

New thinking mode for Claude 4.6:

> Adaptive thinking (`thinking: {type: "adaptive"}`) is the recommended thinking mode for Opus 4.6. Claude dynamically decides when and how much to think.

**Migration path:**
```python
# Before (deprecated)
thinking={
    "type": "enabled",
    "budget_tokens": 32000
}
betas=["interleaved-thinking-2025-05-14"]

# After
thinking={
    "type": "adaptive"
}
output_config={
    "effort": "high"  # or "low", "medium", "max"
}
# No beta header required
```

**Note:** Extended thinking with `budget_tokens` is deprecated on Claude 4.6 and will be removed in future releases.

### Effort Parameter (Now GA)

> The effort parameter is now generally available (no beta header required). A new `max` effort level provides the absolute highest capability on Opus 4.6.

**Effort levels:** `low`, `medium`, `high`, `max`

Remove `betas=["effort-2025-11-24"]` from requests.

### Structured Outputs Parameter Change

`output_format` parameter moved to `output_config.format`:

```python
# Old (deprecated, still functional)
output_format={"type": "json_schema", "schema": {...}}

# New
output_config={"format": {"type": "json_schema", "schema": {...}}}
```

> The old parameter remains functional but is deprecated and will be removed in a future model release.

### Fine-Grained Tool Streaming (Now GA)

Remove `betas=["fine-grained-tool-streaming-2025-05-14"]` from requests.

### Interleaved Thinking Header Deprecated

> The `interleaved-thinking-2025-05-14` beta header is deprecated on Opus 4.6. Adaptive thinking automatically enables interleaved thinking.

## 📊 Model Deprecations

### Active Deprecations

| Model | Deprecated | Retirement Date | Replacement |
|-------|-----------|----------------|-------------|
| `claude-3-7-sonnet-20250219` | Oct 28, 2025 | Feb 19, 2026 | `claude-opus-4-6` |
| `claude-3-5-haiku-20241022` | Dec 19, 2025 | Feb 19, 2026 | `claude-haiku-4-5-20251001` |

### Recently Retired

- `claude-3-opus-20240229` - Retired Jan 5, 2026
- `claude-3-5-sonnet-20240620` - Retired Oct 28, 2025
- `claude-3-5-sonnet-20241022` - Retired Oct 28, 2025

> Anthropic notifies customers with active deployments for models with upcoming retirements. We provide at least 60 days notice before model retirement for publicly released models.

## 🔧 SDK Updates

### New SDKs

- **Go SDK** - Complete API support with types
- **Java SDK** - Complete API support with types
- **Ruby SDK** - Complete API support with types
- **Claude Agent SDK** - Python and TypeScript

All SDKs now include comprehensive support for:
- Beta features (files, skills, message batches)
- Model listing and retrieval
- Completions API
- Admin API support

### OpenAI SDK Compatibility

Documentation now includes OpenAI SDK compatibility layer:

> Use Claude with the OpenAI Python/TypeScript SDK by changing the base URL and API key.

## 🛠️ Tool Use Updates

### New Built-in Tools

Documentation now covers additional built-in tools:

- **Memory tool** - Persistent context across sessions
- **Tool Search tool** - Discovering available MCP tools
- **Web Fetch tool** - HTTP requests from Claude
- **Web Search tool** - Web search capabilities
- **Bash tool** - Enhanced command execution
- **Code execution tool** - Version `code_execution_20250825`
- **Text editor tool** - Version `text_editor_20250728`

### Programmatic Tool Calling

> Note that when you have `tool_choice` as `any` or `tool`, we will prefill the assistant message to force a tool to be used.

**Important for Claude 4.6:** Prefilling is not supported, but forced tool use via `tool_choice` still works differently.

### Tool Use with Extended Thinking

> When using extended thinking with tool use, `tool_choice: {"type": "any"}` and `tool_choice: {"type": "tool", "name": "..."}` are not supported and will result in an error.

Only `tool_choice: {"type": "auto"}` (default) and `tool_choice: {"type": "none"}` work with extended thinking.

## 📚 New Documentation Sections

### About Claude

- **Glossary** - Comprehensive terminology (context window, fine-tuning, HHH, latency, LLM, MCP, RAG, RLHF, temperature, TTFT, tokens)
- **Model Deprecations** - Lifecycle tracking and migration guidance
- **Choosing a Model** - Decision framework for model selection
- **Migration Guide** - Step-by-step Claude 4.6 migration
- **What's New in Claude 4.6** - Feature announcements
- **Pricing** - Detailed pricing information
- **Use Case Guides** - Content moderation, customer support, legal summarization, ticket routing

### Build with Claude (Enhanced)

New comprehensive guides:
- Adaptive thinking
- Citations
- Claude Code Analytics API
- Compaction
- Context editing
- Data residency
- Effort parameter
- Search results
- Skills guide
- Workspaces
- Zero data retention

### Test and Evaluate (New Section)

- Define success criteria
- Develop tests
- Eval tool
- Strengthen guardrails:
  - Handle streaming refusals
  - Increase consistency
  - Keep Claude in character
  - Mitigate jailbreaks
  - Reduce hallucinations
  - Reduce latency
  - Reduce prompt leak

### Prompt Engineering (Comprehensive)

- Be clear and direct
- Chain of thought
- Chain prompts
- Claude prompting best practices
- Extended thinking tips
- Long context tips
- Multishot prompting
- Prompt generator
- Prompt improver
- Prompt templates and variables
- System prompts
- Use XML tags

### Prompt Library

65 new prompt examples including:
- Adaptive editor
- Code clarifier/consultant
- CSV converter
- Data organizer
- Email extractor
- Grammar genie
- Python bug buster
- SQL sorcerer
- And many more...

## 🏢 Enterprise Features

### Data Residency

> These settings can be configured through the Console or the Admin API under the `data_residency` field.

Region-specific data processing now configurable via API.

### Workspaces

Programmatic workspace management via Admin API:
- Create workspaces
- Archive workspaces
- Manage workspace members (add, remove, update roles)
- Retrieve workspace details

### Service Tiers

New documentation on service tiers and SLA commitments.

### IP Addresses

Documentation of Claude API IP address ranges for firewall configuration.

### Supported Regions

Comprehensive region availability information.

## 🔒 Security & Privacy

### Zero Data Retention

> Claude API offers zero data retention options for enterprise customers.

Documentation of data retention policies and enterprise privacy options.

### Handling Refusals

New stop reason for safety refusals:

```python
if response.stop_reason == "refusal":
    # Handle refusal appropriately
    pass
```

## 🌐 Platform Availability

New platform-specific guides:
- Claude on Amazon Bedrock
- Claude on Vertex AI
- Claude in Microsoft Foundry (Azure AI)

Each with specific model IDs and platform-specific features.

## Hidden Gems

### Context Window Expansion

> Claude Opus 4.6 supports a 200K context window (with 1M token context window available in beta).

The 1M token context window is mentioned as a beta feature - this is a significant capability increase.

### Model Preservation Commitment

> At some point, we hope to make past models publicly available again. In the meantime, we've committed to long-term preservation of model weights and other measures to help mitigate these impacts.

Reference to [Commitments on Model Deprecation and Preservation](https://www.anthropic.com/research/deprecation-commitments).

### Batch API Discounts

Multiple references to batch API pricing discounts in pricing footnotes, suggesting batch processing cost optimization.

### Prompt Caching with Thinking

> Extended thinking impacts prompt caching efficiency.

Important performance consideration for caching strategies.

### Legacy Beta Headers Deprecated

> Remove legacy beta headers: `token-efficient-tools-2025-02-19` and `output-128k-2025-02-19`. All Claude 4+ models have built-in token-efficient tool use.

These features are now built-in to Claude 4+ models.

### File API (Beta)

New file management endpoints:
- Upload files (`POST /v1/beta/files`)
- Download files (`GET /v1/beta/files/{file_id}/content`)
- List files (`GET /v1/beta/files`)
- Delete files (`DELETE /v1/beta/files/{file_id}`)
- Retrieve metadata (`GET /v1/beta/files/{file_id}`)

### Models API

New endpoints to list and retrieve model information:
- `GET /v1/models` - List available models
- `GET /v1/models/{model_id}` - Get model details

### Message Batches (Beta)

Batch processing API:
- Create batches (`POST /v1/beta/messages/batches`)
- Retrieve batch status (`GET /v1/beta/messages/batches/{batch_id}`)
- List batches (`GET /v1/beta/messages/batches`)
- Cancel batches (`POST /v1/beta/messages/batches/{batch_id}/cancel`)
- Get results (`GET /v1/beta/messages/batches/{batch_id}/results`)
- Delete batches (`DELETE /v1/beta/messages/batches/{batch_id}`)

### Token Counting API

> `/v1/beta/messages/count_tokens` endpoint for pre-flight token estimation.

Useful for cost estimation before making actual API calls.

## Technical Details

### API Versioning

> Anthropic uses dated API versions to manage breaking changes. The current version is specified via the `anthropic-version` header.

### Rate Limits

Comprehensive rate limiting documentation with tier-based limits and best practices.

### Beta Headers

Beta features now require specific headers:
- `anthropic-beta: skills-2025-10-02` - Skills API
- Various other beta headers for experimental features

### Error Handling

Expanded error documentation including:
- 400 errors for invalid requests (e.g., prefill on Claude 4.6)
- New error codes and messages
- Streaming error handling

## Migration Checklist Summary

For Claude 4.6 migration:

- [ ] Update model ID to `claude-opus-4-6`
- [ ] **BREAKING:** Remove assistant message prefills
- [ ] Migrate to adaptive thinking with effort parameter
- [ ] Update sampling parameters (no both `temperature` and `top_p`)
- [ ] Update tool versions (text editor, code execution)
- [ ] Handle new stop reasons (`refusal`, `model_context_window_exceeded`)
- [ ] Verify trailing newline handling in tool parameters
- [ ] Remove deprecated beta headers
- [ ] Migrate `output_format` to `output_config.format`
- [ ] Update prompts for behavioral changes

---

*Generated from Claude API documentation changes detected on 2026-02-06*

**Note:** This represents a complete documentation rebuild with 493 new pages added and 0 pages removed or modified, suggesting a major platform update or documentation restructuring. The changes indicate significant new capabilities across models, APIs, SDKs, and developer tools.
