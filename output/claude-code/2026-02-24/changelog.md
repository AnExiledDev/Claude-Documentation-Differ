# Claude Code Documentation Changes — 2026-02-24

## Summary

A new **Remote Control** feature is introduced as a research preview (Pro and Max plans), enabling users to continue a locally-running Claude Code session from a phone, tablet, or browser via `claude.ai/code` or the Claude mobile app, without moving execution to the cloud. Alongside it, the managed-settings documentation is substantially expanded to cover MDM/OS-level policy delivery (macOS managed preferences, Windows registry), a new precedence ordering within the managed tier, a new `/status` command for inspecting active settings, and a new `allow_remote_sessions` managed-only setting.

---

## Significant Changes

### Remote Control (New Feature)

- **New `claude remote-control` CLI command**: Starts a Remote Control session bridging a locally-running Claude Code instance to the `claude.ai/code` web interface or the Claude mobile app. The local process stays running; the web/mobile client is a window into it.

  > Continue a local Claude Code session from your phone, tablet, or any browser using Remote Control. Works with claude.ai/code and the Claude mobile app.

  Key behavior documented:
  - Run `claude remote-control` in a project directory; the process prints a session URL and (on spacebar) a QR code for phone access.
  - From an existing terminal session, `/remote-control` (alias `/rc`) carries over conversation history and displays a session URL.
  - `--verbose`, `--sandbox`, and `--no-sandbox` flags available on the CLI command; not available via the `/remote-control` slash command.
  - Enable automatically for all sessions via `/config` → **Enable Remote Control for all sessions**.
  - One remote connection per Claude Code instance; multiple instances each get independent sessions.
  - Sessions time out after ~10 minutes of network unavailability; the terminal must stay open for the session to persist.
  - *Implication*: Developers can hand off in-progress local sessions to a phone or secondary machine without any code or files leaving their machine.
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md), [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **Security model for Remote Control**: All code execution and file access stays on the local machine. Traffic routes through the Anthropic API over TLS; no inbound ports are opened.

  > The connection uses multiple short-lived, narrowly scoped credentials, each limited to a specific purpose and expiring independently, to limit the blast radius of any single compromised credential.

  - *Source*: [Security](https://code.claude.com/docs/en/security.md)

- **Data flow clarification**: Remote Control sessions are classified as **local** data flow, not cloud.

  > Remote Control sessions follow the local data flow since all execution happens on your machine.

  - *Source*: [Data Usage](https://code.claude.com/docs/en/data-usage.md)

- **Availability**: Research preview on **Pro and Max plans only**; not available on Team or Enterprise plans. Requires `/login` authentication via claude.ai — API keys are not supported.

- **Android app now linked**: `claude-code-on-the-web.md` previously referenced only the Claude iOS app. Both iOS and Android apps are now mentioned throughout the Remote Control documentation and in the web interface page.

  > Claude Code is also available on the Claude app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) and [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) for kicking off tasks on the go and monitoring work in progress.

  - *Source*: [Claude Code on the Web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

---

### Configuration & Managed Settings

- **MDM/OS-level policy delivery now documented**: The managed-settings section in `permissions.md` and `settings.md` now explicitly covers native OS policy delivery alongside file-based `managed-settings.json`:

  > **MDM/OS-level policies**:
  > - **macOS**: `com.anthropic.claudecode` managed preferences domain, deployed via configuration profiles
  > - **Windows**: `HKLM\SOFTWARE\Policies\ClaudeCode` registry key with a `Settings` REG\_SZ value containing JSON
  > - **Windows (user-level)**: `HKCU\SOFTWARE\Policies\ClaudeCode` (lowest policy priority)

  - *Implication*: Administrators using Jamf, Kandji, Group Policy, or Intune now have a documented native delivery path alongside the existing file-based approach.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md), [Settings](https://code.claude.com/docs/en/settings.md)

- **Managed settings precedence order made explicit**: Within the managed tier, the priority order is now documented:

  > Within the managed tier, precedence is: server-managed > MDM/OS-level policies > `managed-settings.json` > HKCU registry (Windows only)

  The previous note stated only that system-wide paths require admin privileges. The updated note states that **only one source is used** and sources do not merge — Claude Code uses the first one found.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **New `/status` command for settings inspection**:

  > Run `/status` inside Claude Code to see which settings sources are active and where they come from. The output shows each configuration layer (managed, user, project) along with its origin, such as `Enterprise managed settings (remote)`, `Enterprise managed settings (plist)`, `Enterprise managed settings (HKLM)`, or `Enterprise managed settings (file)`. If a settings file contains errors, `/status` reports the issue so you can fix it.

  - *Implication*: Administrators and users can now diagnose which managed policy is actually in effect without inspecting file locations manually.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **New managed-only setting `allow_remote_sessions`**: Administrators can block users from starting Remote Control or web sessions:

  | Setting | Description |
  |---|---|
  | `allow_remote_sessions` | When `true`, allows users to start Remote Control and web sessions. Defaults to `true`. Set to `false` to prevent remote session access. |

  - *Implication*: Managed deployments can enforce a local-only execution policy centrally.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

---

### Documentation Structure

- **"Environments and interfaces" section added to `how-claude-code-works.md`**: A new section introduces a three-row execution environment comparison table and a complete list of interfaces. The previous note ("This guide focuses on the terminal") was removed.

  > The agentic loop, tools, and capabilities described above are the same everywhere you use Claude Code. What changes is where the code executes and how you interact with it.

  | Environment | Where code runs | Use case |
  |---|---|---|
  | **Local** | Your machine | Default. Full access to your files, tools, and environment |
  | **Cloud** | Anthropic-managed VMs | Offload tasks, work on repos you don't have locally |
  | **Remote Control** | Your machine, controlled from a browser | Use the web UI while keeping everything local |

  - *Source*: [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works.md)

- **Overview integration table updated**: A new row is prepended for Remote Control in the "Use Claude Code everywhere" section:

  > | Continue a local session from my phone or another device | [Remote Control](/en/remote-control) |

  - *Source*: [Overview](https://code.claude.com/docs/en/overview.md)

---

## New Pages

- **[remote-control.md](https://code.claude.com/docs/en/remote-control.md)** — Full documentation for the Remote Control feature: requirements, how to start a new session or attach to an existing one, how to connect from another device (URL, QR code, session list), security and connection model, limitations (one remote session per instance, terminal must stay open, ~10-minute network timeout), and a comparison against Claude Code on the web.

---

## Notable Details

- The `/mobile` slash command is mentioned in `remote-control.md` as a way to display a download QR code for the Claude iOS or Android app from inside Claude Code — this command does not yet appear in the CLI reference command table.
- The `/rename` slash command is recommended before `/remote-control` to assign a descriptive session name for easier discovery across devices.
- Remote Control sessions display a **computer icon with a green status dot** in the claude.ai/code session list when online — a useful indicator for multi-device workflows.
- `server-managed-settings.md` updated its comparison table security model column to read "deployed to devices via MDM configuration profiles, registry policies, or managed settings files" — reflecting the expanded delivery mechanisms.
- The `claude-code-on-the-web.md` page now cross-references Remote Control for users who want to use the web interface while keeping execution local, clearly distinguishing the two modes.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `remote-control.md` | New | +110 | Full documentation for the new Remote Control feature |
| `settings.md` | Modified | +20/-9 | MDM/OS policy delivery, managed-tier precedence, new `/status` command section |
| `permissions.md` | Modified | +16/-9 | MDM/OS policy locations, new `allow_remote_sessions` managed-only setting |
| `how-claude-code-works.md` | Modified | +18/-2 | New "Environments and interfaces" section with execution environment table |
| `overview.md` | Modified | +9/-7 | Remote Control added to "Work from anywhere" accordion and integration table |
| `cli-reference.md` | Modified | +13/-12 | New `claude remote-control` command row added to commands table |
| `security.md` | Modified | +2/-0 | Remote Control security model paragraph added |
| `server-managed-settings.md` | Modified | +5/-5 | Updated description and comparison table to include MDM/registry delivery |
| `claude-code-on-the-web.md` | Modified | +2/-2 | Added Android app link; added Remote Control cross-reference |
| `data-usage.md` | Modified | +1/-1 | Noted Remote Control follows local data flow |

---

*Generated from Claude Code CLI documentation changes detected on 2026-02-24*
