# Claude Code Documentation Changes — 2026-02-28

## Summary

Five pages were updated in this batch. The most substantive changes are to sandboxing and settings, which document a new `sandbox.filesystem` configuration API (`allowWrite`, `denyWrite`, `denyRead`) that gives subprocess commands granular OS-level filesystem access control. HTTP hooks gained two new security controls — URL allowlisting and environment variable interpolation restrictions — with a corresponding `allowedEnvVars` field added to the hook schema. Session management for Claude Code on the web received new archive and delete functionality.

## Significant Changes

### Sandboxing

- **New `sandbox.filesystem` path control settings**: Three new settings keys — `filesystem.allowWrite`, `filesystem.denyWrite`, and `filesystem.denyRead` — are now documented under the sandbox configuration. These allow subprocess commands like `kubectl`, `terraform`, and `npm` to write outside the project working directory, or to have specific paths blocked for reads and writes.
  > "By default, sandboxed commands can only write to the current working directory. If subprocess commands like `kubectl`, `terraform`, or `npm` need to write outside the project directory, use `sandbox.filesystem.allowWrite` to grant access to specific paths"
  - *Implication*: Teams running infra tooling inside sandboxes no longer need to add those tools to `excludedCommands` as a workaround; they can instead grant targeted write access to specific paths.
  - *Source*: [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)

- **Path prefix semantics documented**: A new reference table documents how path strings are resolved in `filesystem.allowWrite`, `filesystem.denyWrite`, and `filesystem.denyRead`:

  | Prefix | Meaning | Example |
  |:-------|:--------|:--------|
  | `//` | Absolute path from filesystem root | `//tmp/build` → `/tmp/build` |
  | `~/` | Relative to home directory | `~/.kube` → `$HOME/.kube` |
  | `/` | Relative to the settings file's directory | `/build` → `$SETTINGS_DIR/build` |
  | `./` or no prefix | Relative path (resolved by sandbox runtime) | `./output` |

  - *Implication*: The `//` double-slash convention is the correct way to express an absolute path; a single `/` is settings-file-relative, which is easy to confuse.
  - *Source*: [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)

- **Array merging behavior clarified**: All three `sandbox.filesystem` arrays merge across settings scopes (user, project, managed) rather than replacing each other.
  > "When `allowWrite` (or `denyWrite`/`denyRead`) is defined in multiple settings scopes, the arrays are **merged**, meaning paths from every scope are combined, not replaced."
  - *Implication*: Managed settings can define a base set of allowed paths without preventing users or projects from adding more; useful for enterprise deployments where central policy sets minimums.
  - *Source*: [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)

- **Sandbox vs. permissions framing updated**: The docs previously stated "Filesystem and network restrictions are configured through permission rules, not sandbox settings." This has been corrected to "configured through both sandbox settings and permission rules," with clarification that sandbox filesystem paths and permission rule paths are merged together.
  - *Implication*: The old framing was inaccurate for sandboxed subprocess access. Developers who relied solely on permission rules for filesystem control should review whether `sandbox.filesystem` settings are a better fit.
  - *Source*: [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)

### HTTP Hooks Security Controls

- **New `allowedEnvVars` field on HTTP hooks**: HTTP hooks now have an `allowedEnvVars` field that acts as an explicit allowlist of environment variable names that may be interpolated into header values. References to variables not in this list are replaced with empty strings.
  > "| `allowedEnvVars` | no | List of environment variable names that may be interpolated into header values. References to unlisted variables are replaced with empty strings. Required for any env var interpolation to work |"
  - *Implication*: Any existing HTTP hook that interpolates environment variables into headers (e.g., `"Authorization": "Bearer $MY_TOKEN"`) must now also declare `"allowedEnvVars": ["MY_TOKEN"]` for the interpolation to take effect.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

- **New `allowedHttpHookUrls` settings key**: Administrators can now define a URL allowlist for HTTP hooks. Hooks targeting non-matching URLs are silently blocked. Supports `*` as a wildcard. An empty array blocks all HTTP hooks; omitting the setting applies no restriction.
  > "`allowedHttpHookUrls` — Allowlist of URL patterns that HTTP hooks may target. Supports `*` as a wildcard. When set, hooks with non-matching URLs are blocked."
  - *Implication*: Enterprise deployments can now restrict which endpoints HTTP hooks are permitted to call, closing an exfiltration vector.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **New `httpHookAllowedEnvVars` settings key**: Complements the per-hook `allowedEnvVars` field with a global allowlist. Each hook's effective env var set is the intersection of its own `allowedEnvVars` and this setting.
  > "`httpHookAllowedEnvVars` — Allowlist of environment variable names HTTP hooks may interpolate into headers. When set, each hook's effective `allowedEnvVars` is the intersection with this list."
  - *Implication*: Admins can enforce an organization-wide cap on which secrets HTTP hooks may access in headers, regardless of what individual hooks declare.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **Disclaimer scope narrowed**: The security disclaimer previously read "Hooks run with your system user's full permissions." It now reads "Command hooks run with your system user's full permissions," scoping the warning explicitly to command hooks rather than all hook types.
  - *Implication*: HTTP hooks are now implicitly distinguished from command hooks in the security model, consistent with the new HTTP-specific access controls.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

### Session Management (Claude Code on the Web)

- **Archive and delete session actions added**: A new "Managing sessions" section documents two new session lifecycle actions in the web UI.
  - **Archive**: Hides a session from the default list; recoverable by filtering for archived sessions.
  - **Delete**: Permanently removes a session and all its event data. Requires confirmation. Sessions must first be archived before they can be deleted from the sidebar.
  > "Deleting a session permanently removes the session and its data. This action cannot be undone."
  - *Implication*: Users can now clean up session history and permanently purge session event data on demand, without contacting support.
  - *Source*: [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

### Data Usage

- **Session deletion cross-referenced in data retention docs**: The data-usage page now explicitly states that individual web sessions can be deleted at any time and links to the new Managing sessions section.
  > "You can delete individual Claude Code on the web sessions at any time. Deleting a session permanently removes the session's event data."
  - *Implication*: Users with data residency concerns have a documented self-service path for removing session data without waiting for the retention period to expire.
  - *Source*: [Data usage](https://code.claude.com/docs/en/data-usage.md)

## Notable Details

- The settings.md configuration example was updated to use `sandbox.filesystem` directly in place of the previous `permissions.deny` approach. The old example showed `Read(.envrc)` and `Read(~/.aws/**)` as deny rules; the new example uses `"denyRead": ["~/.aws/credentials"]` inside the `filesystem` block alongside `"allowWrite": ["//tmp/build", "~/.kube"]`. This is a meaningful shift in recommended practice, not just a documentation cleanup.

- The `allowedHttpHookUrls` and `httpHookAllowedEnvVars` settings are documented as merging across settings scopes (user, project, managed), consistent with the array-merging behavior now applying broadly to array-valued settings. A new callout note in settings.md makes this policy explicit: "When the same array-valued setting ... appears in multiple scopes, the arrays are **concatenated and deduplicated**, not replaced."

- The Hook configuration section description was broadened from "Managed settings only" to cover all settings levels, reflecting that `allowedHttpHookUrls` and `httpHookAllowedEnvVars` (unlike `allowManagedHooksOnly`) are not restricted to managed settings.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| claude-code-on-the-web.md | Modified | +17/-0 | Added "Managing sessions" section with archive and delete instructions |
| data-usage.md | Modified | +2/-0 | Added note that web sessions can be individually deleted, with link to new session management docs |
| hooks.md | Modified | +10/-8 | Added `allowedEnvVars` field to HTTP hook schema; narrowed security disclaimer to "command hooks"; updated example to show `allowedEnvVars` usage |
| sandboxing.md | Modified | +37/-1 | Added `sandbox.filesystem.allowWrite/denyWrite/denyRead` docs with path prefix table, array merge behavior, and updated permissions vs. sandbox framing |
| settings.md | Modified | +42/-16 | Added `filesystem.allowWrite/denyWrite/denyRead` to sandbox settings table; added "Sandbox path prefixes" section; added `allowedHttpHookUrls` and `httpHookAllowedEnvVars` settings; updated config example; added array-merge behavior note |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-28*
