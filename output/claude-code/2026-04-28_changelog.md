# Claude Code Documentation Changes — 2026-04-28

## Summary

Two releases shipped on April 28, 2026: **v2.1.120** and **v2.1.121**. The most significant changes are Windows dropping the Git for Windows hard requirement (PowerShell is now a fallback shell), a new `claude ultrareview` non-interactive subcommand for CI use, the `claude plugin prune` command for dependency cleanup, and expanded PostToolUse hook capabilities that now allow replacing output from any built-in tool (previously MCP-only). 29 documentation pages were modified across features, configuration, integrations, and troubleshooting.

---

## Significant Changes

### Features & New Commands

- **`claude ultrareview [target]` subcommand**: New CLI command to run `/ultrareview` non-interactively from CI or scripts. Blocks until the remote review finishes, prints findings to stdout, exits 0 on success or 1 on failure.
  > "Use the `claude ultrareview` subcommand to start an ultrareview from CI or a script without an interactive session. The subcommand launches the same review as `/ultrareview`, blocks until the remote review finishes, prints the findings to stdout, and exits with code 0 on success or 1 on failure."
  > "Without arguments, the subcommand reviews the diff between your current branch and the default branch. Pass a PR number to review a pull request, or pass a base branch to review the diff against that branch instead."
  - Supports `--json` for raw `bugs.json` payload, `--timeout <minutes>` to override the 30-minute default; progress messages go to stderr.
  - Exit codes: 0 on completion (with or without findings), 1 on launch failure/timeout, 130 on Ctrl-C. The remote review continues running if you interrupt the client.
  - *Source*: [ultrareview.md](https://code.claude.com/docs/en/ultrareview.md), [cli-reference.md](https://code.claude.com/docs/en/cli-reference.md)

- **`claude plugin prune` command**: New command to remove orphaned auto-installed plugin dependencies. Only removes dependencies that Claude Code pulled in automatically; plugins you installed directly are never touched.
  > "Run `claude plugin prune` to list the auto-installed dependencies that no longer have any installed plugin requiring them and remove them after a confirmation prompt."
  - Options: `--scope <user|project|local>`, `--dry-run`, `-y` to skip confirmation. Alias: `autoremove`.
  - `claude plugin uninstall <plugin> --prune` also cascades cleanup in a single step.
  - *Implication*: Addresses disk accumulation from plugins that have been removed but left behind their auto-pulled dependencies.
  - *Source*: [plugins-reference.md](https://code.claude.com/docs/en/plugins-reference.md), [plugin-dependencies.md](https://code.claude.com/docs/en/plugin-dependencies.md)

- **`alwaysLoad` option for MCP servers**: A new per-server config flag that bypasses tool-search deferral, loading all of that server's tools into context at session start.
  > "If a server's tools should always be visible to Claude without a search step, set `alwaysLoad` to `true` in that server's configuration. Every tool from that server then loads into context at session start regardless of the `ENABLE_TOOL_SEARCH` setting."
  ```json
  {
    "mcpServers": {
      "core-tools": {
        "type": "http",
        "url": "https://mcp.example.com/mcp",
        "alwaysLoad": true
      }
    }
  }
  ```
  - Individual tools can also be marked always-loaded by including `"anthropic/alwaysLoad": true` in the tool's `_meta` object.
  - *Implication*: Allows mixing deferred and eager tool loading in the same session; use sparingly since each upfront tool consumes context.
  - *Source*: [mcp.md](https://code.claude.com/docs/en/mcp.md)

- **`${CLAUDE_EFFORT}` skill placeholder**: Skills can now reference the current effort level dynamically.
  > "The current effort level: `low`, `medium`, `high`, `xhigh`, or `max`. Use this to adapt skill instructions to the active effort setting."
  - *Source*: [skills.md](https://code.claude.com/docs/en/skills.md)

- **`hideVimModeIndicator` statusline field**: New optional field that suppresses the built-in `-- INSERT --` text when your status line script renders `vim.mode` itself.
  > "The optional `hideVimModeIndicator` field suppresses the built-in `-- INSERT --` text below the prompt. Set this to `true` when your script renders `vim.mode` itself, so the mode is not shown twice."
  - *Source*: [statusline.md](https://code.claude.com/docs/en/statusline.md)

---

### Hooks

- **`updatedToolOutput` expands to all built-in tools**: PostToolUse hooks can now replace the output of any tool, not just MCP tools. The old `updatedMCPToolOutput` field is now deprecated in favor of the new `updatedToolOutput` field.
  > "Replaces the tool's output with the provided value before it is sent to Claude. The value must match the tool's output shape."
  > "`updatedMCPToolOutput` — Replaces the output for MCP tools only. Prefer `updatedToolOutput`, which works for all tools."
  - The replacement value must match the tool's output schema (e.g., `Bash` requires `stdout`, `stderr`, `interrupted`, `isImage`). A non-matching value for a built-in tool is silently ignored and the original output is used. MCP tools pass through without schema validation.
  - *Implication*: Enables output redaction, transformation, or injection for built-in Bash, file, and other tool calls from a hook script.
  - **Warning**: `updatedToolOutput` changes only what Claude sees; the tool has already executed. OpenTelemetry spans and analytics capture the original output before the hook fires.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md)

---

### Platform: Windows

- **Git for Windows is now optional**: Claude Code on native Windows no longer requires Git for Windows. When it is absent, Claude Code uses PowerShell as the shell tool instead.
  > "[Git for Windows](https://git-scm.com/downloads/win) is recommended on native Windows so Claude Code can use the Bash tool. If Git for Windows is not installed, Claude Code uses PowerShell as the shell tool instead. WSL setups do not need Git for Windows."
  - The troubleshooting entry for `Claude Code on Windows requires git-bash` has been updated to reflect the new error message: `Claude Code on Windows requires either Git for Windows (for bash) or PowerShell`.
  - The PowerShell tool limitations note that previously said "Git Bash is still required to start Claude Code" has been removed.
  - *Implication*: Windows environments without Git can now run Claude Code using PowerShell. Bash tool features (shell history, certain glob behaviors) remain available only when Git Bash is present.
  - *Source*: [setup.md](https://code.claude.com/docs/en/setup.md), [troubleshooting.md](https://code.claude.com/docs/en/troubleshooting.md), [overview.md](https://code.claude.com/docs/en/overview.md), [tools-reference.md](https://code.claude.com/docs/en/tools-reference.md)

---

### Integrations

- **Vertex AI: X.509 certificate-based Workload Identity Federation**: Claude Code v2.1.121+ supports mTLS ADC via the standard Application Default Credentials chain.
  > "Claude Code v2.1.121 or later supports X.509 certificate-based Workload Identity Federation through the same Application Default Credentials chain. Set `GOOGLE_APPLICATION_CREDENTIALS` to the path of your credential configuration file."
  - *Source*: [google-vertex-ai.md](https://code.claude.com/docs/en/google-vertex-ai.md)

- **Amazon Bedrock: `bedrock:GetInferenceProfile` IAM permission documented**: New IAM action added to the recommended policy, with a description of the fallback behavior if it is missing.
  > "`bedrock:GetInferenceProfile` lets Claude Code resolve an application inference profile ARN to its backing foundation model, which is used to select the correct request shape for that model."
  > "If the token is missing this permission, Claude Code recovers automatically by retrying once with the alternate shape, so requests still succeed but each new model adds an extra round-trip. Granting the permission avoids the retry. This applies most often to `AWS_BEARER_TOKEN_BEDROCK` deployments, where the token's policy is typically narrower than a full IAM role."
  - *Source*: [amazon-bedrock.md](https://code.claude.com/docs/en/amazon-bedrock.md)

- **Cloud sessions and organization IP allowlists**: New constraint documented for Claude Code on the Web, Code Review, and Routines.
  > "Organization IP allowlist: cloud sessions call the Anthropic API from Anthropic-managed infrastructure, not your network. If your organization has IP allowlisting enabled, every cloud session fails with an authentication error. The same applies to Code Review and Routines. Contact Anthropic support to exempt Anthropic-hosted services from your organization's IP allowlist."
  - *Source*: [claude-code-on-the-web.md](https://code.claude.com/docs/en/claude-code-on-the-web.md)

---

### OpenTelemetry / Monitoring

- **New `stop_reason` and `gen_ai.response.finish_reasons` span attributes**: Added to the `claude_code.llm_request` span on LLM requests.
  > "`stop_reason` — API response `stop_reason`, such as `end_turn`, `tool_use`, `max_tokens`, `stop_sequence`, `pause_turn`, or `refusal`"
  > "`gen_ai.response.finish_reasons` — Same value as `stop_reason`, wrapped in a string array. OpenTelemetry GenAI semantic convention"
  - *Source*: [monitoring-usage.md](https://code.claude.com/docs/en/monitoring-usage.md)

- **`user_system_prompt` attribute in detailed beta tracing**: A new content-bearing attribute emitted once per session (not per request) when both detailed beta tracing and `OTEL_LOG_USER_PROMPTS=1` are active.
  > "`user_system_prompt` additionally requires `OTEL_LOG_USER_PROMPTS=1`. It carries only the system prompt text you provide via the `systemPrompt` SDK option or `--system-prompt` and `--append-system-prompt` flags, truncated at 60 KB, and is emitted once per session rather than per request."
  - *Source*: [monitoring-usage.md](https://code.claude.com/docs/en/monitoring-usage.md)

---

### Data Usage

- **Session quality survey: optional transcript upload follow-up documented**: The data usage page now describes a two-step survey flow. After rating, users may see a separate follow-up asking to share their session transcript.
  > "After the rating prompt, you may see a separate follow-up asking 'Can Anthropic look at your session transcript to help us improve Claude Code?'... **Yes**: uploads your conversation transcript, any subagent transcripts, and the raw session log file from disk to Anthropic. Known API key and token patterns are redacted before upload. Source code, file contents, and other conversation content are uploaded as-is. Shared transcripts are retained for up to 6 months."
  - Organizations with zero data retention or disabled product feedback never see this follow-up.
  - *Implication*: Developers should be aware that opting in explicitly shares full conversation content; nothing is uploaded without an explicit **Yes**.
  - *Source*: [data-usage.md](https://code.claude.com/docs/en/data-usage.md)

---

### Configuration

- **`CLAUDE_CODE_FORK_SUBAGENT` now works in non-interactive mode**: The env var previously enabled fork mode only in interactive sessions; it now also applies to the SDK and `claude -p`.
  > "Works in interactive mode and via the SDK or `claude -p`"
  - The sub-agents page limitation note has been updated: "Setting `CLAUDE_CODE_FORK_SUBAGENT=1` enables fork mode in interactive sessions, non-interactive mode, and the Agent SDK."
  - *Source*: [env-vars.md](https://code.claude.com/docs/en/env-vars.md), [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md)

- **`CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT` scoped to Opus 4.7 only**: The description of this env var has changed substantially — it no longer claims to replicate `CLAUDE_CODE_SIMPLE` behavior on any model.
  > "Set to `1` to use a shorter system prompt and abbreviated tool descriptions on Opus 4.7. Has no effect on other models. The full tool set, hooks, MCP servers, and CLAUDE.md discovery remain enabled."
  - *Implication*: Teams using this variable with non-Opus-4.7 models should expect no effect.
  - *Source*: [env-vars.md](https://code.claude.com/docs/en/env-vars.md)

- **Server-managed settings bypass list expanded**: The table row for third-party provider bypass was broadened from just `ANTHROPIC_BASE_URL` to include `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_MANTLE`, `CLAUDE_CODE_USE_VERTEX`, and `CLAUDE_CODE_USE_FOUNDRY`.
  > "User configures a third-party model provider — Server-managed settings are bypassed. This includes setting `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_MANTLE`, `CLAUDE_CODE_USE_VERTEX`, `CLAUDE_CODE_USE_FOUNDRY`, or a non-default `ANTHROPIC_BASE_URL`"
  - *Source*: [server-managed-settings.md](https://code.claude.com/docs/en/server-managed-settings.md)

---

### Plugin System

- **`$schema` field now accepted in `plugin.json` and `marketplace.json`**: Both manifest files now officially support a `$schema` field for editor autocomplete and JSON Schema validation. Claude Code ignores the field at load time.
  - `marketplace.json` also now accepts top-level `description` and `version` (previously only under `metadata`); `metadata.description` and `metadata.version` remain accepted for backward compatibility.
  > "`description` and `version` are also accepted under `metadata` for backward compatibility."
  - *Source*: [plugins-reference.md](https://code.claude.com/docs/en/plugins-reference.md), [plugin-marketplaces.md](https://code.claude.com/docs/en/plugin-marketplaces.md)

---

### Interactive Mode / Terminal

- **"Bash mode" renamed to "Shell mode"**: The `!` prefix mode in the interactive prompt is now referred to as "Shell mode" throughout the documentation, reflecting that it now runs in PowerShell on systems without Git Bash.
  - *Source*: [interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md)

- **iTerm2 clipboard and bypass modifier documented**: The fullscreen mouse capture page now documents two improvements:
  1. The Option modifier in iTerm2 (or Shift in Linux/Windows terminals) lets you temporarily bypass Claude Code's mouse capture for native selection without disabling it globally.
  2. `/terminal-setup` now enables iTerm2's "Applications in terminal may access clipboard" setting automatically.
  > "For a one-off native selection, hold your terminal's bypass modifier while you click and drag: `Option` in iTerm2, or `Shift` in most Linux and Windows terminals."
  - *Source*: [fullscreen.md](https://code.claude.com/docs/en/fullscreen.md), [terminal-config.md](https://code.claude.com/docs/en/terminal-config.md)

- **VS Code voice dictation respects `accessibility.voice.speechLanguage`**: When the Claude Code `language` setting is empty, the VS Code extension now falls back to VS Code's own voice speech language setting before defaulting to English.
  > "In the VS Code extension, if `language` is empty, dictation uses VS Code's `accessibility.voice.speechLanguage` setting before defaulting to English."
  - *Source*: [voice-dictation.md](https://code.claude.com/docs/en/voice-dictation.md)

---

### MCP

- **MCP startup auto-retry documented**: As of v2.1.121, HTTP/SSE servers that fail their initial connection at startup are retried up to three times (transient errors only; auth/404 errors are not retried).
  > "As of v2.1.121, Claude Code retries the initial connection up to three times on transient errors such as a 5xx response, a connection refused, or a timeout, then marks the server as failed if it still cannot connect. Authentication and not-found errors are not retried because they require a configuration change to resolve."
  - *Source*: [mcp.md](https://code.claude.com/docs/en/mcp.md)

---

## Notable Details

- **HackerOne vulnerability reporting URL changed**: Both `security.md` and `legal-and-compliance.md` updated the HackerOne link from a team-report URL to an embedded submission form URL (`/4f1f16ba-10d3-4d09-9ecc-c721aad90f24/embedded_submissions/new`). Developers with bookmarked links should update them.
- **Troubleshooting: Homebrew no longer recommended as an architecture mismatch workaround**: The troubleshooting section for `Illegal instruction` on Linux now states "Alternative install methods download the same architecture-specific binary and won't resolve this error," removing the previous suggestion to try `brew install --cask claude-code` as a workaround.
- **MCP per-tool `alwaysLoad`**: Individual tools can be exempt from deferral via `"anthropic/alwaysLoad": true` in the tool's `_meta` object — a server-side option that plugin/server authors can use independently of the client-side server-level `alwaysLoad` config.
- **`claude plugin prune` aliases `autoremove`**: Consistent with apt/yum conventions, making it familiar for users coming from Linux package managers.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +67/-0 | Release notes for v2.1.120 and v2.1.121 |
| plugins-reference.md | Modified | +42/-14 | Added `plugin prune` command; `plugin uninstall --prune` option; `$schema` field in plugin manifest |
| ultrareview.md | Modified | +21/-0 | New section: `claude ultrareview` non-interactive subcommand |
| hooks.md | Modified | +22/-9 | `updatedToolOutput` field for all tools in PostToolUse; updated example and warning |
| mcp.md | Modified | +22/-0 | New `alwaysLoad` server config option; startup auto-retry documented |
| monitoring-usage.md | Modified | +25/-23 | Added `stop_reason`, `gen_ai.response.finish_reasons`, `user_system_prompt` span attributes |
| plugin-dependencies.md | Modified | +18/-0 | New section: `claude plugin prune` for orphaned dependencies |
| data-usage.md | Modified | +9/-1 | Two-step session survey with optional transcript upload now documented |
| amazon-bedrock.md | Modified | +6/-1 | `bedrock:GetInferenceProfile` IAM permission added and explained |
| plugin-marketplaces.md | Modified | +6/-3 | Top-level `$schema`, `description`, `version` now accepted in `marketplace.json` |
| troubleshooting.md | Modified | +14/-21 | Windows shell error updated for PowerShell fallback; Homebrew workaround removed |
| setup.md | Modified | +8/-8 | Git for Windows now optional on native Windows; PowerShell fallback documented |
| server-managed-settings.md | Modified | +7/-7 | Third-party provider bypass list expanded to include Bedrock/Vertex/Foundry/Mantle env vars |
| google-vertex-ai.md | Modified | +2/-0 | X.509 certificate-based Workload Identity Federation (mTLS ADC) documented |
| fullscreen.md | Modified | +4/-2 | iTerm2 clipboard access note; bypass modifier for native selection documented |
| env-vars.md | Modified | +2/-2 | `CLAUDE_CODE_FORK_SUBAGENT` now works in SDK/`-p`; `CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT` scoped to Opus 4.7 |
| cli-reference.md | Modified | +21/-20 | `claude ultrareview [target]` command added to reference table |
| interactive-mode.md | Modified | +5/-5 | "Bash mode" renamed to "Shell mode" throughout |
| sub-agents.md | Modified | +2/-2 | Fork mode limitations updated: now works in non-interactive/SDK mode |
| statusline.md | Modified | +2/-0 | `hideVimModeIndicator` field documented |
| terminal-config.md | Modified | +2/-0 | `/terminal-setup` iTerm2 clipboard setup behavior documented |
| skills.md | Modified | +1/-0 | `${CLAUDE_EFFORT}` placeholder added |
| voice-dictation.md | Modified | +1/-1 | VS Code extension falls back to `accessibility.voice.speechLanguage` |
| claude-code-on-the-web.md | Modified | +1/-0 | Organization IP allowlist constraint for cloud sessions documented |
| overview.md | Modified | +1/-1 | Windows Git for Windows changed from required to recommended |
| quickstart.md | Modified | +1/-1 | Same Windows Git for Windows language change |
| tools-reference.md | Modified | +0/-1 | Removed note that Git Bash is required to start Claude Code on Windows |
| security.md | Modified | +1/-1 | HackerOne report URL updated |
| legal-and-compliance.md | Modified | +1/-1 | HackerOne report URL updated |

---

*Generated from Claude Code CLI documentation changes detected on 2026-04-28*
