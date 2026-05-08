# Claude Code Documentation Changes — 2026-03-04

## Summary

Three pages were modified in this batch. The most substantive changes clarify `ultrathink` keyword behavior — reinstating it as a functional per-turn high-effort trigger rather than a no-op phrase — and document a new default effort level for Opus 4.6 on Max and Team plans. The PR creation workflow section was also simplified by removing references to the `/commit-push-pr` skill.

## Significant Changes

### Thinking Mode

- **`ultrathink` keyword reinstated as a functional per-turn effort trigger**: The thinking configuration table was updated to add `ultrathink` as a named configuration option. Simultaneously, it was removed from the list of phrases treated as plain prompt instructions with no effect on thinking tokens.

  Removed from the note (no longer a no-op):
  > Phrases like "think", "think hard", "ultrathink", and "think more" are interpreted as regular prompt instructions and don't allocate thinking tokens.

  Updated note now reads:
  > Phrases like "think", "think hard", and "think more" are interpreted as regular prompt instructions and don't allocate thinking tokens.

  New row added to the thinking configuration table:
  > **`ultrathink` keyword** | Include "ultrathink" anywhere in your prompt | Sets effort to high for that turn on Opus 4.6 and Sonnet 4.6. Useful for one-off tasks requiring deep reasoning without permanently changing your effort setting

  - *Implication*: Including "ultrathink" in a prompt now has a documented, functional effect: it triggers high effort for that single turn without permanently changing the session's effort level. This is confirmed by the v2.1.68 changelog entry "Re-introduced the 'ultrathink' keyword to enable high effort for the next turn."
  - *Source*: [Common workflows](https://code.claude.com/docs/en/common-workflows.md)

### Model Configuration

- **Opus 4.6 defaults to medium effort for Max and Team subscribers**: The effort level documentation now explicitly states the default effort level for Opus 4.6 on Max and Team plans.

  > Three levels are available: **low**, **medium**, and **high**. Opus 4.6 defaults to medium effort for Max and Team subscribers.

  - *Implication*: Developers on Max or Team plans who have not explicitly configured an effort level should expect medium-depth adaptive reasoning from Opus 4.6. This aligns with the v2.1.68 changelog entry "Opus 4.6 now defaults to medium effort for Max and Team subscribers."
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

### Workflows

- **PR creation docs simplified — `/commit-push-pr` skill reference removed**: The "Create pull requests" section previously described the `/commit-push-pr` bundled skill (commit, push, and open a PR in one step) and noted automatic Slack MCP posting behavior. This content was removed. The section now only covers asking Claude directly or following a manual step-by-step flow.

  Removed text:
  > You can create pull requests by asking Claude directly ("create a pr for my changes") or by using the `/commit-push-pr` skill, which commits, pushes, and opens a PR in one step.
  > If you have a Slack MCP server configured and specify channels in your CLAUDE.md (for example, "post PR URLs to #team-prs"), the skill automatically posts the PR URL to those channels.
  > For more control over the process, guide Claude through it step-by-step or [create your own skill](/en/skills):

  New text:
  > You can create pull requests by asking Claude directly ("create a pr for my changes"), or guide Claude through it step-by-step:

  - *Implication*: The `/commit-push-pr` skill still exists (the changelog.md page references it as changed in v2.1.20), but it is no longer documented in the standard common-workflows page. The simplified wording removes the pointer to custom skills as well.
  - *Source*: [Common workflows](https://code.claude.com/docs/en/common-workflows.md)

## Notable Details

- The `changelog.md` page changes are purely GitHub repository metadata counter updates (Forks: 5.8k → 5.9k, Stars: 73.5k → 73.6k, Pull requests: 252 → 253). There is no change to documented release notes content.
- The `ultrathink` change is a reversal of a prior documentation update. It was previously listed among no-op phrases; it is now a first-class configuration method in the thinking table.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| common-workflows.md | Modified | +9/-16 | Removed `/commit-push-pr` skill reference from PR workflow; updated thinking configuration table to add `ultrathink` as a functional keyword and remove it from the no-op phrases note |
| changelog.md | Modified | +3/-3 | GitHub repo metadata counter updates (forks, stars, PR count) — no documentation content change |
| model-config.md | Modified | +1/-1 | Added default effort level note: Opus 4.6 defaults to medium effort for Max and Team subscribers |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-04*
