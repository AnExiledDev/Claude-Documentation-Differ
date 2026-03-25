# Claude Code Documentation Changes — 2026-03-25

## Summary

Three pages were updated in this revision. The largest change introduces a new `headersHelper` configuration option for MCP servers, enabling dynamic header generation for non-OAuth authentication schemes. Two smaller updates clarify that `@mention` is unavailable in remote Desktop sessions and confirm that the settings hierarchy applies uniformly across CLI, VS Code, and JetBrains.

## Significant Changes

### MCP Configuration

- **New `headersHelper` field for custom MCP authentication**: A new section documents how to use `headersHelper` in MCP server config to support authentication schemes outside of OAuth — such as Kerberos, short-lived tokens, or internal SSO systems. Claude Code executes the specified command at connection time and merges its stdout into the request headers.

  > "If your MCP server uses an authentication scheme other than OAuth (such as Kerberos, short-lived tokens, or an internal SSO), use `headersHelper` to generate request headers at connection time. Claude Code runs the command and merges its output into the connection headers."

  Example configuration:
  ```json
  {
    "mcpServers": {
      "internal-api": {
        "type": "http",
        "url": "https://mcp.internal.example.com",
        "headersHelper": "/opt/bin/get-mcp-auth-headers.sh"
      }
    }
  }
  ```

  Key behavioral constraints documented:
  - The command must write a JSON object of string key-value pairs to stdout
  - Runs in a shell with a **10-second timeout**
  - Dynamic headers **override** any static `headers` with the same name
  - Runs fresh on every connection — no caching is performed
  - When defined at project or local scope, only executes after the workspace trust dialog is accepted

  - *Implication*: Teams using enterprise auth systems (Kerberos, internal SSO) can now connect MCP servers without requiring OAuth flows. The security note about workspace trust is important — this executes arbitrary shell commands.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

- **Fixed plugin `.mcp.json` example — missing `mcpServers` wrapper**: The JSON code example for configuring an MCP server inside a plugin was corrected to include the required top-level `"mcpServers"` key, which was absent in the previous version.

  Before:
  ```json
  {
    "database-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      ...
    }
  }
  ```

  After:
  ```json
  {
    "mcpServers": {
      "database-tools": {
        "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
        ...
      }
    }
  }
  ```

  - *Implication*: Plugin authors using the old example format may have had silently broken MCP server configurations. The corrected structure matches the standard MCP config schema.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

### Desktop Application

- **`@mention` files unavailable in remote sessions**: The documentation now explicitly states that file `@mention` does not work in remote Desktop sessions. This appears in both the feature description prose and the CLI vs. Desktop comparison table.

  > "@mention is not available in remote sessions."

  The comparison table entry for `@mention files` was updated from "With autocomplete" to "With autocomplete; local and SSH sessions only".

  - *Implication*: Users connecting to Claude Code Desktop via remote sessions should use file attachments instead of `@mention` for adding file context.
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

### Settings

- **Settings precedence hierarchy now explicitly covers VS Code and JetBrains**: The description of how the settings hierarchy works was extended to confirm it applies identically across all Claude Code surfaces.

  > "The same precedence applies whether you run Claude Code from the CLI, the [VS Code extension](/en/vs-code), or a [JetBrains IDE](/en/jetbrains)."

  - *Implication*: Clarifies that organizational policy enforcement via enterprise/project settings files works consistently regardless of which editor or interface a developer uses.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| mcp.md | Modified | +49 / -5 | New `headersHelper` auth section; fixed plugin `.mcp.json` structure |
| desktop.md | Modified | +2 / -2 | `@mention` files restricted to local/SSH sessions only |
| settings.md | Modified | +1 / -1 | Settings hierarchy clarified to include VS Code and JetBrains |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-25*
