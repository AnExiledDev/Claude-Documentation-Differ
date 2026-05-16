# Claude Code Documentation Changes — 2026-05-16

## Summary

Version 2.1.143 (May 15, 2026) was released with substantial additions to plugin management, background session control, and PowerShell integration. The `/feedback` command gained third-party provider support via local archive saving, and MCP tool search on Vertex AI was expanded to support Claude Sonnet 4.5+ and Opus 4.5+ models. Seven documentation pages were modified; no pages were added or removed.

---

## Significant Changes

### Version 2.1.143 Release

The official changelog page records the 2.1.143 release across four major areas:

#### Plugin Management

- **Plugin dependency enforcement**: `claude plugin disable` now refuses to disable a plugin when another enabled plugin depends on it, and provides a copy-pasteable disable-chain hint. `claude plugin enable` force-enables transitive dependencies.
  > `claude plugin disable` now refuses when another enabled plugin depends on the target (with a copy-pasteable disable-chain hint), and `claude plugin enable` force-enables transitive dependencies
  - *Implication*: Plugin graphs are now guarded against accidental breakage; order of disable operations is enforced automatically.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Plugin marketplace cost display**: The `/plugin` marketplace browse pane now shows projected context cost (per-turn and per-invocation token estimates) before you install a plugin.
  > Added projected context cost (per-turn and per-invocation token estimates) to the `/plugin` marketplace browse pane
  - *Implication*: Developers can make informed decisions about plugin context overhead before enabling them.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

#### Background Sessions & Agents

- **`worktree.bgIsolation: "none"` setting**: New setting that lets background sessions edit the working copy directly without `EnterWorktree`, for repositories where worktrees are impractical.
  > Added `worktree.bgIsolation: "none"` setting to let background sessions edit the working copy directly without `EnterWorktree`, for repos where worktrees are impractical
  - *Implication*: Teams that cannot use Git worktrees (e.g., monorepos with complex tooling) can still use background sessions.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Expanded `claude agents` CLI flags**: `claude agents` now accepts `--add-dir`, `--settings`, `--mcp-config`, `--plugin-dir`, `--permission-mode`, `--model`, `--effort`, and `--dangerously-skip-permissions`, applying them to the dashboard and to background sessions it dispatches.
  > `claude agents` now accepts `--add-dir`, `--settings`, `--mcp-config`, and `--plugin-dir` and applies them to the dashboard and to background sessions dispatched from it
  - *Implication*: The agent dashboard can now be fully configured at launch, making scripted or CI-driven agent setups more practical.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/bg` flag preservation**: `/bg` and `←`-detach now preserve `--mcp-config`, `--settings`, `--add-dir`, `--plugin-dir`, `--strict-mcp-config`, `--fallback-model`, and `--allow-dangerously-skip-permissions` across session respawn and retire→wake cycles.
  > `/bg` now preserves `--mcp-config`, `--settings`, `--add-dir`, `--plugin-dir`, and `--strict-mcp-config`, so backgrounded sessions keep their MCP servers and settings across respawn.
  - *Implication*: Background workers no longer lose configuration on respawn; essential for long-running autonomous tasks.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`permissions.defaultMode` honored by `claude agents`**: Background sessions launched from `claude agents` now respect `permissions.defaultMode` from `settings.json`; previously this was overridden to auto mode.
  > Background sessions launched from `claude agents` now honor `permissions.defaultMode` from settings.json (was previously overridden to auto mode)
  - *Implication*: Enterprise deployments that set a restrictive default permission mode can now enforce it across all agent sessions.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

#### PowerShell

- **`-ExecutionPolicy Bypass` now default**: The PowerShell tool now passes `-ExecutionPolicy Bypass` automatically. Opt out by setting `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1`.
  > PowerShell tool now passes `-ExecutionPolicy Bypass`. Opt out with `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1`
  - *Implication*: Scripts that were silently skipped due to restrictive execution policies will now run; teams with enforced policies should set the opt-out variable.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **PowerShell tool enabled by default on Windows for third-party providers**: Now on by default for Bedrock, Vertex, and Foundry users on Windows. Opt out with `CLAUDE_CODE_USE_POWERSHELL_TOOL=0`.
  > The PowerShell tool is now enabled by default on Windows for Bedrock, Vertex, and Foundry users. Opt out with `CLAUDE_CODE_USE_POWERSHELL_TOOL=0`.
  - *Implication*: Windows users on these providers get native PowerShell scripting capability without manual configuration.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

#### Bug Fixes (2.1.143)

Fourteen bugs were fixed in this release. Notable ones include:

- **Stop hook infinite loop cap**: Stop hooks that block repeatedly no longer loop forever — the turn now ends with a warning after 8 consecutive blocks. Override via `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`.
- **`NO_COLOR`/`FORCE_COLOR` scoping fixed**: These env vars in `settings.json`'s `env` block now apply to subprocesses only, not to Claude Code's own UI colors.
- **Worktree cleanup safety**: Cleanup no longer falls back to `rm -rf` when `git worktree remove` fails, preventing loss of gitignored or in-progress files.
- **macOS full disk access fix**: Background sessions on macOS no longer get "Operation not permitted" errors reading `~/Documents`, `~/Desktop`, or `~/Downloads` even with Full Disk Access granted.
- **`--agent <name>` prefix fix**: `--agent <name>` now finds plugin-contributed agents without requiring the `plugin:` prefix.
- **False-positive stall detection**: Background agent worker-stall detection no longer fires spuriously after host sleep or macOS App Nap.
- *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

### `/feedback` Command — Third-Party Provider Support

The `/feedback` command now works on Bedrock, Vertex AI, Foundry, and other third-party provider deployments by saving a redacted local archive instead of sending data to Anthropic directly.

> When you use a third-party provider such as Bedrock or Vertex, or have no Anthropic credentials configured, `/feedback` writes the report to a local archive under `~/.claude/feedback-bundles/` instead of sending it to Anthropic. Known API key and token patterns are redacted before the archive is written. Nothing leaves your machine until you send that file to your Anthropic account representative or attach it to a support request.

Additionally, the command now allows choosing the history scope before submission:

> Before submitting, you choose how much history to include: the current session only, which is the default, or also other sessions from the same project over the last 24 hours or 7 days.

- *Implication*: Enterprise and cloud-provider users who previously had no way to submit feedback can now generate redacted bundles for their account team. The scoping control reduces accidental over-sharing of unrelated session history.
- *Source*: [Data Usage](https://code.claude.com/docs/en/data-usage.md), [Errors](https://code.claude.com/docs/en/errors.md), [Claude Directory](https://code.claude.com/docs/en/claude-directory.md)

---

### MCP Tool Search — Vertex AI Model Version Clarification

MCP tool search support on Vertex AI is no longer a blanket "disabled by default and unsupported" — it is now enabled for specific model versions.

**Previous documentation:**
> MCP tool search is disabled by default on Vertex AI because the endpoint does not accept the required beta header. All MCP tool definitions load upfront instead. Setting `ENABLE_TOOL_SEARCH=true` forces Claude Code to send the header anyway, which causes Vertex AI to reject requests.

**Updated documentation:**
> Claude Code disables MCP tool search by default on Vertex AI, so MCP tool definitions load upfront. Vertex AI supports tool search for Claude Sonnet 4.5 and later and Claude Opus 4.5 and later. Set `ENABLE_TOOL_SEARCH=true` to enable it on those models. Earlier models on Vertex AI do not accept the required beta header, and requests fail if you enable tool search with them.

The `ENABLE_TOOL_SEARCH=true` entry in the env-vars table was also updated to reflect this:
> supported on Vertex AI with Sonnet 4.5 and later or Opus 4.5 and later; requests fail on earlier Vertex AI models or on proxies that do not support `tool_reference`

- *Implication*: Vertex AI users on Sonnet 4.5+ or Opus 4.5+ can now enable MCP tool search to defer tool loading; users on older model versions must keep `ENABLE_TOOL_SEARCH` unset or `false`.
- *Source*: [MCP](https://code.claude.com/docs/en/mcp.md), [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai.md), [Env Vars](https://code.claude.com/docs/en/env-vars.md)

---

### `~/.claude/feedback-bundles/` Directory Added

The `~/.claude/` directory reference table gained a new row documenting the `feedback-bundles/` path:

> `feedback-bundles/` — Redacted transcript archives written by `/feedback` on third-party providers, for sending to your Anthropic account team

- *Implication*: Operators auditing the `~/.claude/` directory now have a documented entry for these archive files.
- *Source*: [Claude Directory](https://code.claude.com/docs/en/claude-directory.md)

---

## Minor Changes

- **errors.md**: Replaced "unavailable on your provider" with "unavailable in your environment" in two places, and updated the description of `/feedback` unavailability from "Feedback is unavailable on Bedrock, Vertex AI, and Foundry deployments" to "On Bedrock, Vertex AI, Foundry, and other third-party providers, `/feedback` saves a local archive you can send to your Anthropic account representative instead." (+3/-3 lines)

- **env-vars.md**: `ENABLE_TOOL_SEARCH=true` description clarified to note Vertex AI support for Sonnet 4.5+/Opus 4.5+ and failure on earlier models (+1/-1 lines)

- **google-vertex-ai.md**: MCP tool search paragraph updated to reflect Vertex AI model version support for Sonnet 4.5+/Opus 4.5+ (+1/-1 lines)

---

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| changelog.md | Modified | SIGNIFICANT | +36/-0 | Version 2.1.143 release entry added |
| claude-directory.md | Modified | SIGNIFICANT | +14/-13 | Added `feedback-bundles/` directory row; table reformatted |
| mcp.md | Modified | SIGNIFICANT | +10/-8 | MCP tool search Vertex AI model version clarifications; table updated |
| errors.md | Modified | SIGNIFICANT | +3/-3 | `/feedback` wording updated to reflect third-party provider archive support |
| data-usage.md | Modified | MINOR | +3/-1 | `/feedback` history scoping and third-party provider behavior documented |
| env-vars.md | Modified | MINOR | +1/-1 | `ENABLE_TOOL_SEARCH` Vertex AI model version support clarified |
| google-vertex-ai.md | Modified | MINOR | +1/-1 | MCP tool search model version support clarified for Vertex AI |

---

*Generated from Claude Code CLI documentation changes detected on 2026-05-16*
