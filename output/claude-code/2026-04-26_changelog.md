# Claude Code Documentation Changes — 2026-04-26

## Summary

Three pages were modified. The most substantive change is an expansion of the `/claude-api` skill with two new sub-commands for model migration and Managed Agent onboarding. Two other pages received minor wording and link improvements.

## Significant Changes

### Commands

- **`/claude-api` gains `migrate` and `managed-agents-onboard` sub-commands**: The command signature changed from `/claude-api` to `/claude-api [migrate|managed-agents-onboard]`, with two new modes of operation:

  > Run `/claude-api migrate` to upgrade existing Claude API code to a newer model: Claude asks which files to scan and which model to target, then updates model IDs, thinking configuration, and other parameters that changed between versions. Run `/claude-api managed-agents-onboard` for an interactive walkthrough that creates a new Managed Agent from scratch.

  - *Implication*: Developers on older Claude model versions can now run an in-session migration workflow instead of manually updating model ID strings and configuration parameters. The Managed Agent onboarding path lowers the barrier to building agent-based applications.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

### Integrations

- **Chrome extension page now links directly to the Chrome Web Store**: The introductory paragraph on the Chrome integration page changed the phrase "Claude in Chrome browser extension" from plain text to a direct hyperlink pointing to `https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn`.
  - *Implication*: Users can now click directly to install the extension from the documentation, rather than searching for it manually.
  - *Source*: [Chrome](https://code.claude.com/docs/en/chrome.md)

### Configuration

- **Skills priority wording clarified**: The description of skill name conflict resolution was reworded for readability:

  > Before: "higher-priority locations win: enterprise > personal > project"
  >
  > After: "enterprise overrides personal, and personal overrides project"

  The resolution order itself is unchanged; only the shorthand notation was replaced with explicit prose.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

## Notable Details

- The bulk of the line count change in `commands.md` (+85/-85) is a cosmetic table reformatting — the command column was widened to accommodate the longer `/claude-api [migrate|managed-agents-onboard]` signature. No other command descriptions changed.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| commands.md | Modified | +85/-85 | Table reformatted; `/claude-api` command expanded with `migrate` and `managed-agents-onboard` sub-commands |
| chrome.md | Modified | +1/-1 | Chrome extension name changed from plain text to Chrome Web Store hyperlink |
| skills.md | Modified | +1/-1 | Skill priority conflict wording clarified from shorthand notation to plain prose |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-26*
