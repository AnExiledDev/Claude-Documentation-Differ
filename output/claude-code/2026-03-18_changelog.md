# Claude Code Documentation Changes — 2026-03-18

## Summary

This update introduces push-to-talk voice dictation as a major new feature, adding a dedicated documentation page and touching eight existing pages across commands, keybindings, settings, and interactive mode. A second significant change introduces `${CLAUDE_PLUGIN_DATA}`, a persistent data directory for plugins that survives updates, alongside a new `--keep-data` flag for plugin uninstall. Several smaller clarifications address permissions, Windows path handling, network access URLs, and an environment variable rename affecting Bedrock and Vertex AI users.

---

## Significant Changes

### Features

#### Voice Dictation (New)

A full push-to-talk voice dictation system is now documented and available in Claude Code v2.1.69+.

> Hold a key and speak to dictate your prompts. Your speech is transcribed live into the prompt input, so you can mix voice and typing in the same message. Enable dictation with `/voice`. The default push-to-talk key is `Space`.

Key specifics:

- **Activation**: Run `/voice` to toggle. State persists across sessions; written to `voiceEnabled` in user settings.
- **Account requirement**: Uses a streaming speech-to-text service that requires a Claude.ai account. Not available with direct API key auth, Amazon Bedrock, Google Vertex AI, or Microsoft Foundry.
- **Local only**: Does not work in remote environments (Claude Code on the web, SSH sessions). In WSL, requires WSLg (WSL2 on Windows 11).
- **Hold-to-record mechanics**: Space-bar hold detection relies on key-repeat events. There is a brief warmup period before recording begins; rebinding to a modifier combination (e.g., `meta+k`) skips warmup entirely.
- **Transcription**: Streaming, tuned for coding vocabulary; adds current project name and git branch as recognition hints automatically.
- **Language**: Dictation uses the existing `language` setting (same one that controls Claude's response language). Supports 20 languages. Falls back to English if the configured language is unsupported.
- **Linux fallback**: If the native audio module fails to load, falls back to `arecord` (ALSA) or `rec` (SoX).
- **Rebinding**: `voice:pushToTalk` action in the `Chat` context, bindable in `~/.claude/keybindings.json`.

> Voice dictation requires Claude Code v2.1.69 or later. Check your version with `claude --version`.

- *Implication*: Developers can dictate prompts instead of typing; particularly useful for longer, free-form instructions. The Claude.ai account requirement excludes enterprise users authenticated via API key or cloud provider integrations.
- *Source*: [Voice dictation](https://code.claude.com/docs/en/voice-dictation.md)

---

### Configuration

#### Plugin Persistent Data Directory (`${CLAUDE_PLUGIN_DATA}`)

Plugins now have a dedicated persistent data directory that survives plugin updates, distinct from `${CLAUDE_PLUGIN_ROOT}` which changes on each update.

> **`${CLAUDE_PLUGIN_DATA}`**: a persistent directory for plugin state that survives updates. Use this for installed dependencies such as `node_modules` or Python virtual environments, generated code, caches, and any other files that should persist across plugin versions. The directory is created automatically the first time this variable is referenced.

Directory path convention: `~/.claude/plugins/data/{id}/`, where `{id}` is the plugin identifier with non-alphanumeric characters (except `_` and `-`) replaced by `-`. Example: a plugin installed as `formatter@my-marketplace` → `~/.claude/plugins/data/formatter-my-marketplace/`.

The recommended pattern for managing dependencies that need to be reinstalled on update uses a `SessionStart` hook that diffs the bundled `package.json` against a copy in the data directory:

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
      }]
    }]
  }
}
```

> The data directory is deleted automatically when you uninstall the plugin from the last scope where it is installed. The `/plugin` interface shows the directory size and prompts before deleting. The CLI deletes by default; pass `--keep-data` to preserve it.

- *Implication*: Plugin authors can now install language-runtime dependencies (e.g., `node_modules`, Python venvs) once and reuse them across sessions and version updates, without re-running install on every plugin update.
- *Source*: [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md)

#### `plugin uninstall --keep-data` Flag (New)

A new `--keep-data` option for `claude plugin uninstall` preserves the plugin's `${CLAUDE_PLUGIN_DATA}` directory when removing the plugin.

> By default, uninstalling from the last remaining scope also deletes the plugin's `${CLAUDE_PLUGIN_DATA}` directory. Use `--keep-data` to preserve it, for example when reinstalling after testing a new version.

- *Implication*: Useful for iterative plugin development or when reinstalling a newer version without losing cached dependencies.
- *Source*: [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md)

#### `voiceEnabled` Setting (New)

A new user setting controls voice dictation state:

> `voiceEnabled`: Enable push-to-talk voice dictation. Written automatically when you run `/voice`. Requires a Claude.ai account.

- *Implication*: Can be pre-configured in user settings; `/voice` simply writes this setting rather than managing its own state separately.
- *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

#### `language` Setting Now Controls Dictation Language

The existing `language` setting's description has been extended:

> Also sets the voice dictation language.

- *Implication*: There is no separate voice language setting. Users who have already configured `language` for response language automatically get matching dictation language.
- *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

#### Managed CLAUDE.md vs. Managed Settings Guidance

The memory/CLAUDE.md documentation now includes an explicit comparison table clarifying when to use managed settings versus a managed CLAUDE.md for organizational deployments:

> A managed CLAUDE.md and managed settings serve different purposes. Use settings for technical enforcement and CLAUDE.md for behavioral guidance.

| Concern | Configure in |
|---|---|
| Block specific tools, commands, or file paths | Managed settings: `permissions.deny` |
| Enforce sandbox isolation | Managed settings: `sandbox.enabled` |
| Environment variables and API provider routing | Managed settings: `env` |
| Authentication method and organization lock | Managed settings: `forceLoginMethod`, `forceLoginOrgUUID` |
| Code style and quality guidelines | Managed CLAUDE.md |
| Data handling and compliance reminders | Managed CLAUDE.md |
| Behavioral instructions for Claude | Managed CLAUDE.md |

> Settings rules are enforced by the client regardless of what Claude decides to do. CLAUDE.md instructions shape Claude's behavior but are not a hard enforcement layer.

- *Implication*: Organizations deploying Claude Code at scale now have clear authoritative guidance on the enforcement boundary between settings and CLAUDE.md.
- *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

---

### Permissions

#### Read/Edit Deny Rules Do Not Apply to Bash Subprocesses

A new Warning callout clarifies a common misconception about permission rule scope:

> Read and Edit deny rules apply to Claude's built-in file tools, not to Bash subprocesses. A `Read(./.env)` deny rule blocks the Read tool but does not prevent `cat .env` in Bash. For OS-level enforcement that blocks all processes from accessing a path, enable the sandbox.

- *Implication*: Teams relying on `Read` deny rules for security must also enable sandboxing to prevent Bash-level bypasses.
- *Source*: [Configure permissions](https://code.claude.com/docs/en/permissions.md)

#### Windows Path Normalization for Permission Rules

Documentation now explicitly covers how Windows paths are handled in permission patterns:

> On Windows, paths are normalized to POSIX form before matching. `C:\Users\alice` becomes `/c/Users/alice`, so use `//c/**/.env` to match `.env` files anywhere on that drive. To match across all drives, use `//**/.env`.

- *Implication*: Windows users writing permission rules must account for this normalization; the `//` absolute-path prefix convention applies using the drive letter as the first path component.
- *Source*: [Configure permissions](https://code.claude.com/docs/en/permissions.md)

---

### Network & Infrastructure

#### Native Installer URLs Added to Network Requirements

The network configuration page now documents two additional URLs required by the native installer and update mechanism:

> The native installer and update checks also require the following URLs. If you install Claude Code through npm or manage your own binary distribution, end users may not need access:
> - `downloads.claude.ai`: CDN hosting the install script, version pointers, manifests, and executables
> - `storage.googleapis.com`: legacy download bucket, deprecation in progress

- *Implication*: Enterprise firewall allowlists must include `downloads.claude.ai` for auto-update to function. `storage.googleapis.com` is flagged as being deprecated on the Anthropic side — organizations that have added it for legacy access can plan to remove it eventually.
- *Source*: [Enterprise network configuration](https://code.claude.com/docs/en/network-config.md)

---

### Breaking / Renamed

#### `ANTHROPIC_SMALL_FAST_MODEL` Renamed to `ANTHROPIC_DEFAULT_HAIKU_MODEL`

The environment variable for specifying a secondary fast model has been renamed in both the Amazon Bedrock and Google Vertex AI documentation:

```bash
# Before
export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# After
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

- *Implication*: Users relying on `ANTHROPIC_SMALL_FAST_MODEL` in their Bedrock or Vertex AI configurations should update to the new variable name. The old name is no longer referenced in documentation.
- *Source*: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md), [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai.md)

---

## New Pages

- **[voice-dictation.md](https://code.claude.com/docs/en/voice-dictation.md)** — Complete reference for push-to-talk voice dictation: requirements, enabling/disabling, recording mechanics, language configuration, push-to-talk key rebinding, and troubleshooting. Covers macOS, Linux, Windows, and WSL specifics.

---

## Notable Details

- The `${CLAUDE_PLUGIN_ROOT}` description in hooks documentation was updated from "plugin's root directory" to "plugin's **installation** directory" with the added note: "Changes on each plugin update." This wording shift is meaningful — it signals to plugin authors that any files written to this path will be lost on update.
- The MCP plugin documentation now explicitly lists both `${CLAUDE_PLUGIN_ROOT}` (for bundled files) and `${CLAUDE_PLUGIN_DATA}` (for persistent state), replacing a single-variable mention. This affects `mcp.md` and `plugin-marketplaces.md` in addition to the main `plugins-reference.md`.
- Voice dictation adds a new `voice:pushToTalk` action to the `Chat` keybinding context. Because hold detection uses key-repeat, the docs specifically warn against binding a bare letter key (e.g., `v`) as it will type during the warmup period. The recommendation is to use `Space` (default) or a modifier combo like `meta+k`.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| voice-dictation.md | New | +138 | Full reference for push-to-talk voice dictation feature |
| plugins-reference.md | Modified | +57/-5 | New `${CLAUDE_PLUGIN_DATA}` persistent directory, `--keep-data` uninstall flag |
| memory.md | Modified | +14/-0 | Managed CLAUDE.md vs. managed settings comparison table |
| keybindings.md | Modified | +8/-0 | New "Voice actions" section with `voice:pushToTalk` action |
| interactive-mode.md | Modified | +6/-0 | New "Voice input" shortcut table (Hold Space for push-to-talk) |
| permissions.md | Modified | +6/-0 | Warning about Bash subprocess bypass; Windows path normalization note |
| network-config.md | Modified | +5/-0 | `downloads.claude.ai` and `storage.googleapis.com` added to allowlist requirements |
| settings.md | Modified | +2/-1 | New `voiceEnabled` setting; `language` setting updated to mention voice dictation |
| hooks.md | Modified | +2/-1 | `${CLAUDE_PLUGIN_ROOT}` clarified; `${CLAUDE_PLUGIN_DATA}` documented |
| google-vertex-ai.md | Modified | +2/-2 | `ANTHROPIC_SMALL_FAST_MODEL` → `ANTHROPIC_DEFAULT_HAIKU_MODEL` |
| commands.md | Modified | +1/-0 | `/voice` command added to commands reference |
| mcp.md | Modified | +1/-1 | Plugin MCP env vars updated to include `${CLAUDE_PLUGIN_DATA}` |
| amazon-bedrock.md | Modified | +1/-1 | `ANTHROPIC_SMALL_FAST_MODEL` → `ANTHROPIC_DEFAULT_HAIKU_MODEL` |
| plugin-marketplaces.md | Modified | +1/-1 | `${CLAUDE_PLUGIN_ROOT}` note updated to reference `${CLAUDE_PLUGIN_DATA}` |

---

*Generated from Claude Code CLI documentation changes detected on 2026-03-18*
