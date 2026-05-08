# Claude API Documentation Changes — 2026-04-15

## Summary

Three pages were modified in this update. The primary change is a new release note entry announcing the deprecation of Claude Sonnet 4 and Claude Opus 4, with retirement on the Claude API scheduled for June 15, 2026. Two other pages received minor edits (2 lines each), likely model reference corrections.

## Significant Changes

### Deprecations

- **Claude Sonnet 4 and Opus 4 deprecated**: Both `claude-sonnet-4-20250514` and `claude-opus-4-20250514` are now officially deprecated, with retirement on the Claude API set for **June 15, 2026**.
  > "We announced the deprecation of the Claude Sonnet 4 model (`claude-sonnet-4-20250514`) and the Claude Opus 4 model (`claude-opus-4-20250514`), with retirement on the Claude API scheduled for June 15, 2026. We recommend migrating to Claude Sonnet 4.6 and Claude Opus 4.6 respectively."
  - *Implication*: Any production code pinned to `claude-sonnet-4-20250514` or `claude-opus-4-20250514` will break after June 15, 2026. Migrate to the 4.6 series before that date.
  - *Source*: [Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

## Migration Guidance

- **Sonnet 4 → Sonnet 4.6**: Replace `claude-sonnet-4-20250514` with `claude-sonnet-4-6` (or `claude-sonnet-4-6-latest`).
- **Opus 4 → Opus 4.6**: Replace `claude-opus-4-20250514` with `claude-opus-4-6` (or `claude-opus-4-6-latest`).
- Both 4.6 models support a 1M token context window at standard pricing with no beta header required, as well as extended thinking and all current GA tools.
- Retirement deadline: **June 15, 2026**.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| release-notes/overview.md | Modified | +3 / -0 | Added April 14, 2026 entry announcing Sonnet 4 and Opus 4 deprecation |
| agents-and-tools/tool-use/code-execution-tool.md | Modified | +2 / -2 | Minor edits (likely model reference corrections) |
| test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md | Modified | +1 / -1 | Minor edit (likely model reference correction) |

---
*Generated from Claude API documentation changes detected on 2026-04-15*
