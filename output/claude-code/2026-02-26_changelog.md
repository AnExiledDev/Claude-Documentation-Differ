# Claude Code Documentation Changes — 2026-02-26

## Summary

One documentation page was updated: `discover-plugins.md` received a concrete JSON configuration example for the team marketplace feature. No pages were added or removed.

## Significant Changes

### Configuration

- **Added `extraKnownMarketplaces` JSON example for team marketplace setup**: The "Configure team marketplaces" section previously described the feature in prose but lacked a concrete configuration snippet. A JSON code block has been added showing the exact structure to place in `.claude/settings.json`.

  > ```json
  > {
  >   "extraKnownMarketplaces": {
  >     "my-team-tools": {
  >       "source": {
  >         "source": "github",
  >         "repo": "your-org/claude-plugins"
  >       }
  >     }
  >   }
  > }
  > ```

  - *Implication*: Team admins now have a copy-pasteable starting point for wiring a GitHub-hosted plugin repository into project settings, reducing ambiguity about the required nesting (`source.source` and `source.repo`).
  - *Source*: [Discover Plugins](https://code.claude.com/docs/en/discover-plugins.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `discover-plugins.md` | Modified | +15 / -0 | Added `extraKnownMarketplaces` JSON example to the "Configure team marketplaces" section |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-26*
