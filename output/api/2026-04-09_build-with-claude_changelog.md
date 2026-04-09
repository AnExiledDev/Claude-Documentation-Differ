# Claude API Documentation Changes — 2026-04-09

## Summary

28 pages in the `build-with-claude` documentation were updated (+2,615 / -145 lines). The dominant theme is the addition of `ant` CLI examples across virtually every feature page, and the addition of **Claude Mythos Preview** (`claude-mythos-preview`) to the supported-models list for adaptive thinking, compaction, context windows, effort, prompt caching, and extended thinking. A secondary theme is the GA promotion of structured outputs from beta (the `output_format` parameter has moved to `output_config.format`), and a new Vertex AI multi-region endpoint type.

---

## Significant Changes

### Claude Mythos Preview — New Model Documented

- **Claude Mythos Preview added across core feature pages**: The model `claude-mythos-preview` now appears in the supported-models lists for adaptive thinking, extended thinking, compaction, prompt caching, effort control, and context windows. It is described as a research preview available to invited customers on the Anthropic API, Amazon Bedrock, Vertex AI, and Microsoft Foundry.

  > Adaptive thinking is the recommended way to use extended thinking with Claude Opus 4.6 and Claude Sonnet 4.6, and is the default mode on [Claude Mythos Preview](https://anthropic.com/glasswing) (where it auto-applies whenever `thinking` is unset).

  Key behavior differences from other Claude 4 models:
  - **Adaptive thinking is the default**; `thinking: {type: "disabled"}` is rejected (returns 400).
  - **`display` defaults to `"omitted"`** rather than `"summarized"` — developers must pass `display: "summarized"` explicitly to receive thinking summaries.
  - Summarization begins from the first token (no verbose preamble seen in Claude 4 models).
  - Inter-tool reasoning automatically moves into thinking blocks; the `interleaved-thinking-2025-05-14` beta header is not needed or supported.
  - **Prefilled last-assistant-turn messages return a 400 error** (other models silently ignore them; on Mythos Preview this is enforced).
  - **1M-token context window**, same as Opus 4.6 and Sonnet 4.6.
  - Effort parameter includes `max` level support.
  - Minimum cacheable prompt length is 4,096 tokens (same as Opus 4.6 / Opus 4.5).

  - *Implication*: Developers targeting Mythos Preview must audit their code for `thinking: {type: "disabled"}`, prefilled assistant messages, and thinking display logic before switching to this model.
  - *Sources*: [Adaptive Thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md), [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md), [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction.md), [Context Windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md), [Effort](https://platform.claude.com/docs/en/build-with-claude/effort.md), [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

### Structured Outputs — `output_format` Promoted to `output_config.format`

- **API parameter rename, beta header removed**: The structured outputs feature is now generally available. The `output_format` request parameter has moved to `output_config.format`. The old beta header (`structured-outputs-2025-11-13`) and the `output_format` parameter continue to work during a transition period.

  > **Migrating from beta?** The `output_format` parameter has moved to `output_config.format`, and beta headers are no longer required. The old beta header (`structured-outputs-2025-11-13`) and `output_format` parameter will continue working for a transition period.

  - Availability note added: generally available on the Claude API and Amazon Bedrock for Claude Mythos Preview, Claude Opus 4.6, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.5, and Claude Haiku 4.5. **In beta on Microsoft Foundry. Not supported on Vertex AI for Claude Mythos Preview.**
  - SDK helper methods (`.parse()`, Pydantic/Zod integrations) still accept `output_format` as a convenience alias; the SDK translates internally.

  - *Implication*: Update API calls to use `output_config.format` when removing the beta header. No functional change during the transition period.
  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

### Extended Thinking — New `redacted_thinking` Block Type Documented

- **`redacted_thinking` content blocks**: A new section documents a block type that the API may return when portions of thinking are safety-redacted. These blocks carry an opaque encrypted `data` field and must be passed back to the API unchanged in multi-turn conversations with tools.

  > ```json
  > {
  >   "type": "redacted_thinking",
  >   "data": "..."
  > }
  > ```
  >
  > If your code filters content blocks by type (for example, `block.type == "thinking"`) when round-tripping responses with tool use, also include `redacted_thinking` blocks. Filtering on `block.type == "thinking"` alone silently drops `redacted_thinking` blocks and breaks the multi-turn protocol.

  - *Implication*: Agent loops that filter content blocks to extract thinking blocks must also handle `redacted_thinking` to avoid breaking multi-turn tool use.
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

### Vertex AI — Multi-Region Endpoints Added

- **New endpoint type between global and regional**: The "Global vs regional endpoints" section has been renamed to **"Global, multi-region, and regional endpoints"** and a third tier documented.

  > **Multi-region endpoints:**
  > - Dynamically route requests across regions within a geographic area (currently `us`, with `eu` coming soon)
  > - Useful when you need data residency within a broad geography but want higher availability than a single region
  > - 10% pricing premium over global endpoints
  > - Only supports pay-as-you-go traffic (provisioned throughput requires regional endpoints)

  Multi-region is set by passing a short code like `"us"` as the `region` parameter. SDK examples added for Python, TypeScript, C#, Go, Java, PHP, and Ruby.

  - *Implication*: Developers with US data-residency requirements but who previously used global endpoints for availability now have an intermediate option.
  - *Source*: [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

### Amazon Bedrock — Legacy Integration Disambiguation

- **New note distinguishing the legacy Bedrock integration**: The `claude-on-amazon-bedrock.md` page now opens with a note clarifying it covers the legacy `InvokeModel` API with ARN-versioned model identifiers and AWS event-stream encoding:

  > This page covers the legacy Amazon Bedrock integration (the `InvokeModel` API with ARN-versioned model identifiers and AWS event-stream encoding). For the new AWS-managed offering with the Messages API at `/anthropic/v1/messages` and SSE streaming, see [Claude in Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock).

  - *Implication*: Developers starting a new Bedrock integration should navigate to `claude-in-amazon-bedrock.md`, not this page.
  - *Source*: [Claude on Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md)

### Java SDK Version Bump (2.18.0 → 2.20.0)

- **`anthropic-java-foundry`, `anthropic-java-bedrock`, `anthropic-java-vertex`** all updated from `2.18.0` to `2.20.0` in Gradle and Maven dependency snippets across the respective platform pages.
  - *Sources*: [Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md), [Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md), [Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

### Prompt Caching — Supported Models Simplified

- **Model list replaced with a blanket statement**: The explicit enumeration of supported models was replaced with:
  > Prompt caching (both automatic and explicit) is supported on all [active Claude models](/docs/en/about-claude/models/overview).

  The FAQ answer was updated to match. The 4,096-token minimum cache length now explicitly includes Claude Mythos Preview alongside Opus 4.6 and Opus 4.5.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

### Context Editing — Model Support Simplified

- **Explicit model list replaced**: The `context-editing.md` supported models list (previously enumerating 9 specific model IDs) was replaced with:
  > Context editing is available on all supported Claude models.
  - *Source*: [Context Editing](https://platform.claude.com/docs/en/build-with-claude/context-editing.md)

### Extended Thinking — Model Support Simplified

- **Explicit model list replaced**: The `extended-thinking.md` supported models list (previously 10 named models) was replaced with:
  > Extended thinking is supported on all supported Claude models. A few models have mode-specific behavior: [Claude Mythos Preview, Opus 4.6, Sonnet 4.6 notes follow].
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

### Batch Processing — Error Type Correction

- **`invalid_request` → `invalid_request_error`**: Code examples checking the batch error type were corrected in both Shell and Python:

  ```diff
  - if [ "$error_type" = "invalid_request" ]; then
  + if [ "$error_type" = "invalid_request_error" ]; then
  ```

  ```diff
  - if result.result.error.type == "invalid_request":
  + if result.result.error.error.type == "invalid_request_error":
  ```

  - *Implication*: Existing code that checks for `"invalid_request"` when handling errored batch results will miss the match. The corrected path is `result.result.error.error.type`.
  - *Source*: [Batch Processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing.md)

---

## Notable Details

- **Prefill enforcement on Mythos Preview**: The prompting best-practices page notes that on Claude Mythos Preview, prefilled last-turn assistant messages return a 400 error (not just silently ignored as on older models). *Source*: [Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

- **`dynamic-filtering` anchor fix**: Links to the dynamic filtering section in `web-search-tool` were updated from `#dynamic-filtering-with-opus-4-6-and-sonnet-4-6` to `#dynamic-filtering` in `api-and-data-retention.md` and `overview.md`.

- **API reference link normalization**: Many internal links pointing to `/docs/en/api/messages` were updated to `/docs/en/api/messages/create` across batch processing, extended thinking, files, handling stop reasons, and Vertex AI pages.

- **`ant` CLI — bedrock and Vertex AI not yet supported**: Every Shell code block in `claude-on-amazon-bedrock.md` and `claude-on-vertex-ai.md` that previously had no CLI tab now has a stub: `# The ant CLI does not yet support Amazon Bedrock.` / `# The ant CLI does not yet support Vertex AI.`

- **`ant` CLI — `--inference-geo` flag**: The data residency page adds a CLI example using `--inference-geo us`.

- **`ant` CLI — `--transform-error` flag**: The fast-mode fallback pattern introduces `--transform-error error.type --format-error yaml` for branching on error type in shell scripts.

- **Thinking model comparison table expanded**: The differences table in `extended-thinking.md` now includes a Claude Mythos Preview column documenting that thinking is omitted by default, inter-tool reasoning always lives inside thinking blocks, and thinking blocks are preserved across turns (with a note that blocks are stripped when continuing on a model that does not support the Mythos thinking format).

- **`api-and-data-retention.md`**: The related links section at the bottom removed the "Agent SDK Sessions" entry.

---

## `ant` CLI Examples — Bulk Addition

The majority of the line additions across this diff consist of new `ant` CLI tab examples added alongside existing Shell/Python/TypeScript/etc. examples. Affected pages and the features they cover:

| Page | CLI Examples Added For |
|------|------------------------|
| `adaptive-thinking.md` | Basic adaptive thinking, structured output with effort, streaming |
| `batch-processing.md` | Create batch, polling, list, cancel, results, prompt caching with batch, 300k output beta |
| `citations.md` | Basic citations, citations with caching |
| `claude-in-microsoft-foundry.md` | Basic messages with `--base-url` |
| `compaction.md` | Basic compaction, trigger config, custom instructions, pause-and-preserve, streaming, token counting, full loop |
| `context-editing.md` | Tool use clearing, thinking clearing, combined strategies, token counting |
| `data-residency.md` | `--inference-geo` flag usage |
| `effort.md` | `output_config.effort` parameter |
| `extended-thinking.md` | Basic thinking, omitted display, streaming, tool use multi-turn, prompt caching interaction |
| `fast-mode.md` | Fast speed, usage check, 429-fallback pattern |
| `files.md` | Upload, reference in message, inline `@` path, list, metadata, delete, download |
| `handling-stop-reasons.md` | `max_tokens` truncation retry |
| `pdf-support.md` | URL source, base64 source, Files API source, caching, batches |
| `prompt-caching.md` | System caching, multi-turn caching, tool caching, large document caching |
| `search-results.md` | Multi-result with citations |
| `skills-guide.md` | Basic skill use, file download, file management, container reuse, `pause_turn` loop, Skills API CRUD, custom skills, caching |
| `streaming.md` | `--stream` flag raw events |
| `structured-outputs.md` | `output_config.format`, strict tool use |
| `token-counting.md` | Token counting for various request types |
| `vision.md` | URL image, base64 image, Files API image |
| `working-with-messages.md` | Multi-turn, base64 image, URL image |

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| skills-guide.md | Modified | +400/-5 | Extensive `ant` CLI examples for all Skills API operations |
| extended-thinking.md | Modified | +297/-29 | Mythos Preview model docs, `redacted_thinking` section, CLI examples, thinking comparison table expansion |
| structured-outputs.md | Modified | +233/-3 | `output_config.format` GA promotion, multi-SDK examples with new parameter shape |
| claude-on-vertex-ai.md | Modified | +198/-9 | Multi-region endpoint type added; Java SDK 2.20.0; CLI stubs |
| prompt-caching.md | Modified | +177/-15 | CLI examples, model list simplified, Mythos Preview added to min-cache-length |
| compaction.md | Modified | +213/-2 | Mythos Preview added to supported models; extensive CLI examples |
| context-editing.md | Modified | +154/-13 | Model support simplified to "all models"; CLI examples |
| batch-processing.md | Modified | +154/-7 | CLI examples; error type corrected (`invalid_request_error`) |
| token-counting.md | Modified | +93/-5 | CLI examples |
| pdf-support.md | Modified | +118/-1 | CLI examples; API reference link fix |
| vision.md | Modified | +65/-3 | CLI examples for URL, base64, and Files API image inputs |
| fast-mode.md | Modified | +64/-1 | CLI examples including 429-fallback pattern |
| files.md | Modified | +64/-3 | CLI examples for all Files API operations |
| streaming.md | Modified | +71/-0 | CLI `--stream` flag examples |
| adaptive-thinking.md | Modified | +46/-9 | Mythos Preview model docs; CLI examples |
| citations.md | Modified | +42/-0 | CLI examples |
| search-results.md | Modified | +36/-0 | CLI multi-result example |
| working-with-messages.md | Modified | +80/-6 | CLI examples for multi-turn and image messages |
| claude-in-microsoft-foundry.md | Modified | +23/-4 | CLI example; Java SDK 2.20.0; Mythos Preview note; link fix |
| claude-on-amazon-bedrock.md | Modified | +21/-3 | Legacy integration note; CLI stubs; Java SDK 2.20.0; Mythos Preview note |
| effort.md | Modified | +16/-3 | Mythos Preview support; CLI example |
| handling-stop-reasons.md | Modified | +23/-10 | CLI example; code block language annotations |
| data-residency.md | Modified | +10/-1 | CLI example; JSON label fix |
| context-windows.md | Modified | +1/-1 | Mythos Preview added to 1M-token context window list |
| prompt-engineering/claude-prompting-best-practices.md | Modified | +12/-8 | Prefill 400 error on Mythos Preview; code block language annotations |
| workspaces.md | Modified | +2/-1 | Minor copy edit |
| api-and-data-retention.md | Modified | +1/-2 | Anchor link fix; removed Agent SDK Sessions from related links |
| overview.md | Modified | +1/-1 | Dynamic filtering anchor fix |

---

*Generated from Claude API documentation changes detected on 2026-04-09*
