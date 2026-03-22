# Claude Code Documentation Changes — 2026-03-22

## Summary

Nine pages were modified with no pages added or removed (472 additions, 94 deletions). The largest change is the addition of a **permission relay** capability to the Channels API, enabling channel servers to forward tool-use approval prompts to remote users (e.g. via phone over Telegram or Discord). A second meaningful change documents the new `--bare` CLI flag for scripted and CI use, which skips all auto-discovery at startup and is flagged as the future default for `-p` mode.

---

## Significant Changes

### Channels: Permission Relay (New Capability)

- **Remote tool-use approval via channels**: Two-way channel servers can now opt in to receive permission prompts in parallel with the local terminal dialog, enabling a developer away from their desk to approve or deny `Bash`, `Write`, and `Edit` calls remotely. Requires **Claude Code v2.1.81 or later**.
  > "A two-way channel can opt in to receive the same prompt in parallel and relay it to you on another device. Both stay live: you can answer in the terminal or on your phone, and Claude Code applies whichever answer arrives first and closes the other."
  - *Implication*: Channel builders must declare `capabilities.experimental['claude/channel/permission']: {}` in the `Server` constructor. Claude Code then sends `notifications/claude/channel/permission_request` notifications to the server when a dialog opens, and accepts verdicts via `notifications/claude/channel/permission` with `request_id` and `behavior: 'allow' | 'deny'`. Earlier versions silently ignore the capability.
  - *Source*: [Channels reference](https://code.claude.com/docs/en/channels-reference.md)

- **`notifications/claude/channel/permission_request` schema**: The outbound notification carries four fields:

  | Field           | Description |
  |-----------------|-------------|
  | `request_id`    | Five lowercase letters (`a`–`z`, excluding `l`) so the ID is unambiguous when typed on a phone |
  | `tool_name`     | Name of the tool, e.g. `Bash` or `Write` |
  | `description`   | Human-readable summary of the specific call — same text shown in the local dialog |
  | `input_preview` | Tool arguments as JSON, truncated to 200 characters |

  The inbound verdict uses `yes <id>` / `no <id>` format. The documentation provides a reference regex: `/^\s*(y|yes|n|no)\s+([a-km-z]{5})\s*$/i`.
  - *Source*: [Channels reference](https://code.claude.com/docs/en/channels-reference.md)

- **Security: allowlist gates permission relay**: The sender allowlist that already controls inbound chat messages also gates permission relay. This was added to both `channels-reference.md` and the Security section of `channels.md`.
  > "Only declare the capability if your channel authenticates the sender, because anyone who can reply through your channel can approve or deny tool use in your session."
  - *Source*: [Channels](https://code.claude.com/docs/en/channels.md), [Channels reference](https://code.claude.com/docs/en/channels-reference.md)

- **Updated `Server` options table**: `capabilities.experimental['claude/channel/permission']` was added as a new optional field alongside the existing `claude/channel` entry.
  - *Source*: [Channels reference](https://code.claude.com/docs/en/channels-reference.md)

- **Webhook example upgraded with SSE**: The full two-way `webhook.ts` example was reworked to use Server-Sent Events on `GET /events` so developers can watch Claude's replies and permission prompts arrive live via `curl -N localhost:8788/events`. The previous version wrote replies to stderr.
  - *Source*: [Channels reference](https://code.claude.com/docs/en/channels-reference.md)

- **Troubleshooting steps added to webhook walkthrough**: Two diagnostic bullet points were added for when events don't arrive:
  > "**`curl` succeeds but nothing reaches Claude**: run `/mcp` in your session to check the server's status... check the debug log at `~/.claude/debug/<session-id>.txt`"
  > "**`curl` fails with 'connection refused'**: the port is either not bound yet or a stale process is holding it. `lsof -i :<port>` shows what's listening."
  - *Source*: [Channels reference](https://code.claude.com/docs/en/channels-reference.md)

---

### CLI: New `--bare` Flag for Scripted Use

- **`--bare` flag documented**: A new flag that skips auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md. Reduces startup time and ensures consistent, environment-independent behavior.
  > "`--bare` is the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release."
  - *Implication*: Teams running `claude -p` in CI should add `--bare` now. Authentication in bare mode requires `ANTHROPIC_API_KEY` or `apiKeyHelper` in `--settings`; OAuth/keychain reads are skipped. The flag internally sets `CLAUDE_CODE_SIMPLE=1`.
  - *Source*: [CLI reference](https://code.claude.com/docs/en/cli-reference.md), [Run Claude Code programmatically](https://code.claude.com/docs/en/headless.md)

- **Context-loading reference table for bare mode** (from `headless.md`):

  | To load                 | Use                                                     |
  |-------------------------|---------------------------------------------------------|
  | System prompt additions | `--append-system-prompt`, `--append-system-prompt-file` |
  | Settings                | `--settings <file-or-json>`                             |
  | MCP servers             | `--mcp-config <file-or-json>`                           |
  | Custom agents           | `--agents <json>`                                       |
  | A plugin directory      | `--plugin-dir <path>`                                   |

  - *Source*: [Run Claude Code programmatically](https://code.claude.com/docs/en/headless.md)

---

### Settings: New `showClearContextOnPlanAccept` Option

- **`showClearContextOnPlanAccept` setting added**: Controls whether the "clear context" option is shown on the plan accept screen. Defaults to `false`.
  > "Show the 'clear context' option on the plan accept screen. Defaults to `false`. Set to `true` to restore the option."
  - *Implication*: This indicates the option was hidden by default in a recent release. Teams that relied on clearing context at plan acceptance should add this to their settings.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

---

### MCP: OAuth Client ID Metadata Document (CIMD) Support

- **CIMD OAuth discovery added**: Claude Code now attempts to auto-discover MCP servers using a Client ID Metadata Document in addition to Dynamic Client Registration (DCR).
  > "Claude Code also supports servers that use a Client ID Metadata Document (CIMD) instead of Dynamic Client Registration, and discovers these automatically. If automatic discovery fails, register an OAuth app through the server's developer portal first."
  - *Implication*: Fewer OAuth-protected MCP servers should require manual credential pre-registration, as CIMD is now tried automatically.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

---

## Notable Details

- **`CLAUDE_CODE_SIMPLE` description expanded** (`env-vars.md`): Previously described as "Disables MCP tools, attachments, hooks, and CLAUDE.md files." Now reads: "Disables auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md." The new description aligns with what `--bare` does, adding "auto memory" and "skills" to the affected list.

- **`--bare` as future default — a compatibility signal**: The documentation explicitly flags `--bare` as the future default for `claude -p`. Existing scripts that depend on `claude -p` loading `.mcp.json`, CLAUDE.md, or hooks will break when that default changes.

- **`how-claude-code-works.md` context window description**: "auto memory" was added to the list of items that populate Claude's context window. Minor clarification confirming auto memory occupies context space alongside CLAUDE.md and loaded skills.

- **`interactive-mode.md` Ctrl+O context expanded**: The `Ctrl+O` (Toggle verbose output) shortcut now notes it "Also expands MCP read and search calls, which collapse to a single line like 'Queried slack' by default." The remaining +18/-18 line delta in this file is table column-width reformatting with no other content change.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| channels-reference.md | Modified | +361/-15 | New "Relay permission prompts" section with protocol spec, full TypeScript examples with SSE, and troubleshooting |
| headless.md | Modified | +29/-1 | New "Start faster with bare mode" subsection; CI guidance and context-loading table |
| cli-reference.md | Modified | +57/-56 | Added `--bare` flag to CLI flags table; remainder is table column-width reformatting |
| interactive-mode.md | Modified | +18/-18 | Expanded `Ctrl+O` description for MCP call collapsing; table column-width reformatting |
| channels.md | Modified | +3/-1 | Updated permission prompt note; security warning for permission relay added |
| settings.md | Modified | +1/-0 | New `showClearContextOnPlanAccept` setting |
| env-vars.md | Modified | +1/-1 | `CLAUDE_CODE_SIMPLE` description updated to match `--bare` behavior |
| how-claude-code-works.md | Modified | +1/-1 | "auto memory" added to context window description |
| mcp.md | Modified | +1/-1 | CIMD OAuth auto-discovery added to OAuth setup documentation |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-22*
