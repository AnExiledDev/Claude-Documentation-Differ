# Claude Code Documentation Changes — 2026-03-18

## Summary

One page was modified: the Remote Control documentation. The update adds three new structured troubleshooting subsections covering distinct error states users may encounter, clarifies the admin opt-in requirement for Team/Enterprise plans, and replaces a vague session-naming sentence with an explicit priority-ordered list.

## Significant Changes

### Remote Control Troubleshooting Expansion

- **Three new named error subsections added to Troubleshooting**: The troubleshooting section was restructured from a single paragraph about credential failures into three subsections, each keyed to a specific error message.

  **"Remote Control is not yet enabled for your account"** — documents environment variables that block the eligibility check:
  > `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` or `DISABLE_TELEMETRY`: unset them and try again.
  > `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX`, or `CLAUDE_CODE_USE_FOUNDRY`: Remote Control requires claude.ai authentication and does not work with third-party providers.

  - *Implication*: Developers using Bedrock, Vertex, or Foundry providers — or those with telemetry-related env vars set — now have explicit guidance rather than encountering a silent failure.

  **"Remote Control is disabled by your organization's policy"** — lists three distinct root causes, with the most common flagged explicitly:
  > This error has three distinct causes. The first is the most common on developer machines.
  >
  > - **You're authenticated with an API key or Console account**: Remote Control requires claude.ai OAuth. Run `/login` and choose the claude.ai option. If `ANTHROPIC_API_KEY` is set in your environment, unset it.
  > - **Your Team or Enterprise admin hasn't enabled it**: Remote Control is off by default on these plans. An admin can turn it on at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code). The Remote Control toggle depends on the Claude Code on the web toggle on the same page; enable Claude Code on the web first if Remote Control appears unavailable.
  > - **The admin toggle is grayed out**: your organization has a data retention or compliance configuration that is incompatible with Remote Control. This cannot be changed from the admin panel. Contact Anthropic support to discuss options.

  - *Implication*: The `ANTHROPIC_API_KEY` override is now explicitly identified as the most common cause of this error on developer machines. The compliance/data-retention dead-end case is newly documented — users in that state now know to contact Anthropic support rather than continuing to troubleshoot locally. The dependency between the "Claude Code on the web" toggle and the Remote Control toggle is also newly surfaced here.

  **"Remote credentials fetch failed"** — the existing credential-failure paragraph was promoted to a named subsection with minor wording cleanup (no substantive content change).

  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

### Session Title Priority Order Clarified

- **Named session title resolution replaced with an ordered list**: A single prose sentence was replaced with a numbered priority list making the precedence unambiguous.

  Before:
  > The remote session takes its name from the `--name` argument (or the name passed to `/remote-control`), your last message, your `/rename` value, or "Remote Control session" if there's no conversation history.

  After:
  > 1. The name you passed to `--name`, `--remote-control`, or `/remote-control`
  > 2. The title you set with `/rename`
  > 3. The last meaningful message in existing conversation history
  > 4. Your first prompt once you send one

  - *Implication*: `/rename` is now explicitly ranked second (above conversation history), which the previous prose did not make clear. The "Remote Control session" fallback default is gone — if no name source applies yet, the session title is set by the user's first prompt.
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

### Admin Opt-In Wording Sharpened

- **Remote Control described as off by default on Team/Enterprise**: Both the introductory Note and the Requirements section updated to make the opt-in nature of the feature explicit, and to name the specific toggle involved.

  Before (Note):
  > Team and Enterprise admins must first enable Claude Code in admin settings.

  After (Note):
  > On Team and Enterprise, it is off by default until an admin enables the Remote Control toggle in Claude Code admin settings.

  Before (Requirements):
  > Team and Enterprise admins must first enable Claude Code in admin settings.

  After (Requirements):
  > On Team and Enterprise, an admin must first enable the Remote Control toggle in Claude Code admin settings.

  - *Implication*: Remote Control now has a documented dedicated toggle (distinct from the broader "Claude Code" admin setting). The default-off state on Team/Enterprise plans is explicitly stated rather than implied.
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `remote-control.md` | Modified | +31 / -5 | Three new troubleshooting subsections; admin opt-in wording sharpened; session-naming replaced with ordered priority list |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-18*
