# Claude Code Documentation Changes — 2026-04-29

## Summary

16 pages modified in two releases (v2.1.122–v2.1.123). The headline change is that Git for Windows is no longer a hard requirement on native Windows — Claude Code now falls back to the PowerShell tool automatically when Git Bash is absent. Other significant additions: Amazon Bedrock service tier selection, a new keyboard shortcut to clear conversations, a new OpenTelemetry `at_mention` event, and a type change to `status_code` in telemetry events (string → number, breaking for consumers).

## Significant Changes

### Features

- **New keyboard shortcut to clear conversation (double `Ctrl+L` / `Cmd+K`)**: A new `chat:clearScreen` action (default: `Cmd+K`) was added to the keybindings table. The existing `chat:clearInput` (`Ctrl+L`) now doubles as a conversation-clear trigger in fullscreen mode: pressing it twice within two seconds runs `/clear`.
  > Press `Ctrl+L` twice within two seconds to run `/clear` and start a new conversation. The first press clears the input box and shows a hint; the second press clears the conversation. On macOS, double-pressing `Cmd+K` also runs `/clear`.
  - *Implication*: Fullscreen-mode users now have a keyboard-only path to reset conversation state without typing `/clear`.
  - *Source*: [Fullscreen rendering](https://code.claude.com/docs/en/fullscreen.md), [Keybindings](https://code.claude.com/docs/en/keybindings.md)

- **Session picker: paste a PR URL to find its session**: The `/resume` picker's search field now accepts GitHub, GitHub Enterprise, GitLab, and Bitbucket pull/merge request URLs and jumps to the session that created that PR.
  > Enter search mode and filter sessions. Paste a GitHub, GitHub Enterprise, GitLab, or Bitbucket pull or merge request URL to find the session that created it
  - *Implication*: Teams no longer need to remember session names for PR-linked sessions; pasting the PR URL is sufficient.
  - *Source*: [Common workflows](https://code.claude.com/docs/en/common-workflows.md)

- **New OpenTelemetry event: `claude_code.at_mention`**: A new observability event is emitted when Claude Code resolves an `@`-mention in a prompt. Covers file, directory, agent, and MCP resource mentions; early-exit paths (permission denials, oversized files, PDF references, directory listing failures) do not emit the event.

  **Event name**: `claude_code.at_mention`

  **Attributes**: `mention_type` (`"file"`, `"directory"`, `"agent"`, `"mcp_resource"`), `success` (`"true"` or `"false"`), plus all standard session attributes.
  - *Implication*: Teams using OpenTelemetry pipelines can now track `@`-mention resolution rates and failure modes per mention type.
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

### Configuration

- **Amazon Bedrock service tier selection via `ANTHROPIC_BEDROCK_SERVICE_TIER`**: New environment variable and documentation section for selecting a Bedrock inference service tier (`default`, `flex`, or `priority`), sent as the `X-Amzn-Bedrock-Service-Tier` header on each request.
  > Set `ANTHROPIC_BEDROCK_SERVICE_TIER` to `default`, `flex`, or `priority` [...] Claude Code sends this as the `X-Amzn-Bedrock-Service-Tier` header on each request. Tier availability varies by model and region. Reserved capacity uses a provisioned throughput ARN as the model ID instead of this setting.
  - *Implication*: Organizations on Amazon Bedrock can trade off latency against cost at the Claude Code level without custom proxy logic.
  - *Source*: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md), [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **Caps Lock added to list of reserved (non-rebindable) keys**: The keybindings reference now lists Caps Lock alongside Ctrl+C, Ctrl+D, and Ctrl+M as a key that cannot be rebound, with the reason "Not delivered to terminal applications."
  - *Source*: [Keybindings](https://code.claude.com/docs/en/keybindings.md), [Claude directory](https://code.claude.com/docs/en/claude-directory.md)

### Platform — Windows

- **Git for Windows downgraded from required to recommended; PowerShell used as automatic fallback**: Documentation across setup, quickstart, overview, tools-reference, env-vars, statusline, and troubleshoot-install changed language from "required" to "recommended." Claude Code now automatically enables the PowerShell tool when Git Bash is not found.
  > [Git for Windows](https://git-scm.com/downloads/win) is recommended on native Windows so Claude Code can use the Bash tool. If Git for Windows is not installed, Claude Code uses PowerShell as the shell tool instead.

  The `CLAUDE_CODE_USE_POWERSHELL_TOOL` env var behavior was updated to reflect this:
  > On Windows without Git Bash, the tool is enabled automatically; set to `0` to disable it. On Windows with Git Bash installed, the tool is rolling out progressively: set to `1` to opt in or `0` to opt out.
  - *Implication*: Windows users without Git for Windows can now use Claude Code out of the box. The Windows setup comparison table's "Requires" column now reads "Git for Windows recommended; PowerShell used if absent."
  - *Source*: [Setup](https://code.claude.com/docs/en/setup.md), [Quickstart](https://code.claude.com/docs/en/quickstart.md), [Overview](https://code.claude.com/docs/en/overview.md), [Tools reference](https://code.claude.com/docs/en/tools-reference.md), [Environment variables](https://code.claude.com/docs/en/env-vars.md), [Status line](https://code.claude.com/docs/en/statusline.md)

- **Windows troubleshooting section updated to reflect PowerShell as an alternative**: The error previously titled "Claude Code on Windows requires Git Bash" now reads "Claude Code on Windows requires either Git for Windows (for bash) or PowerShell." The fix now documents PowerShell 7 (`aka.ms/powershell`) as a valid alternative installation path.
  > Claude Code on native Windows needs at least one shell: either Git for Windows for Bash, or PowerShell. When neither is found, this error appears at startup. If only PowerShell is found, Claude Code uses the PowerShell tool instead of Bash.
  - *Source*: [Troubleshoot installation](https://code.claude.com/docs/en/troubleshoot-install.md)

### Integrations — MCP

- **Claude Code MCP server takes precedence over a matching claude.ai connector**: A new note clarifies behavior when a locally-added Claude Code MCP server and a claude.ai connector point to the same URL.
  > A server you've added in Claude Code takes precedence over a claude.ai connector that points at the same URL. When this happens, `/mcp` lists the connector as hidden and shows how to remove the duplicate if you'd rather use the connector.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

### Sandboxing

- **Network proxy TLS non-inspection explicitly documented**: A new callout note and an expanded security warning clarify that the built-in proxy makes allow/deny decisions from the client-supplied hostname without inspecting TLS traffic. Domain fronting is now explicitly named as a bypass risk.
  > The built-in proxy enforces the allowlist based on the requested hostname and does not terminate or inspect TLS traffic. See Security limitations for the implications of this design, and Custom proxy configuration if your threat model requires TLS inspection.

  > Allowing broad domains such as `github.com` can create paths for data exfiltration. Because the proxy makes its allow decision from the client-supplied hostname without inspecting TLS, code running inside the sandbox can potentially use domain fronting or similar techniques to reach hosts outside the allowlist. [...] Stronger TLS-aware network isolation is an active area of development.
  - *Implication*: Teams with strict security requirements should review this section and consider a TLS-terminating custom proxy.
  - *Source*: [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)

## Notable Details

- **`status_code` field in OTel events changed from string to number (breaking)**: Both `api_error` and `api_retries_exhausted` events had their `status_code` field type updated. Previously documented as a string (e.g., `"404"`), returning `"undefined"` for non-HTTP errors — it is now a number, and **absent entirely** for non-HTTP errors such as connection failures. Consumers parsing this field as a string will need updates.
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **v2.1.123 bug fix — OAuth 401 retry loop**: Fixed OAuth authentication failing with a 401 retry loop when `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` is set.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Status line Windows behavior now shell-aware**: On Windows, Claude Code runs status line commands through Git Bash when installed, or through PowerShell when Git Bash is absent. The bash-script example in the status line documentation is now labeled "when Git Bash is installed."
  - *Source*: [Status line](https://code.claude.com/docs/en/statusline.md)

- **PowerShell tool auto-enable on Windows without Git Bash**: The tools reference now explicitly states "On Windows without Git Bash, the tool is enabled automatically" rather than the previous "rolling out progressively on Windows and is opt-in on Linux, macOS, and WSL."
  - *Source*: [Tools reference](https://code.claude.com/docs/en/tools-reference.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| monitoring-usage.md | Modified | +17/-2 | New `claude_code.at_mention` OTel event; `status_code` type changed to number |
| keybindings.md | Modified | +22/-20 | New `chat:clearScreen` action (Cmd+K); Caps Lock added to reserved keys |
| common-workflows.md | Modified | +13/-13 | Session picker `/` search documents PR URL lookup; table reformatted |
| amazon-bedrock.md | Modified | +10/-0 | New "Service tiers" section for `ANTHROPIC_BEDROCK_SERVICE_TIER` |
| setup.md | Modified | +8/-8 | Git for Windows changed to recommended; PowerShell fallback; comparison table updated |
| troubleshoot-install.md | Modified | +7/-4 | Error message updated; PowerShell 7 added as resolution path |
| sandboxing.md | Modified | +6/-2 | TLS non-inspection callout and expanded security warning with domain fronting |
| fullscreen.md | Modified | +4/-0 | New "Clear the conversation" section (double Ctrl+L / Cmd+K) |
| changelog.md | Modified | +4/-0 | v2.1.123 OAuth bug fix entry |
| overview.md | Modified | +3/-3 | Git for Windows changed to recommended; PowerShell fallback |
| quickstart.md | Modified | +3/-3 | Git for Windows changed to recommended; PowerShell fallback |
| env-vars.md | Modified | +2/-1 | `ANTHROPIC_BEDROCK_SERVICE_TIER` added; `CLAUDE_CODE_USE_POWERSHELL_TOOL` description updated |
| mcp.md | Modified | +2/-0 | Claude Code server precedence over claude.ai connectors documented |
| statusline.md | Modified | +2/-2 | Windows status line now runs via Git Bash or PowerShell depending on what is installed |
| tools-reference.md | Modified | +1/-1 | PowerShell tool auto-enable clarified for Windows without Git Bash |
| claude-directory.md | Modified | +1/-1 | Caps Lock added to reserved keys in keybindings description |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-29*
