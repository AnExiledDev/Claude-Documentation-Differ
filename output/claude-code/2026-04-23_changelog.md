# Claude Code Documentation Changes — 2026-04-23

## Summary

A new dedicated page for auto mode classifier configuration extracts ~116 lines from `permissions.md` into its own reference. Voice dictation gains a tap-to-record mode alongside the existing hold-to-record behavior, with a new `voice` settings object replacing the old `voiceEnabled` scalar. Monitoring telemetry adds `effort` attributes to cost and token counters, and new `command_name`/`command_source` fields appear on `user_prompt` events.

---

## Significant Changes

### Auto Mode Configuration (New Dedicated Page)

- **Auto mode classifier config extracted to its own page**: The sections "Review auto mode denials", "Configure the auto mode classifier", "Define trusted infrastructure", "Override the block and allow rules", and "Inspect the defaults and your effective config" have been removed from `permissions.md` and consolidated into a new `auto-mode-config.md` reference page.
  > "For rules that apply across projects, such as trusted infrastructure or organization-wide deny rules, use the `autoMode` settings block. The classifier reads `autoMode` from the following scopes..."
  - *Implication*: All internal links across `commands.md`, `desktop.md`, `permission-modes.md`, `server-managed-settings.md`, and `settings.md` now point to `/en/auto-mode-config` instead of `/en/permissions#configure-the-auto-mode-classifier`. Bookmarks to the old anchors will break.
  - *Source*: [Configure auto mode](https://code.claude.com/docs/en/auto-mode-config.md)

- **`environment` replacement warning strengthened**: The new page clarifies that setting `environment` also replaces the default environment list (not just `allow` and `soft_deny`). Previously the `<Danger>` block only called out `allow` or `soft_deny`.
  > "Setting any of `environment`, `allow`, or `soft_deny` replaces the entire default list for that section."
  - *Implication*: Organizations using `autoMode.environment` must include the defaults (via `claude auto-mode defaults`) to avoid narrowing the trusted scope.
  - *Source*: [Configure auto mode](https://code.claude.com/docs/en/auto-mode-config.md)

- **Scope table gains `--settings` flag row**: The configuration scope table now includes a row for `--settings` flag or Agent SDK inline JSON, documenting per-invocation overrides for automation.
  - *Source*: [Configure auto mode](https://code.claude.com/docs/en/auto-mode-config.md)

---

### Voice Dictation

- **Tap-to-record mode added**: A new `/voice tap` mode starts recording on a single keypress and sends the prompt automatically when recording stops. Previously only hold-to-talk (push-to-talk) was supported. Tap mode requires v2.1.116+.
  > "Tap mode toggles recording with a single keypress: tap once to start, speak, then tap again to send the prompt. There is no warmup, and you do not need to keep the key held."
  > "Recording also stops automatically after 15 seconds of silence or two minutes total."
  - *Implication*: The default remains hold mode. Run `/voice tap` or set `"mode": "tap"` in settings to switch.
  - *Source*: [Voice dictation](https://code.claude.com/docs/en/voice-dictation.md)

- **`/voice` command gains mode arguments**: `/voice` now accepts `hold`, `tap`, and `off` arguments. Previously it was a plain toggle with no arguments.
  > | `/voice` | Toggle on or off, keep the current mode |
  > | `/voice hold` | Enable in hold mode |
  > | `/voice tap` | Enable in tap mode |
  > | `/voice off` | Disable |
  - *Implication*: The `commands.md` entry is updated from `/voice` to `/voice [hold|tap|off]`.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

- **`voice` settings object replaces `voiceEnabled` scalar**: The settings key `voiceEnabled` (boolean) is now a legacy alias. The new `voice` object supports `enabled`, `mode` (`"hold"` or `"tap"`), and `autoSubmit`.
  > `"voice": { "enabled": true, "mode": "tap" }` — new preferred form
  > `"voiceEnabled": true` — legacy alias for `voice.enabled`. Prefer the `voice` object.
  - *Implication*: Existing settings using `voiceEnabled: true` continue to work but are now documented as deprecated.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`autoSubmit` option for hold mode**: Setting `"autoSubmit": true` in the `voice` object sends the prompt automatically when releasing the key in hold mode, provided the transcript is at least three words.
  - *Source*: [Voice dictation](https://code.claude.com/docs/en/voice-dictation.md)

- **Transcription does not consume Claude tokens**: Documentation now explicitly states that voice transcription does not consume Claude messages or tokens and does not count toward limits shown in `/usage`.
  - *Source*: [Voice dictation](https://code.claude.com/docs/en/voice-dictation.md)

- **VS Code extension voice dictation noted**: Voice dictation is confirmed to work in the VS Code extension but is unavailable in VS Code Remote sessions (SSH, Dev Containers, Codespaces) because the microphone is on the local machine while the extension runs on the remote host.
  - *Source*: [Voice dictation](https://code.claude.com/docs/en/voice-dictation.md)

---

### Model Configuration

- **`/model` selection persists to `.claude/settings.local.json`** (as of v2.1.117): When a project's `.claude/settings.json` pins a different model, Claude Code writes your `/model` choice to `.claude/settings.local.json` so the choice survives restarts in that project.
  > "As of v2.1.117, if the project's `.claude/settings.json` pins a different model, Claude Code also writes your choice to `.claude/settings.local.json` so it continues to apply in that project after a restart."
  - *Implication*: The model source is now shown in the startup header when it comes from project or managed settings.
  - *Source*: [Model config](https://code.claude.com/docs/en/model-config.md)

- **Default effort level simplified** (as of v2.1.117): The plan-dependent default effort differentiation ("medium on Pro and Max") is removed. The default is now `xhigh` on Opus 4.7 and `high` on Opus 4.6 and Sonnet 4.6 regardless of plan.
  > "As of v2.1.117, the default effort is `xhigh` on Opus 4.7 and `high` on Opus 4.6 and Sonnet 4.6."
  - *Source*: [Model config](https://code.claude.com/docs/en/model-config.md)

---

### Monitoring & Telemetry (OTEL)

- **`effort` attribute added to cost counter, token counter, API request event, and API error event**: The reasoning effort level is now emitted on all per-request telemetry as `"low"`, `"medium"`, `"high"`, `"xhigh"`, or `"max"`. Absent when the model does not support effort.
  > "`effort`: Effort level applied to the request: `"low"`, `"medium"`, `"high"`, `"xhigh"`, or `"max"`. Absent when the model does not support effort."
  - *Implication*: Teams using OTEL cost monitoring can now break down usage by reasoning effort tier.
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **`command_name` and `command_source` fields added to `user_prompt` events**: Slash command invocations are now captured in telemetry. Built-in command names are emitted as-is; custom, plugin, and MCP command names are redacted to `custom` or `mcp` by default, and only emitted verbatim when `OTEL_LOG_TOOL_DETAILS=1`.
  > "`command_name`: Command name when the prompt invokes one. ... Custom, plugin, and MCP command names collapse to `custom` or `mcp` unless `OTEL_LOG_TOOL_DETAILS=1` is set."
  > "`command_source`: Origin of the command when present: `builtin`, `custom`, or `mcp`. Plugin-provided commands report as `custom`."
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **`OTEL_LOG_TOOL_DETAILS` now also logs custom/MCP command names on `user_prompt` events**: In addition to existing tool parameter logging, enabling this flag causes `user_prompt` events to include the verbatim command names for custom, plugin, and MCP commands.
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

---

### Network Configuration

- **Network access requirements reformatted as a table**: The free-form bullet list is replaced with a structured table including all required URLs with descriptions. Two entries are newly explicit:
  - `bridge.claudeusercontent.com` — Chrome extension WebSocket bridge
  - `storage.googleapis.com` — marked as legacy (pre-v2.1.116 native installer only)
  > "If you install Claude Code through npm or manage your own binary distribution, end users may not need access to `downloads.claude.ai` or `storage.googleapis.com`."
  - *Source*: [Network config](https://code.claude.com/docs/en/network-config.md)

---

### Google Vertex AI

- **Multi-region endpoint support added**: `CLOUD_ML_REGION` now accepts multi-region values `eu` and `us` in addition to `global` and specific regions. Claude Code selects the correct hostname, including `aiplatform.eu.rep.googleapis.com` and `aiplatform.us.rep.googleapis.com`.
  > "Claude Code supports Vertex AI global, multi-region, and regional endpoints. Set `CLOUD_ML_REGION` to `global`, a multi-region location such as `eu` or `us`, or a specific region such as `us-east5`."
  - *Implication*: Some models are only available on `global` or multi-region locations; the troubleshooting section is updated accordingly.
  - *Source*: [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai.md)

---

### GitHub MCP Server Authentication

- **GitHub MCP server now requires an explicit PAT header**: The previous docs showed `claude mcp add --transport http github https://api.githubcopilot.com/mcp/` followed by interactive OAuth. The new docs require passing a personal access token as an `Authorization` header at add time.
  > "GitHub's remote MCP server authenticates with a GitHub personal access token passed as a header. To get one, open your GitHub token settings, generate a new fine-grained token... then add the server:"
  > ```bash
  > claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  >   --header "Authorization: Bearer YOUR_GITHUB_PAT"
  > ```
  - *Implication*: Existing GitHub MCP integrations set up via interactive auth will need to be reconfigured with a PAT header. Both `mcp.md` and `vs-code.md` are updated.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md), [VS Code](https://code.claude.com/docs/en/vs-code.md)

---

### Plugin Marketplace Enforcement

- **`strictKnownMarketplaces` and `blockedMarketplaces` enforcement extended**: Both settings now enforce restrictions at plugin install, update, refresh, and auto-update time — not only when adding a new marketplace. A marketplace added before the policy was configured can no longer be used to fetch plugins once its source falls outside the allowlist.
  > "The restriction is enforced on marketplace add and on plugin install, update, refresh, and auto-update. A marketplace added before the policy was set cannot be used to install or update plugins once its source no longer matches the allowlist."
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md), [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

- **New `dependency-unsatisfied` plugin error code**: A new error type surfaces when a declared dependency is not installed or is installed but disabled. The fix steps include running `claude plugin install` or `claude plugin marketplace add`.
  - *Source*: [Plugin dependencies](https://code.claude.com/docs/en/plugin-dependencies.md)

---

### Sub-agents: `mcpServers` in Main-Session Mode

- **`mcpServers` field now documented for `--agent` main-session context**: Previously only described for subagent spawning, the `mcpServers` frontmatter field also applies when an agent file is launched as the main session via `--agent`. Inline server definitions connect at startup alongside `.mcp.json` entries.
  > "The `mcpServers` field applies in both contexts where an agent file can run: as a subagent, spawned through the Agent tool or an @-mention; as the main session, launched with `--agent` or the `agent` setting."
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

---

### Session Resume from Summary

- **Large old sessions offer summary-based resume**: When resuming a session old and large enough to consume a substantial share of usage limits, `--resume`, `--continue`, and `/resume` now offer to resume from a summary instead of loading the full transcript. Not available on Amazon Bedrock, Google Cloud Vertex AI, or Microsoft Foundry.
  - *Source*: [Common workflows](https://code.claude.com/docs/en/common-workflows.md)

---

### Remote Control Status

- **Remote Control labeled "research preview"**: The note at the top of the Remote Control page now reads "Remote Control is in research preview and available on all plans."
  - *Source*: [Remote control](https://code.claude.com/docs/en/remote-control.md)

---

## Notable Details

- **Download URL change logged in changelog**: The release notes now document that Claude Code and the installer use `https://downloads.claude.ai/claude-code-releases` instead of the old `storage.googleapis.com` bucket path. This aligns with the network config table update marking `storage.googleapis.com` as a legacy pre-v2.1.116 host.

- **`~/.claude/backups/` moved to auto-cleanup**: The `backups/` directory (timestamped copies of `~/.claude.json` before config migrations) is now listed under auto-cleanup (deleted after `cleanupPeriodDays`, default 30 days) rather than "kept until you delete them". Teams relying on these config migration backups for rollback should be aware they expire.

- **`~/.claude/tasks/` and `~/.claude/shell-snapshots/` documented**: Two new auto-cleanup paths added to the directory reference: `tasks/` (per-session task lists from task tools) and `shell-snapshots/` (captured shell environment used by Bash tool, cleared on clean exit or by the cleanup sweep after a crash).

- **Deferred hook sessions subject to `cleanupPeriodDays`**: The hooks page now notes that sessions waiting on a `"defer"` result are retained "subject to the `cleanupPeriodDays` retention sweep that deletes session files after 30 days by default." Previously stated "no timeout or retry limit" with no retention caveat.

- **CLAUDE.md size guidance updated**: The recommended approach for large memory files now prioritizes path-scoped rules (`.claude/rules/` with path matchers) over `@path` imports, explicitly noting that imported files still load at launch and do not reduce context consumption.

- **Effort level defaults: plan-based differentiation removed**: The prior statement "default is `high`, or `medium` on Pro and Max" for Opus 4.6 and Sonnet 4.6 is replaced with a flat `high` default as of v2.1.117. The per-plan differentiation is gone from the docs.

---

## New Pages

- **[auto-mode-config.md](https://code.claude.com/docs/en/auto-mode-config.md)** — Full configuration reference for the auto mode classifier: where the classifier reads config, how to define trusted infrastructure with `autoMode.environment`, how to override block/allow rules, CLI subcommands (`claude auto-mode defaults|config|critique`), and how to review denials. Content previously embedded in `permissions.md`.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| auto-mode-config.md | New | +170 | Full auto mode classifier configuration reference, extracted from permissions.md |
| permissions.md | Modified | +2/-116 | Removed auto mode classifier config sections; added link to new auto-mode-config page |
| voice-dictation.md | Modified | +46/-17 | New tap-to-record mode, `/voice` mode arguments, `autoSubmit` option, new troubleshooting entries |
| sub-agents.md | Modified | +16/-1 | Clarified `mcpServers` applies in `--agent` main-session context; reformatted intro to bullet list |
| monitoring-usage.md | Modified | +8/-2 | Added `effort` attribute to metrics; new `command_name`/`command_source` fields on user_prompt events |
| common-workflows.md | Modified | +2/-0 | Summary-based resume offer for large old sessions |
| claude-directory.md | Modified | +21/-20 | Added `tasks/`, `shell-snapshots/`, `backups/` to auto-cleanup; moved `backups/` from permanent storage |
| network-config.md | Modified | +11/-13 | Reformatted as table; added Chrome bridge URL; marked storage.googleapis.com as legacy |
| model-config.md | Modified | +5/-1 | `/model` persists to local settings; effort defaults simplified as of v2.1.117 |
| settings.md | Modified | +7/-6 | New `voice` object; `voiceEnabled` now legacy; marketplace enforcement timing updated |
| permission-modes.md | Modified | +5/-4 | Updated links to new auto-mode-config page; updated See also section |
| mcp.md | Modified | +4/-7 | GitHub MCP example updated to require PAT header |
| vs-code.md | Modified | +3/-2 | GitHub MCP example updated to require PAT header |
| google-vertex-ai.md | Modified | +4/-4 | Multi-region endpoint support (`eu`, `us`) added |
| plugin-dependencies.md | Modified | +7/-6 | New `dependency-unsatisfied` error; additional dependency resolution triggers |
| plugin-marketplaces.md | Modified | +1/-1 | Enforcement timing extended beyond marketplace-add |
| memory.md | Modified | +2/-2 | CLAUDE.md size guidance now recommends path-scoped rules over imports |
| errors.md | Modified | +2/-2 | Context window guidance updated; effort default note simplified |
| hooks.md | Modified | +1/-1 | Deferred hook sessions now noted as subject to cleanupPeriodDays |
| interactive-mode.md | Modified | +3/-3 | Voice shortcut updated to reflect hold-or-tap; link to rebind-the-dictation-key |
| keybindings.md | Modified | +3/-3 | `voice:pushToTalk` description updated for hold/tap modes |
| commands.md | Modified | +2/-2 | `/voice` updated to `/voice [hold\|tap\|off]`; `/permissions` link updated |
| desktop.md | Modified | +1/-1 | `autoMode` setting link updated to auto-mode-config |
| server-managed-settings.md | Modified | +1/-1 | Link updated to auto-mode-config |
| remote-control.md | Modified | +1/-1 | Added "research preview" qualifier |
| changelog.md | Modified | +1/-0 | Download URL migration noted |

---

*Generated from Claude Code CLI documentation changes detected on 2026-04-23*
