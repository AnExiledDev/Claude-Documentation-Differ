# Claude Code Documentation Changes — 2026-04-15

## Summary

Three documentation pages were updated today. The most significant change is a major reduction in the GitHub trigger event types supported by Routines — from 17 categories down to 2 (Pull request and Release). The extended-thinking indicator also received a UI improvement, now displaying rotating progress hints during active reasoning.

## Significant Changes

### Routines — GitHub Trigger Events Narrowed

- **Supported GitHub trigger events reduced from 17 to 2**: The Routines GitHub trigger previously supported a broad set of event categories (push, issues, PR reviews, workflow runs, discussions, check runs, merge queue, etc.). The documentation now lists only **Pull request** and **Release** as supported event categories.

  Previous text:
  > GitHub triggers can subscribe to **any** of the following event categories.

  Updated to:
  > GitHub triggers can subscribe to **either** of the following event categories.

  The supported events table was trimmed from 17 rows to 2:

  | Event        | Triggers when                                                                 |
  | :----------- | :---------------------------------------------------------------------------- |
  | Pull request | A PR is opened, closed, assigned, labeled, synchronized, or otherwise updated |
  | Release      | A release is created, published, edited, or deleted                           |

  - *Implication*: Routines that previously relied on GitHub triggers for push events, issues, workflow runs, discussions, check runs, or other event types are no longer documented as supported. The trigger overview description was also updated to reflect this — "run automatically in response to repository events such as pull requests or releases" (previously also listed "pushes, issues, or workflow runs").
  - *Source*: [Routines](https://code.claude.com/docs/en/routines.md)

- **Pull request filter operators now documented**: New text was added explaining how PR filter conditions work, including operator semantics and important behavior of the `matches regex` operator.

  > Each filter pairs a field with an operator: equals, contains, starts with, is one of, is not one of, or matches regex.
  >
  > The `matches regex` operator tests the entire field value, not a substring within it. To match any title containing `hotfix`, write `.*hotfix.*`. Without the surrounding `.*`, the filter matches only a title that is exactly `hotfix` with nothing before or after. For literal substring matching without regex syntax, use the `contains` operator instead.

  - *Implication*: This clarifies a non-obvious behavior: regex filters are implicitly anchored to the full field value, not a substring. Users expecting partial-match semantics should wrap patterns in `.*….*` or use the `contains` operator instead.
  - *Source*: [Routines](https://code.claude.com/docs/en/routines.md)

### Extended Thinking — Progress Hints in Indicator

- **Rotating progress hints added to the extended-thinking indicator** (v2.1.109): The extended-thinking UI now shows progress hints below the indicator while Claude is actively reasoning.

  > During extended thinking, progress hints appear below the indicator to show that Claude is actively working.

  - *Implication*: Provides visible feedback during long reasoning sessions, reducing ambiguity about whether the model is still processing.
  - *Source*: [Common Workflows](https://code.claude.com/docs/en/common-workflows.md), [Changelog](https://code.claude.com/docs/en/changelog.md)

## Notable Details

- The session-mapping note for GitHub-triggered routines was updated in sync with the event reduction: it previously cited "two pushes or two PR updates produce two independent sessions"; it now reads "two PR updates produce two independent sessions", consistent with push events no longer being listed as supported.
- Version 2.1.109 (April 15, 2026) contains a single change: the extended-thinking indicator improvement.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `routines.md` | Modified | +12 / -24 | GitHub trigger events reduced from 17 to 2 (Pull request, Release); PR filter operator behavior documented |
| `changelog.md` | Modified | +4 / -0 | Added v2.1.109 entry: extended-thinking indicator with rotating progress hints |
| `common-workflows.md` | Modified | +1 / -1 | Added sentence documenting progress hints during extended thinking |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-15*
