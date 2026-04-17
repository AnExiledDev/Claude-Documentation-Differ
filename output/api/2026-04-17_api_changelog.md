# Claude API Documentation Changes — 2026-04-17

## Summary

This update introduces the User Profiles API (beta), a new `claude-opus-4-7` model, and several extensions to the beta Messages API including a `task_budget` parameter, a new `xhigh` effort level, `encrypted_content` fields on compaction blocks, and a `user_profile_id` request parameter. All SDKs (Python, TypeScript, Ruby, Go, Java, C#, and CLI) received corresponding documentation updates, and the C# SDK gained substantial new beta coverage.

---

## Significant Changes

### New API: User Profiles (Beta)

- **User Profiles resource added at `/v1/user_profiles`**: A new beta resource for managing per-user profiles that can be associated with API requests. Five operations are documented:
  - `POST /v1/user_profiles` — Create a user profile
  - `GET /v1/user_profiles` — List user profiles (paginated)
  - `GET /v1/user_profiles/{user_profile_id}` — Retrieve a user profile
  - `POST /v1/user_profiles/{user_profile_id}` — Update a user profile
  - `POST /v1/user_profiles/{user_profile_id}/enrollment_url` — Create an enrollment URL

  > `id: string` — Unique identifier for this user profile, prefixed `uprof_`.
  >
  > `trust_grants: map[BetaUserProfileTrustGrant]` — Trust grants for this profile, keyed by grant name. Key omitted when no grant is active or in flight.
  >
  > `status: "active" or "pending" or "rejected"` — Status of the trust grant.

  The enrollment URL endpoint (`POST /v1/user_profiles/{id}/enrollment_url`) returns a time-limited URL (`expires_at`, `url`) to be sent to an end user for completing their trust grant flow.

  Profile objects support optional `external_id` (up to 255 chars, not enforced unique) and free-form `metadata` (max 16 key-value pairs, keys ≤64 chars, values ≤512 chars).

  The beta header `user-profiles-2026-03-24` is required to use this resource.

  - *Implication*: Enables per-user attribution and trust delegation in multi-tenant applications. The `trust_grants` mechanism and enrollment URL flow suggest an identity verification workflow where end users grant specific trust levels to agent operations on their behalf.
  - *Source*: [User Profiles API (beta)](https://platform.claude.com/docs/en/api/beta/user_profiles.md)

### Models

- **New model `claude-opus-4-7`**: Added to all model enumeration lists across the API and every SDK. Now appears first in the `UnionMember0` model list, ahead of `claude-mythos-preview`.

  > `"claude-opus-4-7"` — Frontier intelligence for long-running agents and coding

  The model is also added to the Agents API model list (`BetaManagedAgentsModel`) and is now supported on Priority Tier.

  - *Implication*: Developers should use `claude-opus-4-7` as the new top-tier model for agent and coding workloads. Code examples in beta-headers.md and service-tiers.md have been updated to use this model.
  - *Source*: [Beta API reference](https://platform.claude.com/docs/en/api/beta.md)

- **Rate limits note updated to include Opus 4.7**: The Opus combined-traffic footnote now reads:

  > `* - Opus rate limit is a total limit that applies to combined traffic across Opus 4.7, Opus 4.6, Opus 4.5, Opus 4.1, and Opus 4.`

  - *Source*: [Rate Limits](https://platform.claude.com/docs/en/api/rate-limits.md)

### Beta Messages API

- **New `xhigh` effort level**: A new effort value `"xhigh"` has been added to `output_config.effort`, sitting between `"high"` and `"max"`. The `BetaEffortCapability` type has been expanded to `object { high, low, max, xhigh, ... }`, and model capability introspection now exposes an `xhigh` field.

  > `effort: optional "low" or "medium" or "high" or 2 more`
  >
  > Available values: `"low"`, `"medium"`, `"high"`, `"xhigh"`, `"max"`

  - *Implication*: Provides an additional granularity point for reasoning effort control between `high` and `max`. Check model capability objects to determine which models support `xhigh`.
  - *Source*: [Beta Messages Create](https://platform.claude.com/docs/en/api/beta/messages/create.md)

- **New `task_budget` parameter in `output_config`**: A new optional `task_budget` field on `output_config` enables token budget tracking across contexts in a session.

  > `task_budget: optional BetaTokenTaskBudget`
  >
  > User-configurable total token budget across contexts.
  >
  > - `total: number` — Total token budget across all contexts in the session.
  > - `type: "tokens"` — The budget type. Currently only 'tokens' is supported.
  > - `remaining: optional number` — Remaining tokens in the budget. Use this to track usage across contexts when implementing compaction client-side. Defaults to total if not provided.

  The `BetaOutputConfig` type is now `object { effort, format, task_budget }`.

  - *Implication*: Enables client-side management of token consumption across compacted conversation contexts. Pairs with the new `encrypted_content` compaction fields to support robust multi-turn agent patterns.
  - *Source*: [Beta Messages Create](https://platform.claude.com/docs/en/api/beta/messages/create.md)

- **New `user_profile_id` parameter on beta Messages.Create**:

  > `user_profile_id: optional string` — The user profile ID to attribute this request to. Use when acting on behalf of a party other than your organization.

  - *Implication*: Links a message request to a specific `uprof_`-prefixed user profile created via the new User Profiles API. Required for associating inference with an identified end user.
  - *Source*: [Beta Messages Create](https://platform.claude.com/docs/en/api/beta/messages/create.md)

- **`encrypted_content` added to compaction block types**: Three compaction-related types now include `encrypted_content`:
  - `BetaCompactionBlock` — Added `encrypted_content: string`
  - `BetaCompactionBlockParam` — Added `encrypted_content: optional string`
  - `BetaCompactionContentBlockDelta` — Added `encrypted_content: string`

  > `encrypted_content: string` — Opaque metadata from prior compaction, to be round-tripped verbatim

  - *Implication*: When receiving a compaction response, preserve and re-submit `encrypted_content` verbatim in the next request's compaction block. This enables server-side state continuity across compacted contexts.
  - *Source*: [Beta Messages](https://platform.claude.com/docs/en/api/beta/messages.md)

### Service Tiers

- **Opus 4.7 added to Priority Tier US-inference pricing**: The service-tiers page now explicitly lists Claude Opus 4.7 alongside 4.6 in the 1.1× input/output token accounting for US-only inference (`inference_geo: "us"`) requests.

  > `Priority Tier is supported on all available Claude models (including Claude Opus 4.7) except Claude Mythos Preview.`

  - *Source*: [Service Tiers](https://platform.claude.com/docs/en/api/service-tiers.md)

### SDKs

- **User Profiles documentation added to all SDKs**: 48 new pages published covering User Profiles CRUD and enrollment URL creation across Python, TypeScript, Ruby, Go, Java, C#, and CLI SDKs. Each SDK now documents the full User Profiles surface with typed parameters and code examples.
  - *Source*: [Python](https://platform.claude.com/docs/en/api/python/beta/user_profiles.md) · [TypeScript](https://platform.claude.com/docs/en/api/typescript/beta/user_profiles.md) · [Ruby](https://platform.claude.com/docs/en/api/ruby/beta/user_profiles.md) · [Go](https://platform.claude.com/docs/en/api/go/beta/user_profiles.md) · [Java](https://platform.claude.com/docs/en/api/java/beta/user_profiles.md) · [C#](https://platform.claude.com/docs/en/api/csharp/beta/user_profiles.md) · [CLI](https://platform.claude.com/docs/en/api/cli/beta/user_profiles.md)

- **C# SDK beta documentation expanded significantly**: The C# SDK received a large number of previously missing beta pages (agents, environments, files, messages/batches, models, sessions, skills, vaults — all sub-operations included). These pages appear to be newly published rather than updated, bringing C# to feature parity with other SDKs in the beta reference docs.

- **`user-profiles-2026-03-24` beta header added to all SDK enumerations**: The new beta tag appears in the `AnthropicBeta` enum across all SDKs and the base API reference.

---

## New Pages

All 48 new pages are SDK-specific reference pages for the User Profiles beta resource. The canonical REST API page is:

- **`en_api_beta_user_profiles.md`** — User Profiles API: Create, List, Retrieve, Update, and Create Enrollment URL operations with domain type definitions (`BetaUserProfile`, `BetaUserProfileEnrollmentURL`, `BetaUserProfileTrustGrant`). [View](https://platform.claude.com/docs/en/api/beta/user_profiles.md)

SDK-specific variants published for: Python, TypeScript, Ruby, Go, Java, C#, and CLI — each with full operation detail pages.

---

## Notable Details

- **Count Tokens example model updated**: The `beta/messages/count_tokens` example body was changed from `{ "content": "string", "model": "claude-mythos-preview" }` to `{ "content": "Hello, world", "model": "claude-opus-4-6" }`. This is a documentation correction rather than an API change.
- **Model list ordering changed**: In all model enumerations, `claude-opus-4-7` now appears before `claude-mythos-preview` as the primary member of `UnionMember0`. This positions it as the recommended first-choice model.
- **`BetaEffortCapability` type shape changed**: From `object { high, low, max, 2 more }` to `object { high, low, max, 3 more }` — the addition of `xhigh` reflects a new supported effort tier at the model-capabilities level, not just as a parameter value.
- **Enrollment URL TTL not configurable**: The `create_enrollment_url` operation returns `expires_at` but accepts no parameters for controlling expiry, implying server-controlled TTL.
- **Trust grant model is eventually consistent**: The `trust_grants` map on `BetaUserProfile` is keyed by grant name and omits keys when no grant is active or in-flight, indicating a sparse/lazy model rather than a comprehensive list.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `beta/user_profiles.md` + 5 sub-pages | New (×8 SDKs = 48 total) | ~48 new pages | User Profiles CRUD + enrollment URL for all SDKs |
| `beta.md` | Modified | +1586/-332 | Added User Profiles, `user-profiles-2026-03-24` beta tag, `xhigh` capability fields |
| `python/beta.md` | Modified | +1906/-587 | Same additions for Python SDK |
| `typescript/beta.md` | Modified | +1714/-434 | Same additions for TypeScript SDK |
| `ruby/beta.md` | Modified | +1720/-464 | Same additions for Ruby SDK |
| `go/beta.md` | Modified | +1855/-558 | Same additions for Go SDK |
| `java/beta.md` | Modified | +1461/-222 | Same additions for Java SDK |
| `csharp/beta.md` | Modified | +1439/-236 | Same additions for C# SDK |
| `cli/beta.md` | Modified | +818/-72 | Same additions for CLI SDK |
| `beta/messages.md` | Modified | +400/-68 | Added `task_budget`, `xhigh` effort, `user_profile_id`, `encrypted_content` on compaction blocks, `claude-opus-4-7` |
| `python/beta/messages.md` | Modified | +526/-164 | Same for Python |
| `typescript/beta/messages.md` | Modified | +376/-44 | Same for TypeScript |
| `ruby/beta/messages.md` | Modified | +377/-45 | Same for Ruby |
| `go/beta/messages.md` | Modified | +285/-1 | Same for Go |
| `java/beta/messages.md` | Modified | +280/-0 | Same for Java |
| `csharp/beta/messages.md` | Modified | +282/-2 | Same for C# |
| `cli/beta/messages.md` | Modified | +262/-50 | Same for CLI |
| `beta/messages/create.md` | Modified | +58/-8 | Added `user_profile_id`, `xhigh`, `task_budget`, `claude-opus-4-7` |
| `beta/agents.md` | Modified | +91/-23 | Updated model list to include `claude-opus-4-7` |
| `models.md` | Modified | +47/-3 | Added `user-profiles-2026-03-24` beta tag |
| `beta-headers.md` | Modified | +5/-5 | Updated code examples to use `claude-opus-4-7` |
| `rate-limits.md` | Modified | +1/-1 | Added Opus 4.7 to Opus combined-rate footnote |
| `service-tiers.md` | Modified | +5/-5 | Added Opus 4.7 to US-only inference (1.1×) and Priority Tier supported models |
| `client-sdks.md` | Modified | +16/-16 | Minor SDK description updates |

---

*Generated from Claude API documentation changes detected on 2026-04-17*
