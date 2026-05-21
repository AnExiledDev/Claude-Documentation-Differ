# Claude Code Documentation Changes — 2026-05-21

## Summary

Six pages were modified across the Claude Code documentation, spanning a v2.1.146 release entry, a new enterprise managed-settings lockdown feature (`strictPluginOnlyCustomization`), and several clarifications to hook exit-code semantics. The hook documentation also gains new event fields and corrects the hook-type support lists for `PermissionDenied` and `TeammateIdle`.

---

## Significant Changes

### Enterprise / Admin Settings

- **New managed setting: `strictPluginOnlyCustomization`**: Administrators can now block skills, agents, hooks, and MCP servers from user-level and project-level sources, restricting them to plugin-provided or managed-settings sources only.
  > `true` locks all four surfaces; an array such as `["skills", "hooks"]` locks only the named ones.
  
  The setting operates per-surface:

  | Surface  | Blocked when locked                               | Still loads                                                                         |
  |----------|---------------------------------------------------|-------------------------------------------------------------------------------------|
  | `skills` | `~/.claude/skills/`, `.claude/skills/`            | Plugin skills, bundled skills, skills in the managed policy directory               |
  | `agents` | `~/.claude/agents/`, `.claude/agents/`            | Plugin agents, built-in agents, agents in the managed policy directory              |
  | `hooks`  | Hooks in user, project, and local `settings.json` | Plugin hooks, hooks in managed settings                                             |
  | `mcp`    | Servers in `~/.claude.json` and `.mcp.json`       | Plugin MCP servers, `managed-mcp.json` servers                                      |

  > Combine it with `strictKnownMarketplaces` to control the full customization supply chain: the marketplace allowlist controls which plugins users can install, and this setting blocks everything that doesn't come from a plugin or from managed settings.

  - *Implication*: This is a managed-settings-only key requiring Claude Code v2.1.82+. Earlier clients ignore it silently, so rollout in mixed-version fleets requires care.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md), [Permissions](https://code.claude.com/docs/en/permissions.md), [Admin Setup](https://code.claude.com/docs/en/admin-setup.md)

- **`strictPluginOnlyCustomization` added to admin control surface table**: The admin setup page now includes a dedicated row for "Customization lockdown" alongside the existing permission, sandboxing, and hook restriction controls.
  > Block skills, agents, hooks, and MCP servers from user and project sources, so they can only come from plugins or managed settings
  - *Source*: [Admin Setup](https://code.claude.com/docs/en/admin-setup.md)

### Hooks

- **Exit code 0 semantics clarified — it no longer means "allow"**: Documentation across both `hooks.md` and `hooks-guide.md` now explicitly states that exit code 0 from a `PreToolUse` hook means *no decision*, not approval. The normal permission flow still applies.
  > Exit code 0 with no output means the hook has no decision to report, so the tool call continues through the normal permission flow. The hook can deny the call, but staying silent doesn't approve it.

  The updated exit code table now reads:
  > **Exit 0**: the hook reports no objection and the action proceeds normally. For a `PreToolUse` hook this doesn't approve the tool call: the normal permission flow still applies.

  - *Implication*: If you relied on exit 0 to act as an implicit approval (e.g., to bypass interactive permission prompts), that assumption is now explicitly wrong. Use `hookSpecificOutput.permissionDecision: "allow"` to approve explicitly.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md), [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)

- **Structured JSON output description updated**: The introductory sentence describing when to use JSON output has changed to align with the new exit-0 semantics.
  > Exit codes only let you block or stay silent. For more control, exit 0 and print a JSON object to stdout instead.
  - *Source*: [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md), [Hooks](https://code.claude.com/docs/en/hooks.md)

- **New `SessionStart` hook output fields — `initialUserMessage` and `watchPaths`**: Two new event-specific fields are now documented for `SessionStart` hooks.
  > `initialUserMessage`: String used as the first user message of the session. Applies in non-interactive mode (`-p`), where it becomes the first turn even if no prompt is provided. If a prompt is provided, it follows as the next turn. Unlike `additionalContext`, which attaches to an existing turn, this creates the turn.
  >
  > `watchPaths`: Array of absolute paths to watch for FileChanged events during this session.
  - *Implication*: Hooks can now bootstrap headless sessions with a synthesized first user message and configure file-watch paths dynamically at session start.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

- **New `UserPromptSubmit` field — `suppressOriginalPrompt`**: A new field is available when blocking a prompt via `decision: "block"`.
  > `suppressOriginalPrompt`: If `true` when `decision` is `"block"`, omits the original prompt text from the block message shown to the user.
  - *Implication*: Allows hooks to block sensitive prompts without leaking the prompt content in the UI notification.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

- **`PermissionDenied` and `TeammateIdle` now support all five hook types**: Both events were previously listed under the command/http/mcp_tool-only table. They now appear in the "all five hook types" table, meaning `prompt` and `agent` hooks can also subscribe to these events.
  - *Implication*: Prompt-based and agent-based hooks can now react to permission denials and idle teammates. However, note that for `PermissionDenied`, prompt and agent hook output is discarded — only command hooks can return `hookSpecificOutput.retry`.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

- **Decision control table gains `SessionStart`, `Setup`, `SubagentStart` row**: A new "Context only" pattern row is added to the event decision table, documenting that these events accept `hookSpecificOutput.additionalContext` but offer no blocking or decision control.
  > `SessionStart` also accepts `initialUserMessage` and `watchPaths`. No blocking or decision control.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

- **`TeammateIdle` `ok: false` behavior documented**: Clarifies what happens when a hook blocks a `TeammateIdle` event.
  > `TeammateIdle`: by default the teammate stops and the reason appears as a warning line. Set `continueOnBlock: true` to feed the reason back to the teammate and keep it working instead.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

- **`PermissionDenied` `ok: false` behavior documented**: Explicitly states that `ok: false` has no effect on `PermissionDenied` since the denial already happened, and that only command hooks (not prompt or agent hooks) can set `hookSpecificOutput.retry`.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

- **`suppressOutput` description corrected**: The field now correctly states that it hides stdout from the *transcript*, not the debug log.
  > If `true`, hides the hook's stdout from the transcript. Stdout still appears in the debug log.
  - *Implication*: Hooks using `suppressOutput: true` will still have their stdout available for debugging — it was previously ambiguous whether the debug log was also suppressed.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

### Permission Modes

- **New `auto` mode added to `setMode` valid values**: The `PermissionRequest` hook's `setMode` operation now accepts `auto` alongside the existing `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, and `plan` modes.
  > Valid modes are `default`, `auto`, `acceptEdits`, `dontAsk`, `bypassPermissions`, and `plan`.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

### Changelog — v2.1.146 (May 21, 2026)

- **`/simplify` renamed to `/code-review`** with an optional effort level parameter (e.g., `/code-review high`).
- **Auto mode no longer suppresses `AskUserQuestion`** when the user or a skill explicitly relies on it.
- **Bug fixes**:
  - Windows PowerShell tool failed with "command line is invalid" when `pwsh` is installed via winget or Microsoft Store (regression in v2.1.124) — fixed.
  - MCP `resources/list`, `resources/templates/list`, and `prompts/list` dropped items past page 1 on paginating servers — fixed.
  - Full-screen strobing in attached background sessions on Windows Terminal while streaming — fixed.
  - Auto-updater status line not showing current version when an update fails — fixed.
  - On Windows, removing a background-job worktree no longer follows NTFS junctions into the main repo.
  - `/background` was refusing sessions whose only typed input was a skill or custom slash command — fixed.
  - Backgrounded sessions re-prompted for tool permissions already granted with "don't ask again" — fixed.
  - `/theme` color editor and "New custom theme" dialogs not responding to Esc — fixed.
  - Uncaught exception at the end of streaming sessions when running via the Agent SDK — fixed.
  - `forceLoginOrgUUID` and `forceLoginMethod` managed-settings policies not enforced against third-party-provider and API-key sessions — fixed.
  - GNOME Terminal right-click and middle-click paste not inserting text — fixed.
  - `CLAUDE_CODE_SUBAGENT_MODEL` not forwarded to child processes in multi-agent sessions — fixed.
- **Improved auto-updater reliability**: native version checks and downloads now retry transient network failures.
- **Improved diff rendering performance** for large file edits.
- *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

## Migration Notes

- **Hook exit code 0 is no longer documented as "allow"**: If any `PreToolUse` hook relied on exit 0 to grant permission implicitly, update it to return `{"hookSpecificOutput": {"permissionDecision": "allow"}}` for an explicit allow.
- **`/simplify` command renamed to `/code-review`**: Update scripts, keybindings, or documentation that reference `/simplify`.
- **`strictPluginOnlyCustomization` requires v2.1.82+**: Clients on earlier versions silently ignore this key. Enforce a `minimumVersion` floor before relying on this lockdown.

---

## Notable Details

- The `strictPluginOnlyCustomization` setting's surface-name handling is forward-compatible: unrecognized surface names are ignored rather than failing the settings file, allowing admins to configure new surfaces before all clients have updated.
- `PermissionDenied` prompt and agent hooks now run (they can subscribe) but their output is silently discarded — only command hooks can influence retry behavior on this event. This is a subtle but important constraint for hook authors.
- The `initialUserMessage` field for `SessionStart` creates a new conversation turn rather than attaching to an existing one (unlike `additionalContext`), which matters for how the conversation history is structured in non-interactive sessions.

---

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| `en/hooks.md` | Modified | SIGNIFICANT | +34/-28 | Exit code 0 semantics clarified; new SessionStart fields (`initialUserMessage`, `watchPaths`); new `suppressOriginalPrompt` for UserPromptSubmit; `PermissionDenied`/`TeammateIdle` moved to all-hook-types list; `auto` mode added; `suppressOutput` corrected |
| `en/settings.md` | Modified | SIGNIFICANT | +28/-0 | New `strictPluginOnlyCustomization` setting entry and full reference section added |
| `en/changelog.md` | Modified | SIGNIFICANT | +19/-0 | v2.1.146 release notes added |
| `en/permissions.md` | Modified | SIGNIFICANT | +15/-14 | `strictPluginOnlyCustomization` added to managed-only settings table |
| `en/admin-setup.md` | Modified | SIGNIFICANT | +12/-11 | "Customization lockdown" row added to managed settings control surface table |
| `en/hooks-guide.md` | Modified | SIGNIFICANT | +3/-3 | Exit code 0 and JSON output intro text updated to match new "no decision" semantics |

---

*Generated from Claude Code CLI documentation changes detected on 2026-05-21*
