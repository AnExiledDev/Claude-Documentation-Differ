# Claude Code Documentation Changes — 2026-04-02

## Summary

Version 2.1.90 was released on April 1, 2026, bringing a new `/powerup` interactive tutorial command, several bug fixes, and performance improvements. Alongside the release, documentation was updated to cover binary integrity verification (GPG-signed manifests starting v2.1.89), a new `--include-hook-events` CLI flag, managed subagents via organization settings, and an extension of the scheduled-task expiry window from 3 days to 7 days.

---

## Significant Changes

### Features & CLI

- **New `/powerup` command**: Interactive lessons teaching Claude Code features with animated demos, added in v2.1.90.
  > `Added /powerup — interactive lessons teaching Claude Code features with animated demos`
  - *Implication*: Provides an in-terminal onboarding path for new users without leaving the CLI.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **New `--include-hook-events` CLI flag**: Streams all hook lifecycle events into the `stream-json` output.
  > `--include-hook-events` — Include all hook lifecycle events in the output stream. Requires `--output-format stream-json`
  - *Implication*: Developers building pipelines on top of Claude Code's print mode can now observe hook execution in the event stream without additional tooling.
  - *Source*: [cli-reference.md](https://code.claude.com/docs/en/cli-reference.md)

- **`--include-partial-messages` requirement simplified**: Previously required `--print`, `--output-format stream-json`, *and* `--verbose`; the `--verbose` requirement has been dropped.
  - *Source*: [cli-reference.md](https://code.claude.com/docs/en/cli-reference.md)

- **`--replay-user-messages` requirement simplified**: Previously required `--print`, `--input-format stream-json`, `--output-format stream-json`, and `--verbose`; the `--print` and `--verbose` requirements have been removed.
  - *Source*: [cli-reference.md](https://code.claude.com/docs/en/cli-reference.md)

- **`--maintenance` behavior changed**: Flag description updated from "Run maintenance hooks and exit" to "Run maintenance hooks and **start interactive mode**".
  > Old: `Run maintenance hooks and exit`
  > New: `Run maintenance hooks and start interactive mode`
  - *Implication*: `--maintenance` no longer terminates after running hooks; it proceeds into an interactive session. Users relying on the exit behavior should review their workflows.
  - *Source*: [cli-reference.md](https://code.claude.com/docs/en/cli-reference.md)

- **`--agent-teams` flag removed from CLI reference**: The `--agent-teams` flag entry has been removed from the CLI flags table. Agent teams documentation now only references the `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` environment variable to enable `SendMessage`, `TeamCreate`, and `TeamDelete` tools.
  - *Implication*: The environment variable is the sole documented activation mechanism for experimental agent teams. Users relying on the `--agent-teams` flag should migrate to the env var.
  - *Source*: [cli-reference.md](https://code.claude.com/docs/en/cli-reference.md), [tools-reference.md](https://code.claude.com/docs/en/tools-reference.md)

- **`/tasks` command gains `/bashes` alias**:
  > `/tasks` — List and manage background tasks. Also available as `/bashes`
  - *Source*: [commands.md](https://code.claude.com/docs/en/commands.md)

- **`CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` env var**: New variable preserves the existing plugin marketplace cache when `git pull` fails, useful in offline or restricted-network environments.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

### Security & Installation

- **GPG-signed release manifests (from v2.1.89 onward)**: The setup documentation now includes a full step-by-step process for verifying release integrity using a GPG-signed `manifest.json`. The signing key fingerprint is:
  > `31DD DE24 DDFA B679 F42D  7BD2 BAA9 29FF 1A7E CACE`

  The manifest lists SHA256 checksums for every platform binary. Verifying the manifest signature transitively verifies every binary it covers.

  > Manifest signatures are available for releases from `2.1.89` onward. Earlier releases publish checksums in `manifest.json` without a detached signature.
  - *Implication*: Organizations with supply-chain requirements can now automate verification as part of their deployment pipeline.
  - *Source*: [setup.md](https://code.claude.com/docs/en/setup.md)

- **Platform code signing verification commands added**: Documentation now includes the exact commands to verify platform-native signatures rather than just listing that they exist:
  > * **macOS**: Verify with `codesign --verify --verbose ./claude`.
  > * **Windows**: Verify with `Get-AuthenticodeSignature .\claude.exe`.
  > * **Linux**: use the manifest signature above to verify integrity. Linux binaries are not individually code-signed.
  - *Source*: [setup.md](https://code.claude.com/docs/en/setup.md)

- **Network config URL roles clarified**: The "legacy/deprecation in progress" label for `storage.googleapis.com` was removed; `downloads.claude.ai` now explicitly covers signing keys and plugin executables. Both URLs are required.
  > `downloads.claude.ai`: CDN hosting the install script, version pointers, manifests, signing keys, and plugin executables
  > `storage.googleapis.com`: download bucket for the Claude Code binary and auto-updater
  - *Source*: [network-config.md](https://code.claude.com/docs/en/network-config.md)

### Subagents & Configuration

- **Managed subagents (organization-wide)**: A new "Managed settings" source is now documented as the highest-priority location for subagent definitions, superseding all user and project-level agents.
  > Managed subagents are deployed by organization administrators. Place markdown files in `.claude/agents/` inside the managed settings directory, using the same frontmatter format as project and user subagents. Managed definitions take precedence over project and user subagents with the same name.

  Updated priority table:

  | Priority | Location | Scope |
  |----------|----------|-------|
  | 1 (highest) | Managed settings | Organization-wide |
  | 2 | `--agents` CLI flag | Current session |
  | 3 | `.claude/agents/` | Current project |
  | 4 | `~/.claude/agents/` | All your projects |
  | 5 (lowest) | Plugin's `agents/` directory | Where plugin is enabled |

  - *Implication*: Enterprise administrators can now enforce standard subagent definitions that cannot be overridden by project or user configurations.
  - *Source*: [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md)

- **New `color` frontmatter field for subagents**: Subagents can now declare a display color shown in the task list and transcript.
  > `color` — Display color for the subagent in the task list and transcript. Accepts `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, or `cyan`
  - *Implication*: Useful when running multiple concurrent subagents to distinguish them visually.
  - *Source*: [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md)

- **`auto` permission mode added to subagents**: The `permissionMode` frontmatter field now accepts `auto` in addition to existing modes.
  > `auto` — Auto mode: an AI classifier evaluates each tool call
  - *Source*: [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md)

- **`Bash` removed from built-in helper agents table**: The `Bash` agent (model: Inherits, purpose: running terminal commands in a separate context) has been removed from the documented list of built-in helper agents. Only `statusline-setup` and `Claude Code Guide` remain.
  - *Source*: [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md)

- **`permissions.disableAutoMode` key corrected**: The settings key to disable auto mode was previously documented inconsistently as `disableAutoMode`; it is now consistently shown as `permissions.disableAutoMode`.
  > To prevent `bypassPermissions` or `auto` mode from being used, set `permissions.disableBypassPermissionsMode` or `permissions.disableAutoMode` to `"disable"` in any settings file.
  - *Implication*: Admins relying on the bare key `disableAutoMode` should verify their managed settings use the fully-qualified `permissions.disableAutoMode` key.
  - *Source*: [permissions.md](https://code.claude.com/docs/en/permissions.md)

### Scheduled Tasks

- **Recurring task expiry extended from 3 days to 7 days**:
  > Recurring tasks automatically expire **7 days** after creation. The task fires one final time, then deletes itself.

  The section heading was renamed from "Three-day expiry" to "Seven-day expiry".
  - *Implication*: Tasks set up early in the week will now survive through a weekend without requiring manual renewal.
  - *Source*: [scheduled-tasks.md](https://code.claude.com/docs/en/scheduled-tasks.md)

### Output Styles

- **Token usage documentation added**: A new paragraph clarifies cost implications of output styles.
  > Token usage depends on the style. Adding instructions to the system prompt increases input tokens, though prompt caching reduces this cost after the first request in a session. The built-in Explanatory and Learning styles produce longer responses than Default by design, which increases output tokens. For custom styles, output token usage depends on what your instructions tell Claude to produce.
  - *Source*: [output-styles.md](https://code.claude.com/docs/en/output-styles.md)

- **Removed misleading note about concise output**: The note "All output styles exclude instructions for efficient output (such as responding concisely)" has been removed.
  - *Implication*: The Default output style may include conciseness instructions; the prior statement implied it did not.
  - *Source*: [output-styles.md](https://code.claude.com/docs/en/output-styles.md)

### Bug Fixes (v2.1.90)

Notable fixes documented in the changelog:

- **Rate-limit dialog infinite loop**: Fixed auto-reopening options dialog after hitting usage limit, which could crash the session.
- **`--resume` prompt-cache miss**: Regression since v2.1.69 causing a full cache miss on first request for sessions with deferred tools, MCP servers, or custom agents.
- **PostToolUse format-on-save conflicts**: Fixed `Edit`/`Write` "File content has changed" errors when a format-on-save hook rewrites a file between consecutive edits.
- **`PreToolUse` hook blocking**: Fixed hooks emitting JSON to stdout and exiting with code 2 not correctly blocking the tool call.
- **Auto mode boundary respect**: Fixed auto mode ignoring explicit user constraints ("don't push", "wait for X before Y") even for otherwise-allowed actions.
- **PowerShell security hardening**: Fixed trailing `&` background job bypass, `-ErrorAction Break` debugger hang, archive-extraction TOCTOU, and parse-fail fallback deny-rule degradation.
- **DNS cache commands removed from auto-allow**: `Get-DnsClientCache` and `ipconfig /displaydns` are no longer auto-allowed (DNS cache privacy concern).

### Performance Improvements (v2.1.90)

- Eliminated per-turn `JSON.stringify` of MCP tool schemas on cache-key lookup.
- SSE transport now handles large streamed frames in linear time (previously quadratic).
- SDK sessions with long conversations no longer slow down quadratically on transcript writes.
- `/resume` all-projects view now loads project sessions in parallel.

### Fullscreen Rendering

- **Minimum version bumped**: Fullscreen rendering (`CLAUDE_CODE_NO_FLICKER=1`) now requires Claude Code v2.1.89 (was v2.1.88).
  - *Source*: [fullscreen.md](https://code.claude.com/docs/en/fullscreen.md)

---

## Notable Details

- **IDE integrations link changed** in `how-claude-code-works.md`: The reference to `/en/ide-integrations` was updated to `/en/vs-code`, suggesting the IDE integrations overview has been consolidated into the VS Code-specific page.
- **Remote Control anchor updated**: Both `claude remote-control` and `--remote-control` flag descriptions now link to `#start-a-remote-control-session` instead of `#server-mode` and `#interactive-session` respectively.
- **`--teammate-mode` link updated**: Now points to `#choose-a-display-mode` instead of `#set-up-agent-teams`.
- **Plugin version prerequisite removed**: Both `plugins.md` and `discover-plugins.md` dropped the specific mention of "version 1.0.33 or later" as a requirement for the `/plugin` command, replacing it with generic "update to the latest version" guidance.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| setup.md | Modified | +90/−10 | Added full GPG manifest verification workflow and platform code signing commands |
| cli-reference.md | Modified | +80/−80 | Added `--include-hook-events`; changed `--maintenance` behavior; simplified streaming flag requirements; removed `--agent-teams` |
| sub-agents.md | Modified | +41/−37 | Added managed subagents, `color` field, `auto` permission mode; removed `Bash` from helper agents |
| tools-reference.md | Modified | +36/−36 | Removed `--agent-teams` flag references from `SendMessage`, `TeamCreate`, `TeamDelete` |
| changelog.md | Modified | +22/−0 | Added v2.1.90 release notes |
| output-styles.md | Modified | +7/−2 | Added token usage documentation; removed concise-output note |
| computer-use.md | Modified | +8/−6 | Updated Desktop settings path; added plan-availability annotation |
| network-config.md | Modified | +3/−3 | Clarified CDN URL roles; removed "legacy/deprecation" language |
| permissions.md | Modified | +2/−2 | Corrected `disableAutoMode` to `permissions.disableAutoMode` |
| scheduled-tasks.md | Modified | +2/−2 | Extended recurring task expiry from 3 to 7 days |
| commands.md | Modified | +1/−1 | Added `/bashes` as alias for `/tasks` |
| fullscreen.md | Modified | +1/−1 | Minimum version bumped to v2.1.89 |
| how-claude-code-works.md | Modified | +1/−1 | Updated IDE integrations link from `/ide-integrations` to `/vs-code` |
| plugins.md | Modified | +0/−1 | Removed v1.0.33 version prerequisite |
| discover-plugins.md | Modified | +1/−1 | Removed specific version number from troubleshooting guidance |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-02*
