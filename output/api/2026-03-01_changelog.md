# Claude API Documentation Changes — 2026-03-01

## Summary

The largest update is a significant restructuring and expansion of the Agent SDK hooks documentation, covering how hooks work, callback function inputs and outputs, asynchronous hook output, and a new examples section. The TypeScript SDK reference adds a new `AgentInfo` type and a `supportedAgents()` method to the `Query` object. The Zero Data Retention page clarifies that Claude Code ZDR eligibility now extends to Claude for Enterprise in addition to direct API key use.

## Significant Changes

### Agent SDK — Hooks

- **Hooks page restructured with step-by-step execution model**: The introductory description was rewritten to define hooks as "callback functions that run your code in response to agent events." A new `## How hooks work` section replaces the old prose with an explicit five-step flow (event fires → SDK collects hooks → matchers filter → callback executes → callback returns decision).
  > "Something happens during agent execution and the SDK fires an event: a tool is about to be called (PreToolUse), a tool returned a result (PostToolUse), a subagent started or stopped, the agent is idle, or execution finished."
  - *Implication*: Developers new to hooks now have a clearer mental model before reading configuration details.
  - *Source*: [hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md)

- **Available hooks table expanded — several hooks promoted to Python SDK support**: Three hooks previously marked as TypeScript-only are now listed as supported in both SDKs: `PostToolUseFailure`, `SubagentStart`, and `PermissionRequest`. The `Notification` hook is also now marked as available in Python (previously TypeScript-only). Six new TypeScript-only hook events are added to the table: `Setup`, `TeammateIdle`, `TaskCompleted`, `ConfigChange`, `WorktreeCreate`, and `WorktreeRemove`.
  > | `PostToolUseFailure` | Yes | Yes | Tool execution failure | Handle or log tool errors |
  > | `SubagentStart` | Yes | Yes | Subagent initialization | Track parallel task spawning |
  > | `PermissionRequest` | Yes | Yes | Permission dialog would be displayed | Custom permission handling |
  > | `Notification` | Yes | Yes | Agent status messages | Send agent status updates to Slack or PagerDuty |
  - *Implication*: Python SDK users can now handle tool failures, subagent starts, permission requests, and notifications without switching to TypeScript.
  - *Source*: [hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md)

- **Python SDK examples updated to `ClaudeSDKClient` client pattern**: All Python code samples now use the `async with ClaudeSDKClient(options=options) as client:` pattern with `client.query()` and `client.receive_response()` instead of directly calling the `query()` generator function.
  > ```python
  > async with ClaudeSDKClient(options=options) as client:
  >     await client.query("Update the database configuration")
  >     async for message in client.receive_response():
  >         if isinstance(message, (AssistantMessage, ResultMessage)):
  >             print(message)
  > ```
  - *Implication*: Existing Python SDK hook examples using `async for message in query(...)` need to be updated to the client pattern.
  - *Source*: [hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md)

- **Callback inputs and outputs reorganized into structured subsections**: The old `### Callback function inputs`, `### Input data`, and `### Callback outputs` sections are replaced by `### Callback functions` with `#### Inputs`, `#### Outputs`, and `#### Asynchronous output` subsections. The output description now clearly distinguishes top-level fields (`systemMessage`, `continue`) from `hookSpecificOutput` fields.
  > "Your callback returns an object with two categories of fields: Top-level fields control the conversation: systemMessage injects a message into the conversation visible to the model, and continue (continue_ in Python) determines whether the agent keeps running after this hook. hookSpecificOutput controls the current operation."
  - *Implication*: The hook return value structure is more clearly explained, reducing confusion about which fields go where.
  - *Source*: [hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md)

- **New section: Asynchronous hook output**: A new `#### Asynchronous output` subsection documents how to return `{"async_": True, "asyncTimeout": 30000}` (Python) or `{ async: true, asyncTimeout: 30000 }` (TypeScript) to let the agent proceed without waiting for the hook to complete.
  > "By default, the agent waits for your hook to return before proceeding. If your hook performs a side effect (logging, sending a webhook) and doesn't need to influence the agent's behavior, you can return an async output instead."
  > | `async` | `true` | Signals async mode. The agent proceeds without waiting. In Python, use `async_` to avoid the reserved keyword. |
  - *Implication*: Logging and notification hooks can now be marked non-blocking, reducing latency introduced by side-effect-only hooks.
  - *Source*: [hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md)

- **"Common use cases" tabs section removed; replaced by concrete examples section**: The old `## Common use cases` tab-based overview (Security, Logging, Tool interception, Authorization) is removed. A new `## Examples` section replaces it with full, runnable code samples for each pattern.
  - *Implication*: Developers get working code instead of a bulleted summary of categories.
  - *Source*: [hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md)

- **"Auto-approve specific tools" example removes `LS` from read-only tools list**: The example callback `auto_approve_read_only` previously auto-approved `["Read", "Glob", "Grep", "LS"]`; `"LS"` is removed from both the Python and TypeScript examples.
  > ```python
  > read_only_tools = ["Read", "Glob", "Grep"]
  > ```
  - *Implication*: Code copied from previous docs that auto-approved `LS` should be reviewed; `LS` may now require an explicit permission decision.
  - *Source*: [hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md)

- **Python `Make HTTP requests from hooks` example updated to use `urllib` instead of `aiohttp`**: The webhook example no longer imports `aiohttp`; it uses `urllib.request` run via `asyncio.to_thread()` to avoid blocking the event loop.
  > ```python
  > # Run the blocking HTTP call in a thread to avoid blocking the event loop
  > await asyncio.to_thread(_send_webhook, input_data["tool_name"])
  > ```
  - *Implication*: Removes a dependency on `aiohttp` in the documented pattern; code using the old `aiohttp` approach will still work but differs from the documented example.
  - *Source*: [hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md)

- **"Sending notifications (TypeScript only)" renamed and expanded to include a Python example**: The section is now titled `### Forward notifications to Slack` and includes a full Python implementation. Notification types (`permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`) are explicitly listed in the prose.
  > "Notifications fire for specific event types: permission_prompt (Claude needs permission), idle_prompt (Claude is waiting for input), auth_success (authentication completed), and elicitation_dialog (Claude is prompting the user)."
  - *Implication*: Python SDK users can now implement Slack notification forwarding without porting from a TypeScript example.
  - *Source*: [hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md)

- **"Session hooks not available" troubleshooting section expanded with workarounds**: The section is renamed `### Session hooks not available in Python` and now explains that `SessionStart`/`SessionEnd` can be used as shell command hooks loaded via `setting_sources`, and offers an alternative approach (use the first message from `client.receive_response()` as a trigger).
  > "`SessionStart` and `SessionEnd` can be registered as SDK callback hooks in TypeScript, but are not available in the Python SDK... To run initialization logic as a Python SDK callback instead, use the first message from `client.receive_response()` as your trigger."
  - *Source*: [hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md)

- **Matcher documentation clarified to cover non-tool events**: The description of the `matcher` field now states it matches against "the event's filter field" rather than only tool names, and links to the Claude Code hooks reference for the full list of matcher values per event type.
  > "The matcher field is a regex string that matches against a different value depending on the hook event type. For example, tool-based hooks match against the tool name, while Notification hooks match against the notification type."
  - *Source*: [hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md)

- **Permission decision priority documented inline**: The old separate `#### Permission decision flow` section (with four numbered rules) is removed and replaced with a `<Note>` block embedded in the Outputs section.
  > "When multiple hooks or permission rules apply, deny takes priority over ask, which takes priority over allow. If any hook returns deny, the operation is blocked regardless of other hooks."
  - *Source*: [hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md)

- **`## Learn more` renamed `## Related resources` with updated links**: The footer now links to the Claude Code hooks reference and hooks guide in addition to the SDK references and permissions/custom-tools pages.
  - *Source*: [hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md)

### Agent SDK — TypeScript Reference

- **New `AgentInfo` type added**: A new `### AgentInfo` section documents a type describing available subagents.
  > ```typescript
  > type AgentInfo = {
  >   name: string;
  >   description: string;
  >   model?: string;
  > }
  > ```
  > | `name` | `string` | Agent type identifier (e.g., `"Explore"`, `"general-purpose"`) |
  > | `description` | `string` | Description of when to use this agent |
  > | `model` | `string \| undefined` | Model alias this agent uses. If omitted, inherits the parent's model |
  - *Implication*: Callers can now programmatically inspect available subagents.
  - *Source*: [typescript.md](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

- **`Query` object gains `supportedAgents()` method**: The `Query` interface now includes `supportedAgents(): Promise<AgentInfo[]>`, and `SDKControlInitializeResponse` now includes an `agents: AgentInfo[]` field.
  > | `supportedAgents()` | Returns available subagents |
  - *Implication*: Applications can call `supportedAgents()` to enumerate available agent types at runtime.
  - *Source*: [typescript.md](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

- **`### Query` section renamed to `### Query object`**: The section anchor changed from `#query` to `#query-object`; existing deep links using the old anchor will break.
  - *Implication*: Any bookmarks or documentation that linked to `#query` will need to be updated to `#query-object`.
  - *Source*: [typescript.md](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

- **Widespread TypeScript type definition formatting fix**: Closing braces on type definitions throughout the reference changed from `}` to `};` (adding a semicolon) across dozens of types (`BaseHookInput`, `PreToolUseHookInput`, `BashInput`, `FileReadInput`, `ModelInfo`, `SlashCommand`, etc.). This is a formatting/style normalization with no semantic change to the types themselves.
  - *Source*: [typescript.md](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

- **`tool_input` access pattern updated to cast through `Record<string, unknown>`**: TypeScript examples that previously accessed `preInput.tool_input?.file_path` now cast `tool_input` to `Record<string, unknown>` first, reflecting that `tool_input` is typed as `unknown` in the SDK.
  > ```typescript
  > const toolInput = preInput.tool_input as Record<string, unknown>;
  > const filePath = toolInput?.file_path as string;
  > ```
  - *Implication*: TypeScript code accessing `tool_input` fields directly (without casting) will produce type errors; the cast to `Record<string, unknown>` is now the documented pattern.
  - *Source*: [typescript.md](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

### Agent SDK — Python Reference

- **`HookCallback` parameter doc cross-reference updated**: The description of the `input` parameter now links to `[HookInput](#hook-input)` instead of the old `[Hook input types](#pretoolusehookinput)` anchor.
  - *Source*: [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md)

- **`HookSpecificOutput` cross-reference anchor corrected**: The link in the `HookSpecificOutput` section now points to `hooks#outputs` instead of the old `hooks#callback-outputs`.
  - *Source*: [python.md](https://platform.claude.com/docs/en/agent-sdk/python.md)

### Agent SDK — Skills

- **`settingSources`/`setting_sources` reference anchor corrected**: The cross-reference link in the skills page now points to `#setting-source` instead of the previous `#settingsource`.
  - *Source*: [skills.md](https://platform.claude.com/docs/en/agent-sdk/skills.md)

### Build with Claude — Zero Data Retention

- **Claude Code ZDR eligibility expanded to include Claude for Enterprise**: The page previously stated Claude Code ZDR was only available via pay-as-you-go API keys ("not eligible" for OAuth/Claude for Enterprise). This is now expanded to a two-path eligibility model.
  > "Claude Code is eligible for ZDR through two paths:
  > - API keys: Claude Code used with pay-as-you-go API keys from a Commercial organization
  > - Claude for Enterprise: Claude Code used through Claude for Enterprise with ZDR enabled on the organization"
  > "ZDR is enabled on a per-organization basis. Each new organization requires ZDR to be enabled separately by your account team. ZDR does not automatically apply to new organizations created under the same account."
  - *Implication*: Enterprise customers using Claude for Enterprise can now qualify for ZDR for Claude Code, provided ZDR is enabled on their organization by the account team.
  - *Source*: [zero-data-retention.md](https://platform.claude.com/docs/en/build-with-claude/zero-data-retention.md)

- **"What ZDR covers" bullet for Claude Code updated with a link**: The bullet now reads "ZDR applies when used with enterprise API credentials or through Claude for Enterprise" and includes a direct link to the Claude Code ZDR docs at `https://code.claude.com/docs/en/zero-data-retention`.
  - *Source*: [zero-data-retention.md](https://platform.claude.com/docs/en/build-with-claude/zero-data-retention.md)

- **New FAQ answer directs readers to Claude Code ZDR documentation**: A new paragraph at the end of the "Is Claude Code eligible for ZDR?" FAQ links to the Claude Code ZDR documentation for details on disabled features and how to request enablement.
  - *Source*: [zero-data-retention.md](https://platform.claude.com/docs/en/build-with-claude/zero-data-retention.md)

### Build with Claude — Prompt Caching

- **JSON formatting in code examples normalized**: `cache_control` object examples changed from inline `{"type": "ephemeral"}` to `{ "type": "ephemeral" }` (spaces added). The combined caching example's `"messages"` field changed from `[...]` to a concrete example `[{ "role": "user", "content": "What are the key terms?" }]`.
  - *Implication*: No functional change; the concrete messages example is more useful than the placeholder.
  - *Source*: [prompt-caching.md](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

### Build with Claude — Structured Outputs

- **Java annotation summary and Ruby SDK feature list formatting normalized**: Annotation list items changed from `--` delimiters to `:` delimiters (`@JsonClassDescription -- Add a description` → `@JsonClassDescription: Add a description`). Similarly for Ruby SDK feature bullets.
  - *Implication*: Purely cosmetic; no content change.
  - *Source*: [structured-outputs.md](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

## Migration Guidance

**Python SDK hook code using the `query()` generator directly**: All Python examples in the hooks page have been updated to use `ClaudeSDKClient` as a context manager. If your code uses the old pattern:

```python
async for message in query(prompt="...", options=ClaudeAgentOptions(hooks={...})):
    print(message)
```

The documented pattern is now:

```python
options = ClaudeAgentOptions(hooks={...})
async with ClaudeSDKClient(options=options) as client:
    await client.query("...")
    async for message in client.receive_response():
        if isinstance(message, (AssistantMessage, ResultMessage)):
            print(message)
```

**TypeScript `tool_input` access**: If your hook code accesses `tool_input` fields directly without casting, add an intermediate cast to `Record<string, unknown>`:

```typescript
// Old pattern (will produce type errors)
const filePath = preInput.tool_input?.file_path as string;

// New pattern
const toolInput = preInput.tool_input as Record<string, unknown>;
const filePath = toolInput?.file_path as string;
```

**TypeScript SDK anchor change for `Query`**: The `#query` anchor in the TypeScript reference is now `#query-object`. Update any links that referenced the old anchor.

**Claude Code ZDR for Claude for Enterprise**: ZDR eligibility for Claude Code through Claude for Enterprise is not automatic. It must be enabled per-organization by your account team. Contact your account team to enable it.

## Notable Details

- The `"LS"` tool name was removed from the auto-approve read-only tools example in the hooks documentation. If you copied this pattern, verify whether `LS` should remain in your approved list.
- The hooks page now explicitly states that async outputs cannot block or modify operations: "Async outputs cannot block, modify, or inject context into the operation since the agent has already moved on."
- The `hookEventName` field in `hookSpecificOutput` is now shown in an example using a hardcoded string literal (`"PreToolUse"`) rather than `input.hook_event_name`, which matches the troubleshooting tip about fixing incorrect `hookEventName` values.
- The `SubagentStop` hook example now logs `agent_id` and `agent_transcript_path`, fields that were not used in the previous version of the example.
- The `parent_tool_use_id` field mentioned in the old troubleshooting tip for "Subagent permission prompts multiplying" is removed; the guidance now recommends using "a shared variable or session state" instead.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| [agent-sdk/hooks.md](https://platform.claude.com/docs/en/agent-sdk/hooks.md) | Modified | +333 / -342 | Major restructure: new step-by-step execution model, expanded hooks table (Python now supports PostToolUseFailure, SubagentStart, PermissionRequest, Notification), async output section, new examples section, updated Python to ClaudeSDKClient pattern |
| [agent-sdk/typescript.md](https://platform.claude.com/docs/en/agent-sdk/typescript.md) | Modified | +168 / -124 | New `AgentInfo` type and `supportedAgents()` method; `Query` section renamed to `Query object`; widespread semicolon normalization on type closing braces |
| [build-with-claude/zero-data-retention.md](https://platform.claude.com/docs/en/build-with-claude/zero-data-retention.md) | Modified | +9 / -5 | Claude Code ZDR now eligible via Claude for Enterprise; per-org activation note added; new FAQ link to Claude Code ZDR docs |
| [agent-sdk/python.md](https://platform.claude.com/docs/en/agent-sdk/python.md) | Modified | +5 / -3 | Corrected cross-reference anchors for `HookCallback` and `HookSpecificOutput` |
| [build-with-claude/prompt-caching.md](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md) | Modified | +4 / -4 | JSON formatting normalization; placeholder `[...]` replaced with concrete messages example |
| [build-with-claude/structured-outputs.md](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md) | Modified | +12 / -12 | Java annotation and Ruby SDK feature list delimiter style change (`--` → `:`) |
| [agent-sdk/skills.md](https://platform.claude.com/docs/en/agent-sdk/skills.md) | Modified | +1 / -1 | Cross-reference anchor fix: `#settingsource` → `#setting-source` |
| [build-with-claude/prompt-engineering/prompting-tools.md](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools.md) | Modified | +1 / -1 | Code block language tag added (```` ``` ```` → ```` ```text ````) |
