# Claude API Documentation Changes — 2026-04-29

## Summary

The primary change in this update is a significant expansion of thinking block preservation behavior: **Claude Sonnet 4.6+ is now documented alongside Opus 4.5+ as a model class that keeps all prior thinking blocks by default**, replacing the previous Opus-only framing. Alongside this, the `display` field for omitting thinking output now has **native SDK support across all SDKs** (C#, Go, Java, PHP, Ruby, TypeScript), removing the previous requirement to use raw HTTP requests for most of them. TypeScript SDK type assertions (`as unknown as ...`) have been cleaned up throughout multiple documentation pages.

---

## Significant Changes

### Extended Thinking

- **Thinking block preservation is now model-class-specific, not Opus-only**: The documentation section previously titled "Thinking block preservation in Claude Opus 4.5 and later" has been renamed to "Thinking block preservation by model" and now covers three distinct tiers:
  > **Opus**: Claude Opus 4.5 and later Opus models keep all prior thinking blocks; Claude Opus 4.1 and earlier Opus models keep only the last assistant turn's thinking. **Sonnet**: Claude Sonnet 4.6 and later Sonnet models keep all; Claude Sonnet 4.5 and earlier Sonnet models keep only the last turn. **Haiku**: all Haiku models through Claude Haiku 4.5 keep only the last turn.
  - *Implication*: Developers using Claude Sonnet 4.6+ no longer need to manage thinking block retention manually; the API keeps all turns by default. Code that relies on the old behavior (strips-all) will behave differently on Sonnet 4.6+.
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

- **Non-tool-result user turns no longer universally invalidate thinking block cache**: The cache invalidation table row for "Non-tool results passed to extended thinking requests" has been updated from a blanket `✘` (invalidates) to `Model-specific`:
  > On Opus 4.5+ and Sonnet 4.6+, thinking blocks are preserved by default, so the cache remains valid (✓). On earlier Opus/Sonnet models and all Haiku models, all previously-cached thinking blocks are stripped from context, and any messages that follow those thinking blocks are removed from the cache (✘).
  - *Implication*: Prompt caching cost and hit-rate calculations now depend on which model tier is in use when thinking is enabled.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **Claude Opus 4.7 added to model comparison table**: The feature comparison table in extended-thinking.md now includes a dedicated column for Claude Opus 4.7 (adaptive thinking). Like Opus 4.6, it preserves all prior thinking blocks by default and uses adaptive thinking; it does not support the `interleaved-thinking-2025-05-14` beta header.
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

- **`display` field for omitted thinking now natively supported in all SDKs**: The documentation previously contained a note stating that C#, Go, Java, PHP, and Ruby SDKs required raw HTTP requests for the `display` field, and that TypeScript required a type assertion. All of these caveats have been removed and replaced with native SDK code examples:
  - **C#**: Uses `ThinkingConfigEnabled` with `Display = ThinkingConfigEnabledDisplay.Omitted`
  - **Go**: Uses `anthropic.ThinkingConfigEnabledDisplayOmitted` in `ThinkingConfigEnabledParam`
  - **Java**: Uses `ThinkingConfigEnabled.builder().display(ThinkingConfigEnabled.Display.OMITTED)`
  - **PHP**: Uses `ThinkingConfigEnabled::with(display: Display::OMITTED)`
  - **Ruby**: Uses `display_: :omitted` — the trailing underscore is intentional to avoid shadowing `Kernel#display`; the wire field name remains `display`
  - **TypeScript**: No longer requires `as unknown as Anthropic.MessageCreateParamsNonStreaming` type assertion
  - *Implication*: Developers on C#, Go, Java, PHP, and Ruby can now use the `display` field through the official SDK rather than hand-rolling HTTP calls.
  - *Source*: [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md), [Adaptive Thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md)

### Context Editing

- **`clear_thinking_20251015` strategy default changed from fixed to model-specific**: The `keep` parameter's documented default has changed from the hardcoded `{type: "thinking_turns", value: 1}` to a model-specific value:
  > Opus 4.5+ and Sonnet 4.6+: all turns. Earlier Opus/Sonnet and all Haiku: last turn only.
  - *Implication*: Code that runs across multiple model tiers should now set `keep` explicitly rather than relying on the per-model default, as the behavior now differs by model class.
  - *Source*: [Context Editing](https://platform.claude.com/docs/en/build-with-claude/context-editing.md)

### Advisor Tool

- **`clear_thinking` default behavior note updated**: The warning about cache misses from extended thinking without explicit `clear_thinking` configuration has been refined:
  > `keep: {type: "thinking_turns", value: 1}`, which triggers this behavior (the default on earlier Opus/Sonnet models and all Haiku models; on Opus 4.5+ and Sonnet 4.6+ the default is to keep all turns). Set `keep: "all"` to preserve advisor cache stability.
  - *Implication*: On newer models (Opus 4.5+, Sonnet 4.6+), advisor cache stability is better by default; the warning is still relevant for older Opus/Sonnet and all Haiku models.
  - *Source*: [Advisor Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md)

### SDKs

- **Go SDK install instruction simplified**: The install command changed from a version-pinned form to the plain module install:
  > Install with `go get`:
  > ```bash
  > go get github.com/anthropics/anthropic-sdk-go
  > ```
  Previously this was `go get -u 'github.com/anthropics/anthropic-sdk-go@v1.38.0'` under the heading "Or to pin the version:".
  - *Source*: [Go SDK](https://platform.claude.com/docs/en/api/sdks/go.md)

- **Java SDK: native `.required()` method for tool schema**: The `define-tools.md` Java example was updated to use the SDK's native `.required(List.of("location"))` builder method instead of `.putAdditionalProperty("required", JsonValue.from(List.of("location")))`.
  - *Implication*: Developers no longer need to use `putAdditionalProperty` workarounds for the `required` field in tool schemas; a typed method is available.
  - *Source*: [Define Tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools.md)

- **PHP SDK: `FileParam::fromResource()` for file uploads in code execution**: The PHP example for the code execution tool was updated to use `FileParam::fromResource(fopen('data.csv', 'r'))` instead of passing a raw resource directly to `file:`.
  - *Implication*: PHP developers must wrap file resources in `FileParam::fromResource()` when uploading to the Files API.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

- **PHP SDK: `extractFileIds` now uses typed signature**: The code execution example function signature changed from `function extractFileIds($response)` to `function extractFileIds(BetaMessage $response): array`, and the logic was rewritten using early-return guard clauses.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

- **TypeScript SDK type assertions removed across multiple pages**: Throughout compaction.md, adaptive-thinking.md, extended-thinking.md, and migration-guide.md, `as unknown as Anthropic.Beta.Messages.MessageCreateParamsNonStreaming`, `as unknown as Anthropic.MessageCreateParamsNonStreaming`, and related type assertions have been replaced with plain `})` — indicating the TypeScript SDK types now cover these parameters natively.

### Compaction / Streaming (Null Safety Fixes)

Null-safety fixes were applied to compaction delta length calculations across three SDKs:
- **Python**: `len(event.delta.content)` → `len(event.delta.content or '')`
- **PHP**: `strlen($event->delta->content)` → `strlen($event->delta->content ?? '')`
- **Ruby**: `event.delta.content.length` → `(event.delta.content || "").length`
- **TypeScript**: `(event.delta as { type: string }).type === "compaction_delta"` replaced with proper typed access; length calculation uses `event.delta.content?.length ?? 0`
- *Implication*: These prevent runtime errors when `content` is null in a compaction delta event.
- *Source*: [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction.md)

---

## Notable Details

- The Ruby SDK's use of `display_:` (trailing underscore) for the thinking `display` field is a SDK-level naming convention to avoid conflicting with Ruby's built-in `Kernel#display` method. The field sent over the wire is still named `display` — no API change, just a Ruby-specific binding alias.
- The TypeScript `compaction.md` example that checks `event.content_block.type === "compaction"` also lost the `as { type: string }` cast, meaning the TypeScript SDK's `content_block_start` event type definition now includes `"compaction"` as a valid block type.
- The `nocheck` directive was removed from the TypeScript streaming compaction example (`-```typescript TypeScript nocheck hidelines={1..2}` → `+```typescript TypeScript hidelines={1..2}`), meaning the TypeScript example is now considered valid and type-checkable without workarounds.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| extended-thinking.md | Modified | +160/-258 | Native SDK support for `display` field; thinking preservation expanded to Sonnet 4.6+; Opus 4.7 added to comparison table; TypeScript type assertions removed |
| compaction.md | Modified | +22/-26 | TypeScript type assertions removed; null-safety fixes for compaction delta in Python, PHP, Ruby, TypeScript |
| context-editing.md | Modified | +2/-4 | `clear_thinking_20251015` default changed from fixed to model-specific |
| adaptive-thinking.md | Modified | +5/-9 | SDK `display` caveat note removed; thinking preservation note updated for Sonnet 4.6+; TypeScript assertions removed |
| code-execution-tool.md | Modified | +25/-20 | PHP: `FileParam::fromResource()` for uploads; typed `extractFileIds` function |
| prompt-caching.md | Modified | +5/-5 | Cache invalidation for non-tool-result turns changed to model-specific |
| advisor-tool.md | Modified | +4/-2 | `clear_thinking` default behavior note updated for model-specific defaults |
| define-tools.md | Modified | +2/-4 | Java SDK: `.required()` replaces `putAdditionalProperty("required", ...)` |
| go.md | Modified | +2/-2 | Install instruction changed to unpinned `go get` |
| migration-guide.md | Modified | +1/-1 | TypeScript type assertion removed from example |

---

*Generated from Claude API documentation changes detected on 2026-04-29*
