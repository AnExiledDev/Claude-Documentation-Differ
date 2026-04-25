# Claude API Documentation Changes — 2026-04-25

## Summary

This update introduces two major new beta APIs: **Memory Stores** for persistent agent memory in Managed Agents sessions, and **Admin Rate Limits** endpoints for querying organization and workspace rate limit configurations. Additionally, the `"managed"` user role was removed from the Admin API, the Usage Report API gained service account filtering, and `BetaTokenTaskBudget` / User Profiles were removed from the beta API documentation.

---

## Significant Changes

### Beta: Memory Stores API (Managed Agents)

- **New Memory Stores CRUD API**: A full memory management API is now documented under the Managed Agents beta, activated with the `managed-agents-2026-04-01` beta header. Memory stores are named, persistent stores of key-value memories that agents can read and write during sessions.

  > `POST /v1/memory_stores` — Create a memory store with `name`, optional `description`, and `metadata`.
  >
  > `GET /v1/memory_stores` — List stores (filterable by `created_at[gte]`/`created_at[lte]`, `include_archived`, pagination via `page`).
  >
  > `POST /v1/memory_stores/{id}/archive` — Archive a store (soft delete preserving history).

  - *Implication*: Developers can now create persistent stores of named memories that survive session boundaries. This enables agents to accumulate knowledge across sessions without relying on external databases.
  - *Source*: [Memory Stores](https://platform.claude.com/docs/en/api/beta/memory_stores.md)

- **Memories sub-resource**: Each store contains individual `memory` objects identified by a hierarchical `path` and a string `content`. Full CRUD operations are available.

  > `POST /v1/memory_stores/{memory_store_id}/memories` — Create a memory with required `content` (string) and `path` (string). Returns `BetaManagedAgentsMemory` with `id`, `content_sha256`, `content_size_bytes`, `created_at`, `updated_at`.
  >
  > Supports a `view` query parameter: `"basic"` or `"full"` to control content inclusion.

  - *Implication*: The path-based hierarchy allows structured organization of memories within a store (e.g., `user/preferences`, `project/context`). The `content_sha256` field enables content-based concurrency control via preconditions.
  - *Source*: [Memories](https://platform.claude.com/docs/en/api/beta/memory_stores/memories.md)

- **Memory Versions audit log**: Every mutation to a memory creates a versioned record with actor tracking.

  > `GET /v1/memory_stores/{id}/memory_versions` — List version history. Filterable by `memory_id`, `operation` (`created`/`modified`/`deleted`), `api_key_id`, `session_id`, `created_at` range.
  >
  > `POST /v1/memory_stores/{id}/memory_versions/{vid}/redact` — Permanently redact (wipe) the content of a specific version while preserving the audit record.
  >
  > Actor types: `session_actor` (session_id), `api_actor` (api_key_id), `user_actor` (user_id).

  - *Implication*: Full audit trail with actor attribution enables compliance use cases and debugging of unexpected memory mutations. The Redact endpoint allows removing sensitive content from history without deleting the version record.
  - *Source*: [Memory Versions](https://platform.claude.com/docs/en/api/beta/memory_stores/memory_versions.md)

- **Sessions: Memory Store resource attachment**: The Sessions API `resources` parameter now accepts a third resource type alongside GitHub repositories and files.

  > `BetaManagedAgentsMemoryStoreResourceParam = { memory_store_id, type: "memory_store", access?, instructions? }`
  >
  > - `access`: `"read_write"` or `"read_only"` — controls whether the agent can write to the store
  > - `instructions`: optional string up to 4096 chars — per-attachment guidance rendered into the memory section of the system prompt

  - *Implication*: Memory stores can now be attached at session creation time (or added dynamically), and the `instructions` field lets each attachment carry its own usage guidance without changing the agent's system prompt definition.
  - *Source*: [Sessions](https://platform.claude.com/docs/en/api/beta/memory_stores.md)

- **SDK support**: Memory Stores documentation and examples have been added for all official SDKs — Python, TypeScript, Go, Java, Ruby, C#, and CLI.

---

### Admin API: Rate Limits Endpoints

- **New organization-level rate limit query**: A new read endpoint lists the active rate limits for an organization, grouped by API surface or model family.

  > `GET /v1/organizations/rate_limits`
  >
  > Returns entries per `group_type`: `model_group`, `batch`, `token_count`, `files`, `skills`, `web_search`. Each entry contains a `limits` array of `{ type, value }` pairs (e.g., `requests_per_minute`, `input_tokens_per_minute`) and a `models` array (non-null only for `model_group` entries). Filterable by `group_type` or by `model` name (returns 404 if the model isn't found).

  - *Implication*: Admins and platform integrations can now programmatically read their enforced limits without checking the console UI. Useful for dashboards and capacity planning.
  - *Source*: [Rate Limits](https://platform.claude.com/docs/en/api/admin/rate_limits.md)

- **New workspace-level rate limit override query**: A companion endpoint returns only the groups that have a workspace-level override (i.e., differ from the organization default).

  > `GET /v1/organizations/workspaces/{workspace_id}/rate_limits`
  >
  > Response entries include `org_limit` alongside the workspace `value`, allowing callers to compare overrides against the org baseline. Groups without overrides are omitted — use the org endpoint to see inherited limits.

  - *Implication*: Workspace administrators can audit which limits have been customized vs. inherited, simplifying multi-workspace governance.
  - *Source*: [Workspace Rate Limits](https://platform.claude.com/docs/en/api/admin/workspaces/rate_limits.md)

---

### Admin API: `"managed"` Role Removed

- **Role enum no longer includes `"managed"`**: The `managed` role has been removed from all user/invite endpoints in the Admin API. The valid roles are now: `user`, `developer`, `billing`, `claude_code_user` (plus `admin` where applicable).

  > Before: `role: "user" or "developer" or "billing" or 3 more` (included `"managed"`)
  > After: `role: "user" or "developer" or "billing" or "claude_code_user"`

  - *Implication*: Any code that creates invites or updates users with `role: "managed"` will need to be updated. Existing managed-role users are not explicitly addressed in the documentation change.
  - *Source*: [Admin API](https://platform.claude.com/docs/en/api/admin.md)

---

### Usage Report: New Service Account Filters and Grouping

- **`service_account_ids` filter and `service_account_id` group-by added**: The Messages Usage Report endpoint now supports filtering and grouping by service account identity (for OIDC-federated callers).

  > New `group_by` values: `"account_id"`, `"service_account_id"`
  >
  > New filter: `service_account_ids: optional array of string`
  >
  > New result fields in each bucket item:
  > - `account_id` — ID of the user account; `null` if not grouping by account or for non-OAuth requests
  > - `service_account_id` — ID of the service account; `null` if not grouping by service account or for non-OIDC-federation requests

  - *Implication*: Organizations using OIDC federation can now break down API usage by service account identity in addition to API keys and workspaces.
  - *Source*: [Usage Report](https://platform.claude.com/docs/en/api/admin.md)

---

### Beta Deprecations / Removals

- **`BetaTokenTaskBudget` / `task_budget` removed**: The `task_budget` field (type `BetaTokenTaskBudget`) has been removed from `BetaOutputConfig` and from message response types across the Beta Messages API documentation. The `BetaTokenTaskBudget` domain type itself is also gone. This affects all SDK variants (Python, TypeScript, Go, Java, Ruby, C#, CLI).

  - *Implication*: Code using `output_config.task_budget` or reading `task_budget` from message responses needs to be updated. No replacement is documented in this diff.

- **User Profiles API removed from beta docs**: The `User Profiles` section (`POST /v1/user_profiles`, `GET /v1/user_profiles`, `GET /v1/user_profiles/{id}`, `POST /v1/user_profiles/{id}`, `POST /v1/user_profiles/{id}/enrollment_url`) and associated domain types (`BetaUserProfile`, `BetaUserProfileEnrollmentURL`, `BetaUserProfileTrustGrant`) have been removed from the beta API reference across all SDK documentation.

  - *Implication*: Developers who built integrations against the User Profiles beta API should check for an updated endpoint path or alternative approach, as this API no longer appears in the documentation.

---

## Notable Details

- **New beta header `"managed-agents-2026-04-01"`**: All Memory Stores API calls require this value in `anthropic-beta`. It now appears in the documented list of valid beta strings alongside existing headers.

- **`anthropic-beta` now lists 22 named values**: The enumerated beta values list has grown. Newly visible named values in this diff include `"managed-agents-2026-04-01"` (for Memory Stores). The full list includes `output-300k-2026-03-24`, `advisor-tool-2026-03-01`, `fast-mode-2026-02-01`, and others.

- **Workspace path parameter descriptions removed**: Minor wording cleanup — the inline description `"ID of the Workspace."` was removed from `workspace_id` path parameters on the Update Workspace and Archive Workspace endpoints. No behavioral change.

- **Speed filter attribution clarified**: The `speeds` filter on Usage Report was previously described as "research preview" and is now "Claude Code research preview", clarifying the feature's scope.

- **`priority_on_demand` and `flex_discount` service tiers**: The Usage Report `service_tiers` filter now explicitly lists `"priority_on_demand"` and `"flex_discount"` (previously listed only as "3 more").

---

## New Pages

- **`en_api_admin_rate_limits.md`** — Organization-level rate limit listing endpoint (`GET /v1/organizations/rate_limits`). [View](https://platform.claude.com/docs/en/api/admin/rate_limits.md)
- **`en_api_admin_workspaces_rate_limits.md`** — Workspace-level rate limit override listing (`GET /v1/organizations/workspaces/{id}/rate_limits`). [View](https://platform.claude.com/docs/en/api/admin/workspaces/rate_limits.md)
- **`en_api_beta_memory_stores.md`** — Memory Stores CRUD reference (HTTP). [View](https://platform.claude.com/docs/en/api/beta/memory_stores.md)
- **`en_api_beta_memory_stores_memories.md`** — Memories sub-resource (HTTP). [View](https://platform.claude.com/docs/en/api/beta/memory_stores/memories.md)
- **`en_api_beta_memory_stores_memory_versions.md`** — Memory version history and redaction (HTTP). [View](https://platform.claude.com/docs/en/api/beta/memory_stores/memory_versions.md)
- *(+130 additional SDK-variant pages for Memory Stores across Python, TypeScript, Go, Java, Ruby, C#, and CLI)*

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/api/beta.md` | Modified | +3228 / -1595 | Memory Stores API added; User Profiles and BetaTokenTaskBudget removed |
| `docs/api/en/api/cli/beta.md` | Modified | +1926 / -622 | Memory Stores added to CLI SDK; same removals |
| `docs/api/en/api/admin.md` | Modified | +378 / -84 | Rate Limits section added; `"managed"` role removed from invites/users |
| `docs/api/en/api/beta/sessions.md` | Modified | +541 / -47 | MemoryStoreResourceParam added to session resources |
| `docs/api/en/api/beta/sessions/resources.md` | Modified | +265 / -19 | BetaManagedAgentsMemoryStoreResource domain type added |
| `docs/api/en/api/admin/workspaces.md` | Modified | +157 / -5 | Workspace rate limit override endpoint added |
| `docs/api/en/api/admin/usage_report/retrieve_messages.md` | Modified | +23 / -12 | service_account_ids filter and account_id/service_account_id group-by added |
| `docs/api/en/api/beta/messages.md` | Modified | +42 / -254 | BetaTokenTaskBudget removed |
| `docs/api/en/api/beta/messages/create.md` | Modified | +7 / -41 | BetaTokenTaskBudget removed from create |
| `docs/api/en/api/beta/messages/batches/create.md` | Modified | +7 / -37 | BetaTokenTaskBudget removed from batch create |
| `docs/api/en/api/beta/sessions/create.md` | Modified | +62 / -4 | MemoryStoreResourceParam in session create body |
| `docs/api/en/api/admin/rate_limits.md` | New | — | Organization rate limits listing |
| `docs/api/en/api/admin/rate_limits/list.md` | New | — | List rate limits (standalone page) |
| `docs/api/en/api/admin/workspaces/rate_limits.md` | New | — | Workspace rate limit overrides |
| `docs/api/en/api/admin/workspaces/rate_limits/list.md` | New | — | List workspace overrides (standalone page) |
| `docs/api/en/api/beta/memory_stores.md` | New | — | Memory Stores API reference |
| `docs/api/en/api/beta/memory_stores/memories.md` | New | — | Memories sub-resource |
| `docs/api/en/api/beta/memory_stores/memory_versions.md` | New | — | Memory version history |
| *(+118 more SDK variant pages)* | New | — | Python, TypeScript, Go, Java, Ruby, C#, CLI memory stores |

---

*Generated from Claude API documentation changes detected on 2026-04-25*
