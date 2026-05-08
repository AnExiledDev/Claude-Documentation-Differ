# Claude API Documentation Changes — 2026-03-19

## Summary

This update introduces three substantive API changes: a new web fetch tool version (`web_fetch_20260309`) with a `use_cache` bypass parameter, a `display` field on thinking configurations to control whether thinking tokens appear in responses, and a fully-populated `capabilities` object (plus `max_input_tokens`/`max_tokens` fields) on the Models API `ModelInfo` type. All changes are reflected across the base REST API and all six SDK language variants (Python, TypeScript, Go, Java, Ruby, C#), in both standard and beta namespaces.

---

## Significant Changes

### Tools — Web Fetch

- **New `WebFetchTool20260309` with `use_cache` parameter**: A new version of the web fetch tool (`type: "web_fetch_20260309"`) replaces the previous `web_fetch_20260209`. The key addition is a `use_cache: optional boolean` parameter that allows bypassing the cache to fetch fresh content.

  > `Web fetch tool with use_cache parameter for bypassing cached content.`
  >
  > `use_cache: optional boolean` — `Whether to use cached content. Set to false to bypass the cache and fetch fresh content. Only set to false when the user explicitly requests fresh content or when fetching rapidly-changing sources.`

  The new version also documents `allowed_callers` now accepting `"code_execution_20260120"` in addition to `"direct"` and `"code_execution_20250825"`, indicating an updated code execution integration. Other parameters remain the same: `allowed_domains`, `blocked_domains`, `citations`, `defer_loading`, `max_content_tokens`, `max_uses`, `strict`, and `cache_control`.

  - *Implication*: Developers using the web fetch tool can now explicitly control cache behaviour per-request. Set `use_cache: false` only when freshness is required; the docs discourage using it unnecessarily.
  - *Source*: [Messages API](https://platform.claude.com/docs/en/api/messages.md) · [Beta Messages API](https://platform.claude.com/docs/en/api/beta/messages.md)

### Extended Thinking — Display Control

- **`display` field added to `ThinkingConfigEnabled` and `ThinkingConfigAdaptive`**: Both thinking configuration objects now accept an optional `display` parameter with values `"summarized"` (default) or `"omitted"`.

  > `display: optional "summarized" or "omitted"` — `Controls how thinking content appears in the response. When set to summarized, thinking is returned normally. When set to omitted, thinking content is redacted but a signature is returned for multi-turn continuity. Defaults to summarized.`

  This applies to both `type: "enabled"` and `type: "adaptive"` thinking configs, and to both the standard and beta Messages API endpoints.

  - *Implication*: Setting `display: "omitted"` allows applications to hide thinking tokens from end users while preserving the cryptographic signature needed to continue multi-turn conversations. This is useful for production applications where raw thinking traces should not be surfaced.
  - *Source*: [Messages API](https://platform.claude.com/docs/en/api/messages.md) · [Beta Messages API](https://platform.claude.com/docs/en/api/beta/messages.md)

### Models API — Capability Metadata

- **`ModelInfo` now includes a `capabilities` object**: The list (`GET /v1/models`) and retrieve (`GET /v1/models/{model_id}`) endpoints now return a `capabilities` field on every `ModelInfo` object. Each capability uses a `CapabilitySupport` shape (`{ supported: boolean }`) or a richer nested type.

  Capability fields included:

  | Field | Type | Description |
  |-------|------|-------------|
  | `batch` | `CapabilitySupport` | Whether the model supports the Batch API |
  | `citations` | `CapabilitySupport` | Whether the model supports citation generation |
  | `code_execution` | `CapabilitySupport` | Whether the model supports code execution tools |
  | `context_management` | `ContextManagementCapability` | Context management strategies: `clear_thinking_20251015`, `clear_tool_uses_20250919`, `compact_20260112` |
  | `effort` | `EffortCapability` | `reasoning_effort` levels supported: `low`, `medium`, `high`, `max` |
  | `image_input` | `CapabilitySupport` | Whether the model accepts image content blocks |
  | `pdf_input` | `CapabilitySupport` | Whether the model accepts PDF content blocks |
  | `structured_outputs` | `CapabilitySupport` | Whether the model supports structured output / JSON mode / strict tool schemas |
  | `thinking` | `ThinkingCapability` | Thinking support and type configs (`adaptive`, `enabled`) |

  > `capabilities: ModelCapabilities` — `Model capability information.`

  - *Implication*: Developers can now programmatically detect which features a model supports rather than maintaining static capability tables. This is especially useful for applications that need to route requests across models or display feature availability.
  - *Source*: [Models API](https://platform.claude.com/docs/en/api/models.md) · [Beta Models API](https://platform.claude.com/docs/en/api/beta/models.md)

- **`max_input_tokens` and `max_tokens` added to `ModelInfo`**: Two new fields expose the model's context window limits directly from the API response.

  > `max_input_tokens: number` — `Maximum input context window size in tokens for this model.`
  >
  > `max_tokens: number` — `Maximum value for the max_tokens parameter when using this model.`

  - *Implication*: Applications can now query the model's token limits at runtime instead of hardcoding them. Both fields appear in list and retrieve responses, and in the beta equivalents (`BetaModelInfo`).
  - *Source*: [Models API](https://platform.claude.com/docs/en/api/models.md) · [Beta Models API](https://platform.claude.com/docs/en/api/beta/models.md)

---

## Notable Details

- **`BetaModelInfo` shape change**: The beta type was previously documented as `BetaModelInfo = object { id, created_at, display_name, type }`. It is now `BetaModelInfo = object { id, capabilities, created_at, 4 more }`, reflecting the same capability expansion as the non-beta type.

- **`tools` union type count incremented in beta count_tokens**: The beta `count_tokens` endpoint tools parameter was previously `18 more` variants; it is now `19 more`, reflecting the addition of `BetaWebFetchTool20260309` to the union.

- **SDK-wide rollout**: All capability, web fetch, and thinking display changes appear in documentation for Python, TypeScript, Go, Java, Ruby, and C# SDKs simultaneously, in both standard and beta namespaces (approximately 130 pages updated). Ruby SDK also received minor formatting/reference updates across several beta endpoint pages (files, skills, completions).

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/api/csharp/beta.md` | Modified | +1839/-636 | C# beta: ModelCapabilities, WebFetchTool20260309, ThinkingConfig display |
| `docs/api/en/api/go/beta.md` | Modified | +1723/-496 | Go beta: ModelCapabilities, WebFetchTool20260309, ThinkingConfig display |
| `docs/api/en/api/ruby/beta.md` | Modified | +1379/-120 | Ruby beta: ModelCapabilities, WebFetchTool20260309, ThinkingConfig display |
| `docs/api/en/api/beta.md` | Modified | +1367/-108 | Base beta: ModelCapabilities, WebFetchTool20260309, ThinkingConfig display |
| `docs/api/en/api/python/beta.md` | Modified | +1354/-95 | Python beta: ModelCapabilities, WebFetchTool20260309, ThinkingConfig display |
| `docs/api/en/api/typescript/beta.md` | Modified | +1355/-96 | TypeScript beta: ModelCapabilities, WebFetchTool20260309, ThinkingConfig display |
| `docs/api/en/api/java/beta.md` | Modified | +1322/-95 | Java beta: ModelCapabilities, WebFetchTool20260309, ThinkingConfig display |
| `docs/api/en/api/models.md` | Modified | +775/-3 | ModelCapabilities, ContextManagementCapability, EffortCapability, ThinkingCapability types |
| `docs/api/en/api/beta/models.md` | Modified | +775/-3 | Beta ModelCapabilities types added |
| `docs/api/en/api/ruby/models.md` | Modified | +775/-3 | Ruby SDK ModelCapabilities types |
| `docs/api/en/api/csharp/models.md` | Modified | +773/-1 | C# SDK ModelCapabilities types |
| `docs/api/en/api/go/models.md` | Modified | +773/-1 | Go SDK ModelCapabilities types |
| `docs/api/en/api/java/models.md` | Modified | +773/-1 | Java SDK ModelCapabilities types |
| `docs/api/en/api/python/models.md` | Modified | +773/-1 | Python SDK ModelCapabilities types |
| `docs/api/en/api/typescript/models.md` | Modified | +773/-1 | TypeScript SDK ModelCapabilities types |
| `docs/api/en/api/messages.md` | Modified | +580/-12 | WebFetchTool20260309, ThinkingConfig display |
| `docs/api/en/api/ruby/messages.md` | Modified | +570/-2 | WebFetchTool20260309 for Ruby SDK |
| `docs/api/en/api/typescript/messages.md` | Modified | +570/-2 | WebFetchTool20260309 for TypeScript SDK |
| `docs/api/en/api/python/messages.md` | Modified | +568/-0 | WebFetchTool20260309 for Python SDK |
| `docs/api/en/api/go/messages.md` | Modified | +536/-0 | WebFetchTool20260309 for Go SDK |
| `docs/api/en/api/java/messages.md` | Modified | +536/-0 | WebFetchTool20260309 for Java SDK |
| `docs/api/en/api/beta/messages.md` | Modified | +499/-12 | Beta WebFetchTool20260309, ThinkingConfig display |
| `docs/api/en/api/ruby/beta/messages.md` | Modified | +497/-10 | Ruby beta WebFetchTool20260309 |
| `docs/api/en/api/typescript/beta/messages.md` | Modified | +489/-2 | TypeScript beta WebFetchTool20260309 |
| `docs/api/en/api/python/beta/messages.md` | Modified | +487/-0 | Python beta WebFetchTool20260309 |
| `docs/api/en/api/go/beta/messages.md` | Modified | +455/-0 | Go beta WebFetchTool20260309 |
| `docs/api/en/api/java/beta/messages.md` | Modified | +455/-0 | Java beta WebFetchTool20260309 |
| `docs/api/en/api/csharp/messages.md` | Modified | +504/-1 | C# SDK WebFetchTool20260309 |
| `docs/api/en/api/csharp/beta/messages.md` | Modified | +431/-3 | C# beta WebFetchTool20260309 |
| `docs/api/en/api/*/models/list.md` | Modified | ~+160 each | ModelCapabilities fields in list response (all 12 SDK variants) |
| `docs/api/en/api/*/models/retrieve.md` | Modified | ~+160 each | ModelCapabilities fields in retrieve response (all 12 SDK variants) |
| `docs/api/en/api/*/messages/create.md` | Modified | ~+80–99 each | WebFetchTool20260309 in tools union (all SDK variants) |
| `docs/api/en/api/*/messages/batches/create.md` | Modified | ~+97–99 each | WebFetchTool20260309 in batch tools union (all SDK variants) |
| `docs/api/en/api/*/messages/count_tokens.md` | Modified | ~+75–100 each | WebFetchTool20260309 in count_tokens tools union (all SDK variants) |

---

*Generated from Claude API documentation changes detected on 2026-03-19*
