# Claude Code Documentation Changes — 2026-05-12

## Summary

Eleven pages were modified across permissions, MCP, channels, and the quickstart guide. The most substantive changes add `server:` prefix syntax for testing bare MCP servers during the channels research preview, document `permissions.disableAutoMode` as an explicit admin control, and rename the MCP streamable-HTTP transport flag from `--transport streamable-http` to `--transport http`.

## Significant Changes

### Channels

- **`server:` prefix for bare MCP.json channel testing**: The channels reference now documents two distinct forms for `--dangerously-load-development-channels`: a `plugin:` prefix for wrapped plugin entries and a new `server:` prefix for bare `.mcp.json` entries that don't yet have a plugin wrapper.
  > ```bash
  > # Testing a plugin you're developing
  > claude --dangerously-load-development-channels plugin:yourplugin@yourmarketplace
  >
  > # Testing a bare .mcp.json server (no plugin wrapper yet)
  > claude --dangerously-load-development-channels server:webhook
  > ```
  - *Implication*: Developers building custom channels can now test local `.mcp.json` entries without first packaging them as a plugin, lowering the friction for iterative channel development.
  - *Source*: [Channels reference](https://code.claude.com/docs/en/channels-reference.md)

### MCP

- **HTTP transport flag renamed from `streamable-http` to `http`**: The auto-generated `claude mcp add` commands in the MCP server registry now use `--transport http` instead of `--transport streamable-http`. The command generation logic explicitly replaces the old flag: `replace('--transport streamable-http', '--transport http')`.
  > ```bash
  > claude mcp add my-server --transport http https://api.example.com/mcp
  > ```
  - *Implication*: Developers using registry-generated commands or copying examples from the MCP page should update any local scripts that use `--transport streamable-http`; the shorter `--transport http` form is now canonical.
  - *Source*: [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp.md)

### Permissions

- **`permissions.disableAutoMode` documented as an explicit admin control**: The permissions page now describes `permissions.disableAutoMode` as a parallel setting to `permissions.disableBypassPermissionsMode`, giving administrators a dedicated knob to prevent auto mode from being activated.
  > To prevent `bypassPermissions` or `auto` mode from being used, set `permissions.disableBypassPermissionsMode` or `permissions.disableAutoMode` to `"disable"` in any [settings file]. These are most useful in [managed settings] where they cannot be overridden.
  - *Implication*: Enterprise admins who need to enforce manual review on all tool use can now lock out auto mode via managed settings, rather than relying on the admin UI toggle alone.
  - *Source*: [Configure permissions](https://code.claude.com/docs/en/permissions.md)

### Quickstart

- **Quickstart content updated (+5/-5 lines)**: The quickstart guide received equal-magnitude additions and removals, consistent with a section rewrite rather than a net addition. Content is likely restructured for clarity; no new prerequisites or steps appear to have been added based on the current page structure.
  - *Implication*: Developers referencing the quickstart for onboarding scripts or team docs should review the current version for any wording changes.
  - *Source*: [Quickstart](https://code.claude.com/docs/en/quickstart.md)

### Configuration

- **`.claude` directory reference updated (+7/-5 lines)**: The `claude-directory.md` page describing the `.claude/` file tree received both additions and removals, indicating rewording or restructuring of existing entries rather than a net new entry.
  - *Source*: [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory.md)

## Minor Changes

- **channels.md**: Small addition (+2/-0 lines) — likely a note or clarification to the supported channels overview. (+2/-0)
- **env-vars.md**: Single-line substitution (+1/-1 lines) — minor wording update to an environment variable description. (+1/-1)
- **google-vertex-ai.md**: Single-line substitution (+1/-1 lines) — minor update to Vertex AI setup instructions. (+1/-1)
- **interactive-mode.md**: One line added (+1/-0 lines) — likely a new keyboard shortcut row or clarification to an existing entry. (+1/-0)
- **model-config.md**: Two lines added (+2/-0 lines) — small addition to model configuration documentation. (+2/-0)
- **permission-modes.md**: Two lines added (+2/-0 lines) — small clarification to permission modes documentation. (+2/-0)

## Notable Details

- The `--transport streamable-http` → `--transport http` rename in `mcp.md` is embedded in JavaScript component code (the `MCPServersTable` component), not just documentation prose. This means auto-generated commands shown in the MCP registry UI on the docs page were also updated.
- The `permissions.disableAutoMode` setting mirrors the existing `permissions.disableBypassPermissionsMode` pattern, suggesting the permission control system is being systematically extended to cover each non-default mode individually.
- The `full_diff.txt` workspace file was empty (0 bytes) for this run; analysis above is based on current page content and line-count statistics rather than a unified diff.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| channels-reference.md | Modified | SIGNIFICANT | +7/-1 | Added `server:` prefix form for testing bare `.mcp.json` channel entries |
| claude-directory.md | Modified | SIGNIFICANT | +7/-5 | Directory file tree entries reworded or restructured |
| mcp.md | Modified | SIGNIFICANT | +10/-8 | HTTP transport flag renamed from `streamable-http` to `http` |
| permissions.md | Modified | SIGNIFICANT | +5/-1 | `permissions.disableAutoMode` added as explicit admin control |
| quickstart.md | Modified | SIGNIFICANT | +5/-5 | Quickstart content rewritten with equal additions and removals |
| channels.md | Modified | MINOR | +2/-0 | Small addition to supported channels overview |
| env-vars.md | Modified | MINOR | +1/-1 | Minor wording update to an environment variable description |
| google-vertex-ai.md | Modified | MINOR | +1/-1 | Minor update to Vertex AI setup instructions |
| interactive-mode.md | Modified | MINOR | +1/-0 | Small addition to interactive mode reference |
| model-config.md | Modified | MINOR | +2/-0 | Small addition to model configuration documentation |
| permission-modes.md | Modified | MINOR | +2/-0 | Small clarification to permission modes documentation |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-12*
