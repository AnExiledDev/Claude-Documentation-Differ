# Claude Code Documentation Changes — 2026-04-16

## Summary

Version 2.1.110 was released on April 15, 2026, bringing a substantial set of new commands, configuration options, and bug fixes — it is the largest release entry in the changelog this cycle. The web quickstart gained a new "Pre-fill sessions" section documenting URL parameters for programmatic session creation. The overview page also received the `InstallConfigurator` interactive widget that previously only appeared on the quickstart page.

---

## Significant Changes

### CLI Release: Version 2.1.110

- **New `/tui` command and `tui` setting**: Introduces a flicker-free fullscreen rendering mode that can be activated mid-conversation.
  > Added `/tui` command and `tui` setting — run `/tui fullscreen` to switch to flicker-free rendering in the same conversation
  - *Implication*: Users on terminals with rendering artifacts can switch to the alternate renderer without restarting their session.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`Ctrl+O` behavior change and new `/focus` command**: `Ctrl+O` now only toggles verbose transcript mode; focus view moves to a dedicated `/focus` command.
  > Changed `Ctrl+O` to toggle between normal and verbose transcript only; focus view is now toggled separately with the new `/focus` command
  - *Implication*: Existing muscle memory for `Ctrl+O` will need to be updated if focus view was the intended action.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **New `autoScrollEnabled` config**: Adds a config option to disable automatic conversation scrolling when in fullscreen mode.
  > Added `autoScrollEnabled` config to disable conversation auto-scroll in fullscreen mode
  - *Implication*: Users who prefer to stay at a fixed scroll position while Claude is responding can now opt out of auto-scroll.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **External editor context option**: The `Ctrl+G` external editor can now optionally show Claude's last response as commented context.
  > Added option to show Claude's last response as commented context in the `Ctrl+G` external editor (enable via `/config`)
  - *Implication*: Provides inline context when editing prompts in an external editor without needing to switch back to the CLI.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Improved `/plugin` Installed tab**: Items needing attention and favorites now surface at the top; disabled plugins are hidden behind a fold; `f` favorites the selected item.
  > Improved `/plugin` Installed tab — items needing attention and favorites appear at the top, disabled items are hidden behind a fold, and `f` favorites the selected item
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`/doctor` MCP scope conflict warning**: The diagnostics command now flags when a single MCP server is defined across multiple config scopes with different endpoints.
  > Improved `/doctor` to warn when an MCP server is defined in multiple config scopes with different endpoints
  - *Implication*: Helps diagnose subtle MCP misconfiguration that could cause unexpected server routing.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`--resume`/`--continue` resurrects scheduled tasks**: These flags will now bring back unexpired scheduled tasks, not just conversations.
  > `--resume`/`--continue` now resurrects unexpired scheduled tasks
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Remote Control commands expanded**: `/autocompact`, `/context`, `/exit`, and `/reload-plugins` now execute when sent from Remote Control (mobile/web) clients.
  > `/autocompact`, `/context`, `/exit`, and `/reload-plugins` now work from Remote Control (mobile/web) clients
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Write tool IDE diff feedback**: When a user edits the proposed content in the IDE diff view before accepting, the Write tool now informs the model that edits were made.
  > Write tool now informs the model when you edit the proposed content in the IDE diff before accepting
  - *Implication*: The model gets more accurate context about what the final applied change was vs. what it originally proposed.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Bash tool timeout enforcement**: The Bash tool now enforces its documented maximum timeout rather than accepting arbitrarily large values.
  > Bash tool now enforces the documented maximum timeout instead of accepting arbitrarily large values
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Distributed tracing support for SDK/headless sessions**: Reads `TRACEPARENT`/`TRACESTATE` from the environment to enable distributed trace linking in headless and SDK usage.
  > SDK/headless sessions now read `TRACEPARENT`/`TRACESTATE` from the environment for distributed trace linking
  - *Implication*: Teams using observability tooling (OpenTelemetry, etc.) can now trace Claude Code SDK sessions within their existing trace graphs.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Session recap enabled for telemetry-disabled users**: The recap feature (context summary when returning to a session) now works for Bedrock, Vertex, Foundry, and `DISABLE_TELEMETRY` users. Opt out via `/config` or `CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0`.
  > Session recap is now enabled for users with telemetry disabled (Bedrock, Vertex, Foundry, `DISABLE_TELEMETRY`). Opt out via `/config` or `CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0`.
  - *Implication*: Enterprise/cloud-provider users who previously couldn't use this feature will now see it active by default.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

### Bug Fixes in 2.1.110

Notable security and correctness fixes included in this release:

- **Security**: Hardened "Open in editor" actions against command injection from untrusted filenames.
- **Security**: Fixed `PermissionRequest` hooks returning `updatedInput` not being re-checked against `permissions.deny` rules; `setMode:'bypassPermissions'` updates now respect `disableBypassPermissionsMode`.
- **MCP**: Fixed tool calls hanging indefinitely when a server connection drops mid-response on SSE/HTTP transports.
- **MCP**: Fixed stdio MCP servers that print stray non-JSON lines to stdout being disconnected on the first stray line (regression in 2.1.105).
- **Hooks**: Fixed `PreToolUse` hook `additionalContext` being dropped when the tool call fails.
- **Reliability**: Fixed non-streaming fallback retries causing multi-minute hangs when the API is unreachable.
- **Remote Control**: Fixed sessions showing a generic error instead of prompting re-login when the session is too old; fixed session renames from claude.ai not persisting to the local CLI session.
- **Rendering**: Fixed garbled startup rendering in macOS Terminal.app and other terminals that don't support synchronized output; fixed high CPU usage in fullscreen when text is selected during a tool run.
- **Skills**: Fixed skills with `disable-model-invocation: true` failing when invoked via `/<skill>` mid-message.

### Web Quickstart: Pre-fill Sessions

- **New URL parameter API for claude.ai/code**: A new "Pre-fill sessions" section documents query parameters that let external tools (e.g., issue trackers) open Claude Code with a prompt and context pre-loaded.
  > You can prefill the prompt, repositories, and environment for a new session by adding query parameters to the claude.ai/code URL. Use this to build integrations such as a button in your issue tracker that opens Claude Code with the issue description as the prompt.

  | Parameter | Description |
  |-----------|-------------|
  | `prompt` / `q` | Prompt text to prefill in the input box |
  | `prompt_url` | URL to fetch prompt text from (for long prompts; ignored if `prompt` is set) |
  | `repositories` / `repo` | Comma-separated `owner/repo` slugs to preselect |
  | `environment` | Name or ID of the environment to preselect |

  - *Implication*: Enables one-click "Open in Claude Code" integrations from GitHub, Jira, Linear, or any other tool that can construct a URL.
  - *Source*: [web-quickstart.md](https://code.claude.com/docs/en/web-quickstart.md)

### Overview Page: Interactive Install Configurator

- **`InstallConfigurator` widget added to overview**: The interactive installation wizard (previously only on the quickstart page) is now embedded on the overview page, gated behind the `overview-install-configurator` experiment flag. It also supports a new `install-configurator-default-surface` flag to default to the Desktop tab.
  - *Source*: [overview.md](https://code.claude.com/docs/en/overview.md)

### Install Configurator UI Improvements (Quickstart)

- **`defaultSurface` prop**: The `InstallConfigurator` component now accepts a `defaultSurface` prop (default: `'terminal'`), allowing it to open on a specific tab (e.g., `desktop`).
- **Taglines added for non-terminal targets**: Desktop, VS Code, and JetBrains targets each have a short descriptor displayed in the handoff card.
  > Desktop: "The full agent in a native app for macOS and Windows."
  > VS Code: "Review diffs, manage context, and chat without leaving your editor."
  > JetBrains: "Native plugin for IntelliJ, PyCharm, WebStorm, and other JetBrains IDEs."
- **Windows shell switcher redesigned**: The "CMD instead of PowerShell" checkbox was replaced with a tab-style toggle (`PowerShell` / `CMD`).
- **Handoff card visual update**: Now uses a gradient background and box shadow instead of a flat white card; title and tagline replace the old generic "steps below use the command line" text.
  - *Source*: [quickstart.md](https://code.claude.com/docs/en/quickstart.md)

---

## Notable Details

- The `Experiment` component's bucketing logic was updated across **all five** docs pages that embed it (`amazon-bedrock.md`, `google-vertex-ai.md`, `microsoft-foundry.md`, `third-party-integrations.md`, `quickstart.md`). It now reads `document.documentElement.dataset['gb_' + flag]` to check for server-side pre-bucketing before falling back to client-side bucketing. This is an infrastructure change enabling server-driven A/B test assignment.
- In the 2.1.108 changelog entry, formatting was corrected: `/config` and `/recap` are now wrapped in backticks consistently.
- The `quickstart.md` experiment slot flag changed from `quickstart-install-configurator` to `install-configurator-default-surface`, and the slot element changed from a bare `<Experiment>` to a named `<div className="install-configurator-slot">` wrapper — likely to enable targeting across multiple pages.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +36/-1 | Added v2.1.110 release notes; minor formatting fix in v2.1.108 |
| web-quickstart.md | Modified | +17/-0 | New "Pre-fill sessions" section with URL parameter table |
| overview.md | Modified | +641/-0 | Added `InstallConfigurator` React component and experiment wrapper |
| quickstart.md | Modified | +62/-34 | `InstallConfigurator` improvements: `defaultSurface` prop, taglines, shell switcher redesign, handoff card polish |
| amazon-bedrock.md | Modified | +3/-1 | Experiment bucketing logic: server-side pre-bucketing support |
| google-vertex-ai.md | Modified | +3/-1 | Experiment bucketing logic: server-side pre-bucketing support |
| microsoft-foundry.md | Modified | +3/-1 | Experiment bucketing logic: server-side pre-bucketing support |
| third-party-integrations.md | Modified | +3/-1 | Experiment bucketing logic: server-side pre-bucketing support |

---

*Generated from Claude Code CLI documentation changes detected on 2026-04-16*
