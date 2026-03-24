# Claude Code Documentation Changes — 2026-03-24

## Summary

This update introduces auto mode — a research preview that replaces manual permission prompts with a background classifier model — along with a dedicated `permission-modes.md` reference page that consolidates all mode documentation. iMessage is added as a third supported channel alongside Telegram and Discord, and the LiteLLM docs include a security advisory about two compromised package versions (1.82.7 and 1.82.8).

## Significant Changes

### Permissions & Auto Mode

- **New page: `permission-modes.md`**: Permission mode documentation has been extracted into its own dedicated reference page, covering how to switch modes in CLI, JetBrains, VS Code, Desktop, and web/mobile surfaces.
  > "Switch between supervised editing, read-only planning, and auto mode where a background classifier replaces manual permission prompts. Cycle modes with Shift+Tab in the CLI or use the mode selector in VS Code, Desktop, and claude.ai."
  - *Implication*: Links previously pointing to `permissions.md#permission-modes` now point to `/en/permission-modes`. Internal links and bookmarks to the old anchor should be updated.
  - *Source*: [permission-modes.md](https://code.claude.com/docs/en/permission-modes.md)

- **Auto mode (research preview)**: A new permission mode — `auto` — has been documented. It runs a background classifier (Claude Sonnet 4.6) to approve or block each pending action without surfacing a prompt.
  > "Auto mode lets Claude execute actions without showing permission prompts. Before each action runs, a separate classifier model reviews the conversation and decides whether the action matches what you asked for: it blocks actions that escalate beyond the task scope, target infrastructure the classifier doesn't recognize as trusted, or appear to be driven by hostile content encountered in a file or web page."
  - Currently limited to **Team plans** (Enterprise and API described as "rolling out shortly"). Requires **Claude Sonnet 4.6 or Opus 4.6**. Not available on Haiku, claude-3 models, or third-party providers (Bedrock, Vertex, Foundry).
  - On Team/Enterprise plans, an admin must enable auto mode in Claude Code admin settings before users can turn it on.
  - **Classifier defaults — blocked**: `curl | bash`, production deploys, mass cloud storage deletion, IAM or repo permission grants, force push, pushing directly to `main`, irreversible file destruction, sending sensitive data to external endpoints.
  - **Classifier defaults — allowed**: local file operations in the working directory, installing declared dependencies, read-only HTTP requests, pushing to the branch you started on or one Claude created.
  - **Fallback behavior**: if the classifier blocks 3 consecutive actions or 20 total in one session, auto mode pauses and Claude Code resumes per-action prompts. In non-interactive (`-p`) mode it aborts the session instead.
  - **Cost**: each classifier call contributes to token usage. Shell commands and network operations trigger classifier calls; read-only actions and file edits in the working directory do not.
  - *Implication*: Auto mode is the documented preferred alternative to `bypassPermissions` for automated workflows where safety checks are still desirable. It is not a drop-in replacement for manual review on sensitive operations.
  - *Source*: [permission-modes.md](https://code.claude.com/docs/en/permission-modes.md), [permissions.md](https://code.claude.com/docs/en/permissions.md)

- **Auto mode classifier configuration (`autoMode` settings block)**: Extensive new configuration guide added to `permissions.md` explaining how organizations configure the classifier's trust model.
  > "For most organizations, `autoMode.environment` is the only field you need to set. It tells the classifier which repos, buckets, and domains are trusted, without touching the built-in block and allow rules."
  - Three sub-fields: `environment` (prose descriptions of trusted infrastructure), `allow` (override default allow exceptions), `soft_deny` (override default block rules).
  - `autoMode` is read from user settings, `.claude/settings.local.json`, and managed settings. **Not** from shared project `.claude/settings.json` — a checked-in repo cannot inject its own classifier allow rules.
  - **Critical warning**: Setting `allow` or `soft_deny` replaces the entire default list for that section. Always run `claude auto-mode defaults` before customizing to start from the full default lists.
  - *Implication*: Organizations whose developers push to non-default repos, write to cloud buckets, or use internal services will see classifier false-positive blocks until an admin populates `autoMode.environment`.
  - *Source*: [permissions.md](https://code.claude.com/docs/en/permissions.md)

- **New CLI subcommands for auto mode inspection**:
  > `claude auto-mode defaults` — Print the built-in auto mode classifier rules as JSON. Use `claude auto-mode config` to see your effective config with settings applied.
  - Three new subcommands: `claude auto-mode defaults`, `claude auto-mode config`, `claude auto-mode critique`.
  - `critique` provides AI feedback on custom `allow` and `soft_deny` rules, flagging ambiguous or redundant entries.
  - *Source*: [cli-reference.md](https://code.claude.com/docs/en/cli-reference.md)

- **New CLI flag `--enable-auto-mode`**: Unlocks `auto` in the `Shift+Tab` mode cycle without activating it. Requires a Team plan and Claude Sonnet 4.6 or Opus 4.6.
  > "Unlock auto mode in the Shift+Tab cycle. Requires a Team plan (Enterprise and API support rolling out shortly) and Claude Sonnet 4.6 or Opus 4.6"
  - *Source*: [cli-reference.md](https://code.claude.com/docs/en/cli-reference.md)

- **`disableAutoMode` managed setting**: Administrators can prevent auto mode use across an organization by setting `disableAutoMode` to `"disable"` in managed settings (also accepted under `permissions`). This joins `permissions.disableBypassPermissionsMode` as a managed lockout control.
  - *Source*: [desktop.md](https://code.claude.com/docs/en/desktop.md), [permissions.md](https://code.claude.com/docs/en/permissions.md)

- **`disableBypassPermissionsMode` key updated in Desktop managed settings table**: The table now uses `permissions.disableBypassPermissionsMode` (with the `permissions.` prefix) instead of the bare `disableBypassPermissionsMode`.
  - *Implication*: Verify which key format your Desktop managed settings configuration uses; both forms appear to be accepted per the inline documentation.
  - *Source*: [desktop.md](https://code.claude.com/docs/en/desktop.md)

- **`bypassPermissions` and `auto` mode disable instructions clarified**: New sentence in `permissions.md`:
  > "To prevent `bypassPermissions` or `auto` mode from being used, set `permissions.disableBypassPermissionsMode` or `disableAutoMode` to `"disable"` in any settings file. These are most useful in managed settings where they cannot be overridden."
  - *Source*: [permissions.md](https://code.claude.com/docs/en/permissions.md)

### Channels

- **iMessage added as a supported channel**: iMessage joins Telegram and Discord as an officially supported channel plugin in the research preview.
  > "The iMessage channel reads your Messages database directly and sends replies through AppleScript. It requires macOS and needs no bot token or external service."
  - Install: `/plugin install imessage@claude-plugins-official`
  - Launch: `claude --channels plugin:imessage@claude-plugins-official`
  - Requires **Full Disk Access** permission for the terminal to read `~/Library/Messages/chat.db`. Without it, the server exits immediately with `authorization denied`.
  - Self-chat (texting yourself) bypasses access control automatically. Other senders are added by handle: `/imessage:access allow +15551234567`.
  - Unlike Telegram/Discord, iMessage detects the user's own addresses from the Messages database at startup rather than using a pairing code flow.
  - *Source*: [channels.md](https://code.claude.com/docs/en/channels.md), [channels-reference.md](https://code.claude.com/docs/en/channels-reference.md)

### Security

- **LiteLLM security warning — compromised package versions**: A `<Note>` block in `llm-gateway.md` has been upgraded to a `<Warning>` with an active security advisory:
  > "LiteLLM PyPI versions 1.82.7 and 1.82.8 were compromised with credential-stealing malware. Do not install these versions. If you have already installed them: Remove the package, Rotate all credentials on affected systems, Follow the remediation steps in BerriAI/litellm#24518"
  - *Implication*: Anyone using LiteLLM as an LLM gateway with Claude Code should immediately check their installed version and rotate credentials if affected.
  - *Source*: [llm-gateway.md](https://code.claude.com/docs/en/llm-gateway.md)

### Configuration

- **`autoMode` configuration in server-managed settings**: The server-managed settings docs now include an example showing how to configure auto mode classifier trust via the admin console:
  ```json
  {
    "autoMode": {
      "environment": [
        "Source control: github.example.com/acme-corp and all repos under it",
        "Trusted cloud buckets: s3://acme-build-artifacts, gs://acme-ml-datasets",
        "Trusted internal domains: *.corp.example.com"
      ]
    }
  }
  ```
  - *Source*: [server-managed-settings.md](https://code.claude.com/docs/en/server-managed-settings.md)

- **`settings.md` restructured around scopes**: The settings page has been reorganized around an explicit scope model (Managed → User → Project → Local), with a table explaining which features live at each scope. Also notes that the legacy Windows managed settings path `C:\ProgramData\ClaudeCode\managed-settings.json` is no longer supported as of v2.1.75; the new path is `C:\Program Files\ClaudeCode\managed-settings.json`.
  - *Source*: [settings.md](https://code.claude.com/docs/en/settings.md)

### Best Practices

- **New section "Run autonomously with auto mode"**: Added under the "Automate and scale" section:
  > "For uninterrupted execution with background safety checks, use auto mode. A classifier model reviews commands before they run, blocking scope escalation, unknown infrastructure, and hostile-content-driven actions while letting routine work proceed without prompts."
  - Example: `claude --permission-mode auto -p "fix all lint errors"`
  - For non-interactive runs with `-p`, auto mode aborts if the classifier repeatedly blocks actions.
  - *Source*: [best-practices.md](https://code.claude.com/docs/en/best-practices.md)

- **Permission configuration section updated**: The "Configure permissions" tip now mentions auto mode as a third option alongside allowlists and sandboxing. The warning about `--dangerously-skip-permissions` was removed from this section (it remains documented in `permission-modes.md`).
  - *Source*: [best-practices.md](https://code.claude.com/docs/en/best-practices.md)

### IDE & Surface Updates

- **Desktop permission mode table updated**: Auto mode is now listed in the Desktop permission mode table with availability details. The CLI-vs-Desktop comparison table at the bottom of the page is updated to include Auto among the Desktop-available modes.
  - *Source*: [desktop.md](https://code.claude.com/docs/en/desktop.md)

- **Hooks `permission_mode` field updated**: The `permission_mode` field in the common hook JSON fields table now lists `"auto"` as a valid value alongside `"default"`, `"plan"`, `"acceptEdits"`, `"dontAsk"`, and `"bypassPermissions"`.
  - *Implication*: Hooks that branch on `permission_mode` should be updated to handle the new `"auto"` value.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md)

- **`Shift+Tab` description updated**: In `interactive-mode.md`, the shortcut description changed from "Toggle permission modes" to "Cycle permission modes":
  > "Cycle through `default`, `acceptEdits`, `plan`, and any modes you have enabled, such as `auto` or `bypassPermissions`. See permission modes."
  - *Source*: [interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md)

## New Pages

- **[permission-modes.md](https://code.claude.com/docs/en/permission-modes.md)** — Dedicated reference for all permission modes (default, acceptEdits, plan, auto, dontAsk, bypassPermissions). Covers switching modes across CLI, JetBrains, VS Code, Desktop, and web/mobile; auto mode classifier behavior including defaults, fallback thresholds, subagent handling, and cost; plan mode workflow; and a side-by-side comparison table of all modes.

## Notable Details

- Auto mode explicitly drops broad allow rules when activated: `Bash(*)`, wildcarded interpreters like `Bash(python*)`, package-manager run commands, and `Agent` allow rules. Narrow rules like `Bash(npm test)` are preserved and restored when leaving auto mode.
- The classifier receives only user messages and tool calls — Claude's own text and tool results are stripped. This means hostile content in a file or web page **cannot reach the classifier directly**, only through Claude's action choices.
- When a plan mode session completes, one of the approval options is "Approve and start in auto mode", enabling a plan-then-automate workflow without restarting.
- `--allow-dangerously-skip-permissions` is documented as a flag (distinct from `--dangerously-skip-permissions`) that adds `bypassPermissions` to the `Shift+Tab` cycle **without** activating it, allowing composition like `--permission-mode plan --allow-dangerously-skip-permissions`.
- The `autoMode` settings block is deliberately excluded from shared project settings (`.claude/settings.json`) to prevent a cloned repo from injecting its own classifier allow rules.
- The `disableBypassPermissionsMode` entry was **removed** from the managed-only settings table in `permissions.md`. It now appears in a different context as `permissions.disableBypassPermissionsMode`, implying it is no longer strictly managed-only but is most effective there.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| permission-modes.md | New | +290 | New dedicated page covering all permission modes including full auto mode docs |
| permissions.md | Modified | +118/-9 | Added `auto` to modes table; new auto mode classifier configuration guide; `disableAutoMode` setting |
| channels.md | Modified | +55/-5 | Added iMessage as a supported channel with full setup instructions |
| settings.md | Modified | +58/-56 | Restructured around explicit scope model; legacy Windows path deprecation noted |
| best-practices.md | Modified | +15/-10 | New "Run autonomously with auto mode" section; updated permission tips |
| desktop.md | Modified | +15/-12 | Added Auto mode to permission table and managed settings keys table |
| vs-code.md | Modified | +15/-15 | Updated permission mode references to new page |
| interactive-mode.md | Modified | +18/-18 | Updated Shift+Tab description to mention auto mode and new page link |
| server-managed-settings.md | Modified | +16/-2 | Added `autoMode` configuration example |
| llm-gateway.md | Modified | +8/-2 | Security warning for compromised LiteLLM versions 1.82.7 and 1.82.8 |
| overview.md | Modified | +11/-11 | Updated channels feature table to mention iMessage |
| cli-reference.md | Modified | +4/-2 | Added `claude auto-mode defaults` command; added `--enable-auto-mode` flag; updated links |
| hooks.md | Modified | +7/-7 | Added `"auto"` to `permission_mode` field values |
| how-claude-code-works.md | Modified | +1/-0 | Added auto mode to Shift+Tab mode list |
| channels-reference.md | Modified | +3/-3 | Added iMessage to supported channels list and pairing flow notes |
| sub-agents.md | Modified | +3/-3 | Updated permission mode links to new page |
| remote-control.md | Modified | +1/-1 | Updated permission mode link to new page |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-24*
