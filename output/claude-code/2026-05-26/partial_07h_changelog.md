# Claude Code Documentation Changes — 2026-05-26

## Summary

One page was modified in this update. The GitHub Enterprise Server documentation was updated to add Claude Security as a supported feature for GHES, noting it is available in public beta for Enterprise plans. Related setup instructions and permissions descriptions were updated accordingly.

## Significant Changes

### Integrations

- **Claude Security now supported on GitHub Enterprise Server**: A new entry was added to the GHES feature support table documenting that Claude Security works with self-hosted GitHub Enterprise Server instances.
  > `| Claude Security | ✅ Supported | Available in public beta for Enterprise plans at [claude.ai/security](https://claude.ai/security) |`
  - *Implication*: Enterprise plan users on GHES can now enroll in the Claude Security public beta. The existing GitHub App manifest (configured during admin setup) already provisions the required permissions — no separate app installation is needed.
  - *Source*: [GitHub Enterprise Server](https://code.claude.com/docs/en/github-enterprise-server.md)

- **Admin setup step updated to include Claude Security**: The "Enable features" step in the GHES admin setup guide now explicitly lists Claude Security alongside Code Review and contribution metrics.
  > `Return to claude.ai/admin-settings/claude-code and enable Code Review, Claude Security, and contribution metrics for your GHES repositories using the same configuration as github.com.`
  - *Implication*: Admins setting up a new GHES connection should visit the admin settings page to enable Claude Security in addition to the other features.
  - *Source*: [GitHub Enterprise Server](https://code.claude.com/docs/en/github-enterprise-server.md)

- **GitHub App permissions description updated**: The description of what the auto-generated GitHub App manifest covers now includes Claude Security.
  > `The manifest configures the GitHub App with the permissions and webhook events Claude needs across web sessions, Code Review, Claude Security, and contribution metrics:`
  - *Implication*: The manifest-based setup already covers Claude Security; no additional GitHub App permission grants are required.
  - *Source*: [GitHub Enterprise Server](https://code.claude.com/docs/en/github-enterprise-server.md)

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| github-enterprise-server.md | Modified | SIGNIFICANT | +3/-2 | Added Claude Security as a supported GHES feature (public beta, Enterprise plans); updated setup and permissions descriptions |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-26*
