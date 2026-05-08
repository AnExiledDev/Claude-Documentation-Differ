# Claude Code Documentation Changes — 2026-03-30

## Summary

The primary change is the addition of a new `computer-use.md` page documenting CLI-based computer use (macOS screen and app control), which was previously only available in the Desktop app. Accompanying this are targeted clarifications to `--permission-mode` flag behavior, `bypassPermissions` mode carve-outs, and voice dictation data handling.

---

## Significant Changes

### New Feature: Computer Use in the CLI

- **Computer use now available from the CLI**: A full documentation page covers enabling Claude to control native macOS apps directly from the terminal via the built-in `computer-use` MCP server. Previously, computer use was documented only for the Desktop app.

  > "Computer use lets Claude open apps, control your screen, and work on your machine the way you would. From the CLI, Claude can compile a Swift app, launch it, click through every button, and screenshot the result, all in the same conversation where it wrote the code."

  Key details from the new page:
  - Requires **Pro or Max plan**, Claude Code **v2.1.85 or later**, and an **interactive session** (not available with `-p`)
  - **macOS only** — not available on Linux or Windows
  - Not available with third-party providers (Bedrock, Vertex AI, Foundry) — requires a claude.ai account
  - Enabled per-project via `/mcp` → select `computer-use` → Enable
  - Requires two macOS permissions: **Accessibility** and **Screen Recording**
  - Uses a **machine-wide lock** — only one Claude session can use computer use at a time
  - Apps are hidden while Claude works; terminal window is excluded from screenshots
  - Press `Esc` anywhere or `Ctrl+C` in terminal to abort immediately

  > "Unlike the sandboxed Bash tool, computer use runs on your actual desktop with access to the apps you approve."

  - *Implication*: Developers can now build, test, and debug native macOS and iOS Simulator apps end-to-end from the CLI without switching to the Desktop app.
  - *Source*: [Computer Use (CLI)](https://code.claude.com/docs/en/computer-use.md)

### Permission Modes: `bypassPermissions` Carve-outs Documented

- **`bypassPermissions` mode no longer skips all checks**: The description was updated to specify which paths still prompt even in bypass mode.

  > "`bypassPermissions` mode disables permission prompts and safety checks. Tool calls execute immediately, except for writes to `.git`, `.vscode`, and `.idea`, which still prompt to prevent accidental corruption of repository state and local configuration. Writes to `.claude` also prompt, except for `.claude/commands`, `.claude/agents`, and `.claude/skills` where Claude routinely creates skills, subagents, and commands."

  - *Implication*: Developers relying on `bypassPermissions` for full automation should be aware that writes to `.git`, `.vscode`, `.idea`, and most `.claude` paths will still generate interactive prompts.
  - *Source*: [Permission Modes](https://code.claude.com/docs/en/permission-modes.md)

### CLI Reference: Flag Descriptions Clarified

- **`--allow-dangerously-skip-permissions` behavior reworded**: The description now explains the flag adds `bypassPermissions` to the `Shift+Tab` mode cycle rather than "enabling it as an option without activating it."

  > "Add `bypassPermissions` to the `Shift+Tab` mode cycle without starting in it. Lets you begin in a different mode like `plan` and switch to `bypassPermissions` later."

  - *Implication*: Clarifies the flag's purpose for users composing it with `--permission-mode`.

- **`--dangerously-skip-permissions` now described as equivalent to `--permission-mode bypassPermissions`**: Previously described only as "skip permission prompts (use with caution)."

  > "Skip permission prompts. Equivalent to `--permission-mode bypassPermissions`."

- **`--permission-mode` now enumerates valid values**: The flag description now lists all accepted values and notes it overrides `defaultMode` from settings files.

  > "Accepts `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, or `bypassPermissions`. Overrides `defaultMode` from settings files"

  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

### Settings: `defaultMode` Valid Values Listed

- **`defaultMode` setting now documents all valid values**: Matches the new `--permission-mode` documentation and notes the CLI flag override relationship.

  > "Valid values: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. The `--permission-mode` CLI flag overrides this setting for a single session"

  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Voice Dictation: Audio Handling Clarified

- **Audio processing disclosure added**: The requirements section now explicitly states that audio is streamed to Anthropic's servers and is not processed locally, with a link to the data usage page.

  > "Voice dictation streams your recorded audio to Anthropic's servers for transcription. Audio is not processed locally. [...] See data usage for how Anthropic handles your data."

  - *Implication*: Users in sensitive environments should be aware that voice dictation audio leaves the local machine.
  - *Source*: [Voice Dictation](https://code.claude.com/docs/en/voice-dictation.md)

### Dev Container Extension Name Updated

- **Command Palette command corrected**: The devcontainer setup instructions updated "Remote-Containers: Reopen in Container" to "Dev Containers: Reopen in Container" and linked the extension by its current Marketplace name ("Dev Containers extension").
  - *Implication*: Users following the setup guide will now see matching command names in VS Code.
  - *Source*: [Dev Container](https://code.claude.com/docs/en/devcontainer.md)

---

## New Pages

- **[computer-use.md](https://code.claude.com/docs/en/computer-use.md)** — Full guide to CLI-based computer use on macOS: enabling the `computer-use` MCP server, per-session app approvals, the machine-wide lock model, safety guardrails, example workflows (native build validation, layout bug reproduction, iOS Simulator testing), and a comparison table vs. the Desktop app.

---

## Changelog Entry (v2.1.87)

- **Fixed**: Messages in Cowork Dispatch not getting delivered (March 29, 2026)
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

## Notable Details

- The `desktop.md` CLI vs. Desktop comparison table previously listed computer use as "Not available" for the CLI. It now reads "[Enable via `/mcp`](/en/computer-use) on macOS", confirming feature parity on macOS for Pro/Max CLI users.
- The `sandboxing.md` reference to "Computer use on Desktop" was broadened to "Computer use" with links to both CLI and Desktop pages — reflecting that the feature now spans both surfaces.
- The `platforms.md` CLI platform entry now mentions "computer use on Pro and Max" alongside the Agent SDK, elevating it to a headline CLI capability.
- Total documented pages increased from 72 to 73 with the addition of `computer-use.md`.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| computer-use.md | New | +205 | Full CLI computer use guide for macOS |
| cli-reference.md | Modified | +3/-3 | Clarified `--allow-dangerously-skip-permissions`, `--dangerously-skip-permissions`, and `--permission-mode` flag descriptions |
| permission-modes.md | Modified | +1/-1 | Documented `.git`, `.vscode`, `.idea`, `.claude` write carve-outs in `bypassPermissions` mode |
| platforms.md | Modified | +2/-1 | Added computer use to CLI platform entry and Integrations list |
| voice-dictation.md | Modified | +1/-1 | Disclosed server-side audio processing; linked data-usage page |
| settings.md | Modified | +1/-1 | Listed valid `defaultMode` values; noted `--permission-mode` override behavior |
| devcontainer.md | Modified | +2/-2 | Updated extension name and Command Palette command to "Dev Containers" |
| desktop.md | Modified | +1/-1 | Updated CLI computer use row from "Not available" to CLI enable instructions |
| sandboxing.md | Modified | +1/-1 | Broadened "Computer use on Desktop" reference to cover CLI as well |
| changelog.md | Modified | +4/-0 | Added v2.1.87 entry: fixed Dispatch message delivery |
| chrome.md | Modified | +1/-0 | Added "See also" link to new computer-use page |

---

*Generated from Claude Code CLI documentation changes detected on 2026-03-30*
