# Claude API Documentation Changes — 2026-05-19

## Summary

This update is focused entirely on the Compliance API documentation. The most substantive changes are: (1) Compliance API access is no longer self-service — organizations on either plan must now contact their Anthropic representative; (2) the rate limit model has been clarified and expanded from a per-key budget to a shared per-parent-organization budget with full header documentation; and (3) two new organization-membership activity types are documented. There are also minor deprecation and schema cleanup items across several pages.

---

## Significant Changes

### Compliance API — Access and Enablement

- **Compliance API access is now request-based, not self-service**: The enablement flow has changed. Previously, claude.ai Enterprise primary owners could click **Enable** in Organization settings to activate the Compliance API themselves. The docs now state that all organizations must contact their Anthropic representative to request access. After Anthropic enables it, the **Compliance access keys** section appears in the Settings UI.
  > "Contact your Anthropic representative to request access. Enablement happens at the parent organization level and cascades to every linked organization, both claude.ai and Claude Console."
  - *Implication*: Organizations that had expected a self-service path to activate the Compliance API will now need to go through Anthropic. This affects the provisioning timeline for new integrations.
  - *Source*: [Get access to the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access.md)

- **Claude Console organizations now have documented Compliance API access (Activity Feed only)**: The previous note said the Compliance API was "available only on the Claude Enterprise plan." This note is updated across every Compliance API page. Claude Console organizations can access the Activity Feed endpoint (with Admin API keys), but not the chat/file/project content endpoints.
  > "The Compliance API is enabled on request. Claude Enterprise organizations have access to the full API; Claude Console organizations have access to the Activity Feed only."
  - *Implication*: Claude Console customers can now formally use the Compliance API for Activity Feed queries. The access model is tiered by organization type, not just plan tier.
  - *Source*: [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api.md)

- **Admin API key scope guidance clarified for pre/post enablement**: The docs now explicitly note that Admin API keys created before enablement lack `read:compliance_activities`, and directs users to create a new key to pick up the scope.
  > "Admin API keys created from then on carry the `read:compliance_activities` scope. Admin API keys created before enablement continue to work with the Admin API, but calling the Activity Feed with one returns 403 Forbidden; create a new Admin API key to pick up the scope."
  - *Implication*: Developers who enabled Compliance API access but are using a pre-existing Admin API key and seeing 403 errors should create a new Admin API key.
  - *Source*: [Get access to the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access.md)

- **Key leak recovery guidance improved**: The instructions for handling a compromised Compliance Access Key now include a specific query strategy: use `activity_types[]=compliance_api_accessed` to scope the Activity Feed query, then filter client-side by `actor.type == api_actor` and `actor.api_key_id`.
  - *Source*: [Get access to the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access.md)

### Compliance API — Rate Limits

- **Rate limit scope changed from per-key to per parent organization**: The 429 Too Many Requests documentation has been substantially expanded. The 600 requests/minute limit is now described as a single budget shared across all keys, all linked organizations, and all `/v1/compliance/*` endpoints under a single parent organization.
  > "Requests to the Compliance API are limited to **600 requests per minute per parent organization**. The limit is a single budget shared across every key under the parent (Compliance Access Keys and the Admin API keys of all linked organizations) and across every `/v1/compliance/*` endpoint."
  - *Implication*: Multi-tenant integrations or organizations with multiple linked Claude Console organizations share a single request budget. High-volume workers across multiple keys can collectively exhaust the limit.
  - *Source*: [Compliance API errors](https://platform.claude.com/docs/en/manage-claude/compliance-errors.md)

- **Rate limit response headers now documented**: Three proactive throttling headers and a `retry-after` header are now documented for Compliance API responses.
  > "Every Compliance API response includes the standard rate-limit response headers so your client can throttle proactively instead of waiting for a 429:
  > - `anthropic-ratelimit-requests-limit` is your parent organization's per-minute request budget.
  > - `anthropic-ratelimit-requests-remaining` is the budget left in the current window.
  > - `anthropic-ratelimit-requests-reset` is the RFC 3339 timestamp when the window resets.
  > A 429 response also carries a `retry-after` header with the number of seconds to wait."
  - *Implication*: Clients should read `anthropic-ratelimit-requests-remaining` on every response to slow down before hitting the ceiling, rather than reacting to 429s. The `retry-after` header should be honored over exponential backoff when present.
  - *Source*: [Compliance API errors](https://platform.claude.com/docs/en/manage-claude/compliance-errors.md)

- **Quota consumption clarified for auth vs. scope failures**: Failed authentication (missing or invalid key) does not consume quota. A valid key that calls an endpoint it lacks scope for does consume one quota unit before the 403 is returned.
  - *Source*: [Compliance API errors](https://platform.claude.com/docs/en/manage-claude/compliance-errors.md)

- **429 retry guidance updated**: The table entry for 429 changed from "Yes, with backoff" to "Yes, after `retry-after`", and the fix instruction now says to wait the `retry-after` seconds, falling back to exponential backoff only if that header is absent.
  - *Source*: [Compliance API errors](https://platform.claude.com/docs/en/manage-claude/compliance-errors.md)

### Compliance API — Organization Data and Activity Types

- **Two new organization-membership activity types documented**: `org_parent_join_proposal_created` and `org_join_proposal_decided` are added alongside the existing `org_deletion_requested` and `org_deleted_via_bulk`. The previous note stating "there is currently no activity type for an organization being created or joining the tree" has been removed.
  > "The Activity Feed also surfaces membership events through the `org_deletion_requested`, `org_deleted_via_bulk`, `org_parent_join_proposal_created`, and `org_join_proposal_decided` activity types."
  - *Implication*: Integrations that poll the organizations endpoint on a schedule to detect newly linked organizations can now supplement or replace polling by watching for these join-proposal activity types.
  - *Source*: [Compliance API org data](https://platform.claude.com/docs/en/manage-claude/compliance-org-data.md)

- **`organization_id` field deprecated on chat and project records**: The `organization_id` field is now described as deprecated on chat and project records, directing developers to use `organization_uuid` instead. In the `compliance-content-data.md` example responses, the `organization_id` field has been removed from the JSON samples.
  > "`organization_id` | Activity Feed, chat, and project records | Same organization, `org_`-prefixed. Deprecated on chat and project records; use `organization_uuid` instead."
  - *Implication*: Clients parsing chat or project responses that key on `organization_id` should migrate to `organization_uuid`. The field is present in the field-reference table but removed from example payloads.
  - *Source*: [Compliance API org data](https://platform.claude.com/docs/en/manage-claude/compliance-org-data.md)

### Compliance API — Integration Patterns

- **Rate limit constraint added to integration patterns constraints list**: The 600 req/min per parent organization limit is now listed alongside pagination and cursor constraints in the "Choose a feed consumption pattern" section, with a link to the error-handling guidance.
  - *Source*: [Design your compliance integration](https://platform.claude.com/docs/en/manage-claude/compliance-integration-patterns.md)

- **`compliance_api_accessed` query guidance updated**: The SIEM correlation section now recommends passing `activity_types[]=compliance_api_accessed` as a query parameter to scope the request, rather than filtering after fetching.
  - *Source*: [Design your compliance integration](https://platform.claude.com/docs/en/manage-claude/compliance-integration-patterns.md)

### Compliance API — Overview

- **Rate limit added to API overview**: The overview (`compliance-api.md`) now explicitly states the 600 req/min per-parent-organization rate limit under "How the Compliance API works."
  > "All `/v1/compliance/*` endpoints share a single rate limit of 600 requests per minute per parent organization."
  - *Source*: [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api.md)

- **Key-type comparison table removed from overview page**: The inline table listing Compliance Access Key vs. Admin API key was removed from `compliance-api.md` and is now only in `compliance-api-access.md`. The note now points to [Which key do you need?](https://platform.claude.com/docs/en/manage-claude/compliance-api-access.md#which-key-do-you-need) instead.
  - *Source*: [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api.md)

### Activity Feed Terminology

- **"parsers" renamed to "handlers" in forward-compatibility note**: The advisory note about building forward-compatible integrations changed "parsers" to "handlers" throughout.
  > "**Build forward-compatible handlers.** Pass through unrecognized `type` and `actor.type` values, and ignore fields your handler does not expect."
  - *Source*: [Query the Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed.md)

---

## Minor Changes

- **api-and-data-retention.md**: Added **Cache diagnostics** to the feature eligibility table. It is ZDR-qualified (a fingerprint of cryptographic hashes and token-count estimates is retained briefly) but not HIPAA eligible. The link to claude.ai Organization settings was converted to a direct URL (`https://claude.ai/admin-settings/data-privacy-controls`). (+2/-1)

- **data-residency.md**: Removed the note stating that workspace-level inference geography controls (`allowed_inference_geos` and `default_inference_geo`) are not available on Claude Platform on AWS. The advice to use the per-request `inference_geo` parameter instead is no longer documented on this page. (+0/-4)

- **compliance-api-access.md / compliance-api.md / compliance-faq.md**: Plain-text UI navigation paths (e.g., **claude.ai > Organization settings > Data and privacy**) have been converted to hyperlinks pointing to their actual URLs (e.g., `https://claude.ai/admin-settings/data-privacy-controls`, `https://platform.claude.com/settings/admin-keys`, `https://claude.ai/analytics/api-keys`).

---

## Migration Notes

- **Compliance API enablement is no longer self-service**: If your deployment plan assumed a primary owner could self-activate the Compliance API by clicking Enable in claude.ai settings, that path is removed. Contact your Anthropic representative to request activation before proceeding with key creation.

- **`organization_id` deprecated on chat and project records**: Update parsers that use `organization_id` from chat/project API responses to use `organization_uuid` instead. The `org_`-prefixed form is still present in Activity Feed records, but `organization_uuid` is now the canonical join key across all Compliance API data.

- **Rate limit is per parent organization, not per key**: If you run multiple workers or keys in parallel under the same parent organization, they share the 600 req/min budget. Redesign throughput planning to account for aggregate consumption. Monitor `anthropic-ratelimit-requests-remaining` across all workers.

---

## Notable Details

- The compliance-content-data page now carries **two** availability notes: the general one (Compliance API is enabled on request; Console orgs get Activity Feed only) plus a second note specific to the chat/file/project endpoints clarifying that those endpoints are **Enterprise-only** because they serve claude.ai content.
- The parent organization warning in `compliance-api-access.md` was extended: "The parent carries no workloads, no Claude API keys, **and no Admin API keys**." The addition of Admin API keys is noteworthy — it confirms Admin API keys are created at the linked Console organization level, not the parent.
- The 429 error message itself has changed: the new documented string includes the rate limit value, the retry instruction, and a prompt to include `request-id` when contacting support — useful for instrumentation and support workflows.

---

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| compliance-api-access.md | Modified | SIGNIFICANT | +19/-19 | Enablement renamed to "Request access"; now requires contacting Anthropic rep; links converted to URLs |
| compliance-errors.md | Modified | SIGNIFICANT | +28/-9 | 429 section expanded: per-org rate limit, response headers, retry-after, new activity types |
| compliance-api.md | Modified | SIGNIFICANT | +12/-13 | Rate limit added to overview; key table removed; How it Works section restructured |
| compliance-activity-feed.md | Modified | SIGNIFICANT | +9/-3 | Availability note updated; Console org access documented; "parsers" → "handlers" |
| compliance-content-data.md | Modified | SIGNIFICANT | +7/-3 | Two availability notes; `organization_id` removed from JSON examples |
| compliance-org-data.md | Modified | SIGNIFICANT | +4/-4 | `organization_id` deprecated on chat/project; two new org-membership activity types added |
| compliance-faq.md | Modified | SIGNIFICANT | +3/-3 | Availability note updated; sandbox setup reflects contact-Anthropic flow; link converted to URL |
| compliance-integration-patterns.md | Modified | SIGNIFICANT | +3/-2 | Rate limit constraint added; `compliance_api_accessed` query pattern updated |
| api-and-data-retention.md | Modified | MINOR | +2/-1 | Cache diagnostics row added to eligibility table; settings link converted to URL |
| data-residency.md | Modified | MINOR | +0/-4 | Removed note about Claude Platform on AWS workspace-level inference geo controls |

---
*Generated from Claude API documentation changes detected on 2026-05-19*
