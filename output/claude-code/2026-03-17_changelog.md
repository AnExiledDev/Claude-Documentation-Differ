# Claude Code Documentation Changes — 2026-03-17

## Summary

17 pages were modified in this update with no pages added or removed (176 additions, 85 deletions). The most significant changes are: a new Troubleshooting section for Remote Control, sandbox path-merging behavior documentation, authentication scope clarifications for `apiKeyHelper` and API key environment variables, a new plugin marketplace section for containerized environments, and streaming `api_retry` event documentation for programmatic usage.

## Significant Changes

### Authentication

- **`apiKeyHelper` slow-response warning**: Claude Code now displays a prompt-bar notice when `apiKeyHelper` takes longer than 10 seconds to return a credential, showing elapsed time.
  > "if `apiKeyHelper` takes longer than 10 seconds to return a key, Claude Code displays a warning notice in the prompt bar showing the elapsed time. If you see this notice regularly, check whether your credential script can be optimized."
  - *Implication*: Developers using custom credential scripts can now diagnose slow auth helpers at a glance without enabling debug logging.
  - *Source*: [Authentication](https://code.claude.com/docs/en/authentication.md)

- **API key env vars are terminal CLI–only**: The documentation now explicitly states that `apiKeyHelper`, `ANTHROPIC_API_KEY`, and `ANTHROPIC_AUTH_TOKEN` apply only to terminal CLI sessions, not Claude Desktop or remote sessions.
  > "`apiKeyHelper`, `ANTHROPIC_API_KEY`, and `ANTHROPIC_AUTH_TOKEN` apply to terminal CLI sessions only. Claude Desktop and remote sessions use OAuth exclusively and do not call `apiKeyHelper` or read API key environment variables."
  - *Implication*: Teams mixing CLI with Desktop or remote sessions should not expect credential helpers or API key env vars to take effect outside the terminal.
  - *Source*: [Authentication](https://code.claude.com/docs/en/authentication.md)

### Sandboxing

- **Sandbox path arrays merge across settings scopes**: The documentation now clarifies that `allowWrite`, `denyWrite`, `denyRead`, and `allowRead` path arrays **merge** across all settings scopes rather than being replaced by higher-priority scopes.
  > "When `allowWrite` (or `denyWrite`/`denyRead`/`allowRead`) is defined in multiple settings scopes, the arrays are **merged**, meaning paths from every scope are combined, not replaced. For example, if managed settings allow writes to `//opt/company-tools` and a user adds `~/.kube` in their personal settings, both paths are included in the final sandbox configuration. This means users and projects can extend the list without duplicating or overriding paths set by higher-priority scopes."
  - *Implication*: Managed settings and user settings for sandbox paths coexist rather than conflict. Admins can set baseline paths; users can extend them.
  - *Source*: [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)

- **Path prefix resolution table for sandbox settings**: An explicit table was added documenting how path prefixes resolve in `allowWrite`, `denyWrite`, `denyRead`, and `allowRead`:

  | Prefix | Meaning | Example |
  |--------|---------|---------|
  | `//` | Absolute path from filesystem root | `//tmp/build` → `/tmp/build` |
  | `~/` | Relative to home directory | `~/.kube` → `$HOME/.kube` |
  | `/` | Relative to the settings file's directory | `/build` → `$SETTINGS_DIR/build` |
  | `./` or no prefix | Relative path (resolved by sandbox runtime) | `./output` |

  - *Implication*: Removes ambiguity — a path like `/Users/alice/...` in a settings file is *not* an absolute path; it resolves relative to the settings file location. Use `//Users/alice/...` for absolute paths.
  - *Source*: [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)

### Remote Control

- **New Troubleshooting section**: Added guidance for the `Remote credentials fetch failed` error, including how to obtain full details via `--verbose` and a breakdown of common causes.
  > "If your terminal shows `Remote credentials fetch failed — see debug log`, Claude Code could not obtain a short-lived credential from the Anthropic API to establish the Remote Control connection. To see the full error detail, re-run with the `--verbose` flag: `claude remote-control --verbose`"

  Common causes now documented:
  - Not signed in — API key authentication is not supported for Remote Control; use `/login` to authenticate via claude.ai.
  - Network or proxy blocking outbound HTTPS (port 443) to the Anthropic API.
  - Inactive subscription — confirmed by an accompanying `Session creation failed` log entry.
  - *Implication*: Users troubleshooting Remote Control now have a clear diagnostic path, including a specific error message pattern to watch for.
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

### Plugin Marketplaces

- **New section: "Pre-populate plugins for containers"**: Added guidance for pre-populating plugins in containerized environments where interactive `/plugin install` workflows are unavailable.
  - *Implication*: Teams running Claude Code in Docker or CI containers can now configure plugins declaratively at image build time using the `CLAUDE_CODE_PLUGIN_SEED_DIR` environment variable.
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

### Programmatic / Headless Mode

- **`system/api_retry` streaming event documented**: When an API request fails with a retryable error during `stream-json` output mode, Claude Code emits a `system/api_retry` event before retrying. The documentation now includes a complete field reference:

  | Field | Type | Description |
  |-------|------|-------------|
  | `type` | `"system"` | message type |
  | `subtype` | `"api_retry"` | identifies this as a retry event |
  | `attempt` | integer | current attempt number, starting at 1 |
  | `max_retries` | integer | total retries permitted |
  | `retry_delay_ms` | integer | milliseconds until the next attempt |
  | `error_status` | integer or null | HTTP status code, or `null` for connection errors with no HTTP response |
  | `error` | string | error category: `authentication_failed`, `billing_error`, `rate_limit`, `invalid_request`, `server_error`, `max_output_tokens`, or `unknown` |
  | `uuid` | string | unique event identifier |
  | `session_id` | string | session the event belongs to |

  > "When an API request fails with a retryable error, Claude Code emits a `system/api_retry` event before retrying. You can use this to surface retry progress or implement custom backoff logic."
  - *Implication*: Automation scripts consuming streaming output can now detect retries and implement observability, alerting, or custom backoff around transient API failures.
  - *Source*: [Run Claude Code programmatically](https://code.claude.com/docs/en/headless.md)

- **Headless mode terminology clarified**: A note was added stating that the CLI (`claude -p`) was previously called "headless mode" — the `-p` flag and all CLI options work the same way.
  - *Source*: [Run Claude Code programmatically](https://code.claude.com/docs/en/headless.md)

### Permissions

- **`allow_remote_sessions` added to managed-only settings**: A new managed-only setting controls whether users can start Remote Control and web sessions. Defaults to `true`; set to `false` to block remote session access organization-wide.
  > "`allow_remote_sessions`: When `true`, allows users to start Remote Control and web sessions. Defaults to `true`. Set to `false` to prevent remote session access."
  - *Implication*: Enterprise administrators can now centrally disable remote session capabilities via managed policy settings.
  - *Source*: [Configure permissions](https://code.claude.com/docs/en/permissions.md)

### Common Workflows

- **PR session auto-linking**: Sessions are now automatically linked to pull requests created with `gh pr create`. Linked sessions can be resumed later with `claude --from-pr <number>`.
  > "When you create a PR using `gh pr create`, the session is automatically linked to that PR. You can resume it later with `claude --from-pr <number>`."
  - *Source*: [Common workflows](https://code.claude.com/docs/en/common-workflows.md)

- **Code intelligence plugin tip added**: The "Find relevant code" workflow now recommends installing a language-specific code intelligence plugin to give Claude precise "go to definition" and "find references" navigation rather than relying solely on text search.
  - *Source*: [Common workflows](https://code.claude.com/docs/en/common-workflows.md)

### Memory

- **Subagent auto memory callout**: A note was added clarifying that subagents can maintain their own auto memory across conversations — the memory page previously covered only the main session.
  > "Subagents can also maintain their own auto memory. See subagent configuration for details."
  - *Source*: [How Claude remembers your project](https://code.claude.com/docs/en/memory.md)

## Notable Details

- **`Task` tool renamed to `Agent` (v2.1.63)**: Sub-agents documentation now includes an explicit note that the `Task` tool was renamed to `Agent` in v2.1.63, and that existing `Task(...)` references in settings and agent definitions continue to work as aliases.
  > "In version 2.1.63, the Task tool was renamed to Agent. Existing `Task(...)` references in settings and agent definitions still work as aliases."

- **Hooks reference and guide tables (+14/-14 and +3/-1)**: The equal line counts in `hooks.md` suggest description refinements or matcher value clarifications rather than new events. Both the reference and guide tables list `InstructionsLoaded`, `ElicitationResult`, `PostToolUseFailure`, and `Elicitation` events consistently.

- **Compound bash `"always allow"` behavior documented in permissions** (`permissions.md`, +16/-11): The permissions page now explicitly documents that approving a compound command (e.g., `git status && npm test`) saves separate rules per subcommand — up to 5 rules — rather than a single rule for the full string. This corrects an earlier behavior where full-string rules would go stale.

- **Plugin marketplaces and plugins-reference content is substantial**: `plugin-marketplaces.md` at +35/-8 is the largest change by net additions. Beyond the new container section, the diff includes expanded source type documentation and reference table clarifications.

- **Settings page restructured** (`settings.md`, +21/-19): The near-equal additions and deletions indicate table reformatting or setting description updates rather than new settings. No new settings names are surfaced in the page content observed.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| authentication.md | Modified | +4/-1 | apiKeyHelper slow warning; CLI-only scope for API key env vars |
| commands.md | Modified | +3/-3 | Minor command description updates |
| common-workflows.md | Modified | +14/-12 | PR session auto-linking; code intelligence plugin tip |
| costs.md | Modified | +1/-1 | Minor wording update |
| env-vars.md | Modified | +5/-3 | Environment variable table updates |
| headless.md | Modified | +14/-0 | api_retry streaming event documented; headless mode terminology note |
| hooks-guide.md | Modified | +3/-1 | Hook event table refinements |
| hooks.md | Modified | +14/-14 | Hook event descriptions and matcher value clarifications |
| interactive-mode.md | Modified | +1/-0 | Minor addition |
| memory.md | Modified | +2/-0 | Note that subagents can maintain auto memory |
| permissions.md | Modified | +16/-11 | allow_remote_sessions managed setting; compound bash rule behavior |
| plugin-marketplaces.md | Modified | +35/-8 | New "Pre-populate plugins for containers" section; source table clarifications |
| plugins-reference.md | Modified | +8/-8 | Technical reference clarifications |
| remote-control.md | Modified | +14/-0 | New Troubleshooting section for credential fetch failures |
| sandboxing.md | Modified | +17/-2 | Array merging behavior; path prefix resolution table |
| settings.md | Modified | +21/-19 | Settings table restructuring |
| sub-agents.md | Modified | +4/-2 | Task→Agent rename note; frontmatter field table updates |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-17*
