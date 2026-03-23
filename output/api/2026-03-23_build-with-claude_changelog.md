# Claude API Documentation Changes — 2026-03-23

## Summary

All 22 modified pages in the `build-with-claude` section received documentation formatting-only changes. No API parameters, endpoints, models, or SDK behaviors were altered. The changes consist entirely of adjustments to `hidelines` metadata annotations in code block examples across Python, TypeScript, Go, Java, PHP, Ruby, and C# SDK tabs.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| [adaptive-thinking.md](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md) | Modified | +17/-17 | `hidelines` range adjustments in all SDK code blocks |
| [batch-processing.md](https://platform.claude.com/docs/en/build-with-claude/batch-processing.md) | Modified | +37/-37 | `hidelines` range adjustments in all SDK code blocks |
| [citations.md](https://platform.claude.com/docs/en/build-with-claude/citations.md) | Modified | +4/-4 | `hidelines` range adjustments |
| [claude-in-microsoft-foundry.md](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md) | Modified | +2/-2 | `hidelines` range adjustments |
| [claude-on-amazon-bedrock.md](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md) | Modified | +11/-11 | `hidelines` range adjustments in all SDK code blocks |
| [claude-on-vertex-ai.md](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md) | Modified | +10/-10 | `hidelines` range adjustments in all SDK code blocks |
| [compaction.md](https://platform.claude.com/docs/en/build-with-claude/compaction.md) | Modified | +62/-62 | `hidelines` range adjustments across numerous code blocks |
| [context-editing.md](https://platform.claude.com/docs/en/build-with-claude/context-editing.md) | Modified | +33/-33 | `hidelines` range adjustments in all SDK code blocks |
| [data-residency.md](https://platform.claude.com/docs/en/build-with-claude/data-residency.md) | Modified | +2/-2 | `hidelines` range adjustments |
| [effort.md](https://platform.claude.com/docs/en/build-with-claude/effort.md) | Modified | +6/-6 | `hidelines` range adjustments |
| [extended-thinking.md](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md) | Modified | +33/-33 | `hidelines` range adjustments in all SDK code blocks |
| [fast-mode.md](https://platform.claude.com/docs/en/build-with-claude/fast-mode.md) | Modified | +13/-13 | `hidelines` range adjustments |
| [files.md](https://platform.claude.com/docs/en/build-with-claude/files.md) | Modified | +14/-14 | `hidelines` range adjustments in all SDK code blocks |
| [pdf-support.md](https://platform.claude.com/docs/en/build-with-claude/pdf-support.md) | Modified | +11/-11 | `hidelines` range adjustments |
| [prompt-caching.md](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md) | Modified | +47/-47 | `hidelines` range adjustments across numerous code blocks |
| [search-results.md](https://platform.claude.com/docs/en/build-with-claude/search-results.md) | Modified | +14/-14 | `hidelines` range adjustments in all SDK code blocks |
| [skills-guide.md](https://platform.claude.com/docs/en/build-with-claude/skills-guide.md) | Modified | +63/-63 | `hidelines` range adjustments across numerous code blocks |
| [streaming.md](https://platform.claude.com/docs/en/build-with-claude/streaming.md) | Modified | +36/-36 | `hidelines` range adjustments in all SDK code blocks |
| [structured-outputs.md](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md) | Modified | +86/-63 | `hidelines` range adjustments; minor Python import reordering in one example |
| [token-counting.md](https://platform.claude.com/docs/en/build-with-claude/token-counting.md) | Modified | +25/-25 | `hidelines` range adjustments in all SDK code blocks |
| [vision.md](https://platform.claude.com/docs/en/build-with-claude/vision.md) | Modified | +20/-20 | `hidelines` range adjustments in all SDK code blocks |
| [working-with-messages.md](https://platform.claude.com/docs/en/build-with-claude/working-with-messages.md) | Modified | +23/-23 | `hidelines` range adjustments in all SDK code blocks |

## Notable Details

The `hidelines` attribute controls which lines of code are collapsed/hidden by default in the rendered documentation UI. The systematic pattern across all pages suggests a coordinated recalibration of what counts as boilerplate in each SDK's code examples:

- **Python/TypeScript**: Most blocks changed from `hidelines={1..4}` or `hidelines={1..2}` to a narrower range (e.g., `hidelines={1..2}`), showing fewer collapsed import lines.
- **Go**: Import blocks commonly changed from `hidelines={1..13,-1}` to `hidelines={1..11,-1}`, reducing the number of hidden import lines.
- **Java**: Ranges shifted from simple spans like `hidelines={1..8,-1}` to compound ranges like `hidelines={1..3,5..8,-2..}`, targeting specific lines rather than a contiguous block.
- **PHP**: Several blocks that had no `hidelines` attribute now have `hidelines={1..4}`, adding initial line collapsing.
- **Ruby**: Many blocks that had no `hidelines` attribute now have `hidelines={1..2}`, collapsing the `require "anthropic"` line and blank line.
- **`structured-outputs.md`** (+86/-63, the only page with a net addition): Beyond the `hidelines` changes, one Python code example had its imports reordered — `from pydantic import BaseModel` moved before `client = Anthropic()`. This is a cosmetic code style fix with no API impact.

No API endpoints, request parameters, response schemas, model names, rate limits, or SDK method signatures changed in this update.

---
*Generated from Claude API documentation changes detected on 2026-03-23*
