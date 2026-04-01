# Claude Code Documentation Changes — 2026-04-01

## Summary

22 pages were modified across the Claude Code documentation, with no new or removed pages. The most substantive updates are a large expansion of the environment variables reference (~62 net new lines), clarification of what `--add-dir` does and does not configure, new tooling reference sections for LSP behavior and tool discovery, new CLI flags, and refined guidance on hooks and managed settings precedence. The upstream changelog entry for version 2.1.88 was removed from the docs changelog (it has now scrolled off the visible top of the page).

## Significant Changes

### CLI Flags

- **`--agent-teams` flag added**: A new explicit flag `--agent-teams` enables the experimental agent teams feature, equivalent to setting `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. This makes `SendMessage`, `TeamCreate`, and `TeamDelete` tools available without setting the environment variable.
  > `--agent-teams` Enable experimental [agent teams](/en/agent-teams). Makes the `SendMessage`, `TeamCreate`, and `TeamDelete` tools available.
  - *Implication*: Teams using agent teams in scripts can now enable the feature via a flag rather than an env var.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **`--debug-file <path>` flag added**: Writes debug logs to a specific file path and implicitly enables debug mode in one step. Takes precedence over `CLAUDE_CODE_DEBUG_LOGS_DIR`.
  > Takes precedence over `CLAUDE_CODE_DEBUG_LOGS_DIR`
  - *Implication*: Simplifies debug log capture in CI or scripted environments — no need to separately enable `--debug`.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **`--replay-user-messages` flag added**: Re-emits user messages from stdin back on stdout for acknowledgment. Requires `--print`, `--input-format stream-json`, `--output-format stream-json`, and `--verbose`.
  - *Implication*: Useful for SDK integrations that need to confirm receipt of user messages in the stream.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **`--include-partial-messages` requirement tightened**: Now also requires `--verbose` in addition to `--print` and `--output-format stream-json` (previously only required the latter two).
  > Requires `--print`, `--output-format stream-json`, and `--verbose`
  - *Implication*: Scripts using `--include-partial-messages` without `--verbose` will now need to add that flag.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **`--add-dir` description clarified**: The description now explicitly states that `--add-dir` grants file access but most `.claude/` configuration is not discovered from added directories.
  > Add additional working directories for Claude to read and edit files. Grants file access; most `.claude/` configuration is [not discovered] from these directories.
  - *Implication*: This is a documentation-only change; behavior is unchanged, but users expecting hooks or subagents from `--add-dir` paths will now see a clear explanation.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

### Environment Variables

The env vars reference gained approximately 30 new entries and updated descriptions on ~15 existing ones. Key additions:

- **`ANTHROPIC_BEDROCK_BASE_URL`** and **`ANTHROPIC_VERTEX_BASE_URL`**: Override the endpoint URL for Bedrock and Vertex respectively, enabling LLM gateway routing for both providers.
- **`ANTHROPIC_BETAS`**: Comma-separated list of additional `anthropic-beta` header values, and unlike the `--betas` flag, this works with all auth methods including Claude.ai subscriptions.
- **`API_TIMEOUT_MS`**: Controls API request timeout (default: 600000ms / 10 minutes).
- **`CLAUDE_CODE_OAUTH_REFRESH_TOKEN`** / **`CLAUDE_CODE_OAUTH_TOKEN`** / **`CLAUDE_CODE_OAUTH_SCOPES`**: Enable non-interactive OAuth authentication, useful for provisioning automated environments.
- **`CLAUDE_CODE_DEBUG_LOGS_DIR`** and **`CLAUDE_CODE_DEBUG_LOG_LEVEL`**: Fine-grained debug log configuration. Note: `CLAUDE_CODE_DEBUG_LOGS_DIR` sets a file path (not a directory) and requires debug mode to be separately enabled.
- **`CLAUDE_CODE_RESUME_INTERRUPTED_TURN`**: For SDK mode; automatically resumes if the previous session ended mid-turn.
- **`CLAUDE_ENABLE_STREAM_WATCHDOG`**: Enables a 90-second idle stream watchdog. `CLAUDE_STREAM_IDLE_TIMEOUT_MS` now requires this to be set — previously the watchdog appeared to be always-on.
- **`DISABLE_AUTO_COMPACT`** and **`DISABLE_COMPACT`**: Two new separate controls — one disables only automatic compaction (manual `/compact` still works), the other disables all compaction.
- **`DISABLE_DOCTOR_COMMAND`**, **`DISABLE_EXTRA_USAGE_COMMAND`**, **`DISABLE_INSTALL_GITHUB_APP_COMMAND`**, **`DISABLE_LOGIN_COMMAND`**, **`DISABLE_LOGOUT_COMMAND`**, **`DISABLE_UPGRADE_COMMAND`**: New variables for hiding individual commands, useful for managed deployments.
- **`CLAUDE_CODE_GLOB_HIDDEN`**, **`CLAUDE_CODE_GLOB_NO_IGNORE`**, **`CLAUDE_CODE_GLOB_TIMEOUT_SECONDS`**: New controls for Glob tool behavior.
- **`OTEL_LOG_TOOL_CONTENT`**, **`OTEL_LOG_TOOL_DETAILS`**, **`OTEL_LOG_USER_PROMPTS`**, **`OTEL_METRICS_INCLUDE_ACCOUNT_UUID`**, **`OTEL_METRICS_INCLUDE_SESSION_ID`**, **`OTEL_METRICS_INCLUDE_VERSION`**: New fine-grained OpenTelemetry output controls.
- **`VERTEX_REGION_CLAUDE_4_5_SONNET`**, **`VERTEX_REGION_CLAUDE_4_6_SONNET`**, **`VERTEX_REGION_CLAUDE_HAIKU_4_5`**, **`VERTEX_REGION_CLAUDE_3_5_SONNET`**: New per-model Vertex regional override variables.
- **Several env vars standardized from `true`/`false` to `1`**: `FORCE_AUTOUPDATE_PLUGINS`, `CLAUDE_CODE_PROXY_RESOLVES_HOSTS`, `CLAUDE_CODE_ENABLE_TASKS`, `CLAUDE_CODE_NEW_INIT`, and `IS_DEMO` all moved from `true` to `1` as the documented value.
- **`CLAUDE_CONFIG_DIR`**: Description expanded to include an example usage for running multiple accounts side-by-side.
- *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

### Permissions

- **`--add-dir` grants file access only, not configuration**: A new section explicitly documents what is and isn't loaded from directories added via `--add-dir`.
  > Adding a directory extends where Claude can read and edit files. It does not make that directory a full configuration root: most `.claude/` configuration is not discovered from additional directories, though a few types are loaded as exceptions.

  The documented exceptions are:
  | Configuration | Loaded from `--add-dir` |
  |---|---|
  | Skills in `.claude/skills/` | Yes, with live reload |
  | Plugin settings `enabledPlugins` / `extraKnownMarketplaces` | Yes |
  | CLAUDE.md / `.claude/rules/` | Only with `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` |

  Subagents, hooks, output styles, and other settings are **not** loaded from added directories.
  - *Implication*: Teams that pass multiple repos via `--add-dir` expecting full configuration sharing will need to use user-level config (`~/.claude/`) or plugins instead.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

- **`skipDangerousModePermissionPrompt` setting added**: New permission setting that skips the confirmation prompt before entering bypass permissions mode. Ignored in project settings to prevent untrusted repos from auto-bypassing.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Hooks

- **Multi-hook conflict resolution documented**: Added explicit guidance on what happens when multiple hooks match the same event.
  > For decisions, Claude Code picks the most restrictive answer. A `PreToolUse` hook returning `deny` cancels the tool call no matter what the others return. One hook returning `ask` forces the permission prompt even if the rest return `allow`. Text from `additionalContext` is kept from every hook and passed to Claude together.
  - *Implication*: Developers building hook stacks now have documented conflict resolution semantics.
  - *Source*: [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)

- **New "Hooks and permission modes" section**: Clarifies the interaction between `PreToolUse` hooks and permission mode bypass.
  > PreToolUse hooks fire before any permission-mode check. A hook that returns `permissionDecision: "deny"` blocks the tool even in `bypassPermissions` mode or with `--dangerously-skip-permissions`.
  > The reverse is not true: a hook returning `"allow"` does not bypass deny rules from settings.
  - *Implication*: Hooks can be used to enforce policy that users cannot sidestep by changing permission mode.
  - *Source*: [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)

- **Non-deterministic `updatedInput` warning added**: When multiple `PreToolUse` hooks return `updatedInput` to rewrite a tool's arguments, the last to finish wins — order is non-deterministic because hooks run in parallel.
  - *Source*: [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)

### Tools Reference

- **New "LSP tool behavior" section**: Describes what the LSP tool does in detail — automatic type error reporting after edits, navigation capabilities (jump to definition, find references, call hierarchies, etc.). Notes that the tool is inactive until a code intelligence plugin is installed.
  - *Source*: [Tools Reference](https://code.claude.com/docs/en/tools-reference.md)

- **New "Check which tools are available" section**: Advises users to ask Claude directly (`What tools do you have access to?`) to discover what's loaded, since the exact tool set depends on provider, platform, and settings.
  - *Source*: [Tools Reference](https://code.claude.com/docs/en/tools-reference.md)

- **`SendMessage` and `TeamCreate`/`TeamDelete` added to tool table**: These were previously absent from the reference table. `SendMessage` is now documented as only available when agent teams are enabled via flag or env var.
  - *Source*: [Tools Reference](https://code.claude.com/docs/en/tools-reference.md)

- **`MCPSearch` renamed to `ToolSearch`**: The tool name used in permission deny rules has changed.
  > `"deny": ["ToolSearch"]`
  - *Implication*: Any existing config that uses `"deny": ["MCPSearch"]` will need to be updated to `ToolSearch`.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

### Managed Settings

- **Managed settings precedence clarified**: Server-managed and endpoint-managed settings no longer simply "both occupy the highest tier" — server-managed is checked first, and if it delivers any keys at all, endpoint-managed settings are ignored entirely (no merging).
  > Sources do not merge: if server-managed settings deliver any keys at all, endpoint-managed settings are ignored entirely.
  - *Implication*: Organizations using both server and endpoint managed settings need to be aware that clearing server-managed settings does not immediately fall back to endpoint settings due to client-side caching.
  - *Source*: [Server-Managed Settings](https://code.claude.com/docs/en/server-managed-settings.md)

- **Managed-only settings table updated**: `channelsEnabled`, `pluginTrustMessage`, and `sandbox.filesystem.allowManagedReadPathsOnly` explicitly added to the managed-only settings list. Description for `sandbox.filesystem.allowManagedReadPathsOnly` corrected: `denyRead` still merges from all sources (not just managed).
  - *Source*: [Server-Managed Settings](https://code.claude.com/docs/en/server-managed-settings.md)

### Integrations

- **Vertex AI: example updated to newer model names**: The global endpoint example was updated from `VERTEX_REGION_CLAUDE_3_5_HAIKU`, `VERTEX_REGION_CLAUDE_3_5_SONNET`, and `VERTEX_REGION_CLAUDE_4_0_*` to `VERTEX_REGION_CLAUDE_HAIKU_4_5` and `VERTEX_REGION_CLAUDE_4_6_SONNET`. A note was added directing to the full env vars list and Vertex Model Garden for global endpoint support status.
  - *Source*: [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai.md)

- **Bedrock custom endpoint documented**: `ANTHROPIC_BEDROCK_BASE_URL` added as a commented example in the Bedrock setup code block.
  - *Source*: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md)

- **Web auto-fix warning added**: A new warning block cautions that Claude can reply to PR review comments using your GitHub account, which can trigger comment-based automation (Atlantis, Terraform Cloud, custom GitHub Actions on `issue_comment` events).
  > If your repository uses comment-triggered automation such as Atlantis, Terraform Cloud, or custom GitHub Actions that run on `issue_comment` events, be aware that Claude can reply on your behalf, which can trigger those workflows.
  - *Implication*: Users with infrastructure-as-code repos using auto-fix should audit their automation before enabling.
  - *Source*: [Claude Code on the Web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

### Configuration

- **`strictKnownMarketplaces` is now a managed-only setting**: The settings table now marks this as `(Managed settings only)`, matching the other managed-only keys.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **Settings table alphabetized**: The available settings table was reorganized alphabetically. No keys added or removed, but the ordering is now consistent.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

## Notable Details

- **CLAUDE.md size guideline reduced from ~500 to 200 lines**: Both `costs.md` and `features-overview.md` changed this recommendation. The tilde was also removed, making it a hard target rather than an approximation.
  > Keep CLAUDE.md under 200 lines. Move reference material to skills, which load on-demand.

- **`CLAUDE_CODE_NEW_INIT` changed from `true` to `1`**: Documented in `memory.md`, `commands.md`, and `env-vars.md`. Consistent with the broader pattern of normalizing boolean env vars to `1`/`0`.

- **`/init` environment variable format**: The commands reference changed `CLAUDE_CODE_NEW_INIT=true` to `CLAUDE_CODE_NEW_INIT=1`, matching the env vars reference update.

- **Prompt suggestion acceptance**: Right arrow key added alongside Tab as an accepted gesture for completing prompt suggestions.
  > Press **Tab** or **Right arrow** to accept the suggestion

- **Terminal: Ctrl+J for newlines**: Added as an explicit option for inserting a newline without terminal-specific configuration.

- **Subagents and `--add-dir`**: Documentation now explicitly states that project subagents in `.claude/agents/` are discovered by walking up from the current working directory and that `--add-dir` paths are not scanned for subagents.

- **`SendMessage` tool gated on agent teams**: The docs now clarify that `SendMessage` (used to resume subagents) is only available when agent teams are enabled. Previously this was unstated.

- **`disableBypassPermissionsMode` scope**: Now documented to work from any settings scope (not just managed), including user settings — meaning a user can lock themselves out of bypass mode via their own settings.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| amazon-bedrock.md | Modified | +3/-0 | Added `ANTHROPIC_BEDROCK_BASE_URL` as commented example |
| changelog.md | Modified | +0/-44 | v2.1.88 entry scrolled off the visible page |
| claude-code-on-the-web.md | Modified | +4/-0 | Added warning about comment-triggered automation with auto-fix |
| cli-reference.md | Modified | +62/-59 | Added `--agent-teams`, `--debug-file`, `--replay-user-messages`; tightened `--include-partial-messages` requirements; clarified `--add-dir` |
| commands.md | Modified | +2/-2 | Updated `/add-dir` description and `CLAUDE_CODE_NEW_INIT` value from `true` to `1` |
| costs.md | Modified | +1/-1 | CLAUDE.md size guideline changed from ~500 to 200 lines |
| discover-plugins.md | Modified | +4/-4 | `FORCE_AUTOUPDATE_PLUGINS` and `DISABLE_AUTOUPDATER` values standardized to `1` from `true` |
| env-vars.md | Modified | +77/-15 | ~30 new variables; ~15 description updates; `1` standardized over `true`; OTel and Glob tuning vars added |
| features-overview.md | Modified | +1/-1 | CLAUDE.md size guideline changed from ~500 to 200 lines |
| google-vertex-ai.md | Modified | +8/-9 | Updated global endpoint example to newer model names; added `ANTHROPIC_VERTEX_BASE_URL` |
| hooks-guide.md | Modified | +10/-1 | Added multi-hook conflict resolution, "Hooks and permission modes" section, `updatedInput` non-determinism warning |
| interactive-mode.md | Modified | +1/-1 | Right arrow key added for prompt suggestion acceptance |
| mcp.md | Modified | +2/-2 | `MCPSearch` renamed to `ToolSearch` in deny rule example |
| memory.md | Modified | +1/-1 | `CLAUDE_CODE_NEW_INIT` value from `true` to `1` |
| permissions.md | Modified | +26/-4 | New "Additional directories grant file access, not configuration" section with exceptions table |
| sandboxing.md | Modified | +1/-1 | Clarified `denyRead` still merges from all sources when `allowManagedReadPathsOnly` is set |
| server-managed-settings.md | Modified | +12/-3 | Managed settings precedence clarified (no merging); managed-only settings section expanded |
| settings.md | Modified | +51/-50 | Table alphabetized; `skipDangerousModePermissionPrompt` added; `strictKnownMarketplaces` marked managed-only |
| skills.md | Modified | +3/-1 | Clarified skills are an exception to `--add-dir`'s file-access-only semantics |
| sub-agents.md | Modified | +5/-1 | Added note that `--add-dir` paths aren't scanned for subagents; `SendMessage` gated on agent teams flag |
| terminal-config.md | Modified | +1/-0 | Added Ctrl+J as a newline option |
| tools-reference.md | Modified | +64/-35 | New LSP behavior section, "Check which tools are available" section; `SendMessage`/`TeamCreate`/`TeamDelete` added to table; introductory text expanded |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-01*
