# Claude Code Documentation Changes — 2026-03-20

## Summary

This update introduces **Channels**, a research preview feature in Claude Code v2.1.80 that allows MCP servers to push messages, alerts, and chat events into a running Claude Code session. Two new documentation pages cover user setup (Telegram, Discord, fakechat) and developer reference for building custom channel MCP servers. Supporting changes land across the CLI reference, MCP docs, settings, and several related pages.

---

## Significant Changes

### Features: Channels (Research Preview)

- **`--channels` flag — push external events into a running session**: Claude Code v2.1.80 adds a `--channels` flag that opts named MCP servers into message-push mode. When enabled, those servers can deliver events (chat messages, CI alerts, webhooks) into the active session, and Claude can react to them in real time. The feature requires a claude.ai login; Console and API key auth are not supported.

  > "A channel is an MCP server that pushes events into your running Claude Code session, so Claude can react to things that happen while you're not at the terminal. Channels can be two-way: Claude reads the event and replies back through the same channel, like a chat bridge."

  - *Implication*: Developers can now drive Claude Code from Telegram or Discord, or pipe CI/monitoring webhooks into an active session. Previously the only push-style interface was Remote Control (browser/phone to local terminal); channels add a programmatic event-push layer.
  - *Source*: [Channels](https://code.claude.com/docs/en/channels.md)

- **Telegram and Discord plugins (official research preview)**: Both are installable via `/plugin install telegram@claude-plugins-official` or `/plugin install discord@claude-plugins-official`, then activated per session with `--channels plugin:telegram@claude-plugins-official`. Pairing bootstraps a sender allowlist using a code exchange.

  > "Every approved channel plugin maintains a sender allowlist: only IDs you've added can push messages, and everyone else is silently dropped."

  - *Implication*: Access control is opt-in per sender and per session — both the `--channels` flag and pairing are required before any message is forwarded to Claude.
  - *Source*: [Channels](https://code.claude.com/docs/en/channels.md)

- **Fakechat — localhost demo channel**: An officially supported demo that runs a browser chat UI at `http://localhost:8787` with no external credentials. Useful for testing the plugin flow before connecting a real platform.
  - *Source*: [Channels](https://code.claude.com/docs/en/channels.md)

- **`--dangerously-load-development-channels` flag**: Bypasses the Anthropic-curated channel allowlist (which only permits `claude-plugins-official` entries during the research preview), allowing developers to test custom channels locally. Works with both `plugin:<name>@<marketplace>` and `server:<name>` entry types.

  > "The bypass is per-entry. Combining this flag with `--channels` doesn't extend the bypass to the `--channels` entries."

  - *Implication*: Custom channel development is possible locally but requires this flag throughout the research preview period. Publishing to an official marketplace requires Anthropic security review.
  - *Source*: [Channels reference](https://code.claude.com/docs/en/channels-reference.md)

### Configuration: New `channelsEnabled` Managed Setting

- **`channelsEnabled` setting for Team/Enterprise admins**: A new managed-settings-only field that controls whether channel message delivery is active for an organization. Defaults to disabled for Team/Enterprise; Pro/Max (no org) users can opt in per session.

  > "Unset or `false` blocks channel message delivery regardless of what users pass to `--channels`"

  - *Implication*: Admins on Team/Enterprise must explicitly enable this at `claude.ai → Admin settings → Claude Code → Channels` before users can receive channel messages. The MCP server still connects and its non-channel tools work regardless of this setting — only message push is gated.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### MCP: Channel Capability Protocol

- **`claude/channel` MCP capability**: The channels feature is built on top of MCP. A server becomes a channel by declaring `capabilities.experimental['claude/channel']: {}` in its constructor and emitting `notifications/claude/channel` events. Events are delivered to Claude wrapped in a `<channel source="...">` XML tag, with optional `meta` key-value pairs as attributes.

  > "An MCP server can also push messages directly into your session so Claude can react to external events like CI results, monitoring alerts, or chat messages. To enable this, your server declares the `claude/channel` capability and you opt it in with the `--channels` flag at startup."

  - *Implication*: Any MCP server can be extended to push events into Claude Code without requiring a new transport mechanism. Two-way channels additionally expose a standard MCP reply tool.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md), [Channels reference](https://code.claude.com/docs/en/channels-reference.md)

### Version 2.1.80 Release Notes (from changelog)

The following additional changes ship in v2.1.80 (documented in the official changelog, not in separate pages):

- **`rate_limits` field for statusline scripts**: Shows Claude.ai rate limit usage across 5-hour and 7-day windows with `used_percentage` and `resets_at` fields.
- **`source: 'settings'` plugin marketplace source**: Plugin entries can now be declared inline in `settings.json`.
- **`effort` frontmatter for skills and slash commands**: Overrides the model effort level when the skill is invoked.
- **CLI tool usage detection for plugin tips**: Plugin tip matching now considers CLI tool usage in addition to file pattern matching.
- **Fix: `--resume` dropping parallel tool results**: Sessions with parallel tool calls now restore all `tool_use`/`tool_result` pairs instead of showing `[Tool result missing]` placeholders.
- **Fix: voice mode WebSocket failures**: Resolved Cloudflare bot detection failures caused by non-browser TLS fingerprints.
- **Fix: 400 errors on fine-grained tool streaming**: Fixed errors when routing through API proxies, Bedrock, or Vertex.
- **Fix: managed settings not applied at startup**: `enabledPlugins`, `permissions.defaultMode`, and policy-set env vars now apply correctly when `remote-settings.json` was cached from a prior session.
- **Fix: `/remote-control` appearing in gateway deployments**: Removed the command for gateway and third-party provider deployments where it cannot function.
- **~80 MB memory reduction on startup** in large repositories (250k-file repos).
- **Improved `@` file autocomplete** responsiveness in large git repositories.
- *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

## New Pages

- **[channels.md](https://code.claude.com/docs/en/channels.md)** — User-facing guide for the Channels research preview. Covers Telegram and Discord plugin installation and pairing, the fakechat localhost demo, sender security model, and enterprise controls (`channelsEnabled`). Requires Claude Code v2.1.80+ and claude.ai login.

- **[channels-reference.md](https://code.claude.com/docs/en/channels-reference.md)** — Developer reference for building custom channel MCP servers. Covers the channel capability declaration, `notifications/claude/channel` event format, `meta` key encoding, two-way reply tool pattern, sender gating (prompt injection defense), and packaging as a plugin. Includes a full webhook receiver walkthrough in TypeScript/Bun.

---

## Notable Details

- **Column width reformatting in `cli-reference.md`**: The 56-addition/54-deletion diff for `cli-reference.md` is almost entirely whitespace reformatting of the flags table — column widths were widened to accommodate the new `--dangerously-load-development-channels` flag. Only two substantive rows were added: `--channels` and `--dangerously-load-development-channels`.

- **`overview.md` code block attribute duplication**: The diff shows `theme={null}` repeated multiple times in fenced code block attributes (e.g., ` ```bash theme={null} theme={null} theme={null}...`). This appears to be a rendering artifact in the source markdown and does not affect the displayed documentation.

- **Channels added to `scheduled-tasks.md` as a counterpart**: The scheduled tasks description now explicitly cross-references Channels as the event-driven alternative to polling: *"To react to events as they happen instead of polling, see Channels: your CI can push the failure into the session directly."* This positions the two features as complementary (polling vs. push) rather than overlapping.

- **Security note on `meta` key naming**: The channels reference specifies that `meta` keys must match `[a-zA-Z0-9_]` — keys with hyphens are silently dropped. This is a non-obvious constraint for developers integrating webhook payloads with hyphenated field names.

- **`channelsEnabled` is managed-settings only**: Unlike most Claude Code settings that can appear in user or project config, `channelsEnabled` is explicitly restricted to managed settings. Individual users cannot self-enable the feature on Team/Enterprise plans.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| channels.md | New | +257 | User guide for Channels: Telegram/Discord setup, fakechat quickstart, security model, enterprise controls |
| channels-reference.md | New | +403 | Developer reference for building channel MCP servers: capability protocol, notification format, reply tools, sender gating |
| cli-reference.md | Modified | +56/-54 | Added `--channels` and `--dangerously-load-development-channels` flags; table column width reformatting |
| changelog.md | Modified | +20/-0 | Added v2.1.80 release notes |
| mcp.md | Modified | +5/-0 | Added "Push messages with channels" section and channels bullet to use-case list |
| overview.md | Modified | +15/-14 | Added Channels row to integrations table; minor code block formatting changes |
| remote-control.md | Modified | +1/-0 | Added Channels cross-link in related resources |
| scheduled-tasks.md | Modified | +1/-1 | Added Channels as event-driven alternative to polling |
| settings.md | Modified | +1/-0 | Added `channelsEnabled` managed setting documentation |

---

*Generated from Claude Code CLI documentation changes detected on 2026-03-20*
