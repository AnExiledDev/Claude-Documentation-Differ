# Claude API Documentation Changes — 2026-03-07

## Summary

Two new Agent SDK reference pages were added covering the agent loop lifecycle and Claude Code feature integration. The sessions guide was substantially rewritten with a new decision framework and clearer API patterns for continue/resume/fork. The subagents page gained an explicit "What subagents inherit" section with a structured context table.

## Significant Changes

### Agent SDK

- **New: Agent loop reference page**: Comprehensive new page documenting the full lifecycle of an SDK agent run — turns, message types, tool execution, context window management, automatic compaction, permission modes, effort levels, and result subtypes.
  > "Every agent session follows the same cycle: Receive prompt → Evaluate and respond → Execute tools → Repeat → Return result."
  > "A turn is one round trip inside the loop: Claude produces output that includes tool calls, the SDK executes those tools, and the results feed back to Claude automatically."

  Key specifics documented:
  - Five message types: `SystemMessage`, `AssistantMessage`, `UserMessage`, `StreamEvent`, `ResultMessage`
  - `ResultMessage.subtype` values: `success`, `error_max_turns`, `error_max_budget_usd`, `error_during_execution`, `error_max_structured_output_retries`
  - `stop_reason` field on `ResultMessage` (values: `end_turn`, `max_tokens`, `refusal`)
  - `effort` option (`"low"` / `"medium"` / `"high"` / `"max"`); TypeScript defaults to `"high"`, Python leaves it unset
  - Permission modes: `"default"`, `"acceptEdits"`, `"plan"`, `"dontAsk"` (TypeScript only), `"bypassPermissions"`
  - Read-only tools (`Read`, `Glob`, `Grep`, MCP read-only) run concurrently; state-modifying tools run sequentially
  - `"compact_boundary"` `SystemMessage` subtype emitted on automatic context compaction
  - *Implication*: Developers building production agents now have a single canonical reference for loop internals, termination states, and cost controls.
  - *Source*: [How the agent loop works](https://platform.claude.com/docs/en/agent-sdk/agent-loop.md)

- **New: Claude Code features integration guide**: New page documenting the `settingSources` option (`"project"`, `"user"`, `"local"`) and how it enables CLAUDE.md files, rules, skills, hooks, and permissions from the filesystem.
  > "By default, the SDK loads no filesystem settings. Your agent runs in isolation mode with only what you pass programmatically. To load CLAUDE.md, skills, or filesystem hooks, set `settingSources` to tell the SDK where to look."

  Covers:
  - `"project"` loads from `<cwd>/.claude/` and parent directories; `"user"` loads from `~/.claude/`; `"local"` loads gitignored `CLAUDE.local.md` and `settings.local.json`
  - To match full Claude Code CLI behavior: `["user", "project", "local"]`
  - Filesystem hooks (`settings.json`) vs. programmatic hooks (callbacks in `query()`) — both run in the same lifecycle; filesystem hooks fire in subagents too, programmatic hooks are scoped to the main session only
  - Decision table mapping goals (persistent instructions, on-demand skills, subagents, hooks, MCP, agent teams) to the right SDK surface
  - Auto memory (`~/.claude/projects/*/memory/`) is CLI-only and never loaded by the SDK
  - *Implication*: SDK agents can now be configured to fully share CLAUDE.md, skills, and hook definitions with interactive Claude Code sessions with a single option.
  - *Source*: [Use Claude Code features in the SDK](https://platform.claude.com/docs/en/agent-sdk/claude-code-features.md)

- **Sessions guide rewritten**: The `sessions.md` page was significantly restructured (+249/-169 lines). The previous version focused on low-level mechanics (how to get a session ID from the init `SystemMessage`, `resume`, and `fork`). The new version leads with a decision table mapping application shapes to the right session strategy.

  New structure:
  - **Choose an approach** — decision table covering one-shot tasks, multi-turn in-process chat, resuming after process restart, resuming a specific past session, forking, and stateless (TypeScript `persistSession: false`)
  - **Automatic session management** — `ClaudeSDKClient` (Python) and `continue: true` (TypeScript) documented as the zero-ID-tracking options for multi-turn conversations
  - **Use session options with `query()`** — explicit capture, resume, and fork patterns, each with code examples in both SDKs
  - **Resume across hosts** — guidance on moving `.jsonl` session files and a note about the `listSessions()` TypeScript utility

  Notable new details:
  > "Sessions are stored under `~/.claude/projects/<encoded-cwd>/*.jsonl`, where `<encoded-cwd>` is the absolute working directory with every non-alphanumeric character replaced by `-`."
  > "Forking branches the conversation history, not the filesystem. If a forked agent edits files, those changes are real and visible to any session working in the same directory."

  - *Implication*: The new decision table makes it easier to choose the right pattern. The `ClaudeSDKClient` (Python) and `continue: true` (TypeScript) patterns are now prominently documented as first-class options rather than buried in the reference.
  - *Source*: [Work with sessions](https://platform.claude.com/docs/en/agent-sdk/sessions.md)

- **Subagents: explicit context inheritance table**: The `subagents.md` page replaced the "Context management" section with a new "Context isolation" section and a new "What subagents inherit" section containing a structured table.
  > "A subagent's context window starts fresh (no parent conversation) but isn't empty. The only channel from parent to subagent is the Task prompt string, so include any file paths, error messages, or decisions the subagent needs directly in that prompt."

  The new inheritance table:

  | The subagent receives | The subagent does not receive |
  |:---|:---|
  | Its own system prompt + Task prompt | Parent's conversation history or tool results |
  | Project CLAUDE.md (via `settingSources`) | Skills (unless listed in `AgentDefinition.skills`, TypeScript only) |
  | Tool definitions (inherited or scoped via `tools`) | The parent's system prompt |

  - *Implication*: Clarifies a previously underdocumented boundary — subagents do not inherit parent system prompts or prior conversation turns, only the Task prompt string. Developers building multi-agent pipelines should ensure all required context is passed explicitly in the Task prompt.
  - *Source*: [Subagents in the SDK](https://platform.claude.com/docs/en/agent-sdk/subagents.md)

## New Pages

- **agent-loop.md** — Full reference for the SDK agent loop: message lifecycle, turn structure, message types, tool execution (built-in tools, parallel execution, permission modes), context window, automatic compaction, result subtypes, and hooks. Includes worked examples in Python and TypeScript. [View](https://platform.claude.com/docs/en/agent-sdk/agent-loop.md)
- **claude-code-features.md** — Guide to enabling Claude Code filesystem features in SDK agents via `settingSources`: CLAUDE.md, rules, skills, filesystem hooks, and programmatic hooks. Includes decision table and code examples for both SDKs. [View](https://platform.claude.com/docs/en/agent-sdk/claude-code-features.md)

## Notable Details

- The `agent-loop.md` page documents that `effort` trades latency and token cost for reasoning depth, and is explicitly noted as independent from extended thinking: `effort: "low"` can coexist with extended thinking enabled, and vice versa.
- `"dontAsk"` permission mode is documented as TypeScript-only. `"bypassPermissions"` cannot be used when running as root on Unix.
- The TypeScript SDK's `persistSession: false` option (stateless, in-memory sessions only) is called out in the sessions decision table — Python always persists to disk.
- Custom tool parallel execution: custom tools default to sequential; mark them `readOnly: true` (TypeScript) or `readOnlyHint=True` (Python) in their annotations to enable concurrency.
- The sessions page documents a TypeScript V2 preview (`createSession()` with `send` / `stream` pattern) as unstable; the rest of the documentation continues to use the stable V1 `query()` interface.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| agent-sdk/agent-loop.md | New | +399 | Full agent loop reference: turns, messages, tools, context, results, hooks |
| agent-sdk/claude-code-features.md | New | +275 | Guide to settingSources, CLAUDE.md, skills, and filesystem hooks in SDK |
| agent-sdk/sessions.md | Modified | +249/-169 | Major rewrite: decision table, automatic session management, resume/fork patterns |
| agent-sdk/subagents.md | Modified | +21/-6 | Added "Context isolation" section and "What subagents inherit" table |
| agent-sdk/python.md | Modified | +2/-1 | Minor update |
| agent-sdk/typescript.md | Modified | +2/-2 | Minor update |

---
*Generated from Claude API documentation changes detected on 2026-03-07*
