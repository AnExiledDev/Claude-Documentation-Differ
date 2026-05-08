# Claude Code Documentation Changes — 2026-03-19

## Summary

One page was updated today: the VS Code integration guide gained a new section documenting the built-in IDE MCP server that the extension runs locally. This is primarily relevant to teams using `PreToolUse` hooks to allowlist MCP tools, and to developers working in Jupyter notebooks within VS Code.

## Significant Changes

### IDE Integrations

- **Built-in IDE MCP server documented for VS Code**: A new section explains the local MCP server that the VS Code extension automatically starts when active. The server enables core CLI-to-editor features — opening diffs in VS Code's native diff viewer, reading the current selection for `@`-mentions, and executing Jupyter notebook cells.

  > When the extension is active, it runs a local MCP server that the CLI connects to automatically. This is how the CLI opens diffs in VS Code's native diff viewer, reads your current selection for `@`-mentions, and — when you're working in a Jupyter notebook — asks VS Code to execute cells.

  - *Implication*: The server is named `ide` and is intentionally hidden from `/mcp` (nothing to configure), but **teams using `PreToolUse` hooks to allowlist MCP tools must explicitly account for it** — the hook-visible tool names (`mcp__ide__getDiagnostics`, `mcp__ide__executeCode`) won't surface in `/mcp`.
  - *Source*: [VS Code Integration](https://code.claude.com/docs/en/vs-code.md)

- **Two model-visible tools exposed by the IDE server**: The documentation specifies that of the dozen tools the server hosts, only two are visible to Claude. The rest are internal RPC (for diff viewing, selection reading, file saving) and are filtered out before the tool list reaches the model.

  | Tool name (as seen by hooks) | What it does | Writes? |
  |---|---|---|
  | `mcp__ide__getDiagnostics` | Returns language-server diagnostics from VS Code's Problems panel; optionally scoped to one file | No |
  | `mcp__ide__executeCode` | Runs Python code in the active Jupyter notebook's kernel | Yes |

  - *Implication*: Allowlist entries for these tools use the `mcp__ide__` prefix. Hook configurations that filter by tool name prefix need to include `mcp__ide__` to permit diagnostics access or Jupyter execution.
  - *Source*: [VS Code Integration](https://code.claude.com/docs/en/vs-code.md)

- **Jupyter notebook execution requires mandatory in-editor confirmation**: `mcp__ide__executeCode` cannot run code silently. Every invocation inserts the code as a new cell at the end of the active notebook and presents a native VS Code Quick Pick prompting **Execute** or **Cancel**. Cancelling or pressing `Esc` returns an error to Claude; nothing runs.

  > The Quick Pick confirmation is separate from `PreToolUse` hooks. An allowlist entry for `mcp__ide__executeCode` lets Claude *propose* running a cell; the Quick Pick inside VS Code is what lets it *actually* run.

  The tool also refuses outright when: no notebook is active, the Jupyter extension (`ms-toolsai.jupyter`) is not installed, or the kernel is not Python.

  - *Implication*: This is a two-layer permission model. Even with a permissive `PreToolUse` hook, users retain a mandatory in-editor confirmation gate for every notebook cell execution — `PreToolUse` approval is necessary but not sufficient.
  - *Source*: [VS Code Integration](https://code.claude.com/docs/en/vs-code.md)

- **Local-only transport with per-activation auth token**: The server binds exclusively to `127.0.0.1` on a random high port (not reachable from other machines). A fresh random auth token is generated on each extension activation and written to a lock file under `~/.claude/ide/` with `0600` permissions in a `0700` directory.

  > The server binds to `127.0.0.1` on a random high port and is not reachable from other machines. Each extension activation generates a fresh random auth token that the CLI must present to connect. The token is written to a lock file under `~/.claude/ide/` with `0600` permissions in a `0700` directory, so only the user running VS Code can read it.

  - *Implication*: No network-accessible attack surface and no persistent credential. The security posture is scoped strictly to the local user.
  - *Source*: [VS Code Integration](https://code.claude.com/docs/en/vs-code.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/claude-code/en/vs-code.md` | Modified | +21 / -0 | New section: "The built-in IDE MCP server" — documents transport, auth, tool surface (`mcp__ide__getDiagnostics`, `mcp__ide__executeCode`), and Jupyter execution confirmation flow |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-19*
