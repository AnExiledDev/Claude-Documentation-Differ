# Claude Code Documentation Changes — 2026-03-28

## Summary

Six pages were updated in this batch. The most substantive changes are a halving of the skill metadata character budget (2% → 1% of context window, 16,000 → 8,000 character fallback), a new per-session request header documented for LLM gateway operators, and a clarification that `CLAUDE_CODE_SIMPLE` / `--bare` mode still exposes MCP tools provided via `--mcp-config`. The remaining changes are wording clarifications and a macOS notification troubleshooting tip.

## Significant Changes

### Configuration

- **`CLAUDE_CODE_SIMPLE` / `--bare` mode now explicitly passes through MCP tools from `--mcp-config`**: The description of the `CLAUDE_CODE_SIMPLE` environment variable was updated to note that MCP tools provided via `--mcp-config` remain available even in bare mode.
  > `Set to 1 to run with a minimal system prompt and only the Bash, file read, and file edit tools. MCP tools from --mcp-config are still available. Disables auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md.`
  - *Implication*: Developers using `--bare` for lightweight scripted runs can still inject targeted MCP tools without enabling the full auto-discovery stack. This also clarifies a known bug fix documented in the v2.1.86 changelog.
  - *Source*: [env-vars.md](https://code.claude.com/docs/en/env-vars.md)

- **Skill metadata character budget halved**: `SLASH_COMMAND_TOOL_CHAR_BUDGET` now scales at **1% of the context window** with a **fallback of 8,000 characters**, down from 2% / 16,000.
  > `The budget scales dynamically at 1% of the context window, with a fallback of 8,000 characters. Legacy name kept for backwards compatibility`
  - *Implication*: Teams with many skills are more likely to see descriptions truncated. Developers should audit skill descriptions and front-load key use cases within the first 250 characters. The environment variable can be set to raise the limit.
  - *Source*: [env-vars.md](https://code.claude.com/docs/en/env-vars.md)

- **`DISABLE_FEEDBACK_COMMAND` opt-out value clarified**: The `/feedback` telemetry opt-out instruction now explicitly states the variable must be set to `1`.
  > `To opt out, set the DISABLE_FEEDBACK_COMMAND environment variable to 1.`
  - *Implication*: Aligns with the consistent pattern across Claude Code opt-out variables requiring value `1` rather than bare presence.
  - *Source*: [data-usage.md](https://code.claude.com/docs/en/data-usage.md)

### Skills

- **Skill descriptions truncated at 250 characters; behavior and FAQ section updated**: The FAQ entry "Claude doesn't see all my skills" was replaced with "Skill descriptions are cut short", reflecting a changed behavior: skill names are now always included in context, but descriptions are shortened to fit the budget.
  > `All skill names are always included, but if you have many skills, descriptions are shortened to fit the character budget, which can strip the keywords Claude needs to match your request. The budget scales dynamically at 1% of the context window, with a fallback of 8,000 characters.`

  The `description` frontmatter field documentation was also updated:
  > `Front-load the key use case: descriptions longer than 250 characters are truncated in the skill listing to reduce context usage.`

  The remediation advice was also updated:
  > `To raise the limit, set the SLASH_COMMAND_TOOL_CHAR_BUDGET environment variable. Or trim descriptions at the source: front-load the key use case, since each entry is capped at 250 characters regardless of budget.`
  - *Implication*: Skill authors should treat the first 250 characters of a description as the effective visibility boundary — this cap applies regardless of the overall budget. The previous guidance to run `/context` to check for excluded skills no longer applies in the same way, since names are always shown.
  - *Source*: [skills.md](https://code.claude.com/docs/en/skills.md)

### LLM Gateway / Proxies

- **New `X-Claude-Code-Session-Id` request header documented**: Claude Code now sends a `X-Claude-Code-Session-Id` header on every API request. A new "Request headers" table was added to the LLM gateway page.
  > `A unique identifier for the current Claude Code session. Proxies can use this to aggregate all API requests from a single session without parsing the request body.`
  - *Implication*: Gateway and proxy operators can use this header to correlate all API calls from a single Claude Code session for logging, rate-limiting, or cost attribution — without needing to inspect or parse request bodies.
  - *Source*: [llm-gateway.md](https://code.claude.com/docs/en/llm-gateway.md)

### Hooks

- **macOS notification troubleshooting tip added**: A new collapsible section ("If no notification appears") was added to the macOS tab of the hooks notification example. It explains that `osascript` routes through Script Editor, which can fail silently if notification permissions haven't been granted.
  > `osascript routes notifications through the built-in Script Editor app. If Script Editor doesn't have notification permission, the command fails silently, and macOS won't prompt you to grant it. Run this in Terminal once to make Script Editor appear in your notification settings: osascript -e 'display notification "test"'`

  The fix requires opening **System Settings > Notifications**, finding Script Editor, and enabling **Allow Notifications**.
  - *Implication*: Addresses a common silent failure point for the `Notification` hook event on macOS — previously there was no in-docs guidance for this scenario.
  - *Source*: [hooks-guide.md](https://code.claude.com/docs/en/hooks-guide.md)

## Notable Details

- **Keybindings wording only**: The `Attachments` context description changed from "Image/attachment bar navigation" to "Image attachment navigation in select dialogs", and `attachments:exit` changed from "Exit attachment bar" to "Exit attachment navigation". No keybinding behavior was changed.
- **Skill budget reduction may affect existing setups silently**: The shift from 16,000 to 8,000 character fallback is a meaningful reduction. Unlike the previous behavior (where skills could be excluded entirely with a `/context` warning), descriptions are now always truncated silently at 250 characters per entry. Existing skill definitions with long descriptions will have less content available to Claude without any visible warning.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| hooks-guide.md | Modified | +10/−0 | macOS notification troubleshooting accordion added |
| llm-gateway.md | Modified | +8/−0 | New `X-Claude-Code-Session-Id` request header table added |
| skills.md | Modified | +4/−4 | Skill description 250-char truncation documented; budget halved to 1%/8,000 chars; FAQ section renamed |
| env-vars.md | Modified | +2/−2 | `CLAUDE_CODE_SIMPLE` clarified (MCP tools from `--mcp-config` still available); `SLASH_COMMAND_TOOL_CHAR_BUDGET` budget updated to 1%/8,000 |
| keybindings.md | Modified | +2/−2 | Wording clarification for `Attachments` context and `attachments:exit` action |
| data-usage.md | Modified | +1/−1 | `DISABLE_FEEDBACK_COMMAND` opt-out now specifies value `1` |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-28*
