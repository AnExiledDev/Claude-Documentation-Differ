# Claude Code Documentation Changes — 2026-04-29

## Summary

Installation and login troubleshooting content has been extracted from the main `troubleshooting.md` into a new dedicated `troubleshoot-install.md` page, reducing the main page by ~910 lines while reorganizing the content with a structured error-lookup table. The hooks system gained a new `Setup` event type (tied to `--init`, `--init-only`, and `--maintenance` flags), and four new environment variables were documented.

## Significant Changes

### Documentation Structure

- **New `troubleshoot-install` page**: Installation, PATH, authentication, and platform-specific errors have been extracted from `troubleshooting.md` into a new dedicated page at `/en/troubleshoot-install`. The new page opens with a lookup table mapping error messages to specific fixes, then provides diagnostic procedures and per-error remediation steps for ~20 distinct failure modes.
  > "If installation fails or you can't sign in, find your error below. For runtime issues after Claude Code is working, see Troubleshooting. For configuration problems such as settings not applying or hooks not firing, see Debug your configuration."
  - *Implication*: Cross-references in `authentication.md`, `errors.md`, `setup.md`, `admin-setup.md`, `settings.md`, `debug-your-config.md`, and the install configurators in `overview.md` and `quickstart.md` have all been updated to point to the new page. Bookmarks to `troubleshooting.md#authentication-issues` and similar anchors will now 404; the correct anchors are on `troubleshoot-install.md`.
  - *Source*: [Troubleshoot installation and login](https://code.claude.com/docs/en/troubleshoot-install.md)

- **`troubleshooting.md` scope narrowed**: The page lost its installation, PATH, authentication, and IDE integration sections (910 lines removed). It now focuses on runtime issues: performance, hangs, and search. `debug-your-config.md`'s "See also" section was updated to distinguish: `troubleshoot-install` for "`command not found`, PATH, and authentication problems" vs. `troubleshooting` for "performance, hangs, and search issues."
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

### Hooks

- **New `Setup` hook event**: A new lifecycle event fires only when Claude Code is launched with `--init-only`, or with `--init` or `--maintenance` in print mode (`-p`). It does not fire on normal session startup. The matcher distinguishes between `init` and `maintenance` triggers. `CLAUDE_ENV_FILE` is available to Setup hooks, so environment variables written there persist into the session.
  > "Fires only when you launch Claude Code with `--init-only`, or with `--init` or `--maintenance` in print mode (`-p`). It does not fire on normal startup. Use it for one-time dependency installation or scheduled cleanup that you trigger explicitly from CI or scripts, separate from normal session startup."
  - *Implication*: CI pipelines can now run a distinct hook for environment preparation (`--init-only`) without triggering it on every interactive session. The `--init-only` flag runs Setup hooks and `SessionStart` hooks with the `startup` matcher, then exits without starting a conversation.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **`--init` and `--maintenance` flag descriptions corrected**: The CLI reference now documents that these flags run Setup hooks and are only effective in print mode (`-p`). Previously the descriptions implied they worked in interactive mode.
  > "`--init`: Run Setup hooks with the `init` matcher before the session (print mode only)" / "`--maintenance`: Run Setup hooks with the `maintenance` matcher before the session (print mode only)"
  - *Source*: [CLI reference](https://code.claude.com/docs/en/cli-reference.md)

- **`SubagentStart` built-in agent type renamed**: The built-in general-purpose agent was previously documented as `"Bash"` in matcher examples and `agent_type` values. It is now documented as `"general-purpose"`.
  > "Supports matchers to filter by agent type name (built-in agents like `general-purpose`, `Explore`, `Plan`, or custom agent names from `.claude/agents/`)"
  - *Implication*: Hooks that match on `SubagentStart` with matcher `"Bash"` may need updating to `"general-purpose"`.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **`Notification` hook gained two new matchers**: `elicitation_complete` (fires when an MCP elicitation form is submitted or dismissed) and `elicitation_response` (fires when an MCP elicitation response is sent back to the server) are now valid matcher values for `Notification` hooks.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md), [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md), [Common workflows](https://code.claude.com/docs/en/common-workflows.md)

- **Exit code 2 behavior clarified**: The hooks guide now explicitly documents which events cannot be blocked, and links to a per-event table in the reference.
  > "Some events cannot be blocked: for `SessionStart`, `Setup`, `Notification`, and others, exit 2 shows stderr to the user and execution continues. See exit code 2 behavior per event for the full list."
  - *Source*: [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)

- **Hook matcher note for file changes via Bash**: A new note clarifies that files modified via the `Bash` tool do not trigger `Edit` or `Write` hook matchers. The workaround is a `Stop` hook scanning the working tree, or adding a `Bash` matcher and calling `git status --porcelain`.
  - *Source*: [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)

### Environment Variables

- **`CLAUDE_CODE_DISABLE_POLICY_SKILLS`**: New. Set to `1` to skip loading skills from the system-wide managed skills directory.
  > "Useful for container or CI sessions that should not load operator-provisioned skills"
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_EXTRA_BODY`**: New. A JSON object merged into the top level of every API request body.
  > "Useful for passing provider-specific parameters that Claude Code does not expose directly"
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_MCP_ALLOWLIST_ENV`**: New. Set to `1` to spawn stdio MCP servers with only a safe baseline environment plus the server's configured `env`, instead of inheriting your full shell environment.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_USE_NATIVE_FILE_SEARCH`**: New. Set to `1` to use Node.js file APIs instead of ripgrep for discovering custom commands, subagents, and output styles. Useful when the bundled ripgrep binary is unavailable or blocked.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

### JetBrains Integration

- **WSL configuration section expanded**: The vague warning pointing to `troubleshooting.md` was replaced with inline step-by-step instructions. Two concrete options are now documented: (1) a Windows Firewall rule allowing WSL2's subnet traffic, and (2) switching WSL2 to mirrored networking mode (requires Windows 11 22H2+).
  > "If you're using Claude Code on WSL2 with a JetBrains IDE and see 'No available IDEs detected', the cause is usually WSL2's NAT networking or Windows Firewall blocking the connection between WSL2 and the IDE running on the Windows host."
  - *Source*: [JetBrains](https://code.claude.com/docs/en/jetbrains.md)

- **Section heading casing normalized to sentence case**: All section headings in `jetbrains.md` changed from Title Case to sentence case (e.g., "Marketplace Installation" → "Marketplace installation", "Security Considerations" → "Security considerations"). The content is unchanged; this is a formatting normalization.
  - *Source*: [JetBrains](https://code.claude.com/docs/en/jetbrains.md)

- **"Command not found" verification step updated**: The check `npm list -g @anthropic-ai/claude-code` was replaced with `claude --version` in a terminal. This reflects the shift from npm to the native binary installer.
  - *Source*: [JetBrains](https://code.claude.com/docs/en/jetbrains.md)

### Sandboxing

- **WSL1 and WSL2 sandboxing limitations documented**: Two new paragraphs explicitly document:
  1. WSL1 does not support sandboxing ("lacks the required Linux namespace primitives").
  2. WSL2 sandboxed commands cannot launch Windows binaries (`cmd.exe`, `powershell.exe`, paths under `/mnt/c/`). The workaround is `excludedCommands` in sandbox settings.
  - *Source*: [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)

### Release: v2.1.122 (April 28, 2026)

- **`ANTHROPIC_BEDROCK_SERVICE_TIER`** environment variable added to select a Bedrock service tier (`default`, `flex`, or `priority`), sent as the `X-Amzn-Bedrock-Service-Tier` header.
- **`/resume` PR URL paste**: Pasting a PR URL into the `/resume` search box now finds the session that created that PR (GitHub, GitHub Enterprise, GitLab, and Bitbucket).
- **OpenTelemetry**: Numeric attributes on `api_request`/`api_error` log events now emit as numbers, not strings; added `claude_code.at_mention` log event for `@`-mention resolution.
- **Bug fixes**: `/branch` forks from rewound timelines; `/model` effort option for Bedrock ARNs; Vertex AI/Bedrock `invalid_request_error` on structured-output queries; Vertex AI `count_tokens` 400 errors behind proxy gateways; `spinnerTipsOverride.excludeDefault` suppression; ToolSearch missing MCP tools connected post-start in nonblocking mode; `!exit`/`!quit` in bash mode; image resizing (2576px → 2000px max); remote control session idle status redrawing flooding tmux; blank assistant messages from stale view preference; malformed hooks entry no longer invalidates entire `settings.json`.
- **Voice mode**: Keybindings bound to Caps Lock now show an error since terminals don't deliver Caps Lock as a key event.
- *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

## New Pages

- **[troubleshoot-install.md](https://code.claude.com/docs/en/troubleshoot-install.md)** — Dedicated installation and login troubleshooting page. Covers: error lookup table with ~20 failure modes mapped to fixes, diagnostic checks (network connectivity, PATH verification, conflicting installations, directory permissions, binary validation), common installation errors (HTML install scripts, `command not found`, curl failures, TLS errors, Windows shell mismatches, low-memory kills, Docker hangs), platform-specific issues (Windows, macOS, Linux, WSL), authentication problems (OAuth errors, 403, model access, WSL2 OAuth), and cloud provider credential issues (Bedrock, Vertex, Foundry).

## Notable Details

- **Git for Windows changed from "recommended" to "required"** on native Windows in `setup.md`, `quickstart.md`, and `overview.md`. Previously the docs said PowerShell would be used as a fallback; that fallback language has been removed.
- **`/heapdump` output path updated**: The command now writes to `~/Desktop` or the home directory on Linux without a Desktop folder (not only `~/Desktop`).
- **`fullscreen.md`**: Added that running `/terminal-setup` in iTerm2 enables clipboard access via OSC 52 sequences automatically, rather than requiring manual configuration.
- **`monitoring-usage.md`**: The telemetry privacy note now distinguishes OpenTelemetry export (opt-in) from Anthropic's separate operational telemetry, linking to `/en/data-usage#telemetry-services` for the latter.
- **`debug-your-config.md`**: The `SessionEnd` hook troubleshooting entry now says "Add a `SessionEnd` hook in `settings.json`" rather than just pointing to the hook events list.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| troubleshoot-install.md | New | +782 | New dedicated installation and login troubleshooting page |
| troubleshooting.md | Modified | +48/-910 | Installation/auth/IDE sections extracted to troubleshoot-install.md |
| hooks.md | Modified | +59/-8 | New Setup hook event, updated lifecycle diagram, SubagentStart agent type renamed, new Notification matchers |
| jetbrains.md | Modified | +71/-34 | WSL config expanded with step-by-step instructions, heading case normalized |
| env-vars.md | Modified | +5/-1 | Four new env vars: DISABLE_POLICY_SKILLS, EXTRA_BODY, MCP_ALLOWLIST_ENV, USE_NATIVE_FILE_SEARCH |
| changelog.md | Modified | +21/-0 | v2.1.122 release entry added |
| hooks-guide.md | Modified | +9/-3 | Setup event in event table, exit code 2 clarification, Bash/file-change note |
| setup.md | Modified | +12/-10 | Git for Windows changed to required; link to troubleshoot-install |
| common-workflows.md | Modified | +8/-6 | Notification matcher table expanded with elicitation_complete, elicitation_response |
| sandboxing.md | Modified | +4/-0 | WSL1 unsupported, WSL2 Windows binary limitation documented |
| errors.md | Modified | +7/-6 | Updated cross-references to troubleshoot-install |
| debug-your-config.md | Modified | +4/-3 | Updated cross-references, SessionEnd hook description improved |
| cli-reference.md | Modified | +3/-3 | --init, --init-only, --maintenance descriptions updated |
| overview.md | Modified | +3/-3 | Git for Windows required; link to troubleshoot-install |
| quickstart.md | Modified | +2/-2 | Git for Windows required; link to troubleshoot-install |
| plugins-reference.md | Modified | +1/-0 | Setup event added to hook events table |
| fullscreen.md | Modified | +1/-1 | /terminal-setup mention for iTerm2 clipboard |
| commands.md | Modified | +1/-1 | /heapdump output path updated for Linux |
| monitoring-usage.md | Modified | +1/-1 | OTel opt-in note clarified vs Anthropic operational telemetry |
| settings.md | Modified | +1/-1 | Link updated to troubleshoot-install |
| admin-setup.md | Modified | +1/-1 | Link updated to troubleshoot-install |
| authentication.md | Modified | +1/-1 | Link updated to troubleshoot-install |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-29*
