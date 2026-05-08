# Claude API Documentation Changes — 2026-03-05

## Summary

This update substantially expands the Claude 4.6 migration guide with multi-SDK code examples covering TypeScript, C#, Go, Java, PHP, and Ruby across all migration scenarios. The pricing page gains a dedicated "Prompt caching" section that consolidates pricing multiplier details previously scattered across a note. Use-case guide and "What's new" code examples received `nocheck` annotation metadata, which are documentation tooling markers with no API impact.

## Significant Changes

### Models — Migration Guide

- **Multi-SDK code examples added to adaptive thinking migration (Opus 4.6)**: The "Migrate to adaptive thinking" section previously showed only Python before/after snippets. It now includes complete, runnable examples for TypeScript, C#, Go, Java, PHP, and Ruby, all demonstrating the switch from `client.beta.messages.create` with `thinking: {type: "enabled", budget_tokens: N}` to `client.messages.create` with `thinking: {type: "adaptive"}` and `output_config: {effort: "high"}`.
  > ```python After nocheck
  > response = client.messages.create(
  >     model="claude-opus-4-6",
  >     max_tokens=16000,
  >     thinking={"type": "adaptive"},
  >     output_config={"effort": "high"},
  >     messages=[{"role": "user", "content": "Your prompt here"}],
  > )
  > ```
  - *Implication*: Developers using non-Python SDKs now have concrete reference examples for the adaptive thinking migration. The note that adaptive thinking is GA (no beta namespace or beta headers required) is highlighted across all SDK snippets.
  - *Source*: [Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **Multi-SDK code examples added to Sonnet 4.6 extended thinking migration**: Two new multi-SDK code groups were added for migrating from Sonnet 4.5 extended thinking to Sonnet 4.6 — one for coding/agentic use cases (`medium` effort, `interleaved-thinking-2025-05-14` beta header retained) and one for chat/non-coding use cases (`low` effort, adaptive thinking via `thinking: {type: "adaptive"}`). All six SDKs (Shell/curl, Python, TypeScript, C#, Go, Java, PHP, Ruby) are covered in each group.
  > For agentic coding, frontend design, tool-heavy workflows, and complex enterprise workflows, start with `medium` effort. If you find latency is too high, consider reducing effort to `low`. If you need higher intelligence, consider increasing effort to `high` or migrating to Opus 4.6.
  - *Implication*: Sonnet 4.6 extended thinking uses `client.beta.messages.create` with the `interleaved-thinking-2025-05-14` beta header for manual thinking, while adaptive thinking (`thinking: {type: "adaptive"}`) goes through the GA `client.messages.create` path. The two paths are now clearly separated by use case.
  - *Source*: [Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **Python example refinements**: The `messages=[...]` placeholder in the "After" Python snippet was replaced with an explicit `messages=[{"role": "user", "content": "Your prompt here"}]` for clarity. All Python code blocks in migration scenarios gained `nocheck` annotations (documentation tooling metadata indicating the examples should not be linted/executed in CI).
  - *Source*: [Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

### Pricing

- **New dedicated "Prompt caching" section under Feature-specific pricing**: The pricing page previously embedded cache multiplier details in a `<Note>` block within the model pricing table. These details have been moved into a new standalone `### Prompt caching` section that also introduces the two caching modes and their break-even points.
  > There are two ways to enable prompt caching:
  > - **Automatic caching:** Add a single `cache_control` field at the top level of your request. The system automatically manages cache breakpoints as conversations grow.
  > - **Explicit cache breakpoints:** Place `cache_control` directly on individual content blocks for fine-grained control over exactly what gets cached.

  | Cache operation | Multiplier | Duration |
  |:----------------|:-----------|:---------|
  | 5-minute cache write | 1.25x base input price | Cache valid for 5 minutes |
  | 1-hour cache write | 2x base input price | Cache valid for 1 hour |
  | Cache read (hit) | 0.1x base input price | Same duration as the preceding write |

  - *Implication*: The break-even analysis is now explicit: a 5-minute cache pays off after a single cache hit (1.25x write / 0.1x read = break-even at 1 read), while a 1-hour cache requires two reads (2x write). The new section also clarifies that these multipliers stack with Batch API discounts, long context pricing, and data residency.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

- **Model pricing table note updated**: The `<Note>` below the model pricing table was simplified to point readers to the new `#prompt-caching` anchor rather than embedding multiplier details inline.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

## Notable Details

- **`nocheck` annotations added to code examples across multiple pages**: The "What's new in Claude 4.6" page had three Python code blocks updated from ` ```python ` to ` ```python nocheck ` (adaptive thinking example, fast mode example, and `output_format` deprecation example). The same annotation was added across use-case guide code blocks (content-moderation, customer-support-chat, legal-summarization, ticket-routing). This is a documentation tooling marker that prevents CI linting/execution of illustrative snippets that depend on external context — no API behavior changes.

- **Minor wording cleanup in pricing page**: Instances of "our sales team" and "we accept" were rewritten to third-person ("the sales team", "major credit cards are accepted"). The FAQ entry on discount stacking now cross-links to `#prompt-caching`.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| migration-guide.md | Modified | +729/-69 | Added TypeScript, C#, Go, Java, PHP, Ruby SDK examples for Opus 4.6 adaptive thinking and Sonnet 4.6 extended/adaptive thinking migrations |
| pricing.md | Modified | +29/-11 | Added dedicated "Prompt caching" section with multiplier table; consolidated details previously in a `<Note>` block |
| whats-new-claude-4-6.md | Modified | +3/-3 | Added `nocheck` annotation to three Python code blocks |
| content-moderation.md | Modified | +4/-4 | Added `nocheck` and `hidelines` annotations to four Python code blocks |
| customer-support-chat.md | Modified | +3/-3 | Added `nocheck` annotation to three Python code blocks |
| legal-summarization.md | Modified | +3/-3 | Added `nocheck` annotation to three Python code blocks |
| ticket-routing.md | Modified | +4/-3 | Added `nocheck` annotation to Python code blocks |

---
*Generated from Claude API documentation changes detected on 2026-03-05*
