# Claude API Documentation Changes — 2026-04-11

## Summary

A new beta **Advisor tool** (`advisor_20260301`) has been documented, enabling a dual-model pattern where a faster executor model can call a higher-intelligence advisor model mid-generation for strategic guidance. Alongside this, the code execution tool and programmatic tool calling pages received explicit per-model compatibility tables replacing the previous generic descriptions.

---

## Significant Changes

### Tools — New: Advisor Tool (Beta)

- **New server-side tool `advisor_20260301`**: Allows a faster, lower-cost executor model to consult a more capable advisor model during generation — server-side, within a single `/v1/messages` call. No extra API round-trips required from the client.

  > "The advisor tool lets a faster, lower-cost **executor model** consult a higher-intelligence **advisor model** mid-generation for strategic guidance. The advisor reads the full conversation, produces a plan or course correction (typically 400 to 700 text tokens, 1,400 to 1,800 tokens total including thinking), and the executor continues with the task."

  - *Beta header*: Include `anthropic-beta: advisor-tool-2026-03-01` in requests.
  - *Activation*: Tool type `"advisor_20260301"`, name must be `"advisor"`. Access requires contacting your Anthropic account team.
  - *Source*: [Advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md)

- **Supported model pairs** (executor → advisor):

  | Executor | Advisor |
  |----------|---------|
  | `claude-haiku-4-5-20251001` | `claude-opus-4-6` |
  | `claude-sonnet-4-6` | `claude-opus-4-6` |
  | `claude-opus-4-6` | `claude-opus-4-6` |

  > "If you request an invalid pair, the API returns a `400 invalid_request_error` naming the unsupported combination."

  - *Implication*: Developers must explicitly form valid executor/advisor pairs; the advisor must be at least as capable as the executor.
  - *Source*: [Advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md)

- **Tool parameters**:

  | Parameter | Type | Default | Description |
  |-----------|------|---------|-------------|
  | `type` | string | required | Must be `"advisor_20260301"` |
  | `name` | string | required | Must be `"advisor"` |
  | `model` | string | required | Advisor model ID (e.g. `"claude-opus-4-6"`) |
  | `max_uses` | integer | unlimited | Per-request cap on advisor calls |
  | `caching` | object\|null | `null` | Enables advisor-side prompt caching; shape: `{"type": "ephemeral", "ttl": "5m" \| "1h"}` |

  - *Implication*: `max_uses` enforces a per-request cap; when exceeded, advisor calls return `advisor_tool_result_error` with `error_code: "max_uses_exceeded"` and the executor continues. Conversation-level caps must be managed client-side.
  - *Source*: [Advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md)

- **New response content block types**: `server_tool_use` (with `name: "advisor"` and empty `input`) and `advisor_tool_result` (carrying either `advisor_result` with `text`, or `advisor_redacted_result` with `encrypted_content`).

  > "When the advisor is invoked, a `server_tool_use` block is followed by an `advisor_tool_result` block in the assistant's content."

  - *Implication*: Clients must pass the full assistant content (including `advisor_tool_result` blocks) verbatim on subsequent turns. Omitting the advisor tool from `tools` when history contains `advisor_tool_result` blocks returns a `400 invalid_request_error`.
  - *Source*: [Advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md)

- **New usage field `usage.iterations[]`**: Advisor sub-inference tokens appear as entries with `type: "advisor_message"` in the `usage.iterations` array. Advisor tokens are **not** rolled into the top-level `usage` totals, which reflect executor tokens only.

  > "Top-level `usage` fields reflect executor tokens only. Advisor tokens are not rolled into the top-level totals because they are billed at a different rate."

  - *Implication*: Cost-tracking logic must read `usage.iterations` to account for advisor billing; top-level token counts will undercount total spend when the advisor is used.
  - *Source*: [Advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md)

- **SDK support**: Code examples provided for Shell (curl), CLI (`ant`), Python, TypeScript, C#, Go, PHP, and Ruby.

- **Advisor error codes**:

  | `error_code` | Meaning |
  |---|---|
  | `max_uses_exceeded` | Per-request cap reached |
  | `too_many_requests` | Advisor sub-inference rate-limited |
  | `overloaded` | Advisor capacity exceeded |
  | `prompt_too_long` | Transcript exceeded advisor context window |
  | `execution_time_exceeded` | Advisor sub-inference timed out |
  | `unavailable` | Any other advisor failure |

  - *Implication*: Advisor failures surface as error results inside `advisor_tool_result`, not as HTTP-level failures (except for executor rate limits, which still return HTTP 429).
  - *Source*: [Advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md)

- **`context-editing` / `clear_thinking` interaction**: Using `clear_thinking` with a `keep` value other than `"all"` shifts the advisor's transcript and causes advisor-side cache misses. The API defaults to `keep: {type: "thinking_turns", value: 1}` when extended thinking is on without explicit configuration; set `keep: "all"` to maintain cache stability.

  - *Source*: [Advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md)

---

### Tools — Code Execution Model Compatibility Clarified

- **Explicit per-model compatibility table for code execution tool**: The previous documentation stated the tool was "available on all supported Claude models using tool version `code_execution_20250825`." This has been replaced with a detailed per-model table.

  > "`code_execution_20260120` adds REPL state persistence and programmatic tool calling from within the sandbox, and is available on Opus 4.5+ and Sonnet 4.5+ only."

  Highlighted: `code_execution_20260120` is **not** available on Claude Haiku 4.5, Opus 4.1, Opus 4, Sonnet 4, Sonnet 3.7, or Haiku 3.5.

  | Model | Tool versions |
  |-------|--------------|
  | Claude Opus 4.6 | `code_execution_20250825`, `code_execution_20260120` |
  | Claude Sonnet 4.6 | `code_execution_20250825`, `code_execution_20260120` |
  | Claude Opus 4.5 | `code_execution_20250825`, `code_execution_20260120` |
  | Claude Sonnet 4.5 | `code_execution_20250825`, `code_execution_20260120` |
  | Claude Haiku 4.5 | `code_execution_20250825` only |
  | Claude Opus 4.1 | `code_execution_20250825` only |
  | Claude Opus 4 | `code_execution_20250825` only |
  | Claude Sonnet 4 | `code_execution_20250825` only |
  | Claude Sonnet 3.7 (deprecated) | `code_execution_20250825` only |
  | Claude Haiku 3.5 (deprecated) | `code_execution_20250825` only |

  - *Implication*: Code that uses `code_execution_20260120` (REPL persistence, programmatic tool calling) will fail on Haiku 4.5 and all pre-4.5 models. Developers who previously relied on "all models" phrasing and assumed `code_execution_20260120` worked everywhere need to verify model selection.
  - *Source*: [Code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

---

### Tools — Programmatic Tool Calling Model Compatibility Clarified

- **Explicit model list for programmatic tool calling**: Previously pointed to the tool reference for compatibility details. Now states the supported models directly.

  > "Programmatic tool calling requires `code_execution_20260120`, which is supported on the following models: Claude Opus 4.6, Claude Sonnet 4.6, Claude Opus 4.5, Claude Sonnet 4.5."

  - *Implication*: Haiku 4.5 and older models are explicitly excluded from programmatic tool calling. The page now links to the code execution tool compatibility table for the full version matrix.
  - *Source*: [Programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md)

---

### Tools — Tool Reference Table Updated

- **Advisor tool added to the Anthropic-provided tools table** in the tool reference, listed as a server tool with `type: advisor_20260301` and status `Beta: advisor-tool-2026-03-01`.

  - *Source*: [Tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference.md)

---

## New Pages

- **[advisor-tool.md]** — Full documentation for the new Advisor tool beta, including quick start, how it works, tool parameters, response structure, multi-turn conversation handling, streaming behavior, usage/billing breakdown, prompt caching configuration, composition with other tools, best practice system prompts, cost control guidance, and known limitations. [View](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md)

---

## Notable Details

- **Streaming behavior**: The advisor sub-inference does not stream. The executor's SSE stream pauses while the advisor runs; keepalive `ping` events are emitted roughly every 30 seconds during the pause. When the advisor finishes, the full `advisor_tool_result` arrives in a single `content_block_start` event (no deltas), and executor output resumes.
- **`max_tokens` scope**: `max_tokens` on the request applies to executor output only and does not bound advisor sub-inference tokens. Advisor tokens also do not draw from any task budget applied to the executor.
- **Priority Tier**: Anthropic Priority Tier is honored per model; Priority Tier on the executor does not extend to the advisor.
- **Batch processing**: The advisor tool is compatible with batch processing; `usage.iterations` is reported per item.
- **`clear_tool_uses` not yet compatible**: Context editing's `clear_tool_uses` is not yet fully compatible with advisor tool blocks; full support is planned for a follow-up release.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `agents-and-tools/tool-use/advisor-tool.md` | New | +630 | Full documentation for the Advisor tool beta |
| `agents-and-tools/tool-use/code-execution-tool.md` | Modified | +15/-2 | Replaced generic model compatibility note with explicit per-model table; clarified `code_execution_20260120` scope |
| `agents-and-tools/tool-use/programmatic-tool-calling.md` | Modified | +10/-1 | Added explicit model compatibility table; links to code execution table for full version matrix |
| `agents-and-tools/tool-use/tool-reference.md` | Modified | +27/-24 | Added advisor tool row to Anthropic-provided tools table; table formatting improvements |

---

*Generated from Claude API documentation changes detected on 2026-04-11*
