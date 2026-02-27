# Claude API Documentation Changes — 2026-02-27

## Summary

Six documentation pages were modified in this update. The most substantive changes are to the TypeScript SDK page, which gained new documentation for the `ToolError` class and MCP helper utilities, and the get-started page, which was rewritten with a richer quickstart example and expanded output samples. Several pages received minor model name updates across code examples.

## Significant Changes

### SDKs — TypeScript

- **`ToolError` class for structured tool error responses**: The TypeScript SDK documentation now covers `ToolError`, importable from `@anthropic-ai/sdk/lib/tools/BetaRunnableTool`. Unlike a plain `Error`, `ToolError` accepts content blocks (text, images, etc.) as its payload, enabling tools to return rich error diagnostics to the model.

  > "To report an error from a tool back to the model, throw a `ToolError` from the `run` function. Unlike a plain `Error`, `ToolError` accepts content blocks, allowing you to include images or other structured content in the error response"

  ```typescript
  import { ToolError } from "@anthropic-ai/sdk/lib/tools/BetaRunnableTool";

  throw new ToolError([
    { type: "text", text: `Failed to load page: ${result.error}` },
    { type: "image", source: { type: "base64", data: result.screenshot, media_type: "image/png" } }
  ]);
  ```

  - *Implication*: Tool authors can now pass structured, multi-modal error context back to Claude instead of plain string messages, improving model-side error recovery in agentic workflows.
  - *Source*: [TypeScript SDK](https://platform.claude.com/docs/en/api/sdks/typescript.md)

- **MCP helper utilities added to TypeScript SDK**: A new MCP helpers section documents four utility functions exported from `@anthropic-ai/sdk/helpers/beta/mcp`: `mcpTools`, `mcpMessages`, `mcpResourceToContent`, and `mcpResourceToFile`. These convert MCP SDK types to Claude API types for use with `toolRunner`, `messages.create`, and `beta.files.upload`.

  > "These helpers convert MCP types to Claude API types, reducing boilerplate when working with MCP tools, prompts, and resources."

  The section also clarifies when to use the SDK helpers vs. the API-native `mcp_servers` parameter:

  > "Use `mcp_servers` when you have remote servers accessible via URL and only need tool support. Use the MCP helpers when you need local MCP servers, prompts, resources, or more control over the MCP connection."

  The section covers error handling via `UnsupportedMCPValueError` for unsupported content types and MIME types.

  - *Implication*: Developers building local MCP server integrations with the TypeScript SDK now have documented, first-party helpers instead of writing conversion glue code manually.
  - *Source*: [TypeScript SDK](https://platform.claude.com/docs/en/api/sdks/typescript.md)

### Get Started / Quickstart

- **Quickstart rewritten around a "web search assistant" example**: The get-started page was substantially revised (+36/-33 lines). The quickstart example now uses the prompt `"What should I search for to find the latest developments in renewable energy?"` across all SDK tabs (cURL, Python, TypeScript, Java), and the page now includes detailed representative output blocks for each tab.

  - *Implication*: The new example more clearly demonstrates a practical use case (research assistance) and shows what real-world API responses look like, which is more useful for evaluating the API than a minimal "Hello, Claude" prompt.
  - *Source*: [Get Started](https://platform.claude.com/docs/en/get-started.md)

### API — Errors

- **New section: prefill not supported on Claude Opus 4.6**: The errors page gained a "Common validation errors" section with a specific entry documenting that `claude-opus-4-6` does not support prefilling assistant messages. Sending a prefilled last assistant message returns `400 invalid_request_error`.

  > "Claude Opus 4.6 does not support prefilling assistant messages. Sending a request with a prefilled last assistant message to this model returns a 400 `invalid_request_error`"

  The section directs developers to use structured outputs, system prompt instructions, or `output_config.format` as alternatives.

  - *Implication*: This is an API behavioral constraint specific to `claude-opus-4-6` that developers migrating from older models should be aware of.
  - *Source*: [Errors](https://platform.claude.com/docs/en/api/errors.md)

### Model Name Updates (Cross-Page)

- Code examples in `beta-headers.md`, `client-sdks.md`, `errors.md`, and `openai-sdk.md` were updated to reference `claude-opus-4-6` in place of prior model identifiers. These are small edits (+1/-3 or +2/-7 lines per page) with no behavioral documentation changes.
  - *Source*: [Beta Headers](https://platform.claude.com/docs/en/api/beta-headers.md), [Client SDKs](https://platform.claude.com/docs/en/api/client-sdks.md), [Errors](https://platform.claude.com/docs/en/api/errors.md), [OpenAI SDK](https://platform.claude.com/docs/en/api/openai-sdk.md)

## Notable Details

- The Java SDK version in the `client-sdks.md` quick installation section is now listed as `2.11.1` (Gradle/Maven), while the get-started page still shows `1.0.0`. This discrepancy is worth noting if you are pinning a version from the quickstart.
- The TypeScript SDK tool helpers section now imports `betaZodTool` from `@anthropic-ai/sdk/helpers/beta/zod` (previously undocumented in this page). Combined with the new `ToolError` documentation, this section now covers the full lifecycle of tool definition, execution, and error handling.
- The `UnsupportedMCPValueError` thrown by MCP helpers covers: unsupported content types, unsupported MIME types, and non-http/https resource links — a specific set of constraints developers should validate against before deploying MCP integrations.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/api/sdks/typescript.md` | Modified | +31/-10 | Added ToolError class docs, MCP helper utilities section |
| `docs/api/en/get-started.md` | Modified | +36/-33 | Rewrote quickstart with web search assistant example and example outputs |
| `docs/api/en/api/openai-sdk.md` | Modified | +2/-7 | Model name updates in code examples |
| `docs/api/en/api/beta-headers.md` | Modified | +1/-3 | Model name update in code examples |
| `docs/api/en/api/client-sdks.md` | Modified | +1/-3 | Model name update in code examples |
| `docs/api/en/api/errors.md` | Modified | +1/-3 | Model name update; added prefill-not-supported validation error section |

---
*Generated from Claude API documentation changes detected on 2026-02-27*
