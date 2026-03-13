# Claude Code Documentation Changes — 2026-03-13

## Summary

One page was modified: the Code Review documentation. The update introduces a new **Manual** review trigger mode and a new `@claude review` comment command for on-demand PR reviews. Existing trigger option labels were also renamed for clarity.

## Significant Changes

### Features

- **New "Manual" review trigger mode**: A third option has been added to the per-repository **Review Behavior** dropdown, alongside the two existing automatic triggers. In Manual mode, reviews only start when someone comments `@claude review` on a PR; subsequent pushes to that PR are then reviewed automatically from that point forward.
  > *"Manual: reviews start only when someone comments `@claude review` on a PR; subsequent pushes to that PR are then reviewed automatically"*
  - *Implication*: Teams managing high-traffic repositories can opt specific PRs into review rather than reviewing every PR or every push, providing more granular cost control.
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

- **New `@claude review` comment command**: Posting `@claude review` as a top-level PR comment starts a review on-demand and opts that PR into push-triggered reviews going forward. This works in any configured trigger mode — not only Manual.
  > *"Comment `@claude review` on a pull request to start a review and opt that PR into push-triggered reviews going forward. This works regardless of the repository's configured trigger: use it to opt specific PRs into review in Manual mode, or to get an immediate re-review in other modes."*
  - *Implication*: Developers can request an immediate re-review in any mode without waiting for an automatic trigger. Notably, using this command in any mode causes all subsequent pushes to that PR to trigger reviews, which has billing implications.
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

  **Requirements for `@claude review` to trigger a review:**
  - Must be a top-level PR comment (not an inline comment on a diff line)
  - `@claude review` must appear at the start of the comment
  - Commenter must have owner, member, or collaborator repository access
  - PR must be open and not a draft
  - If a review is already in progress, the request is queued until it completes

### Configuration

- **Review trigger option labels renamed**: The options in the admin settings **Review Behavior** dropdown were renamed (the dropdown itself was also given this explicit label). A third "Manual" option was added.

  | Old Label | New Label |
  |-----------|-----------|
  | After PR creation only | Once after PR creation |
  | After every push to PR branch | After every push |
  | *(not available)* | Manual *(new)* |

  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

- **Updated setup verification instructions**: The post-setup verification step now distinguishes between automatic and manual trigger configurations.
  > *"If you chose an automatic trigger, a check run named Claude Code Review appears within a few minutes. If you chose Manual, comment `@claude review` on the PR to start the first review."*
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

## Notable Details

- **Cost implications of `@claude review` in any mode**: The billing section now explicitly notes that commenting `@claude review` opts a PR into push-triggered reviews going forward, meaning cost accrues per push even when starting from Manual mode. This is a meaningful billing consideration for teams using Manual mode to control spend.
  > *"In any mode, commenting `@claude review` opts the PR into push-triggered reviews, so additional cost accrues per push after that comment."*

- **"How reviews work" section updated**: The opening paragraph now leads with the three possible trigger conditions before describing review agent mechanics, giving administrators clearer framing before they reach the configuration section.
  > *"reviews trigger when a PR opens, on every push, or when manually requested, depending on the repository's configured behavior. Commenting `@claude review` starts reviews on a PR in any mode."*

- **Manual mode cost guidance replaces "on-push" advisory**: The previous recommendation to "Start with PR creation only and switch to on-push for repos where you want continuous coverage" was replaced with a description of when Manual mode is appropriate: *"Manual mode is useful for high-traffic repos where you want to opt specific PRs into review, or to only start reviewing your PRs once they're ready."*

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| code-review.md | Modified | +27/-8 | Added Manual trigger mode, `@claude review` comment command, renamed trigger option labels, updated billing section |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-13*
