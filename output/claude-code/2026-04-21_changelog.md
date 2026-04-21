# Claude Code Documentation Changes — 2026-04-21

## Summary

Two pages were updated to clarify that the 3 free ultrareview runs included for Pro and Max subscribers now carry an explicit expiration date of **May 5, 2026**. Previously the free runs were described only as a "one-time allotment"; they are now also time-limited — unused runs expire on May 5, 2026 regardless of whether they have been consumed.

## Significant Changes

### Billing / Pricing

- **Ultrareview free runs now expire on May 5, 2026**: The 3 free ultrareview runs included for Pro and Max plan subscribers were previously described as a "one-time allotment per account" with no time constraint. Documentation now adds a hard deadline — unused free runs expire on May 5, 2026 even if not consumed.

  > *Before (pricing table):* "3 free runs, one-time"
  > *After (pricing table):* "3 free runs through May 5, 2026"

  > "These three runs are a one-time allotment per account, do not refresh, and expire on May 5, 2026. After you use all three, or after the free run period ends, each review is billed to extra usage and typically costs $5 to $20 depending on the size of the change."

  - *Implication*: Pro and Max users who haven't tried ultrareview have until May 5, 2026 to use their free runs. The new "or after the free run period ends" clause means the deadline is absolute — runs are forfeited if not used by that date, regardless of count.
  - *Source*: [ultrareview.md](https://code.claude.com/docs/en/ultrareview.md)

  The `/ultrareview` entry in the commands reference was updated to match:

  > *Before:* "Includes 3 free runs on Pro and Max, then requires extra usage"
  > *After:* "Includes 3 free runs on Pro and Max **through May 5, 2026**, then requires extra usage"

  - *Source*: [commands.md](https://code.claude.com/docs/en/commands.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| commands.md | Modified | +1/-1 | Added "through May 5, 2026" deadline to `/ultrareview` free-run description |
| ultrareview.md | Modified | +6/-6 | Pricing table and prose updated to reflect May 5, 2026 expiration for free runs |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-21*
