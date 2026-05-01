# Claude Code Documentation Changes — 2026-05-01

## Summary

Two pages were updated in this cycle. The auto mode configuration reference gained a plan/platform availability notice clarifying which accounts can use auto mode. The memory page received a more precise description of CLAUDE.md loading order across a directory tree.

## Significant Changes

### Configuration

- **Auto mode plan and platform availability notice**: A new callout block was added to the auto mode configuration reference explicitly stating which plans and platforms support auto mode.

  > Auto mode is available on Max, Team, Enterprise, and API plans through the Anthropic API. It is not available on Pro or on Bedrock, Vertex, or Foundry. If Claude Code reports auto mode as unavailable for your account, check the full requirements, which also cover the supported models and admin enablement on Team and Enterprise plans.

  - *Implication*: Developers on Pro plans or using Bedrock, Vertex, or Foundry will now find a clear, direct note explaining the restriction rather than discovering it through trial and error. This reduces confusion for users who have auto mode blocked without an obvious explanation.
  - *Source*: [Configure auto mode](https://code.claude.com/docs/en/auto-mode-config.md)

### Memory / CLAUDE.md

- **Clarified CLAUDE.md directory tree ordering**: The description of how CLAUDE.md files are ordered in context was updated to specify that files are loaded from the filesystem root *down* to the working directory — meaning files closer to the working directory are appended last and therefore read last by Claude.

  Before:
  > All discovered files are concatenated into context rather than overriding each other. Within each directory, `CLAUDE.local.md` is appended after `CLAUDE.md`, so when instructions conflict, your personal notes are the last thing Claude reads at that level.

  After:
  > All discovered files are concatenated into context rather than overriding each other. Across the directory tree, content is ordered from the filesystem root down to your working directory. For the `foo/bar/` example, `foo/CLAUDE.md` appears in context before `foo/bar/CLAUDE.md`, so instructions closer to where you launched Claude are read last. Within each directory, `CLAUDE.local.md` is appended after `CLAUDE.md`, so your personal notes are the last thing Claude reads at that level.

  - *Implication*: This clarifies that more-specific (deeper) CLAUDE.md files take effective precedence over ancestor files when instructions conflict — because Claude reads them last. Developers relying on project-level overrides of user-level or parent-directory instructions should verify their file placement matches this expectation.
  - *Source*: [How Claude remembers your project](https://code.claude.com/docs/en/memory.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `auto-mode-config.md` | Modified | +4 / -0 | Added plan/platform availability note for auto mode |
| `memory.md` | Modified | +1 / -1 | Clarified root-to-working-directory ordering of CLAUDE.md files in context |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-01*
