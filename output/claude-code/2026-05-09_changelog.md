# Claude Code Documentation Changes — 2026-05-09

## Summary

13 documentation pages were modified (+97/−21 lines total). The most significant additions are `autoMode.hard_deny` — a new unconditional classifier block tier that cannot be overridden by user intent — and the new `policyHelper` setting, which lets admins run an executable at startup to generate managed settings dynamically. Several smaller changes add a `/radio` command, new env vars, MCP transport alias support, and troubleshooting entries for org-policy-disabled routines.

## Significant Changes

### Features

- **New `/radio` command**: Opens Claude FM lo-fi radio in a browser; prints the stream URL when no browser is available.
  > "Open Claude FM lo-fi radio in your browser. Prints the stream URL when no browser is available. Not available on Bedrock, Vertex, or Foundry"
  - *Implication*: Available on Claude.ai subscription plans only; not supported on API, Bedrock, Vertex, or Foundry deployments.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

- **`/clear` accepts an optional `[name]` argument**: Pass a name to label the previous conversation in the `/resume` picker.
  > "`/clear [name]` — Pass a name to label the previous conversation in the `/resume` picker."
  - *Implication*: Makes it easier to identify past sessions when switching between multiple workstreams.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

- **`/context` gains `[all]` flag**: In fullscreen mode, the per-item breakdown is now collapsed by default to keep the grid visible; pass `all` to expand it.
  > "In fullscreen mode the per-item breakdown is collapsed to keep the grid visible. Pass `all` to expand it"
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

- **`CLAUDE_CODE_NATIVE_CURSOR` env var**: Set to `1` to use the terminal's native cursor at the input caret instead of Claude Code's drawn block. Respects the terminal's blink, shape, and focus settings.
  - *Implication*: Useful for terminals where the custom cursor block conflicts with user preferences or accessibility tooling.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **`DO_NOT_TRACK` env var now honored**: Setting `DO_NOT_TRACK=1` opts out of telemetry, equivalent to `DISABLE_TELEMETRY`. Aligns with the [standard cross-tool convention](https://consoledonottrack.com/).
  - *Implication*: Environments that already set `DO_NOT_TRACK` globally (common in developer tooling setups) will now automatically suppress Claude Code telemetry without a Claude-specific variable.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

### Configuration

- **`autoMode.hard_deny` — new unconditional classifier tier**: A fourth tier has been added to the auto mode classifier. `hard_deny` rules block regardless of user intent or `allow` entries.

  The new four-tier precedence:
  > "* `hard_deny` rules block unconditionally. User intent and `allow` exceptions do not apply.
  > * `soft_deny` rules block next. User intent and `allow` exceptions can override these.
  > * `allow` rules then override matching `soft_deny` rules as exceptions.
  > * Explicit user intent overrides the remaining soft blocks"

  The `claude auto-mode defaults`, `claude auto-mode config`, and `claude auto-mode critique` commands are all updated to include `hard_deny`. Developers can extend `hard_deny` with personal entries but cannot remove entries managed settings provide.

  > "A `hard_deny` array without `\"$defaults\"` discards the built-in data exfiltration and safety-check bypass rules."

  - *Implication*: Admins can now enforce rules no user phrasing can bypass — e.g., prohibiting sending repo contents to third-party APIs. Omitting `"$defaults"` from `hard_deny` silently removes built-in safety boundaries; review carefully.
  - *Source*: [Configure auto mode](https://code.claude.com/docs/en/auto-mode-config.md), [Settings](https://code.claude.com/docs/en/settings.md)

- **New `policyHelper` setting** (requires v2.1.136+): An admin-deployed executable that generates managed settings at startup from dynamic sources (device posture, identity, remote service).

  Accepted keys:

  | Key | Type | Description |
  |---|---|---|
  | `path` | string | Absolute path to the helper executable |
  | `timeoutMs` | number | Wait limit before treating the run as failed |
  | `refreshIntervalMs` | number | Re-run interval; `0` disables refresh, minimum `60000` |

  The helper writes a JSON envelope to stdout:
  ```json
  {
    "managedSettings": {
      "permissions": { "deny": ["Read(//etc/secrets/**)"] }
    },
    "claudeMd": "# Organization context\n...",
    "appendSystemPrompt": "Always cite the internal style guide."
  }
  ```

  > "Claude Code ignores `policyHelper` when it appears in any other scope, including user settings, project settings, the HKCU registry hive, and server-managed settings."
  > "When the helper exits non-zero at startup, Claude Code prints the error and refuses to start, so a helper that needs outage resilience should serve from its own cache and exit `0`."

  - *Implication*: Enterprise admins can serve context-aware policies without static MDM profiles. A helper that fails at startup blocks all Claude Code usage — build in a cache/fallback and exit `0` for availability.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`plugins.skills` path is now additive, not replacing**: Previously documented as replacing the default `skills/` directory; corrected to state it loads alongside the default.
  > "`skills` — Custom skill directories containing `<name>/SKILL.md` (in addition to default `skills/`)"

  The fields `commands`, `agents`, `outputStyles`, `experimental.themes`, and `experimental.monitors` still replace the default when specified.

  - *Implication*: Plugins listing custom `skills` paths will have both directories scanned. This is a documentation correction of existing behavior.
  - *Source*: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

- **Server-managed settings: `policyHelper` and `wslInheritsWindowsSettings` are OS-level only**: These settings are not honored when delivered via server-managed settings.
  > "Settings restricted to OS-level policy sources, such as `policyHelper` and `wslInheritsWindowsSettings`, are not honored. Deploy them through MDM or a system `managed-settings.json` file instead."
  - *Source*: [Server-managed Settings](https://code.claude.com/docs/en/server-managed-settings.md)

### Integrations

- **MCP: `streamable-http` accepted as alias for `http` transport**: When configuring MCP servers via JSON in `.mcp.json`, `~/.claude.json`, or `claude mcp add-json`, the `type` field now accepts `streamable-http` as a synonym for `http`.
  > "The MCP specification uses the name `streamable-http` for this transport, so configurations copied from server documentation work without modification."
  - *Implication*: Config blocks copied directly from MCP server documentation no longer require renaming the transport field.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

- **`--worktree` exception to non-interactive trust bypass**: The `-p` flag disables trust verification in non-interactive runs, but `--worktree` still requires trust to have been accepted for the directory.
  > "Trust verification is disabled when running non-interactively with the `-p` flag. The exception is `--worktree`, which still requires that trust has been accepted for the directory"
  - *Implication*: Automated pipelines using `--worktree` must have interactively accepted trust for the directory at least once before CI runs can proceed.
  - *Source*: [Security](https://code.claude.com/docs/en/security.md)

### Error Handling & Troubleshooting

- **New error: "Routines are disabled by your organization's policy"**: Documented in both `errors.md` and `routines.md`. Appears when a Team or Enterprise admin has disabled the Routines toggle at the org level.
  > "This is a server-side setting, so it cannot be overridden from local settings, environment variables, or CLI flags."

  Resolution: Ask admin to enable the **Routines** toggle at `claude.ai/admin-settings/claude-code`, or use [scheduled tasks](/en/scheduled-tasks) for one-off work that doesn't require org routines.
  - *Source*: [Errors](https://code.claude.com/docs/en/errors.md), [Routines](https://code.claude.com/docs/en/routines.md)

### Permissions

- **Deny rule anchor semantics clarified**: New table explaining exactly which paths a deny rule covers based on its form:

  | Deny rule | Blocks | Does not block |
  |---|---|---|
  | `Read(.env)` or `Read(**/.env)` | any `.env` at or under the current directory | `.env` in a parent directory or another project |
  | `Read(//**/.env)` | any `.env` anywhere on the filesystem | nothing; the rule is anchored at the filesystem root |

  > "Bare filenames follow gitignore semantics and match at any depth, so `Read(.env)` and `Read(**/.env)` are equivalent"
  - *Implication*: Deny rules for sensitive files like `.env` do not protect copies in parent directories. Filesystem-wide blocks require the `//` root anchor.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

## Notable Details

- **Auto-suggestion Tab behavior wording corrected**: The prior wording said "press Tab or Right arrow to accept the suggestion, or press Enter to accept and submit." Updated to: "press Tab or Right arrow to place the suggestion in the prompt input, then Enter to submit." This is a clarification of existing behavior, not a behavior change.
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

- **Version 2.1.138 released**: Internal fixes only; no user-facing changes listed. The prior entry, 2.1.137 (same day), fixed VS Code extension activation on Windows.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`auto-mode-config` danger note updated**: Now distinguishes what's lost per array: dropping `soft_deny` defaults removes force-push and `curl | bash` blocks; dropping `hard_deny` defaults removes data exfiltration and safety-check bypass rules. Each section remains independently evaluated.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| settings.md | Modified | +28/−1 | New `policyHelper` setting and full documentation section; `autoMode` updated to include `hard_deny` |
| auto-mode-config.md | Modified | +16/−11 | `hard_deny` fourth classifier tier; danger note and CLI references updated |
| errors.md | Modified | +16/−0 | New error section for org-policy-disabled routines |
| plugins-reference.md | Modified | +8/−3 | `skills` corrected from "replaces" to "adds to" default; path behavior rules rewritten |
| permissions.md | Modified | +7/−0 | New table clarifying deny rule anchor semantics |
| commands.md | Modified | +3/−2 | `/clear [name]`, `/context [all]`, and new `/radio` command |
| routines.md | Modified | +6/−0 | New Troubleshooting section for org-policy-disabled routines |
| server-managed-settings.md | Modified | +3/−2 | OS-level-only settings limitation; `hard_deny` reference updated |
| env-vars.md | Modified | +2/−0 | New `CLAUDE_CODE_NATIVE_CURSOR` and `DO_NOT_TRACK` variables |
| mcp.md | Modified | +2/−0 | `streamable-http` accepted as alias for `http` transport |
| changelog.md | Modified | +4/−0 | Version 2.1.138 entry (internal fixes) |
| interactive-mode.md | Modified | +1/−1 | Tab/Right arrow places suggestion rather than submitting it |
| security.md | Modified | +1/−1 | `--worktree` still enforces trust verification even with `-p` flag |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-09*
