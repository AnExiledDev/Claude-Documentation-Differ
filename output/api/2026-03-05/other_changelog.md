# Claude API Documentation Changes — 2026-03-05

## Summary

The most significant update is a near-complete rewrite of the streaming refusals handling page, which documents the `stop_reason: "refusal"` API behavior introduced with Claude 4 models. The Agent SDK permissions page received substantial new content documenting allow/deny rules and the TypeScript-only `dontAsk` permission mode.

## Significant Changes

### Streaming API — Refusal Handling

- **New `stop_reason: "refusal"` documentation**: The streaming refusals page has been substantially expanded (+206 lines) to fully document how Claude 4+ models signal policy violations during streaming. When a streaming classifier intervenes, the API returns `stop_reason: "refusal"` with no additional message body.

  > Starting with Claude 4 models, streaming responses from Claude's API return **`stop_reason`: `"refusal"`** when streaming classifiers intervene to handle potential policy violations.

  Key behaviors documented:
  - **Mandatory context reset**: After receiving a `refusal` stop reason, the refused turn must be removed or updated before continuing. Continuing without resetting causes repeated refusals.
  - **Billing still applies**: Usage metrics (and token billing) are reported even for refused responses, up to the point of refusal.
  - **Test trigger string**: A magic string is provided for testing refusal handling locally: `ANTHROPIC_MAGIC_STRING_TRIGGER_REFUSAL_1FAEFB6177B4672DEE07F9D3AFC62588CCD2631EDCF22E8CCC1FB35B501C9C86`
  - **Three distinct refusal types** are now documented:

    | Refusal Type | Response Format | When It Occurs |
    |---|---|---|
    | Streaming classifier refusals | `stop_reason: "refusal"` | During streaming, policy violation |
    | API input and copyright validation | 400 error codes | Input fails validation |
    | Model-generated refusals | Standard text responses | Model self-refuses |

  > Future API versions will expand the **`stop_reason`: `refusal`** pattern to unify refusal handling across all types.

  - *Implication*: Developers using streaming with Claude 4+ models must add explicit checks for `stop_reason === "refusal"` in their event loops and implement context reset logic. The page includes working examples for Python, TypeScript, Go, Java, C#, PHP, Ruby, and Shell.
  - *Source*: [Handle Streaming Refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md)

### Agent SDK — Permissions

- **New "Allow and deny rules" section**: The permissions page was significantly expanded to clarify how `allowed_tools`/`allowedTools` and `disallowed_tools`/`disallowedTools` behave within the permission evaluation pipeline. These options add entries to the allow/deny rule lists but do not restrict which tools are visible to Claude.

  > `allowed_tools` and `disallowed_tools` (TypeScript: `allowedTools` / `disallowedTools`) add entries to the allow and deny rule lists in the evaluation flow above. They control whether a tool call is approved, not whether the tool is available to Claude.

  - *Implication*: The distinction is critical: `allowed_tools=["Read"]` does not prevent Claude from attempting to call `Bash` — it only means `Read` is auto-approved. Unlisted tools fall through to the permission mode.

- **`bypassPermissions` + `allowed_tools` warning**: Documentation now explicitly states that `allowed_tools` does not constrain `bypassPermissions` mode.

  > Setting `allowed_tools=["Read"]` alongside `permission_mode="bypassPermissions"` still approves every tool, including `Bash`, `Write`, and `Edit`. If you need `bypassPermissions` but want specific tools blocked, use `disallowed_tools`.

  - *Implication*: Developers combining these two options expecting a restricted bypass mode will be surprised. Use `disallowed_tools` for explicit blocks when using `bypassPermissions`.

- **New `dontAsk` permission mode (TypeScript only)**: A new `dontAsk` permission mode is now documented. It converts any unresolved permission prompt into a denial instead of calling `canUseTool`, making it suitable for headless locked-down agents.

  > Converts any permission prompt into a denial. Tools pre-approved by `allowed_tools`, `settings.json` allow rules, or a hook run as normal. Everything else is denied without calling `canUseTool`.

  Example for a locked-down TypeScript agent:
  ```typescript
  const options = {
    allowedTools: ["Read", "Glob", "Grep"],
    permissionMode: "dontAsk"
  };
  ```

  > `dontAsk` is available in the TypeScript SDK only. In Python, there is no exact equivalent. Use `disallowed_tools` to explicitly block tools you don't want Claude to use.

  - *Implication*: TypeScript developers building headless agents now have a first-class mode to enforce a fixed tool surface without relying on the absence of a `canUseTool` callback. Python developers must use `disallowed_tools` as a workaround.
  - *Source*: [Configure Permissions](https://platform.claude.com/docs/en/agent-sdk/permissions.md)

### Agent SDK — SDK Rename

- **Claude Code SDK renamed to Claude Agent SDK**: The overview page and several other Agent SDK pages reflect the SDK's rename from "Claude Code SDK" to "Claude Agent SDK". Package names have also been updated (`claude_agent_sdk` for Python, `@anthropic-ai/claude-agent-sdk` for TypeScript). A migration guide is referenced for users of the old SDK.

  > The Claude Code SDK has been renamed to the Claude Agent SDK. If you're migrating from the old SDK, see the [Migration Guide](/docs/en/agent-sdk/migration-guide).

  - *Implication*: Developers using the old package names should update their install commands and imports. The migration guide linked from the overview page provides specifics.
  - *Source*: [Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview.md)

### Get Started Page

- **Example model updated to `claude-opus-4-6`**: All code examples across the cURL, Python, TypeScript, and Java quickstart tabs now use `claude-opus-4-6` as the demonstration model, with corresponding example outputs reflecting this model's identifier.
  - *Source*: [Get Started](https://platform.claude.com/docs/en/get-started.md)

### Resources Overview

- **Minor content removal**: Four lines were removed from the resources overview page. Based on the remaining content, model cards for current Claude 4 and 4.x-series models are still present; the removed entries likely represented outdated or duplicate resource links.
  - *Source*: [Resources Overview](https://platform.claude.com/docs/en/resources/overview.md)

## Notable Details

- The `stop_reason: "refusal"` signal is distinct from HTTP 400 errors and model-level text refusals. These three refusal types are now explicitly delineated; developers should handle all three separately.
- The `dontAsk` mode skips the `canUseTool` callback entirely, which changes the flow for any application that relies on that callback for audit logging or conditional approval. Hooks still execute before `dontAsk` takes effect, so hook-based audit trails remain intact.
- The deny evaluation order is: hooks → deny rules → permission mode → allow rules → `canUseTool`. Deny rules (`disallowed_tools`) are evaluated before the permission mode, meaning they block tools even in `bypassPermissions` mode.
- The `develop-tests.md` page received 2 minor additions (no new sections), likely a small clarification or example update.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| handle-streaming-refusals.md | Modified | +206/-2 | Near-complete rewrite: documents `stop_reason: "refusal"`, reset behavior, multi-SDK examples, refusal type table |
| agent-sdk/permissions.md | Modified | +50/-9 | New allow/deny rules section, `dontAsk` mode docs, `bypassPermissions` + `allowed_tools` warning |
| get-started.md | Modified | +25/-24 | Example model updated to `claude-opus-4-6` across all SDK tabs |
| agent-sdk/overview.md | Modified | +4/-5 | SDK rename from Claude Code SDK to Claude Agent SDK |
| agent-sdk/skills.md | Modified | +4/-4 | Minor updates (likely SDK rename references) |
| agent-sdk/quickstart.md | Modified | +3/-2 | Minor updates (likely SDK rename references) |
| agent-sdk/python.md | Modified | +2/-2 | Minor updates (likely package name or import changes) |
| agent-sdk/typescript.md | Modified | +2/-2 | Minor updates (likely package name or import changes) |
| test-and-evaluate/develop-tests.md | Modified | +2/-0 | Minor additions |
| resources/overview.md | Modified | +0/-4 | Removed 4 lines of resource links |

---
*Generated from Claude API documentation changes detected on 2026-03-05*
