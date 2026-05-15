# Claude API Documentation Changes — 2026-05-15

## Summary

One documentation page was modified today, affecting the Managed Agents Dreams API (Research Preview). The change removes the optional status of the `sessions` input, establishing a minimum of 1 session required per dream job.

## Minor Changes

- **dreams.md**: Sessions input changed from "optionally, up to 100" to "1 to 100" — sessions are now explicitly required (minimum 1). Prose updated from "an optional array of sessions" to "an array of sessions" to match. (+2/-2 lines)

## Migration Notes

- **Dreams `sessions` input is now required**: Documentation previously described sessions as optional when creating a dream. It now specifies a range of 1 to 100 sessions. Developers creating dreams without any sessions input should supply at least one session transcript. This applies to the Research Preview `dreaming-2026-04-21` beta feature.

## Notable Details

The change removes "optionally" in two places within the Dreams page:

> **Before:** `optionally, up to 100 **sessions**: past transcripts Claude mines for patterns and insights to fold into the output.`
> **After:** `1 to 100 **sessions**: past transcripts Claude mines for patterns and insights to fold into the output.`

> **Before:** `Dreaming inputs include the pre-existing memory store and an optional array of sessions.`
> **After:** `Dreaming inputs include the pre-existing memory store and an array of sessions.`

The minimum bound of 1 is newly explicit. Since Dreams is a Research Preview feature (requiring both `managed-agents-2026-04-01` and `dreaming-2026-04-21` beta headers), this kind of behavioral refinement is expected during the preview period.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| dreams.md | Modified | MINOR | +2/-2 | Sessions input changed from optional to required (1–100 minimum) |

---
*Generated from Claude API documentation changes detected on 2026-05-15*
*Source: [Dreams — Managed Agents](https://platform.claude.com/docs/en/managed-agents/dreams.md)*
