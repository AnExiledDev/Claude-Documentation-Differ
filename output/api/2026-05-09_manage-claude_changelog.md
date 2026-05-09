# Claude API Documentation Changes — 2026-05-09

## Summary

Nine new pages document a new Compliance API (Claude Enterprise only) giving programmatic access to organization activity, chats, files, projects, and user/group directories for audit and governance use cases. A new dedicated Admin API overview page replaces a former "overview" link referenced across multiple existing docs. The WIF/SPIFFE provider guide was expanded to cover any SPIFFE-conformant issuer (not SPIRE exclusively) and gained multi-language SDK examples.

---

## Significant Changes

### Compliance API (New — Claude Enterprise Only)

- **New Compliance API launched**: Eight new documentation pages cover a brand-new API family under `/v1/compliance/*`. It is available only on the Claude Enterprise plan and must be explicitly enabled before use. Two key types control access:

  > "A **Compliance Access Key** (created in claude.ai) reaches every endpoint, and an **Admin API key** (created in Claude Console) reaches the Activity Feed only."

  | Key type | Prefix | Created in | Access |
  |---|---|---|---|
  | Compliance Access Key | `sk-ant-api01-...` | claude.ai > Org Settings > Data and privacy | Full Compliance API |
  | Admin API key | `sk-ant-admin01-...` | Claude Console > Settings > Admin keys | Activity Feed only |

  - *Implication*: Enterprises can now programmatically ingest audit events, retrieve/delete chat content, and enumerate org directories without manual CSV exports from the Console.
  - *Source*: [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api.md)

- **Compliance API scopes**: Compliance Access Keys are provisioned with one or more immutable scopes at creation time:

  | Scope | Grants |
  |---|---|
  | `read:compliance_activities` | Activity Feed across parent and linked organizations |
  | `read:compliance_user_data` | Read user chats, messages, files, projects, users, group members |
  | `delete:compliance_user_data` | Hard-delete user chats, files, and projects |
  | `read:compliance_org_data` | Organization metadata, roles, groups |

  > "Compliance Access Key scopes are immutable after creation. To change scopes, create a new key with the scopes you want, then delete the old one."

  - *Implication*: Scope selection is final at key creation. Integrations that need both read and delete should use two separate keys so a leaked read key cannot delete data.
  - *Source*: [Get access to the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access.md)

- **Activity Feed endpoint**: `GET /v1/compliance/activities` returns a reverse-chronological stream of every authentication, chat, file, project, administrative, and platform action in the organization. Activities are queryable within 1 minute of occurrence and retained for **6 years**.

  > "Repeatable parameters use array-bracket query syntax: pass `activity_types[]=...`, `actor_ids[]=...`, or `organization_ids[]=...` once for each value."

  The endpoint supports both cursor-driven incremental reads (`after_id` / `before_id`) and window polling (`created_at.gte` / `created_at.lt`). Activity Feed calls themselves emit `compliance_api_accessed` events, so access to compliance data is itself auditable.
  - *Implication*: Developers building SIEM integrations should use `actor.user_id` (not `email_address`) as the primary join key; it is stable across email/display-name changes.
  - *Source*: [Query the Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed.md)

- **Content retrieval and deletion endpoints**: New endpoints under `/v1/compliance/apps/*` allow reading chat messages, downloading file and artifact content, listing projects and project attachments, and permanently hard-deleting chats, files, project documents, and projects. Require `read:compliance_user_data` / `delete:compliance_user_data` on a Compliance Access Key; Admin API keys cannot call these endpoints.

  > "Every successful delete is permanent and immediate. There is no recovery window."
  > "A project cannot be deleted while any chats remain attached to it."

  - *Implication*: Soft-deleted (user-deleted) chats remain visible via the API with `deleted_at` populated; Compliance API hard-deletes do not.
  - *Source*: [Retrieve and delete chats, files, and projects](https://platform.claude.com/docs/en/manage-claude/compliance-content-data.md)

- **Organization directory endpoints**: New endpoints enumerate organizations, users, roles, role permissions, groups, and group members across the entire Claude Enterprise parent/linked-organization tree. Require `read:compliance_org_data` or `read:compliance_user_data`.
  - *Source*: [List organizations, users, roles, and groups](https://platform.claude.com/docs/en/manage-claude/compliance-org-data.md)

- **Integration patterns guide**: New documentation covers two Activity Feed consumption patterns (window polling vs. cursor-driven incremental reads), SIEM correlation field mapping, and content retention planning.

  > "Treat the Activity Feed as **at-least-once**: a correctly paginated traversal returns every activity at least once, but a retry after a partial failure can re-deliver activities you already stored. Deduplicate on the activity `id` field."

  - *Source*: [Design your compliance integration](https://platform.claude.com/docs/en/manage-claude/compliance-integration-patterns.md)

- **Data retention addendum**: `api-and-data-retention.md` now explicitly states the Compliance API follows its own retention model:

  > "The Activity Feed retains data for 6 years. Chat, file, and project content from claude.ai follows your organization's retention policy, set in **claude.ai** > **Organization settings** > **Data and privacy**."

  - *Source*: [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention.md)

---

### Admin API

- **New dedicated Admin API page**: A standalone `admin-api.md` replaces the previously referenced `overview` page as the canonical entry point for the Admin API. The new page documents all Admin API resource families (organization members, invites, workspaces, workspace members, API keys), role definitions, the `/v1/organizations/me` endpoint, and key FAQs.

  > "The Admin API requires a special Admin API key (starting with `sk-ant-admin...`) that differs from standard API keys. Only organization members with the admin role can provision Admin API keys through the Claude Console."

  - *Implication*: All cross-links from `rate-limits-api.md`, `usage-cost-api.md`, `workspaces.md`, `data-residency.md`, and `claude-code-analytics-api.md` now resolve to `/docs/en/manage-claude/admin-api` instead of `/docs/en/manage-claude/overview`.
  - *Source*: [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api.md)

---

### Rate Limits

- **Example response values updated**: The sample JSON in `rate-limits-api.md` now shows higher token-per-minute values. These are documentation example values; the actual limits for an organization depend on its tier.

  | Limit type | Old example value | New example value |
  |---|---|---|
  | `input_tokens_per_minute` (org) | 2,000,000 | 10,000,000 |
  | `output_tokens_per_minute` (org) | 400,000 | 800,000 |
  | `input_tokens_per_minute` (org_limit in workspace example) | 2,000,000 | 10,000,000 |

  - *Source*: [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api.md)

---

### Workload Identity Federation — SPIFFE

- **Expanded to cover all SPIFFE-conformant issuers**: The SPIFFE guide title and intro changed from "SPIRE-issued workloads" to "SPIFFE workloads from SPIRE or any other SPIFFE-conformant issuer." The opening section now explains that Anthropic federates with any implementation emitting OIDC-compatible JWT-SVIDs, including commercial SPIFFE products.

  > "Anthropic additionally requires `iss` and `iat`, neither of which the JWT-SVID spec mandates, so configure your implementation to populate both."

  - *Implication*: Developers using commercial SPIFFE implementations (listed at [spiffe.io](https://spiffe.io/docs/latest/spiffe-about/overview/#commercial-software-that-implements-spiffe)) can now follow the same guide rather than treating it as SPIRE-only.
  - *Source*: [Use WIF with SPIFFE](https://platform.claude.com/docs/en/manage-claude/wif-providers/spiffe.md)

- **Direct SPIFFE Workload API callable integration added**: A second integration tab ("Callable via the SPIFFE Workload API") shows how to skip the spiffe-helper sidecar and pass a token-provider callable directly to the Anthropic SDK using `go-spiffe` (Go) or `py-spiffe` (Python), with the SDK invoking the callable before each token exchange to ensure a fresh JWT-SVID.
  - *Implication*: Go and Python workloads that link a SPIFFE Workload API client can eliminate the spiffe-helper sidecar. Other languages should fall back to the file-based approach via `ANTHROPIC_IDENTITY_TOKEN_FILE`.
  - *Source*: [Use WIF with SPIFFE](https://platform.claude.com/docs/en/manage-claude/wif-providers/spiffe.md)

- **SPIFFE card description updated**: The WIF provider card for SPIFFE on `workload-identity-federation.md` now reads "Workloads with SPIFFE JWT-SVIDs from SPIRE or another conformant issuer" (was "SPIRE-issued workloads using JWT-SVIDs and the OIDC Discovery Provider").
  - *Source*: [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation.md)

---

## New Pages

- **[admin-api.md]** — Comprehensive Admin API guide: organization roles/permissions, member management, invites, workspace management, API key management, `/v1/organizations/me` endpoint, and FAQ. [View](https://platform.claude.com/docs/en/manage-claude/admin-api.md)
- **[compliance-api.md]** — Compliance API overview: what the API covers, key-type comparison table, and links to each sub-guide. [View](https://platform.claude.com/docs/en/manage-claude/compliance-api.md)
- **[compliance-api-access.md]** — How to enable the Compliance API, create Compliance Access Keys and Admin API keys, choose scopes, inspect scope assignments, and rotate keys. [View](https://platform.claude.com/docs/en/manage-claude/compliance-api-access.md)
- **[compliance-activity-feed.md]** — Activity Feed filtering, pagination (cursor and page-token schemes), backfill loop patterns, and `Activity` object schema including the six `actor.type` discriminator values. [View](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed.md)
- **[compliance-content-data.md]** — Retrieving chat metadata and messages, downloading files and artifacts, listing projects and attachments, and permanently deleting content via `DELETE` endpoints. [View](https://platform.claude.com/docs/en/manage-claude/compliance-content-data.md)
- **[compliance-org-data.md]** — Listing organizations, users, roles, role permissions, groups, and group members across the Claude Enterprise parent/linked-org tree. [View](https://platform.claude.com/docs/en/manage-claude/compliance-org-data.md)
- **[compliance-integration-patterns.md]** — Window-polling vs. cursor-driven consumption patterns, SIEM correlation field mapping, delivery guarantees, and content retention planning. [View](https://platform.claude.com/docs/en/manage-claude/compliance-integration-patterns.md)
- **[compliance-errors.md]** — Compliance API error catalog: every 400, 401, 403, 404, 409, 429, and 5xx response with cause and fix. [View](https://platform.claude.com/docs/en/manage-claude/compliance-errors.md)
- **[compliance-faq.md]** — FAQ covering key types, scopes, availability, data coverage, and integration questions. [View](https://platform.claude.com/docs/en/manage-claude/compliance-faq.md)

---

## Notable Details

- **Admin API key prefix changed in docs**: The Compliance API access page shows Admin API keys as starting with `sk-ant-admin01-` (note the `01` suffix), while the Admin API page itself uses `sk-ant-admin...` without a version suffix. Developers should match on the `sk-ant-admin` prefix regardless of the numeric suffix.
- **Compliance API calls are self-auditing**: The Activity Feed emits `compliance_api_accessed` events for every Compliance API call, so security teams can detect unauthorized access to compliance data by filtering `actor.type: api_actor` and `actor.api_key_id`.
- **Admin API key timing matters for Compliance access**: Admin API keys created *before* the Compliance API was enabled for a Claude Console organization do NOT carry `read:compliance_activities`. They continue working with the Admin API but return 403 Forbidden on Activity Feed calls.
- **Claude Code Analytics API cross-link updated**: The "See also" section now references the Compliance API alongside the existing Admin API and Usage/Cost API links.
- **WIF reference doc updated**: Minor edits to the WIF reference page (+15/-13 lines), likely aligning validation rules and environment variable documentation with the expanded SPIFFE guide.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| manage-claude/admin-api.md | New | +248 | New dedicated Admin API guide replacing "overview" page |
| manage-claude/compliance-api.md | New | +111 | Compliance API overview |
| manage-claude/compliance-api-access.md | New | +181 | Key creation, scopes, enablement steps |
| manage-claude/compliance-activity-feed.md | New | +186 | Activity Feed filtering, pagination, object schema |
| manage-claude/compliance-content-data.md | New | ~+307 | Chat/file/project retrieval and deletion |
| manage-claude/compliance-errors.md | New | ~+295 | Full Compliance API error catalog |
| manage-claude/compliance-faq.md | New | ~+112 | Compliance API FAQ |
| manage-claude/compliance-integration-patterns.md | New | ~+163 | SIEM integration patterns and retention guidance |
| manage-claude/compliance-org-data.md | New | ~+218 | Org directory enumeration endpoints |
| manage-claude/wif-providers/spiffe.md | Modified | +35/-16 | Expanded to all SPIFFE issuers; added Workload API callable integration |
| manage-claude/wif-reference.md | Modified | +15/-13 | WIF reference updates (aligned with SPIFFE guide changes) |
| manage-claude/rate-limits-api.md | Modified | +5/-5 | Updated example token limit values; link to admin-api.md |
| manage-claude/claude-code-analytics-api.md | Modified | +3/-2 | Updated link to admin-api.md; added Compliance API cross-link |
| manage-claude/usage-cost-api.md | Modified | +2/-2 | Updated link to admin-api.md |
| manage-claude/api-and-data-retention.md | Modified | +2/-0 | Added Compliance API retention model note |
| manage-claude/workspaces.md | Modified | +2/-2 | Updated links to admin-api.md |
| manage-claude/data-residency.md | Modified | +1/-1 | Updated link to admin-api.md |
| manage-claude/workload-identity-federation.md | Modified | +1/-1 | Updated SPIFFE card description |

---

*Generated from Claude API documentation changes detected on 2026-05-09*
