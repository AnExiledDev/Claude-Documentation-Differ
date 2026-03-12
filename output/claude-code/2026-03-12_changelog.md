# Claude Code Documentation Changes — 2026-03-12

## Summary

The Claude Code changelog page was updated with the 2.1.74 release notes. This release adds two new features — actionable suggestions in the `/context` command and a configurable `autoMemoryDirectory` setting — along with 13 bug fixes covering memory leaks, MCP OAuth, policy enforcement, RTL text rendering, Windows LSP, and VS Code improvements. One behavioral change was made to `--plugin-dir` override precedence.

## Significant Changes

### Features

- **Enhanced `/context` command with actionable suggestions**: The `/context` command now analyzes and surfaces specific optimization tips alongside its report, identifying context-heavy tools, memory bloat, and capacity warnings.
  > `Added actionable suggestions to /context command — identifies context-heavy tools, memory bloat, and capacity warnings with specific optimization tips`
  - *Implication*: Developers working near context limits get guided recommendations rather than raw counts alone, making it easier to act on context warnings.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`autoMemoryDirectory` setting**: A new configuration key allows users to specify a custom directory for auto-memory file storage, overriding the default location.
  > `Added autoMemoryDirectory setting to configure a custom directory for auto-memory storage`
  - *Implication*: Teams or users who want auto-memory files in a project root, shared config location, or other non-default path can now configure this without workarounds.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Bug Fixes

- **Memory leak in streaming API responses (Node.js/npm)**: Streaming API response buffers were not released when the generator was terminated early, causing RSS memory to grow without bound over time.
  > `Fixed memory leak where streaming API response buffers were not released when the generator was terminated early, causing unbounded RSS growth on the Node.js/npm code path`
  - *Implication*: Long-running Claude Code sessions on the Node.js/npm distribution should see significantly reduced memory growth.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Managed policy ask rules bypass**: User allow rules and skill `allowed-tools` settings could silently override managed policy ask rules, undermining enterprise policy enforcement.
  > `Fixed managed policy ask rules being bypassed by user allow rules or skill allowed-tools`
  - *Implication*: Enterprise deployments relying on managed policies to require tool approval can now trust those rules are not overridden by user-level configuration.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Full model IDs silently ignored in agent config**: Full model identifiers (e.g. `claude-opus-4-5`) specified in agent frontmatter `model:` fields or `--agents` JSON were silently dropped, falling back to a default.
  > `Fixed full model IDs (e.g., claude-opus-4-5) being silently ignored in agent frontmatter model: field and --agents JSON config — agents now accept the same model values as --model`
  - *Implication*: Agent configurations that pin to a specific model version by full ID now behave as intended, matching the behavior of the `--model` flag.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **MCP OAuth port conflict hang**: MCP OAuth authentication would hang indefinitely if the localhost callback port was already in use by another process.
  > `Fixed MCP OAuth authentication hanging when the callback port is already in use`
  - *Implication*: MCP OAuth flows are now more robust when running multiple services on the same machine.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **MCP OAuth refresh loop broken on HTTP 200 error servers (e.g. Slack)**: After a refresh token expired on OAuth servers that signal errors with HTTP 200 responses (such as Slack), Claude Code would never prompt for re-authentication, leaving the MCP connection permanently broken.
  > `Fixed MCP OAuth refresh never prompting for re-auth after the refresh token expires, for OAuth servers that return errors with HTTP 200 (e.g. Slack)`
  - *Implication*: Slack MCP integrations and other non-standard OAuth servers will correctly surface a re-authentication prompt when sessions expire.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Voice mode silent failure on macOS native binary**: Voice mode failed without any error message on the macOS native binary when the terminal application had never been granted microphone access. The root cause was a missing `audio-input` entitlement in the binary.
  > `Fixed voice mode silently failing on the macOS native binary for users whose terminal had never been granted microphone permission — the binary now includes the audio-input entitlement so macOS prompts correctly`
  - *Implication*: First-time voice mode users on macOS will now see the system microphone permission dialog rather than experiencing unexplained silence.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`SessionEnd` hooks killed too early regardless of timeout config**: `SessionEnd` hooks were unconditionally terminated after 1.5 seconds on exit, even when `hook.timeout` was set to a longer value.
  > `Fixed SessionEnd hooks being killed after 1.5 s on exit regardless of hook.timeout — now configurable via CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`
  - *Implication*: Hooks performing cleanup work (e.g. flushing logs, syncing state) that takes longer than 1.5 seconds can now complete by setting the `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` environment variable to an appropriate value.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/plugin install` failing in REPL for local-source marketplace plugins**: Running `/plugin install` from within the interactive REPL failed for marketplace plugins that referenced local sources.
  > `Fixed /plugin install failing inside the REPL for marketplace plugins with local sources`
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Marketplace updates not syncing git submodules**: Plugin sources stored in git submodules would break after a marketplace update because the update process did not sync submodules.
  > `Fixed marketplace update not syncing git submodules — plugin sources in submodules no longer break after update`
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Unknown slash commands silently dropping arguments**: Invoking an unknown slash command with arguments caused the entire input to be discarded without any user feedback.
  > `Fixed unknown slash commands with arguments silently dropping input — now shows your input as a warning`
  - *Implication*: Typos in slash command names (e.g. `/comit` instead of `/commit`) will now surface a warning showing the discarded input rather than silently failing.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **RTL text rendering in Windows terminals**: Hebrew, Arabic, and other right-to-left scripts were not rendered correctly in Windows Terminal, conhost, and the VS Code integrated terminal.
  > `Fixed Hebrew, Arabic, and other RTL text not rendering correctly in Windows Terminal, conhost, and VS Code integrated terminal`
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **LSP servers broken on Windows due to malformed file URIs**: Language Server Protocol servers failed to start on Windows because Claude Code was constructing malformed `file://` URIs.
  > `Fixed LSP servers not working on Windows due to malformed file URIs`
  - *Implication*: LSP-dependent features (e.g. language intelligence, go-to-definition) are now functional on Windows.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Configuration

- **`--plugin-dir` local dev copies now override marketplace installs**: When `--plugin-dir` points to a local development copy of a plugin with the same name as an installed marketplace plugin, the local copy now takes precedence — unless the marketplace plugin is force-enabled by managed settings.
  > `Changed --plugin-dir so local dev copies now override installed marketplace plugins with the same name (unless that plugin is force-enabled by managed settings)`
  - *Implication*: Plugin developers can now test local builds without uninstalling the marketplace version first. Enterprise force-enabled plugins retain their precedence, preserving policy enforcement.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### VS Code Integration

- **Delete button fixed for Untitled sessions**: The delete button in the VS Code extension was non-functional when used on Untitled (unsaved) sessions.
  > `[VSCode] Fixed delete button not working for Untitled sessions`
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Improved scroll wheel responsiveness in integrated terminal**: Scroll wheel input in the VS Code integrated terminal now uses terminal-aware acceleration, resulting in more responsive scrolling behavior.
  > `[VSCode] Improved scroll wheel responsiveness in the integrated terminal with terminal-aware acceleration`
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

## Notable Details

- The GitHub repository star count (76.8k → 76.9k) and open pull request count (336 → 338) changed in the changelog page scrape. These reflect live GitHub metadata rendered into the page and carry no documentation significance.
- The `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` environment variable is newly introduced as the mechanism to extend the session-end hook timeout — this is the first time this env var appears in the changelog and is not yet documented in the settings reference based on this diff alone.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +20 / -2 | Added Claude Code 2.1.74 release notes (2 features, 13 fixes, 1 behavior change) |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-12*
