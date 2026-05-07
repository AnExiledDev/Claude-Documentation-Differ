# Claude API Documentation Changes — 2026-05-07

## Summary

Anthropic published a new `manage-claude` documentation section comprising 17 new pages. The additions cover a complete Admin API reference, Workload Identity Federation (WIF) for keyless authentication from cloud workloads, programmatic usage and cost reporting, Claude Code analytics, data residency controls, and workspace management — all backed by code examples across Python, TypeScript, Go, Java, C#, PHP, Ruby, and cURL.

---

## Significant Changes

### Authentication: Workload Identity Federation (WIF)

- **New authentication method — keyless OIDC federation**: The Claude API now supports Workload Identity Federation as an alternative to long-lived `sk-ant-api...` keys. A workload presents a signed JWT from its identity provider; Anthropic validates it against configured trust rules and returns a short-lived `sk-ant-oat01-...` access token. The SDKs refresh the token automatically before expiry.

  > "Workload Identity Federation (WIF) lets your workloads authenticate to the Claude API using short-lived OpenID Connect (OIDC) tokens issued by an identity provider (IdP) you already operate, such as AWS IAM, Google Cloud, or any standards-compliant OIDC issuer… instead of long-lived `sk-ant-...` API keys."

  - *Implication*: Production workloads on AWS, GCP, Azure, GitHub Actions, Kubernetes, SPIFFE, and Okta can now eliminate static API key distribution entirely.
  - *Source*: [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation.md)

- **Token exchange endpoint — `POST /v1/oauth/token`**: A new OAuth 2.0 endpoint accepts RFC 7523 `jwt-bearer` grant requests and returns a standard token response (`access_token`, `token_type`, `expires_in`, `scope`).

  > "The SDK posts the JWT to `POST /v1/oauth/token` using the RFC 7523 `jwt-bearer` grant. Anthropic verifies the signature against the JWKS you registered for the issuer… The response is a standard OAuth 2.0 token response with a short-lived `sk-ant-oat01-...` token."

  - *Implication*: Shell scripts and languages without SDK support can implement WIF using a direct cURL call to `/v1/oauth/token` followed by `Authorization: Bearer <token>` on subsequent Claude API requests.
  - *Source*: [WIF Reference](https://platform.claude.com/docs/en/manage-claude/wif-reference.md)

- **Three WIF primitives in the Claude Console**: Federation requires configuring a **service account** (`svac_...`), a **federation issuer** (`fdis_...`), and a **federation rule** (`fdrl_...`) under Settings → Workload identity.

  > "You configure three resources in the Claude Console before any workload can federate. Together they express 'tokens signed by issuer X, with claims that look like Y, may act as service account Z.'"

  - *Implication*: The rule system supports `subject_prefix`, `audience`, exact `claims` matching, and [CEL](https://cel.dev/) expressions for complex conditions, giving teams fine-grained per-workload access control.
  - *Source*: [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation.md)

- **SDK-level WIF support across all official SDKs**: All eight official SDKs (Python, TypeScript, Go, Java, C#, PHP, Ruby, CLI) now have WIF credential classes. Environment-variable-driven configuration (`ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, `ANTHROPIC_IDENTITY_TOKEN_FILE`) allows zero-code-change deployment across environments.

  > "Ship the same container image everywhere and inject `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, `ANTHROPIC_WORKSPACE_ID`, and `ANTHROPIC_IDENTITY_TOKEN_FILE` per environment."

  - *Implication*: Developers migrating from API keys unset `ANTHROPIC_API_KEY` (which takes precedence over federation in the credential chain) and inject the five federation variables instead — no code changes required.
  - *Source*: [Authentication](https://platform.claude.com/docs/en/manage-claude/authentication.md)

- **Credential precedence order documented**: The SDK resolves credentials in a fixed five-tier order: constructor argument → `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN` → `ANTHROPIC_PROFILE` → federation environment variables → active profile.

  > "`ANTHROPIC_API_KEY` sits above the federation tiers, so a leftover key in the environment silently shadows federation. When migrating a workload from API keys to Workload Identity Federation, confirm `ANTHROPIC_API_KEY` is unset everywhere that workload runs."

  - *Implication*: Teams debugging WIF failures should verify that no API key variable is set in the environment, CI secrets, or shell profiles.
  - *Source*: [WIF Reference](https://platform.claude.com/docs/en/manage-claude/wif-reference.md)

- **Token lifetime and advisory refresh schedule**: Minted Anthropic tokens default to 3600-second lifetimes (configurable 60–86400 seconds per rule). The SDK refreshes at expiry − 120 s (advisory) and expiry − 30 s (mandatory).
  - *Source*: [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation.md)

- **OAuth scope `workspace:developer`**: At launch, the only available scope grants access to all non-administrative Claude API endpoints in the rule's workspace — Messages (including streaming and token counting), Models, Managed Agents, Files, and Skills.
  - *Source*: [WIF Reference](https://platform.claude.com/docs/en/manage-claude/wif-reference.md)

### Admin API

- **New `GET /v1/organizations/me` endpoint**: Returns the organization ID, type, and name for a given Admin API key — useful for programmatically determining which organization a key belongs to.
  - *Source*: [Admin API Overview](https://platform.claude.com/docs/en/manage-claude/overview.md)

- **Admin API key format documented**: Admin API keys begin with `sk-ant-admin...` and are distinct from standard API keys. Only organization members with the `admin` role can provision them through the Claude Console.

  > "The Admin API requires a special Admin API key (starting with `sk-ant-admin...`) that differs from standard API keys."

  - *Source*: [Admin API Overview](https://platform.claude.com/docs/en/manage-claude/overview.md)

- **Five organization roles listed**: `user`, `claude_code_user`, `developer`, `billing`, and `admin`. The `claude_code_user` role is new — it enables Workbench and [Claude Code](https://code.claude.com/) access.
  - *Source*: [Admin API Overview](https://platform.claude.com/docs/en/manage-claude/overview.md)

### Usage and Cost Reporting

- **New Usage API — `GET /v1/organizations/usage_report/messages`**: Provides token-level consumption data broken down by model, workspace, API key, service tier, context window, inference geo, and fast mode. Supports `1m`, `1h`, and `1d` time buckets.

  > "Track token consumption across your organization with detailed breakdowns by model, workspace, and service tier."

  - *Implication*: Teams can build cost attribution dashboards, track cache efficiency, and power alerting without relying on Console screenshots.
  - *Source*: [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api.md)

- **New Cost API — `GET /v1/organizations/cost_report`**: Returns USD cost breakdowns at daily granularity, with grouping by workspace or `description`. Covers token, web search, and code execution costs. Priority Tier costs are excluded (use the usage endpoint instead).
  - *Source*: [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api.md)

- **Fast mode (beta) trackable via usage API**: Usage filtered/grouped by `speed` dimension requires the `anthropic-beta: fast-mode-2026-02-01` header. Valid speed values are `standard` and `fast`.
  - *Source*: [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api.md)

- **Inference geo dimension in usage data**: The `inference_geo` dimension can be used to group or filter usage by geographic routing. Models released before Claude Opus 4.6 return `"not_available"` for this dimension.
  - *Source*: [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api.md)

### Claude Code Analytics

- **New Claude Code Analytics API — `GET /v1/organizations/usage_report/claude_code`**: Returns daily, per-user aggregated metrics including sessions, lines of code added/removed, commits, pull requests, tool acceptance/rejection rates (Edit, Write, NotebookEdit), and per-model token and cost breakdowns.

  > "The Claude Code Analytics Admin API provides programmatic access to daily aggregated usage metrics for Claude Code users, enabling organizations to analyze developer productivity and build custom dashboards."

  - *Implication*: Org admins can build custom dashboards, compare Claude Code against other AI coding tools, and justify adoption internally — without relying solely on the Console Analytics tab.
  - *Source*: [Claude Code Analytics API](https://platform.claude.com/docs/en/manage-claude/claude-code-analytics-api.md)

- **Actor field distinguishes user vs. API key sessions**: The `actor` field contains either a `user_actor` (with `email_address`) for OAuth-authenticated users or an `api_actor` (with `api_key_name`) for API key sessions.
  - *Source*: [Claude Code Analytics API](https://platform.claude.com/docs/en/manage-claude/claude-code-analytics-api.md)

### Rate Limits API

- **New Rate Limits API**: Two new endpoints programmatically expose configured rate limits:
  - `GET /v1/organizations/rate_limits` — organization-level limits, filterable by model string or `group_type`
  - `GET /v1/organizations/workspaces/{workspace_id}/rate_limits` — workspace-level overrides (absent groups inherit from the organization)

  > "Keep gateways and proxies in sync: Read your current limits at startup and on a schedule instead of hardcoding values that drift when Anthropic adjusts them."

  - *Implication*: Automated infrastructure can self-configure rate limiting at startup and detect when limits change without a human checking the Console.
  - *Source*: [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api.md)

- **`group_type` filter values**: `model_group`, `batch`, `token_count`, `files`, `skills`, `web_search`.
  - *Source*: [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api.md)

### Data Residency

- **`inference_geo` parameter on `POST /v1/messages`**: Accepted values are `"us"` (US-only inference) and `"global"` (default, any available region). The response `usage` object echoes the actual `inference_geo` value where inference ran. Supported on Claude Opus 4.6 and newer; older models return 400.

  > "The `inference_geo` parameter controls where model inference runs for a specific API request."

  - *Implication*: Request-level geo control replaces the previous organization-wide opt-out, enabling per-request routing decisions without changing workspace config.
  - *Source*: [Data Residency](https://platform.claude.com/docs/en/manage-claude/data-residency.md)

- **US-only inference pricing**: Claude Opus 4.6 and newer: `inference_geo: "us"` is priced at **1.1× the standard rate** across all token categories (input, output, cache write, cache read). Global routing retains standard pricing.
  - *Implication*: Priority Tier customers: the 1.1× multiplier also affects how tokens draw down committed TPM capacity.
  - *Source*: [Data Residency](https://platform.claude.com/docs/en/manage-claude/data-residency.md)

- **Workspace-level inference geo controls**: Workspaces now support `allowed_inference_geos` (restricts which geos keys in that workspace may use) and `default_inference_geo` (fallback when a request omits `inference_geo`). Legacy US-only opt-outs were automatically migrated to `allowed_inference_geos: ["us"]`, `default_inference_geo: "us"`.
  - *Source*: [Data Residency](https://platform.claude.com/docs/en/manage-claude/data-residency.md)

- **Batch API supports `inference_geo`**: Each request in a batch can specify its own geo value independently.
  - *Source*: [Data Residency](https://platform.claude.com/docs/en/manage-claude/data-residency.md)

### Workspaces

- **Workspace identifiers documented**: Workspaces use the `wrkspc_` prefix (e.g., `wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ`). Maximum 100 workspaces per organization; archived workspaces don't count.
- **`Workspace Limited Developer` role added**: A new workspace role that allows creating/managing API keys and using the API, but blocks session tracing views and file downloads.
- **Prompt cache isolation coming**: Starting February 5, 2026, prompt caches will be isolated per workspace (Claude API and Azure only).
- **Admin API endpoints for workspaces**: `POST /v1/organizations/workspaces`, list with `include_archived` filter, `POST /v1/organizations/workspaces/{id}/archive`, and member management.
  - *Source*: [Workspaces](https://platform.claude.com/docs/en/manage-claude/workspaces.md)

### API and Data Retention

- **Comprehensive ZDR and HIPAA feature eligibility table**: A new reference table maps every Claude API feature (35+ features) to its ZDR and HIPAA eligibility status. Notable designations:
  - **Not ZDR/HIPAA eligible**: Batch processing (29-day retention), Files API (until deleted), Code execution (up to 30 days), MCP connector, Agent skills
  - **HIPAA-eligible but not ZDR**: Web fetch, Computer use is not HIPAA-eligible
  - **ZDR qualified** (minimal technical data retained): Structured outputs (JSON schema cached up to 24 hours)
  - *Source*: [API and Data Retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention.md)

- **HIPAA-ready API access now separate from ZDR**: Organizations can now have HIPAA-ready API access without requiring ZDR. A signed BAA and a dedicated HIPAA-enabled organization are required. The API automatically blocks non-eligible features with a `400 invalid_request_error`.

  > "HIPAA-ready API access removes this requirement [for ZDR] and provides a foundation for Anthropic to progressively enable additional features as they are audited for HIPAA readiness."

  - *Implication*: Healthcare organizations can use more API features (e.g., prompt caching, fast mode, extended thinking) under HIPAA controls than were previously available under a ZDR-only arrangement.
  - *Source*: [API and Data Retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention.md)

- **PHI restriction in JSON schemas**: For HIPAA-enabled organizations using structured outputs or tools with `strict: true`, JSON schema definitions (property names, `enum` values, `const` values, `pattern` regexes) must not contain PHI. These schemas are cached separately and are not covered by HIPAA safeguards.
  - *Source*: [API and Data Retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention.md)

---

## New Pages

- **[overview.md](https://platform.claude.com/docs/en/manage-claude/overview.md)** — Admin API overview: organization members, invites, workspace management, and API key management via the Admin API (`/v1/organizations/*`).

- **[authentication.md](https://platform.claude.com/docs/en/manage-claude/authentication.md)** — Unified authentication reference comparing API keys vs. Workload Identity Federation with SDK examples for all eight SDKs.

- **[workload-identity-federation.md](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation.md)** — Full WIF setup walkthrough: concepts (service accounts, issuers, rules), token exchange flow, SDK credential construction, credential precedence, migration from API keys, and token refresh schedule.

- **[wif-reference.md](https://platform.claude.com/docs/en/manage-claude/wif-reference.md)** — WIF technical reference: token exchange request/response schemas, all environment variables, credential precedence table, profile configuration file format, OAuth scopes, validation constraints, JWT verification rules, rule matching semantics (including CEL), JWKS source modes, key rotation caching, and error codes.

- **[wif-providers/aws.md](https://platform.claude.com/docs/en/manage-claude/wif-providers/aws.md)** — AWS-specific WIF guide: STS `GetWebIdentityToken` path (Lambda, EC2, ECS, EKS) and EKS projected service-account token path, with SDK examples.

- **[wif-providers/gcp.md](https://platform.claude.com/docs/en/manage-claude/wif-providers/gcp.md)** — Google Cloud WIF guide: identity tokens via the GCP metadata server.

- **[wif-providers/azure.md](https://platform.claude.com/docs/en/manage-claude/wif-providers/azure.md)** — Azure WIF guide: Managed Identity (IMDS) and Entra Workload ID on AKS.

- **[wif-providers/github-actions.md](https://platform.claude.com/docs/en/manage-claude/wif-providers/github-actions.md)** — GitHub Actions WIF guide: keyless CI authentication with the Actions OIDC token.

- **[wif-providers/kubernetes.md](https://platform.claude.com/docs/en/manage-claude/wif-providers/kubernetes.md)** — Kubernetes WIF guide: projected service-account tokens for self-managed and on-premises clusters.

- **[wif-providers/spiffe.md](https://platform.claude.com/docs/en/manage-claude/wif-providers/spiffe.md)** — SPIFFE/SPIRE WIF guide: JWT-SVIDs via the OIDC Discovery Provider.

- **[wif-providers/okta.md](https://platform.claude.com/docs/en/manage-claude/wif-providers/okta.md)** — Okta WIF guide: service applications using client-credentials flow.

- **[usage-cost-api.md](https://platform.claude.com/docs/en/manage-claude/usage-cost-api.md)** — Usage and Cost Admin API: token consumption by model/workspace/service tier/geo/speed, USD cost breakdowns, pagination, and partner integrations (CloudZero, Datadog, Grafana, Honeycomb, Vantage).

- **[rate-limits-api.md](https://platform.claude.com/docs/en/manage-claude/rate-limits-api.md)** — Rate Limits Admin API: read organization and workspace rate limits, filter by model or group type.

- **[claude-code-analytics-api.md](https://platform.claude.com/docs/en/manage-claude/claude-code-analytics-api.md)** — Claude Code Analytics Admin API: daily per-user productivity metrics, tool acceptance rates, per-model token and cost breakdown.

- **[data-residency.md](https://platform.claude.com/docs/en/manage-claude/data-residency.md)** — Data residency controls: `inference_geo` parameter, workspace-level allowed/default geo settings, pricing (1.1× for US-only on Opus 4.6+), Batch API support, and legacy opt-out migration guidance.

- **[workspaces.md](https://platform.claude.com/docs/en/manage-claude/workspaces.md)** — Workspace management: roles and permissions, Console and Admin API workflows, resource scoping, spend and rate limits, and usage tracking.

- **[api-and-data-retention.md](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention.md)** — ZDR and HIPAA readiness reference: feature eligibility table for 35+ API features, HIPAA-ready API access setup, PHI handling guidelines for JSON schemas, and CORS limitations.

---

## Migration Guidance

### Migrating from API keys to Workload Identity Federation

For workloads already using API keys, the WIF documentation recommends a parallel cutover:

1. Configure federation (service account, issuer, rule) while leaving `ANTHROPIC_API_KEY` in place.
2. Smoke-test with `ant auth status` — the API key still wins at this stage due to credential precedence.
3. Remove `ANTHROPIC_API_KEY` from all injection points (CI secrets, container env, shell profiles).
4. Confirm `ant auth status` shows the federation source; then revoke the old API key in the Console.

### Legacy US inference opt-outs (data residency)

Organizations that previously opted out of global routing have been automatically migrated:

| Legacy setting | New equivalent |
|:---|:---|
| Global routing opt-out (US-only) | `allowed_inference_geos: ["us"]`, `default_inference_geo: "us"` |

No code changes are required. Existing requests continue running on US infrastructure.

---

## Notable Details

- **`ANTHROPIC_API_KEY=""` (empty string) still wins precedence**: An exported variable set to an empty string occupies its precedence slot. Developers must use `unset ANTHROPIC_API_KEY`, not `ANTHROPIC_API_KEY=""`, when migrating to WIF.
- **JWT size limit**: The `assertion` JWT passed to `/v1/oauth/token` must be ≤ 16 KiB.
- **Supported JWT signing algorithms**: Only asymmetric algorithms (RSA and ECDSA: ES256, ES384, RS256, RS384, PS256, PS384). HMAC (`HS256`, etc.) and `none` are rejected.
- **Clock skew tolerance**: 30-second leeway applied to `exp`, `nbf`, and `iat` during JWT verification.
- **JWKS key rotation cache**: In `discovery` and `explicit_url` modes, Anthropic caches the JWKS; exchanges can fail for up to one minute after a provider rotates its signing key. Best practice: publish new keys at least 15 minutes before first use.
- **`inline` JWKS mode requires manual rotation**: There is no automatic key refresh in `inline` mode; operators must update the issuer configuration when the IdP rotates keys.
- **Default Workspace has no ID**: It returns `null` for `workspace_id` in all API responses and cannot have rate limit overrides set on the workspace endpoint.
- **`inference_geo` not available on the OpenAI-compatible endpoint** (`/v1/messages` via OpenAI SDK compatibility layer) or on third-party platforms (AWS Bedrock, Google Vertex AI).
- **Claude Code WIF profile interop**: A federation profile in `~/.config/anthropic/configs/<name>.json` is honored by Claude Code and the Claude Agent SDK without additional setup.
- **`ant auth status` CLI command**: Described as a diagnostic tool for checking which credential source won in the precedence chain — useful when debugging WIF configuration.

---

## Changes by Page

| Page | Type | Summary |
|------|------|---------|
| manage-claude/overview.md | New | Admin API overview: members, invites, workspaces, API keys, org info endpoint |
| manage-claude/authentication.md | New | API key vs. WIF authentication reference with SDK examples |
| manage-claude/workload-identity-federation.md | New | Complete WIF setup guide, token flow, SDK examples, migration from API keys |
| manage-claude/wif-reference.md | New | WIF technical reference: env vars, profile schema, scopes, validation, errors |
| manage-claude/wif-providers/aws.md | New | AWS STS and EKS projected-token WIF integration guide |
| manage-claude/wif-providers/gcp.md | New | Google Cloud metadata server WIF integration guide |
| manage-claude/wif-providers/azure.md | New | Azure Managed Identity and Entra Workload ID integration guide |
| manage-claude/wif-providers/github-actions.md | New | GitHub Actions OIDC keyless CI integration guide |
| manage-claude/wif-providers/kubernetes.md | New | Kubernetes projected service-account token integration guide |
| manage-claude/wif-providers/spiffe.md | New | SPIFFE/SPIRE JWT-SVID integration guide |
| manage-claude/wif-providers/okta.md | New | Okta client-credentials WIF integration guide |
| manage-claude/usage-cost-api.md | New | Usage and Cost Admin API with filtering, grouping, pagination |
| manage-claude/rate-limits-api.md | New | Rate Limits Admin API for org and workspace limits |
| manage-claude/claude-code-analytics-api.md | New | Claude Code Analytics Admin API: per-user daily productivity metrics |
| manage-claude/data-residency.md | New | `inference_geo` parameter, workspace geo controls, pricing, Batch API support |
| manage-claude/workspaces.md | New | Workspace management: roles, limits, API, resource scoping |
| manage-claude/api-and-data-retention.md | New | ZDR and HIPAA eligibility table for 35+ API features |

---

*Generated from Claude API documentation changes detected on 2026-05-07*
