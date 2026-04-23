# Claude Code Documentation Changes — 2026-04-23

## Summary

Version 2.1.118 was released on April 23, 2026, adding vim visual mode, a unified `/usage` command, custom theming, MCP tool hooks, a new `DISABLE_UPDATES` env var, and numerous bug fixes. Setup documentation gained comprehensive native Linux package manager support (apt/dnf/apk) with signed repositories for Debian/Ubuntu, Fedora/RHEL, and Alpine Linux.

## Significant Changes

### New Features (v2.1.118)

- **Vim visual mode**: Both character (`v`) and line (`V`) visual modes are now supported with selection, operators, and visual feedback.
  > Added vim visual mode (`v`) and visual-line mode (`V`) with selection, operators, and visual feedback
  - *Implication*: Users relying on vim keybindings gain standard visual selection workflows.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/usage` replaces `/cost` and `/stats`**: The two commands have been merged into `/usage`. Both old names remain as shortcuts that open the relevant tab.
  > Merged `/cost` and `/stats` into `/usage` — both remain as typing shortcuts that open the relevant tab
  - *Implication*: Existing muscle memory still works; `/usage` is the canonical command going forward.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Custom themes**: Named custom themes can be created and switched from `/theme`, or hand-edited as JSON files in `~/.claude/themes/`. Plugins can also ship themes via a `themes/` directory.
  > Create and switch between named custom themes from `/theme`, or hand-edit JSON files in `~/.claude/themes/`; plugins can also ship themes via a `themes/` directory
  - *Implication*: Teams and plugin authors can now distribute consistent visual styles.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Hooks can invoke MCP tools directly**: Hooks now support `type: "mcp_tool"` to call MCP tools inline from a hook definition.
  > Hooks can now invoke MCP tools directly via `type: "mcp_tool"`
  - *Implication*: Hooks can trigger MCP-backed actions without spawning a separate agent step.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`DISABLE_UPDATES` env var**: A new environment variable completely blocks all update paths, including manual `claude update`. This is stricter than the existing `DISABLE_AUTOUPDATER`.
  > Added `DISABLE_UPDATES` env var to completely block all update paths including manual `claude update` — stricter than `DISABLE_AUTOUPDATER`
  - *Implication*: Managed/enterprise environments can now prevent any update activity, not just background auto-updates.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **WSL inherits Windows managed settings**: WSL sessions on Windows can now inherit Windows-side managed settings via the `wslInheritsWindowsSettings` policy key.
  > WSL on Windows can now inherit Windows-side managed settings via the `wslInheritsWindowsSettings` policy key
  - *Implication*: Enterprise policy enforced on the Windows host now automatically applies to WSL-based Claude Code sessions.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Auto mode `"$defaults"` sentinel**: Including `"$defaults"` in `autoMode.allow`, `autoMode.soft_deny`, or `autoMode.environment` adds custom rules alongside the built-in list rather than replacing it.
  > Auto mode: include `"$defaults"` in `autoMode.allow`, `autoMode.soft_deny`, or `autoMode.environment` to add custom rules alongside the built-in list instead of replacing it
  - *Implication*: Customizing auto mode no longer requires replicating the full default ruleset manually.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`claude plugin tag`**: New subcommand creates release git tags for plugins with version validation.
  > Added `claude plugin tag` to create release git tags for plugins with version validation
  - *Implication*: Plugin authors have a first-class workflow for versioned releases.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`--continue`/`--resume` respects `/add-dir` sessions**: These flags now find sessions that added the current directory via `/add-dir`, not only sessions explicitly started in that directory.
  > `--continue`/`--resume` now find sessions that added the current directory via `/add-dir`
  - *Implication*: Resuming sessions in multi-root workspaces is more reliable.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/model` picker honors custom gateway overrides**: The picker now respects `ANTHROPIC_DEFAULT_*_MODEL_NAME` and `ANTHROPIC_DEFAULT_*_MODEL_DESCRIPTION` env vars when using a custom `ANTHROPIC_BASE_URL` gateway.
  > The `/model` picker now honors `ANTHROPIC_DEFAULT_*_MODEL_NAME`/`_DESCRIPTION` overrides when using a custom `ANTHROPIC_BASE_URL` gateway
  - *Implication*: Teams routing through proxy gateways with custom model names will see those names reflected in the picker UI.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/color` syncs to claude.ai/code**: When Remote Control is connected, `/color` now syncs the session accent color to claude.ai/code.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

### Installation — Linux Native Package Managers

- **New apt/dnf/apk installation method**: Claude Code now publishes signed repositories for native Linux package managers. Supported distributions are Debian/Ubuntu (apt), Fedora/RHEL (dnf), and Alpine Linux (apk).
  > Claude Code publishes signed apt, dnf, and apk repositories. Replace `stable` with `latest` for the rolling channel. Package manager installations do not auto-update through Claude Code; updates arrive through your normal system upgrade workflow.

  Install commands by package manager:
  - **apt**: Download the signing key to `/etc/apt/keyrings/claude-code.asc`, add the source list, then `sudo apt install claude-code`. Verify fingerprint: `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE`.
  - **dnf**: Write a repo file to `/etc/yum.repos.d/claude-code.repo` pointing to `https://downloads.claude.ai/claude-code/rpm/stable`, then `sudo dnf install claude-code`. Confirm the same fingerprint at first install.
  - **apk**: Download the RSA public key to `/etc/apk/keys/`, add the repo URL to `/etc/apk/repositories`, then `apk add claude-code`. Verify key SHA-256: `395759c1f7449ef4cdef305a42e820f3c766d6090d142634ebdb049f113168b6`.

  - *Implication*: Linux users on supported distros can now install, update, and remove Claude Code using standard system tooling without manual binary management. Updates come via `apt upgrade`, `dnf upgrade`, or `apk upgrade`.
  - *Source*: [Setup](https://code.claude.com/docs/en/setup.md)

- **Auto-update note updated**: The update documentation now explicitly lists apt, dnf, and apk alongside Homebrew and WinGet as installations that require manual upgrades.
  > Homebrew, WinGet, apt, dnf, and apk installations do not auto-update. For Linux package managers, see the upgrade commands in Install with Linux package managers.
  - *Source*: [Setup](https://code.claude.com/docs/en/setup.md)

- **Linux binary integrity note clarified**: The binary integrity section now distinguishes between direct downloads (verify via manifest signature) and package manager installs (signatures verified automatically by the package manager).
  > If you install with [apt, dnf, or apk], your package manager verifies signatures automatically using the repository signing key.
  - *Source*: [Setup](https://code.claude.com/docs/en/setup.md)

- **Uninstall instructions for apt/dnf/apk**: Full removal commands are now documented, including cleanup of repository config files and signing keys.
  - *Source*: [Setup](https://code.claude.com/docs/en/setup.md)

- **Overview and Quickstart cross-references added**: Both the Overview and Quickstart pages now include a one-line note pointing users to the Linux package manager section.
  > You can also install with [apt, dnf, or apk] on Debian, Fedora, RHEL, and Alpine.
  - *Source*: [Overview](https://code.claude.com/docs/en/overview.md), [Quickstart](https://code.claude.com/docs/en/quickstart.md)

---

### Bug Fixes (v2.1.118)

Notable fixes in this release:

- **MCP OAuth reliability**: Multiple fixes for OAuth token refresh — cross-process lock contention, macOS keychain race conditions, scope-mismatch silent refresh (should re-prompt instead), `expires_in`-less token responses triggering re-auth every hour, transient 401 "needs authentication" loops for HTTP/SSE servers, and token revocation before local expiry.
- **`/login` with `CLAUDE_CODE_OAUTH_TOKEN`**: `/login` now clears the env token so disk credentials take effect, instead of silently having no effect.
- **Credential save crash on Linux/Windows**: Fixed corrupted `~/.claude/.credentials.json` on crash during save.
- **`/fork` disk bloat**: `/fork` no longer writes the full parent conversation per fork — it writes a pointer and hydrates on read.
- **Agent-type hooks**: Fixed "Messages are required for agent hooks" errors when hooks were configured for events other than `Stop`/`SubagentStop`; also fixed prompt hooks re-firing on tool calls made by a verifier subagent.
- **Remote Control session archival**: Fixed sessions getting archived on transient CCR initialization blips during JWT refresh.
- **Keyboard input freeze**: Fixed Alt+K / Alt+X / Alt+^ / Alt+\_ freezing keyboard input.
- **Session model bleed**: Fixed connecting to a remote session overwriting the local `model` setting in `~/.claude/settings.json`.
- **Plugin dependency resolution**: Fixed `plugin install` on an already-installed plugin not re-resolving a dependency installed at the wrong version.
- **`subagents` spawned via `SendMessage`**: Fixed subagents not restoring the explicit `cwd` they were spawned with when resumed via `SendMessage`.

---

## Notable Details

- **`DISABLE_UPDATES` vs `DISABLE_AUTOUPDATER` distinction**: The changelog explicitly names both env vars, indicating a deliberate tiered model — `DISABLE_AUTOUPDATER` only suppresses background updates while `DISABLE_UPDATES` also blocks `claude update`. Environments that previously relied on `DISABLE_AUTOUPDATER` to prevent all updates should audit this difference.
- **Auto mode `"$defaults"` follows the partial-override pattern**: The sentinel allows incremental customization rather than full replacement of the default ruleset. This approach mirrors how other layered settings in Claude Code work and reduces the risk of inadvertently narrowing the effective policy.
- **Linux package manager channel selection**: The docs specify that replacing `stable` with `latest` in the repository URL switches to the rolling channel, mirroring the Homebrew `@latest` cask distinction. The default is `stable`.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| setup.md | Modified | +95 / -4 | Added Linux package manager install/uninstall sections; updated auto-update and binary integrity notes |
| changelog.md | Modified | +37 / -0 | Added v2.1.118 release notes |
| overview.md | Modified | +2 / -0 | Added cross-reference to Linux package manager install section |
| quickstart.md | Modified | +2 / -0 | Added cross-reference to Linux package manager install section |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-23*
