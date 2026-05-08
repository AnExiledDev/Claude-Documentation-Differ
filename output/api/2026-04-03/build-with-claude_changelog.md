# Claude API Documentation Changes — 2026-04-03

## Summary

Anthropic has added comprehensive HIPAA readiness documentation to the Claude API, introducing HIPAA-ready API access as a distinct compliance arrangement alongside the existing Zero Data Retention (ZDR) offering. The main eligibility table has been expanded to cover both ZDR and HIPAA columns across all features. The structured outputs data retention section also received an explicit HIPAA eligibility note with a PHI-in-schema restriction.

---

## Significant Changes

### Compliance & Data Retention

- **New HIPAA Readiness Program**: Anthropic now offers HIPAA-ready API access for organizations handling Protected Health Information (PHI), separate from and as an alternative to ZDR. Organizations must sign a Business Associate Agreement (BAA) and receive a dedicated HIPAA-enabled organization provisioned by Anthropic.

  > "Previously, organizations that required HIPAA readiness for the Claude API needed to enable ZDR. HIPAA-ready API access removes this requirement and provides a foundation for Anthropic to progressively enable additional features as they are audited for HIPAA readiness."

  - *Implication*: Healthcare and regulated-data API users can now opt into HIPAA-ready access without the constraints of full ZDR. Contact Anthropic sales to sign a BAA.
  - *Source*: [API and Data Retention](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention.md)

- **Feature Eligibility Table Now Includes HIPAA Column**: The former "ZDR eligibility by feature" table (section `#zdr-eligibility-by-feature`) has been renamed to "Feature eligibility" (`#feature-eligibility`) and expanded with a new **HIPAA eligible** column. Notable per-feature HIPAA eligibility outcomes:

  | Feature | ZDR eligible | HIPAA eligible |
  |---------|-------------|----------------|
  | Messages API, Token counting, Fast mode, 1M context, Extended thinking, Citations, Data residency, Effort, Adaptive thinking, PDF support, Search results, Bash/Text editor tools, Fine-grained tool streaming, Prompt caching | Yes | Yes |
  | Structured outputs | Yes (qualified) | Yes (with PHI schema restriction) |
  | Web search | Yes¹ | Yes¹ |
  | Web fetch | Yes¹ ² | **No** |
  | Context management (compaction) | Yes | **No** |
  | Context editing | Yes | **No** |
  | Computer use | Yes | **No** |
  | Tool search | Yes (qualified) | **No** |
  | Batch processing, Code execution, Programmatic tool calling, Files API, Agent skills, MCP connector | No | **No** |

  ¹ Dynamic filtering is not eligible for either ZDR or HIPAA.

  - *Implication*: Developers building HIPAA-compliant integrations now have a single authoritative reference. Features like web fetch, context management/editing, computer use, and tool search are not HIPAA-eligible and will be automatically blocked by the API for HIPAA-enabled organizations.
  - *Source*: [API and Data Retention](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention.md)

- **HIPAA Error Handling — Automatic `400` Blocking**: HIPAA-enabled organizations that send API requests using non-eligible features will receive an automatic `400` error:

  ```json
  {
    "type": "error",
    "error": {
      "type": "invalid_request_error",
      "message": "The requested features are not available for HIPAA-regulated organizations without Zero Data Retention: code_execution."
    }
  }
  ```

  - *Implication*: Unlike ZDR (which is honor-system at the feature level), HIPAA enforcement is active — the API will reject non-compliant requests rather than silently allowing them.
  - *Source*: [API and Data Retention](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention.md)

- **PHI Must Not Appear in JSON Schema Definitions**: For structured outputs (`strict: true`) and strict tool use, JSON schemas are compiled into grammars cached separately from message content and do not receive PHI protections. The restriction applies to schema property names, `enum` values, `const` values, and `pattern` regular expressions.

  > "Patient-specific information should only appear in message content, where it is protected under HIPAA safeguards."

  - *Implication*: HIPAA users of structured outputs must audit their schemas to ensure no patient-identifiable data is embedded in schema definitions. PHI belongs only in the messages (prompts/responses), not in schema structure.
  - *Source*: [API and Data Retention](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention.md), [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **HIPAA Readiness Scope Clarifications**: The documentation explicitly states what is *not* covered by the BAA, including Claude consumer plans (Free/Pro/Max), Console/Workbench, Claude Code, AWS Bedrock, Google Cloud Vertex AI, third-party integrations, and beta features not listed as eligible.

  - *Implication*: Organizations using Claude Code or deploying via cloud marketplaces should not rely on this BAA — separate compliance arrangements are required for those surfaces.
  - *Source*: [API and Data Retention](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention.md)

- **CORS Restriction Clarified as ZDR-Specific**: The section formerly titled "CORS not supported" has been renamed to "CORS not supported for ZDR", clarifying that this CORS limitation applies specifically to ZDR arrangements rather than the API generally.

  - *Implication*: HIPAA-enabled organizations (without ZDR) may have different CORS considerations; the prior wording was ambiguous.
  - *Source*: [API and Data Retention](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention.md)

---

## Notable Details

- **Strict tool use now explicitly linked to the structured outputs grammar pipeline**: The feature eligibility table note for structured outputs now reads: "This also covers [strict tool use](/docs/en/agents-and-tools/tool-use/strict-tool-use) (`strict: true` on tools), which uses the same grammar pipeline." This makes explicit that the PHI-in-schema restriction applies equally to `strict: true` tool definitions.

- **FAQ accordion retitled for ZDR specificity**: The accordion "What happens if I use a feature marked 'No'?" is now "What happens if I use a feature marked 'No' under ZDR?" — a disambiguation added alongside the new parallel HIPAA FAQ entries.

- **New FAQ entries for HIPAA** cover: how HIPAA differs from ZDR, whether ZDR is still needed with HIPAA, what happens on non-eligible HIPAA feature use, organization separation requirements, and how to request access.

- **Internal anchor link updated in `overview.md`**: The footnote linking to the eligibility table was updated from `#zdr-eligibility-by-feature` to `#feature-eligibility` to match the renamed section.

- **Structured outputs page updated** to explicitly state HIPAA eligibility and the PHI schema restriction, and the link at the bottom of the data retention subsection was updated from "ZDR eligibility" to "ZDR and HIPAA eligibility".

- **Data retention policy footnote for law/policy violations** extended: Now reads "Even with ZDR **or HIPAA** arrangements in place..." — confirming the 2-year retention exception applies to both compliance arrangements.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| [api-and-data-retention.md](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention.md) | Modified | +166 / -44 | Added HIPAA readiness program, getting started steps, scope, PHI handling guidelines, schema restrictions, error handling, expanded feature eligibility table with HIPAA column, new FAQs |
| [structured-outputs.md](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md) | Modified | +3 / -1 | Added HIPAA eligibility note with PHI-in-schema restriction in data retention section |
| [overview.md](https://platform.claude.com/docs/en/build-with-claude/overview.md) | Modified | +1 / -1 | Updated internal anchor link from `#zdr-eligibility-by-feature` to `#feature-eligibility` |

---

*Generated from Claude API documentation changes detected on 2026-04-03*
