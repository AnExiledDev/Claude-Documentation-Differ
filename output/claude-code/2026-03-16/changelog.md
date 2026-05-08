# Claude Code Documentation Changes — 2026-03-16

## Summary

Five pages were updated in this cycle, with the most significant changes to the hooks system. The `PermissionRequest` hook gained a richer, formally documented permission update API — including new entry types for managing rules, modes, and directories — along with a new guide example showing how to auto-approve specific permission dialogs. A JSON formatting bug in the server-managed settings example was also corrected.

## Significant Changes

### Hooks: Permission Update Entries (New Reference Section)

- **Formal schema for `updatedPermissions` and `permission_suggestions`**: A new `#### Permission update entries` section in the hooks reference documents the complete set of entry objects that both `updatedPermissions` (hook output) and `permission_suggestions` (hook input) accept. Previously, these fields were described only in prose; they now have structured tables.

  > The `updatedPermissions` output field and the `permission_suggestions` input field both use the same array of entry objects. Each entry has a `type` that determines its other fields, and a `destination` that controls where the change is written.

  Six entry types are now documented:

  | `type` | Effect |
  |---|---|
  | `addRules` | Adds permission rules (`toolName`, optional `ruleContent`, `behavior`) |
  | `replaceRules` | Replaces all rules of a given behavior at a destination |
  | `removeRules` | Removes matching rules |
  | `setMode` | Changes permission mode (`default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`) |
  | `addDirectories` | Adds working directories |
  | `removeDirectories` | Removes working directories |

  Four `destination` values control persistence:

  | `destination` | Writes to |
  |---|---|
  | `session` | In-memory only; discarded at session end |
  | `localSettings` | `.claude/settings.local.json` |
  | `projectSettings` | `.claude/settings.json` |
  | `userSettings` | `~/.claude/settings.json` |

  - *Implication*: Hook authors can now precisely target where permission changes persist. A hook can echo back a `permission_suggestions` entry it received as its own `updatedPermissions` output, replicating what a user would do by selecting "always allow" in the dialog.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **`permission_suggestions` example updated**: The `PermissionRequest` input example replaced the `toolAlwaysAllow` type with the `addRules` type, aligning the documented schema with the new entry format.

  Before:
  ```json
  { "type": "toolAlwaysAllow", "tool": "Bash" }
  ```
  After:
  ```json
  {
    "type": "addRules",
    "rules": [{ "toolName": "Bash", "ruleContent": "rm -rf node_modules" }],
    "behavior": "allow",
    "destination": "localSettings"
  }
  ```

  - *Implication*: The old `toolAlwaysAllow` type is no longer shown in documentation; hooks that previously used that type should be updated to `addRules`.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

### Hooks Guide: Auto-Approve Permission Prompts (New Example)

- **New `PermissionRequest` hook example for auto-approval**: A new section "Auto-approve specific permission prompts" was added to the hooks guide. It demonstrates how to skip the permission dialog for specific tool calls by writing a JSON decision to stdout.

  > Unlike the exit-code examples above, auto-approval requires your hook to write a JSON decision to stdout. A `PermissionRequest` hook fires when Claude Code is about to show a permission dialog, and returning `"behavior": "allow"` answers it on your behalf.

  The example auto-approves `ExitPlanMode` specifically:

  ```json
  {
    "hooks": {
      "PermissionRequest": [
        {
          "matcher": "ExitPlanMode",
          "hooks": [
            {
              "type": "command",
              "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"PermissionRequest\", \"decision\": {\"behavior\": \"allow\"}}}'"
            }
          ]
        }
      ]
    }
  }
  ```

  The section also shows how to combine approval with a `setMode` change (e.g., switching the session to `acceptEdits`) using `updatedPermissions`.

  > Keep the matcher as narrow as possible. Matching on `.*` or leaving the matcher empty would auto-approve every permission prompt, including file writes and shell commands.

  - *Implication*: Developers who always approve certain prompts (like plan-mode exits) can now eliminate those interruptions entirely using a targeted `PermissionRequest` hook. The documentation explicitly warns against broad matchers.
  - *Source*: [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)

### Sub-Agents: Plugin Security Restriction Documented

- **Plugin subagents cannot use `hooks`, `mcpServers`, or `permissionMode`**: A new `<Note>` block explicitly documents that these three frontmatter fields are ignored when loading agents from a plugin, for security reasons.

  > For security reasons, plugin subagents do not support the `hooks`, `mcpServers`, or `permissionMode` frontmatter fields. These fields are ignored when loading agents from a plugin. If you need them, copy the agent file into `.claude/agents/` or `~/.claude/agents/`. You can also add rules to `permissions.allow` in `settings.json` or `settings.local.json`, but these rules apply to the entire session, not just the plugin subagent.

  - *Implication*: Plugin authors who rely on hooks or custom MCP servers inside plugin agents need to document this limitation or instruct users to copy agents into their local agent directories. This is a pre-existing behavior now made explicit in docs.
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

### Server-Managed Settings: JSON Example Bug Fix

- **`disableBypassPermissionsMode` moved inside `permissions` object**: The JSON example showing how to enforce a deny list and disable bypass mode had a structural error — `disableBypassPermissionsMode` was placed as a sibling of `permissions` rather than nested inside it.

  Before (incorrect):
  ```json
  {
    "permissions": {
      "deny": ["Bash(curl *)", "Read(./.env)", ...]
    },
    "disableBypassPermissionsMode": "disable"
  }
  ```
  After (correct):
  ```json
  {
    "permissions": {
      "deny": ["Bash(curl *)", "Read(./.env)", ...],
      "disableBypassPermissionsMode": "disable"
    }
  }
  ```

  - *Implication*: Administrators who copied the previous example verbatim may have had `disableBypassPermissionsMode` silently ignored. The corrected example reflects the actual settings schema.
  - *Source*: [Server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md)

## Notable Details

- **Status line Bash examples switched from `tr` to parameter expansion**: The context window progress bar examples in `statusline.md` replaced `printf "%Ns" | tr ' ' '▓'` with `printf -v VAR "%Ns" && ${VAR// /▓}`. This is a functional change in the example code — the new form avoids spawning a `tr` subprocess and uses pure Bash string substitution, which is more efficient in tight loops. The Python and Node.js examples were not changed.

- **`updatedPermissions` field description updated**: The description of `updatedPermissions` in the `PermissionRequest` decision control table changed from "equivalent to the user selecting an 'always allow' option" to "array of [permission update entries] to apply, such as adding an allow rule or changing the session permission mode." This reflects the expanded capabilities now documented in the new entry types section.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| hooks-guide.md | Modified | +49 / -0 | New "Auto-approve specific permission prompts" section with `PermissionRequest` hook example |
| hooks.md | Modified | +37 / -8 | New "Permission update entries" reference section; `permission_suggestions` example updated from `toolAlwaysAllow` to `addRules` |
| sub-agents.md | Modified | +4 / -0 | Added note that plugin subagents do not support `hooks`, `mcpServers`, or `permissionMode` fields |
| server-managed-settings.md | Modified | +3 / -3 | Fixed JSON structure: `disableBypassPermissionsMode` now correctly nested inside `permissions` |
| statusline.md | Modified | +6 / -4 | Updated Bash progress bar examples to use `printf -v` and parameter expansion instead of `tr` |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-16*
