# Claude API Documentation Changes — 2026-05-13

## Summary

All six modified pages are in the `manage-claude` section and share a common theme: documenting the capabilities and limitations of **Claude Platform on AWS** alongside the existing first-party Claude API. Additional changes clarify which models support the `inference_geo` parameter (now explicitly including Claude Sonnet 4.6), add a new `MultiEdit` tool metric to the Claude Code Analytics API, and update prompt cache isolation to reflect that it is now active and available on more platforms.

## Significant Changes

### Claude Platform on AWS — Availability Documentation

A coordinated set of notes was added across multiple admin/management pages to define what is and is not supported on Claude Platform on AWS.

- **Admin API availability on Claude Platform on AWS**: Most Admin API endpoints are unavailable. Only workspace endpoints (`/v1/organizations/workspaces` — create, get, list, update, archive) are accessible; organization members, workspace members, invites, API keys, usage reports, cost reports, and rate limit reports are not.
  > **Claude Platform on AWS:** Most of the Admin API is not available on Claude Platform on AWS. Workspace endpoints (create, get, list, update, and archive on `/v1/organizations/workspaces`) are available. Other endpoints including organization members, workspace members, invites, API keys, usage reports, cost reports, and rate limit reports are not available.
  - *Implication*: Organizations using Claude Platform on AWS cannot automate user/key/invite management via the Admin API; only workspace-level operations are supported.
  - *Source*: [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api.md)

- **Claude Code Analytics API unavailable on Claude Platform on AWS**: The analytics API endpoints are not currently accessible; the Console Usage page is the recommended alternative.
  > **Claude Platform on AWS:** The Claude Code Analytics API is not currently available. View Claude Code usage on the **Usage** page in the Claude Console instead.
  - *Source*: [Claude Code Analytics API](https://platform.claude.com/docs/en/manage-claude/claude-code-analytics-api.md)

- **Usage and Cost API unavailable on Claude Platform on AWS**: Programmatic usage/cost endpoints are not available; the Console pages are the fallback.
  > **Claude Platform on AWS:** The programmatic Usage and Cost API endpoints are not currently available. View usage and cost data on the **Usage** and **Cost** pages in the Claude Console instead.
  - *Source*: [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api.md)

- **Inference geo on Claude Platform on AWS**: The `inference_geo` per-request parameter is now documented as supported on Claude Platform on AWS. However, workspace-level controls (`allowed_inference_geos` and `default_inference_geo`) are not available — developers must use per-request `inference_geo` instead.
  > The `inference_geo` parameter is available on the Claude API (first-party) and [Claude Platform on AWS]. On Amazon Bedrock, Vertex AI, and Microsoft Foundry, the inference region is determined by the endpoint URL or inference profile, so `inference_geo` is not applicable.
  - *Implication*: Claude Platform on AWS users can control inference geography per-request but cannot set workspace-level defaults or restrictions.
  - *Source*: [Data Residency](https://platform.claude.com/docs/en/manage-claude/data-residency.md)

- **Workspace geo not configurable on Claude Platform on AWS**: Workspaces are provisioned through AWS Console; the Claude Console Workspaces page is read-only. Claude Managed Agents sessions run with an effective workspace geo of `"us"`.
  > **Claude Platform on AWS:** Workspace geo is not configurable. Workspaces are provisioned through the AWS Console, and the Claude Console Workspaces page is read-only. Claude Managed Agents sessions on this platform run with an effective Workspace geo of `"us"`, which is currently the only available workspace geo.
  - *Source*: [Data Residency](https://platform.claude.com/docs/en/manage-claude/data-residency.md)

---

### HIPAA and ZDR — Claude Platform on AWS and Platform Clarifications

- **HIPAA readiness not available on Claude Platform on AWS or Microsoft Foundry**: Previously, documentation listed only third-party platforms (Bedrock, Vertex AI) as outside HIPAA scope. The updated text explicitly adds Claude Platform on AWS and Microsoft Foundry.
  > - **Partner-operated platforms:** Amazon Bedrock or Vertex AI (refer to those platforms' compliance documentation)
  > - **Claude Platform on AWS and Microsoft Foundry:** HIPAA readiness is not available
  - *Source*: [API and Data Retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention.md)

- **New FAQ: Claude Platform on AWS ZDR eligibility**: A new FAQ entry clarifies that Claude Platform on AWS follows the same data retention policy as the first-party Claude API, ZDR is available on request (via account representative), but HIPAA readiness is not available.
  > Claude Platform on AWS follows the same data retention policy as the first-party Claude API. ZDR is available on request; contact your Anthropic account representative to enable it. HIPAA readiness is not available on Claude Platform on AWS.
  - *Implication*: Customers on Claude Platform on AWS who need ZDR have a path; those requiring HIPAA compliance must use the first-party Claude API.
  - *Source*: [API and Data Retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention.md)

- **Claude Code removed from HIPAA guide scope**: The HIPAA Implementation Guide note previously listed "Claude Enterprise, Claude Code, and configuration requirements." Claude Code has been removed from that description.
  > This page covers HIPAA readiness for the Claude API. For the full HIPAA Implementation Guide covering Claude Enterprise and configuration requirements, see the [Anthropic Trust Center](https://trust.anthropic.com/resources).
  - *Implication*: Confirms Claude Code is not covered by HIPAA readiness, consistent with the existing exclusion bullet point on the same page.
  - *Source*: [API and Data Retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention.md)

---

### Data Residency — Model Support and Pricing Updates

- **`inference_geo` model support now explicitly includes Claude Sonnet 4.6**: Previous text said "Claude Opus 4.6 and all subsequent models." Updated text calls out Opus 4.6 and Sonnet 4.6 by name, and specifies which models return a 400 error (Claude Opus 4.5, Claude Sonnet 4.5, Claude Haiku 4.5, or earlier).
  > The `inference_geo` parameter is supported on Claude Opus 4.6, Claude Sonnet 4.6, and later models. Requests with `inference_geo` on Claude Opus 4.5, Claude Sonnet 4.5, Claude Haiku 4.5, or earlier models return a 400 error.
  - *Implication*: The 4.5-generation models (Opus, Sonnet, Haiku) are explicitly unsupported; developers must upgrade to 4.6+ for inference geo control.
  - *Source*: [Data Residency](https://platform.claude.com/docs/en/manage-claude/data-residency.md)

- **Data residency 1.1x pricing now includes Claude Sonnet 4.6**: The pricing tier for US-only inference previously listed only "Claude Opus 4.6 and newer." It now explicitly covers Claude Sonnet 4.6 as well.
  > **Claude Opus 4.6, Claude Sonnet 4.6, and later:** US-only inference (`inference_geo: "us"`) is priced at 1.1x the standard rate across all token pricing categories.
  - *Implication*: Sonnet 4.6 users with `inference_geo: "us"` will see 1.1x pricing; this applies to both the first-party Claude API and Claude Platform on AWS.
  - *Source*: [Data Residency](https://platform.claude.com/docs/en/manage-claude/data-residency.md)

- **Pricing coverage extended to Claude Platform on AWS**: Data residency pricing (the 1.1x multiplier) now explicitly applies to "the Claude API (first-party) and Claude Platform on AWS." Bedrock and Vertex AI are described as "partner-operated platforms" with their own regional pricing.
  - *Source*: [Data Residency](https://platform.claude.com/docs/en/manage-claude/data-residency.md)

- **`inference_geo: "global"` language tightened**: The pricing table previously listed global routing as `inference_geo: "global"` **or omitted**. The "or omitted" clause has been removed from this entry. The current limitations note about inference geo also removed "at launch," indicating the two available values (`"us"` and `"global"`) are the stable set for now.
  - *Source*: [Data Residency](https://platform.claude.com/docs/en/manage-claude/data-residency.md)

---

### Claude Code Analytics API — MultiEdit Tool Added

- **New `MultiEdit` tool metric**: The Claude Code Analytics API now tracks `multi_edit_tool.accepted/rejected` alongside the existing Edit, Write, and NotebookEdit metrics. This is also surfaced in the feature bullet list, which now reads "Edit, MultiEdit, Write, NotebookEdit."
  > - **multi_edit_tool.accepted/rejected:** Number of MultiEdit tool proposals that the user accepted/rejected
  - *Implication*: Organizations querying analytics data can now separately measure acceptance rates for batch/multi-file edits vs. single-file edits.
  - *Source*: [Claude Code Analytics API](https://platform.claude.com/docs/en/manage-claude/claude-code-analytics-api.md)

- **Supported deployment platforms enumerated explicitly**: The FAQ answer for "Which Claude Code deployments are supported?" now links to each platform by name rather than using a generic list.
  > This API only tracks Claude Code usage on the Claude API. Usage through [Claude Platform on AWS], [Claude in Microsoft Foundry], [Claude in Amazon Bedrock], or [Claude on Vertex AI] is not included.
  - *Source*: [Claude Code Analytics API](https://platform.claude.com/docs/en/manage-claude/claude-code-analytics-api.md)

---

### Workspaces — Prompt Cache Isolation Now Active and Expanded

- **Prompt cache isolation is now live and covers more platforms**: Previously the note read "Starting February 5, 2026, prompt caches will also be isolated per workspace." The date qualifier has been removed (isolation is now in effect), and coverage is expanded to include Claude Platform on AWS and Microsoft Foundry (in beta). Amazon Bedrock and Vertex AI isolate prompt caches per organization rather than per workspace.
  > [Prompt caches](/docs/en/build-with-claude/prompt-caching) are also isolated per workspace on the Claude API, [Claude Platform on AWS], and [Microsoft Foundry] (in beta). On Amazon Bedrock and Vertex AI, prompt caches are isolated per organization.
  - *Implication*: Developers on Bedrock/Vertex AI share prompt caches across all workspaces in their org; developers on the Claude API, Claude Platform on AWS, or Microsoft Foundry have workspace-level isolation.
  - *Source*: [Workspaces](https://platform.claude.com/docs/en/manage-claude/workspaces.md)

---

### Admin API — curl Example Fixes

- **`content-type: application/json` header added to POST/PATCH curl examples**: Five curl examples that send a request body (`--data`) were missing the `content-type` header. All have been corrected: update member role (org), create invite, add member to workspace, update member role (workspace), and update API key.
  - *Implication*: Developers copying these examples verbatim should now get correct behavior; without `content-type: application/json`, the body may be misinterpreted.
  - *Source*: [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api.md)

- **Environment variable standardized to `$ANTHROPIC_ADMIN_KEY`**: Two examples used `$ADMIN_API_KEY`; both are updated to `$ANTHROPIC_ADMIN_KEY` to match the variable name used throughout the rest of the docs. Affected pages: `admin-api.md` and `workspaces.md`.
  - *Source*: [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api.md), [Workspaces](https://platform.claude.com/docs/en/manage-claude/workspaces.md)

---

### Usage and Cost API — Model Clarification

- **`inference_geo` unavailability note updated to include Claude Sonnet 4.6**: The note about models that return `"not_available"` for the `inference_geo` dimension now reads "prior to Claude Opus 4.6 and Claude Sonnet 4.6" (was "prior to Claude Opus 4.6" only).
  > Models released before February 2026 (prior to Claude Opus 4.6 and Claude Sonnet 4.6) don't support the `inference_geo` request parameter, so their usage reports return `"not_available"` for this dimension.
  - *Source*: [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api.md)

## Notable Details

- The wording "via" is consistently replaced with "through" across all six pages (curl examples, bullet points, FAQ answers). This appears to be a documentation style standardization.
- "1st party" / "1P" phrasing is replaced with "first-party" throughout.
- "AWS Bedrock" is corrected to "Amazon Bedrock" throughout.
- The Claude Code Analytics API FAQ phrasing changes from "authenticate via OAuth" to "authenticate through OAuth" and "authenticate via API key" to "authenticate with an API key."
- `customer_type` clarification: `api` now described as "pay-as-you-go API" instead of "API PAYG."

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| admin-api.md | Modified | SIGNIFICANT | +12/-3 | Added Claude Platform on AWS availability note; fixed curl examples (content-type header, env var name) |
| api-and-data-retention.md | Modified | SIGNIFICANT | +11/-4 | HIPAA/ZDR scoping for Claude Platform on AWS and Microsoft Foundry; new FAQ entry; removed Claude Code from HIPAA guide mention |
| claude-code-analytics-api.md | Modified | SIGNIFICANT | +20/-15 | Added MultiEdit tool metric; added Claude Platform on AWS unavailability note; expanded platform list in FAQ |
| data-residency.md | Modified | SIGNIFICANT | +17/-9 | Sonnet 4.6 added to inference_geo support and 1.1x pricing; Claude Platform on AWS notes for inference geo and workspace geo |
| usage-cost-api.md | Modified | SIGNIFICANT | +5/-1 | Added Claude Platform on AWS unavailability note; updated model cutoff to include Sonnet 4.6 |
| workspaces.md | Modified | SIGNIFICANT | +5/-5 | Prompt cache isolation now live and extended to Claude Platform on AWS and Microsoft Foundry; env var name fix |

---
*Generated from Claude API documentation changes detected on 2026-05-13*
