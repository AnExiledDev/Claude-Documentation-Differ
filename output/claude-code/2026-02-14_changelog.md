# Claude Code Documentation Changes — 2026-02-14

## Summary

Two documentation pages received minor updates: the agent teams page added a visual diagram comparing subagents and agent teams, and the network configuration page revised its list of required URLs to reflect authentication endpoints.

## Significant Changes

### Documentation Enhancements

- **Agent Teams Architecture Diagram**: The agent teams documentation now includes a visual comparison diagram showing the architectural differences between subagents and agent teams
  > "Subagents only report results back to the main agent and never talk to each other. In agent teams, teammates share a task list, claim work, and communicate directly with each other."
  - *Implication*: Developers evaluating whether to use subagents or agent teams can now see a visual representation of how each approach handles communication and coordination
  - *Source*: [Agent Teams](https://code.claude.com/docs/en/agent-teams.md)

### Network Configuration

- **Required URLs Updated**: The network access requirements section was revised to focus on authentication endpoints, removing telemetry and error reporting URLs
  - Before: Listed `api.anthropic.com`, `claude.ai`, `statsig.anthropic.com`, and `sentry.io`
  - After: Lists `api.anthropic.com` (Claude API endpoints), `claude.ai` (authentication for claude.ai accounts), and `platform.claude.com` (authentication for Anthropic Console accounts)
  - *Implication*: Enterprise network administrators should ensure `platform.claude.com` is allowlisted in addition to the existing `api.anthropic.com` and `claude.ai` endpoints. The removal of `statsig.anthropic.com` and `sentry.io` suggests these services may now be optional or routed differently.
  - *Source*: [Network Configuration](https://code.claude.com/docs/en/network-config.md)

## Notable Details

The network configuration change shifts from generic descriptions ("WebFetch safeguards") to specific use cases ("authentication for claude.ai accounts"), clarifying the purpose of each endpoint. The addition of `platform.claude.com` indicates support for authentication through the Anthropic Console in addition to claude.ai accounts.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| agent-teams.md | Modified | +6/-0 | Added visual diagram comparing subagent and agent team architectures |
| network-config.md | Modified | +3/-4 | Updated network access requirements, added platform.claude.com endpoint |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-14*
