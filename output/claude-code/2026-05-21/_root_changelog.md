# Claude Code Documentation Changes — 2026-05-21

## Summary

Two new documentation pages were added: one dedicated to organizational MCP server access control (`managed-mcp.md`) and one comparing sandbox environment approaches (`sandbox-environments.md`). Alongside these additions, the sandboxing reference page was substantially restructured to focus specifically on the built-in sandboxed Bash tool, and 227 lines of MCP admin content was extracted from `mcp.md` into the new dedicated page. The product changelog was also updated with two new release entries covering versions 2.1.145 and 2.1.147.

---

## Significant Changes

### Documentation Restructuring

- **MCP admin controls moved to dedicated page**: The "Manage MCP servers for your organization" content — covering `managed-mcp.json`, allowlists, denylists, and restriction evaluation — has been removed from `mcp.md` (-227 lines) and relocated to the new `managed-mcp.md` page with expanded detail.
  > `mcp.md` previously contained `### Option 1: Exclusive control with managed-mcp.json` and `### Option 2: Policy-based control with allowlists and denylists` along with all sub-sections on restriction options, URL matching, and evaluation order.
  - *Implication*: Developers looking for MCP connection setup are no longer distracted by organizational policy content; administrators get a more complete reference. Existing links into the admin sections of `mcp.md` will need to be updated to `managed-mcp.md`.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

- **Sandboxing page rewritten and refocused**: `sandboxing.md` was substantially restructured (+211/-177 lines). The page is renamed from "Sandboxing" to "Configure the sandboxed Bash tool" and reorganized around practical configuration tasks rather than conceptual overview.
  > New top-level structure: *Get started → Configure sandboxing → How sandboxing works → How sandboxing relates to permissions and permission modes → Configure the sandbox for your organization → Troubleshooting → Limitations*
  - *Implication*: Sections on "Why sandboxing matters", "Security benefits", "Best practices", "Integration with existing security tools", and "Open source" have been removed in favor of direct configuration guidance and troubleshooting. The new "Limitations" section is split into *Security limitations*, *Platform and tool compatibility*, and *Scope* subsections.
  - *Source*: [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)

### New Pages

- **`managed-mcp.md`** — New dedicated reference for organizational MCP server access control. Covers the full spectrum of restriction patterns from disabling MCP entirely through fine-grained allowlists/denylists.
  > "Claude Code supports a range of restriction levels. Each pattern uses one or both of the mechanisms covered below: `managed-mcp.json` for deploying a fixed set, and `allowedMcpServers`/`deniedMcpServers` for filtering what users configure."
  
  Key content includes:
  - A pattern-selection table (Disable MCP / Fixed deployment / Approved catalog / Plugin servers only / Soft allowlist / Denylist only / No restrictions)
  - `managed-mcp.json` file format and deployment paths per platform (macOS, Linux/WSL, Windows)
  - URL wildcard matching semantics (`*` anywhere in the pattern, case-insensitive hostname matching)
  - Exact command matching semantics for stdio servers
  - The full server evaluation order (merge lists → denylist check → allowlist check)
  - `allowManagedMcpServersOnly` flag to prevent users from broadening the allowlist
  - `claude mcp list` and `claude mcp add` validation commands to confirm policy is active
  
  > "An allowlist that uses only `serverName` entries is not a security control. The name is the label a user assigns when running `claude mcp add`... so a user can call any server `github`. To enforce which servers actually run, add `serverCommand` or `serverUrl` entries."
  - *Implication*: Administrators now have a single, comprehensive reference for MCP governance. The warning about `serverName` as a non-security control is an important clarification for policy design.
  - *Source*: [Control MCP server access for your organization](https://code.claude.com/docs/en/managed-mcp.md)

- **`sandbox-environments.md`** — New comparison guide for all Claude Code isolation approaches.
  > "Claude Code can run in several kinds of isolated environments, ranging from a lightweight per-command sandbox to a fully separate virtual machine."
  
  Covers and compares six approaches in a single reference table:
  | Approach | What is isolated | Requires Docker |
  |---|---|---|
  | Sandboxed Bash tool | Bash commands and child processes | No |
  | Sandbox runtime | Whole Claude Code process | No |
  | Dev container | Full dev environment | Yes |
  | Custom container | Full dev environment | Yes |
  | Virtual machine | Full OS | No |
  | Claude Code on the web | Full OS, Anthropic-hosted | No |
  
  Also documents the `@anthropic-ai/sandbox-runtime` beta package, which wraps the entire Claude Code process in Seatbelt/bubblewrap isolation (not just Bash commands), and organizational enforcement options per approach.
  - *Implication*: Fills a navigation gap — previously there was no single page to compare all isolation options. The sandbox runtime (`npx @anthropic-ai/sandbox-runtime claude`) is surfaced here as an alternative to Docker for teams wanting full-process isolation.
  - *Source*: [Choose a sandbox environment](https://code.claude.com/docs/en/sandbox-environments.md)

### Features & Releases (changelog.md)

Two new version entries were added to the product changelog:

**Version 2.1.147 (May 21, 2026)**
- **`Workflow` tool for deterministic multi-agent orchestration** — Disabled by default; enable with `CLAUDE_CODE_WORKFLOWS=1`.
- **Pinned background sessions** — `Ctrl+T` in `claude agents` keeps a session alive when idle, restarts in place for updates, and is shed under memory pressure only after non-pinned sessions.
- **`/simplify` renamed to `/code-review`** — New behavior reports correctness bugs at a configurable effort level (e.g., `/code-review high`); pass `--comment` to post findings as inline GitHub PR comments. The previous cleanup-and-fix behavior has been removed.
- **Hardened sandboxes** — REPL and Workflow tool sandboxes hardened against prototype-pollution and thenable-based escape techniques.
- **Enterprise login fix** — Fixed `forceLoginOrgUUID` and `forceLoginMethod` managed-settings not being enforced for third-party-provider and API-key sessions.
- **Prompt history deduplication** — Consecutive duplicate entries are no longer recorded; re-submitting a recalled prompt won't add another copy.
- Multiple additional bug fixes covering Windows-specific issues, MCP paginated resource handling, PowerShell tool behavior, auto mode, background sessions, and rendering glitches.

**Version 2.1.145 (May 19, 2026)**
- **`claude agents --json`** — Lists live Claude sessions as JSON for scripting use cases (tmux-resurrect, status bars, session pickers).
- **OTEL span enrichment** — `agent_id` and `parent_agent_id` added to `claude_code.tool` spans; background subagent spans now nest correctly under their dispatching Agent tool span.
- **Status line GitHub context** — Status line JSON input now includes GitHub repo and PR info when detected.
- **Plugin pre-install preview** — `/plugin` Discover and Browse screens now show a plugin's commands, agents, skills, hooks, and MCP/LSP servers before installation.
- **Permission-prompt bypass fix** — Fixed a bypass where bare variable assignments to non-allowlisted environment variables in Bash commands were auto-approved.
- *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Administration

- **`admin-setup.md` updated**: The "Decide what to enforce" table now links to `/en/managed-mcp` for MCP server control and lists `allowedMcpServers`, `deniedMcpServers`, `allowManagedMcpServersOnly`, and `managed-mcp.json` as the key settings.
  - *Implication*: The admin setup page now correctly cross-references the new dedicated page rather than the old inline `mcp.md` section.
  - *Source*: [Set up Claude Code for your organization](https://code.claude.com/docs/en/admin-setup.md)

- **`settings.md` updated**: +10/-10 lines, consistent with reference updates to point `managed-mcp.json` documentation to the new page and reflect updated file-based settings paths.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

---

## Minor Changes

- **`auto-mode-config.md`**: Minor text update (+1/-1 lines). (+1/-1)
- **`desktop.md`**: Minor text update (+1/-1 lines). (+1/-1)
- **`devcontainer.md`**: One line added, likely a cross-reference to the new `sandbox-environments.md` page. (+1/-0)
- **`glossary.md`**: One term or definition updated (+1/-1 lines). (+1/-1)
- **`permission-modes.md`**: Minor text or link updates (+2/-2 lines). (+2/-2)
- **`permissions.md`**: Minor text or link updates (+2/-2 lines). (+2/-2)
- **`security.md`**: Updated references and minor wording adjustments (+6/-5 lines). Cross-references to `sandboxing.md` likely updated to reflect new page title. (+6/-5)
- **`server-managed-settings.md`**: One-line update (+1/-1 lines). (+1/-1)

---

## New Pages

- **`managed-mcp.md`** — Comprehensive administrator guide for controlling MCP server access, including `managed-mcp.json` deployment, allowlists/denylists, URL wildcards, and evaluation order. [View](https://code.claude.com/docs/en/managed-mcp.md)
- **`sandbox-environments.md`** — Comparison guide for all Claude Code isolation approaches (sandboxed Bash tool, sandbox runtime, dev containers, custom containers, VMs, Claude Code on the web). [View](https://code.claude.com/docs/en/sandbox-environments.md)

---

## Migration Notes

- **`/simplify` command removed**: The `/simplify` command has been renamed `/code-review` with a fundamentally different behavior. The old cleanup-and-fix behavior is gone; the new command focuses on reporting correctness bugs. Any workflows or documentation referencing `/simplify` should be updated to `/code-review`.
- **Links to MCP admin sections in `mcp.md`**: Internal links to `mcp.md#option-1-exclusive-control-with-managed-mcp-json`, `mcp.md#option-2-policy-based-control`, or related anchors will be broken. These sections now live at `managed-mcp.md`.

---

## Notable Details

- The `@anthropic-ai/sandbox-runtime` package (`npx @anthropic-ai/sandbox-runtime claude`) is now documented in `sandbox-environments.md` as a beta research preview. It applies Seatbelt/bubblewrap to the *entire* Claude Code process — covering built-in file tools, MCP servers, and hooks — not just Bash commands. Configuration format may change.
- The `allowManagedMcpServersOnly` setting is explicitly distinguished from `allowManagedPermissionRulesOnly`: setting the latter does *not* enforce the MCP allowlist. This is a common misconfiguration surface.
- The `Workflow` tool (v2.1.147, `CLAUDE_CODE_WORKFLOWS=1`) represents a new capability class: deterministic multi-agent orchestration, distinct from the existing agentic patterns. Being off-by-default and env-var gated signals it is in early rollout.
- The enterprise login bypass fix (v2.1.147) is a security-relevant correction: `forceLoginOrgUUID` and `forceLoginMethod` were previously not enforced for third-party-provider and API-key sessions, meaning managed login restrictions could be bypassed.

---

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| managed-mcp.md | New | SIGNIFICANT | new | Dedicated MCP organizational access control reference |
| sandbox-environments.md | New | SIGNIFICANT | new | Sandbox approach comparison guide |
| sandboxing.md | Modified | SIGNIFICANT | +211/-177 | Full restructure: renamed and refocused on Bash tool configuration |
| mcp.md | Modified | SIGNIFICANT | +1/-227 | MCP admin sections extracted to managed-mcp.md |
| changelog.md | Modified | SIGNIFICANT | +32/-13 | Added v2.1.147 and v2.1.145 release notes |
| admin-setup.md | Modified | SIGNIFICANT | +12/-12 | Updated MCP control row to reference managed-mcp.md |
| settings.md | Modified | SIGNIFICANT | +10/-10 | Reference updates for managed-mcp.json documentation |
| security.md | Modified | SIGNIFICANT | +6/-5 | Minor wording and reference updates |
| permission-modes.md | Modified | MINOR | +2/-2 | Minor text/link updates |
| permissions.md | Modified | MINOR | +2/-2 | Minor text/link updates |
| auto-mode-config.md | Modified | MINOR | +1/-1 | Minor text update |
| desktop.md | Modified | MINOR | +1/-1 | Minor text update |
| glossary.md | Modified | MINOR | +1/-1 | Minor term update |
| server-managed-settings.md | Modified | MINOR | +1/-1 | Minor text update |
| devcontainer.md | Modified | MINOR | +1/-0 | One line added |

---

*Generated from Claude Code CLI documentation changes detected on 2026-05-21*
