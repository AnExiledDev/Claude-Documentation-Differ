# Claude Code Documentation Changes — 2026-03-05

## Summary

Six documentation pages were modified in this update. The most substantive changes are: a new Windows-specific status line configuration guide (PowerShell and Git Bash examples), a new MCP OAuth metadata override option (`authServerMetadataUrl`), and a clarification across three pages that `allowManagedDomainsOnly` silently blocks non-allowed domains rather than prompting the user.

## Significant Changes

### Integrations

- **Status line Windows configuration guide added**: A new dedicated section documents how Windows users can configure status line scripts, covering both PowerShell (invoked via Git Bash) and native Bash script approaches. Previously, the docs only noted that WSL or PowerShell rewrites were an option with no examples.

  > "On Windows, Claude Code runs status line commands through Git Bash. You can invoke PowerShell from that shell"

  The section includes full working examples for both `settings.json` configuration and the companion script files.
  - *Implication*: Windows developers no longer need to infer how to adapt macOS/Linux examples — drop-in configs are now provided.
  - *Source*: [statusline.md](https://code.claude.com/docs/en/statusline.md)

- **Two new status line troubleshooting tips**: Added to the troubleshooting section alongside the Windows guide.

  > "Run `claude --debug` to log the exit code and stderr from the first status line invocation in a session"
  > "Ask Claude to read your settings file and execute the `statusLine` command directly to surface errors"

  - *Implication*: These tips make diagnosing broken status line scripts significantly easier, particularly `--debug` mode which previously wasn't called out in this context.
  - *Source*: [statusline.md](https://code.claude.com/docs/en/statusline.md)

### MCP (Model Context Protocol)

- **New OAuth metadata override option (`authServerMetadataUrl`)**: A new `authServerMetadataUrl` field in the `oauth` object of `.mcp.json` allows Claude Code to fetch OAuth metadata from a specified URL instead of using the standard `/.well-known/oauth-authorization-server` discovery chain.

  > "If your MCP server returns errors on the standard OAuth metadata endpoint (`/.well-known/oauth-authorization-server`) but exposes a working OIDC endpoint, you can tell Claude Code to fetch OAuth metadata directly from a URL you specify, bypassing the standard discovery chain."

  Example config:
  ```json
  {
    "mcpServers": {
      "my-server": {
        "type": "http",
        "url": "https://mcp.example.com/mcp",
        "oauth": {
          "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
        }
      }
    }
  }
  ```

  The URL must use `https://`. **Requires Claude Code v2.1.64 or later.**
  - *Implication*: MCP servers that use OIDC-style metadata endpoints (rather than the OAuth 2.0 Authorization Server Metadata spec) can now be configured without workarounds.
  - *Source*: [mcp.md](https://code.claude.com/docs/en/mcp.md)

### Configuration & Security

- **`allowManagedDomainsOnly` behavior clarified — silent blocking, not prompting**: The description of `network.allowManagedDomainsOnly` was updated across three pages (`settings.md`, `permissions.md`, `sandboxing.md`) to explicitly state that non-allowed domains are blocked automatically without prompting the user.

  Previous wording (settings.md):
  > "Domains from user, project, and local settings are ignored. Denied domains are still respected from all sources."

  Updated wording:
  > "Non-allowed domains are blocked automatically without prompting the user. Denied domains are still respected from all sources."

  The sandboxing.md page now cross-references this setting inline:
  > "New domain requests trigger permission prompts (unless [`allowManagedDomainsOnly`](/en/settings#sandbox-settings) is enabled, which blocks non-allowed domains automatically)"

  - *Implication*: This is a behavior clarification, not a new feature. Administrators relying on this setting for enterprise policy enforcement should confirm their understanding of the UX: users will not see a prompt asking to allow a new domain — it will simply be blocked silently.
  - *Source*: [settings.md](https://code.claude.com/docs/en/settings.md), [permissions.md](https://code.claude.com/docs/en/permissions.md), [sandboxing.md](https://code.claude.com/docs/en/sandboxing.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| statusline.md | Modified | +54/-1 | New Windows configuration section (PowerShell + Git Bash examples); two new troubleshooting tips |
| mcp.md | Modified | +22/-0 | New `authServerMetadataUrl` OAuth override option, requires v2.1.64+ |
| settings.md | Modified | +17/-17 | Clarified `network.allowManagedDomainsOnly` blocks silently (table reformatting only, no structural change) |
| permissions.md | Modified | +10/-10 | Same `allowManagedDomainsOnly` wording clarification in managed settings table |
| sandboxing.md | Modified | +1/-1 | Added inline note linking `allowManagedDomainsOnly` to silent domain blocking |
| changelog.md | Modified | +1/-1 | GitHub star count metadata update (73.6k → 73.7k); not substantive |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-05*
