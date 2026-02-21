# Claude API Documentation Changes — 2026-02-21

## Summary

Four pages in the "About Claude" documentation were updated to reflect model lifecycle changes effective February 19, 2026. Claude Haiku 3 (`claude-3-haiku-20240307`) has been deprecated with a retirement date of April 20, 2026, while Claude Sonnet 3.7 and Claude Haiku 3.5 transitioned from "Deprecated" to "Retired" status. Fast mode pricing for Opus 4.6 was also simplified, removing the tiered input cost structure.

## Significant Changes

### Models

- **Claude Haiku 3 Deprecated**: `claude-3-haiku-20240307` has been formally deprecated as of February 19, 2026, with a retirement date of April 20, 2026. The recommended replacement is `claude-haiku-4-5-20251001`.
  > "On February 19, 2026, Anthropic notified developers using Claude Haiku 3 model of its upcoming retirement on the Claude API."
  - *Implication*: Developers using `claude-3-haiku-20240307` must migrate to `claude-haiku-4-5-20251001` before April 20, 2026, or API requests will begin to fail.
  - *Source*: [Model Deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations.md)

- **Claude Sonnet 3.7 and Haiku 3.5 Retired**: Both `claude-3-7-sonnet-20250219` and `claude-3-5-haiku-20241022` have moved from "Deprecated" to "Retired" status as of February 19, 2026. Requests to these models will now fail.
  > "Retired: The model is no longer available for use. Requests to retired models will fail."
  - *Implication*: Any application still referencing these model IDs will receive errors immediately. Migration to active models is required.
  - *Source*: [Model Deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations.md)

- **Claude Sonnet 3.7 Removed from Legacy Models Table**: The models overview page removed `claude-3-7-sonnet-20250219` from the "Legacy models" comparison table, as it is now retired. Claude Haiku 3 remains in the table but is now labeled with "(deprecated)" in the column header.
  > "Claude Haiku 3 (deprecated)" — column header in the updated legacy models table
  > "Claude Haiku 3 (`claude-3-haiku-20240307`) is deprecated and will be retired on April 19, 2026. Migrate to [Claude Haiku 4.5] before the retirement date."
  - *Implication*: The legacy table now has 6 columns instead of 7. The footnote about Claude Sonnet 3.7's 128K output beta header (`output-128k-2025-02-19`) has also been removed.
  - *Source*: [Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

- **Migration Guide Extended for Haiku 3**: The migration guide's code examples now include a "From Haiku 3" path, and the rate limits note has been updated to reference both Haiku 3.5 and Haiku 3.
  > "# From Haiku 3\nmodel = \"claude-3-haiku-20240307\"  # Before\nmodel = \"claude-haiku-4-5-20251001\"  # After"
  > "**Review new rate limits:** Haiku 4.5 has separate rate limits from Haiku 3.5 and Haiku 3."
  - *Implication*: Developers migrating from Haiku 3 now have explicit code examples in the official migration guide.
  - *Source*: [Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

### Pricing

- **Fast Mode Pricing Simplified**: The tiered fast mode pricing table for Claude Opus 4.6 has been replaced with a single flat rate. Previously, requests over 200K input tokens were charged at $60/MTok input; the new structure charges $30/MTok input uniformly across all context window sizes.
  > "Fast mode pricing applies across the full context window, including requests over 200K input tokens."

  Previous pricing table:
  | Context window | Input | Output |
  |:---|:---|:---|
  | ≤ 200K input tokens | $30 / MTok | $150 / MTok |
  | > 200K input tokens | $60 / MTok | $225 / MTok |

  New pricing table:
  | Input | Output |
  |:---|:---|
  | $30 / MTok | $150 / MTok |

  - *Implication*: Long-context fast mode requests (over 200K tokens) are now significantly cheaper — input cost drops from $60/MTok to $30/MTok and output from $225/MTok to $150/MTok. The previous premium for long-context fast mode no longer applies.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

- **Long Context Pricing Clarification**: The long context pricing section was updated to clarify that the premium long context rates apply only when using standard speed.
  > "When using Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5, or Sonnet 4 at standard speed with the [1M token context window enabled], requests that exceed 200K input tokens are automatically charged at premium long context rates. [Fast mode] includes the full 1M context window at no additional long context charge."
  - *Implication*: Fast mode users with long contexts are not subject to additional long context charges on top of fast mode rates. This clarifies pricing interactions between fast mode and long context use.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

## Migration Guidance

**Claude Haiku 3 retirement (deadline: April 20, 2026)**

`claude-3-haiku-20240307` will stop accepting requests on April 20, 2026. Migrate to `claude-haiku-4-5-20251001`:

```python
# Before
model = "claude-3-haiku-20240307"

# After
model = "claude-haiku-4-5-20251001"
```

Note that Haiku 4.5 has separate rate limits from Haiku 3. Review [rate limits documentation](https://platform.claude.com/docs/en/api/rate-limits) after migrating.

**Claude Sonnet 3.7 and Haiku 3.5 are already retired**

`claude-3-7-sonnet-20250219` and `claude-3-5-haiku-20241022` are retired as of February 19, 2026. Requests to these models will fail immediately. If your application is still using these model IDs, migration is urgent.

## Notable Details

- The `output-128k-2025-02-19` beta header footnote (which enabled 128K output tokens for Claude Sonnet 3.7) has been removed from the models overview page, consistent with Sonnet 3.7's retirement.
- The model status table now shows `claude-3-haiku-20240307` with a "Deprecated" date of February 19, 2026, and a tentative retirement date of April 20, 2026 — giving developers approximately 60 days' notice, consistent with Anthropic's stated policy of at least 60 days notice before retirement.
- Retirement notes ("This model was retired February 19, 2026.") have been added to the deprecation history entries for both Haiku 3.5 and Sonnet 3.7.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| model-deprecations.md | Modified | +19 / -3 | Added Haiku 3 deprecation entry; updated Sonnet 3.7 and Haiku 3.5 status to Retired; added retirement notices |
| models/overview.md | Modified | +18 / -16 | Removed Sonnet 3.7 from legacy table; labeled Haiku 3 as deprecated; added deprecation warning; removed 128K output footnote |
| models/migration-guide.md | Modified | +5 / -1 | Added "From Haiku 3" code example; updated rate limits note to include Haiku 3 |
| pricing.md | Modified | +5 / -6 | Simplified fast mode pricing to flat rate; clarified long context pricing applies at standard speed only |
