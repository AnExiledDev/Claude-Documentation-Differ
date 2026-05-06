# Claude Code Documentation Changes — 2026-05-06

## Summary

15 documentation pages were updated with no new or removed pages. The most significant additions are a new `autoMemoryEnabled` setting, a `pathPattern` marketplace allowlist type, and split-pane session view for Desktop. Several plugin-related corrections fix naming conventions and schema formats.

## Significant Changes

### Features

- **Desktop split-pane session view**: Holding **Cmd** (macOS) or **Ctrl** (Windows) and clicking a sidebar session now opens it in a second pane alongside the current one. Closing the pane uses **Cmd+\\** / **Ctrl+\\**.
  > "To view two sessions at once, hold **Cmd** on macOS or **Ctrl** on Windows and click a session in the sidebar. The session opens in a second pane alongside the one you already have open. While the split is active, clicking another sidebar session replaces whichever pane has focus."
  - *Implication*: Developers can now compare sessions or monitor a background task alongside active work without switching contexts.
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

- **`autoMemoryEnabled` setting**: New boolean setting that fully disables auto memory reads and writes when set to `false`. Can also be toggled via `/memory` during a session.
  > "`autoMemoryEnabled` — Enable auto memory. When `false`, Claude does not read from or write to the auto memory directory. Default: `true`. You can also toggle this with `/memory` during a session"
  - *Implication*: Useful for shared or ephemeral environments where persistent auto memory is undesirable.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`pathPattern` marketplace allowlist source type**: A new allowlist entry type for plugin marketplaces that uses regex matching against filesystem paths, complementing the existing `hostPattern` for network sources.
  > "Fields: `pathPattern` (required: regex pattern matched against the `path` field of `file` and `directory` sources). Use path pattern matching to allow filesystem-based marketplaces alongside `hostPattern` restrictions for network sources. Set `\".*\"` to allow all local paths, or a narrower pattern to restrict to specific directories."
  - *Implication*: Enterprises can now write allowlist policies that cover local/file-based plugin marketplaces with the same regex precision as network-based sources.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Configuration

- **`extraKnownMarketplaces` schema updated**: The `source` field in `extraKnownMarketplaces` entries is now a nested object rather than a flat property alongside `repo`.

  Before:
  ```json
  "acme-tools": {
    "source": "github",
    "repo": "acme-corp/claude-plugins"
  }
  ```
  After:
  ```json
  "acme-tools": {
    "source": {
      "source": "github",
      "repo": "acme-corp/claude-plugins"
    }
  }
  ```
  - *Implication*: Users with custom marketplace config in `settings.json` must update to the nested format.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`/focus` command now linkable to `viewMode` setting**: The `/focus` command description now mentions that the persisted selection can be overridden via the `viewMode` setting.
  > "The selection persists across sessions; set `viewMode` in settings to override it."
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

### Plugin System

- **`rust-lsp` plugin renamed to `rust-analyzer-lsp`**: The Rust LSP plugin identifier in the plugins reference table has been corrected.

  | Before | After |
  |--------|-------|
  | `rust-lsp` | `rust-analyzer-lsp` |

  - *Implication*: Installations or scripts referencing `rust-lsp` by name will need to be updated.
  - *Source*: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

- **Plugin skill invocation namespaced by plugin name**: The marketplace walkthrough now correctly shows that skills are invoked with the plugin name as a namespace prefix, not as bare skill names.
  > "Plugin skills are namespaced with the plugin name."
  - The example invocation changed from `/quality-review` to `/quality-review-plugin:quality-review`.
  - *Implication*: Developers creating or documenting custom plugins should use the `plugin-name:skill-name` format in instructions.
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

### Network & Security

- **`raw.githubusercontent.com` added to required network access list**: This domain is now listed as required for the `/release-notes` command changelog feed and plugin marketplace install counts.
  > "`raw.githubusercontent.com` — Changelog feed for `/release-notes` and the release notes shown after updating; plugin marketplace install counts"
  - *Implication*: Firewall or proxy allowlists in enterprise environments need to include this host for release notes and marketplace features to work.
  - *Source*: [Network Configuration](https://code.claude.com/docs/en/network-config.md)

- **System CA store note removed from network docs and `CLAUDE_CODE_CERT_STORE` description**: The previous note stating that system CA store integration requires the native binary and is unavailable in Node.js runtime has been removed from both `network-config.md` and the `env-vars.md` table entry.
  - *Implication*: The native binary restriction on system CA store merging may have been lifted; operators relying on this caveat should retest.
  - *Source*: [Network Configuration](https://code.claude.com/docs/en/network-config.md), [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **Accept Edits mode explicitly lists auto-approved Bash commands**: The security and permissions pages now name the specific Bash commands that Accept Edits auto-approves.
  > "Auto-approves file edits and a fixed set of filesystem Bash commands like `mkdir`, `touch`, `rm`, `mv`, `cp`, and `sed` for paths in the working directory. Other Bash commands and out-of-scope paths still prompt"
  - *Source*: [Security](https://code.claude.com/docs/en/security.md)

### Troubleshooting & Clarifications

- **New troubleshooting entry: sessions hanging during setup**: `web-quickstart.md` adds a dedicated section explaining why new web sessions stall at the setup script step and how to fix it.
  > "If new sessions stall on the setup script step or fail with a generic container error before the script finishes, the script is likely exceeding the roughly five-minute time budget for building the environment cache."
  - Recommended fixes: run independent installs in parallel with `&`/`wait`, move large downloads to a `SessionStart` hook, remove long retry sleeps.
  - *Source*: [Web Quickstart](https://code.claude.com/docs/en/web-quickstart.md)

- **Web setup script 5-minute guidance added**: The main web documentation page now also surfaces this advice inline, with a forward reference to `SessionStart` hooks for downloads that won't fit.
  - *Source*: [Claude Code on the Web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

- **Plan mode description clarified**: The `plan` permission mode description is more precise about what Claude can do.
  > Before: "Claude can analyze but not modify files or execute commands"
  > After: "Claude reads files and runs read-only shell commands to explore but does not edit your source files"
  - *Implication*: Plan mode permits read-only shell commands; it is not a fully command-free mode.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

- **Sandbox filesystem restriction clarified**: The description of how sandbox filesystem boundaries are composed is now more precise.
  > "Filesystem restrictions in the sandbox combine the `sandbox.filesystem` settings with Read and Edit deny rules; both are merged into the final sandbox boundary"
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

- **Platforms page updated for provider support matrix**: The comparison paragraph now documents that VS Code supports third-party providers, and Desktop enterprise deployments support Vertex AI and gateway providers — but Bedrock and Foundry require CLI or VS Code.
  > "Third-party providers also work in VS Code. Enterprise Desktop deployments support Vertex AI and gateway providers; for Bedrock or Foundry, use the CLI or VS Code instead of Desktop."
  - *Source*: [Platforms](https://code.claude.com/docs/en/platforms.md)

- **Vim mode: `Space` key documented**: The interactive mode vim keybinding table now includes `Space` as an alias for move-right.
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

- **SSL error messaging de-coupled from Node.js**: Error documentation now refers to "the runtime" and "Claude Code" rather than "Node.js" in connection failure and SSL certificate error descriptions.
  - *Source*: [Errors](https://code.claude.com/docs/en/errors.md)

- **Hooks `ok`/`reason` field descriptions tightened**: The LLM hook response table now reads "true to allow, false to block. See the per-event behavior below" and "Explanation for the decision" (previously "Explanation for the block").
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| settings.md | Modified | +18/-4 | `autoMemoryEnabled` setting added; `extraKnownMarketplaces` schema nested; `pathPattern` allowlist type added |
| web-quickstart.md | Modified | +10/-0 | New troubleshooting section for setup script timeout/hang |
| network-config.md | Modified | +9/-12 | `raw.githubusercontent.com` added to allowlist; system CA note removed |
| hooks.md | Modified | +4/-4 | Hook response field descriptions tightened |
| errors.md | Modified | +3/-3 | Node.js references replaced with runtime-agnostic wording |
| claude-code-on-the-web.md | Modified | +2/-0 | 5-minute setup script budget guidance added inline |
| desktop.md | Modified | +2/-0 | Split-pane session view documented |
| permissions.md | Modified | +2/-2 | Plan mode and sandbox filesystem restriction descriptions clarified |
| plugin-marketplaces.md | Modified | +6/-6 | Skill namespacing fix; invocation example corrected to plugin-name:skill-name |
| plugins-reference.md | Modified | +5/-5 | `rust-lsp` renamed to `rust-analyzer-lsp` |
| commands.md | Modified | +1/-1 | `/focus` description notes `viewMode` setting override |
| env-vars.md | Modified | +1/-1 | `CLAUDE_CODE_CERT_STORE` description simplified; native binary caveat removed |
| interactive-mode.md | Modified | +1/-0 | `Space` key added to vim mode keybindings |
| platforms.md | Modified | +1/-1 | Provider support matrix updated for VS Code, Desktop, CLI |
| security.md | Modified | +1/-1 | Accept Edits mode lists specific auto-approved Bash commands |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-06*
