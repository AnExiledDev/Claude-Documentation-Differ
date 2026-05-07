# Claude API Documentation Changes — 2026-05-07

## Summary

Two new pages document the **Dreams** memory-curation feature and **Webhooks** for event-driven session monitoring. Five existing Managed Agents pages received substantive updates: Outcomes graduated out of Research Preview (dropping the extra beta header), the multi-agent threading model was reorganized with new interrupt/archive patterns, and vaults gained credential-refresh observability including an OAuth diagnostic endpoint.

---

## Significant Changes

### Dreams — New Asynchronous Memory Curation API

- **New `/v1/dreams` endpoint**: A dream reads an existing memory store plus up to 100 past session transcripts and produces a reorganized output memory store. Duplicates are merged, stale entries replaced, and new insights surfaced. The input store is never modified.
  > "Dreams let Claude clean that up. A dream reads an existing memory store alongside past session transcripts, then produces a new, reorganized memory store: duplicates merged, stale or contradicted entries replaced with the latest value, and new insights surfaced."
  - *Implication*: Developers building long-running agents with memory stores now have an API-managed garbage-collection path instead of managing memory cleanup themselves.
  - *Source*: [Dreams](https://platform.claude.com/docs/en/managed-agents/dreams.md)

- **Requires `dreaming-2026-04-21` beta header** (in addition to `managed-agents-2026-04-01`). SDKs set both automatically.
  > "Dreams additionally require the `dreaming-2026-04-21` beta header."

- **Dream resource lifecycle**: Status progresses through `pending` → `running` → `completed` / `failed` / `canceled`. Once `running`, the `session_id` field on the dream points to the underlying session executing the pipeline, which can be streamed in real time.

- **Model support**: During research preview, `claude-opus-4-7` and `claude-sonnet-4-6` are supported as the dream model.

- **Operations**: Create (`POST /v1/dreams`), retrieve, cancel, archive, and list dreams. Cancel is idempotent for already-canceled dreams; archive is supported only on terminal-state dreams.

- **SDK coverage**: bash/curl, CLI (`ant`), Python, TypeScript, C#, Go, Java, PHP, Ruby.

---

### Webhooks — New Event-Subscription Page

- **New webhooks documentation** covering session and vault state-change notifications without polling.
  > "Sessions are long-running interactions. While most real-time interactions happen through the SSE event stream, webhooks notify you of major state changes."
  - *Implication*: Developers can eliminate polling loops for session idle/terminate events by subscribing to webhooks instead.
  - *Source*: [Subscribe to webhooks](https://platform.claude.com/docs/en/managed-agents/webhooks.md)

- **Supported session event types**: `session.status_run_started`, `session.status_idled`, `session.status_rescheduled`, `session.status_terminated`, `session.thread_created`, `session.thread_idled`, `session.thread_terminated`, `session.outcome_evaluation_ended`.

- **Supported vault event types**: `vault.created`, `vault.archived`, `vault.deleted`, `vault_credential.created`, `vault_credential.archived`, `vault_credential.deleted`, `vault_credential.refresh_failed`.

- **Signature verification** via `X-Webhook-Signature` header; SDKs expose `client.beta.webhooks.unwrap()` to verify and parse in one step. The `ANTHROPIC_WEBHOOK_SIGNING_KEY` env var holds the `whsec_`-prefixed secret.

- **Delivery behavior**: Retries at least once with the same `event.id`; ordering is not guaranteed; endpoints that return 3xx or 20+ consecutive failures are auto-disabled.

- **Payload pattern**: Webhook events carry `type`, `id`, and `created_at` plus a minimal `data` object (type + IDs only). Callers must fetch the full resource separately to avoid stale-data issues on retries.

- **SDK coverage**: Python, TypeScript, C#, Go, Java, PHP, Ruby.

---

### Outcomes — Graduated from Research Preview

- **Research Preview tip removed** and beta header simplified. The `managed-agents-2026-04-01-research-preview` header is no longer required; outcomes now use the standard `managed-agents-2026-04-01` header.
  > Before: `"All Managed Agents API requests require the managed-agents-2026-04-01 beta header. Research preview features additionally require managed-agents-2026-04-01-research-preview."`
  > After: `"All Managed Agents API requests require the managed-agents-2026-04-01 beta header. The SDK sets this beta header automatically."`
  - *Implication*: **Breaking change for existing callers** using the research-preview header — any code hardcoding `managed-agents-2026-04-01-research-preview` will need to be updated to the standard header.
  - *Source*: [Define outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes.md)

- **File download method renamed** in the output-file retrieval examples: previously documented as `# Download by file_id`; now `# Download a file` with an updated pattern using `client.beta.files.download()` returning a writable stream rather than a raw response. Additionally, the file listing now uses `scope_id=session.id` without requiring the `files-api-2025-04-14` beta header in this context.

---

### Multi-Agent — Threading Model Reorganized

- **API path updated for thread event streaming**: `sessions.threads.stream()` → `sessions.threads.events.stream()`. This affects all SDKs.
  - *Source*: [Multiagent sessions](https://platform.claude.com/docs/en/managed-agents/multi-agent.md)

- **Event type renamed**: `session.thread_idle` → `session.thread_status_idle` (aligns with the session-level pattern `session.status_idle`). Code checking for this event type must be updated.
  > Before: `case "session.thread_idle": break`
  > After: `case "session.thread_status_idle": break`

- **Thread interrupt now accepts `session_thread_id`**: To interrupt a specific sub-agent thread rather than the primary thread, pass `session_thread_id` on the `user.interrupt` event. Omitting it targets the primary thread (unchanged behavior).
  ```json
  {"type": "user.interrupt", "session_thread_id": "<thread_id>"}
  ```

- **Thread archiving added**: A thread can be interrupted then archived via `POST /v1/sessions/:id/threads/:thread_id/archive`. SDKs expose `sessions.threads.archive()`. Archived threads persist their transcript.

- **Multiagent configuration section renamed**: "Declare callable agents" → "Configure the coordinator". The agent roster now explicitly documents `{"type": "self"}` as a valid entry allowing the coordinator to spawn copies of itself.

- **"Multiagent event types" table removed**: The separate event-type table was replaced by inline documentation within the Threads section and the events-and-streaming reference.

- **Concurrency limits documented**: Maximum 25 concurrent threads per session; maximum 20 unique agents in `multiagent.agents`, but each agent can be called multiple times.

- **Primary thread clarified**: The session-level event stream (`/v1/sessions/:id/events/stream`) is the primary thread. Non-coordinator agent activity is condensed there; full activity is available per-thread.

---

### Vaults — Credential Refresh and OAuth Diagnostics

- **New `## Credential refresh` section**: Credentials are re-resolved periodically during a session and during the vault lifecycle, ensuring credential rotation, archival, or deletion propagates to running sessions without a restart.
  - *Source*: [Authenticate with vaults](https://platform.claude.com/docs/en/managed-agents/vaults.md)

- **`vault_credential.refresh_failed` webhook event**: Emitted when an `mcp_oauth` credential cannot be refreshed (invalid refresh token or irrecoverable OAuth server error). Now documented in vaults with a link to the webhooks page.

- **New OAuth diagnostic endpoint** (`/mcp_oauth_validate`): Enables callers to determine why an OAuth refresh failed and what remediation to apply. The response includes `status`, `has_refresh_token`, `mcp_probe` (MCP server connectivity check), and `refresh.status` (e.g. `no_refresh_token`, `expired`).
  > "To diagnose why a refresh failed, use the `/mcp_oauth_validate` endpoint. This enables you to determine how to handle the failure, which is distinct by error type."

---

### Events and Streaming — Interrupt-and-Redirect Workflow

- **New combined interrupt + redirect pattern**: Documentation now explicitly shows sending `user.interrupt` and `user.message` in the same `events[]` array in a single API call to atomically stop the agent and redirect it.
  - *Source*: [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming.md)

- **Streaming section reorganized**: The bash streaming example now shows the correct race-condition-safe pattern (open stream before sending message). SDK examples were reorganized to match.

---

## New Pages

- **[dreams.md](https://platform.claude.com/docs/en/managed-agents/dreams.md)** — Documents the Dreams API (`/v1/dreams`): create asynchronous memory-curation jobs that read memory stores and session transcripts to produce reorganized output stores. Research Preview; requires `dreaming-2026-04-21` beta header.

- **[webhooks.md](https://platform.claude.com/docs/en/managed-agents/webhooks.md)** — Documents webhook registration, signature verification, supported event types (session and vault), delivery behavior, and auto-disable policy for failing endpoints.

---

## Migration Guidance

### Outcomes: Remove Research Preview Header

```python
# Before
client = anthropic.Anthropic(
    default_headers={"anthropic-beta": "managed-agents-2026-04-01-research-preview"}
)

# After
client = anthropic.Anthropic(
    default_headers={"anthropic-beta": "managed-agents-2026-04-01"}
)
# Or rely on SDK automatic header injection
```

### Multi-Agent: Rename Thread Streaming Call

```python
# Before
with client.beta.sessions.threads.stream(thread.id, session_id=session.id) as stream:
    ...

# After
with client.beta.sessions.threads.events.stream(thread.id, session_id=session.id) as stream:
    ...
```

### Multi-Agent: Update `session.thread_idle` Event Check

```python
# Before
case "session.thread_idle":
    break

# After
case "session.thread_status_idle":
    break
```

---

## Notable Details

- The Dreams API assigns IDs with a `drm_` prefix (e.g., `drm_01AbCDefGhIjKlMnOpQrStUv`).
- While a dream is `pending` or `running`, archiving or deleting its output memory store returns 400. Archiving or deleting an input store or session mid-run causes the dream to fail with `input_memory_store_unavailable` or `input_session_unavailable`.
- Webhook events return only IDs in the payload (`data.type` + `data.id`), not full objects — callers must fetch the resource on receipt. This is intentional to prevent stale data on retries.
- The `user.interrupt` event with `session_thread_id` in multiagent sessions is sent to `/v1/sessions/:id/events`, not a thread-specific endpoint.
- The CLI tool is `ant` (not `anthropic-cli`), with subcommands like `ant beta:dreams`, `ant beta:sessions:threads`, `ant beta:vaults:credentials`.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| managed-agents/dreams.md | New | +717 | Full Dreams API documentation: create, poll, use output, cancel, archive |
| managed-agents/webhooks.md | New | +350 | Webhook subscription, signature verification, event types, delivery behavior |
| managed-agents/multi-agent.md | Modified | +736/-320 | Threading model reorganized; thread interrupt/archive added; `session.thread_idle` → `session.thread_status_idle`; streaming path updated |
| managed-agents/define-outcomes.md | Modified | +549/-389 | Outcomes graduated from Research Preview; beta header simplified; file download examples updated |
| managed-agents/events-and-streaming.md | Modified | +379/-244 | Combined interrupt+redirect pattern added; streaming examples reorganized |
| managed-agents/vaults.md | Modified | +233/-162 | Credential refresh section added; OAuth diagnostic endpoint documented; `vault_credential.refresh_failed` event |
| managed-agents/files.md | Modified | +3/-12 | Minor cleanup; simplified file listing in session output examples |

---
*Generated from Claude API documentation changes detected on 2026-05-07*
