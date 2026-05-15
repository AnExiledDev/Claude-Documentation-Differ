# Claude API Documentation Changes — 2026-05-15

## Summary

Nine pages in the `build-with-claude` section were updated, with no new or removed pages. The most impactful changes are a new context window overflow behavior for Claude 4.5+ models (replacing the previous validation error approach), updated model lifecycle statuses across Batch API and prompt caching pricing tables, and revised platform-specific guidance for prompt caching minimums. Claude Sonnet 3.7 references have been largely removed from compatibility tables across multiple pages.

## Significant Changes

### Context Window Behavior

- **New overflow stop reason for Claude 4.5+ models**: The API behavior when input tokens plus `max_tokens` exceeds the context window has changed for Claude 4.5 and newer models. Instead of returning a validation error, the API now accepts the request and stops generation with `stop_reason: "model_context_window_exceeded"` when the limit is reached.
  > On Claude 4.5 models and newer, if input tokens plus `max_tokens` exceeds the context window size, the API accepts the request. If generation then reaches the context window limit, it stops with `stop_reason: "model_context_window_exceeded"`. On earlier models, the API returns a validation error instead; opt in to the `model_context_window_exceeded` behavior with the `model-context-window-exceeded-2025-08-26` beta header.
  - *Implication*: Developers using earlier models who want the new graceful overflow behavior (rather than a validation error) can opt in using the `model-context-window-exceeded-2025-08-26` beta header. Code that relies on catching a validation error to detect context overflow needs to be updated to also handle this new `stop_reason`.
  - *Source*: [Context Windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md)

### Extended Thinking

- **Claude Opus 4.7 thinking output now omitted by default**: The model comparison table for extended thinking was updated. Claude Opus 4.7 now shows thinking output as omitted by default (requiring `display: "summarized"` to receive summarized thinking), bringing it in line with Claude Mythos Preview behavior. Previously, this "omit by default" behavior was only documented for Claude Mythos Preview.
  > | **Thinking output** | Returns summarized thinking | Returns summarized thinking | Returns summarized thinking | Returns summarized thinking | Omitted by default; set `display: "summarized"` to receive summarized thinking | Omitted by default; set `display: "summarized"` to receive summarized thinking. Raw thinking tokens are never returned.

  - *Implication*: Developers using Claude Opus 4.7 who expect thinking blocks in responses must explicitly set `display: "summarized"` to receive them.
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

- **Claude Sonnet 3.7 removed from extended thinking comparison table**: The model version comparison table no longer includes Claude Sonnet 3.7 as a column. References to the Sonnet 3.7 → Claude 4 migration path and notes about Sonnet 3.7 returning full thinking output have been removed throughout the page.
  - *Implication*: Sonnet 3.7 is effectively end-of-life for extended thinking documentation purposes.
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

- **Context window overflow behavior aligned in extended thinking docs**: The extended thinking page now reflects the same new overflow policy — Claude 4.5+ models accept requests exceeding the context window and stop with `stop_reason: "model_context_window_exceeded"`.
  > `max_tokens` (which includes your thinking budget when thinking is enabled) is enforced as a strict limit. On Claude 4.5 models and newer, if input tokens plus `max_tokens` exceeds the context window size, the API accepts the request. If generation then reaches the context window limit, it stops with `stop_reason: "model_context_window_exceeded"`. On earlier models, the API returns a validation error instead.
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

### Model Lifecycle Updates (Batch API Pricing Table)

- **Claude Sonnet 4 and Claude Opus 4 marked deprecated; older models removed**: The Batches API pricing table has been updated. Claude Opus 4 and Claude Sonnet 4 are now explicitly flagged as deprecated. Claude Sonnet 3.7, Claude Haiku 3, and Claude Opus 3 have been removed from the table. Claude Haiku 3.5 is now labeled "retired, except on Bedrock and Vertex AI."
  - *Implication*: Developers still using Claude Sonnet 3.7, Claude Haiku 3, or Claude Opus 3 with the Batches API should plan migrations to supported models. Claude Haiku 3.5 remains available on Bedrock and Vertex AI but not on the Anthropic API.
  - *Source*: [Batch Processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing.md)

### Model Lifecycle Updates (Amazon Bedrock)

- **Claude Opus 4 retirement date on Bedrock moved up to May 31, 2026**: The previously documented Bedrock retirement date for Claude Opus 4 was October 14, 2026; it is now May 31, 2026 — over four months earlier.
  > Claude Opus 4 Deprecated. Retiring May 31, 2026.
  - *Implication*: Developers on Amazon Bedrock using Claude Opus 4 need to migrate significantly sooner than previously communicated.
  - *Source*: [Claude on Amazon Bedrock (Legacy)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy.md)

- **Claude Sonnet 3.7 now fully retired on Bedrock (all regions)**: Claude Sonnet 3.7 has been updated from partial regional availability to no availability across all Bedrock regions (global, us, eu, jp, apac all set to No). Retirement date updated to April 28, 2026.
  - *Implication*: Bedrock users on Claude Sonnet 3.7 must have already migrated or need to do so immediately.
  - *Source*: [Claude on Amazon Bedrock (Legacy)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy.md)

- **Claude Haiku 3.5 re-classified on Bedrock from Retired to Deprecated (retiring June 19, 2026)**: Previously shown as "Retired as of February 19, 2026," Haiku 3.5 is now listed as "Deprecated. Retiring June 19, 2026" on Bedrock — indicating continued availability until the June date.
  - *Implication*: Bedrock users of Haiku 3.5 have until June 19, 2026 before the model is retired on that platform.
  - *Source*: [Claude on Amazon Bedrock (Legacy)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy.md)

- **Lifecycle terminology disclaimer added to Bedrock model table**: A new paragraph clarifies that Bedrock retirement dates are set independently by AWS and may differ from the Anthropic-operated schedule.
  > Lifecycle terms (Deprecated, Retired) are defined in Model deprecations; a "Retiring" annotation gives the platform's announced retirement date. The dates in the following table are the **Amazon Bedrock** schedule, which AWS sets independently.
  - *Source*: [Claude on Amazon Bedrock (Legacy)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy.md)

### Model Lifecycle Updates (Vertex AI)

- **Claude Sonnet 3.7 retired on Vertex AI as of May 11, 2026**: Retirement date updated from an earlier February 19, 2026 reference to May 11, 2026.
  - *Source*: [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

- **Claude Haiku 3.5 re-classified on Vertex AI from Retired to Deprecated (retiring July 5, 2026)**: Like the Bedrock table, Haiku 3.5 is now shown as "Deprecated. Retiring July 5, 2026" rather than "Retired."
  - *Implication*: Vertex AI users of Haiku 3.5 have until July 5, 2026 before the model retires on that platform.
  - *Source*: [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

- **Lifecycle terminology disclaimer added to Vertex AI model table**: Identical disclaimer to the Bedrock page — Vertex AI dates are set by Google Cloud independently of Anthropic's schedule.
  - *Source*: [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

### Prompt Caching

- **Cache minimum token thresholds revised; Claude Sonnet 4.6 minimum lowered to 1,024**: The minimum cacheable prompt length for Claude Sonnet 4.6 has changed from 2,048 tokens to 1,024 tokens. The updated list consolidates several models at the 1,024-token threshold.
  > 1,024 tokens for Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.1, Claude Opus 4 (deprecated), and Claude Sonnet 4 (deprecated)
  - *Implication*: Prompts between 1,024 and 2,047 tokens on Claude Sonnet 4.6 that were previously uncacheable are now eligible for prompt caching, potentially reducing costs for those use cases.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **Platform-specific guidance added to cache limitations**: The cache limitations section now explicitly lists which platforms the minimums apply to (Claude API, Claude Platform on AWS, Vertex AI, Microsoft Foundry beta) and adds a note directing Bedrock users to Bedrock's own prompt caching documentation.
  > [Bedrock] is an AWS-operated platform. On Bedrock, see the [Bedrock prompt caching documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) for the per-model minimums, failure behavior, and usage-field names that apply.
  - *Implication*: Bedrock developers should not rely on the Anthropic docs for Bedrock-specific caching minimums or failure behavior — the Bedrock docs may differ.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **Prompt caching pricing table updated**: Claude Opus 4 and Claude Sonnet 4 are now marked deprecated. Claude Sonnet 3.7, Claude Haiku 3, and Claude Opus 3 have been removed. Claude Haiku 3.5 is now labeled "retired, except on Bedrock and Vertex AI."
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

## Minor Changes

- **adaptive-thinking.md**: Removed clause about summarization enabling "easy migration from Claude Sonnet 3.7 to Claude 4" and removed note that "Claude Sonnet 3.7 continues to return full thinking output." (+1/-3)
- **files.md**: Updated model support description for `file_id` (removed specific version references for Claude 3+/3.5+ in favor of linking to per-feature pages); fixed a broken internal anchor link (`#supported-file-types` → `#upload-and-analyze-your-own-files`). (+2/-2)
- **search-results.md**: Removed Claude Sonnet 3.7 from the supported models list for the search results feature; Claude Haiku 3.5 updated to "retired, except on Bedrock and Vertex AI." (+1/-2)

## Migration Notes

- **Claude Opus 4 on Amazon Bedrock retires May 31, 2026**: This is a significantly earlier date than previously documented (was October 14, 2026). Migrate to Claude Opus 4.5 or Claude Opus 4.6 immediately.
- **Context window overflow handling**: Applications using pre-4.5 models that catch validation errors for context overflow should also handle the new `stop_reason: "model_context_window_exceeded"` if opting into the `model-context-window-exceeded-2025-08-26` beta header. Applications on Claude 4.5+ must handle this stop reason directly.
- **Claude Opus 4.7 thinking output**: If you rely on receiving thinking blocks from Claude Opus 4.7 responses, add `display: "summarized"` to your request — thinking is now omitted by default on this model.
- **Prompt caching on Bedrock**: Do not use Anthropic's token minimum tables to configure prompt caching on Bedrock. Consult the [AWS Bedrock prompt caching docs](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) directly.

## Notable Details

- The Bedrock and Vertex AI model tables now use `<br /><small>` inline HTML for lifecycle annotations instead of Tooltip components. This is a rendering change with no API impact, but it signals a documentation standardization effort.
- The `model-context-window-exceeded-2025-08-26` beta header is newly documented as the opt-in mechanism for the graceful overflow behavior on pre-4.5 models. Developers on older models who want consistent behavior with Claude 4.5+ can use this header now.
- The extended thinking comparison table now starts at "Claude 4 models (pre-Opus 4.5)" — Claude Sonnet 3.7 is no longer a reference point in any extended thinking documentation.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| context-windows.md | Modified | SIGNIFICANT | +3/-5 | New overflow behavior section; `model_context_window_exceeded` stop reason documented; Claude Sonnet 3.7 interleaved thinking note removed |
| extended-thinking.md | Modified | SIGNIFICANT | +11/-21 | Claude Sonnet 3.7 removed from comparison table; Opus 4.7 thinking now omitted by default; overflow behavior updated |
| prompt-caching.md | Modified | SIGNIFICANT | +18/-14 | Pricing table cleaned up; Sonnet 4.6 cache minimum lowered to 1,024 tokens; Bedrock-specific caching note added |
| claude-on-amazon-bedrock-legacy.md | Modified | SIGNIFICANT | +6/-4 | Opus 4 retirement moved to May 31, 2026; Sonnet 3.7 fully retired; Haiku 3.5 re-classified; lifecycle disclaimer added |
| claude-on-vertex-ai.md | Modified | SIGNIFICANT | +6/-4 | Sonnet 3.7 retired May 11, 2026; Haiku 3.5 re-classified; lifecycle disclaimer added |
| batch-processing.md | Modified | SIGNIFICANT | +3/-6 | Pricing table: Opus 4/Sonnet 4 deprecated; Sonnet 3.7/Haiku 3/Opus 3 removed; Haiku 3.5 retired on API |
| adaptive-thinking.md | Modified | MINOR | +1/-3 | Removed Sonnet 3.7 migration and full-thinking-output references |
| files.md | Modified | MINOR | +2/-2 | Updated model support wording; fixed broken anchor link |
| search-results.md | Modified | MINOR | +1/-2 | Sonnet 3.7 removed; Haiku 3.5 status updated |

---
*Generated from Claude API documentation changes detected on 2026-05-15*
