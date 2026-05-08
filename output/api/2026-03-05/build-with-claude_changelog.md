# Claude API Documentation Changes — 2026-03-05

## Summary

This update documents a large-scale expansion of multi-language SDK examples across nearly all "Build with Claude" pages, adding C#, Go, Java, PHP, and Ruby code alongside the existing Python, TypeScript, and Shell examples. Two meaningful API-level changes are included: structured outputs is now generally available with a renamed parameter (`output_format` → `output_config.format`), and the "thinking redaction" documentation has been removed from both the extended thinking and adaptive thinking pages. The Ruby SDK is newly listed as supporting client-side compaction.

## Significant Changes

### Structured Outputs — GA with Parameter Rename

- **`output_format` renamed to `output_config.format`; beta header no longer required**: Structured outputs have graduated from beta. The parameter previously at `output_format` is now `output_config.format`, and the old beta header `structured-outputs-2025-11-13` is no longer needed.
  > **Migrating from beta?** The `output_format` parameter has moved to `output_config.format`, and beta headers are no longer required. The old beta header (`structured-outputs-2025-11-13`) and `output_format` parameter will continue working for a transition period.
  - *Implication*: Developers using the old `output_format` shape or beta header should update their requests, though both old forms remain functional during a transition period.
  - *Source*: [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **Supported models explicitly listed**: Structured outputs are generally available on Claude Opus 4.6, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.5, and Claude Haiku 4.5 on the Claude API and Amazon Bedrock. Public beta on Microsoft Foundry.
  - *Source*: [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

### Thinking — Redaction Documentation Removed

- **"Thinking redaction" section removed from extended thinking and adaptive thinking pages**: The `### Thinking redaction` section—which documented `redacted_thinking` blocks, the special prompts to trigger them, and how to handle them in multi-turn conversations—has been deleted from both `extended-thinking.md` and `adaptive-thinking.md`. The current documentation makes no mention of redacted thinking.
  - *Implication*: Thinking redaction appears to be deprecated or no longer supported as a user-facing feature. Developers relying on `redacted_thinking` block handling should test whether the behavior persists and not rely on it going forward.
  - *Source*: [Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md), [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md)

- **`thinking.type: "enabled"` and `budget_tokens` deprecated on Opus 4.6 and Sonnet 4.6**: The documentation now explicitly states these are deprecated on the newer model versions, with removal planned in a future release.
  > `thinking.type: "enabled"` and `budget_tokens` are **deprecated** on Opus 4.6 and Sonnet 4.6 and will be removed in a future model release. Use `thinking.type: "adaptive"` with the `effort` parameter instead.
  - *Implication*: Update Opus 4.6 and Sonnet 4.6 integrations to use `thinking.type: "adaptive"` with `output_config.effort`. Older models (Sonnet 4.5, Opus 4.5, etc.) still require `type: "enabled"` with `budget_tokens`.
  - *Source*: [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md)

### Context Editing — Ruby SDK Now Supported for Client-Side Compaction

- **Ruby SDK added to client-side compaction support**: The comparison table in the context editing docs was updated to reflect that client-side compaction is now available in Python, TypeScript, **and Ruby** SDKs (previously only Python and TypeScript were listed).
  > Available in [Python, TypeScript, and Ruby SDKs](/docs/en/api/client-sdks) when using `tool_runner`.
  - *Implication*: Ruby SDK users can now use `tool_runner`-based client-side compaction in agentic workflows.
  - *Source*: [Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing.md)

## SDK Coverage Expansion

The most volumetrically significant change in this update is a broad addition of C#, Go, Java, PHP, and Ruby code examples across documentation that previously showed only Python, TypeScript, and Shell (curl). This affects the following pages:

| Page | SDKs Added |
|------|-----------|
| Adaptive thinking | C#, Go, Java, PHP, Ruby (basic usage + effort + streaming) |
| Effort | Shell (curl), C#, Go, Java, PHP, Ruby |
| Compaction | PHP, Ruby |
| Context editing (tool result clearing) | C#, Go, Java, PHP, Ruby |
| Context windows (1M context) | C#, Go, Java, PHP, Ruby |
| Streaming | C#, Go, Java, PHP, Ruby |
| Token counting | C#, Go, Java, PHP, Ruby |
| Prompt caching | C#, Go, Java, PHP, Ruby |
| Working with messages | C#, Go, Java, PHP, Ruby (including image handling) |
| Files API | C#, Go, Java, PHP, Ruby (updated examples) |
| Skills guide | C#, Go, Java, PHP, Ruby (file download, version management, multi-skill) |
| Batch processing | C#, Go, Java, PHP, Ruby; Ruby auto-fetch pagination added |
| Search results | C#, Go, Java, PHP, Ruby |
| Extended thinking | C#, Go, Java, PHP, Ruby |
| Structured outputs | C#, Go, Java, PHP, Ruby |
| Claude on Amazon Bedrock | C#, Go, Java, PHP, Ruby (listing models + making requests) |
| Claude on Vertex AI | C#, Go, Java, PHP, Ruby |
| Claude in Microsoft Foundry | C#, Go, Java, PHP, Ruby |
| Vision | Updated examples |
| PDF support | Updated examples |

This suggests a coordinated effort to bring all six official SDKs (Python, TypeScript, C#, Go, Java, Ruby) and the community PHP SDK to parity across the developer documentation.

## Migration Guidance

### Structured Outputs Parameter Rename

Update requests from `output_format` to `output_config.format`, and remove the `structured-outputs-2025-11-13` beta header:

```python
# Before (old beta form)
response = client.beta.messages.create(
    betas=["structured-outputs-2025-11-13"],
    output_format={"type": "json_schema", "schema": {...}},
    ...
)

# After (GA form)
response = client.messages.create(
    output_config={"format": {"type": "json_schema", "schema": {...}}},
    ...
)
```

### Adaptive Thinking on Opus 4.6 / Sonnet 4.6

```python
# Before (deprecated on Opus 4.6 / Sonnet 4.6)
response = client.messages.create(
    model="claude-opus-4-6",
    thinking={"type": "enabled", "budget_tokens": 10000},
    ...
)

# After (recommended)
response = client.messages.create(
    model="claude-opus-4-6",
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},  # "high" is the default
    ...
)
```

## Notable Details

- **`output_config.effort` in same request as `thinking.type: "adaptive"`**: The effort parameter is placed inside `output_config` (not at the top level), and is used alongside `thinking: {type: "adaptive"}`. This is consistent across all SDK examples shown in the adaptive thinking and effort pages.

- **Compaction beta header**: The compaction feature uses `compact-2026-01-12` as its beta header (note the 2026 year), and the edit type is `compact_20260112`. Both reflect the January 2026 launch date of this feature.

- **ZDR eligibility note on prompt caching**: A new note clarifies that prompt caching stores KV cache representations and cryptographic hashes but not raw prompt text, and may be suitable for customers with ZDR-type commitments — a meaningful privacy clarification for enterprise customers.

- **Context editing default thinking behavior clarified**: The docs now explicitly state the default behavior when extended thinking is enabled without configuring `clear_thinking_20251015`: only the last assistant turn's thinking blocks are kept (`keep: {type: "thinking_turns", value: 1}`). To maximize cache hits, set `keep: "all"`.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| skills-guide.md | Modified | +3782/-386 | Extensive SDK example expansion; file download, version management, multi-skill workflows |
| structured-outputs.md | Modified | +2216/-428 | GA release; `output_format` → `output_config.format`; beta header removed; full SDK coverage |
| extended-thinking.md | Modified | +2124/-287 | Thinking redaction section removed; multi-SDK examples added; deprecation warnings for `budget_tokens` on v4.6 models |
| compaction.md | Modified | +2246/-62 | PHP and Ruby examples added; pause-after-compaction pattern documented |
| context-editing.md | Modified | +1622/-27 | Ruby SDK added to client-side compaction; C#, Go, Java, PHP, Ruby examples for tool result clearing |
| prompt-caching.md | Modified | +1246/-22 | Automatic caching documented at top level; full multi-SDK coverage; ZDR clarification |
| streaming.md | Modified | +947/-44 | C#, Go, Java, PHP, Ruby examples added throughout |
| batch-processing.md | Modified | +827/-169 | Multi-SDK examples; Ruby auto-fetch pagination |
| search-results.md | Modified | +826/-53 | Full multi-SDK coverage added |
| token-counting.md | Modified | +806/-62 | Multi-SDK examples added |
| files.md | Modified | +725/-177 | SDK examples updated; C#, Go, Java, PHP, Ruby parity |
| working-with-messages.md | Modified | +706/-7 | Multi-SDK examples; image handling (base64 + URL) |
| context-windows.md | Modified | +118/-3 | Multi-SDK examples for 1M context beta |
| adaptive-thinking.md | Modified | +506/-70 | Thinking redaction section removed; C#, Go, Java, PHP, Ruby examples added |
| claude-on-amazon-bedrock.md | Modified | +362/-131 | C#, Go, Java, PHP, Ruby examples; model listing examples added; Java example replaced with C# |
| claude-on-vertex-ai.md | Modified | +285/-107 | Multi-SDK examples added |
| effort.md | Modified | +149/-19 | Shell (curl) example added first; C#, Go, Java, PHP, Ruby examples |
| fast-mode.md | Modified | +133/-42 | Code example updates |
| handling-stop-reasons.md | Modified | +62/-16 | Example updates |
| pdf-support.md | Modified | +86/-52 | Example updates |
| claude-in-microsoft-foundry.md | Modified | +177/-84 | Multi-SDK examples updated |
| vision.md | Modified | +125/-85 | Example updates |
| citations.md | Modified | +37/-36 | Minor example updates |
| data-residency.md | Modified | +5/-2 | TypeScript example type safety fix |
| embeddings.md | Modified | +6/-5 | Minor updates |
| multilingual-support.md | Modified | +1/-4 | Minor text updates |
| prompt-engineering/claude-prompting-best-practices.md | Modified | +5/-5 | Minor updates |
| prompt-engineering/prompting-tools.md | Modified | +0/-3 | Lines removed |

---
*Generated from Claude API documentation changes detected on 2026-03-05*
