# Claude Code Documentation Changes — 2026-04-17

## Summary

This update introduces a new standalone error reference page and documents several recently shipped features: plugin background monitors, mobile push notifications for Remote Control, session recap, cloud environment caching, MCP automatic reconnection, and a `minimumVersion` update pin. Monitoring coverage expands with two new raw API body OTel events. Forty-one existing pages received updates, mostly to reflect these features and add cross-links.

---

## Significant Changes

### New Feature: Error Reference Page

- **Comprehensive runtime error lookup**: A new `errors.md` page catalogs every runtime error Claude Code can surface — 20+ distinct messages — organized into five categories: Server errors, Usage limits, Authentication, Network/connection, and Request errors. Each entry shows the exact error string, explains the cause, and provides step-by-step recovery.
  > "This page lists runtime errors Claude Code displays and how to recover from each one... These errors and recovery commands apply across the CLI, the Desktop app, and Claude Code on the web, since all three wrap the same Claude Code CLI."
  - *Implication*: Developers troubleshooting failures now have a single authoritative destination instead of scattered troubleshooting docs. The page also clarifies the retry behavior (`CLAUDE_CODE_MAX_RETRIES`, default 10 attempts with exponential backoff) and links to `API_TIMEOUT_MS`.
  - *Source*: [Error reference](https://code.claude.com/docs/en/errors.md)

### Features

#### Remote Control: Mobile Push Notifications

- **Push notifications when Claude finishes or needs input**: Remote Control sessions can now send push notifications to the Claude mobile app. Claude decides autonomously when to push (long-running task completion, decisions required). Users can also request a push explicitly in their prompt.
  > "When Remote Control is active, Claude can send push notifications to your phone. Claude decides when to push. It typically sends one when a long-running task finishes or when it needs a decision from you to continue."
  - *Implication*: Enables truly async workflows — start a long task, step away, and receive a notification when Claude needs you. Requires Claude Code v2.1.110+, the Claude mobile app (iOS or Android), and enabling **Push when Claude decides** in `/config`.
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

#### Interactive Mode: Session Recap

- **Automatic one-line recap on return**: When 3+ minutes pass since the last completed turn and the terminal is unfocused, Claude Code generates a background recap. It appears when you switch back to the terminal, so you immediately see what happened while you were away.
  > "When you return to the terminal after stepping away, Claude Code shows a one-line recap of what happened in the session so far... Run `/recap` to generate a summary on demand. To turn automatic recaps off, open `/config` and disable **Session recap**."
  - *Implication*: Reduces cognitive overhead in long sessions. On by default across all plans and providers. Controllable via `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` env var (set to `0` to disable).
  - *Source*: [Interactive mode](https://code.claude.com/docs/en/interactive-mode.md)

#### Plugin System: Background Monitors

- **Plugins can now declare persistent background monitors**: A new `monitors` plugin component lets plugins run shell commands as long-lived background processes. Each stdout line is delivered to Claude as a notification, so Claude can react to log entries, CI status, or polled events automatically.
  > "Plugins can declare background monitors that Claude Code starts automatically when the plugin is active. Each monitor runs a shell command for the lifetime of the session and delivers every stdout line to Claude as a notification, so Claude can react to log entries, status changes, or polled events without being asked to start the watch itself."
  - *Implication*: Enables reactive plugin behaviors (e.g., tail an error log, poll a deployment endpoint) without requiring the user to manually start watchers each session. Supports a `when: "on-skill-invoke:<skill-name>"` trigger to start monitors only when a specific skill is invoked. Requires Claude Code v2.1.105+.
  - *Source*: [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md), [Create plugins](https://code.claude.com/docs/en/plugins.md)

#### Plugin CLI: `plugin list` Command

- **New `claude plugin list` subcommand**: Lists installed plugins with their version, source marketplace, and enable status.
  > ```
  > claude plugin list [options]
  > ```
  - *Implication*: Provides a quick audit path for installed plugins, useful for scripting and managed deployments.
  - *Source*: [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md)

### Configuration

#### Setup: `minimumVersion` Setting

- **Pin a minimum update floor with `minimumVersion`**: A new settings key prevents auto-updates and `claude update` from installing any version below the specified value. This guards against accidental downgrades when switching from the `latest` to `stable` release channel.
  > "The `minimumVersion` setting establishes a floor. Background auto-updates and `claude update` refuse to install any version below this value, so moving to the `"stable"` channel does not downgrade you if you are already on a newer `"latest"` build."
  ```json
  {
    "autoUpdatesChannel": "stable",
    "minimumVersion": "2.1.100"
  }
  ```
  - *Implication*: Particularly useful in managed enterprise settings where the key can be deployed org-wide to enforce a minimum version floor that user and project settings cannot override. The `/config` channel-switching UI now prompts whether to stay on the current version or allow downgrade, and sets `minimumVersion` automatically.
  - *Source*: [Advanced setup](https://code.claude.com/docs/en/setup.md)

#### MCP: Automatic Reconnection + OAuth Scope Restriction

- **Automatic reconnection for HTTP/SSE servers**: If an HTTP or SSE MCP server drops mid-session, Claude Code now reconnects automatically with exponential backoff — up to five attempts starting at 1 second.
  > "If an HTTP or SSE server disconnects mid-session, Claude Code automatically reconnects with exponential backoff: up to five attempts, starting at a one-second delay and doubling each time. The server appears as pending in `/mcp` while reconnection is in progress. After five failed attempts the server is marked as failed and you can retry manually from `/mcp`."
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

- **Restrict OAuth scopes for MCP servers**: A new `oauth.scopes` field lets you pin the scopes Claude Code requests during an MCP server's authorization flow, restricting it to a security-approved subset.
  > "Set `oauth.scopes` to pin the scopes Claude Code requests during the authorization flow. This is the supported way to restrict an MCP server to a security-team-approved subset when the upstream authorization server advertises more scopes than you want to grant."
  - *Implication*: Enables least-privilege OAuth configurations for MCP servers in enterprise environments.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

#### Permissions: Read-Only Commands Documented

- **Built-in read-only command set formalized**: The documentation now explicitly lists the Bash commands Claude Code treats as read-only and runs without a permission prompt in every mode: `ls`, `cat`, `head`, `tail`, `grep`, `find`, `wc`, `diff`, `stat`, `du`, `cd`, and read-only forms of `git`.
  > "Claude Code recognizes a built-in set of Bash commands as read-only and runs them without a permission prompt in every mode. These include `ls`, `cat`, `head`, `tail`, `grep`, `find`, `wc`, `diff`, `stat`, `du`, `cd`, and read-only forms of `git`. The set is not configurable; to require a prompt for one of these commands, add an `ask` or `deny` rule for it."
  - *Implication*: Clarifies what `dontAsk` mode allows by default and documents a behavior that was previously undocumented. Unquoted glob patterns on read-only commands are permitted; commands with write-capable flags still prompt.
  - *Source*: [Configure permissions](https://code.claude.com/docs/en/permissions.md)

#### Auto Mode: Conversation Boundaries

- **Stated boundaries are enforced by the auto mode classifier**: A new section documents that boundaries stated in conversation ("don't push", "wait before deploying") are treated as block signals by the auto mode classifier for the remainder of the session.
  > "The classifier treats boundaries you state in the conversation as a block signal... A boundary stays in force until you lift it in a later message. Claude's own judgment that a condition was met does not lift it."
  - *Implication*: Developers should be aware that context compaction may lose stated boundaries — for hard guarantees, use a `deny` rule instead.
  - *Source*: [Choose a permission mode](https://code.claude.com/docs/en/permission-modes.md)

### Monitoring

#### New Raw API Body OTel Events

- **Two new OTel log events for full API payloads**: Enabling `OTEL_LOG_RAW_API_BODIES=1` now emits `claude_code.api_request_body` and `claude_code.api_response_body` events containing the full JSON of each Messages API request and response, truncated at 60 KB.
  > "Emit the full Anthropic Messages API request and response JSON as `api_request_body` / `api_response_body` log events (default: disabled). Bodies include the entire conversation history and are truncated at 60 KB. Enabling this implies consent to everything `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_DETAILS`, and `OTEL_LOG_TOOL_CONTENT` would reveal."
  - *Implication*: Enables deep audit logging of the full conversation payload at the API level. Extended-thinking content is redacted automatically. One event is emitted per attempt, so retries produce separate events. Enterprise teams should ensure their OTel backends are configured to handle the data sensitivity implied by this flag.
  - *Source*: [Monitoring](https://code.claude.com/docs/en/monitoring-usage.md)

### Cloud Web (Claude Code on the Web)

#### Environment Caching

- **Setup scripts are now cached after first run**: Cloud environments snapshot the filesystem after the setup script completes. Subsequent sessions start from the snapshot, skipping the setup script entirely. The cache expires after roughly 7 days or when the setup script or network configuration changes.
  > "The setup script runs the first time you start a session in an environment. After it completes, Anthropic snapshots the filesystem and reuses that snapshot as the starting point for later sessions. New sessions start with your dependencies, tools, and Docker images already on disk, and the setup script step is skipped."
  - *Implication*: Faster session startup for environments with large toolchain installs or Docker image pulls. The comparison table between setup scripts and SessionStart hooks was updated to reflect this: setup scripts now run "when no cached environment is available" rather than "on new sessions only."
  - *Source*: [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

#### New Troubleshooting Section

- **Troubleshooting guidance added for cloud-session-specific issues**: Three new subsections cover: `Session creation failed` (capacity/repo access), `Remote Control session expired or access denied` (short-lived credential expiry via `--teleport`), and `Environment expired` (inactivity reclaim).
  - *Source*: [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

### CLI

#### Typo Detection in Subcommands

- **Mistyped subcommands now suggest the closest match**: When Claude Code doesn't recognize a subcommand, it prints a suggestion and exits without starting a session.
  > "If you mistype a subcommand, Claude Code suggests the closest match and exits without starting a session. For example, `claude udpate` prints `Did you mean claude update?`."
  - *Source*: [CLI reference](https://code.claude.com/docs/en/cli-reference.md)

#### `--bare` Mode Toward Default

- **`--bare` flag flagged as future default for `-p`**: The headless/programmatic mode docs now note that `--bare` (which skips hooks, plugins, MCP servers, auto memory, and CLAUDE.md at startup) will become the default behavior for `claude -p` in a future release.
  > "`--bare` is the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release."
  - *Implication*: Scripts relying on implicit context loading from local config in `-p` mode should audit their usage and add `--bare` explicitly now to avoid behavior changes on upgrade.
  - *Source*: [Run Claude Code programmatically](https://code.claude.com/docs/en/headless.md)

---

## New Pages

- **[errors.md](https://code.claude.com/docs/en/errors.md)** — Complete runtime error reference: 20+ error messages with exact text, cause explanations, and step-by-step recovery. Covers server errors (500, 529), usage limits (session/weekly limits, rate limits, credit balance), authentication (not logged in, invalid key, OAuth token), network errors (SSL, connection refused), and request errors (context too long, PDF limits, model mismatch, tool use/thinking block issues). Also documents automatic retry behavior and the `CLAUDE_CODE_MAX_RETRIES` / `API_TIMEOUT_MS` tuning knobs.

---

## Notable Details

- **Changelog entry v2.1.112** (April 16, 2026): Fixed "claude-opus-4-7 is temporarily unavailable" for auto mode. The new `errors.md` page includes a specific entry for this transient classifier outage pattern under "Auto mode cannot determine the safety of an action."
- **Fullscreen rendering**: The "Adjust wheel scroll speed" section was replaced with "Auto-follow" and "Mouse wheel scrolling" sections, suggesting a redesign of scroll behavior controls.
- **Amazon Bedrock**: The 1M context window setup wizard now offers a 1M context option directly. The docs previously only described manually appending `[1m]` to model IDs.
- **OTel table reorganization** (`monitoring-usage.md`): `OTEL_LOG_TOOL_CONTENT`, `OTEL_LOG_RAW_API_BODIES`, `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE`, and `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` were added to the common configuration table.
- **`authServerMetadataUrl` clarification** (MCP): The `scopes_supported` from the metadata URL's response now overrides what the upstream authorization server advertises — this is a behavioral clarification, not a new feature.
- **Docker in cloud sessions**: Guidance was updated to explicitly recommend `docker compose up` and to note that large images can be pre-pulled in setup scripts (benefiting from environment caching).

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| errors.md | New | +537 | Complete runtime error reference page |
| plugins-reference.md | Modified | +86/-16 | Added Monitors component spec and `plugin list` CLI command |
| monitoring-usage.md | Modified | +64/-21 | Added `api_request_body`/`api_response_body` OTel events and `OTEL_LOG_RAW_API_BODIES` env var |
| claude-code-on-the-web.md | Modified | +51/-13 | Added environment caching section, troubleshooting section, Docker/PostgreSQL clarifications |
| commands.md | Modified | +85/-80 | Reformatting and updates to command reference table |
| tools-reference.md | Modified | +45/-42 | Updates to tool reference content |
| remote-control.md | Modified | +37/-0 | Added mobile push notifications section |
| common-workflows.md | Modified | +26/-16 | Content updates |
| interactive-mode.md | Modified | +41/-31 | Added session recap section |
| mcp.md | Modified | +30/-2 | Added automatic reconnection and restrict OAuth scopes sections |
| setup.md | Modified | +20/-1 | Added "Pin a minimum version" section for `minimumVersion` setting |
| headless.md | Modified | +20/-1 | `--bare` flagged as future default; plugin event documentation expanded |
| plugins.md | Modified | +22/-1 | Added "Add background monitors to your plugin" section |
| permissions.md | Modified | +16/-1 | Added read-only commands documentation |
| permission-modes.md | Modified | +11/-6 | Added "Boundaries you state in conversation" section for auto mode |
| hooks.md | Modified | +11/-7 | Minor updates |
| fullscreen.md | Modified | +20/-19 | Replaced "Adjust wheel scroll speed" with "Auto-follow" and "Mouse wheel scrolling" |
| keybindings.md | Modified | +20/-19 | Updates to keybindings reference |
| desktop.md | Modified | +16/-4 | Updates to Desktop app documentation |
| desktop-scheduled-tasks.md | Modified | +11/-11 | Content updates |
| troubleshooting.md | Modified | +28/-24 | Content updates |
| discover-plugins.md | Modified | +9/-3 | Minor updates |
| env-vars.md | Modified | +9/-4 | Added `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` and other new env vars |
| hooks-guide.md | Modified | +4/-0 | Minor additions |
| changelog.md | Modified | +4/-0 | Added v2.1.112 entry |
| settings.md | Modified | +6/-2 | Updates to settings reference |
| desktop-quickstart.md | Modified | +4/-12 | Simplified quickstart content |
| ultrareview.md | Modified | +8/-8 | Content updates |
| amazon-bedrock.md | Modified | +1/-1 | Bedrock setup wizard now offers 1M context option |
| cli-reference.md | Modified | +2/-0 | Added typo-detection note for mistyped subcommands |
| model-config.md | Modified | +2/-2 | Minor updates |
| google-vertex-ai.md | Modified | +1/-1 | Minor update |
| how-claude-code-works.md | Modified | +1/-1 | Minor update |
| plugin-marketplaces.md | Modified | +1/-1 | Minor update |
| routines.md | Modified | +1/-1 | Minor update |
| skills.md | Modified | +2/-2 | Minor updates |
| sub-agents.md | Modified | +1/-1 | Minor update |
| terminal-config.md | Modified | +2/-2 | Minor updates |
| ultraplan.md | Modified | +1/-0 | Minor addition |
| vs-code.md | Modified | +1/-1 | Minor update |
| web-quickstart.md | Modified | +1/-1 | Minor update |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-17*
