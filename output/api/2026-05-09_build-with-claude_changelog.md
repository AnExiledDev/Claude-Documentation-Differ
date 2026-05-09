# Claude API Documentation Changes — 2026-05-09

## Summary

Six pages in the "Build with Claude" section were updated. The most notable changes are: structured outputs reaching general availability on Google Cloud Vertex AI for several models, and the Java SDK being bumped to version 2.30.0 across all cloud provider integrations. A Compliance API reference was also added to the overview and Microsoft Foundry unsupported-features list.

## Significant Changes

### Structured Outputs

- **Structured outputs now GA on Google Cloud Vertex AI**: The availability note for structured outputs was updated to reflect general availability on Vertex AI for Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6. Previously, Vertex AI was excluded entirely for Claude Mythos Preview, and no GA support was documented.
  > On [Google Cloud Vertex AI](/docs/en/build-with-claude/claude-on-vertex-ai), structured outputs are generally available for Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6.
  - *Implication*: Developers using Vertex AI with these models can now rely on structured outputs without beta caveats.
  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

- **Overview table updated to reflect Vertex AI availability**: The feature availability table on the overview page now includes `vertexAi` in the platform availability component for structured outputs.
  - *Implication*: The feature availability matrix is now consistent with the structured outputs page.
  - *Source*: [Build with Claude Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

### SDKs

- **Java SDK bumped to 2.30.0** across all cloud provider integrations (Amazon Bedrock, Amazon Bedrock Legacy, Google Cloud Vertex AI, and Microsoft Foundry). The `anthropic-java-bedrock`, `anthropic-java-vertex`, and `anthropic-java-foundry` artifacts were all updated from `2.27.0` to `2.30.0`.
  > ```kotlin
  > implementation("com.anthropic:anthropic-java-bedrock:2.30.0")
  > ```
  - *Implication*: Developers should update their Gradle/Maven dependency declarations to `2.30.0` to stay current.
  - *Source*: [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock.md), [Claude on Amazon Bedrock (Legacy)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy.md), [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md), [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md)

### Platform Availability & Compliance

- **Compliance API added to Microsoft Foundry unsupported features**: The `/v1/compliance/*` endpoints were explicitly added to the list of API features not available when using Claude via Microsoft Foundry.
  > - Compliance API (`/v1/compliance/*` endpoints)
  - *Implication*: Developers building compliance workflows on Foundry should be aware this API surface is unavailable there.
  - *Source*: [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md)

- **Compliance API referenced in Build with Claude overview**: A new line was added directing developers to the Admin API, Usage and Cost API, and Compliance API for administration and governance tasks.
  > For administration and governance, see the [Admin API](/docs/en/manage-claude/admin-api), the [Usage and Cost API](/docs/en/manage-claude/usage-cost-api), and the [Compliance API](/docs/en/manage-claude/compliance-api).
  - *Implication*: Surfaces the existence of the Compliance API to developers who land on the overview page.
  - *Source*: [Build with Claude Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

## Notable Details

- **Vertex AI feature link fixed**: On the Claude on Vertex AI page, the "API features overview" link was corrected from the stale path `/docs/en/api/overview` to `/docs/en/build-with-claude/overview`. This was a broken internal link.
  - *Source*: [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

- **`aws_region` comment phrasing clarified**: In the Amazon Bedrock Legacy code examples (both Python and TypeScript), the inline comment describing `aws_region` behavior was reworded from first-person ("we read", "we default to", "we do not read") to third-person, SDK-attributed language ("the SDK reads", "defaults to", "the SDK does not read"). No behavioral change.
  - *Source*: [Claude on Amazon Bedrock (Legacy)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `build-with-claude/structured-outputs.md` | Modified | +1/-1 | Vertex AI structured outputs now GA for multiple models |
| `build-with-claude/overview.md` | Modified | +3/-1 | Added Compliance/Admin/Usage API links; Vertex AI added to structured outputs availability |
| `build-with-claude/claude-in-microsoft-foundry.md` | Modified | +3/-2 | Java SDK 2.27.0→2.30.0; Compliance API added to unsupported features |
| `build-with-claude/claude-on-amazon-bedrock-legacy.md` | Modified | +7/-7 | Java SDK 2.27.0→2.30.0; aws_region comment rephrased |
| `build-with-claude/claude-on-vertex-ai.md` | Modified | +3/-3 | Java SDK 2.27.0→2.30.0; fixed broken feature overview link |
| `build-with-claude/claude-in-amazon-bedrock.md` | Modified | +2/-2 | Java SDK 2.27.0→2.30.0 |

---
*Generated from Claude API documentation changes detected on 2026-05-09*
