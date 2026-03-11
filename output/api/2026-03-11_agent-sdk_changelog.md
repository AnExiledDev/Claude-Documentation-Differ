# Claude API Documentation Changes — 2026-03-11

## Summary

Six Agent SDK documentation pages were updated with internal anchor link corrections across Python and TypeScript reference pages. No API behavior, parameters, or features changed — all modifications are documentation fixes converting camelCase fragment identifiers to kebab-case equivalents.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| [agent-sdk/typescript.md](https://platform.claude.com/docs/en/agent-sdk/typescript.md) | Modified | +17/-17 | Anchor links updated to kebab-case; trailing comma removed from code example |
| [agent-sdk/python.md](https://platform.claude.com/docs/en/agent-sdk/python.md) | Modified | +9/-9 | Anchor links in options table updated to kebab-case |
| [agent-sdk/user-input.md](https://platform.claude.com/docs/en/agent-sdk/user-input.md) | Modified | +5/-5 | Anchor link and tool input schema link corrected; trailing commas removed |
| [agent-sdk/hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md) | Modified | +1/-1 | Anchor link for `max_turns` corrected |
| [agent-sdk/quickstart.md](https://platform.claude.com/docs/en/agent-sdk/quickstart.md) | Modified | +1/-1 | Options reference links corrected for both Python and TypeScript |
| [agent-sdk/subagents.md](https://platform.claude.com/docs/en/agent-sdk/subagents.md) | Modified | +1/-1 | `AgentDefinition` anchor links corrected |

## Notable Details

All changes follow a consistent pattern: camelCase anchor fragments were renamed to kebab-case to match standard HTML heading slug generation. The affected anchors include:

- `#sdkbeta` → `#sdk-beta`
- `#canusetool` → `#can-use-tool`
- `#sandboxsettings` → `#sandbox-settings`
- `#sandboxnetworkconfig` → `#sandbox-network-config`
- `#sandboxignoreviolations` → `#sandbox-ignore-violations`
- `#sandboxfilesystemconfig` → `#sandbox-filesystem-config`
- `#thinkingconfig` → `#thinking-config`
- `#streamevent` → `#stream-event`
- `#assistantmessageerror` → `#assistant-message-error`
- `#hookjsonoutput` → `#hook-json-output`
- `#hookevent` → `#hook-event`
- `#hookcallbackmatcher` → `#hook-callback-matcher`
- `#mcpserverconfig` → `#mcp-server-config`
- `#permissionmode` → `#permission-mode`
- `#permissionupdate` → `#permission-update`
- `#sdkpluginconfig` → `#sdk-plugin-config`
- `#agentdefinition` → `#agent-definition`
- `#sdkmessage` / `#sdkusermessage` → `#sdk-message` / `#sdkuser-message`
- `#calltoolresult` → `#call-tool-result`
- `#configuration-options` → `#claude-agent-options` (hooks.md, `max_turns` docs link)
- `#claudeagentoptions` → `#claude-agent-options` (quickstart.md)
- `tool-inputoutput-types` → `tool-input-output-types` (user-input.md)

The TypeScript reference page (`typescript.md`) also had a trailing comma removed from a code snippet inside the `getSessionMessages` example, and `user-input.md` had trailing commas removed from a `toolConfig` / `canUseTool` code block. These are cosmetic code style fixes with no functional impact.

---
*Generated from Claude API documentation changes detected on 2026-03-11*
