# Claude Code Documentation Changes — 2026-05-29

## Summary

Two documentation pages were updated in this cycle. The MCP page gained a new "Option 4" section documenting WebSocket transport support for remote MCP servers, along with corresponding updates to the plugin transport capabilities list. The plugin marketplaces page clarified name-collision behavior for marketplace registration.

## Significant Changes

### MCP Configuration

- **New WebSocket transport option for MCP servers**: A fourth MCP server configuration method is now documented, adding `type: "ws"` (WebSocket) alongside the existing stdio, SSE, and HTTP options.
  > WebSocket servers hold a persistent bidirectional connection, which suits remote MCP servers that push events to Claude unprompted. Use HTTP instead when your server only responds to requests, since HTTP supports OAuth and the `claude mcp add --transport` flag, while WebSocket supports neither.
  - *Implication*: Developers building event-driven or server-push MCP integrations now have an officially documented path. WebSocket servers must be configured via `.mcp.json` or `claude mcp add-json` — the `--transport ws` flag is explicitly not supported. Authentication is header-only (no OAuth), so tokens must be passed via `headers` or generated dynamically using `headersHelper`.
  - *Example*:
    ```bash
    claude mcp add-json events-server \
      '{"type":"ws","url":"wss://mcp.example.com/socket","headers":{"Authorization":"Bearer YOUR_TOKEN"}}'
    ```
  - *Source*: [MCP Documentation](https://code.claude.com/docs/en/mcp.md)

- **Plugin transport list updated**: The "Multiple transport types" bullet in the plugin MCP server documentation was updated to include WebSocket.
  > Support stdio, SSE, HTTP, and WebSocket transports (transport support may vary by server)
  - *Implication*: Plugin authors can now declare WebSocket-based MCP servers in their `plugin.json`.
  - *Source*: [MCP Documentation](https://code.claude.com/docs/en/mcp.md)

### Plugin Marketplaces

- **Marketplace name collision behavior clarified**: The `name` field description in the marketplace schema was expanded to document what happens when two marketplaces share the same name.
  > Each user can register only one marketplace per name: adding a second marketplace with the same name replaces the first. To publish multiple plugins under one marketplace name, list them all in a [single `marketplace.json`](#create-the-marketplace-file).
  - *Implication*: Marketplace publishers should be aware that re-registering a name silently replaces the prior registration. Publishing multiple plugins under a single marketplace name requires a single `marketplace.json` listing all plugins — splitting them across separate registrations with the same name will not work as intended.
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

## Notable Details

- The MCP page intro was updated from "three different ways" to "several ways" to accommodate the new fourth option — a minor wording change that reflects the growing transport option count.
- WebSocket (`ws`) transport shares the same configuration fields as `http` (`url`, `headers`, `headersHelper`, `timeout`, `alwaysLoad`) but lacks OAuth support. This asymmetry is explicitly called out in the documentation, making it a deliberate constraint rather than a missing feature.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| mcp.md | Modified | SIGNIFICANT | +15/-2 | New "Option 4: Add a remote WebSocket server" section; plugin transport list updated |
| plugin-marketplaces.md | Modified | SIGNIFICANT | +5/-5 | Expanded `name` field description with marketplace name-collision behavior |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-29*
