# Claude API Documentation Changes — 2026-04-25

## Summary

Two new pages were added: a Rate Limits API guide (programmatic read access to organization and workspace rate limits) and a Claude on Amazon Bedrock (legacy) reference separating the older `InvokeModel`/`Converse` integration from the newer Messages API endpoint. Across 8 modified pages, the most notable pattern is the removal of beta header flags (`files-api-2025-04-14` and `skills-2025-10-02`) from all SDK examples, and the Java SDK version for cloud provider integrations was bumped from `2.20.0` to `2.27.0`.

---

## Significant Changes

### Admin API — Rate Limits API (new)

- **New `/v1/organizations/rate_limits` endpoint**: Programmatically read the rate limits configured for your organization. Returns rate limit groups (model groups, batch, files, token count, skills, web search) with their configured `requests_per_minute`, `input_tokens_per_minute`, and `output_tokens_per_minute` values.
  > "The Rate Limits API provides programmatic access to the rate limits configured for your organization and its workspaces. This is the same information shown on the Limits page in the Claude Console."
  - *Implication*: Gateways and proxies can now fetch live rate limits at startup instead of hardcoding values that drift when Anthropic adjusts them. Supports `?model=<model-id>` query to look up limits for a specific model, and `?group_type=` to filter by category.
  - *Source*: [Rate Limits API](https://platform.claude.com/docs/en/build-with-claude/rate-limits-api.md)

- **New `/v1/organizations/workspaces/{workspace_id}/rate_limits` endpoint**: Returns only the overrides configured for a specific workspace. Fields that are absent indicate the workspace inherits the organization-level limit.
  > "A group that is absent from `data` has no workspace override at all. The workspace inherits the organization-level limits for that group (it is not unlimited)."
  - *Implication*: Enables automation to verify that workspace limit overrides match provisioning expectations. The default workspace has no overrides and is not returned by this endpoint.
  - *Source*: [Rate Limits API](https://platform.claude.com/docs/en/build-with-claude/rate-limits-api.md)

- **Admin API key required**: Both endpoints require an Admin API key (`sk-ant-admin...`), not a standard API key.
  - *Source*: [Rate Limits API](https://platform.claude.com/docs/en/build-with-claude/rate-limits-api.md)

- **Administration API docs updated**: A new "Rate limits" section was added to the Administration API overview page, linking to the Rate Limits API guide.
  > "Read the rate limits configured for your organization and its workspaces with the Rate Limits API."
  - *Source*: [Administration API](https://platform.claude.com/docs/en/build-with-claude/administration-api.md)

### Amazon Bedrock — Legacy Integration Separated

- **New `claude-on-amazon-bedrock-legacy.md` page**: The legacy Bedrock integration (the `InvokeModel` and `Converse` APIs with ARN-versioned model identifiers) has been documented on a dedicated page, separate from the newer Messages API endpoint.
  > "This page covers the legacy Amazon Bedrock integration: the `InvokeModel` and `Converse` APIs with ARN-versioned model identifiers and AWS event-stream encoding."
  - *Implication*: The `claude-in-amazon-bedrock.md` page now exclusively covers the Messages API path (`/anthropic/v1/messages`). Links in that page pointing to `claude-on-amazon-bedrock` have been updated to `claude-on-amazon-bedrock-legacy`.
  - *Source*: [Claude on Amazon Bedrock (legacy)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy.md)

- The legacy page includes a note that Claude Opus 4.7 is reachable through `InvokeModel` on `bedrock-runtime` but does not have an ARN-versioned model ID, and therefore is omitted from the model ID table.

### SDKs — Beta Flags Removed (Files API and Skills API)

- **`files-api-2025-04-14` beta header no longer required**: Example code across `files.md`, `pdf-support.md`, `vision.md`, and `skills-guide.md` has had `betas: ["files-api-2025-04-14"]` removed from all Files API calls. Affected operations: `upload`, `list`, `retrieveMetadata`, `delete`, `download`.
  - *Implication*: The Files API beta flag is no longer needed in SDK calls. This applies to Python, TypeScript, C#, Go, Java, PHP, and Ruby SDKs.
  - *Source*: [Files API](https://platform.claude.com/docs/en/build-with-claude/files.md), [Vision](https://platform.claude.com/docs/en/build-with-claude/vision.md), [PDF Support](https://platform.claude.com/docs/en/build-with-claude/pdf-support.md), [Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide.md)

- **`skills-2025-10-02` beta header no longer required**: All Skills API example calls in `skills-guide.md` have had `betas: ["skills-2025-10-02"]` removed. Affected operations: `skills.create`, `skills.list`, `skills.retrieve`, `skills.delete`, `skills.versions.create`, `skills.versions.list`, `skills.versions.delete`.
  - *Implication*: Skills API calls no longer need the beta header across all supported SDKs.
  - *Source*: [Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide.md)

### SDKs — Java Version Bump

- **Java SDK updated to `2.27.0`** for all three cloud provider integrations (Bedrock, Foundry, Vertex AI). Previous version was `2.20.0`.
  - Packages affected: `com.anthropic:anthropic-java-bedrock`, `com.anthropic:anthropic-java-foundry`, `com.anthropic:anthropic-java-vertex`
  - *Source*: [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock.md), [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md), [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

---

## New Pages

- **`rate-limits-api.md`** — Guide to the new Rate Limits API (part of the Admin API). Covers organization-level and workspace-level endpoints, group types, model lookup by ID, filtering, and pagination. Read-only; updating limits requires the Claude Console. [View](https://platform.claude.com/docs/en/build-with-claude/rate-limits-api.md)

- **`claude-on-amazon-bedrock-legacy.md`** — Complete documentation for the legacy Amazon Bedrock integration: `InvokeModel`/`Converse` APIs with ARN-versioned model identifiers, bearer token authentication, global vs. regional endpoints, PDF support, and SDK examples across Python, TypeScript, C#, Go, Java, PHP, and Ruby. [View](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy.md)

---

## Notable Details

- The Rate Limits API `group_type` filter accepts six values: `model_group`, `batch`, `token_count`, `files`, `skills`, and `web_search` — confirming that rate limiting is applied per product area, not just per model.
- The workspace Rate Limits response includes an `org_limit` field alongside each overridden limiter value, making it straightforward to see the organizational ceiling without a separate request.
- The `usage-cost-api.md` page was updated to reference "Claude Console" (was "Anthropic Console") and now links to the new Rate Limits API in its "See also" section.
- The `workspaces.md` page now explicitly mentions the Rate Limits API alongside the existing link to the rate limits reference documentation.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| rate-limits-api.md | New | +177 | New Rate Limits API guide for programmatic limit reads |
| claude-on-amazon-bedrock-legacy.md | New | +970 | Legacy Bedrock integration (InvokeModel/Converse) separated from Messages API page |
| skills-guide.md | Modified | +68/-229 | Removed `skills-2025-10-02` and `files-api-2025-04-14` beta flags from all SDK examples |
| files.md | Modified | +12/-41 | Removed `files-api-2025-04-14` beta flags from all Files API SDK examples |
| administration-api.md | Modified | +4/-0 | Added "Rate limits" section linking to the new Rate Limits API |
| claude-in-amazon-bedrock.md | Modified | +3/-3 | Fixed legacy doc link; Java SDK bumped from 2.20.0 to 2.27.0 |
| claude-in-microsoft-foundry.md | Modified | +2/-2 | Java SDK bumped from 2.20.0 to 2.27.0 |
| claude-on-vertex-ai.md | Modified | +2/-2 | Java SDK bumped from 2.20.0 to 2.27.0 |
| vision.md | Modified | +2/-5 | Removed `files-api-2025-04-14` beta flag from image upload examples |
| usage-cost-api.md | Modified | +2/-1 | Added Rate Limits API cross-link; "Anthropic Console" → "Claude Console" |
| pdf-support.md | Modified | +1/-2 | Removed `files-api-2025-04-14` beta flag from TypeScript upload example |
| workspaces.md | Modified | +1/-1 | Added Rate Limits API mention to rate limits section |

---

*Generated from Claude API documentation changes detected on 2026-04-25*
