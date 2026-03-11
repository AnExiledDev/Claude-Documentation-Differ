# Claude Code Documentation Changes — 2026-03-11

## Summary

Nine documentation pages were modified in this cycle, with no new or removed pages. All changes are infrastructure-level HTML cleanup: responsive image attributes (`srcset`, `data-optimize`, `data-opv`, `data-og-width`, `data-og-height`) were stripped from embedded `<img>` tags across the documentation site. No documentation text, feature descriptions, or user-facing content changed.

## Notable Details

- **Image markup simplification (8 pages)**: Every changed `<img>` tag across `agent-teams.md`, `data-usage.md`, `desktop-quickstart.md`, `features-overview.md`, `hooks.md`, `how-claude-code-works.md`, `statusline.md`, and `vs-code.md` follows the same before/after pattern:
  - **Removed attributes**: `data-og-width`, `data-og-height`, `data-optimize="true"`, `data-opv="3"`, and the full `srcset="..."` string
  - **Retained attributes**: `src`, `alt`, `width`, `height`, `data-path`, and any existing `className` or `style` attributes

  This indicates the documentation platform (Mintlify/mintcdn) has moved responsive image delivery and optimization metadata out of the HTML source and into the CDN layer. No image content, alt text, or visible page text changed.

- **GitHub repository stats bump (`changelog.md`)**: The embedded GitHub widget updated from 76.3k → 76.4k stars and 329 → 330 open pull requests. This is live-scraped embed metadata, not editorial content.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| [statusline.md](https://code.claude.com/docs/en/statusline.md) | Modified | +7/-7 | Image attribute cleanup across 7 embedded images |
| [vs-code.md](https://code.claude.com/docs/en/vs-code.md) | Modified | +5/-5 | Image attribute cleanup across 5 embedded images |
| [agent-teams.md](https://code.claude.com/docs/en/agent-teams.md) | Modified | +2/-2 | Image attribute cleanup across 2 embedded images |
| [changelog.md](https://code.claude.com/docs/en/changelog.md) | Modified | +2/-2 | GitHub star count (76.3k→76.4k) and PR count (329→330) updated |
| [desktop-quickstart.md](https://code.claude.com/docs/en/desktop-quickstart.md) | Modified | +2/-2 | Image attribute cleanup across 2 embedded images |
| [hooks.md](https://code.claude.com/docs/en/hooks.md) | Modified | +2/-2 | Image attribute cleanup across 2 embedded images |
| [how-claude-code-works.md](https://code.claude.com/docs/en/how-claude-code-works.md) | Modified | +2/-2 | Image attribute cleanup across 2 embedded images |
| [data-usage.md](https://code.claude.com/docs/en/data-usage.md) | Modified | +1/-1 | Image attribute cleanup for 1 embedded image |
| [features-overview.md](https://code.claude.com/docs/en/features-overview.md) | Modified | +1/-1 | Image attribute cleanup for 1 embedded image |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-11*
