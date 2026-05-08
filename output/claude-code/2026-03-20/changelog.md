# Claude Code Documentation Changes — 2026-03-20

## Summary

Eleven pages were modified in this update with no pages added or removed (194 additions, 54 deletions). The most significant changes are: rate limit usage fields added to the status line data schema, hooks and environment variables now explicitly supported in server-managed settings, a new `effort` field for per-skill effort level overrides, and a new `settings` inline marketplace source type. Several smaller fixes address anchor links, channel plugin storage paths, and sub-agent tool restriction documentation.

## Significant Changes

### Features

- **Rate limit usage in status line**: Two new `rate_limits` fields are now included in the JSON payload sent to status line scripts. `rate_limits.five_hour` and `rate_limits.seven_day` each expose `used_percentage` (0–100) and `resets_at` (Unix epoch seconds).
  > `rate_limits.five_hour.used_percentage`, `rate_limits.seven_day.used_percentage` — Percentage of the 5-hour or 7-day rate limit consumed, from 0 to 100

  A new "Rate limit usage" example section was added with ready-to-use scripts in Bash, Python, and Node.js. The field is conditional:
  > `rate_limits`: appears only for Claude.ai subscribers (Pro/Max) after the first API response in the session. Each window (`five_hour`, `seven_day`) may be independently absent. Use `jq -r '.rate_limits.five_hour.used_percentage // empty'` to handle absence gracefully.
  - *Implication*: Status line scripts can now surface subscription quota consumption alongside context and cost metrics. Scripts must handle the field's absence (non-subscribers, pre-first-response) using optional chaining or `// empty` fallbacks.
  - *Source*: [Customize your status line](https://code.claude.com/docs/en/statusline.md)

- **Skill `effort` field**: A new `effort` frontmatter field is available in skill definitions, allowing individual skills to override the session-level effort setting.
  > `effort` — [Effort level](/en/model-config#adjust-effort-level) when this skill is active. Overrides the session effort level. Default: inherits from session. Options: `low`, `medium`, `high`, `max` (Opus 4.6 only).
  - *Implication*: Skills that require deeper reasoning (e.g., architectural review) can be pinned to `high` or `max` without requiring users to change effort globally. The `max` option is currently limited to Opus 4.6.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

### Configuration

- **Hooks and environment variables in server-managed settings**: The server-managed settings description was expanded to explicitly call out hooks and environment variables as supported, not just permission and security settings.
  > Add your configuration as JSON. All [settings available in `settings.json`](/en/settings#available-settings) are supported, including [hooks](/en/hooks), [environment variables](/en/env-vars), and [managed-only settings](/en/permissions#managed-only-settings) like `disableBypassPermissionsMode`.

  A concrete example was added showing an organization-wide `PostToolUse` hook that runs an audit script after every file edit:
  ```json
  {
    "hooks": {
      "PostToolUse": [
        {
          "matcher": "Edit|Write",
          "hooks": [
            { "type": "command", "command": "/usr/local/bin/audit-edit.sh" }
          ]
        }
      ]
    }
  }
  ```
  > Because hooks execute shell commands, users see a [security approval dialog](#security-approval-dialogs) before they're applied.
  - *Implication*: Enterprise administrators can now deploy audit trails, compliance scripts, or notification hooks to all users via the Claude.ai admin console without per-device configuration.
  - *Source*: [Configure server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md)

- **Inline marketplace source type (`settings`)**: A new `source: 'settings'` type is now documented for `extraKnownMarketplaces`, enabling a small set of plugins to be declared directly in `settings.json` without hosting a separate marketplace repository.
  > Use `source: 'settings'` to declare a small set of plugins inline without setting up a hosted marketplace repository. Plugins listed here must reference external sources such as GitHub or npm. You still need to enable each plugin separately in `enabledPlugins`.

  ```json
  {
    "extraKnownMarketplaces": {
      "team-tools": {
        "source": {
          "source": "settings",
          "name": "team-tools",
          "plugins": [
            {
              "name": "code-formatter",
              "source": { "source": "github", "repo": "acme-corp/code-formatter" }
            }
          ]
        }
      }
    }
  }
  ```
  - *Implication*: Teams can distribute a curated set of plugins via `settings.json` without maintaining a marketplace server, lowering the barrier to sharing internal tooling.
  - *Source*: [Claude Code settings](https://code.claude.com/docs/en/settings.md)

- **Sub-agent `tools` and `disallowedTools` precedence clarified**: The documentation now provides separate, explicit examples for allowlist (`tools`) and denylist (`disallowedTools`) and documents their interaction when both are set.
  > If both are set, `disallowedTools` is applied first, then `tools` is resolved against the remaining pool. A tool listed in both is removed.
  - *Implication*: The previous single combined example could suggest both fields were used together. The clarification reveals that `disallowedTools` acts as a pre-filter, so a tool appearing in both lists is always excluded.
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

### Channels

- **Channel plugin token storage path corrected to user home**: The `.env` files for Telegram and Discord channel plugins were documented as project-relative (`.claude/channels/<plugin>/.env`) but are now corrected to user-home-relative (`~/.claude/channels/<plugin>/.env`).
  > This saves it to `~/.claude/channels/telegram/.env`. You can also set `TELEGRAM_BOT_TOKEN` in your shell environment before launching Claude Code.
  - *Implication*: The token files are stored per-user, not per-project. Any automation referencing the old project-relative path should be updated.
  - *Source*: [Channels](https://code.claude.com/docs/en/channels.md)

- **`--channels` flag relabeled as research preview requiring Claude.ai auth**: The CLI reference description for `--channels` was updated from a general description referencing an approved allowlist to a research-preview framing.
  > (Research preview) MCP servers whose [channel](/en/channels) notifications Claude should listen for in this session. Space-separated list of `plugin:<name>@<marketplace>` entries. Requires Claude.ai authentication
  - *Implication*: The flag is explicitly scoped to Claude.ai-authenticated users; API key users cannot use channels. The "approved allowlist" language was removed.
  - *Source*: [CLI reference](https://code.claude.com/docs/en/cli-reference.md)

- **Marketplace troubleshooting note added to all channel install steps**: For Telegram, Discord, and fakechat, a consistent recovery instruction was added.
  > If Claude Code reports that the plugin is not found in any marketplace, run `/plugin marketplace add anthropics/claude-plugins-official` first and retry the install.
  - *Implication*: Users on fresh installs or non-standard setups now have a clear recovery path when plugin install fails with a "not found" error.
  - *Source*: [Channels](https://code.claude.com/docs/en/channels.md)

### Removals

- **`pip` plugin source type removed**: The `pip` row was removed from the plugin source types table in `plugin-marketplaces.md`. The remaining supported types are `url`, `git-subdir`, and `npm`.
  - *Implication*: Python-based plugins distributed via pip are no longer a documented or supported installation method. Plugin authors targeting Python should use `npm` or `git`-based sources instead.
  - *Source*: [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

## Notable Details

- **Anchor link fixes across multiple pages**: Several internal anchor links used the old `#claudemd-files` format and were corrected to `#claude-md-files` (with a hyphen) across `memory.md` and `features-overview.md`. Similarly, `#exclude-specific-claudemd-files` → `#exclude-specific-claude-md-files`. These are navigation fixes with no content change.
- **Plugin discover docs use concrete example**: The install snippet in `discover-plugins.md` changed from the generic placeholder `plugin-name@claude-plugins-official` to `github@claude-plugins-official`, making it immediately copy-pasteable.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| statusline.md | Modified | +105/-26 | Added `rate_limits` fields to data schema and JSON example; new "Rate limit usage" section with Bash/Python/Node.js scripts |
| settings.md | Modified | +25/-0 | Documented `source: 'settings'` inline marketplace type for `extraKnownMarketplaces` |
| server-managed-settings.md | Modified | +22/-1 | Explicitly documented hooks and env vars as supported; added PostToolUse audit hook example |
| sub-agents.md | Modified | +12/-1 | Split `tools`/`disallowedTools` into separate examples; documented interaction when both are set |
| skills.md | Modified | +13/-12 | Added `effort` field to skill frontmatter table (overrides session effort level) |
| channels.md | Modified | +7/-3 | Corrected token storage paths to `~/.claude/...`; added marketplace troubleshooting note to all install steps |
| memory.md | Modified | +5/-5 | Fixed anchor links (`#claudemd-files` → `#claude-md-files`) throughout |
| discover-plugins.md | Modified | +2/-2 | Replaced generic placeholder with concrete `github@claude-plugins-official` example |
| features-overview.md | Modified | +2/-2 | Fixed anchor links for CLAUDE.md section references |
| cli-reference.md | Modified | +1/-1 | Updated `--channels` description to "(Research preview)", requires Claude.ai auth |
| plugin-marketplaces.md | Modified | +0/-1 | Removed `pip` from plugin source types table |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-20*
