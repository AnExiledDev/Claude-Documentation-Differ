# Claude API Documentation Changes — 2026-03-07

## Summary

Two documentation pages were updated: the models migration guide and the Claude 4.6 "what's new" page. The substantive changes are corrections to C# SDK example code for beta features (updated namespaces, types, and a typed beta constant). Several Python code block annotations had their `nocheck` markers removed, indicating those examples now validate cleanly against current SDK versions.

## Significant Changes

### C# SDK — Beta Namespace and Type Updates

- **Namespace change for beta message types**: C# examples in the migration guide now import `Anthropic.Models.Beta` and `Anthropic.Models.Beta.Messages` instead of `Anthropic.Models.Messages`.
  > ```csharp
  > // Before
  > using Anthropic.Models.Messages;
  >
  > // After
  > using Anthropic.Models.Beta;
  > using Anthropic.Models.Beta.Messages;
  > ```
  - *Implication*: Developers using the C# SDK with beta features (interleaved thinking, extended output) must update their `using` directives.
  - *Source*: [Model Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **`ThinkingConfigEnabled` renamed to `BetaThinkingConfigEnabled`**: The C# type for configuring thinking budgets has been renamed and its constructor syntax changed to an object initializer.
  > ```csharp
  > // Before
  > Thinking = new ThinkingConfigEnabled(budgetTokens: 16384),
  >
  > // After
  > Thinking = new BetaThinkingConfigEnabled { BudgetTokens = 16384 },
  > ```
  - *Implication*: Breaking change for C# SDK users enabling extended thinking.
  - *Source*: [Model Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **`OutputConfig` renamed to `BetaOutputConfig`**: Consistent with the namespace move, the output configuration type is now prefixed with `Beta`.
  > ```csharp
  > // Before
  > OutputConfig = new OutputConfig { Effort = Effort.Medium },
  >
  > // After
  > OutputConfig = new BetaOutputConfig { Effort = Effort.Medium },
  > ```
  - *Implication*: Breaking change for C# SDK users setting the `effort` parameter.
  - *Source*: [Model Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **Typed constant for `interleaved-thinking` beta header**: The raw string `"interleaved-thinking-2025-05-14"` is replaced with the typed enum value `AnthropicBeta.InterleavedThinking2025_05_14`.
  > ```csharp
  > // Before
  > Betas = ["interleaved-thinking-2025-05-14"],
  >
  > // After
  > Betas = [AnthropicBeta.InterleavedThinking2025_05_14],
  > ```
  - *Implication*: Improves type safety and discoverability of beta features in the C# SDK; raw string values will no longer match the documented pattern.
  - *Source*: [Model Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

### Documentation — Python Code Block Validation

- **`nocheck` markers removed from Python examples**: Several Python code blocks across both pages had `nocheck` (and `After nocheck`) annotations removed, reverting them to standard `python` blocks. This applies to examples covering adaptive thinking, fast mode, and interleaved thinking.
  - *Implication*: These examples are now expected to pass documentation validation/type-checking, suggesting the underlying SDK APIs they demonstrate are stable and correct as written.
  - *Source*: [Model Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md), [What's New in Claude 4.6](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `models/migration-guide.md` | Modified | +14 / -13 | C# SDK namespace/type corrections for beta features; Python `nocheck` annotation removals |
| `models/whats-new-claude-4-6.md` | Modified | +2 / -2 | Python `nocheck` annotation removals from adaptive thinking and fast mode examples |

---
*Generated from Claude API documentation changes detected on 2026-03-07*
