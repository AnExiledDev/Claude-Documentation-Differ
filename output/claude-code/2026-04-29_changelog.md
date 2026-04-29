# Claude Code Documentation Changes — 2026-04-29

## Summary

Two pages updated with minor but substantive corrections. The skills documentation fixes an inaccuracy about what controls a skill's slash-command name (the directory name, not a `name` frontmatter field), and the ultrareview documentation adds a cross-reference to the Code Review integration for teams wanting automated GitHub PR reviews.

## Significant Changes

### Skills

- **Slash-command name is derived from the directory name, not a `name` frontmatter field**: The documentation previously stated that `The name field becomes the /slash-command`. This has been corrected to `The directory name becomes the /slash-command`. The `name: explain-code` key has been removed from the example `SKILL.md` frontmatter entirely to reflect actual behavior.

  Before:
  > The `name` field becomes the `/slash-command`, and the `description` helps Claude decide when to load it automatically.

  After:
  > The directory name becomes the `/slash-command`, and the `description` helps Claude decide when to load it automatically.

  - *Implication*: The `name:` field in SKILL.md frontmatter has no documented effect on the command name. Developers who added it expecting it to define the slash-command should rename the skill directory instead.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

### Ultrareview

- **Added cross-reference to Code Review integration for automated GitHub PR workflows**: A new paragraph was inserted between the exit-code documentation and the "How ultrareview compares to /review" comparison table, directing users to the Code Review feature for automatic, CI-style review.

  > For automatic reviews on GitHub pull requests, [Code Review](/en/code-review) integrates with your repository directly and posts findings as inline PR comments without a CLI step.

  - *Implication*: `/ultrareview` and `claude ultrareview` are manually invoked, one-shot tools. Teams wanting reviews to trigger automatically on every PR without a CLI step should use the Code Review integration instead.
  - *Source*: [Ultrareview](https://code.claude.com/docs/en/ultrareview.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `skills.md` | Modified | +1 / -2 | Corrected slash-command naming to use directory name; removed `name:` key from example frontmatter |
| `ultrareview.md` | Modified | +2 / -0 | Added reference to Code Review integration for automated GitHub PR reviews |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-29*
