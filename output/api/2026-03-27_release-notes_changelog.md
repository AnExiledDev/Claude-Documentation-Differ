# Claude API Documentation Changes — 2026-03-27

## Summary

One page was modified with minor internal link updates. Three links previously pointing to `implement-tool-use` were updated to point to more specific, newly-structured pages within the tool use documentation. No API behavior, parameters, or features changed.

## Notable Details

The `implement-tool-use` page in the tool use documentation appears to have been split into more granular pages, with historical release note entries updated to reflect the new structure:

- **Tool use examples link updated**: The reference to "providing tool use examples" in the March 2026 release notes entry now points to `/docs/en/agents-and-tools/tool-use/define-tools#providing-tool-use-examples` (previously `implement-tool-use#providing-tool-use-examples`). This indicates a new dedicated `define-tools` page.

- **Citable documents link updated**: The September 3, 2025 entry for "citable documents in client-side tool results" now links to `/docs/en/agents-and-tools/tool-use/handle-tool-calls` (previously `implement-tool-use`). This indicates a new dedicated `handle-tool-calls` page.

- **Parallel tool use link updated**: The October 3, 2024 entry for `disable_parallel_tool_use` now links to `/docs/en/agents-and-tools/tool-use/parallel-tool-use` (previously `implement-tool-use#parallel-tool-use`). This indicates a new dedicated `parallel-tool-use` page.

These are link corrections following a documentation restructuring — developers bookmarking or linking to `implement-tool-use` directly may need to update references to the appropriate new page.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| release-notes/overview.md | Modified | +3/-3 | Updated 3 internal links from `implement-tool-use` to restructured `define-tools`, `handle-tool-calls`, and `parallel-tool-use` pages |

---
*Generated from Claude API documentation changes detected on 2026-03-27*
