# Claude Code Documentation Changes — 2026-05-01

## Summary

Version 2.1.126 shipped on May 1, 2026 with 25 modified documentation pages covering a significant batch of new features, bug fixes, and behavior changes. The most structurally notable changes are: a new `claude project purge` command, expanded `bypassPermissions` mode that now truly bypasses all protected paths, automatic model discovery from LLM gateway `/v1/models` endpoints, and PowerShell-first shell behavior on Windows when the PowerShell tool is enabled.

A second documentation update later in the day made two minor editorial corrections to the v2.1.126 changelog entry. A third update clarified the scope of `CLAUDE_CODE_SHELL_PREFIX` to explicitly enumerate which shell commands it covers (see "Notable Details" below).

---

## Significant Changes

### New CLI Command: `claude project purge`

- **`claude project purge [path]`**: New command to delete all Claude Code state for a project — transcripts, task lists, debug logs, file-edit history, prompt history lines, and the project's entry in `~/.claude.json`. Omit `[path]` to pick interactively.
  > "Run `claude project purge` to delete the state Claude Code holds for one project… The command prints the full deletion plan and asks for confirmation before removing anything."
  - Flags: `--dry-run` to preview, `-y`/`--yes` to skip confirmation, `-i`/`--interactive` to step through item by item, `--all` to purge every project at once (which deletes `history.jsonl` outright).
  - The command leaves `shell-snapshots/` and `backups/` untouched; exits with status 1 if no state matches the given path.
  - *Implication*: Provides a safe, auditable path for cleaning project data without manual directory deletion.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md), [Claude Directory](https://code.claude.com/docs/en/claude-directory.md)

### `bypassPermissions` Mode Now Bypasses All Protected Paths

- **Protected paths no longer exempt in `bypassPermissions`**: Previously, writes to `.git`, `.claude`, `.vscode`, `.idea`, and `.husky` still prompted even in `bypassPermissions` mode. As of v2.1.126, those writes are allowed without prompting.
  > "`bypassPermissions` mode disables permission prompts and safety checks so tool calls execute immediately. As of v2.1.126 this includes writes to [protected paths], which earlier versions still prompted for. Removals targeting the filesystem root or home directory, such as `rm -rf /` and `rm -rf ~`, still prompt as a circuit breaker against model error."
  - The summary table for `bypassPermissions` changed from "Everything except protected paths" → "Everything."
  - The protected-paths section now reads: "Writes to a small set of paths are never auto-approved, in every mode *except `bypassPermissions`*."
  - *Implication*: Operators running isolated container/VM environments no longer receive unexpected prompts for git or editor config writes. Ensure `bypassPermissions` is only used in genuinely isolated environments.
  - *Source*: [Permission Modes](https://code.claude.com/docs/en/permission-modes.md), [Permissions](https://code.claude.com/docs/en/permissions.md)

### LLM Gateway: Automatic Model Discovery from `/v1/models`

- **Gateway model auto-discovery**: When `ANTHROPIC_BASE_URL` points at a gateway exposing the Anthropic Messages format, Claude Code now queries the gateway's `/v1/models` endpoint at startup and adds returned models to the `/model` picker. Requires v2.1.126+.
  > "Each discovered entry is labeled 'From gateway' and uses the `display_name` field from the response when one is provided… Results are cached to `~/.claude/cache/gateway-models.json` and refreshed on each startup. If the request fails or the gateway does not implement `/v1/models`, the picker falls back to the cached list from the previous startup or to the built-in model list."
  - Only models whose ID begins with `claude` or `anthropic` are added. Discovery does not apply to Bedrock, Vertex, or `api.anthropic.com`.
  - `ANTHROPIC_CUSTOM_MODEL_OPTION` description updated: "For LLM gateway deployments, Claude Code populates the picker automatically from the gateway's `/v1/models` endpoint, so this variable is needed only when discovery does not return the model you want."
  - *Implication*: Gateway operators no longer need to manually enumerate models via `ANTHROPIC_CUSTOM_MODEL_OPTION` for standard claude/anthropic-prefixed model IDs.
  - *Source*: [LLM Gateway](https://code.claude.com/docs/en/llm-gateway.md), [Model Config](https://code.claude.com/docs/en/model-config.md)

### Windows: PowerShell Becomes Primary Shell

- **PowerShell tool promoted to primary shell on Windows**: When the PowerShell tool is enabled, Claude now treats PowerShell as the primary shell rather than defaulting to Bash.
  > "When the tool is enabled, Claude treats PowerShell as the primary shell. The Bash tool remains available for POSIX scripts when Git Bash is installed."
  - PowerShell 7 detection improved: now finds `pwsh` installed via Microsoft Store, MSI without PATH, or `.NET global tool`.
  - *Implication*: Windows users who enable the PowerShell tool will see Claude default to PowerShell commands; Bash remains a fallback when Git Bash is present.
  - *Source*: [Tools Reference](https://code.claude.com/docs/en/tools-reference.md)

### PowerShell Permission Rules

- **New PowerShell permission rule documentation**: A new `### PowerShell` section in the permissions reference documents how to write allow/deny rules for PowerShell commands.
  > "PowerShell permission rules use the same shape as Bash rules. Wildcards with `*` match at any position… Common aliases are canonicalized before matching. A rule written for the cmdlet name also matches its aliases, so `PowerShell(Get-ChildItem *)` matches `gci`, `ls`, and `dir` as well. Matching is case-insensitive."
  - Claude Code parses the PowerShell AST and checks each command in a compound statement independently. Pipeline `|`, statement separators `;`, and chain operators `&&`/`||` split compound commands.
  - `acceptEdits` mode now also auto-approves `Set-Content`, `Add-Content`, `Clear-Content`, and `Remove-Item` on in-scope paths.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md), [Permission Modes](https://code.claude.com/docs/en/permission-modes.md)

### OAuth Login Improvements for WSL2, SSH, and Containers

- **OAuth troubleshooting section expanded**: The troubleshoot-install guide section was renamed from "OAuth login fails in WSL2" → "OAuth login fails in WSL2, SSH, or containers" and substantially rewritten.
  > "When Claude Code runs in WSL2, on a remote machine over SSH, or inside a container, the browser usually opens on a different host and its redirect can't reach Claude Code's local callback server. After you sign in, the browser shows a login code instead of redirecting back automatically. Paste that code into the terminal at the `Paste code here if prompted` prompt to complete login."
  - Authentication page updated: "This happens when the browser can't reach Claude Code's local callback server, which is common in WSL2, SSH sessions, and containers."
  - *Implication*: Remote-development and containerized workflows now have documented, working OAuth flows without needing API key authentication.
  - *Source*: [Troubleshoot Install](https://code.claude.com/docs/en/troubleshoot-install.md), [Authentication](https://code.claude.com/docs/en/authentication.md)

### `Ctrl+L` Behavior Fixed: No Longer Clears Input

- **`Ctrl+L` now only redraws screen**: The key previously cleared the prompt input box; it now only forces a screen redraw and preserves typed text.
  > "Forces a full terminal redraw. Input and conversation history are kept."
  - Keybindings reference updated: `chat:clearInput` description changed from "Clear prompt input and force a full screen redraw" → "Force a full screen redraw, preserving input."
  - Fullscreen page: "The first press redraws the screen and shows a hint" (was "clears the input box and shows a hint").
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md), [Keybindings](https://code.claude.com/docs/en/keybindings.md), [Fullscreen](https://code.claude.com/docs/en/fullscreen.md)

### History Search: New Scope Cycling with `Ctrl+S`

- **`historySearch:cycleScope` action added**: A new keybinding `Ctrl+S` in history search mode cycles the search scope between this session, this project, and all projects.
  > "Change scope: press `Ctrl+S` to cycle between this session, this project, and all projects"
  - New entry in keybindings table: `historySearch:cycleScope` | `Ctrl+S` | Cycle scope: session, project, everywhere
  - *Source*: [Keybindings](https://code.claude.com/docs/en/keybindings.md), [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

### New Environment Variables and Settings

- **`CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`** (newly documented):
  > "Set by host platforms that embed Claude Code and manage model provider routing on its behalf. When set, provider-selection, endpoint, and authentication variables such as `CLAUDE_CODE_USE_BEDROCK`, `ANTHROPIC_BASE_URL`, and `ANTHROPIC_API_KEY` in settings files are ignored so user settings cannot override the host's routing."
  - Also skips the automatic telemetry opt-out for Bedrock/Vertex/Foundry — telemetry follows the standard `DISABLE_TELEMETRY` opt-out instead.
  - *Source*: [Env Vars](https://code.claude.com/docs/en/env-vars.md), [Data Usage](https://code.claude.com/docs/en/data-usage.md)

- **`DISABLE_GROWTHBOOK`** (new):
  > "Set to `1` to disable GrowthBook feature-flag fetching and use code defaults for every flag. Telemetry event logging stays on unless `DISABLE_TELEMETRY` is also set."
  - *Source*: [Env Vars](https://code.claude.com/docs/en/env-vars.md)

- **`preferredNotifChannel`** setting added:
  > Method for task-complete and permission-prompt notifications: `"auto"`, `"terminal_bell"`, `"iterm2"`, `"iterm2_with_bell"`, `"kitty"`, `"ghostty"`, or `"notifications_disabled"`. Default: `"auto"`.
  - Terminal config docs updated: "set [`preferredNotifChannel`] to `"terminal_bell"` to ring the terminal bell instead" for terminals that don't support desktop notifications.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md), [Terminal Config](https://code.claude.com/docs/en/terminal-config.md)

### New `oauth_org_not_allowed` Error Type

- **New error category across hooks and headless events**: `oauth_org_not_allowed` added to the `StopFailure` hook error type and the `api_retry` stream event error field.
  - Hooks and hooks-guide matcher tables: `StopFailure` example values now include `oauth_org_not_allowed`.
  - Headless `api_retry` event: `error` field now lists `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, ...
  - *Implication*: Hooks that dispatch on `StopFailure` can now distinguish org-level OAuth restriction failures from generic auth failures, enabling targeted error handling.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md), [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md), [Headless](https://code.claude.com/docs/en/headless.md)

### OpenTelemetry: `invocation_trigger` on `skill_activated` Events

- **New `invocation_trigger` attribute on `claude_code.skill_activated`**: Indicates how a skill was invoked.
  > "`invocation_trigger`: How the skill was triggered (`"user-slash"`, `"claude-proactive"`, or `"nested-skill"`)"
  - The event now also fires for user-typed `/` slash commands, not only Claude-initiated skill calls.
  - *Implication*: Operators monitoring OTel pipelines can distinguish user-driven from model-driven skill usage.
  - *Source*: [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage.md)

### Subagent Frontmatter: Plugin Subagent Constraints Documented

- **`permissionMode`, `mcpServers`, and `hooks` fields noted as ignored for plugin subagents**:
  > "`permissionMode` … Ignored for plugin subagents"; "`mcpServers` … Ignored for plugin subagents"; "`hooks` … Ignored for plugin subagents"
  - The `bypassPermissions` warning also updated to reflect the new all-paths behavior: "It skips all permission prompts, allowing the subagent to execute operations without approval, including writes to `.git`, `.claude`, `.vscode`, `.idea`, and `.husky`."
  - *Source*: [Sub-Agents](https://code.claude.com/docs/en/sub-agents.md)

---

## Notable Details

- **`CLAUDE_STREAM_IDLE_TIMEOUT_MS` description simplified**: Previously described separate defaults for byte-level and event-level watchdogs. Now reads: "Default and minimum `300000` (5 minutes) for both the byte-level and event-level watchdogs." The per-watchdog distinction has been removed from the description. — *Source*: [Env Vars](https://code.claude.com/docs/en/env-vars.md)

- **Analytics cross-links monitoring for per-user costs**: "For per-user token counts and cost estimates, configure [OpenTelemetry export](/en/monitoring-usage)." Added to the contribution metrics section. — *Source*: [Analytics](https://code.claude.com/docs/en/analytics.md)

- **Commands page clarifies slash-command parsing**: "A command is only recognized at the start of your message. Text that follows the command name is passed to it as arguments." Previously undocumented behavior. — *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

- **Setup/uninstall now mentions conflicting installations**: "If `claude` still runs afterward, you likely have a second installation or a leftover shell alias from an older installer." Links to the troubleshooting section. — *Source*: [Setup](https://code.claude.com/docs/en/setup.md)

- **`CLAUDE_CODE_SHELL_PREFIX` scope clarified (third update, May 1)**: The description was rewritten to enumerate exactly which commands the prefix applies to, replacing the vague "all bash commands" phrasing.
  - Before: "Command prefix to wrap all bash commands (for example, for logging or auditing)."
  - After: "Command prefix that wraps shell commands Claude Code spawns: Bash tool calls, hook commands, and stdio MCP server startup commands."
  - *Implication*: Developers using this variable for auditing or sandboxing now have explicit confirmation it covers hook execution and stdio MCP server startup — not just interactive Bash tool calls. Relevant for security-sensitive deployments requiring full command coverage.
  - *Source*: [Env Vars](https://code.claude.com/docs/en/env-vars.md)

- **Two changelog bullets quietly corrected (second update, May 1)**: The v2.1.126 release entry in `changelog.md` was revised:
  - **Removed entirely**: `Fixed blank remote-session transcript when certain messaging tools are unavailable` — this bullet was deleted from the published notes, suggesting the fix was not yet complete or was inaccurate.
  - **Shortened**: The `/remote-control` retry fix was trimmed. The original text read:
    > `Fixed /remote-control retries appearing stuck on "connecting…" — each retry now shows its result, and unenrolled trusted-device failures are caught up-front`

    The clause `and unenrolled trusted-device failures are caught up-front` was removed, indicating that behavior is either shipping separately or was premature to document.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Security fix (v2.1.126)**: "Fixed `allowManagedDomainsOnly` / `allowManagedReadPathsOnly` being ignored when a higher-priority managed-settings source lacked a `sandbox` block." (Changelog entry only.)

- **Large image paste no longer breaks sessions**: Images >2000px are now downscaled on paste; oversized images in history are automatically removed and the request retried. (Changelog entry only.)

- **Read tool malware warnings removed**: "Removed the per-file malware-assessment reminder that could cause spurious refusals and 'this is not malware' commentary on legacy models." (Changelog entry only.)

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +36/−0 (initial); +1/−2 (2nd update) | Added v2.1.126 release notes; two bullets later corrected |
| claude-directory.md | Modified | +34/−1 | New `claude project purge` documentation with examples |
| permissions.md | Modified | +24/−2 | New PowerShell permission rules section; updated `bypassPermissions` warning |
| cli-reference.md | Modified | +22/−21 | Added `claude project purge` entry to command table |
| keybindings.md | Modified | +23/−22 | Updated `chat:clearInput` description; added `historySearch:cycleScope` action |
| hooks.md | Modified | +20/−20 | Added `oauth_org_not_allowed` to `StopFailure` matcher values and `error` field |
| sub-agents.md | Modified | +19/−19 | Documented plugin-subagent field restrictions; updated `bypassPermissions` note |
| hooks-guide.md | Modified | +18/−18 | Added `oauth_org_not_allowed` to `StopFailure` matcher values |
| llm-gateway.md | Modified | +8/−2 | Documented automatic `/v1/models` gateway discovery |
| permission-modes.md | Modified | +6/−4 | Updated `bypassPermissions` description; added PowerShell `acceptEdits` support |
| troubleshoot-install.md | Modified | +6/−6 | Expanded OAuth section to cover SSH and containers |
| env-vars.md | Modified | +4/−2 | Added `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`, `DISABLE_GROWTHBOOK`; simplified `CLAUDE_STREAM_IDLE_TIMEOUT_MS`; clarified `CLAUDE_CODE_SHELL_PREFIX` scope |
| headless.md | Modified | +11/−11 | Added `oauth_org_not_allowed` to `api_retry` error field |
| interactive-mode.md | Modified | +4/−3 | Fixed `Ctrl+L` description; added `Ctrl+S` history scope cycling step |
| terminal-config.md | Modified | +4/−2 | Updated notification docs to reference `preferredNotifChannel` |
| analytics.md | Modified | +2/−0 | Added cross-link to OpenTelemetry for per-user token counts |
| commands.md | Modified | +2/−0 | Clarified that commands must appear at start of message |
| data-usage.md | Modified | +2/−0 | Documented telemetry behavior change for `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST` |
| monitoring-usage.md | Modified | +2/−1 | Added `invocation_trigger` attribute to `skill_activated` OTel event |
| authentication.md | Modified | +1/−1 | Added WSL2/SSH/container context to OAuth code-paste explanation |
| fullscreen.md | Modified | +1/−1 | Corrected `Ctrl+L` first-press behavior description |
| model-config.md | Modified | +1/−1 | Updated `ANTHROPIC_CUSTOM_MODEL_OPTION` to reflect gateway auto-discovery |
| settings.md | Modified | +1/−0 | Added `preferredNotifChannel` to settings reference |
| setup.md | Modified | +1/−1 | Added conflicting-installations hint to uninstall section |
| tools-reference.md | Modified | +1/−1 | Clarified PowerShell is primary shell when tool is enabled |

---

*Generated from Claude Code CLI documentation changes detected on 2026-05-01*
