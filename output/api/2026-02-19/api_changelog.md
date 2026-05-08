# Claude API Documentation Changes — 2026-02-19

## Summary

This update adds `claude-sonnet-4-6` as a new model, introduces three new versioned beta tools (`BetaCodeExecutionTool20260120`, `BetaWebSearchTool20260209`, `BetaWebFetchTool20260209`), formalizes several type definitions, and updates the Java SDK to v2.14.0. The majority of line-count changes (325 modified pages) come from a large wave of `curl` example snippets added across beta and non-beta API reference pages, plus a major expansion of the C# non-beta `messages.md` domain types documentation.

---

## Significant Changes

### Models

- **`claude-sonnet-4-6` added to model lists**: The new model ID `"claude-sonnet-4-6"` is now listed as a valid value in all `model` parameters across the Messages API (create, count_tokens, beta, and batches/create endpoints) and the token-counting API.
  > `"claude-sonnet-4-6"` — Frontier intelligence at scale — built for coding, agents, and enterprise workflows
  - *Implication*: Developers can now specify `claude-sonnet-4-6` in API requests. The model appears first after `claude-opus-4-6` in the union, making it the second-listed option.
  - *Source*: [Beta Messages](https://platform.claude.com/docs/en/api/beta/messages.md), [Beta Messages Create](https://platform.claude.com/docs/en/api/beta/messages/create.md)

---

### Beta Tools

- **`BetaCodeExecutionTool20260120` — New code execution tool**: A new versioned code execution tool with type `"code_execution_20260120"`. Described as a code execution tool with REPL state persistence via daemon mode and gVisor checkpoint.
  > `BetaCodeExecutionTool20260120 = object { name, type, allowed_callers, 3 more }`
  > Code execution tool with REPL state persistence (daemon mode + gVisor checkpoint).
  - Parameters: `name: "code_execution"`, `type: "code_execution_20260120"`, `allowed_callers`, `cache_control`, `defer_loading`, `strict`.
  - *Implication*: This is a new version alongside the existing `BetaCodeExecutionTool20250522` and `BetaCodeExecutionTool20250825`, offering persistent REPL state across tool calls. The `tools` union in beta messages now contains 18+ members (up from 15+).
  - *Source*: [Beta API Domain Types](https://platform.claude.com/docs/en/api/beta.md), [Beta Messages](https://platform.claude.com/docs/en/api/beta/messages.md)

- **`BetaWebSearchTool20260209` — New web search tool**: Replaces/supplements the previous `BetaToolSearchToolBm25_20251119` in the tools union. Uses type `"web_search_20260209"` and name `"web_search"`.
  > `BetaWebSearchTool20260209 = object { name, type, allowed_callers, 7 more }`
  - New parameters compared to older search tools: `allowed_domains` (exclusive with `blocked_domains`), `blocked_domains`, `max_uses`, `user_location` (typed as `BetaUserLocation`), `strict`, `defer_loading`.
  > `allowed_domains: optional array of string` — If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.
  - *Implication*: Developers using web search should migrate to `web_search_20260209`. The new tool offers domain allowlist/blocklist controls and per-request usage limits directly on the tool definition.
  - *Source*: [Beta API Domain Types](https://platform.claude.com/docs/en/api/beta.md), [Beta Messages](https://platform.claude.com/docs/en/api/beta/messages.md)

- **`BetaWebFetchTool20260209` — Expanded web fetch tool**: The web fetch tool type is now `"web_fetch_20260209"` (name `"web_fetch"`). Adds several new parameters not previously documented.
  > `BetaWebFetchTool20260209 = object { name, type, allowed_callers, 8 more }`
  - New parameters: `allowed_domains`, `blocked_domains`, `citations` (with `enabled: optional boolean`), `max_content_tokens`, `max_uses`.
  > `citations: optional BetaCitationsConfigParam` — Citations configuration for fetched documents. Citations are disabled by default.
  > `max_content_tokens: optional number` — Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.
  - *Implication*: Developers can now control citation generation and token budgets for fetched web content, and restrict which domains the model fetches from.
  - *Source*: [Beta API Domain Types](https://platform.claude.com/docs/en/api/beta.md), [Beta Messages](https://platform.claude.com/docs/en/api/beta/messages.md)

---

### Beta Types

- **`BetaServerToolCaller20260120` — New server tool caller variant**: Added to the `caller` discriminated union in `BetaToolUseBlock`, `BetaServerToolUseBlock`, `BetaWebSearchToolResultBlock`, `BetaWebFetchToolResultBlock`, and their `Param` counterparts.
  > `caller: optional BetaDirectCaller or BetaServerToolCaller or BetaServerToolCaller20260120`
  > `BetaServerToolCaller20260120 = object { tool_id, type }` — `type: "code_execution_20260120"`
  - *Implication*: Code that pattern-matches on the `caller` field of tool use or result blocks must now handle a third variant (`"code_execution_20260120"`) in addition to `"direct"` and `"code_execution_20250825"`.
  - *Source*: [Beta API Domain Types](https://platform.claude.com/docs/en/api/beta.md)

- **`BetaEncryptedCodeExecutionResultBlock` — New encrypted code execution result type**: Added to the `BetaCodeExecutionToolResultBlockContent` union (and its `Param` counterpart).
  > `BetaEncryptedCodeExecutionResultBlock = object { content, encrypted_stdout, return_code, 2 more }`
  > Code execution result with encrypted stdout for PFC + web_search results.
  - Fields: `content: array of BetaCodeExecutionOutputBlock`, `encrypted_stdout: string`, `return_code: number`, `stderr: string`, `type: "encrypted_code_execution_result"`.
  > `BetaCodeExecutionToolResultBlockContent = BetaCodeExecutionToolResultError or BetaCodeExecutionResultBlock or BetaEncryptedCodeExecutionResultBlock`
  - *Implication*: Consumers of code execution tool results must handle the new `"encrypted_code_execution_result"` type. The encrypted stdout field suggests this is used when code execution runs alongside privacy-preserving features (PFC) or web search.
  - *Source*: [Beta API Domain Types](https://platform.claude.com/docs/en/api/beta.md), [Beta Messages](https://platform.claude.com/docs/en/api/beta/messages.md)

- **`BetaUserLocation` promoted to named type**: The `user_location` parameter on `BetaWebSearchTool20260209` (and the older `BetaToolSearchToolBm25_20251119`) was previously typed as an inline anonymous object `{ type, city, country, 2 more }`. It is now documented as the named type `BetaUserLocation`.
  > `user_location: optional BetaUserLocation`
  > `BetaUserLocation = object { type, city, country, 2 more }` — Fields: `type: "approximate"`, `city`, `country` (ISO 3166-1 alpha-2), `region`, `timezone` (IANA).
  - *Implication*: No behavioral change — this is a documentation/schema formalization. SDK-generated types may reflect the named reference rather than an inline structure.
  - *Source*: [Beta API Domain Types](https://platform.claude.com/docs/en/api/beta.md)

- **`BetaWebSearchToolResultBlock` and `BetaWebFetchToolResultBlock` gain `caller` field**: Both response block types now include an optional `caller` field.
  > `BetaWebSearchToolResultBlock = object { content, tool_use_id, type, caller }`
  > `BetaWebFetchToolResultBlock = object { content, tool_use_id, type, caller }`
  - *Implication*: These blocks now surface which entity triggered the tool call — the model directly (`"direct"`), a prior code execution tool (`"code_execution_20250825"`), or the new code execution variant (`"code_execution_20260120"`).
  - *Source*: [Beta API Domain Types](https://platform.claude.com/docs/en/api/beta.md)

- **`speed` parameter now typed as enum**: The `speed` request parameter in beta Messages Create was previously documented as `optional string`. It is now typed as `optional "standard" or "fast"` with explicit allowed values.
  > `speed: optional "standard" or "fast"` — The inference speed mode for this request. `"fast"` enables high output-tokens-per-second inference.
  - *Implication*: No functional change — valid values remain `"standard"` and `"fast"`. SDK-generated types may now use a string enum rather than a bare string.
  - *Source*: [Beta Messages](https://platform.claude.com/docs/en/api/beta/messages.md), [Beta API Domain Types](https://platform.claude.com/docs/en/api/beta.md)

---

### SDKs

- **Java SDK updated to v2.14.0** (from v2.11.1): The installation snippet in the Java SDK documentation now references `anthropic-java:2.14.0`.
  > `implementation("com.anthropic:anthropic-java:2.14.0")`
  - The client initialization comment was also updated to document `anthropic.apiKey`, `anthropic.authToken`, and `anthropic.baseUrl` system properties (in addition to the existing environment variable equivalents).
  - The structured outputs section was significantly condensed; it now links to the [Structured Outputs](/docs/en/build-with-claude/structured-outputs) page rather than inlining the full walkthrough. Tool use examples and file upload sections remain.
  - *Source*: [Java SDK](https://platform.claude.com/docs/en/api/sdks/java.md)

- **Go SDK SemVer policy documented**: The Go SDK page received a new "Semantic versioning" section explaining that certain backwards-incompatible changes may be released as minor versions (internal changes and changes unlikely to affect most users).
  - *Source*: Go SDK reference page

- **C# Files API — `Upload` method documented**: A new dedicated page for `Beta.Files.Upload` in the C# SDK was added, covering the method signature, `FileUploadParams` fields, and a C# code example.
  - *Source*: [C# Beta Files Upload](https://platform.claude.com/docs/en/api/csharp/beta/files/upload.md)

- **C# `AnthropicBeta` enum gains new values**: The C# SDK's beta enum now documents `TokenEfficientTools2025_02_19`, `Output128k2025_02_19`, and `FastMode2026_02_01` alongside existing beta values. These were already present in other language SDKs but now appear consistently in C# reference pages.

---

### Documentation Examples

A large batch of `curl` example snippets was added to API reference pages across all beta and non-beta endpoints:
- Beta messages, count_tokens, models (list/retrieve), files, skills, and batches endpoints received `?beta=true` curl examples.
- Completions and completions/create pages received curl examples.
- C# SDK beta reference pages received C# code examples for all beta endpoints.
- The `beta-headers.md` example changed its demonstration beta flag from `code-execution-2025-08-25` to `files-api-2025-04-14`.

These are documentation-only additions and do not change API behavior.

---

## New Pages

- **`en_api_csharp_beta_files_upload.md`** — Documents the C# SDK `Beta.Files.Upload` method (`POST /v1/files`), including `FileUploadParams`, `FileMetadata` return type, and a usage example. [View](https://platform.claude.com/docs/en/api/csharp/beta/files/upload.md)

---

## Notable Details

- The `tools` array in the beta Messages Create endpoint now admits **18+ tool types** (up from 15+), reflecting the three new tools added: `BetaCodeExecutionTool20260120`, `BetaWebSearchTool20260209`, and `BetaWebFetchTool20260209`.
- The `BetaEncryptedCodeExecutionResultBlock` description mentions "PFC + web_search results", suggesting it is specifically used when code execution output is encrypted due to privacy-preserving computation alongside web search integration.
- The `BetaCodeExecutionTool20260120` description ("daemon mode + gVisor checkpoint") indicates persistent sandboxed process state across calls within a session — a meaningful execution model change from earlier code execution tools.
- The C# non-beta `messages.md` page received a massive restructure (+20,343 / -6,376 lines), adding the full suite of non-beta domain types (e.g., `EncryptedCodeExecutionResultBlock`, `EncryptedCodeExecutionResultBlockParam`, `DirectCaller`, `ServerToolCaller`, `ServerToolUsage`) directly in the C# SDK reference rather than relying on the language-agnostic reference.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `en/api/beta.md` | Modified | +3691 / -393 | New tools: `BetaCodeExecutionTool20260120`, `BetaWebSearchTool20260209`, `BetaWebFetchTool20260209`; `BetaEncryptedCodeExecutionResultBlock`; `BetaUserLocation` named type; `BetaServerToolCaller20260120`; `claude-sonnet-4-6`; curl examples |
| `en/api/beta/messages.md` | Modified | +3509 / -351 | Same type additions as `beta.md` plus new tool sections; curl examples |
| `en/api/csharp/beta.md` | Modified | +3766 / -676 | New C# SDK types for all new beta tools/results; Files API Upload section |
| `en/api/csharp/messages.md` | Modified | +20343 / -6376 | Major expansion: added full domain types reference for non-beta C# SDK |
| `en/api/csharp/beta/messages.md` | Modified | +3382 / -554 | C# beta messages type additions mirroring `beta.md` |
| `en/api/beta/messages/create.md` | Modified | +453 / -12 | `claude-sonnet-4-6` model; curl example; new tool types |
| `en/api/csharp/beta/messages/batches.md` | Modified | +850 / -10 | C# batch examples added |
| `en/api/beta/messages/batches.md` | Modified | +838 / -31 | Curl examples for batch endpoints |
| `en/api/beta/messages/batches/create.md` | Modified | +351 / -7 | Batch create curl example |
| `en/api/beta/messages/count_tokens.md` | Modified | +348 / -9 | New tool types; curl example |
| `en/api/csharp/beta/files.md` | Modified | +148 / -0 | New C# Files API Upload documentation |
| `en/api/csharp/beta/files/upload.md` | New | +105 | New C# Files API upload method reference |
| `en/api/sdks/java.md` | Modified | ~+large | SDK updated to v2.14.0; structured outputs section condensed |
| `en/api/sdks/python.md` | Modified | ~+medium | Platform integration table added |
| `en/api/sdks/typescript.md` | Modified | ~+medium | Platform SDK install commands reformatted |
| `en/api/beta-headers.md` | Modified | +3 / -3 | Beta example changed from `code-execution-2025-08-25` to `files-api-2025-04-14` |
| `en/api/beta/skills.md` | Modified | +77 / -1 | Skills API curl examples added |
| `en/api/completions.md` | Modified | +30 / -3 | Completions curl example added |
| *(~305 other SDK/language reference pages)* | Modified | varies | Parallel curl/code examples added; new model and tool types propagated across Python, TypeScript, Go, Ruby, Java, C# language reference variants |

---

*Generated from Claude API documentation changes detected on 2026-02-19*
