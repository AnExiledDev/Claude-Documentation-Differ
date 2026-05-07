# Claude Code Documentation Changes — 2026-05-07

## Summary

Six documentation pages were updated, with no pages added or removed. The dominant theme is improved cross-referencing between CLI flags, environment variables, and settings — many entries now explicitly document which mechanism overrides another. Two functional corrections also landed: a Bedrock inference profile ID prefix fix and a web session transcript URL construction fix.

## Significant Changes

### CLI Flags

- **`--add-dir` — Persistence pointer added**: The flag description now directs users to `permissions.additionalDirectories` in settings for persisting additional directories across sessions.
  > "To persist these directories across sessions, set `permissions.additionalDirectories` in settings"
  - *Implication*: Users who routinely add the same directories can move them to settings instead of re-passing the flag every invocation.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **`--effort` — Settings override named explicitly**: The description changed from "Session-scoped and does not persist to settings" to naming the specific `effortLevel` setting it overrides.
  > "Overrides the `effortLevel` setting for this session and does not persist"
  - *Implication*: Makes the flag/setting relationship unambiguous — `--effort` shadows `effortLevel` in settings for the current session only.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **`--model` — Override chain documented**: The flag now states that it overrides both the `model` setting and the `ANTHROPIC_MODEL` environment variable.
  > "Overrides the `model` setting and `ANTHROPIC_MODEL`"
  - *Implication*: Clarifies precedence: `--model` flag > `ANTHROPIC_MODEL` env var > `model` setting.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **`--no-session-persistence` — Env var equivalent noted**: The description now cross-references `CLAUDE_CODE_SKIP_PROMPT_HISTORY`, which achieves the same effect in any mode, not just print mode.
  > "The `CLAUDE_CODE_SKIP_PROMPT_HISTORY` environment variable does the same in any mode"
  - *Implication*: Users running interactive sessions who also need to suppress prompt history now have a non-flag option.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **`--teammate-mode` and `--verbose` — Settings override documented**: Both flags now state they override the corresponding `teammateMode` and `viewMode` settings for the current session only.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

### Environment Variables

- **`CLAUDE_CODE_AUTO_CONNECT_IDE` — Settings precedence clarified**: The description now states it takes precedence over the `autoConnectIde` global config setting.
  > "Takes precedence over the `autoConnectIde` global config setting"
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_DISABLE_AUTO_MEMORY` — `=0` override scope expanded**: The "force on" behavior previously said "during the gradual rollout." It now states setting to `0` forces auto memory on even when `--bare` mode or `autoMemoryEnabled: false` would otherwise disable it.
  > "Set to `0` to force auto memory on even when `--bare` mode or `autoMemoryEnabled: false` would otherwise disable it"
  - *Implication*: The gradual-rollout language is gone, indicating auto memory is fully available. The `=0` override now serves a broader, explicitly documented purpose.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY` — Rate-based alternative surfaced**: The description now points to `feedbackSurveyRate` as an alternative to outright disabling surveys.
  > "To set a sample rate instead of disabling outright, use the `feedbackSurveyRate` setting"
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

### Settings

- **`alwaysThinkingEnabled` — Escape hatch noted**: Added a pointer to `CLAUDE_CODE_DISABLE_THINKING` (set via `env`) as the way to force extended thinking off regardless of this setting.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`apiKeyHelper` — Refresh interval cross-referenced**: Added a link to `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` for configuring the credential refresh interval.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`effortLevel`, `model`, `teammateMode`, `viewMode` — Per-session override patterns noted**: Each setting now documents the flag and/or env var that overrides it for a single session, making the settings → flag → env var precedence chain navigable from any entry point.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`otelHeadersHelper` — Refresh interval cross-referenced**: Added a link to `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` for configuring the OpenTelemetry header refresh cadence.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`autoConnectIde` — Env var override noted**: The global config entry for `autoConnectIde` now states that `CLAUDE_CODE_AUTO_CONNECT_IDE` overrides it when set.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **HTTP hook URL allowlist — Hostname case-insensitivity documented**: The `hookAllowedHttpHosts` description now explicitly states hostname matching is case-insensitive and ignores trailing FQDN dots.
  > "Hostname matching is case-insensitive and ignores a trailing FQDN dot, matching DNS semantics."
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### MCP URL Pattern Matching

- **URL allowlist — Hostname case-insensitivity and FQDN dot handling clarified**: A new paragraph was added explaining that hostname matching follows DNS semantics — case-insensitive and treating a trailing dot as equivalent to no trailing dot. Paths remain case-sensitive.
  > "Hostname matching is case-insensitive and ignores a trailing FQDN dot, matching DNS semantics. A pattern like `*://Mcp.Example.com/*` matches `https://mcp.example.com/api`, and `https://mcp.example.com.` is treated the same as `https://mcp.example.com`. Paths remain case-sensitive."
  - *Implication*: MCP URL allowlists don't require duplicate entries for case variants or FQDN-dotted forms of the same host. This matches the same clarification added to HTTP hook URL restrictions in settings.md.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

### Integrations

- **Web session transcript URL construction corrected**: `CLAUDE_CODE_REMOTE_SESSION_ID` uses a `cse_` prefix, but the transcript URL path requires `session_`. The documentation now explains this mismatch and provides the correct shell substitution.
  > "The variable's value uses a `cse_` prefix, while the transcript URL path takes the same ID with a `session_` prefix. Substitute the prefix when building the link."
  ```bash
  echo "https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID/#cse_/session_}"
  ```
  - *Implication*: The previously documented command (`echo "https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID}"`) would produce broken transcript links. PR templates or scripts using the old form should be updated.
  - *Source*: [Claude Code on the Web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

- **Bedrock inference profile ID prefix corrected**: The example `ANTHROPIC_MODEL` value changed from `global.anthropic.claude-sonnet-4-6` to `us.anthropic.claude-sonnet-4-6`.
  ```bash
  # Before
  export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-6'
  # After
  export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-6'
  ```
  - *Implication*: The `global.` prefix is not a valid Bedrock inference profile ID prefix; regional prefixes like `us.` are correct. Bedrock users copying this example should update their configurations.
  - *Source*: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md)

## Notable Details

- The CLI reference table was reformatted with wider column widths. All content changes are semantic, not layout-only.
- The `CLAUDE_CODE_DISABLE_AUTO_MEMORY=0` description dropped the phrase "during the gradual rollout," suggesting auto memory is now fully available and the override is stable long-term behavior.
- Cross-referencing between settings, flags, and env vars was improved in at least 10 entries across `cli-reference.md` and `settings.md`. This appears to be a systematic documentation pass to make each entry self-contained for precedence lookup.
- The same hostname matching clarification (case-insensitive, FQDN-dot-insensitive) was added to both `mcp.md` (MCP URL allowlists) and `settings.md` (HTTP hook URL restrictions) in the same update, indicating a shared implementation.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| cli-reference.md | Modified | +65/-65 | Table reformatting; description updates for `--add-dir`, `--effort`, `--model`, `--no-session-persistence`, `--teammate-mode`, `--verbose` |
| settings.md | Modified | +16/-16 | Cross-references added for `alwaysThinkingEnabled`, `apiKeyHelper`, `autoMemoryEnabled`, `effortLevel`, `feedbackSurveyRate`, `model`, `otelHeadersHelper`, `teammateMode`, `tui`, `viewMode`, `autoConnectIde`; HTTP hook hostname matching note |
| env-vars.md | Modified | +3/-3 | Clarifications for `CLAUDE_CODE_AUTO_CONNECT_IDE`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY`, `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY` |
| mcp.md | Modified | +2/-0 | New paragraph on case-insensitive hostname matching and FQDN dot handling in MCP URL allowlists |
| claude-code-on-the-web.md | Modified | +2/-2 | Corrected transcript URL construction to handle `cse_` → `session_` prefix substitution |
| amazon-bedrock.md | Modified | +1/-1 | Fixed inference profile ID example from `global.` to `us.` prefix |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-07*
