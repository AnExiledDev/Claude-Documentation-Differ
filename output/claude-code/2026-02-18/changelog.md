# Claude Code Documentation Changes — 2026-02-18

## Summary

One page was modified: `legal-and-compliance.md` gained a new **Usage policy** section (+18/-1 lines) covering acceptable use and authentication/credential restrictions. The sole deletion was a minor wording fix ("Consumer Terms" → "Consumer Terms of Service"). No pages were added or removed.

## Significant Changes

### Policy & Compliance

- **New "Usage policy" section added to Legal and Compliance page**: Anthropic has formally documented constraints on how Claude Code's usage limits and authentication mechanisms may be used, with explicit rules targeting developers who might attempt to route API traffic through consumer plan credentials.

  > Claude Code usage is subject to the [Anthropic Usage Policy](https://www.anthropic.com/legal/aup). Advertised usage limits for Pro and Max plans assume ordinary, individual usage of Claude Code and the Agent SDK.

  - *Implication*: Developers building tools on top of Claude Code should review this section — it makes clear that Pro/Max usage limits are not intended to be shared or proxied for third-party applications.
  - *Source*: [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance.md)

- **OAuth token restrictions explicitly prohibited for third-party use**: A new "Authentication and credential use" subsection clarifies that OAuth tokens from Free, Pro, or Max accounts are restricted to Claude Code and Claude.ai only.

  > **OAuth authentication** (used with Free, Pro, and Max plans) is intended exclusively for Claude Code and Claude.ai. Using OAuth tokens obtained through Claude Free, Pro, or Max accounts in any other product, tool, or service — including the [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) — is not permitted and constitutes a violation of the [Consumer Terms of Service](https://www.anthropic.com/legal/consumer-terms).

  - *Implication*: Any developer currently using OAuth tokens from consumer plans to power their own products or services (e.g., wrappers, bots, automations using the Agent SDK) is now explicitly in violation of the Consumer Terms of Service. The required path is API key authentication via Claude Console.
  - *Source*: [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance.md)

- **Third-party "Claude.ai login" explicitly prohibited**: The documentation now states that Anthropic does not permit third-party developers to offer Claude.ai login flows or route requests through consumer plan credentials on behalf of their users.

  > Anthropic does not permit third-party developers to offer Claude.ai login or to route requests through Free, Pro, or Max plan credentials on behalf of their users.

  - *Implication*: Products offering "Sign in with Claude.ai" or credential-sharing patterns for end users are not permitted. Developers must use their own API keys.
  - *Source*: [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance.md)

- **Enforcement notice added**: The new section closes with a reminder that Anthropic may enforce these restrictions without prior notice.

  > Anthropic reserves the right to take measures to enforce these restrictions and may do so without prior notice.

  - *Implication*: Accounts found in violation may be acted upon without a warning period.
  - *Source*: [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance.md)

## Notable Details

- **Minor wording fix**: "Consumer Terms" was updated to "Consumer Terms of Service" in the License section — a small label correction aligning the text with the official name of the linked agreement.
- The Agent SDK is referenced twice in the new content, explicitly placing it in scope of both the usage limits note and the OAuth restriction. This signals that Anthropic is proactively addressing patterns they may be observing with the Agent SDK's growing adoption.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| legal-and-compliance.md | Modified | +18 / -1 | Added "Usage policy" section covering acceptable use limits and OAuth/API key authentication restrictions |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-18*
