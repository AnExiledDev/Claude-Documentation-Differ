# Claude Code Documentation Changes — 2026-03-06

## Summary

Version 2.1.70 was released, documenting 20+ bug fixes and several performance improvements. Remote Control availability expanded from a Max/Pro research preview to all subscription plans. The VS Code extension gained three new UI capabilities: an always-visible Activity Bar sessions list, Plan mode rendered as a full markdown document with inline commenting, and a native MCP server management dialog accessible via `/mcp` in the chat panel.

## Significant Changes

### Release: Claude Code 2.1.70

The changelog page documents version 2.1.70 with a substantial set of fixes and improvements.

**Bug Fixes**

- **Third-party API gateway compatibility**: Fixed API 400 errors when using `ANTHROPIC_BASE_URL` with a third-party gateway — tool search now correctly detects proxy endpoints and disables `tool_reference` blocks.
- **Custom Bedrock inference profiles**: Fixed `API Error: 400 This model does not support the effort parameter` when using custom Bedrock inference profiles or model identifiers not matching standard Claude naming patterns.
- **Post-ToolSearch empty model responses**: Fixed empty model responses immediately after `ToolSearch` — the server was rendering tool schemas with system-prompt-style tags at the prompt tail, which could confuse models into stopping early.
- **MCP prompt cache stability**: Fixed prompt-cache bust when an MCP server with instructions connects after the first turn.
- **Windows/WSL clipboard**: Fixed clipboard corrupting non-ASCII text (CJK, emoji) on Windows/WSL by switching to PowerShell `Set-Clipboard`.
- **Windows VS Code startup**: Fixed extra VS Code windows opening at startup on Windows when running from the VS Code integrated terminal.
- **Voice mode on Windows**: Fixed voice mode failing on Windows native binary with "native audio module could not be loaded". Also fixed push-to-talk not activating on session start when `voiceEnabled: true` was configured in settings.
- **Permissions in Remote environments**: Fixed `permissions.defaultMode` settings values other than `acceptEdits` or `plan` being applied in Claude Code Remote environments — they are now ignored.
  - *Implication*: Remote deployments will no longer inadvertently apply non-permitted default modes from local settings.
- **Skill re-injection on resume**: Fixed skill listing being re-injected on every `--resume` (~600 tokens saved per resume).
- **`/color` reset**: Fixed `/color` having no way to reset to default — `/color default`, `/color gray`, `/color reset`, and `/color none` now all restore the default color.
- **`/security-review` on older git**: Fixed the command failing with `unknown option merge-base` on older git versions.
- **Feature flag caching**: Fixed feature flags read during early startup never refreshing their disk cache, causing stale values to persist across sessions.
- **Markdown links with `#NNN` references**: Fixed markdown links containing `#NNN` fragment references incorrectly pointing to the current repository instead of the linked URL.
- **Remote Control poll rate**: Reduced `/poll` rate to once per 10 minutes while connected (was 1–2s), cutting server load ~300×. Reconnection is unaffected — transport loss immediately wakes fast polling.
  - *Implication*: Significant server-side efficiency improvement; no change in reconnect responsiveness.

**Performance Improvements**

- Reduced prompt input re-renders during turns by ~74%.
- Reduced startup memory by ~426KB for users without custom CA certificates.
- Improved compaction to preserve images in the summarizer request, allowing prompt cache reuse for faster and cheaper compaction.
- Improved `/rename` to work while Claude is processing, instead of being silently queued.

**VS Code Additions (see also VS Code section below)**

> `[VSCode] Added spark icon in VS Code activity bar that lists all Claude Code sessions, with sessions opening as full editors`
> `[VSCode] Added full markdown document view for plans in VS Code, with support for adding comments to provide feedback`
> `[VSCode] Added native MCP server management dialog — use /mcp in the chat panel to enable/disable servers, reconnect, and manage OAuth authentication without switching to the terminal`

- *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

### Remote Control: Now Available on All Plans

Remote Control availability expanded from a research preview restricted to Max and Pro plans to all subscription tiers, with an admin opt-in requirement for Team and Enterprise.

> **Before:** `Remote Control is available as a research preview on Max and Pro plans. It is not available on Team or Enterprise plans.`
>
> **After:** `Remote Control is available on all plans. Team and Enterprise admins must first enable Claude Code in admin settings.`

The prerequisites section was also updated:

> **Before:** `Subscription: requires a Max plan. Pro plan support is coming soon. API keys are not supported.`
>
> **After:** `Subscription: available on Pro, Max, Team, and Enterprise plans. Team and Enterprise admins must first enable Claude Code in admin settings. API keys are not supported.`

- *Implication*: Team and Enterprise customers can now use Remote Control, but it requires admin enablement at `claude.ai/admin-settings/claude-code` before users can access it.
- *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

---

### VS Code Extension: Activity Bar Sessions, Plan Markdown View, and Native MCP Management

Three new VS Code-specific features were documented across the changelog and VS Code integration pages.

**Activity Bar Sessions List (always visible)**

> `Activity Bar: click the Spark icon in the left sidebar to open the sessions list. Click any session to open it as a full editor tab, or start a new one. This icon is always visible in the Activity Bar.`

The positioning tip was updated to clarify that the sessions list icon and the Claude panel icon are independent:

> **Before:** `Note that the Spark icon only appears in the Activity Bar when the Claude panel is docked to the left. Since Claude defaults to the right side, use the Editor Toolbar icon to open Claude.`
>
> **After:** `The Activity Bar sessions list icon is separate from the Claude panel: the sessions list is always visible in the Activity Bar, while the Claude panel icon only appears there when the panel is docked to the left sidebar.`

- *Implication*: The sessions list is now always accessible regardless of where the Claude panel is docked, resolving previous confusion about when the Activity Bar icon appeared.

**Plan Mode as Full Markdown Document**

The Plan mode description was extended to document inline commenting support:

> **Before:** `In Plan mode, Claude describes what it will do and waits for approval before making changes.`
>
> **After:** `In Plan mode, Claude describes what it will do and waits for approval before making changes. VS Code automatically opens the plan as a full markdown document where you can add inline comments to give feedback before Claude begins.`

- *Implication*: Users can now annotate plans with structured inline feedback directly in the editor before approving execution.

**Native MCP Management via `/mcp` in Chat Panel**

MCP server management can now be done without leaving VS Code:

> `To manage MCP servers without leaving VS Code, type /mcp in the chat panel. The MCP management dialog lets you enable or disable servers, reconnect to a server, and manage OAuth authentication.`

The CLI vs. Extension feature comparison table was updated accordingly:

| Feature | Before | After |
|---------|--------|-------|
| MCP server config | `No (configure via CLI, use in extension)` | `Partial (add servers via CLI; manage existing servers with /mcp in the chat panel)` |

The "Next steps" section footer was also updated to reflect the new workflow:

> **Before:** `Set up MCP servers to extend Claude's capabilities with external tools. Configure servers using the CLI, then use them in the extension.`
>
> **After:** `Set up MCP servers to extend Claude's capabilities with external tools. Add servers using the CLI, then manage them with /mcp in the chat panel.`

- *Implication*: OAuth authentication and server toggling no longer require a terminal context; these can now be handled inline from the chat panel.
- *Source*: [VS Code Integration](https://code.claude.com/docs/en/vs-code.md)

---

## Notable Details

- The GitHub repository star count moved from 74.3k to 74.4k and open pull requests from 255 to 257 — these are scraped UI elements embedded in the changelog page and reflect live repo state, not documentation authoring.
- `how-claude-code-works.md` received a minor prose edit: `"Vague prompts like 'fix the login bug' work"` was simplified to `"Vague prompts work"` — trivial rewording with no semantic impact.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +32 / -2 | Added v2.1.70 release notes: 20+ bug fixes, performance improvements, 3 VS Code additions |
| vs-code.md | Modified | +15 / -12 | Activity Bar sessions list, plan markdown view with comments, native MCP dialog, updated feature table |
| remote-control.md | Modified | +2 / -2 | Remote Control expanded to all plans; Team/Enterprise requires admin enablement |
| how-claude-code-works.md | Modified | +1 / -1 | Minor prose simplification, no semantic change |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-06*
