# Claude Code Documentation Changes — 2026-02-25

## Summary

This update is dominated by a major restructuring of three core documentation pages: `setup.md` (renamed "Advanced setup"), `authentication.md` (now covers individual login flow), and `troubleshooting.md` (expanded from ~121 to ~588 added lines with a new error lookup table and diagnostic procedures). Alongside these structural changes, `settings.md` gains 11 new configuration settings, `permissions.md` corrects the meaning of `/path` patterns, and the CLI reference documents three new `claude auth` commands.

---

## Significant Changes

### Installation & Setup

- **`setup.md` renamed to "Advanced setup"**: The page title changed from "Set up Claude Code" to "Advanced setup," and the subtitle was updated to "System requirements, platform-specific installation, version management, and uninstallation." Authentication content was removed and consolidated into `authentication.md`. The page now explicitly defers first-run onboarding to the quickstart guide.
  > *"This page covers system requirements, platform-specific installation details, updates, and uninstallation. For a guided walkthrough of your first session, see the [quickstart](/en/quickstart)."*
  - *Implication*: Developers looking for the original "Set up Claude Code" guide should use the quickstart; `setup.md` is now reference-focused.
  - *Source*: [Advanced setup](https://code.claude.com/docs/en/setup.md)

- **Shell requirements expanded**: The supported shell list now explicitly includes PowerShell and CMD alongside Bash and Zsh, and formally states Git for Windows is required on Windows.
  > *"Shell: Bash, Zsh, PowerShell, or CMD. On Windows, [Git for Windows](https://git-scm.com/downloads/win) is required."*
  - *Implication*: Windows users no longer need to hunt for the Git for Windows requirement—it's now stated upfront in system requirements, the install tab, the quickstart, and the overview.
  - *Source*: [Advanced setup](https://code.claude.com/docs/en/setup.md)

- **Node.js 18+ dependency removed from system requirements**: Node.js 18+ was listed as an additional dependency; it has been removed. The dependency note is now only present in the deprecated npm installation section.
  - *Implication*: Developers using the native installer no longer need Node.js.
  - *Source*: [Advanced setup](https://code.claude.com/docs/en/setup.md)

- **New `Verify your installation` section**: A dedicated step documents `claude --version` and `claude doctor` for post-install validation.
  > *"For a more detailed check of your installation and configuration, run `claude doctor`"*
  - *Implication*: `claude doctor` is now the canonical first step for diagnosing any post-install issue.
  - *Source*: [Advanced setup](https://code.claude.com/docs/en/setup.md)

- **`DISABLE_AUTOUPDATER` configuration method changed**: The old docs showed setting this as a shell environment variable (`export DISABLE_AUTOUPDATER=1`). The new docs show it configured via the `env` key in `settings.json`:
  ```json
  {
    "env": {
      "DISABLE_AUTOUPDATER": "1"
    }
  }
  ```
  - *Implication*: The persistent, recommended way to disable auto-updates is now via `settings.json`, not a shell export. Shell-level env vars still work at runtime but aren't documented.
  - *Source*: [Advanced setup](https://code.claude.com/docs/en/setup.md)

- **`CLAUDE_CODE_GIT_BASH_PATH` now documented in `settings.json`**: Previously documented as a PowerShell `$env:` variable, the Git Bash path is now configured via the `env` key in `settings.json`:
  ```json
  {
    "env": {
      "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
    }
  }
  ```
  - *Source*: [Advanced setup](https://code.claude.com/docs/en/setup.md)

- **Alpine Linux `USE_BUILTIN_RIPGREP` now documented in `settings.json`**: Previously undocumented in this context, the setting is now shown as a `settings.json` `env` entry.
  - *Source*: [Advanced setup](https://code.claude.com/docs/en/setup.md)

- **npm-to-native migration: `claude install` mentioned**: An alternative migration path is documented:
  > *"You can also run `claude install` from an existing npm installation to install the native binary alongside it, then remove the npm version."*
  - *Source*: [Advanced setup](https://code.claude.com/docs/en/setup.md)

- **Homebrew disk space note added**:
  > *"Homebrew keeps old versions on disk after upgrades. Run `brew cleanup claude-code` periodically to reclaim disk space."*
  - *Source*: [Advanced setup](https://code.claude.com/docs/en/setup.md)

---

### Authentication

- **Authentication page restructured for individual and team flows**: The "Authentication methods" section was replaced by two new sections: "Log in to Claude Code" (covering individual login) and "Set up team authentication." The new individual login section documents the first-run browser flow and a keyboard shortcut:
  > *"If the browser doesn't open automatically, press `c` to copy the login URL to your clipboard, then paste it into your browser."*
  - *Source*: [Authentication](https://code.claude.com/docs/en/authentication.md)

- **`/logout` command documented**: The page now explicitly states that `/logout` at the Claude Code prompt logs you out and allows re-authentication.
  - *Source*: [Authentication](https://code.claude.com/docs/en/authentication.md)

- **Microsoft Azure renamed to Microsoft Foundry**: References to "Microsoft Azure" in the cloud provider authentication section have been updated to "Microsoft Foundry" throughout.
  - *Implication*: Teams using the Microsoft cloud integration should verify they are targeting the Foundry product.
  - *Source*: [Authentication](https://code.claude.com/docs/en/authentication.md)

- **Free plan explicitly excluded**: The setup page now states: *"Claude Code requires a Pro, Max, Teams, Enterprise, or Console account. The free Claude.ai plan does not include Claude Code access."*
  - *Source*: [Advanced setup](https://code.claude.com/docs/en/setup.md)

---

### Troubleshooting

- **Complete restructure with error lookup table**: The troubleshooting page now opens with a two-column quick-lookup table mapping error messages/symptoms to their solution anchors, followed by structured diagnostic procedures.
  > *"Find the error message or symptom you're seeing: [table with 14 entries]"*
  - *Implication*: Developers can now find the right fix directly from an error string rather than reading sequentially.
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

- **New diagnostic procedures**: Five new diagnostic sections walk through root-cause identification:
  - `Check network connectivity` — verifies `storage.googleapis.com` access, documents proxy configuration via `HTTPS_PROXY`/`HTTP_PROXY`
  - `Verify your PATH` — per-platform PATH check commands (macOS/Linux, Windows PowerShell, Windows CMD)
  - `Check for conflicting installations` — detect multiple claude binaries with `which -a claude`, `where.exe claude`
  - `Check directory permissions` — verify `~/.local/bin/` and `~/.claude/` are writable
  - `Verify the binary works` — use `ldd` to check for missing shared libraries on Linux
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

- **New platform-specific installation error entries**:
  | Error | Fix documented |
  |---|---|
  | Install script returns HTML | Regional block detection, Homebrew/WinGet alternatives |
  | `curl: (56) Failure writing output` | Test connectivity to GCS, use package manager alternatives |
  | TLS/SSL errors | Update CA certs, enable TLS 1.2 on Windows, set `NODE_EXTRA_CA_CERTS` |
  | `Failed to fetch version from storage.googleapis.com` | Proxy config via `HTTPS_PROXY` |
  | Windows: `irm` or `&&` not recognized | Shell mismatch diagnosis |
  | Install killed on low-memory Linux | Add 2 GB swap space |
  | Install hangs in Docker | Set `WORKDIR /tmp` before installer, increase memory limit |
  | Windows: Claude Desktop overrides `claude` CLI | Update Claude Desktop |
  | Linux: musl/glibc mismatch | `ldd` diagnosis, manual binary download |
  | `Illegal instruction` on Linux | Architecture mismatch (`uname -m`) |
  | `dyld: cannot load` on macOS | Binary incompatibility |
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

- **New authentication-specific error entries**:
  - OAuth error: Invalid code
  - 403 Forbidden after login
  - OAuth login fails in WSL2
  - "Not logged in" or token expired
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

- **Desktop app tip added**: A callout at the top of the troubleshooting page now suggests the Claude Code Desktop app as an alternative to terminal installation.
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

---

### Configuration & Settings

- **11 new settings documented in `settings.json`**:

  | Setting | Description |
  |---|---|
  | `alwaysThinkingEnabled` | Enable extended thinking by default for all sessions |
  | `plansDirectory` | Customize where plan files are stored (relative to project root; default: `~/.claude/plans`) |
  | `showTurnDuration` | Show turn duration messages after responses (e.g., "Cooked for 1m 6s") |
  | `spinnerVerbs` | Customize action verbs in spinner; `mode: "replace"` or `"append"` |
  | `language` | Configure Claude's preferred response language (e.g., `"japanese"`) |
  | `autoUpdatesChannel` | Release channel: `"latest"` (default) or `"stable"` (≈1 week old) |
  | `spinnerTipsEnabled` | Show tips while Claude works (default: `true`) |
  | `spinnerTipsOverride` | Override spinner tips with custom strings; `excludeDefault` to suppress built-ins |
  | `terminalProgressBarEnabled` | Enable terminal progress bar in supported terminals (default: `true`) |
  | `prefersReducedMotion` | Reduce/disable UI animations for accessibility |
  | `teammateMode` | How agent team teammates display: `auto`, `in-process`, or `tmux` |

  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **New sandbox setting `network.allowManagedDomainsOnly`**: When `true`, only `allowedDomains` and `WebFetch(domain:...)` allow rules from managed settings are respected for outbound network traffic; project and user settings cannot add additional domains. Denied domains still merge from all sources.
  - *Implication*: Enterprise admins can now lock down sandbox network egress to managed-only domain lists, preventing project or user settings from expanding the allowlist.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **Managed settings precedence clarified**: A note was added stating that within the managed tier, sources do not merge—only one source is used:
  > *"Only one managed source is used; sources do not merge."*
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

---

### Permissions

- **`/path` pattern meaning corrected**: The `/path` permission rule pattern (single leading slash) was previously documented as "relative to settings file." It is now documented as "**relative to project root**."
  > *Before*: `Edit(/src/**/*.ts)` → `<settings file path>/src/**/*.ts`
  > *After*: `Edit(/src/**/*.ts)` → `<project root>/src/**/*.ts`
  - The associated warning was updated: *"A pattern like `/Users/alice/file` is NOT an absolute path. It's relative to the project root."*
  - The example clarification was extended: `Edit(/docs/**)` now notes it does NOT match `<project>/.claude/docs/`.
  - *Implication*: Any existing permission rules using `/path` patterns should be verified against the corrected semantics.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

- **Two new managed-only settings**:
  - `allowManagedMcpServersOnly`: When `true`, only `allowedMcpServers` from managed settings are respected; `deniedMcpServers` still merges from all sources.
  - `blockedMarketplaces`: Blocklist of marketplace sources checked before downloading—blocked sources never touch the filesystem.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

- **Managed settings delivery details moved**: The detailed delivery mechanism list (MDM profiles, registry paths, file paths) was removed from `permissions.md` and consolidated into `settings.md`. All cross-references across `desktop.md`, `security.md`, `server-managed-settings.md`, and `plugins-reference.md` have been updated accordingly.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

---

### CLI Reference

- **Three `claude auth` commands now formally documented**:

  | Command | Description |
  |---|---|
  | `claude auth login` | Sign in; `--email` pre-fills email, `--sso` forces SSO |
  | `claude auth logout` | Log out from Anthropic account |
  | `claude auth status` | Show auth status as JSON; `--text` for human-readable; exits 0 if logged in, 1 if not |

  - *Implication*: These commands were previously available but undocumented in the reference. Scripts that check auth status can now rely on the documented exit code behavior.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

---

### How Claude Code Works

- **Tool category count updated**: The built-in tools are now described as falling into "five categories" (previously "four"). The category table itself was not changed in the diff, suggesting a fifth category was added prior to this diff window.
  - *Source*: [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works.md)

---

## Notable Details

- **`DISABLE_AUTOUPDATER` value is now `"1"` (string), not `1` (int)**: The settings.json `env` key requires string values. The old shell-export form used `1` as an integer; the new documented form is `"1"` as a string. Ensure any automated settings files use the string form.

- **Homebrew code fence language corrected**: Multiple pages changed Homebrew install code blocks from ` ```sh ` to ` ```bash ` (overview.md, quickstart.md, setup.md). This is cosmetic but affects syntax highlighting in rendered docs.

- **Link anchor `#managed-settings` → `#managed-only-settings`**: At least five pages updated internal links from `permissions.md#managed-settings` to either `settings.md#settings-files` or `permissions.md#managed-only-settings`. Any external bookmarks or tooling referencing the old anchor may need updating.

- **`claude doctor` now linked as the canonical post-install check**: Previously mentioned only as a tip, it is now referenced in the setup verification section with an anchor link to troubleshooting.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `troubleshooting.md` | Modified | +588 / -121 | Major expansion: error lookup table, 15+ new error scenarios, diagnostic procedures |
| `setup.md` | Modified | +196 / -153 | Renamed "Advanced setup"; authentication moved out; Windows/Alpine setup rewritten |
| `settings.md` | Modified | +69 / -70 | 11 new settings; new sandbox `allowManagedDomainsOnly`; precedence clarification |
| `authentication.md` | Modified | +29 / -16 | Restructured for individual login flow; Microsoft Foundry rename; `/logout` documented |
| `permissions.md` | Modified | +19 / -32 | `/path` pattern corrected to "project root"; two new managed-only settings; delivery details moved |
| `cli-reference.md` | Modified | +16 / -13 | Three `claude auth` commands documented with flags and exit codes |
| `server-managed-settings.md` | Modified | +8 / -8 | Link updates; delivery mechanism description updated |
| `skills.md` | Modified | +7 / -7 | Minor updates (content not materially changed) |
| `plugins-reference.md` | Modified | +6 / -6 | Managed scope row updated to link to settings.md |
| `quickstart.md` | Modified | +4 / -1 | Windows Git requirement noted; terminal guide link added |
| `overview.md` | Modified | +3 / -1 | Windows Git requirement noted in install tab |
| `desktop.md` | Modified | +3 / -3 | Link anchor updated for managed settings |
| `security.md` | Modified | +1 / -1 | Managed settings link updated |
| `how-claude-code-works.md` | Modified | +1 / -1 | Tool categories count updated from four to five |
| `sub-agents.md` | Modified | +1 / -1 | Minor wording update |

---

*Generated from Claude Code CLI documentation changes detected on 2026-02-25*
