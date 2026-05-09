# Claude API Documentation Changes — 2026-05-09

## Summary

Two major new API surface areas were documented in this release: a **Webhooks system** for the Managed Agents beta (covering 22 event types across sessions, vaults, and vault credentials, with SDK bindings for all six languages), and a **Compliance API** (`/v1/compliance/*`) that provides enterprise-grade read-only audit access to organization activities, chats, projects, groups, and more. Alongside these additions, the Managed Agents beta received documentation updates for several new fields (`title` on sessions, `mount_path` on session resources, `description` on environments), and the API reference examples for Messages, Count Tokens, and Completions were expanded to show more complete request payloads. Two new model identifiers — `claude-opus-4-7` and `claude-mythos-preview` — also appeared in model enumerations across the reference.

---

## Significant Changes

### Webhooks (Beta Managed Agents)

- **New webhook event system for sessions and vaults**: The beta API now documents a `BetaWebhookEvent` object with an `id`, `created_at` (RFC 3339), `data`, and `type: "event"` envelope. Events are dispatched for session and vault lifecycle transitions.
  > `BetaWebhookEvent = object { id, created_at, data, type }` — `id: string` — Unique event identifier for idempotency.
  - *Implication*: Developers building on the Managed Agents beta can now receive push notifications for session and vault state changes rather than polling.
  - *Source*: [beta/webhooks.md](https://platform.claude.com/docs/en/api/beta/webhooks.md)

- **22 distinct webhook event types documented**: The `BetaWebhookEventData` union covers the full lifecycle of sessions and vaults:
  - **Session events**: `session.created`, `session.pending`, `session.running`, `session.idled`, `session.requires_action`, `session.archived`, `session.deleted`, `session.status_rescheduled`, `session.status_run_started`, `session.status_idled`, `session.status_terminated`, `session.thread_created`, `session.thread_idled`, `session.thread_terminated`, `session.outcome_evaluation_ended`
  - **Vault events**: `vault.created`, `vault.archived`, `vault.deleted`
  - **Vault credential events**: `vault_credential.created`, `vault_credential.archived`, `vault_credential.deleted`, `vault_credential.refresh_failed`
  - Each event data object carries `{ id, organization_id, type, workspace_id }`; vault credential events additionally include `vault_id`.
  - *Implication*: The `vault_credential.refresh_failed` event in particular signals that credential rotation monitoring is an intended use case.
  - *Source*: [beta/webhooks.md](https://platform.claude.com/docs/en/api/beta/webhooks.md)

- **`UnwrapWebhookEvent` helper**: A domain-type helper `UnwrapWebhookEvent` is documented alongside the event types for safely extracting typed event data from webhook payloads.

- **SDK webhook bindings added for all six languages**: Separate webhook type-binding pages were added for Python, TypeScript, Go, Java, Ruby, and C#, plus the CLI. The same 22 event types are reflected in each SDK's type system.
  - *Source*: [python/beta/webhooks.md](https://platform.claude.com/docs/en/api/python/beta/webhooks.md), [typescript/beta/webhooks.md](https://platform.claude.com/docs/en/api/typescript/beta/webhooks.md), [go/beta/webhooks.md](https://platform.claude.com/docs/en/api/go/beta/webhooks.md), [java/beta/webhooks.md](https://platform.claude.com/docs/en/api/java/beta/webhooks.md), [ruby/beta/webhooks.md](https://platform.claude.com/docs/en/api/ruby/beta/webhooks.md), [csharp/beta/webhooks.md](https://platform.claude.com/docs/en/api/csharp/beta/webhooks.md)

---

### Compliance API (New)

- **New read-only Compliance API at `/v1/compliance/*`**: An entirely new API surface is documented for enterprise compliance and audit use cases. This API uses a separate authentication mechanism (`Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY`) distinct from the standard API key.
  > `curl https://api.anthropic.com/v1/compliance/organizations \ -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"`
  - *Implication*: Enterprise customers with a parent organization can delegate compliance review to a separate key with read-only access, limiting blast radius compared to using a full API key.
  - *Source*: [compliance.md](https://platform.claude.com/docs/en/api/compliance.md)

- **Activity audit log**: `GET /v1/compliance/activities` returns a paginated list of compliance activities filterable by `activity_types`. The documented event type enum contains **295+ distinct activity strings** covering account management, auth flows, billing, SSO, SCIM, MCP servers, Claude skills/commands/plugins, RBAC, and more.
  > `activity_types: optional array of "account_deleted" or "admin_api_key_created" or "admin_api_key_deleted" or 292 more` — Filter activities by type
  - *Implication*: Compliance officers can filter the audit log to specific categories (e.g., `rbac_role_assigned`, `mcp_server_created`, `org_sso_toggled`) without needing to process the full firehose.
  - *Source*: [compliance/activities/list.md](https://platform.claude.com/docs/en/api/compliance/activities/list.md)

- **Chat and project content access**: New endpoints expose Claude.ai chat metadata and content for compliance review:
  - `GET /v1/compliance/apps/chats` — list chats by `user_ids` (required, 1–10 per request), with time-range and project filters
  - `DELETE /v1/compliance/apps/chats/{chat_id}` — delete a chat
  - `GET /v1/compliance/apps/chats/{chat_id}/files` — list uploaded files for a chat
  - `GET /v1/compliance/apps/chats/{chat_id}/messages` — retrieve chat messages
  - `GET /v1/compliance/apps/chats/{chat_id}/generated_files` — list AI-generated files
  - `GET /v1/compliance/apps/artifacts/{artifact_id}/content` — retrieve artifact content
  - Project endpoints: list, retrieve, delete projects; list/retrieve/delete project documents and attachments
  - *Source*: [compliance/apps/chats.md](https://platform.claude.com/docs/en/api/compliance/apps/chats.md), [compliance/apps/projects.md](https://platform.claude.com/docs/en/api/compliance/apps/projects.md)

- **Organization and user management read access**: Compliance endpoints also expose organizational structure:
  - `GET /v1/compliance/organizations` — list sub-organizations (up to 1,000; no pagination)
  - `GET /v1/compliance/organizations/{org_uuid}/users` — list users in an organization
  - `GET /v1/compliance/organizations/{org_uuid}/roles` — list roles and their permissions
  - `GET /v1/compliance/groups` — list groups; `GET /v1/compliance/groups/{group_id}/members`
  - *Source*: [compliance/organizations.md](https://platform.claude.com/docs/en/api/compliance/organizations.md), [compliance/groups.md](https://platform.claude.com/docs/en/api/compliance/groups.md)

---

### Managed Agents Beta — New Fields

- **`title` field on sessions**: The session create (`POST /v1/sessions`) and session update (`POST /v1/sessions/{session_id}`) examples now include a `title` field.
  > `"title": "Order #1234 inquiry"` — added to both create and update examples
  - *Implication*: Sessions can now be labeled with a human-readable title at creation or update time, useful for distinguishing sessions in multi-tenant or multi-topic deployments.
  - *Source*: [beta/sessions/create.md](https://platform.claude.com/docs/en/api/beta/sessions/create.md), [beta/sessions/update.md](https://platform.claude.com/docs/en/api/beta/sessions/update.md)

- **`mount_path` on session resource add**: The `POST /v1/sessions/{session_id}/resources` example now includes a `mount_path` parameter.
  > `"mount_path": "/uploads/receipt.pdf"` — added alongside `file_id` and `type` in the example
  - *Implication*: Files added to a session can now be mounted at a specific path inside the session's execution environment.
  - *Source*: [beta/sessions/resources/add.md](https://platform.claude.com/docs/en/api/beta/sessions/resources/add.md)

- **`description` on environments**: The environment create (`POST /v1/environments`) example now includes a `description` field. The environment update (`POST /v1/environments/{environment_id}`) example was simplified to show `description`-only updates (replacing the previous example that showed a full `config` object with networking and packages).
  > `"description": "Python environment with data-analysis packages."`
  - *Source*: [beta/environments/create.md](https://platform.claude.com/docs/en/api/beta/environments/create.md), [beta/environments/update.md](https://platform.claude.com/docs/en/api/beta/environments/update.md)

- **`metadata` on vaults and credentials**: Vault create, vault update, credential create, and credential update examples now show `metadata` and `display_name` fields. Previously the update examples used empty `{}` bodies.
  > `"metadata": { "environment": "production" }` — added to vault create, vault update, credential create, and credential update examples
  - *Source*: [beta/vaults/create.md](https://platform.claude.com/docs/en/api/beta/vaults/create.md), [beta/vaults/credentials/create.md](https://platform.claude.com/docs/en/api/beta/vaults/credentials/create.md)

- **`external_id` and `metadata` on user profiles**: User profile create and update examples now include `external_id` and `metadata` fields (previously both used empty `{}` request bodies).
  > `"external_id": "user_12345", "metadata": {}`
  - *Source*: [beta/user_profiles/create.md](https://platform.claude.com/docs/en/api/beta/user_profiles/create.md), [beta/user_profiles/update.md](https://platform.claude.com/docs/en/api/beta/user_profiles/update.md)

- **Agent create example updated**: The `POST /v1/agents` curl example changed from a multi-agent coordinator topology to a simple single-agent example using `description`, `metadata`, `system`, and `tools: [{ "type": "agent_toolset_20260401" }]`. The `POST /v1/agents/{agent_id}` (update) example was similarly simplified to a system prompt update only.
  - *Source*: [beta/agents/create.md](https://platform.claude.com/docs/en/api/beta/agents/create.md), [beta/agents/update.md](https://platform.claude.com/docs/en/api/beta/agents/update.md)

---

### Models

- **`claude-opus-4-7` added to model enumerations**: The new model identifier `"claude-opus-4-7"` (described as "Frontier intelligence for long-running agents and coding") appears as the top option in the `BetaManagedAgentsModel` enum (Managed Agents agent create) and in the `Model` enum for the Completions API.
  - *Implication*: `claude-opus-4-7` is now a valid model string for agents and completions endpoints.

- **`claude-mythos-preview` added to Completions model enum**: The identifier `"claude-mythos-preview"` (described as "New class of intelligence, strongest in coding and cybersecurity") is now listed in the `Model` union for the legacy Completions API.
  - *Source*: [completions.md](https://platform.claude.com/docs/en/api/completions.md)

---

### API Reference Examples

- **Messages, Count Tokens, and Completions examples expanded**: The curl examples for `POST /v1/messages`, `POST /v1/messages/count_tokens`, and `POST /v1/complete` were updated to include more parameters, demonstrating fuller usage patterns. These are example updates only — no parameters were added to the API.
  - Messages create now shows `system`, `temperature`, `thinking: { "type": "adaptive" }`, `tools`, `top_k`, `top_p`
  - Count Tokens now shows `system`, `thinking: { "type": "adaptive" }`, `tools`
  - Completions now shows `temperature`, `top_k`, `top_p`
  - *Implication*: The `thinking: { "type": "adaptive" }` value in the Messages example signals that adaptive thinking is a documented, canonical mode — previously examples typically only showed `type: "enabled"`.
  - *Source*: [messages/create.md](https://platform.claude.com/docs/en/api/messages/create.md), [messages/count_tokens.md](https://platform.claude.com/docs/en/api/messages/count_tokens.md), [completions/create.md](https://platform.claude.com/docs/en/api/completions/create.md)

---

## New Pages

- **`beta/webhooks.md`** — Webhook domain types (`BetaWebhookEvent`, 22 event data variants, `UnwrapWebhookEvent`) for the Managed Agents beta. [View](https://platform.claude.com/docs/en/api/beta/webhooks.md)
- **`compliance.md`** — Root Compliance API page with `GET /v1/compliance/activities` and 295+ activity type enum values. [View](https://platform.claude.com/docs/en/api/compliance.md)
- **`compliance/activities/list.md`** — Standalone page for listing compliance activities. [View](https://platform.claude.com/docs/en/api/compliance/activities/list.md)
- **`compliance/apps/chats.md`** — List and filter Claude.ai chats by user for compliance review. [View](https://platform.claude.com/docs/en/api/compliance/apps/chats.md)
- **`compliance/apps/chats/delete.md`**, **`/files.md`**, **`/files/content.md`**, **`/files/delete.md`**, **`/files/retrieve.md`**, **`/generated_files.md`**, **`/generated_files/content.md`**, **`/list.md`**, **`/messages.md`** — Chat sub-resource endpoints. [View](https://platform.claude.com/docs/en/api/compliance/apps/chats/delete.md)
- **`compliance/apps/artifacts.md`** / **`/artifacts/content.md`** — Retrieve artifact content for compliance. [View](https://platform.claude.com/docs/en/api/compliance/apps/artifacts.md)
- **`compliance/apps/projects.md`** and sub-pages (list, retrieve, delete, documents, documents/delete, documents/retrieve, attachments) — Project compliance endpoints. [View](https://platform.claude.com/docs/en/api/compliance/apps/projects.md)
- **`compliance/groups.md`**, **`/groups/list.md`**, **`/groups/retrieve.md`**, **`/groups/members.md`**, **`/groups/members/list.md`** — Group listing for compliance. [View](https://platform.claude.com/docs/en/api/compliance/groups.md)
- **`compliance/organizations.md`**, **`/organizations/list.md`**, **`/organizations/roles.md`**, **`/organizations/roles/list.md`**, **`/organizations/roles/retrieve.md`**, **`/organizations/roles/permissions.md`**, **`/organizations/roles/permissions/list.md`**, **`/organizations/users.md`**, **`/organizations/users/list.md`** — Org-level read access for compliance. [View](https://platform.claude.com/docs/en/api/compliance/organizations.md)
- **SDK webhook pages** (`python/beta/webhooks.md`, `typescript/beta/webhooks.md`, `go/beta/webhooks.md`, `java/beta/webhooks.md`, `ruby/beta/webhooks.md`, `csharp/beta/webhooks.md`, `cli/beta/webhooks.md`) — Language-specific webhook type bindings. [Python](https://platform.claude.com/docs/en/api/python/beta/webhooks.md) · [TypeScript](https://platform.claude.com/docs/en/api/typescript/beta/webhooks.md) · [Go](https://platform.claude.com/docs/en/api/go/beta/webhooks.md) · [Java](https://platform.claude.com/docs/en/api/java/beta/webhooks.md) · [Ruby](https://platform.claude.com/docs/en/api/ruby/beta/webhooks.md) · [C#](https://platform.claude.com/docs/en/api/csharp/beta/webhooks.md)

---

## Notable Details

- **Compliance API uses a different auth header**: The Compliance API examples use `Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY`, not the standard `X-Api-Key` header. This is a distinct credential type for organizations managing compliance-sensitive data at scale.
- **Compliance chat list requires `user_ids` (1–10 per request)**: `GET /v1/compliance/apps/chats` requires at least one `user_id` filter — it is not a free-form scan endpoint.
- **Compliance org list caps at 1,000**: The `GET /v1/compliance/organizations` endpoint explicitly states it returns an error (not pagination) if the result would exceed 1,000 organizations.
- **`vault_credential.refresh_failed` is a credential health event**: Its presence implies that OAuth or rotating credentials managed through Vaults can fail to refresh, and that webhook consumers should handle this failure case programmatically.
- **Beta header enum now at 24 values**: The `anthropic-beta` header enum across beta endpoints now lists 24 named values, including `"managed-agents-2026-04-01"` as the current Managed Agents version. No new beta headers were added in this diff; the enum size reflects the accumulated set.
- **Agent model enum leads with `claude-opus-4-7`**: The ordering of `BetaManagedAgentsModel` puts `claude-opus-4-7` above `claude-opus-4-6`, suggesting `opus-4-7` is now the recommended frontier option for new agent deployments.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `beta.md` | Modified | +1508/-64 | Added complete Webhooks section with 22 event types and `UnwrapWebhookEvent` |
| `python/beta.md` | Modified | +1389/-1 | Added Webhooks section (Python SDK types) |
| `typescript/beta.md` | Modified | +1389/-1 | Added Webhooks section (TypeScript SDK types) |
| `go/beta.md` | Modified | +1389/-1 | Added Webhooks section (Go SDK types) |
| `java/beta.md` | Modified | +1389/-1 | Added Webhooks section (Java SDK types) |
| `ruby/beta.md` | Modified | +1389/-1 | Added Webhooks section (Ruby SDK types) |
| `cli/beta.md` | Modified | +1209/-1 | Added Webhooks section (CLI types) |
| `csharp/beta.md` | Modified | +1209/-1 | Added Webhooks section (C# SDK types) |
| `beta/messages.md` | Modified | +64/-13 | Updated examples (system, thinking, tools) |
| `messages.md` | Modified | +64/-13 | Updated examples (system, thinking, tools) |
| `beta/messages/create.md` | Modified | +34/-7 | Expanded curl example |
| `messages/create.md` | Modified | +34/-7 | Expanded curl example |
| `beta/messages/count_tokens.md` | Modified | +30/-6 | Expanded curl example |
| `messages/count_tokens.md` | Modified | +30/-6 | Expanded curl example |
| `beta/agents.md` | Modified | +18/-25 | Updated agent create example |
| `beta/vaults.md` | Modified | +20/-3 | Updated vault examples with metadata |
| `beta/vaults/credentials.md` | Modified | +10/-1 | Updated credential examples with metadata |
| `beta/environments.md` | Modified | +3/-17 | Simplified environment update example |
| `beta/agents/create.md` | Modified | +14/-13 | Changed example from multiagent to single-agent |
| `beta/vaults/credentials/update.md` | Modified | +6/-1 | Added display_name/metadata to example |
| `beta/vaults/update.md` | Modified | +6/-1 | Added display_name/metadata to example |
| `beta/user_profiles.md` | Modified | +7/-2 | Updated examples with external_id/metadata |
| `beta/sessions.md` | Modified | +7/-3 | Updated examples with title field |
| `beta/agents/update.md` | Modified | +4/-12 | Simplified update example to system prompt only |
| `completions.md` | Modified | +4/-1 | Added temperature/top_k/top_p to example |
| `completions/create.md` | Modified | +4/-1 | Added temperature/top_k/top_p to example |
| `beta/vaults/credentials/create.md` | Modified | +4/-0 | Added display_name/metadata to example |
| `beta/user_profiles/create.md` | Modified | +4/-1 | Added external_id/metadata to example |
| `beta/environments/create.md` | Modified | +2/-1 | Added description to example |
| `beta/sessions/create.md` | Modified | +2/-1 | Added title to example |
| `beta/sessions/resources.md` | Modified | +2/-1 | Updated example |
| `beta/sessions/resources/add.md` | Modified | +2/-1 | Added mount_path to example |
| `beta/environments/update.md` | Modified | +1/-16 | Simplified to description-only update |
| `beta/user_profiles/update.md` | Modified | +3/-1 | Added external_id to example |
| `beta/sessions/update.md` | Modified | +3/-1 | Added title to example |
| `compliance.md` | New | +2909 | Root Compliance API with activities list |
| `compliance/apps/chats.md` | New | — | Chat listing and sub-resource endpoints |
| `compliance/apps/projects.md` | New | — | Project listing and sub-resource endpoints |
| `compliance/organizations.md` | New | — | Org structure (roles, users) |
| `compliance/groups.md` | New | — | Group listing and membership |
| `beta/webhooks.md` | New | — | Webhook domain types (language-agnostic) |
| *(6 SDK webhook pages)* | New | — | Per-SDK webhook type bindings |

---

*Generated from Claude API documentation changes detected on 2026-05-09*
