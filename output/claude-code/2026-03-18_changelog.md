# Claude Code Documentation Changes — 2026-03-18

## Summary

This update delivers substantive clarifications across authentication, permissions, and feedback tooling. The most significant additions are: a new "Authentication precedence" section documenting the explicit 5-step credential resolution order, expanded Linux/Windows credential storage details, and a rename of the `/bug` command to `/feedback` (along with its env var `DISABLE_BUG_COMMAND` → `DISABLE_FEEDBACK_COMMAND`) propagated across six pages. A new troubleshooting entry documents the common failure mode where an `ANTHROPIC_API_KEY` env var silently overrides an active subscription. The `bypassPermissions` mode description is now precise about which directories are still protected. Two global UI settings (`showTurnDuration`, `terminalProgressBarEnabled`) are clarified as belonging in `~/.claude.json` rather than `settings.json`.

---

## Significant Changes

### Authentication

- **New "Authentication precedence" section**: The authentication page gains an explicit ordered list documenting how Claude Code resolves credentials when multiple are present.
  > When multiple credentials are present, Claude Code chooses one in this order:
  > 1. Cloud provider credentials (`CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX`, or `CLAUDE_CODE_USE_FOUNDRY`)
  > 2. `ANTHROPIC_AUTH_TOKEN` environment variable — sent as `Authorization: Bearer`
  > 3. `ANTHROPIC_API_KEY` environment variable — sent as `X-Api-Key`
  > 4. `apiKeyHelper` script output
  > 5. Subscription OAuth credentials from `/login`
  - *Implication*: Developers with both an API key and an active subscription now have a documented explanation for why the API key takes precedence and how to recover from broken auth: `unset ANTHROPIC_API_KEY`, then verify with `/status`.
  - *Source*: [Authentication](https://code.claude.com/docs/en/authentication.md)

- **Credential storage locations expanded for Linux and Windows**: Previously, only macOS Keychain storage was documented. The credential storage bullet now reads:
  > On Linux and Windows, credentials are stored in `~/.claude/.credentials.json`, or under `$CLAUDE_CONFIG_DIR` if that variable is set. On Linux, the file is written with mode `0600`; on Windows, it inherits the access controls of your user profile directory.
  - *Implication*: Linux and Windows users can now audit exactly where credentials live. The `$CLAUDE_CONFIG_DIR` override path is explicitly surfaced for the first time.
  - *Source*: [Authentication](https://code.claude.com/docs/en/authentication.md)

- **Claude Code on the Web always uses subscription credentials**: A new clarifying sentence documents that `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` set in the sandbox environment do not override subscription credentials on the web client.
  - *Implication*: Developers running cloud sessions who have API key env vars set in their sandbox will not see unexpected credential switching.
  - *Source*: [Authentication](https://code.claude.com/docs/en/authentication.md)

---

### Command Rename: `/bug` → `/feedback`

- **`/bug` command renamed to `/feedback`** across data-usage, security, env-vars, and troubleshooting pages. The associated opt-out environment variable was also renamed:
  - Old: `DISABLE_BUG_COMMAND`
  - New: `DISABLE_FEEDBACK_COMMAND`

  The data-usage table's service row was updated from `Claude API (/bug reports)` to `Claude API (/feedback reports)`. The section heading in `data-usage.md` changed from `### Feedback using the /bug command` to `### Feedback using the /feedback command`.

  > If you choose to send us feedback about Claude Code using the `/feedback` command, we may use your feedback to improve our products and services. Transcripts shared via `/feedback` are retained for 5 years.

  - *Implication*: Any shell scripts, CI configurations, or documentation that reference `DISABLE_BUG_COMMAND` or instruct users to run `/bug` must be updated to `DISABLE_FEEDBACK_COMMAND` and `/feedback` respectively.
  - *Source*: [Data Usage](https://code.claude.com/docs/en/data-usage.md), [Security](https://code.claude.com/docs/en/security.md), [Environment Variables](https://code.claude.com/docs/en/env-vars.md), [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

---

### Permissions

- **`bypassPermissions` mode now documents explicit carve-outs**: Descriptions across permissions.md, sub-agents.md, desktop.md, and cli-reference.md changed from "skips all permission prompts" to a precise statement listing which directories still require approval.
  > `bypassPermissions` mode skips permission prompts. Writes to `.git`, `.claude`, `.vscode`, and `.idea` directories still prompt for confirmation to prevent accidental corruption of repository state and local configuration. Writes to `.claude/commands`, `.claude/agents`, and `.claude/skills` are exempt and do not prompt, because Claude routinely writes there when creating skills, subagents, and commands.
  - *Implication*: Users and admins relying on `bypassPermissions` now know which directories still trigger manual approval. The carve-out for `.claude/commands`, `.claude/agents`, and `.claude/skills` (no prompt) is an important behavioral clarification for automated workflows.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md), [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

- **`--dangerously-skip-permissions` CLI flag description updated**: Changed from "Skip all permission prompts" to "Skip permission prompts. See permission modes for what this does and does not skip" with a link to the permissions documentation.
  - *Implication*: The flag no longer implies a total bypass; users are directed to the full exception list.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

---

### Troubleshooting

- **New entry: "This organization has been disabled" with an active subscription**: A new troubleshooting section explains the common failure mode where an `ANTHROPIC_API_KEY` set in a shell profile overrides subscription OAuth credentials.
  > If you see `API Error: 400 ... "This organization has been disabled"` despite having an active Claude subscription, an `ANTHROPIC_API_KEY` environment variable is overriding your subscription. This commonly happens when an old API key from a previous employer or project is still set in your shell profile.
  >
  > To use your subscription instead:
  > ```bash
  > unset ANTHROPIC_API_KEY
  > claude
  > ```
  > Check `~/.zshrc`, `~/.bashrc`, or `~/.profile` for `export ANTHROPIC_API_KEY=...` lines and remove them to make the change permanent. Run `/status` inside Claude Code to confirm which authentication method is active.
  - *Implication*: This is one of the most confusing failure modes for users transitioning from API key usage to subscription plans. The cause (precedence order), fix (`unset`), and verification step (`/status`) are now all documented in one place. A cross-reference to the new Authentication precedence section is included.
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

---

### Settings

- **New "Global config settings" section: two keys moved out of `settings.json`**: `showTurnDuration` and `terminalProgressBarEnabled` were previously listed in the main `settings.json` available-settings table. They are now documented separately under a "Global config settings" section with an explicit warning:
  > These display preferences are stored in `~/.claude.json` rather than `settings.json`. Adding them to `settings.json` will trigger a schema validation error.

  | Key | Description | Default |
  |-----|-------------|---------|
  | `showTurnDuration` | Show turn duration messages after responses ("Cooked for 1m 6s"). Edit `~/.claude.json` directly to change. | `true` |
  | `terminalProgressBarEnabled` | Show terminal progress bar in supported terminals (Windows Terminal, iTerm2). Appears in `/config` as **Terminal progress bar**. | `true` |

  - *Implication*: Developers who previously added these keys to `settings.json` (e.g., to disable `showTurnDuration`) will now encounter schema validation errors. They must move those keys to `~/.claude.json` instead.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

---

### Hooks

- **`PostCompact` hook event added alongside `PreCompact`**: Both `hooks.md` and `hooks-guide.md` now document the `PostCompact` event in their reference tables.
  > `PreCompact`, `PostCompact` — what triggered compaction: `manual`, `auto`
  - *Implication*: The `PostCompact` event was previously undocumented. Hook scripts that need to react after conversation compaction (e.g., to log a summary or trigger a notification) can now reliably use this event.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md), [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)

---

### Sub-agents

- **`/agent` command renamed to `/agents`**: The sub-agents quickstart walkthrough was updated to use `/agents`.

  Old: _"This walkthrough guides you through creating a user-level subagent with the `/agent` command."_
  New: _"This walkthrough guides you through creating a user-level subagent with the `/agents` command."_

  The step title also changed from "Create a new user-level agent" to "Choose a location" with updated UX copy reflecting a new location picker ("Personal" vs. project scope). The save interaction also changed: previously "Press `e` to open in editor", now "Press `s` or `Enter` to save, or press `e` to save and edit the file in your editor."
  - *Implication*: `/agent` is no longer the documented command; use `/agents`. The non-interactive `claude agents` CLI command (listing configured subagents) is unchanged.
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

---

### Overview

- **Log analysis CLI example changed from streaming to fixed-count**: The accordion demonstrating CLI piping was updated.

  Old:
  ```bash
  # Monitor logs and get alerted
  tail -f app.log | claude -p "Slack me if you see any anomalies"
  ```
  New:
  ```bash
  # Analyze recent log output
  tail -200 app.log | claude -p "Slack me if you see any anomalies"
  ```
  - *Implication*: `tail -f` follows the file indefinitely, making it impractical for a one-shot `claude -p` invocation. `tail -200` reads the last 200 lines and exits — a more realistic and correct pattern for non-interactive use.
  - *Source*: [Overview](https://code.claude.com/docs/en/overview.md)

---

### Terminal Configuration

- **Option+Enter setup instructions split into separate sections**: Previously a single "For iTerm2 and VS Code terminal" heading covered both. These are now two distinct sections.
  - "For iTerm2" covers the existing Esc+ key binding approach.
  - "For VS Code terminal" now has its own instruction: set `"terminal.integrated.macOptionIsMeta": true` in VS Code settings.
  - *Implication*: The combined heading obscured that the configuration steps differ between the two apps. Users configuring VS Code terminal now have a clear, dedicated instruction.
  - *Source*: [Terminal Config](https://code.claude.com/docs/en/terminal-config.md)

---

### VS Code Extension

- **`allowDangerouslySkipPermissions` setting description now links to permission modes docs**: The extension settings table updated the description to add a cross-reference.

  Old: `Bypass all permission prompts. **Use with extreme caution.**`
  New: `Bypass permission prompts. **Use with extreme caution.** See [permission modes](/en/permissions#permission-modes)`
  - *Implication*: The word "all" was removed (aligning with the broader `bypassPermissions` clarification), and users now have a direct link to the exception list rather than assuming total bypass.
  - *Source*: [VS Code](https://code.claude.com/docs/en/vs-code.md)

---

## Notable Details

- **Code Review billing wording**: Minor precision improvement — "Reviews average $15-25" became "Each review averages $15-25 in cost, scaling with PR size, codebase complexity, and how many issues require verification." No dollar amounts changed.
- **`bypassPermissions` in the permissions table**: Old text: "Skips all permission prompts (requires safe environment, see warning below)". New text explicitly lists protected directories without requiring readers to consult a separate warning block.
- The `/bug` → `/feedback` rename propagated to six files: `data-usage.md`, `security.md`, `env-vars.md`, `troubleshooting.md`, and their in-table opt-out env vars. Any tooling that parses the opt-out variable name will need updating.
- `plugins-reference.md` received 1 line addition with no section changes (minor).

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `authentication.md` | Modified | +16 / -2 | New "Authentication precedence" section; Linux/Windows credential storage expanded |
| `troubleshooting.md` | Modified | +16 / -1 | New "This organization has been disabled" entry; `/bug` → `/feedback` |
| `vs-code.md` | Modified | +15 / -15 | `allowDangerouslySkipPermissions` updated; settings table reformatted with new description |
| `sub-agents.md` | Modified | +11 / -7 | `/agent` → `/agents` command; location picker UX updated; `bypassPermissions` warning refined |
| `data-usage.md` | Modified | +10 / -10 | `/bug` → `/feedback` rename; `DISABLE_BUG_COMMAND` → `DISABLE_FEEDBACK_COMMAND`; table updated |
| `permissions.md` | Modified | +8 / -8 | `bypassPermissions` description updated with explicit protected-directory carve-outs |
| `settings.md` | Modified | +9 / -2 | New "Global config settings" section; `showTurnDuration` and `terminalProgressBarEnabled` documented as `~/.claude.json` keys |
| `overview.md` | Modified | +7 / -7 | Log example changed from `tail -f` to `tail -200`; accordion title updated |
| `desktop.md` | Modified | +6 / -6 | `bypassPermissions` description updated to reference permission modes page |
| `terminal-config.md` | Modified | +5 / -1 | Option+Enter instructions split into separate iTerm2 and VS Code sections |
| `env-vars.md` | Modified | +4 / -3 | `DISABLE_BUG_COMMAND` → `DISABLE_FEEDBACK_COMMAND` |
| `hooks.md` | Modified | +1 / -1 | `PostCompact` added alongside `PreCompact` in event table |
| `hooks-guide.md` | Modified | +1 / -1 | `PostCompact` added alongside `PreCompact` in event table |
| `cli-reference.md` | Modified | +1 / -1 | `--dangerously-skip-permissions` description updated |
| `best-practices.md` | Modified | +1 / -1 | `/bug` → `/feedback` reference |
| `code-review.md` | Modified | +1 / -1 | Minor billing description rewording |
| `security.md` | Modified | +1 / -1 | `/bug` → `/feedback` reference |
| `plugins-reference.md` | Modified | +1 / -0 | Minor addition |

---

*Generated from Claude Code CLI documentation changes detected on 2026-03-18*
