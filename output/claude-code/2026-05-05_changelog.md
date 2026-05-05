# Claude Code Documentation Changes — 2026-05-05

## Summary

22 pages were modified across this update (200 additions, 87 deletions). The most substantive change is a new security audit section in `monitoring-usage.md` documenting how to route Claude Code events to a SIEM via OTLP, including per-user identity attribution and MCP activity auditing. Several other operationally significant changes landed alongside it: a new `disableRemoteControl` managed setting (v2.1.128+), a new `ShareOnboardingGuide` tool, channels support expanded to Console API key auth, telemetry provider rebranded from Statsig to Anthropic, and scheduled-task jitter increased to 30 minutes.

## Significant Changes

### Security & Monitoring

- **New audit security events section**: `monitoring-usage.md` gained a substantial new section covering how to use OpenTelemetry events as the audit data source for Claude Code activity. It documents user identity attribution in events, auditing MCP tool calls with `OTEL_LOG_TOOL_DETAILS=1`, a signal-to-event lookup table for building SIEM detection rules, and a complete managed-settings example for forwarding logs to a SIEM.
  > OpenTelemetry events are the audit data source for Claude Code activity. Every event carries identity attributes that tie tool calls, MCP activity, and permission decisions back to the user who triggered them, and the OTLP logs exporter can deliver these events to any Security Information and Event Management (SIEM) platform with an OTLP receiver.
  - *Implication*: Security teams can route structured per-user audit logs (Bash commands, MCP calls, permission decisions, auth events) directly to their SIEM by setting `OTEL_LOG_TOOL_DETAILS=1` and pointing `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` at the SIEM's OTLP receiver—no custom proxy needed.
  - *Source*: [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **mTLS authentication clarified by OTLP protocol**: The shared `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY` and `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE` variables were removed from the common configuration table and replaced with a new dedicated section. mTLS configuration is now protocol-dependent: HTTP transports (`http/protobuf`, `http/json`) use `CLAUDE_CODE_CLIENT_CERT` / `CLAUDE_CODE_CLIENT_KEY`; gRPC uses the standard `OTEL_EXPORTER_OTLP_CLIENT_KEY` / `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE` variables.
  > How you configure client certificates for the OTLP exporter depends on the OTLP protocol in use for that signal… The same configuration applies to metrics, logs, and traces.
  - *Implication*: HTTP-based OTLP deployments using mTLS must switch to the `CLAUDE_CODE_CLIENT_*` variables. Existing gRPC deployments that set the per-signal metrics mTLS vars continue to work unchanged.
  - *Source*: [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **Dynamic OTLP headers limited to HTTP protocols**: The documentation now states explicitly that the dynamic headers helper (`OTEL_HEADERS_HELPER`) only applies to `http/protobuf` and `http/json`. The gRPC exporter uses only the static `OTEL_EXPORTER_OTLP_HEADERS` value.
  - *Implication*: Teams using gRPC with rotating credentials need to handle credential rotation outside Claude Code or switch to an HTTP transport.
  - *Source*: [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **`OTEL_*` vars not propagated to subprocesses**: A new note clarifies that Claude Code does not pass `OTEL_*` environment variables to the processes it spawns (Bash tool, hooks, MCP servers, language servers).
  > An OpenTelemetry-instrumented application that you run through the Bash tool does not inherit Claude Code's exporter endpoint or headers, so set those variables directly in the command if that application needs to export its own telemetry.
  - *Source*: [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage.md)

### New Settings & Controls

- **`disableRemoteControl` managed setting (v2.1.128+)**: A new setting that blocks `claude remote-control`, the `--remote-control` flag, auto-start, and the in-session toggle. Designed for per-device MDM enforcement via managed settings, independent of the org-wide admin console toggle.
  > Disable Remote Control: blocks `claude remote-control`, the `--remote-control` flag, auto-start, and the in-session toggle. Typically placed in managed settings for per-device MDM enforcement, but works from any scope. Requires Claude Code v2.1.128 or later.
  - *Implication*: Admins can now enforce Remote Control disablement at the device level (e.g., via MDM) rather than only at the organization level.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **Plugin settings precedence clarified**: A new note explains that project settings (`.claude/settings.json`) take precedence over user settings (`~/.claude/settings.json`). Setting a plugin to `false` in user settings does not disable a plugin enabled by the project. The correct per-machine override is `.claude/settings.local.json`.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **Windows path notation added**: The settings documentation now notes that `~/.claude` on Windows resolves to `%USERPROFILE%\.claude`.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Tools

- **New `ShareOnboardingGuide` tool**: Uploads `ONBOARDING.md` and returns a share link that teammates can open directly in Claude Code. Called automatically from `/team-onboarding` after the guide is written. Available to claude.ai Pro, Max, Team, and Enterprise subscribers; requires permission.
  > Uploads `ONBOARDING.md` and returns a share link teammates can open in Claude Code. Called from `/team-onboarding` after the guide is written. Available to claude.ai subscribers on Pro, Max, Team, and Enterprise plans.
  - *Implication*: `/team-onboarding` now produces a shareable link (not just a markdown document) for users on supported plans. Console API key users do not receive a share link.
  - *Source*: [Tools Reference](https://code.claude.com/docs/en/tools-reference.md)

### Channels

- **Channels now explicitly support Console API key auth**: Previously documented as requiring claude.ai login only, channels now work with Anthropic Console API key authentication. Bedrock, Vertex AI, and Microsoft Foundry remain unsupported.
  > They require Anthropic authentication through claude.ai or a Console API key, and are not available on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry.
  - *Source*: [Channels](https://code.claude.com/docs/en/channels.md)

- **`channelsEnabled` default is now plan-dependent**: On claude.ai Team and Enterprise plans, channels remain blocked by default until an admin enables them. On Anthropic Console with API key authentication, channels are **permitted by default** unless the organization deploys managed settings that explicitly block them.
  > **claude.ai Team and Enterprise**: channels are blocked until an admin enables them. **Anthropic Console with API key authentication**: channels are permitted by default. You only need this setting if your organization deploys managed settings.
  - *Implication*: Console API key users no longer need an admin to enable channels. The org-wide admin toggle is only meaningful for claude.ai Team/Enterprise or Console orgs with managed settings deployed.
  - *Source*: [Channels](https://code.claude.com/docs/en/channels.md), [Permissions](https://code.claude.com/docs/en/permissions.md)

### Headless / Non-interactive Mode

- **10 MB stdin cap in headless mode (v2.1.128)**: Piped stdin is capped at 10 MB as of v2.1.128. Exceeding the limit causes Claude Code to exit with a clear error and a non-zero status.
  > As of Claude Code v2.1.128, piped stdin is capped at 10MB. If you exceed the cap, Claude Code exits with a clear error and a non-zero status. To work with larger inputs, write the content to a file and reference the file path in your prompt instead of piping it.
  - *Implication*: CI pipelines that pipe large build logs or file contents via stdin must switch to file-path references for inputs over 10 MB.
  - *Source*: [Headless](https://code.claude.com/docs/en/headless.md)

### MCP

- **`/mcp` panel shows tool counts and flags empty servers**: The `/mcp` panel now shows the tool count next to each connected server and flags servers that advertise the tools capability but expose no tools.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

- **Server name `workspace` is reserved**: If `.mcp.json` defines a server named `workspace`, Claude Code skips it at load time and shows a warning to rename it.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

- **`alwaysLoad: true` blocks startup even with `MCP_CONNECTION_NONBLOCKING=1`**: Setting `alwaysLoad: true` causes Claude Code to wait for the server to connect at startup (up to the 5-second timeout), regardless of whether `MCP_CONNECTION_NONBLOCKING` is set.
  > Setting `alwaysLoad: true` also blocks startup until the server connects, capped at the standard 5-second connect timeout. This applies even when `MCP_CONNECTION_NONBLOCKING=1` is set, since the tools must be present when the first prompt is built. Other servers still connect in the background when nonblocking is enabled.
  - *Implication*: `MCP_CONNECTION_NONBLOCKING` does not bypass `alwaysLoad` servers. Scripts relying on fast non-blocking startup must avoid `alwaysLoad` on servers not needed at prompt construction time.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

### Hooks

- **`PostToolUse` `decision: "block"` behavior clarified**: The documentation now states that `decision: "block"` adds the `reason` *alongside* the tool result—Claude still sees the original tool output. To replace the output, `updatedToolOutput` must be set separately.
  > `"block"` adds the `reason` next to the tool result. Claude still sees the original output; to replace it, use `updatedToolOutput`.
  - *Implication*: Hooks that set `decision: "block"` to suppress tool output are not actually suppressing it. Authors who need to fully replace or hide output must explicitly set `updatedToolOutput`.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

### Scheduled Tasks

- **Jitter for recurring tasks increased to up to 30 minutes**: The previous jitter cap (10% of period, max 15 minutes) was replaced with up to 30 minutes of jitter for recurring tasks (or up to half the interval for tasks running more frequently than hourly).
  > Recurring tasks fire up to 30 minutes after the scheduled time (or up to half the interval, for tasks that run more often than hourly). An hourly job scheduled for `:00` may fire anywhere up to `:30`.
  - *Implication*: Pipelines requiring sub-30-minute precision for hourly tasks may see wider timing variance. Using a non-`:00`/`:30` minute (e.g., `3 9 * * *`) avoids the one-shot jitter.
  - *Source*: [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks.md)

### CLI

- **`--plugin-dir` now accepts `.zip` archives**: The flag can now load a plugin from a `.zip` archive in addition to an unpacked directory.
  > Load a plugin from a directory or `.zip` archive for this session only. Each flag takes one path. Repeat the flag for multiple plugins: `--plugin-dir A --plugin-dir B.zip`
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

---

## Notable Details

- **Telemetry provider renamed from Statsig to Anthropic**: All references to "Statsig" for operational metrics have been replaced with "Anthropic" in `data-usage.md` and `env-vars.md`. The data flow diagram was also updated. The opt-out mechanism (`DISABLE_TELEMETRY=1`) is unchanged. This indicates metrics collection has migrated to Anthropic's own infrastructure.

- **`/color` with no argument now picks a random color**: Running `/color` without arguments now selects a random color from the available palette, rather than requiring an explicit color name.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

- **`/team-onboarding` share link for subscribers**: In addition to producing a markdown guide, `/team-onboarding` now returns a share link for claude.ai Pro, Max, Team, and Enterprise subscribers.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

- **Status line script now fires after `/compact`**: The statusline update script now runs after `/compact` finishes (in addition to after assistant messages and permission mode/vim mode changes). The `context_window.current_usage` field becomes `null` again immediately after `/compact` until the next API call repopulates it—scripts should handle this null case.
  - *Source*: [Status Line](https://code.claude.com/docs/en/statusline.md)

- **Plugin `CLAUDE.md` is not loaded as context**: A new warning clarifies that a `CLAUDE.md` file at the plugin root is not loaded as project context. Plugins should deliver instructions via skills, agents, or hooks.
  - *Source*: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

- **`${CLAUDE_PLUGIN_ROOT}` cleanup delay and mid-session update behavior**: The previous version's plugin directory is retained for approximately seven days after an update before cleanup. Mid-session plugin updates leave hooks, MCP servers, and LSP servers on the old path until `/reload-plugins` is run; monitors require a full session restart.
  - *Source*: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

- **`strictKnownMarketplaces` exact matching does not normalize URLs**: Trailing slashes, `.git` suffixes, and `ssh://` vs `https://` forms are treated as distinct values. Organizations whose marketplace can be reached by multiple URL forms should use a `hostPattern` entry.
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

- **Authentication credential storage expanded per platform**: The credential storage description was expanded into per-platform bullets, now explicitly documenting Windows (`%USERPROFILE%\.claude\.credentials.json` with user-profile ACL), Linux (`~/.claude/.credentials.json` with mode `0600`), macOS (Keychain), and the `CLAUDE_CONFIG_DIR` override.
  - *Source*: [Authentication](https://code.claude.com/docs/en/authentication.md)

- **Remote Control "disabled by org policy" now has a fourth cause**: The troubleshooting entry was updated to add the `disableRemoteControl` managed setting as a fourth distinct cause, separate from the org-wide admin console toggle.
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

- **Third tmux caveat in fullscreen mode**: A new caveat documents that tmux does not support synchronized output, causing more visible flicker during redraws (especially over SSH). Mitigation: run Claude Code in its own terminal tab outside tmux.
  - *Source*: [Fullscreen](https://code.claude.com/docs/en/fullscreen.md)

- **Skill body conciseness guidance**: New text advises keeping skill body content concise because loaded skill content stays in context across turns, incurring a recurring token cost per turn.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

- **Voice dictation: new "failing repeatedly and paused" error documented**: A new troubleshooting entry covers the state where voice dictation halts after several consecutive startup failures—typically on headless servers or remote shells without audio passthrough.
  - *Source*: [Voice Dictation](https://code.claude.com/docs/en/voice-dictation.md)

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| monitoring-usage.md | Modified | +76/-4 | New audit security events section; mTLS protocol split; OTEL subprocess isolation note; dynamic headers clarification |
| tools-reference.md | Modified | +38/-37 | Added `ShareOnboardingGuide` tool |
| channels.md | Modified | +15/-10 | Console API key auth support; plan-dependent `channelsEnabled` defaults |
| settings.md | Modified | +10/-1 | New `disableRemoteControl` setting; updated `channelsEnabled`; plugin precedence note; Windows path note |
| headless.md | Modified | +8/-4 | 10 MB stdin cap (v2.1.128); expanded `plugin_errors` to include `--plugin-dir` failures |
| hooks.md | Modified | +7/-7 | Clarified `decision: "block"` in PostToolUse doesn't suppress original output |
| mcp.md | Modified | +6/-0 | `/mcp` tool count display; reserved `workspace` name; `alwaysLoad` blocks startup with nonblocking env |
| plugins-reference.md | Modified | +5/-1 | `CLAUDE_PLUGIN_ROOT` 7-day retention; mid-session update behavior; `CLAUDE.md` not loaded as context |
| authentication.md | Modified | +5/-1 | Per-platform credential storage expanded; Windows path explicit |
| remote-control.md | Modified | +4/-3 | Fourth cause for org policy error; mobile app navigation hint |
| data-usage.md | Modified | +4/-4 | Statsig → Anthropic for metrics; data flow diagram URL updated |
| fullscreen.md | Modified | +3/-1 | Third tmux caveat: synchronized output not supported, causes flicker |
| statusline.md | Modified | +3/-3 | Script fires after `/compact`; `current_usage` is null after `/compact` |
| channels-reference.md | Modified | +2/-2 | Removed claude.ai-only login requirement; "org admin" wording |
| commands.md | Modified | +2/-2 | `/color` no-arg picks random color; `/team-onboarding` generates share link for subscribers |
| env-vars.md | Modified | +2/-2 | `DISABLE_TELEMETRY` Statsig reference removed; `MCP_CONNECTION_NONBLOCKING` `alwaysLoad` caveat added |
| permissions.md | Modified | +2/-2 | Updated `channelsEnabled` description; per-device `disableRemoteControl` note |
| plugin-marketplaces.md | Modified | +2/-0 | URL normalization caveat for `strictKnownMarketplaces` |
| skills.md | Modified | +2/-0 | Conciseness guidance for skill body content |
| scheduled-tasks.md | Modified | +2/-2 | Jitter increased to up to 30 minutes for recurring tasks |
| cli-reference.md | Modified | +1/-1 | `--plugin-dir` accepts `.zip` archives |
| voice-dictation.md | Modified | +1/-0 | New troubleshooting entry for repeated voice input failures |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-05*
