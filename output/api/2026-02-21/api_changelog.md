# Claude API Documentation Changes — 2026-02-21

## Summary

84 pages were modified across all SDK language references (Python, TypeScript, Go, Java, Ruby, C#) and the core REST API documentation. The primary changes are: six new server tool type definitions documented (`CodeExecutionTool20260120`, `WebSearchTool20260209`, `WebFetchTool20260209`, `ServerToolCaller20260120`, `UserLocation`, `WebSearchToolResultErrorCode`), a new top-level `cache_control` shorthand parameter on the Messages and Count Tokens endpoints, and expansion of the `allowed_callers` enum to include `"code_execution_20260120"`. The `speed` parameter has been removed from Java and C# SDK documentation for the Messages Create endpoint.

---

## Significant Changes

### New Server Tool Types

Six new type definitions have been added to the domain types reference across all SDK languages and the REST API.

---

#### `CodeExecutionTool20260120` — New Code Execution Tool Version

- **Code execution with REPL state persistence**: A new versioned code execution tool type (`type: "code_execution_20260120"`) is now documented.
  > "Code execution tool with REPL state persistence (daemon mode + gVisor checkpoint)."

  New parameters added relative to `code_execution_20250825`:
  - `defer_loading` (boolean, optional): `"If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search."`
  - `strict` (boolean, optional): `"When true, guarantees schema validation on tool names and inputs"`

  - *Implication*: Developers can use `"code_execution_20260120"` for persistent REPL sessions across tool calls. The `defer_loading` parameter enables lazy tool loading via tool search, reducing initial system prompt size.
  - *Source*: [messages.md (REST)](https://platform.claude.com/docs/en/api/messages.md), [python/messages.md](https://platform.claude.com/docs/en/api/python/messages.md), [typescript/messages.md](https://platform.claude.com/docs/en/api/typescript/messages.md), [go/messages.md](https://platform.claude.com/docs/en/api/go/messages.md), [java/messages.md](https://platform.claude.com/docs/en/api/java/messages.md), [ruby/messages.md](https://platform.claude.com/docs/en/api/ruby/messages.md), [csharp/messages.md](https://platform.claude.com/docs/en/api/csharp/messages.md)

---

#### `WebSearchTool20260209` — New Web Search Tool Version

- **Updated web search tool with user location support**: A new versioned web search type (`type: "web_search_20260209"`) is now documented with additional parameters beyond `web_search_20250305`.

  New parameters:
  - `user_location` (optional `UserLocation`): `"Parameters for the user's location. Used to provide more relevant search results."` — contains `city`, `country` (ISO 3166-1 alpha-2), `region`, `timezone` (IANA)
  - `defer_loading` (optional boolean)
  - `max_uses` (optional integer): `"Maximum number of times the tool can be used in the API request."`
  - `strict` (optional boolean)

  - *Implication*: Passing a `user_location` object to `web_search_20260209` allows geographically relevant search results (e.g., local news, region-specific results). The `max_uses` cap is useful for cost control in agentic loops.
  - *Source*: [messages.md (REST)](https://platform.claude.com/docs/en/api/messages.md)

---

#### `WebFetchTool20260209` — New Web Fetch Tool Version

- **Updated web fetch tool with citations and content limits**: A new versioned web fetch type (`type: "web_fetch_20260209"`) is now documented with additional parameters beyond `web_fetch_20250910`.

  New parameters:
  - `citations` (optional `CitationsConfigParam`): `"Citations configuration for fetched documents. Citations are disabled by default."` — `enabled: bool`
  - `max_content_tokens` (optional integer): `"Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs."`
  - `max_uses` (optional integer): `"Maximum number of times the tool can be used in the API request."`
  - `defer_loading` (optional boolean)
  - `strict` (optional boolean)

  - *Implication*: The `citations` flag enables source attribution for fetched web content. `max_content_tokens` gives developers a budget cap on how much fetched page content consumes context window space.
  - *Source*: [messages.md (REST)](https://platform.claude.com/docs/en/api/messages.md)

---

#### `UserLocation` — New Standalone Type

- **User location type for geo-aware tools**: A new `UserLocation` type is now formally defined as a standalone domain type.

  ```
  UserLocation = object {
    type: "approximate",
    city?: string,
    country?: string,   // ISO 3166-1 alpha-2
    region?: string,
    timezone?: string   // IANA timezone
  }
  ```

  - *Implication*: Currently consumed by `WebSearchTool20260209.user_location`. Defining it as a named type suggests it may be reused by other tools in future.
  - *Source*: [messages.md (REST)](https://platform.claude.com/docs/en/api/messages.md)

---

#### `ServerToolCaller20260120` — Renamed and Formalized Caller Type

- **`CodeExecution20260120` renamed to `ServerToolCaller20260120`**: The anonymous or provisional type used to identify a code execution caller in the response `caller` union was renamed.

  Before (REST API): `caller: optional DirectCaller or ServerToolCaller or object { tool_id, type }` (with inline `CodeExecution20260120`)
  After: `caller: optional DirectCaller or ServerToolCaller or ServerToolCaller20260120`

  Across SDKs:
  - Python: `CallerServerToolCaller20260120` → `ServerToolCaller20260120`
  - C#, REST: `CodeExecution20260120` → `ServerToolCaller20260120`
  - Go, Java, Ruby, TypeScript: parallel renames

  - *Implication*: This is a **documentation rename** — the wire format (`tool_id` + `type`) is unchanged. Code checking class names or type strings may need updating.
  - *Source*: [messages/create.md (REST)](https://platform.claude.com/docs/en/api/messages/create.md), [python/messages/create.md](https://platform.claude.com/docs/en/api/python/messages/create.md), [csharp/messages/create.md](https://platform.claude.com/docs/en/api/csharp/messages/create.md)

---

#### `WebSearchToolResultErrorCode` — Formalized Error Code Enum

- **`WebSearchToolRequestError.error_code` now uses a named type**: Previously documented as an inline literal union, the error code for web search tool failures is now the formal enum `WebSearchToolResultErrorCode`.

  > `WebSearchToolResultErrorCode = "invalid_tool_input" | "unavailable" | "max_uses_exceeded" | "too_many_requests" | "query_too_long" | "request_too_large"`

  Note: `"max_uses_exceeded"` and `"too_many_requests"` are now under the unified `WebSearchToolResultErrorCode` enum (previously inconsistently referenced as `WebSearchToolRequestErrorErrorCode` in the Go SDK, now corrected).

  - *Implication*: Code handling web search tool errors should now check against the `WebSearchToolResultErrorCode` type. The full set of values is: `invalid_tool_input`, `unavailable`, `max_uses_exceeded`, `too_many_requests`, `query_too_long`, `request_too_large`.
  - *Source*: [messages/create.md (REST)](https://platform.claude.com/docs/en/api/messages/create.md), [python/messages/create.md](https://platform.claude.com/docs/en/api/python/messages/create.md)

---

### Messages API — New Top-Level `cache_control` Parameter

- **Top-level `cache_control` shorthand added to `POST /v1/messages` and Count Tokens**: A new optional top-level parameter `cache_control` has been added as a convenience shorthand across the Messages Create, Count Tokens, and Message Batches create endpoints (both beta and non-beta).

  > "Top-level cache control automatically applies a cache_control marker to the last cacheable block in the request."

  Schema:
  ```json
  {
    "cache_control": {
      "type": "ephemeral",
      "ttl": "5m"   // or "1h", defaults to "5m"
    }
  }
  ```

  This is reflected in all SDK language docs: `cache_control: Optional[CacheControlEphemeralParam]` (Python), `cacheControl?: CacheControlEphemeral` (TypeScript/C#), `CacheControl CacheControlEphemeralParam` (Go), etc.

  The Message Batches `params` object count has incremented from "18 more" to "19 more" parameters accordingly.

  - *Implication*: Developers can now enable prompt caching without manually annotating the last content block — set `cache_control` at the request top level and the API will apply it to the last cacheable position automatically. This simplifies caching for common single-turn or system-prompt-heavy request patterns.
  - *Source*: [messages/create.md (REST)](https://platform.claude.com/docs/en/api/messages/create.md), [messages/count_tokens.md (REST)](https://platform.claude.com/docs/en/api/messages/count_tokens.md), [beta/messages/create.md](https://platform.claude.com/docs/en/api/beta/messages/create.md), [messages/batches/create.md (REST)](https://platform.claude.com/docs/en/api/messages/batches/create.md)

---

### `allowed_callers` Enum Extended to Include `code_execution_20260120`

- **All server tool types now accept `"code_execution_20260120"` as a caller**: The `allowed_callers` parameter on every server tool type (bash tools, computer use tools, web search, web fetch, text editor, memory, tool search) has been updated to accept the new code execution version as a valid caller.

  Before:
  > `allowed_callers: optional array of "direct" or "code_execution_20250825"`

  After:
  > `allowed_callers: optional array of "direct" or "code_execution_20250825" or "code_execution_20260120"`

  - *Implication*: Tool orchestration setups that restrict which callers can invoke tools must be updated to explicitly permit (or deny) `"code_execution_20260120"` if needed. By default (no `allowed_callers` set), all callers remain permitted.
  - *Source*: [beta/messages.md (REST)](https://platform.claude.com/docs/en/api/beta/messages.md), [messages.md (REST)](https://platform.claude.com/docs/en/api/messages.md)

---

### `speed` Parameter Removed from Java and C# SDK Docs

- **Java SDK**: `speed: optional "standard" or "fast"` removed from `messages/create.md` request parameters.
  > Previously documented as: `"The inference speed mode for this request. 'fast' enables high output-tokens-per-second inference."`

- **C# SDK**: `Speed? speed` removed from the Messages domain types in `csharp/messages.md`. The position in the param ordering is now occupied by `CacheControlEphemeral? cacheControl`.

  - *Implication*: The `speed` parameter appears to be deprecated and removed from the Java and C# SDK client libraries. Developers using `speed` in these SDKs should remove that parameter. The Python, TypeScript, Ruby, and Go SDK docs do not show this removal.
  - *Source*: [java/messages/create.md](https://platform.claude.com/docs/en/api/java/messages/create.md), [csharp/messages.md](https://platform.claude.com/docs/en/api/csharp/messages.md)

---

### Beta API — New C#, Go, and Java Beta Documentation

- **C# beta docs expanded**: `csharp/beta.md` and `csharp/beta/messages.md` each received +230 lines of new content (no deletions), representing a substantial addition of beta API domain type coverage for the C# SDK. The `csharp/beta/messages/batches/create.md` (+62), `csharp/beta/messages/count_tokens.md` (+44), and `csharp/beta/messages/create.md` (+44) were similarly expanded.

- **Go and Java beta docs expanded**: Both `go/beta.md` and `java/beta.md` received +231 lines of new content each (zero deletions), with parallel additions to their beta sub-pages.

  - *Implication*: C#, Go, and Java SDK users now have more complete beta API type coverage, bringing these SDKs closer to parity with Python and TypeScript for beta feature access.
  - *Source*: [csharp/beta.md](https://platform.claude.com/docs/en/api/csharp/beta.md), [go/beta.md](https://platform.claude.com/docs/en/api/go/beta.md), [java/beta.md](https://platform.claude.com/docs/en/api/java/beta.md)

---

## Migration Guidance

### Rename: `CodeExecution20260120` / `CallerServerToolCaller20260120` → `ServerToolCaller20260120`

If your code checks caller type names (e.g., in typed SDK responses), update the class/type name:

```python
# Python — Before
if isinstance(caller, CallerServerToolCaller20260120):
    ...

# Python — After
if isinstance(caller, ServerToolCaller20260120):
    ...
```

```typescript
// TypeScript — wire format unchanged, type guard by .type field
if (caller.type === "code_execution_20260120") { ... }
```

### Removal: `speed` parameter (Java and C# SDKs)

```java
// Java — Before
MessageCreateParams.builder()
    .speed(MessageCreateParams.Speed.FAST)
    ...

// Java — After (remove the speed parameter)
MessageCreateParams.builder()
    // speed parameter no longer available
    ...
```

---

## Notable Details

- **`defer_loading` is a new cross-tool pattern**: The parameter `defer_loading` (and `strict`) appear on `CodeExecutionTool20260120`, `WebFetchTool20260209`, and `WebSearchTool20260209`. This signals an emerging tool-loading architecture where tools can be registered but not injected into the system prompt until invoked via a tool search result (`tool_reference`). This is distinct from any existing lazy-loading mechanism and suggests infrastructure for large tool registries.

- **Version suffix date scheme**: The new tool versions use `20260120` (Jan 20, 2026) and `20260209` (Feb 9, 2026) as suffixes, consistent with Anthropic's dated versioning scheme for server tools. `web_search_20260209` and `web_fetch_20260209` share the same date, suggesting a coordinated release.

- **`WebSearchToolResultErrorCode` unifies two previously inconsistent type names**: The Go SDK previously used `WebSearchToolRequestErrorErrorCode` for the error code constants; these are now corrected to `WebSearchToolResultErrorCode`. This is a type-name fix, not a value change — the string values (`"max_uses_exceeded"`, `"too_many_requests"`, etc.) remain the same.

- **Top-level `cache_control` is separate from per-block `cache_control`**: The new request-level `cache_control` is additive — it does not replace per-block cache control annotations. Developers can use either or both.

- **Beta `cache_control` also added**: The top-level `cache_control` was added to both the beta Messages API (`BetaCacheControlEphemeral` type) and the non-beta API (`CacheControlEphemeral`), including within beta batch `params`.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `messages.md` (REST) | Modified | +779/-357 | 6 new domain type sections; `allowed_callers` extended to include `code_execution_20260120` |
| `ruby/messages.md` | Modified | +778/-356 | Same new types (Ruby SDK) |
| `go/messages.md` | Modified | +768/-374 | Same new types (Go SDK); Go constant name corrections for `WebSearchToolResultErrorCode` |
| `python/messages.md` | Modified | +700/-278 | Same new types (Python SDK) |
| `typescript/messages.md` | Modified | +623/-201 | Same new types (TypeScript SDK) |
| `java/messages.md` | Modified | +595/-201 | Same new types (Java SDK) |
| `csharp/messages.md` | Modified | +570/-202 | Same new types (C# SDK); `speed` removed, `cacheControl` added |
| `beta.md` (REST) | Modified | +370/-101 | Top-level `cache_control` added; `allowed_callers` extended |
| `beta/messages.md` (REST) | Modified | +370/-101 | Same as beta.md |
| `ruby/beta.md` | Modified | +370/-101 | Beta updates (Ruby SDK) |
| `python/beta.md` | Modified | +369/-100 | Beta updates (Python SDK) |
| `typescript/beta.md` | Modified | +369/-100 | Beta updates (TypeScript SDK) |
| `csharp/beta.md` | Modified | +230/-0 | New C# beta domain types coverage |
| `csharp/beta/messages.md` | Modified | +230/-0 | New C# beta messages types |
| `go/beta.md` | Modified | +231/-0 | New Go beta domain types coverage |
| `go/beta/messages.md` | Modified | +231/-0 | New Go beta messages types |
| `java/beta.md` | Modified | +231/-0 | New Java beta domain types coverage |
| `java/beta/messages.md` | Modified | +231/-0 | New Java beta messages types |
| `messages/create.md` (REST) | Modified | +88/-51 | `ServerToolCaller20260120` rename; `WebSearchToolResultErrorCode` type ref |
| `ruby/messages/create.md` | Modified | +88/-51 | Same renames (Ruby SDK) |
| `python/messages/create.md` | Modified | +79/-42 | `cache_control` top-level added; class rename |
| `messages/count_tokens.md` (REST) | Modified | +79/-34 | `cache_control` top-level added |
| `ruby/messages/count_tokens.md` | Modified | +79/-34 | Same (Ruby SDK) |
| `messages/batches/create.md` (REST) | Modified | +79/-34 | `params` updated (18→19 params); `cache_control` in beta batches |
| `ruby/messages/batches/create.md` | Modified | +79/-34 | Same (Ruby SDK) |
| `go/messages/batches.md` | Modified | +121/-106 | Batches updates (Go SDK) |
| `messages/batches.md` (REST) | Modified | +115/-102 | Batches updates |
| `ruby/messages/batches.md` | Modified | +115/-102 | Batches updates (Ruby SDK) |
| `go/messages/count_tokens.md` | Modified | +58/-30 | Count tokens updates (Go SDK) |
| `java/messages/create.md` | Modified | +49/-29 | `speed` param removed; cache_control added |
| `csharp/messages/create.md` | Modified | +49/-29 | Class renames; `cacheControl` added |
| `go/messages/create.md` | Modified | +69/-49 | Class renames; cache_control added (Go SDK) |
| `typescript/messages/create.md` | Modified | +70/-33 | Class renames; cache_control added (TS SDK) |
| `typescript/messages/count_tokens.md` | Modified | +69/-24 | Count tokens updates (TS SDK) |
| *(beta sub-pages, all SDKs)* | Modified | +44 to +84/-0 to -21 | Beta endpoint docs updates matching above changes |

---

*Generated from Claude API documentation changes detected on 2026-02-21*
