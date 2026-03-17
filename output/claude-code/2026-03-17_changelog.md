# Claude Code Documentation Changes — 2026-03-17

## Summary

Ten pages were modified with no additions or removals. The most substantive changes are: session quality surveys are now **enabled by default for Bedrock, Vertex, and Foundry** (previously off); hooks now reload automatically via file watcher instead of requiring manual review; fast mode pricing is simplified to a flat rate; and two new environment variables (`CLAUDECODE`, `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS`) are documented.

## Significant Changes

### Data Usage & Privacy

- **Session quality surveys now default-on for third-party providers**: The behavior of the "How is Claude doing?" survey was changed for Bedrock, Vertex, and Foundry users. It previously appeared only for Claude API users; it now appears regardless of provider.
  > "By default, error reporting, telemetry, and bug reporting are disabled when using Bedrock, Vertex, or Foundry. Session quality surveys are the exception and appear regardless of provider."
  - *Implication*: Organizations using Bedrock, Vertex, or Foundry that do not want surveys appearing for their users must now explicitly set `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` or `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`.
  - *Source*: [Data usage](https://code.claude.com/docs/en/data-usage.md)

- **Survey disable conditions clarified**: The conditions that automatically suppress surveys were updated. The previous description ("disabled when using third-party providers") is no longer accurate; the new conditions are `DISABLE_TELEMETRY` or `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` being set.
  > "The survey is also disabled when `DISABLE_TELEMETRY` or `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` is set."
  - *Implication*: Teams that assumed surveys were suppressed by virtue of using Bedrock/Vertex/Foundry should review their configuration.
  - *Source*: [Data usage](https://code.claude.com/docs/en/data-usage.md)

- **`feedbackSurveyRate` setting description updated**: The setting description now links to the session quality surveys doc and explicitly notes its utility on third-party providers. The previous note about "Enterprise admins" was replaced with a general "Set to `0` to suppress entirely."
  > "Useful when using Bedrock, Vertex, or Foundry where the default sample rate does not apply."
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Fast Mode Pricing

- **Tiered pricing removed; flat rate clarified**: Fast mode previously had two price tiers based on context window size (< 200K and > 200K tokens). That distinction has been removed. The February 16 introductory 50% discount is also no longer mentioned.

  Previous pricing table:
  | Mode | Input (MTok) | Output (MTok) |
  |---|---|---|
  | Fast mode on Opus 4.6 (<200K) | $30 | $150 |
  | Fast mode on Opus 4.6 (>200K) | $60 | $225 |

  Updated pricing table:
  | Mode | Input (MTok) | Output (MTok) |
  |---|---|---|
  | Fast mode on Opus 4.6 | $30 | $150 |

  > "Fast mode pricing is flat across the full 1M token context window."
  - *Implication*: Users previously subject to the $60/$225 tier at >200K tokens now pay the same flat $30/$150 rate across the entire context window.
  - *Source*: [Fast mode](https://code.claude.com/docs/en/fast-mode.md)

### Hooks File Watching

- **Hook changes now reload automatically**: Previously, editing settings files while Claude Code was running required manual review in the `/hooks` menu or a restart before changes would apply — a security measure described as preventing "malicious or accidental hook modifications." This requirement has been removed.
  > "Direct edits to hooks in settings files are normally picked up automatically by the file watcher."
  - *Implication*: Workflows that edit hook configs externally (via scripts, editors, etc.) will see changes apply without a restart or UI interaction. The previous security framing around requiring explicit review has been dropped.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md), [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)

- **Troubleshooting guidance updated**: The hooks guide troubleshooting section now advises that file edits are normally automatic, with a restart as a fallback only if the watcher misses the change.
  > "File edits are normally picked up automatically. If they haven't appeared after a few seconds, the file watcher may have missed the change: restart your session to force a reload."
  - *Source*: [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)

### Plugin System & `/reload-plugins`

- **`/reload-plugins` now required to activate new plugins**: The "Use your new plugin" step in the getting-started walkthrough was updated — plugins are no longer immediately active after installation. Users must now run `/reload-plugins` first.
  > "After installing, run `/reload-plugins` to activate the plugin."
  - *Implication*: Automated or scripted plugin install workflows that assumed immediate availability need to add a `/reload-plugins` call.
  - *Source*: [Discover plugins](https://code.claude.com/docs/en/discover-plugins.md)

- **`/reload-plugins` now handles MCP servers**: Plugin MCP server connections can now be applied mid-session without a restart, using `/reload-plugins`.
  > "At session startup, servers for enabled plugins connect automatically. If you enable or disable a plugin during a session, run `/reload-plugins` to connect or disconnect its MCP servers."
  - *Implication*: Previously, enabling or disabling a plugin's MCP server required a full restart. This is no longer the case.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

- **`/reload-plugins` output is now component-specific**: The command description was updated in multiple places to indicate it now reports counts per component type rather than a generic summary.
  > "Claude Code reloads all active plugins and shows counts for reloaded commands, skills, agents, hooks, plugin MCP servers, and plugin LSP servers."
  - *Source*: [Discover plugins](https://code.claude.com/docs/en/discover-plugins.md), [Plugins](https://code.claude.com/docs/en/plugins.md), [Commands](https://code.claude.com/docs/en/commands.md)

### New Environment Variables

- **`CLAUDECODE`**: Documents the environment variable Claude Code sets in shells it spawns. Useful for scripts that need to detect when they are running inside a Claude Code-managed shell.
  > "Set to `1` in shell environments Claude Code spawns (Bash tool, tmux sessions). Not set in hooks or status line commands. Use to detect when a script is running inside a shell spawned by Claude Code."
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS`**: New escape hatch for corporate proxy environments where the organization status check endpoint is blocked.
  > "Set to `1` to allow fast mode when the organization status check fails due to a network error. Useful when a corporate proxy blocks the status endpoint. The API still enforces organization-level disable separately."
  - *Implication*: Teams behind strict network proxies that block Anthropic's status endpoints can now use fast mode without being blocked by connectivity errors.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

## Notable Details

- The `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY` env var description was also updated to align with the new provider behavior — it previously said surveys were "Also disabled when using third-party providers or when telemetry is disabled." That provider-based auto-disable is gone; explicit env var flags are now the only way to suppress surveys on Bedrock/Vertex/Foundry.
- LSP server changes are no longer called out as requiring a full restart in `plugins.md` — `/reload-plugins` now lists "plugin LSP servers" as one of the reloaded components.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| data-usage.md | Modified | +8/-8 | Session quality surveys now default-on for all providers; disable conditions updated; provider table revised |
| fast-mode.md | Modified | +5/-6 | Tiered pricing removed; flat $30/$150 MTok rate across full context window; Feb 16 discount removed |
| discover-plugins.md | Modified | +3/-5 | `/reload-plugins` now required to activate plugins; MCP reload added; output description updated |
| env-vars.md | Modified | +3/-1 | Two new env vars: `CLAUDECODE` and `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS`; survey var description updated |
| hooks-guide.md | Modified | +2/-2 | Hook file changes now auto-reload via file watcher; troubleshooting updated accordingly |
| hooks.md | Modified | +1/-1 | Removed "snapshot at startup" security model; file watcher now handles live hook reloads |
| mcp.md | Modified | +1/-1 | Plugin MCP servers can now be connected/disconnected via `/reload-plugins` without restart |
| plugins.md | Modified | +1/-1 | `/reload-plugins` now explicitly includes LSP servers in its reload scope |
| commands.md | Modified | +1/-1 | `/reload-plugins` description updated to reflect component counts and error reporting |
| settings.md | Modified | +1/-1 | `feedbackSurveyRate` description updated with link and third-party provider context |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-17*
