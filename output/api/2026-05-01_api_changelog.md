# Claude API Documentation Changes — 2026-05-01

## Summary

This update introduces the User Profiles API (beta), adds token task budget control to the Messages API, and expands Managed Agents error types to cover memory concurrency conflicts. All changes are reflected across the full SDK documentation set (TypeScript, Python, Ruby, Go, Java, C#, CLI) for a total of 798 modified pages.

---

## Significant Changes

### User Profiles API (new beta feature)

- **New `/v1/user_profiles` endpoints via `user-profiles-2026-03-24` beta**: Five new endpoints have been added to create and manage user profiles — persistent records used to attribute API requests to specific end-users within a workspace.

  | Method | Endpoint | Description |
  |--------|----------|-------------|
  | `POST` | `/v1/user_profiles` | Create a user profile |
  | `GET` | `/v1/user_profiles` | List user profiles |
  | `GET` | `/v1/user_profiles/{user_profile_id}` | Retrieve a user profile |
  | `POST` | `/v1/user_profiles/{user_profile_id}` | Update a user profile |
  | `POST` | `/v1/user_profiles/{user_profile_id}/enrollment_url` | Generate an enrollment URL |

  > `BetaUserProfile = object { id, created_at, metadata, 4 more }`
  > - `trust_grants: map[BetaUserProfileTrustGrant]` — Trust grants for this profile, keyed by grant name. Key omitted when no grant is active or in flight.
  > - `status: "active" or "pending" or "rejected"` — Status of the trust grant.

  New domain types:
  - `BetaUserProfile` — Profile object with `id` (prefixed `uprof_`), `external_id`, `metadata`, `trust_grants`, `created_at`, `updated_at`
  - `BetaUserProfileEnrollmentURL` — Contains `url` and `expires_at` for enrollment flows
  - `BetaUserProfileTrustGrant` — Trust grant with `status: "active" | "pending" | "rejected"`

  Body parameters for `Create`:
  - `external_id: optional string` — Platform's own identifier for this user. Not enforced unique. Maximum 255 characters.
  - `metadata: optional map[string]` — Free-form key-value data. Maximum 16 keys.

  - *Implication*: Enables platforms to create per-user identity records and track trust grants, intended for use alongside the `user_profile_id` parameter when making requests on behalf of end-users.
  - *Source*: [User Profiles (beta)](https://platform.claude.com/docs/en/api/beta.md)

---

### Messages API

- **New `task_budget` field in `output_config`**: `BetaOutputConfig` gains an optional `task_budget: BetaTokenTaskBudget` parameter for tracking token consumption across multi-context sessions.

  > `BetaOutputConfig = object { effort, format, task_budget }`
  >
  > `BetaTokenTaskBudget = object { total, type, remaining }`
  > - `total: number` — Total token budget across all contexts in the session.
  > - `type: "tokens"` — The budget type. Currently only 'tokens' is supported.
  > - `remaining: optional number` — Remaining tokens in the budget. Use this to track usage across contexts when implementing compaction client-side. Defaults to total if not provided.

  - *Implication*: Allows developers to set and track a cross-context token ceiling when using client-side compaction. On each new context, pass back the updated `remaining` value to maintain a running total.
  - *Source*: [Messages Create (beta)](https://platform.claude.com/docs/en/api/beta/messages/create.md)

- **New `user_profile_id` parameter on Messages Create and Messages Batch Create**:

  > `user_profile_id: optional string` — The user profile ID to attribute this request to. Use when acting on behalf of a party other than your organization.

  - *Implication*: Pairs with the new User Profiles API. Pass a `uprof_...` ID to attribute inference costs and activity to a specific end-user profile.
  - *Source*: [Messages Create (beta)](https://platform.claude.com/docs/en/api/beta/messages/create.md), [Messages Batches Create (beta)](https://platform.claude.com/docs/en/api/beta/messages/batches/create.md)

- **`max_tokens: 0` documented for prompt cache pre-warming**: The `max_tokens` parameter description now explicitly states:

  > Set to `0` to populate the [prompt cache](https://docs.claude.com/en/docs/build-with-claude/prompt-caching#pre-warming-the-cache) without generating a response.

  - *Implication*: Setting `max_tokens=0` is now a documented pattern for cache pre-warming, applicable in both Messages Create and Messages Batch Create.
  - *Source*: [Messages Create (beta)](https://platform.claude.com/docs/en/api/beta/messages/create.md), [Messages Batches Create (beta)](https://platform.claude.com/docs/en/api/beta/messages/batches/create.md)

- **New `xhigh` effort level**: The `output_config.effort` enum gains a new `"xhigh"` value, now: `"low" | "medium" | "high" | "xhigh" | "max"`.

  - *Implication*: `xhigh` sits between `high` and `max`, providing additional granularity for reasoning effort. Model capability endpoints (`BetaEffortCapability`) also expose a `xhigh: BetaCapabilitySupport` flag.
  - *Source*: [Messages Create (beta)](https://platform.claude.com/docs/en/api/beta/messages/create.md)

---

### Compaction

- **`encrypted_content` field added to compaction types**: Three compaction-related types gain a new field for round-tripping opaque server metadata across context boundaries:

  | Type | Role | Change |
  |------|------|--------|
  | `BetaCompactionBlock` | Response content block | Added `encrypted_content: string` (required) |
  | `BetaCompactionBlockParam` | Input content block | Added `encrypted_content: optional string` |
  | `BetaCompactionContentBlockDelta` | Streaming delta | Added `encrypted_content: string` (required) |

  > `encrypted_content: string` — Opaque metadata from prior compaction, to be round-tripped verbatim.

  - *Implication*: When the server returns a `BetaCompactionBlock` (auto-compaction response), clients must store and re-submit the `encrypted_content` value in the subsequent `BetaCompactionBlockParam`. Failing to round-trip this field will cause the server to lose compaction context.
  - *Source*: [Messages (beta)](https://platform.claude.com/docs/en/api/beta/messages.md)

---

### Managed Agents — Memory Stores

- **New error types for memory operations**: Two new error types documented for the Memory Stores API:

  **`BetaManagedAgentsConflictError`** — General conflict error.
  > `BetaManagedAgentsConflictError = object { type, message }`
  > - `type: "conflict_error"`

  **`BetaManagedAgentsError`** — New union type covering all standard beta errors plus memory-specific variants:
  - `BetaManagedAgentsMemoryPreconditionFailedError` — `type: "memory_precondition_failed_error"` — Returned (HTTP 409) when an optimistic-concurrency SHA-256 precondition fails on a memory update. If the stored state already exactly matches the requested `content` and `path`, the server returns 200 instead.
  - `BetaManagedAgentsMemoryPathConflictError` — `type: "memory_path_conflict_error"` — Returned when a create or update would result in a duplicate path within a store. Includes `conflicting_memory_id` and `conflicting_path` fields.

  - *Implication*: Clients performing concurrent memory writes should handle `memory_precondition_failed_error` (409) by re-reading and retrying. Path conflict errors require the client to choose a different path or resolve the existing memory first.
  - *Source*: [Memory Stores (beta)](https://platform.claude.com/docs/en/api/beta/memory_stores.md), [Memories (beta)](https://platform.claude.com/docs/en/api/beta/memory_stores/memories.md)

- **Expanded documentation for existing memory types**:
  - `BetaManagedAgentsContentSha256Precondition` — Added detailed description of the optimistic-concurrency semantics:
    > Optimistic-concurrency precondition: the update applies only if the memory's stored `content_sha256` equals the supplied value. On mismatch, the request returns `memory_precondition_failed_error` (HTTP 409); re-read the memory and retry against the fresh state.
  - `BetaManagedAgentsDeletedMemory` — Described as a tombstone; version history persists after deletion.
  - `BetaManagedAgentsMemory` — Clarified `view=basic` vs `view=full` behavior; `content_sha256` and `content_size_bytes` are always populated regardless of view.
  - *Source*: [Memory Stores (beta)](https://platform.claude.com/docs/en/api/beta/memory_stores.md)

---

### Sessions API

- **New `memory_store_id` filter on List Sessions**: The `GET /v1/sessions` endpoint gains a new optional query parameter:

  > `memory_store_id: optional string` — Filter sessions whose resources contain a memory_store with this memory store ID.

  - *Implication*: Enables looking up which sessions have a specific memory store attached as a resource — useful for auditing or resuming sessions tied to a given user's memory.
  - *Source*: [Sessions List (beta)](https://platform.claude.com/docs/en/api/beta/sessions/list.md)

---

### Beta Header — New Flag

- **`user-profiles-2026-03-24` added to `AnthropicBeta` enum**: All API endpoints that accept the `anthropic-beta` header now enumerate `"user-profiles-2026-03-24"` as a valid value. The count of named beta flags increases from 19 to 20 across all SDK references.

  - *Implication*: Pass this flag to enable User Profiles API endpoints and the `user_profile_id` parameter on Messages requests.
  - *Source*: [Beta Types](https://platform.claude.com/docs/en/api/beta.md)

---

## Notable Details

- The `BetaTokenTaskBudget` type's `remaining` field "defaults to `total` if not provided" — the server does not track remaining budget autonomously; it must be maintained and passed by the client across compaction boundaries.
- `BetaUserProfileTrustGrant.status` = `"pending"` indicates an in-flight enrollment, distinct from `"active"` (granted) and `"rejected"`. The `trust_grants` map key is omitted entirely when no grant is active or in-flight.
- The `BetaManagedAgentsMemoryPathConflictError` includes `conflicting_memory_id` and `conflicting_path` as optional fields, enabling clients to programmatically resolve the conflict.
- C# SDK docs for `Beta.Vaults.Retrieve` and `Beta.Vaults.Update` had missing Returns/Example sections that have now been restored.
- The `xhigh` effort level is also exposed in the beta Models API response (`BetaEffortCapability.xhigh: BetaCapabilitySupport`) so callers can check per-model support before using it.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/api/beta.md` | Modified | +1810/-184 | User Profiles API endpoints + BetaTokenTaskBudget + BetaManagedAgentsConflictError + BetaManagedAgentsError types |
| `docs/api/en/api/cli/beta.md` | Modified | +1214/-116 | Same as above, CLI SDK variant |
| `docs/api/en/api/csharp/beta.md` | Modified | +1758/-201 | Same + C# vault doc fixes |
| `docs/api/en/api/beta/memory_stores.md` | Modified | +655/-87 | New error types + expanded type docs |
| `docs/api/en/api/beta/memory_stores/memories.md` | Modified | +278/-12 | Error types + view parameter docs |
| `docs/api/en/api/beta/memory_stores/memory_versions.md` | Modified | +222/-12 | Expanded memory version docs |
| `docs/api/en/api/beta/messages.md` | Modified | +252/-36 | task_budget in BetaOutputConfig, xhigh effort, user_profile_id, encrypted_content on compaction |
| `docs/api/en/api/beta/messages/batches/create.md` | Modified | +36/-4 | user_profile_id + max_tokens=0 docs + task_budget |
| `docs/api/en/api/beta/messages/create.md` | Modified | +40/-4 | user_profile_id + max_tokens=0 docs + task_budget |
| `docs/api/en/api/beta/sessions/list.md` | Modified | +7/-1 | New memory_store_id filter param |
| `docs/api/en/api/beta/models.md` | Modified | +47/-3 | xhigh effort capability in BetaModelCapabilities |
| `docs/api/en/api/beta/memory_stores/memory_versions/list.md` | Modified | +51/-3 | Expanded docs |
| `docs/api/en/api/beta/memory_stores/memory_versions/redact.md` | Modified | +49/-3 | Expanded docs |
| `docs/api/en/api/beta/memory_stores/memory_versions/retrieve.md` | Modified | +49/-3 | Expanded docs |
| `docs/api/en/api/beta/user_profiles.md` | Modified | +11/-11 | Wording update |
| *(+ ~783 SDK mirror pages)* | Modified | varies | Same changes propagated to Python, TypeScript, Ruby, Go, Java, C#, CLI SDK docs |

---

*Generated from Claude API documentation changes detected on 2026-05-01*
