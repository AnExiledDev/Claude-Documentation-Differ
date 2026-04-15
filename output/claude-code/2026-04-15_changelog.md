# Claude Code Documentation Changes — 2026-04-15

## Summary

Version 2.1.108 was released on April 14, 2026, introducing prompt cache TTL controls, a session recap feature, and 15+ bug fixes. The most significant documentation change is a major expansion of the Desktop app guide with nine new sections covering the drag-and-drop workspace layout, integrated terminal, file editor, keyboard shortcuts, side chats, and background task monitoring — paired with a minimum version requirement of Claude Desktop v1.2581.0. Two smaller but notable additions landed in `settings.md` (a new `minimumVersion` setting) and `plugins-reference.md` (a clarification on Glob/Grep behavior with orphaned plugin versions).

---

## Significant Changes

### Release: Version 2.1.108 (April 14, 2026)

- **Prompt cache TTL controls**: Two new environment variables manage cache lifetime across all providers (API, Bedrock, Vertex, Foundry):
  > Added `ENABLE_PROMPT_CACHING_1H` env var to opt into 1-hour prompt cache TTL on API key, Bedrock, Vertex, and Foundry (`ENABLE_PROMPT_CACHING_1H_BEDROCK` is deprecated but still honored), and `FORCE_PROMPT_CACHING_5M` to force 5-minute TTL
  - *Implication*: Teams that previously set `ENABLE_PROMPT_CACHING_1H_BEDROCK` should migrate to the unified variable; it remains honored for now.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Session recap feature**: New `/recap` command and associated configuration injects context when returning to a long-dormant session:
  > Added recap feature to provide context when returning to a session, configurable in /config and manually invocable with /recap; force with `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` if telemetry disabled.
  - *Implication*: Users with `DISABLE_TELEMETRY` must set `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` explicitly to get the 1-hour prompt cache TTL; without it they were silently falling back to 5 minutes (also fixed as a bug in this release).
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Model discovers built-in slash commands via Skill tool**: Claude can now autonomously invoke `/init`, `/review`, `/security-review`, and other built-in commands:
  > The model can now discover and invoke built-in slash commands like `/init`, `/review`, and `/security-review` via the Skill tool
  - *Implication*: Claude can incorporate code review or security checks into its own workflows without explicit prompting from the user.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/undo` alias for `/rewind`**: `/undo` now maps to `/rewind`.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/model` warns before mid-session switch**: The model picker now displays a warning when switching models during an active conversation, since the switch causes a full uncached re-read of conversation history.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/resume` defaults to current-directory sessions**: The resume picker now scopes to sessions from the current working directory by default; `Ctrl+A` shows all projects.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Improved error messages**:
  - Server rate limits are now distinguished from plan usage limits
  - 5xx/529 errors include a link to status.claude.com
  - Unknown slash commands suggest the closest match
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Memory footprint reduction**: Language grammars for syntax highlighting load on demand rather than at startup.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

#### Bug Fixes in 2.1.108

Notable fixes include:

| Fix | Detail |
|-----|---------|
| Paste in `/login` code prompt | Regression introduced in 2.1.105 |
| `DISABLE_TELEMETRY` + prompt cache TTL | Was silently using 5-minute TTL instead of 1-hour for subscribers |
| `CLAUDE_ENV_FILE` ending with `#` comment | Bash tool produced no output |
| `--resume <session-id>` losing custom name/color | Session names set via `/rename` were dropped |
| Session titles showing placeholder text | Triggered when first message was a short greeting |
| Diacritical marks dropped from responses | Occurred when `language` setting was configured |
| `--teleport`/`--resume` precondition errors exiting silently | Dirty git tree and "session not found" errors were swallowed |
| Policy-managed plugins not auto-updating | Happened when running from a different project than where first installed |
| Remote Control session titles overwritten | Titles set in web UI were replaced by auto-generated ones after the third message |

---

### Desktop App: Workspace Layout & Navigation (Major Expansion)

The `desktop.md` reference gained nine new sections covering pane-based workspace management. These features require **Claude Desktop v1.2581.0 or later**.

> The workspace layout, terminal, file editor, side chats, and view modes described on this page require Claude Desktop v1.2581.0 or later. Open **Claude → Check for Updates** on macOS or **Help → Check for Updates** on Windows to update.

- *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

#### Drag-and-drop pane layout

> The desktop app is built around panes you can arrange in any layout: chat, diff, preview, terminal, file, plan, tasks, and subagent. Drag a pane by its header to reposition it, or drag a pane edge to resize it.

Eight named pane types are now documented. Open additional panes from the **Views** menu.

#### Integrated terminal

> The integrated terminal lets you run commands alongside your session without switching to another app. Open it from the **Views** menu or press **Ctrl+\`** on macOS or Windows. The terminal opens in your session's working directory and shares the same environment as Claude.

Available in local sessions only.

#### File pane (direct editing)

> Click a file path in the chat or diff viewer to open it in the file pane. Make spot edits and click **Save** to write them back. If the file changed on disk since you opened it, the pane warns you and lets you override or discard.

Right-clicking any file path in chat, diff, or file pane opens a context menu with options: **Attach as context**, **Open in** (VS Code, Cursor, Zed, etc.), **Show in Finder/Explorer**, and **Copy path**.

#### View modes (Normal / Verbose / Summary)

> View modes control how much detail appears in the chat transcript. Switch modes from the **Transcript view** dropdown next to the send button, or press **Ctrl+O** on macOS or Windows to cycle through them.

| Mode | What it shows |
|------|---------------|
| **Normal** | Tool calls collapsed into summaries, with full text responses |
| **Verbose** | Every tool call, file read, and intermediate step Claude takes |
| **Summary** | Only Claude's final responses and the changes it made |

The `--verbose` CLI flag equivalent in the Desktop CLI-comparison table has been updated from "Not available" to "Verbose view mode in the Transcript view dropdown."

#### Keyboard shortcuts reference

A full shortcut table has been added. Key bindings include:

| Shortcut | Action |
|----------|--------|
| `Cmd /` | Show keyboard shortcuts |
| `Cmd N` | New session |
| `Ctrl Tab` / `Ctrl Shift Tab` | Next or previous session |
| `Esc` | Stop Claude's response |
| `Cmd Shift D` | Toggle diff pane |
| `Cmd Shift P` | Toggle preview pane |
| `Ctrl \`` | Toggle terminal pane |
| `Cmd ;` | Open side chat |
| `Ctrl O` | Cycle view modes |
| `Cmd Shift M` | Open permission mode menu |

On Windows, `Ctrl` replaces `Cmd` for most shortcuts.

#### Usage ring

> Click the usage ring next to the model picker to see your current context window usage and your plan usage for the period. Context usage is per session; plan usage is shared across all your Claude Code surfaces.

#### Side chats (`/btw`)

> A side chat lets you ask Claude a question that uses your session's context but doesn't add anything back to the main conversation.
> Press **Cmd+;** on macOS or **Ctrl+;** on Windows to open a side chat, or type `/btw` in the prompt box.

Available in local and SSH sessions only.

#### Background tasks pane

> The tasks pane shows the background work running inside the current session: subagents, background shell commands, and workflows. Open it from the **Views** menu or drag it into your layout.

---

### Desktop App: Other Behavioral Changes

- **Model is now changeable mid-session**: Previously documented as "The model is locked once the session starts." Now reads:
  > You can change this during the session.
  The CLI-comparison table entry for `--model` and the "Shared configuration" section have been updated to match.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Preview pane opens static files**: HTML files, PDFs, and images can now be opened in the preview pane by clicking their path in chat:
  > The preview pane can also open static HTML files, PDFs, and images from your project. Click an HTML, PDF, or image path in the chat to open it in preview.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Auto-archive after PR merge or close**: Sessions can now archive themselves automatically once their pull request merges or closes:
  > To have sessions archive themselves when their pull request merges or closes, turn on **Auto-archive after PR merge or close** in Settings → Claude Code. Auto-archive only applies to local sessions that have finished running.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **PR monitoring auto-archive link in CI status bar**: The CI status bar documentation now cross-references the auto-archive setting.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **SSH session OS requirement clarified**: Previously stated "Claude Code must be installed on the remote machine." Now adds:
  > The remote machine must run Linux or macOS, and Claude Code must be installed on it.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Sidebar filtering expanded**: The session sidebar now filters by status, project, and environment, and supports grouping sessions by project. (Previously documented as filter by status and environment only.)
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Enterprise: Vertex AI and gateways now available in Desktop**: The CLI-vs-Desktop comparison table previously listed third-party providers as "Not available. Desktop connects to Anthropic's API directly." This has been updated to:
  > Anthropic's API by default. Enterprise deployments can configure Vertex AI and gateway providers. See the [enterprise configuration guide](https://support.claude.com/en/articles/12622667-enterprise-configuration).
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Managed plugins now available in Desktop**: New sentence added:
  > If your organization manages plugins centrally, those plugins are available in desktop sessions the same way they are in the CLI.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

---

### Configuration: New `minimumVersion` Setting

A new global setting prevents the auto-updater from downgrading below a specified version:

> `minimumVersion` — Prevent the auto-updater from downgrading below a specific version. Automatically set when switching to the stable channel and choosing to stay on the current version until stable catches up. Used with `autoUpdatesChannel`

Example value: `"2.1.85"`

- *Implication*: Useful for teams that pin to a known-good version while monitoring the stable channel. This is set automatically by the "stay on current version" prompt when switching channels, so most users won't need to set it manually.
- *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

---

### Plugins: Glob/Grep Skip Orphaned Version Directories

A new clarification was added to the plugin caching documentation:

> Claude's Glob and Grep tools skip orphaned version directories during searches, so file results don't include outdated plugin code.

- *Implication*: When a plugin is updated, the old version directory is marked orphaned and held for 7 days. This change confirms that Claude's file-search tools will not surface stale plugin code during that grace period.
- *Source*: [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md)

---

## Notable Details

- **`desktop-quickstart.md` updated description**: The quickstart page tagline now reads "a drag-and-drop layout with an integrated terminal and file editor, visual diff review, live app preview, GitHub PR monitoring with auto-merge, and scheduled tasks." The "Now what?" section was expanded to reference the tasks pane (`/en/desktop#watch-background-tasks`) and side chats (`/en/desktop#ask-a-side-question-without-derailing-the-session`).

- **"When to use Desktop vs CLI" tip updated**: The recommendation changed from "use Desktop when you want visual diff review, file attachments, or session management in a sidebar" to "use Desktop when you want to manage parallel sessions in one window, arrange panes side by side, or review changes visually." Third-party provider scripting was removed from the CLI-only list (now that Enterprise supports Vertex in Desktop).

- **Whitespace normalization across all 62 files**: Every code block annotation was corrected from `` ```lang  theme={null} `` (double space) to `` ```lang theme={null} `` (single space). This is a formatting-only change with no rendered impact.

- **Model bump in example configs (Bedrock)**: Model ID examples reference `claude-opus-4-6`, `claude-sonnet-4-6`, and `claude-haiku-4-5-20251001-v1:0` throughout the Bedrock documentation.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| desktop.md | Modified | +125 / -40 | Nine new sections for workspace layout, terminal, file editor, view modes, keyboard shortcuts, side chats, tasks pane; model changeable mid-session; preview opens HTML/PDF; auto-archive; v1.2581.0+ requirement |
| changelog.md | Modified | +27 / -0 | New version 2.1.108 entry (April 14, 2026) |
| troubleshooting.md | Modified | +73 / -73 | Whitespace normalization only |
| mcp.md | Modified | +77 / -77 | Whitespace normalization only |
| hooks.md | Modified | +74 / -74 | Whitespace normalization only |
| common-workflows.md | Modified | +72 / -72 | Whitespace normalization only |
| sub-agents.md | Modified | +34 / -34 | Whitespace normalization only |
| hooks-guide.md | Modified | +31 / -31 | Whitespace normalization only |
| settings.md | Modified | +30 / -29 | New `minimumVersion` setting; whitespace normalization |
| quickstart.md | Modified | +30 / -30 | Whitespace normalization only |
| plugin-marketplaces.md | Modified | +47 / -47 | Whitespace normalization only |
| plugins-reference.md | Modified | +25 / -23 | New Glob/Grep orphaned-directory clarification; whitespace normalization |
| skills.md | Modified | +23 / -23 | Whitespace normalization only |
| discover-plugins.md | Modified | +22 / -22 | Whitespace normalization only |
| channels-reference.md | Modified | +19 / -19 | Whitespace normalization only |
| amazon-bedrock.md | Modified | +18 / -18 | Whitespace normalization only |
| agent-teams.md | Modified | +14 / -14 | Whitespace normalization only |
| plugins.md | Modified | +14 / -14 | Whitespace normalization only |
| headless.md | Modified | +14 / -14 | Whitespace normalization only |
| memory.md | Modified | +12 / -12 | Whitespace normalization only |
| claude-code-on-the-web.md | Modified | +12 / -12 | Whitespace normalization only |
| vs-code.md | Modified | +11 / -11 | Whitespace normalization only |
| statusline.md | Modified | +10 / -10 | Whitespace normalization only |
| model-config.md | Modified | +9 / -9 | Whitespace normalization only |
| overview.md | Modified | +9 / -9 | Whitespace normalization only |
| github-actions.md | Modified | +10 / -10 | Whitespace normalization only |
| gitlab-ci-cd.md | Modified | +9 / -9 | Whitespace normalization only |
| permission-modes.md | Modified | +8 / -8 | Whitespace normalization only |
| best-practices.md | Modified | +8 / -8 | Whitespace normalization only |
| setup.md | Modified | +41 / -41 | Whitespace normalization only |
| llm-gateway.md | Modified | +8 / -8 | Whitespace normalization only |
| channels.md | Modified | +7 / -7 | Whitespace normalization only |
| how-claude-code-works.md | Modified | +7 / -7 | Whitespace normalization only |
| monitoring-usage.md | Modified | +7 / -7 | Whitespace normalization only |
| remote-control.md | Modified | +7 / -7 | Whitespace normalization only |
| sandboxing.md | Modified | +7 / -7 | Whitespace normalization only |
| scheduled-tasks.md | Modified | +7 / -7 | Whitespace normalization only |
| github-enterprise-server.md | Modified | +6 / -6 | Whitespace normalization only |
| network-config.md | Modified | +6 / -6 | Whitespace normalization only |
| permissions.md | Modified | +6 / -6 | Whitespace normalization only |
| third-party-integrations.md | Modified | +6 / -6 | Whitespace normalization only |
| computer-use.md | Modified | +5 / -5 | Whitespace normalization only |
| desktop-quickstart.md | Modified | +5 / -3 | Updated description and "Now what?" section to reference new Desktop features |
| fullscreen.md | Modified | +5 / -5 | Whitespace normalization only |
| keybindings.md | Modified | +5 / -5 | Whitespace normalization only |
| microsoft-foundry.md | Modified | +5 / -5 | Whitespace normalization only |
| costs.md | Modified | +4 / -4 | Whitespace normalization only |
| google-vertex-ai.md | Modified | +4 / -4 | Whitespace normalization only |
| server-managed-settings.md | Modified | +4 / -4 | Whitespace normalization only |
| voice-dictation.md | Modified | +3 / -3 | Whitespace normalization only |
| authentication.md | Modified | +2 / -2 | Whitespace normalization only |
| code-review.md | Modified | +2 / -2 | Whitespace normalization only |
| interactive-mode.md | Modified | +2 / -2 | Whitespace normalization only |
| jetbrains.md | Modified | +2 / -2 | Whitespace normalization only |
| output-styles.md | Modified | +2 / -2 | Whitespace normalization only |
| routines.md | Modified | +2 / -2 | Whitespace normalization only |
| tools-reference.md | Modified | +2 / -2 | Whitespace normalization only |
| web-quickstart.md | Modified | +2 / -2 | Whitespace normalization only |
| checkpointing.md | Modified | +1 / -1 | Whitespace normalization only |
| fast-mode.md | Modified | +1 / -1 | Whitespace normalization only |
| terminal-config.md | Modified | +1 / -1 | Whitespace normalization only |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-15*
