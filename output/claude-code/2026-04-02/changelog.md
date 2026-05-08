# Claude Code Documentation Changes — 2026-04-02

## Summary

27 pages modified, no pages added or removed. The most significant changes introduce distributed tracing (beta) to the OpenTelemetry monitoring stack, document a new `/powerup` interactive tutorial command, expand the protected-directories safety model to include `.husky`, and perform a consistent rename of the "Teams" plan to "Team" across the entire documentation set.

## Significant Changes

### Features

- **New `/powerup` command**: A new slash command that delivers interactive lessons about Claude Code features with animated demos.
  > `Discover Claude Code features through quick interactive lessons with animated demos`
  - *Implication*: Provides an in-product onboarding path; the `common-workflows.md` FAQ note now points users to `/powerup` instead of the workflow sections alone.
  - *Source*: [commands.md](https://code.claude.com/docs/en/commands.md)

- **`/resume` picker scoped to interactive sessions**: The session resume picker now explicitly lists only interactive sessions; sessions started with `claude -p` or via the SDK are excluded from the picker but can still be resumed by ID.
  > `Sessions are stored per project directory. The /resume picker shows interactive sessions from the same git repository, including worktrees. Sessions created by claude -p or SDK invocations do not appear in the picker, but you can still resume one by passing its session ID directly to claude --resume <session-id>.`
  - *Implication*: Developers who mix interactive and non-interactive sessions should note the picker filter; programmatic sessions are still fully resumable via `--resume <id>`.
  - *Source*: [common-workflows.md](https://code.claude.com/docs/en/common-workflows.md)

- **`claude --teleport` replaces `/teleport`**: The overview page now references `claude --teleport` (CLI flag) rather than `/teleport` (slash command) for pulling a web/iOS session into a local terminal.
  - *Source*: [overview.md](https://code.claude.com/docs/en/overview.md)

### Monitoring & Telemetry

- **Distributed tracing (beta)**: OpenTelemetry support is extended to include distributed traces. Traces link each user prompt to its API requests and tool executions, enabling full-request waterfall views in trace backends.
  > `Distributed tracing exports spans that link each user prompt to the API requests and tool executions it triggers, so you can view a full request as a single trace in your tracing backend.`
  >
  > Enabling requires both `CLAUDE_CODE_ENABLE_TELEMETRY=1` and `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`, plus setting `OTEL_TRACES_EXPORTER`.

  New environment variables:
  | Variable | Purpose |
  |---|---|
  | `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` | Enable span tracing (required). `ENABLE_ENHANCED_TELEMETRY_BETA` also accepted |
  | `OTEL_TRACES_EXPORTER` | Traces exporter (`console`, `otlp`, `none`) |
  | `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL` | Protocol for traces, overrides the global OTLP protocol |
  | `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | Traces endpoint, overrides the global OTLP endpoint |
  | `OTEL_TRACES_EXPORT_INTERVAL` | Batch export interval in ms (default: 5000) |
  | `OTEL_LOG_TOOL_CONTENT` | Log tool input/output content in span events (default: disabled, truncated at 60 KB) |

  - *Implication*: Organizations using Jaeger, Grafana Tempo, Datadog, or Honeycomb can now trace individual Claude Code sessions end-to-end. Prompt text and tool content are redacted by default; opt in with `OTEL_LOG_USER_PROMPTS=1` and `OTEL_LOG_TOOL_CONTENT=1`.
  - *Source*: [monitoring-usage.md](https://code.claude.com/docs/en/monitoring-usage.md)

### Security & Permissions

- **`.husky` added to protected directories**: The `.husky` directory (git hooks) is now part of the protected-directories list alongside `.git`, `.vscode`, `.idea`, and `.claude`. In `bypassPermissions` and `acceptEdits` modes, writes to `.husky` will still trigger a confirmation prompt.
  > `bypassPermissions mode disables permission prompts and safety checks. Tool calls execute immediately, except for writes to .git, .vscode, .idea, and .husky, which still prompt to prevent accidental corruption of repository state, editor configuration, and git hooks.`
  - *Implication*: This prevents Claude from silently modifying git hooks in any permission mode, closing a potential corruption vector in automated workflows.
  - *Source*: [permission-modes.md](https://code.claude.com/docs/en/permission-modes.md), [permissions.md](https://code.claude.com/docs/en/permissions.md), [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md)

- **Protected directories now documented for `acceptEdits` mode**: The table and descriptions for `acceptEdits` now explicitly state it excludes protected directories from auto-approval, and a new standalone note summarizes which directories are always protected across all modes.
  > `Regardless of mode, writes to .git, .vscode, .idea, .husky, and .claude are never auto-approved, except for .claude/commands, .claude/agents, and .claude/skills where Claude routinely creates skills, subagents, and commands.`
  - *Implication*: The auto mode classifier cost note is also updated: classifier calls are not triggered for "file edits in your working directory outside protected directories" (previously "in your working directory" without qualification).
  - *Source*: [permission-modes.md](https://code.claude.com/docs/en/permission-modes.md)

### Plugin & Marketplace

- **Offline/airgapped marketplace fix — `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE`**: A new environment variable and troubleshooting section document how to prevent Claude Code from wiping the local marketplace cache when `git pull` fails in environments without internet access.
  > `Set CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1 to keep the existing cache when the pull fails instead of wiping it. With this variable set, Claude Code retains the stale marketplace clone on git pull failure and continues using the last-known-good state.`
  - *Implication*: Essential for offline/airgapped deployments. For fully disconnected environments with no future connectivity, `CLAUDE_CODE_PLUGIN_SEED_DIR` remains the recommended approach for pre-populating plugins at build time.
  - *Source*: [plugin-marketplaces.md](https://code.claude.com/docs/en/plugin-marketplaces.md), [env-vars.md](https://code.claude.com/docs/en/env-vars.md)

### Keybindings & UI

- **`Ctrl+L` behavior changed from "clear screen" to "redraw"**: The action is now `app:redraw` and the description has been corrected to "Repaints the current UI without clearing conversation history." Previously described as "Clear terminal screen."
  - *Implication*: Ctrl+L was never clearing conversation history, but the old label implied it might. The corrected description and new action name (`app:redraw`) are more accurate.
  - *Source*: [interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md), [keybindings.md](https://code.claude.com/docs/en/keybindings.md)

- **Additional keybindings documented**:
  - `chat:undo` now also bound to `Ctrl+Shift+-` (in addition to existing `Ctrl+_`)
  - `confirm:toggle` bound to `Space` in the Confirmation context
  - `settings:close` bound to `Enter` (saves and closes config panel; Escape discards and closes)
  - `transcript:exit` (`q`, `Ctrl+C`, `Esc`) — `q` is now documented as rebindable via `transcript:exit` (previously described as not rebindable)
  - *Source*: [keybindings.md](https://code.claude.com/docs/en/keybindings.md)

- **`Alt+T` (toggle extended thinking) no longer requires `/terminal-setup`**: The shortcut note previously said "Run `/terminal-setup` first to enable this shortcut." It now says "configure your terminal to send Option as Meta."
  - *Source*: [interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md)

- **VS Code Option-as-Meta configuration corrected**: The interactive-mode note for macOS now gives the correct VS Code setting (`"terminal.integrated.macOptionIsMeta": true`) instead of the incorrect iTerm2-style menu path. `Alt+T` is also now listed in the set of shortcuts requiring Option-as-Meta on macOS.
  - *Source*: [interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md)

### Statusline

- **Two new statusline JSON fields**:
  - `workspace.added_dirs`: Array of directories added via `/add-dir` or `--add-dir`; empty array if none.
  - `session_name`: Custom session name set with `--name` or `/rename`; absent if no custom name has been set.
  - *Implication*: Statusline scripts can now display multi-root workspace context and named sessions without external state tracking.
  - *Source*: [statusline.md](https://code.claude.com/docs/en/statusline.md)

### Skills

- **`allowed-tools` field now accepts space-separated string or YAML list**: Previously the docs (and examples) showed comma-separated tool names. The format has changed to space-separated strings, and a YAML list is also accepted.
  > `allowed-tools: Read Grep Glob` (was `Read, Grep, Glob`)
  - *Implication*: Existing skills using comma-separated `allowed-tools` values may need to be updated.
  - *Source*: [skills.md](https://code.claude.com/docs/en/skills.md)

- **Supporting file loading description clarified**: The Claude Directory docs now state bundled skill files are read "on demand while running the skill" rather than "when SKILL.md mentions it."
  - *Source*: [claude-directory.md](https://code.claude.com/docs/en/claude-directory.md)

### Installation

- **Windows installer URL path changed**: Download URLs for the Windows Desktop app updated from `.../exe/latest/...` to `.../setup/latest/...`. This affects both x64 and ARM64 links in `desktop-quickstart.md` and `overview.md`. The Windows download link on `setup.md` and `troubleshooting.md` now points to `https://claude.com/download` instead of a direct API redirect URL.

- **Pinned version example updated**: The "install a specific version" example in `setup.md` was bumped from `1.0.58` to `2.1.89`, reflecting the current stable release.

- **Checksum verification note updated**: The guide now notes "Steps 1–3 require a POSIX shell with `gpg` and `curl`. Step 4 includes a PowerShell option." Previously implied all steps required a POSIX shell.
  - *Source*: [setup.md](https://code.claude.com/docs/en/setup.md)

### Terminology

- **"Teams" plan renamed to "Team"** across all docs: Every reference to the "Teams" plan (e.g. "Pro, Max, Teams, or Enterprise") has been updated to "Team" (singular). Affected pages: `analytics.md`, `chrome.md`, `claude-code-on-the-web.md`, `code-review.md`, `desktop.md`, `desktop-quickstart.md`, `fast-mode.md`, `github-enterprise-server.md`, `quickstart.md`, `setup.md`, `slack.md`.

## Notable Details

- **`quickstart.md` cheat sheet**: `claude commit` removed from the "most important commands" table. The exit shortcut was also corrected from `Ctrl+C` to `Ctrl+D` (Ctrl+C interrupts a running task; Ctrl+D exits the session).
- **`fullscreen.md`**: Removed a sentence instructing users to rebind scroll actions via keybindings, simplifying the scroll navigation documentation.
- **`permission-modes.md` permission rules note**: The clarification that rules "apply in every mode except `bypassPermissions`, which skips the permission layer entirely" was shortened — the parenthetical detail was dropped. The note now simply reads "apply in every mode except `bypassPermissions`."
- **Statusline version in example JSON**: Updated from `1.0.80` to `2.1.90`, consistent with the pinned version bump in setup.md.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| monitoring-usage.md | Modified | +28/-3 | Added distributed tracing (beta) section, `OTEL_LOG_TOOL_CONTENT` env var, traces backend recommendations |
| permission-modes.md | Modified | +19/-17 | `.husky` added to protected dirs; `acceptEdits`/`bypassPermissions` tables updated; new protected-dirs summary note |
| keybindings.md | Modified | +13/-10 | Added `app:redraw`, `confirm:toggle`, `settings:close`; updated `chat:undo` bindings; `transcript:exit` now includes `q` |
| plugin-marketplaces.md | Modified | +14/-0 | New troubleshooting section: marketplace updates fail in offline environments |
| sub-agents.md | Modified | +9/-9 | Permission mode table updated to reflect protected-dirs behavior; `.husky` added to warning |
| interactive-mode.md | Modified | +8/-8 | `Ctrl+L` changed to redraw; `Alt+T` no longer requires `/terminal-setup`; VS Code Meta setting corrected; `transcript:exit` note updated |
| statusline.md | Modified | +7/-2 | Added `workspace.added_dirs` and `session_name` fields |
| setup.md | Modified | +11/-11 | Windows download URL; pinned version bumped to 2.1.89; checksum note updated; duplicate `theme` param cleanup |
| env-vars.md | Modified | +1/-0 | Added `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` |
| commands.md | Modified | +1/-0 | Added `/powerup` command |
| skills.md | Modified | +3/-3 | `allowed-tools` format changed to space-separated; YAML list also accepted |
| common-workflows.md | Modified | +2/-2 | `/resume` picker scoped to interactive sessions; `/powerup` reference added to FAQ note |
| desktop.md | Modified | +3/-3 | Skills link target updated; "Teams" → "Team" in two places |
| desktop-quickstart.md | Modified | +3/-3 | Windows installer URL `/exe/` → `/setup/`; "Teams" → "Team" |
| fast-mode.md | Modified | +4/-4 | "Teams" → "Team" in four places |
| analytics.md | Modified | +6/-6 | "Teams" → "Team" throughout; section header and anchor updated |
| overview.md | Modified | +3/-3 | Windows installer URLs updated; `/teleport` → `claude --teleport` |
| claude-code-on-the-web.md | Modified | +3/-3 | "Teams" → "Team" in two places |
| quickstart.md | Modified | +3/-4 | "Teams" → "Team"; `claude commit` removed from cheat sheet; exit key corrected to Ctrl+D |
| fullscreen.md | Modified | +1/-3 | Removed rebind instructions from scroll navigation section |
| permissions.md | Modified | +2/-2 | `acceptEdits` description updated; `.husky` added to `bypassPermissions` warning |
| chrome.md | Modified | +1/-1 | "Teams" → "Team" |
| claude-directory.md | Modified | +1/-1 | Supporting file loading description clarified |
| code-review.md | Modified | +1/-1 | "Teams" → "Team" |
| github-enterprise-server.md | Modified | +1/-1 | "Teams" → "Team" |
| slack.md | Modified | +2/-2 | "Teams" → "Team" in two places |
| troubleshooting.md | Modified | +4/-4 | Windows download URL; WSL2 sandbox error message updated; code block tag cleanup |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-02*
