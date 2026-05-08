# Claude Code Documentation Changes — 2026-05-08

## Summary

Version 2.1.133 was released on May 7, 2026, adding the `worktree.baseRef` setting, effort-level hook variables, and sandbox binary path overrides alongside thirteen bug fixes. Documentation was substantially updated across debugging, error handling, routines, and cloud environment network access to reflect these changes and improve clarity.

## Significant Changes

### CLI Release: Version 2.1.133

- **`worktree.baseRef` setting**: New setting (`fresh` | `head`) controls whether `--worktree`, `EnterWorktree`, and agent-isolation worktrees branch from `origin/<default>` or local `HEAD`.
  > Added `worktree.baseRef` setting (`fresh` | `head`) to choose whether `--worktree`, `EnterWorktree`, and agent-isolation worktrees branch from `origin/<default>` or local `HEAD`. **Note:** the default `fresh` changes `EnterWorktree`'s base back to `origin/<default>` (it has been local `HEAD` since 2.1.128) — set `worktree.baseRef: "head"` to keep unpushed commits in new worktrees
  - *Implication*: Users who relied on `EnterWorktree` branching from local `HEAD` (behavior introduced in 2.1.128) must explicitly set `worktree.baseRef: "head"` to preserve it.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Hooks receive effort level**: Hooks now receive the active effort level via `effort.level` in JSON input and `$CLAUDE_EFFORT` environment variable; Bash tool commands can also read `$CLAUDE_EFFORT`.
  - *Implication*: Hook scripts can now branch behavior based on effort mode without additional configuration.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`sandbox.bwrapPath` and `sandbox.socatPath`**: New managed settings on Linux/WSL for specifying custom bubblewrap and socat binary locations.
  - *Implication*: Admins in environments where these binaries live outside standard paths can now configure them directly.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`parentSettingsBehavior` admin key**: New admin-tier setting (`'first-wins' | 'merge'`) opts SDK `managedSettings` (parent tier) into the policy merge.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Notable bug fixes in 2.1.133**:
  - Parallel sessions dead-ending at 401 after a refresh-token race wiped shared credentials
  - `Edit`/`Write` allow rules scoped to a drive root (`C:\`) or POSIX `/` always prompting instead of matching
  - HTTP(S)_PROXY / NO_PROXY / mTLS not applied to the full MCP OAuth flow
  - Read/Write/Edit denied on mapped network drives passed via `--add-dir` / SDK `additionalDirectories`
  - Remote Control stop/interrupt from claude.ai not fully canceling the CLI session
  - `/effort` in one session unexpectedly changing effort level of other concurrent sessions
  - Subagents not discovering project, user, or plugin skills via the Skill tool
  - `[VSCode]` `claudeCode.claudeProcessWrapper` failing with "Unsupported platform" when extension build doesn't bundle a Claude binary

### Configuration & Debugging

- **New `/debug [issue]` command**: Added to the debugging reference table.
  > `/debug [issue]` — Enables debug logging for the session and prompts Claude to diagnose using the log output and settings paths
  - *Implication*: Provides a direct in-session path to diagnosis without needing to restart with `--debug` flags.
  - *Source*: [Debug your config](https://code.claude.com/docs/en/debug-your-config.md)

- **Clean configuration test procedure**: New "Test against a clean configuration" section documents how to isolate configuration problems using a throwaway `CLAUDE_CONFIG_DIR`.
  > Point `CLAUDE_CONFIG_DIR` at an empty directory to bypass everything under `~/.claude`, and launch from a directory that has no `.claude` folder, `.mcp.json`, or `CLAUDE.md` so project configuration is also skipped.
  ```bash
  cd /tmp && CLAUDE_CONFIG_DIR=/tmp/claude-clean claude
  ```
  - *Implication*: Provides a reproducible isolation technique; the doc notes that managed settings still apply (system path), macOS Keychain credentials carry over, but Linux/Windows credentials will prompt for re-login.
  - *Source*: [Debug your config](https://code.claude.com/docs/en/debug-your-config.md)

- **`/doctor` interactive fix flow**: Documentation now mentions pressing `f` after `/doctor` reports issues to send the diagnostic report to Claude for assisted fixes.
  > When `/doctor` reports issues, press `f` to send the diagnostic report to Claude and have it walk through fixes with you.
  - *Source*: [Debug your config](https://code.claude.com/docs/en/debug-your-config.md)

- **New MCP troubleshooting row**: Added a clarifying entry to the "Check common causes" table for a common misconfiguration.
  > MCP servers added under `mcpServers` in `settings.json` never appear — `settings.json` does not read an `mcpServers` key — Define project servers in `.mcp.json` at the repository root, or run `claude mcp add --scope user` for user-scoped servers.
  - *Implication*: This is a documented common mistake; `mcpServers` in `settings.json` is silently ignored.
  - *Source*: [Debug your config](https://code.claude.com/docs/en/debug-your-config.md)

### Cloud Environment & Network Access

- **New "Host not allowed in a cloud session" error**: New error section documenting the `403` + `x-deny-reason: host_not_allowed` response that occurs when outbound requests from a cloud session or routine are blocked by the environment's network policy.
  > This is not a client-side network problem. Cloud sessions and routines run inside a sandboxed environment whose outbound traffic is filtered to the environment's allowlist.
  - *Implication*: Users encountering TLS certificate mismatches in cloud sessions should check the network policy — the proxy is terminating the connection, not the destination server.
  - *Source*: [Errors](https://code.claude.com/docs/en/errors.md)

- **Routines "Environments and network access" section expanded**: Renamed from "Environments" and substantially expanded with step-by-step instructions for modifying network access on a routine's environment.
  > The **Default** environment uses **Trusted** network access: the default allowlist of package registries, cloud provider APIs, container registries, and common development domains is reachable, but arbitrary domains are not. Outbound requests to other hosts fail with `403` and `x-deny-reason: host_not_allowed`.
  - *Implication*: Routine authors with custom API dependencies now have an explicit guide for enabling their domains without opening full network access.
  - *Source*: [Routines](https://code.claude.com/docs/en/routines.md)

- **Run status clarification note**: Added a callout warning that a green run status only means the session started without an infrastructure error, not that the task succeeded.
  > A green status in the run list means the session started and exited without an infrastructure error. It does not mean the task in your prompt succeeded. Open the run to read the transcript and confirm what Claude actually did.
  - *Source*: [Routines](https://code.claude.com/docs/en/routines.md)

- **MCP connector traffic routing clarified**: Added note explaining that MCP connector traffic routes through Anthropic's servers, so connector hosts don't need to be added to the environment's allowed domain list.
  > MCP connector traffic is routed through Anthropic's servers, so the connectors you enable on a session or routine work without adding their hosts to **Allowed domains**.
  - *Source*: [Claude Code on the Web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

- **"Edit an environment" instructions corrected**: The table row for editing an environment was rewritten to describe the actual UI path via the cloud icon.
  > Select the cloud icon showing the current environment's name to open the selector, hover over an environment, and click the settings icon that appears on the right.
  - *Source*: [Claude Code on the Web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

### Memory & AGENTS.md Compatibility

- **Symlink approach for AGENTS.md**: New guidance that a symlink (`ln -s AGENTS.md CLAUDE.md`) works as an alternative to the `@AGENTS.md` import pattern, with a Windows caveat.
  > On Windows, creating a symlink requires Administrator privileges or Developer Mode, so use the `@AGENTS.md` import instead.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

- **`/init` reads existing tool configs**: Documented that running `/init` in a repo with `AGENTS.md`, `.cursorrules`, or `.windsurfrules` reads those files and incorporates relevant parts into the generated `CLAUDE.md`.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

### Integrations & Authentication

- **VS Code extension installs in forks**: Added documentation that the extension works in VS Code forks like Windsurf and Kiro via the Open VSX registry.
  > The extension also installs in other VS Code forks like Windsurf or Kiro. Search for "Claude Code" in the editor's Extensions view, or install from the [Open VSX registry](https://open-vsx.org/extension/Anthropic/claude-code). If your editor can't install the extension, run `claude` in its integrated terminal instead.
  - *Source*: [VS Code](https://code.claude.com/docs/en/vs-code.md)

- **`ANTHROPIC_BASE_URL` clarification**: Added a note in model configuration that `ANTHROPIC_BASE_URL` changes where requests are sent, not which model answers them, with a pointer to LLM gateway documentation.
  > `ANTHROPIC_BASE_URL` changes where requests are sent, not which model answers them. To route Claude through an LLM gateway, see LLM gateway configuration.
  - *Implication*: Prevents confusion for users who set this variable expecting model-routing behavior.
  - *Source*: [Model config](https://code.claude.com/docs/en/model-config.md)

- **Credentials management clarification**: Added a bullet to the authentication page clarifying that `.credentials.json` is managed exclusively through `/login` and `/logout`, and that `ANTHROPIC_BASE_URL` is the correct mechanism for routing through a custom API endpoint.
  - *Source*: [Authentication](https://code.claude.com/docs/en/authentication.md)

## Notable Details

- The A/B test `Experiment` component (`docs-contact-sales-cta` GrowthBook flag) was removed from all four provider/integration pages (Amazon Bedrock, Google Vertex AI, Microsoft Foundry, third-party integrations). Each page now unconditionally renders `ContactSalesCard`. This accounts for the bulk of the line deletions (−111 per page, −444 total).
- The network errors section description was broadened: "almost always originate in your local network" changed to "usually originate in your local network, proxy, or firewall, **or in the cloud environment's network policy**" — reflecting the new cloud session error category.
- `worktree.baseRef` defaults to `fresh`, which is a **behavior regression** from 2.1.128–2.1.132 where `EnterWorktree` used local `HEAD`. Users with automation that depends on unpushed commits being available in new worktrees must explicitly opt in with `worktree.baseRef: "head"`.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| amazon-bedrock.md | Modified | +1 / -111 | Removed A/B test `Experiment` component; Contact Sales CTA now always shown |
| google-vertex-ai.md | Modified | +1 / -111 | Removed A/B test `Experiment` component; Contact Sales CTA now always shown |
| microsoft-foundry.md | Modified | +1 / -111 | Removed A/B test `Experiment` component; Contact Sales CTA now always shown |
| third-party-integrations.md | Modified | +1 / -111 | Removed A/B test `Experiment` component; Contact Sales CTA now always shown |
| routines.md | Modified | +36 / -4 | Expanded "Environments and network access" with step-by-step guide; added run status clarification note |
| debug-your-config.md | Modified | +49 / -29 | Added `/debug` command, clean-config test procedure, `/doctor` `f`-key tip, new MCP troubleshooting row |
| errors.md | Modified | +23 / -1 | New "Host not allowed in a cloud session" error section; updated network errors description |
| claude-code-on-the-web.md | Modified | +7 / -1 | Fixed environment edit UI instructions; added MCP connector routing note |
| memory.md | Modified | +10 / -0 | Added AGENTS.md symlink guidance and `/init` cross-tool config behavior |
| changelog.md | Modified | +20 / -0 | Added v2.1.133 release notes |
| model-config.md | Modified | +4 / -0 | Added `ANTHROPIC_BASE_URL` clarification note |
| vs-code.md | Modified | +2 / -0 | Added VS Code fork installation guidance (Windsurf, Kiro, Open VSX) |
| authentication.md | Modified | +1 / -0 | Added `.credentials.json` management and custom API endpoint guidance |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-08*
