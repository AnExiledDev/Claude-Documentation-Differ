# Claude Code Documentation Changes — 2026-04-16

## Summary

Three pages received minor updates in this diff cycle. The primary themes are: one new feature entry added to the v2.1.110 changelog (push notifications for Remote Control sessions), and a cross-cutting clarification that cost figures in Claude Code are client-side estimates rather than authoritative billing amounts — applied consistently across both the costs reference page and the statusline field table.

## Significant Changes

### Features

- **Push notification tool added to v2.1.110 release notes**: The changelog now documents that Claude can send mobile push notifications during Remote Control sessions when the "Push when Claude decides" configuration is enabled.
  > Added push notification tool — Claude can send mobile push notifications when Remote Control and "Push when Claude decides" config are enabled
  - *Implication*: Users running Remote Control sessions can receive proactive mobile alerts from Claude without polling the interface manually.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Cost Reporting Accuracy

- **`/cost` command output reframed as a local estimate**: The costs page previously introduced the `/cost` command without qualification. It now explicitly states the dollar figure is computed locally from token counts and may not match the actual bill, with a direct pointer to the Claude Console for authoritative usage data.
  > The `/cost` command provides detailed token usage statistics for your current session. The dollar figure is an estimate computed locally from token counts and may differ from your actual bill. For authoritative billing, see the Usage page in the [Claude Console](https://platform.claude.com/usage).
  - *Implication*: Developers relying on `/cost` for budgeting or cost attribution should cross-reference with the Console; the in-session figure is approximate.
  - *Source*: [Costs](https://code.claude.com/docs/en/costs.md)

- **`cost.total_cost_usd` statusline field description updated**: The statusline JSON schema reference now labels this field as a client-side estimate that may diverge from actual billing, replacing the previous unqualified "Total session cost in USD".
  > `cost.total_cost_usd` — Estimated session cost in USD, computed client-side. May differ from your actual bill
  - *Implication*: Scripts and status line integrations displaying this value should treat it as approximate. The prose section under "Cost and duration tracking" was also updated to use "estimated cost" for consistency.
  - *Source*: [Statusline](https://code.claude.com/docs/en/statusline.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `changelog.md` | Modified | +1 / -0 | Added push notification tool entry to the v2.1.110 release notes |
| `costs.md` | Modified | +1 / -1 | Clarified `/cost` output is a local estimate; added link to Claude Console for billing |
| `statusline.md` | Modified | +2 / -2 | Updated `cost.total_cost_usd` field description and prose to read "estimated" cost |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-16*
