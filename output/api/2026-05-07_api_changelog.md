# Claude API Documentation Changes — 2026-05-07

## Summary

This update documents a major expansion of the Managed Agents beta API (`managed-agents-2026-04-01`), adding multiagent coordination, session thread management, outcome evaluations, and MCP OAuth credential validation. Across all SDK language variants (Python, TypeScript, Go, Java, Ruby, C#, CLI, REST), 64 new pages were added and 802 existing pages were modified — the vast majority of modifications are propagation of the new beta header and expanded citation field descriptions into existing endpoints.

---

## Significant Changes

### Managed Agents — Multiagent Coordination

- **New `multiagent` parameter on Agent Create/Update**: Agents can now be configured as coordinators that orchestrate a roster of sub-agents. The primary session thread spawns child threads from the roster.
  > `multiagent: optional BetaManagedAgentsMultiagentParams` — A coordinator topology: the session's primary thread orchestrates work by spawning session threads, each running an agent drawn from the `agents` roster.
  > `agents: array` — Agents the coordinator may spawn as session threads. 1–20 entries. Each entry is an agent ID string, a versioned `{"type":"agent","id","version"}` reference, or `{"type":"self"}` to allow recursive self-invocation. Entries must reference distinct agents (after resolving `self` and string forms); at most one `self`. Referenced agents must exist, must not be archived, and must not themselves have `multiagent` set (depth limit 1).
  - *Implication*: Developers can now build hierarchical multi-agent systems where a primary coordinator agent delegates subtasks to specialized sub-agents. The `self` roster entry allows the coordinator to recursively spawn copies of itself. Depth is capped at 1 — roster agents cannot themselves be coordinators.
  - *Source*: [Agents Create (beta)](https://platform.claude.com/docs/en/api/beta/agents/create.md), [Agents Update (beta)](https://platform.claude.com/docs/en/api/beta/agents/update.md), [Beta API Reference](https://platform.claude.com/docs/en/api/beta.md)

- **New domain types for multiagent topology**:
  - `BetaManagedAgentsMultiagentParams` / `BetaManagedAgentsMultiagent` — Request/response representation of the coordinator configuration
  - `BetaManagedAgentsMultiagentCoordinatorParams` / `BetaManagedAgentsMultiagentCoordinator` — Resolved coordinator with concrete agent roster
  - `BetaManagedAgentsMultiagentRosterEntryParams` — Union: string agent ID | versioned agent ref | `{type: "self"}`
  - `BetaManagedAgentsMultiagentSelfParams` — Sentinel entry meaning "the agent that owns this configuration"
  - `BetaManagedAgentsAgentReference` — Concrete resolved `{id, type, version}` reference in API responses
  - `BetaManagedAgentsSessionMultiagentCoordinator` — Coordinator snapshot stored on a session, with full agent definitions for each roster member

### Managed Agents — Session Threads

- **New Session Threads API**: Four new endpoint groups for inspecting and managing threads spawned within a multi-agent session.

  | Method | Endpoint | Description |
  |--------|----------|-------------|
  | `GET` | `/v1/sessions/{session_id}/threads` | List all threads in a session (primary + children in spawn order) |
  | `GET` | `/v1/sessions/{session_id}/threads/{thread_id}` | Retrieve a single thread |
  | `POST` | `/v1/sessions/{session_id}/threads/{thread_id}/archive` | Archive a thread |
  | `GET` | `/v1/sessions/{session_id}/threads/{thread_id}/events` | List events for a specific thread |
  | `GET` | `/v1/sessions/{session_id}/threads/{thread_id}/events/stream` | Stream events for a specific thread |

  > `data: optional array of BetaManagedAgentsSessionThread` — Threads in the session, primary first then children in spawn order.

  Thread objects include:
  - `status`: `"running"` | `"idle"` | `"rescheduling"` | `"terminated"`
  - `stats`: `active_seconds`, `duration_seconds`, `startup_seconds`
  - `usage`: Cumulative token usage with cache breakdown (`ephemeral_1h_input_tokens`, `ephemeral_5m_input_tokens`)
  - `parent_thread_id`: `null` for the primary thread
  - `agent`: Snapshot of the agent definition at thread creation time

  - *Implication*: Developers can now observe the internal execution of multiagent sessions at thread granularity, including per-thread token usage and timing statistics.
  - *Source*: [Session Threads](https://platform.claude.com/docs/en/api/beta/sessions/threads.md), [Thread Events](https://platform.claude.com/docs/en/api/beta/sessions/threads/events.md)

- **New thread lifecycle event types** in the sessions event stream:
  - `session.thread_created` — Emitted when a coordinator spawns a new child thread (`session_thread_id` field carries the `sthr_` ID)
  - `session.thread_status_running`, `session.thread_status_idle`, `session.thread_status_rescheduled`, `session.thread_status_terminated` — Thread-level lifecycle events
  - `agent.thread_message_received`, `agent.thread_message_sent` — Messages exchanged between coordinator and sub-agent threads

- **Thread context compaction event**: New `BetaManagedAgentsAgentThreadContextCompactedEvent` (`agent.thread_context_compacted`) emitted when a thread's context window is compacted.

### Managed Agents — Outcome Evaluations

- **New outcome evaluation system**: Sessions can now track defined outcomes and their automated evaluation state.

  > `outcome_evaluations: array of BetaManagedAgentsOutcomeEvaluationResource` — Evaluation state for a single outcome defined via a `define_outcome` event.

  `BetaManagedAgentsOutcomeEvaluationResource` fields:
  - `outcome_id: string` — Server-generated `outc_` ID
  - `description: string` — What the agent should produce
  - `result: string` — Current state: `pending` → `running` → `evaluating` → `satisfied` | `max_iterations_reached` | `failed` | `interrupted`
  - `iteration: number` — 0-indexed revision cycle
  - `explanation: string` — Grader's verdict text (why criteria were/weren't met)

  New event types for evaluation lifecycle:
  - `span.outcome_evaluation_start` — Emitted when an evaluation cycle begins
  - `span.outcome_evaluation_end` — Carries verdict, explanation, and token usage; `needs_revision` means another cycle follows; other verdicts are terminal
  - `span.outcome_evaluation_ongoing` — Emitted during active evaluation

  - *Implication*: Agents can now be given structured outcome criteria with automated grading. The grader runs iteratively until criteria are met (`satisfied`), the iteration budget is exhausted (`max_iterations_reached`), or evaluation fails (`failed`/`interrupted`).
  - *Source*: [Sessions (beta)](https://platform.claude.com/docs/en/api/beta/sessions.md)

- **New rubric types**: `BetaManagedAgentsFileRubric` / `BetaManagedAgentsFileRubricParams` and `BetaManagedAgentsTextRubric` / `BetaManagedAgentsTextRubricParams` for specifying grading criteria.

- **New `user.define_outcome` event**: Client-side event for defining an outcome that the agent should achieve, sent via the session send-event endpoint.

### Managed Agents — MCP OAuth Credential Validation

- **New `POST /v1/vaults/{vault_id}/credentials/{credential_id}/mcp_oauth_validate` endpoint**: Validates an OAuth credential by live-probing the configured MCP server.

  Returns `BetaManagedAgentsCredentialValidation`:
  - `status: "valid" | "invalid" | "unknown"` — Overall verdict
  - `mcp_probe: BetaManagedAgentsMCPProbe` — Details the failing MCP method (e.g. `initialize` or `tools/list`) with HTTP response body (may be truncated, sensitive values scrubbed)
  - `refresh: BetaManagedAgentsRefreshObject` — Outcome of token refresh attempt: `succeeded` | `failed` | `connect_error` | `no_refresh_token`
  - `has_refresh_token: boolean`
  - `validated_at: string` — RFC 3339 timestamp

  Example:
  ```http
  curl https://api.anthropic.com/v1/vaults/$VAULT_ID/credentials/$CREDENTIAL_ID/mcp_oauth_validate \
      -X POST \
      -H 'anthropic-version: 2023-06-01' \
      -H 'anthropic-beta: managed-agents-2026-04-01' \
      -H "X-Api-Key: $ANTHROPIC_API_KEY"
  ```

  - *Implication*: Developers can now programmatically validate that stored MCP OAuth credentials are functional before using them in sessions, with diagnostic information about what step failed.
  - *Source*: [Vaults Credentials MCP OAuth Validate](https://platform.claude.com/docs/en/api/beta/vaults/credentials/mcp_oauth_validate.md)

### Beta Header — `managed-agents-2026-04-01`

- **New beta flag added to `AnthropicBeta` union**: `"managed-agents-2026-04-01"` is now a recognized value for the `anthropic-beta` header, increasing the named beta count from 20 to 21 across all endpoints.
  > Added: `"managed-agents-2026-04-01"`
  - *Implication*: All Managed Agents API features (sessions, agents, threads, vaults, memory stores, skills, user profiles) require this header. It replaces or extends any prior ad-hoc managed-agents header.
  - *Source*: [Beta Domain Types](https://platform.claude.com/docs/en/api/beta.md)

### Sessions — Expanded Event System

The Sessions API (`/v1/sessions`) received a large restructuring of its event taxonomy. Key new event types beyond those mentioned above:

- **Agent events**: `agent.custom_tool_use`, `agent.mcp_tool_result`, `agent.mcp_tool_use`, `agent.message`, `agent.thinking`
- **Session lifecycle events**: `session.deleted`, `session.error`, `session.requires_action`, `session.retries_exhausted`, `session.status_idle`, `session.status_rescheduled`, `session.status_running`, `session.status_terminated`
- **Span events**: `span.model_request_start`, `span.model_request_end` (with `BetaManagedAgentsSpanModelUsage`)
- **User events**: `user.interrupt`, `user.tool_confirmation`, `user.custom_tool_result`, `user.define_outcome`
- **Retry status types**: `BetaManagedAgentsRetryStatusRetrying`, `BetaManagedAgentsRetryStatusExhausted`, `BetaManagedAgentsRetryStatusTerminal`
- **Error types**: `BetaManagedAgentsMCPAuthenticationFailedError`, `BetaManagedAgentsMCPConnectionFailedError`, `BetaManagedAgentsModelOverloadedError`, `BetaManagedAgentsModelRateLimitedError`, `BetaManagedAgentsModelRequestFailedError`

The `user.interrupt` event now clarifies routing: when `session_thread_id` is absent, the interrupt targets every non-archived thread in a multiagent session; when present, it targets only that thread.

- *Source*: [Sessions Events](https://platform.claude.com/docs/en/api/beta/sessions/events.md), [Sessions (beta)](https://platform.claude.com/docs/en/api/beta/sessions.md)

### New Models in Managed Agents

A new model identifier is now documented in the Managed Agents model list:

- `"claude-opus-4-7"` — "Frontier intelligence for long-running agents and coding"

Previously documented models remain: `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5`, `claude-opus-4-5`, `claude-sonnet-4-5`.

- *Source*: [Sessions (beta)](https://platform.claude.com/docs/en/api/beta/sessions.md), [Session Threads](https://platform.claude.com/docs/en/api/beta/sessions/threads.md)

### Messages API — Citation Field Descriptions

Documentation for citation location fields was expanded with precise semantic definitions across all Messages endpoints (beta and non-beta, all SDK languages):

- **`cited_text`**: 
  > The full text of the cited block range, concatenated. Always equals the contents of `content[start_block_index:end_block_index]` joined together. The text block is the minimal citable unit; this field is never a substring of a single block. Not counted toward output tokens, and not counted toward input tokens when sent back in subsequent turns.

- **`start_block_index`**: 
  > 0-based index of the first cited block in the source's `content` array.

- **`end_block_index`**: 
  > Exclusive 0-based end index of the cited block range in the source's `content` array. Always greater than `start_block_index`; a single-block citation has `end_block_index = start_block_index + 1`.

- **`search_result_index`**:
  > 0-based index of the cited search result among all `search_result` content blocks in the request, in the order they appear across messages and tool results. Counted separately from `document_index`; server-side web search results are not included in this count.

  - *Implication*: No API behavior change — these are documentation clarifications for fields that already existed. The `cited_text` note confirms it does not consume tokens when echoed back, which is useful for cost management.
  - *Source*: [Beta Messages](https://platform.claude.com/docs/en/api/beta/messages.md), [Beta Messages Create](https://platform.claude.com/docs/en/api/beta/messages/create.md)

---

## New Pages

All new pages are SDK-mirrored variants of the same two API surfaces, published for: REST (beta), Python, TypeScript, Go, Java, Ruby, C#, and CLI — 8 SDK variants × 8 pages = 64 pages total.

**Session Threads (8 endpoints × 8 SDK variants):**
- **`en_api_beta_sessions_threads.md`** — Session threads overview: List (`GET /v1/sessions/{session_id}/threads`) and Retrieve (`GET /v1/sessions/{session_id}/threads/{thread_id}`) [View](https://platform.claude.com/docs/en/api/beta/sessions/threads.md)
- **`en_api_beta_sessions_threads_archive.md`** — Archive a session thread (`POST /v1/sessions/{session_id}/threads/{thread_id}/archive`) [View](https://platform.claude.com/docs/en/api/beta/sessions/threads/archive.md)
- **`en_api_beta_sessions_threads_events.md`** — Thread event operations overview [View](https://platform.claude.com/docs/en/api/beta/sessions/threads/events.md)
- **`en_api_beta_sessions_threads_events_list.md`** — List thread events (`GET /v1/sessions/{session_id}/threads/{thread_id}/events`) [View](https://platform.claude.com/docs/en/api/beta/sessions/threads/events/list.md)
- **`en_api_beta_sessions_threads_events_stream.md`** — Stream thread events (`GET /v1/sessions/{session_id}/threads/{thread_id}/events/stream`) [View](https://platform.claude.com/docs/en/api/beta/sessions/threads/events/stream.md)
- **`en_api_beta_sessions_threads_list.md`** — List session threads [View](https://platform.claude.com/docs/en/api/beta/sessions/threads/list.md)
- **`en_api_beta_sessions_threads_retrieve.md`** — Retrieve a single thread [View](https://platform.claude.com/docs/en/api/beta/sessions/threads/retrieve.md)

**Vault Credential Validation (1 endpoint × 8 SDK variants):**
- **`en_api_beta_vaults_credentials_mcp_oauth_validate.md`** — Validate MCP OAuth credential (`POST /v1/vaults/{vault_id}/credentials/{credential_id}/mcp_oauth_validate`) [View](https://platform.claude.com/docs/en/api/beta/vaults/credentials/mcp_oauth_validate.md)

---

## Notable Details

- **`BetaManagedAgentsAgent` response object grows from 11 to 12 fields**: The new `multiagent` field is the addition. Similarly, `BetaManagedAgentsSession` grows from 11 to 12 fields with the new `outcome_evaluations` array.

- **Tool permission policy model is now documented**: The `BetaManagedAgentsAlwaysAllowPolicy` (`"always_allow"`) and `BetaManagedAgentsAlwaysAskPolicy` (`"always_ask"`) types are now visible in thread agent snapshots, clarifying how tools behave without user confirmation.

- **`speed` field on model config**: The `BetaManagedAgentsModelConfig.speed` field (`"standard"` | `"fast"`) appears in agent, session, and thread responses. The docs state: "Not all models support `fast`; invalid combinations are rejected at create time."

- **`user.interrupt` routing behavior** clarified in event docs: absent `session_thread_id` interrupts all active threads; present value routes to a specific thread.

- **Outcome evaluation budget**: `max_iterations_reached` is a terminal state where "one final acknowledgment turn follows before the session goes idle, but no further evaluation runs" — important for understanding when a session will eventually idle after a failed evaluation loop.

- **`search_result_index` counting rule**: Server-side web search results are explicitly excluded from `search_result_index` counting. Only client-supplied `search_result` content blocks count.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/api/beta/sessions.md` | Modified | +20474 / -5542 | Major expansion: events, resources, threads, multiagent, outcome evaluations |
| `docs/api/en/api/beta.md` | Modified | +18967 / -1037 | Added managed-agents types, thread types, credential validation types |
| `docs/api/en/api/beta/messages.md` | Modified | +2088 / -8 | Citation field descriptions; managed-agents beta header |
| `docs/api/en/api/beta/sessions/events/list.md` or similar | Modified | Large | New event taxonomy, interrupt routing docs |
| `docs/api/en/api/beta/messages/create.md` | Modified | +267 / -1 | Citation field descriptions; managed-agents beta header |
| `docs/api/en/api/beta/messages/count_tokens.md` | Modified | +219 / -1 | Citation field descriptions; managed-agents beta header |
| `docs/api/en/api/beta/messages/batches/create.md` | Modified | +219 / -1 | Citation field descriptions; managed-agents beta header |
| `docs/api/en/api/beta/agents.md` | Modified | +345 / -13 | New multiagent types: Coordinator, CoordinatorParams, SelfParams, AgentReference |
| `docs/api/en/api/beta/agents/create.md` | Modified | +72 / -3 | Added `multiagent` body parameter; managed-agents beta header |
| `docs/api/en/api/beta/agents/update.md` | Modified | +72 / -3 | Added `multiagent` body parameter; managed-agents beta header |
| `docs/api/en/api/beta/messages/batches/results.md` | Modified | +51 / -1 | Citation field descriptions |
| `docs/api/en/api/beta/memory_stores.md` | Modified | +42 / -14 | Managed-agents beta header propagation |
| `docs/api/en/api/beta/sessions/threads.md` | New | — | Session threads list/retrieve |
| `docs/api/en/api/beta/sessions/threads/archive.md` | New | — | Archive session thread |
| `docs/api/en/api/beta/sessions/threads/events.md` | New | — | Thread events overview |
| `docs/api/en/api/beta/sessions/threads/events/list.md` | New | — | List thread events |
| `docs/api/en/api/beta/sessions/threads/events/stream.md` | New | — | Stream thread events |
| `docs/api/en/api/beta/sessions/threads/list.md` | New | — | List all threads in a session |
| `docs/api/en/api/beta/sessions/threads/retrieve.md` | New | — | Retrieve a single thread |
| `docs/api/en/api/beta/vaults/credentials/mcp_oauth_validate.md` | New | — | MCP OAuth credential validation |
| *(SDK variants)* | New / Modified | — | All 7 SDK variants (Python, TypeScript, Go, Java, Ruby, C#, CLI) received equivalent new/updated pages |

---

*Generated from Claude API documentation changes detected on 2026-05-07*
