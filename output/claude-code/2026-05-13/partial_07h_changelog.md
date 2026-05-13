# Claude Code Documentation Changes — 2026-05-13

## Summary

Three pages were updated in this cycle. The most substantive change documents a v2.1.139 behavior fix: `claude auth` subcommands are now exempt from the `forceRemoteSettingsRefresh` fail-closed check, preventing a lockout when expired credentials cause the settings fetch to fail. Two minor clarifications were also added to Auto-fix controls and Sonnet 1M context availability.

## Significant Changes

### Configuration

- **`forceRemoteSettingsRefresh` auth exemption (v2.1.139)**: When `forceRemoteSettingsRefresh: true` is configured and the Anthropic API is unreachable, the CLI now allows `claude auth` subcommands to proceed instead of exiting. This prevents a bootstrap deadlock where expired credentials caused the settings fetch to fail, which then prevented re-authentication.
  > As of v2.1.139, the `claude auth` subcommands such as `claude auth login` are exempt from this check, so users can re-authenticate when expired credentials are the reason the settings fetch fails.
  - *Implication*: Administrators using `forceRemoteSettingsRefresh` no longer need to provision out-of-band recovery flows for credential expiry. Users can self-serve re-authentication even in fail-closed mode.
  - The security considerations table was also updated to reflect this exemption for the "API is unavailable" scenario.
  - *Source*: [Server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md)

## Minor Changes

- **`claude-code-on-the-web.md`**: Added a clarification that Auto-fix is a per-PR toggle. Documents how to stop monitoring: open the CI status bar in the web session and clear the **Auto-fix** toggle, or tell Claude to stop watching the PR. (+2/-0 lines)

- **`model-config.md`**: Clarified that Sonnet with 1M context is not included in the automatic upgrade available on Max, Team, and Enterprise plans. Sonnet 1M context requires [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) on every subscription plan, including Max. (+1/-1 lines)

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| server-managed-settings.md | Modified | SIGNIFICANT | +9/-7 | `claude auth` subcommands exempt from `forceRemoteSettingsRefresh` fail-closed check (v2.1.139); security table updated |
| claude-code-on-the-web.md | Modified | MINOR | +2/-0 | Auto-fix described as per-PR toggle with instructions to stop monitoring |
| model-config.md | Modified | MINOR | +1/-1 | Sonnet 1M context requires extra usage on all plans; not part of automatic Opus upgrade |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-13*
