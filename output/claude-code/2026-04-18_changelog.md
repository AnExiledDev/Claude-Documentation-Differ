# Claude Code Documentation Changes — 2026-04-18

## Summary

Four pages were modified with no additions or removals. The most significant changes are: the release of version 2.1.113 (April 17, 2026) with a large batch of features, security fixes, and bug fixes; a reversal of npm deprecation in setup docs, now treating npm as a fully supported install path (with the native binary delivered via per-platform optional dependencies); and a new troubleshooting section covering the "native binary not found after npm install" scenario.

## Significant Changes

### Installation: npm No Longer Deprecated

- **npm install path rehabilitated**: The previous "Deprecated npm installation" section — which urged migration to the native installer and framed npm as a compatibility-only fallback — has been replaced with a first-class "Install with npm" section.
  > "The npm package installs the same native binary as the standalone installer. npm pulls the binary in through a per-platform optional dependency such as `@anthropic-ai/claude-code-darwin-arm64`, and a postinstall step links it into place. The installed `claude` binary does not itself invoke Node."
  - *Implication*: Developers using npm-based workflows or corporate registries can now install Claude Code via npm without being steered away. The binary is architecturally the same; npm is simply a delivery mechanism.
  - *Source*: [Setup](https://code.claude.com/docs/en/setup.md)

- **Supported platforms documented**: The npm installation section now explicitly lists the eight supported platform packages:
  > "`darwin-arm64`, `darwin-x64`, `linux-x64`, `linux-arm64`, `linux-x64-musl`, `linux-arm64-musl`, `win32-x64`, and `win32-arm64`. Your package manager must allow optional dependencies."
  - *Implication*: Operators can now check this list to validate whether their platform is supported before attempting npm installation.
  - *Source*: [Setup](https://code.claude.com/docs/en/setup.md)

### New Troubleshooting: Native Binary Not Found After npm Install

- **New section added for npm install failures**: A dedicated troubleshooting entry now covers the `Could not find native binary package "@anthropic-ai/claude-code-<platform>"` error with three root causes:
  1. Optional dependencies suppressed (`--omit=optional`, `--no-optional`, `--ignore-optional`, or `optional=false` in `.npmrc`)
  2. Unsupported platform
  3. Corporate npm mirror not mirroring the eight `@anthropic-ai/claude-code-*` packages
  > "The native binary is delivered only as an optional dependency, so there is no JavaScript fallback if it is skipped."
  - *Implication*: Enterprise environments with locked-down registries or npm configs that suppress optional deps will see this error; the fix is to ensure mirror completeness and remove the suppress flag.
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

- **`--ignore-scripts` behavior clarified**:
  > "Installing with `--ignore-scripts` does not trigger this error. The postinstall step that links the binary into place is skipped, so Claude Code falls back to a wrapper that locates and spawns the platform binary on each launch. This works but starts more slowly; reinstall with scripts enabled for direct execution."
  - *Implication*: CI environments that use `--ignore-scripts` for security can still use Claude Code, but should expect a startup latency penalty.
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

### Version 2.1.113 Release (April 17, 2026)

#### Architecture

- **CLI now uses native binary via optional npm dependency**: The CLI no longer bundles or executes JavaScript at runtime.
  > "Changed the CLI to spawn a native Claude Code binary (via a per-platform optional dependency) instead of bundled JavaScript"
  - *Implication*: This is the architectural change that enables npm to be a first-class install method again — both npm and the standalone installer now produce the same native binary.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

#### New Features

- **`sandbox.network.deniedDomains` setting**: New configuration option to block specific domains even when a broader `allowedDomains` wildcard would otherwise permit them.
  - *Implication*: Provides fine-grained network sandboxing control for environments that allow broad domains but need specific exceptions blocked.

- **`/extra-usage` from Remote Control**: The command now works from mobile/web Remote Control clients.

- **Remote Control `@`-file autocomplete**: Remote Control clients can now query `@`-file autocomplete suggestions.

- **`/ultrareview` improvements**: Faster launch with parallelized checks, diffstat in the launch dialog, and an animated launching state.

- **Subagent stall timeout**: Subagents that stall mid-stream now fail with a clear error after 10 minutes instead of hanging silently.

#### Security Fixes

- **macOS dangerous path expansion**: `/private/{etc,var,tmp,home}` paths are now treated as dangerous removal targets under `Bash(rm:*)` allow rules.
  > "Security: on macOS, `/private/{etc,var,tmp,home}` paths are now treated as dangerous removal targets under `Bash(rm:*)` allow rules"
  - *Implication*: Closes a gap where `/private/tmp` (the macOS symlink target for `/tmp`) could be removed without triggering a danger check.

- **Bash deny rules match exec wrappers**: Deny rules now match commands wrapped in `env`/`sudo`/`watch`/`ionice`/`setsid` and similar exec wrappers.
  - *Implication*: Previously, wrapping a denied command in `sudo` or `env` could bypass deny rules.

- **`Bash(find:*)` no longer auto-approves `find -exec`/`-delete`**: Allow rules for `find` no longer implicitly authorize destructive `find` invocations.
  - *Implication*: A wildcard allow rule for `find` could previously be used to execute or delete arbitrary files; this closes that vector.

- **Multi-line bash command spoofing closed**: Multi-line commands whose first line is a comment now show the full command in the transcript.
  > "Bash tool: multi-line commands whose first line is a comment now show the full command in the transcript, closing a UI-spoofing vector"

- **`cd <current-directory> && git …` no longer prompts**: A no-op `cd` prepended before a `git` command no longer triggers a permission prompt.

#### Input / UX Improvements

- **Fullscreen scroll on selection extension**: `Shift+↑/↓` now scrolls the viewport when extending a selection past the visible edge.
- **`Ctrl+A`/`Ctrl+E` readline behavior**: Now moves to the start/end of the current logical line in multiline input.
- **Windows `Ctrl+Backspace`**: Now deletes the previous word.
- **Long URLs stay clickable when wrapped**: In terminals with OSC 8 hyperlink support, long URLs in responses and bash output remain clickable when they wrap across lines.
- **`/loop` improvements**: Pressing `Esc` cancels pending wakeups; wakeups now display as "Claude resuming /loop wakeup".

#### Bug Fixes (selected)

- Fixed MCP concurrent-call timeout handling where one tool call's response could disarm another call's watchdog.
- Fixed `Cmd-Backspace`/`Ctrl+U` to delete from cursor to start of line.
- Fixed markdown tables breaking when a cell contains an inline code span with a pipe character.
- Fixed session recap auto-firing while composing unsent text.
- Fixed `Bash dangerouslyDisableSandbox` running commands without a permission prompt.
- Fixed `CLAUDE_CODE_EXTRA_BODY` `output_config.effort` causing 400 errors on subagent calls to models that don't support effort and on Vertex AI.
- Fixed `thinking.type.enabled is not supported` 400 error when using Opus 4.7 via a Bedrock Application Inference Profile ARN.
- Fixed `plugin install` succeeding when a dependency version conflicts with an already-installed plugin — now reports `range-conflict`.
- Fixed Remote Control sessions not streaming subagent transcripts and not being archived on exit.
- Fixed SDK image content blocks that fail to process crashing the session — now degrades to a text placeholder.
- Fixed `ToolSearch` ranking so pasted MCP tool names surface the actual tool instead of description-matching siblings.
- Fixed compacting a resumed long-context session failing with "Extra usage is required for long context requests".
- Fixed prompt cursor disappearing when `NO_COLOR` is set.

### Hooks: `once` Field Scope Clarification

- **`once` field behavior narrowed in docs**: The description was updated to explicitly state that `once` is only honored for hooks declared in skill frontmatter, and is ignored in settings files and agent frontmatter.
  > Old: "If `true`, runs only once per session then is removed. Skills only, not agents."
  > New: "If `true`, runs once per session then is removed. Only honored for hooks declared in [skill frontmatter](#hooks-in-skills-and-agents); ignored in settings files and agent frontmatter"
  - *Implication*: Developers who placed `once: true` in `settings.json` hooks or agent frontmatter were likely relying on undocumented behavior; the doc now confirms this is a no-op in those contexts.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +41/-0 | Added version 2.1.113 entry (April 17, 2026) with architecture change, new features, security fixes, and ~20 bug fixes |
| setup.md | Modified | +10/-24 | Replaced "Deprecated npm installation" + migration guide with a first-class "Install with npm" section explaining native binary delivery via optional deps |
| troubleshooting.md | Modified | +10/-0 | New "Native binary not found after npm install" section with three root causes and `--ignore-scripts` behavior note |
| hooks.md | Modified | +1/-1 | Clarified `once` field scope: only honored in skill frontmatter, ignored in settings files and agent frontmatter |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-18*
