# Claude Code Documentation Changes — 2026-03-19

## Summary

Version 2.1.79 was released on March 18, 2026, adding a new `--console` auth flag, a `StopFailure` hook event for API error handling, and a custom model injection mechanism for LLM gateway deployments. Several documentation accuracy fixes also landed, including a breaking clarification to sandbox path prefix semantics and expanded hook matcher coverage.

## Significant Changes

### Features

- **`claude auth login --console` flag**: New flag for authenticating with Anthropic Console (API billing) instead of a Claude subscription.
  > `Sign in to your Anthropic account. Use --email to pre-fill your email address, --sso to force SSO authentication, and --console to sign in with Anthropic Console for API usage billing instead of a Claude subscription`
  - *Implication*: Developers using pay-as-you-go API billing via the Console can now authenticate directly without a Claude subscription. The example in the reference was also updated from `--email user@example.com --sso` to `--console`.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **VSCode `/remote-control` command menu entry**: The VS Code command menu (`/`) now surfaces a `/remote-control` option for bridging to claude.ai/code to continue a session from a browser or phone.
  > `Options include attaching files, switching models, toggling extended thinking, viewing plan usage (/usage), and starting a Remote Control session (/remote-control).`
  - *Implication*: Remote Control is now surfaced in the primary command menu, not just as a separate CLI command.
  - *Source*: [VS Code](https://code.claude.com/docs/en/vs-code.md)

- **VSCode AI-generated session titles**: New sessions in VS Code now automatically receive AI-generated titles based on the first message.
  > `New sessions receive AI-generated titles based on your first message.`
  - *Implication*: Browsing conversation history in the VS Code panel requires less manual renaming.
  - *Source*: [VS Code](https://code.claude.com/docs/en/vs-code.md)

- **`CLAUDE_CODE_PLUGIN_SEED_DIR` multi-directory support**: The env var now accepts multiple seed directories separated by `:` on Unix or `;` on Windows, rather than a single path.
  > `Path to one or more read-only plugin seed directories, separated by : on Unix or ; on Windows.`
  > `To layer multiple seed directories, separate paths with : on Unix or ; on Windows. Claude Code searches each directory in order, and the first seed that contains a given marketplace or plugin cache wins.`
  - *Implication*: Container images can now combine multiple pre-seeded plugin directories (e.g., a base company image plus a project-specific layer) without merging them manually.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md), [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

- **"Show turn duration" toggle in `/config`**: The `showTurnDuration` setting is now accessible from the `/config` menu rather than requiring direct edits to `~/.claude.json`.
  > `Show turn duration messages after responses, e.g. "Cooked for 1m 6s". Default: true. Appears in /config as Show turn duration`
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Hooks

- **New `StopFailure` hook event**: Fires when a turn ends due to an API error (rate limit, auth failure, billing error, etc.) instead of `Stop`. Output and exit code are ignored — this event is for logging and alerting only.
  > `Runs instead of Stop when the turn ends due to an API error. Output and exit code are ignored. Use this to log failures, send alerts, or take recovery actions when Claude cannot complete a response due to rate limits, authentication problems, or other API errors.`

  Input schema includes `error` (the matcher field), optional `error_details`, and optional `last_assistant_message`:
  ```json
  {
    "session_id": "abc123",
    "hook_event_name": "StopFailure",
    "error": "rate_limit",
    "error_details": "429 Too Many Requests",
    "last_assistant_message": "API Error: Rate limit reached"
  }
  ```
  Matcher values: `rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown`.
  - *Implication*: Hooks that previously used `Stop` and tried to detect errors will need to migrate to `StopFailure`. The `Stop` event no longer fires on API errors.
  - *Source*: [Hooks Reference](https://code.claude.com/docs/en/hooks.md), [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)

- **`InstructionsLoaded` now supports matchers**: Previously documented as not supporting matchers; it now matches on `load_reason`.
  > `The matcher runs against load_reason. For example, use "matcher": "session_start" to fire only for files loaded at session start, or "matcher": "path_glob_match|nested_traversal" to fire only for lazy loads.`
  Matcher values: `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`.
  - *Implication*: Hooks that fire on `InstructionsLoaded` can now be scoped to specific load reasons rather than firing on every occurrence. `InstructionsLoaded` has been removed from the "no matcher support" row in both matcher tables.
  - *Source*: [Hooks Reference](https://code.claude.com/docs/en/hooks.md)

- **`Elicitation` and `ElicitationResult` added to matcher table**: Both events now appear in the hook matcher reference table with their matching field (MCP server name).
  - *Implication*: Documentation catch-up — these events were previously missing from the matcher reference; the filtering behavior was already available.
  - *Source*: [Hooks Reference](https://code.claude.com/docs/en/hooks.md), [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)

- **`permission_mode` field clarification**: The common input fields table now notes that not all hook events receive `permission_mode`. Several event JSON examples (`SessionStart`, `InstructionsLoaded`, `Notification`, `SubagentStart`, `ConfigChange`, `PreCompact`, `PostCompact`, `SessionEnd`) had this field removed to reflect actual behavior.
  > `Not all events receive this field: see each event's JSON example below to check`
  - *Implication*: Hook scripts that read `permission_mode` on events where it is absent will receive `undefined`/null rather than a string. Test hook scripts that depend on this field against the specific events they handle.
  - *Source*: [Hooks Reference](https://code.claude.com/docs/en/hooks.md)

### Configuration

- **Custom model option for LLM gateways**: Three new environment variables allow injecting a custom entry into the `/model` picker without replacing built-in aliases.

  | Variable | Purpose |
  |---|---|
  | `ANTHROPIC_CUSTOM_MODEL_OPTION` | Model ID to add (validation is skipped) |
  | `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` | Display name (defaults to model ID) |
  | `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` | Display description (defaults to `Custom model (<model-id>)`) |

  > `Use ANTHROPIC_CUSTOM_MODEL_OPTION to add a single custom entry to the /model picker without replacing the built-in aliases. This is useful for LLM gateway deployments or testing model IDs that Claude Code does not list by default.`
  - *Implication*: Teams routing through an internal LLM gateway can now make their gateway endpoint selectable in the model picker with a friendly name, rather than requiring users to type the model ID manually or use `ANTHROPIC_MODEL`.
  - *Source*: [Model Configuration](https://code.claude.com/docs/en/model-config.md), [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **Sandbox path prefix semantics corrected**: The `/` prefix now correctly means an absolute path (not project-relative as previously documented). Project-relative paths should use `./`.
  > `/tmp/build` stays `/tmp/build` (absolute path from filesystem root)
  > `The older //path prefix for absolute paths still works. If you previously used single-slash /path expecting project-relative resolution, switch to ./path.`

  Updated prefix table:

  | Prefix | Meaning |
  |---|---|
  | `/` | Absolute path from filesystem root |
  | `~/` | Relative to home directory |
  | `./` or no prefix | Relative to project root (project settings) or `~/.claude` (user settings) |

  - *Implication*: **Potentially breaking for users who relied on `/path` meaning project-relative in sandbox config.** Example values in docs updated from `//tmp/build` to `/tmp/build` and `//etc` to `/etc`. Users with existing `sandbox.filesystem.allowWrite` entries using `/path` syntax expecting project-relative resolution should migrate to `./path`.
  - *Source*: [Sandboxing](https://code.claude.com/docs/en/sandboxing.md), [Settings](https://code.claude.com/docs/en/settings.md)

- **Subagent persistent memory default scope changed**: The recommended default scope for subagent persistent memory changed from `user` to `project`.
  > `project is the recommended default scope. It makes subagent knowledge shareable via version control. Use user when the subagent's knowledge is broadly applicable across projects, or local when the knowledge should not be checked into version control.`
  - *Implication*: New subagents following the documentation guidance will store memory in `.claude/` (version-controllable) by default. Existing subagents configured with `user` scope are unaffected.
  - *Source*: [Subagents](https://code.claude.com/docs/en/sub-agents.md)

### Plugins

- **Plugin hooks reference updated to full event list**: The plugins reference page replaced its informal bullet list of hook events with a comprehensive table matching the hooks reference, adding `StopFailure`, `InstructionsLoaded`, `ConfigChange`, `WorktreeCreate`, `WorktreeRemove`, `Elicitation`, `ElicitationResult`, and `SessionEnd`.
  - *Implication*: Plugin authors can now use any hook event documented in the hooks reference; the prior list was incomplete.
  - *Source*: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

- **`http` hook type added to plugins reference**: The plugin hook types listing now includes `http` alongside `command`, `prompt`, and `agent`.
  > `http: send the event JSON as a POST request to a URL`
  - *Source*: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

## Notable Details

- **Non-streaming API fallback timeout (2.1.79)**: A 2-minute per-attempt timeout was added to the non-streaming API fallback, preventing sessions from hanging indefinitely. This is a silent reliability fix with no config surface.
- **Startup memory usage reduced ~18MB** across all scenarios in 2.1.79.
- **`SessionEnd` hooks fix**: 2.1.79 fixed `SessionEnd` hooks not firing when using interactive `/resume` to switch sessions — hooks relying on session-end cleanup should now be reliable across session switches.
- **`claude -p` subprocess hang fix**: 2.1.79 fixed `claude -p` hanging when spawned as a subprocess without explicit stdin (e.g., Python `subprocess.run`). Ctrl+C in `-p` mode was also fixed.
- **Enterprise 429 retry fix**: Enterprise users could not retry on rate limit errors; fixed in 2.1.79.
- **Hooks lifecycle diagram updated**: The `alt` text on the lifecycle SVG now reflects the updated flow including `StopFailure` as an alternative to `Stop`, and `TeammateIdle` appearing after `Stop`/`StopFailure`.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| hooks.md | Modified | +69/-41 | Added `StopFailure` event section and input schema; updated matcher table with `StopFailure`, `InstructionsLoaded`, `Elicitation`, `ElicitationResult`; removed `permission_mode` from several event JSON examples |
| plugins-reference.md | Modified | +31/-21 | Replaced bullet list of hook events with comprehensive table; added `http` hook type |
| cli-reference.md | Modified | +16/-16 | Added `--console` flag to `claude auth login` description and updated example |
| hooks-guide.md | Modified | +17/-12 | Added `StopFailure` to event table; expanded matcher table with new events; clarified `Stop` vs `StopFailure` distinction |
| model-config.md | Modified | +16/-0 | New section: "Add a custom model option" documenting `ANTHROPIC_CUSTOM_MODEL_OPTION` env vars |
| changelog.md | Modified | +21/-0 | Added version 2.1.79 release notes |
| settings.md | Modified | +12/-11 | Corrected sandbox path prefix table; updated examples from `//` to `/`; noted `showTurnDuration` accessible from `/config` |
| sandboxing.md | Modified | +9/-8 | Corrected path prefix table and added migration note for `/` vs `./` semantics |
| env-vars.md | Modified | +4/-1 | Added three `ANTHROPIC_CUSTOM_MODEL_OPTION*` vars; updated `CLAUDE_CODE_PLUGIN_SEED_DIR` to reflect multi-directory support |
| plugin-marketplaces.md | Modified | +3/-1 | Added note about layering multiple seed directories |
| overview.md | Modified | +5/-5 | Whitespace/formatting fix in code block theme attributes |
| vs-code.md | Modified | +2/-2 | Added `/remote-control` to command menu description; noted AI-generated session titles |
| sub-agents.md | Modified | +1/-1 | Changed recommended memory scope default from `user` to `project` |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-19*
