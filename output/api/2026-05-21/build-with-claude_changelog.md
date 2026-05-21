# Claude API Documentation Changes — 2026-05-21

## Summary

This update reorganizes feature support documentation across all cloud provider integrations (Amazon Bedrock, Vertex AI, Microsoft Foundry, Claude Platform on AWS), adds four new documented limitations for Claude Platform on AWS, expands prompt caching 1-hour duration to Amazon Bedrock, and bumps the Java SDK to version 2.33.0. The Files API C# code examples were substantially updated to use typed APIs.

## Significant Changes

### Prompt Caching

- **1-Hour Cache Duration Now Available on Amazon Bedrock**: The extended 1-hour prompt cache duration, previously limited to Claude API, Claude Platform on AWS, Vertex AI, and Foundry, is now also available on Amazon Bedrock (both current and legacy integrations).
  > "The 1-hour cache duration is available on the Claude API, Claude Platform on AWS, Amazon Bedrock, Amazon Bedrock (legacy), Vertex AI, and Microsoft Foundry (beta)."
  - *Implication*: Bedrock customers can now use longer-lived cache entries without migrating to a different platform. The `overview.md` availability table was updated to reflect this.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

### Feature Support Documentation Restructured (Cloud Platforms)

All four cloud platform integration pages received a consistent restructuring of their feature support sections. Flat bullet lists are replaced with two named subsections — `### Supported feature highlights` and `### Features not supported` — with individual items now hyperlinked to their respective documentation pages.

- **Amazon Bedrock (Current Integration)**: Supported features now link to Messages API, Prompt caching, Extended thinking, Tool use (Bash, Computer use, Memory, Text editor), Citations, and Structured outputs. Unsupported features are now grouped by category:
  > "- Input sources (URL sources for images and documents, Files API)\n- Server-side tools (code execution, web search, web fetch, advisor)\n- Agent infrastructure (Agent Skills, MCP connector, programmatic tool calling)\n- API endpoints (Message Batches, Models, Admin, Compliance, Usage and Cost)\n- Claude Managed Agents"
  - *Implication*: More granular than the previous list; "Anthropic-defined tools" is replaced with specific categorical groupings. **Zero data retention (ZDR) information was removed** — the prior note "ZDR is available. To enable ZDR for your account, contact AWS support." no longer appears.
  - *Source*: [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock.md)

- **Amazon Bedrock (Legacy Integration)**: Same structural update and identical supported/unsupported feature lists as the current integration page above.
  - *Source*: [Claude on Amazon Bedrock (legacy)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy.md)

- **Vertex AI**: Same structural update. Vertex AI's supported highlights notably include the Web search tool, which is absent from the Bedrock lists. Unsupported features mirror Bedrock's but exclude `web search` (it is supported) and retain `web fetch` as unsupported. A new **Data retention** section was also added:
  > "Data handling for this offering is governed by Google Cloud Vertex AI. For details, see Vertex AI and zero data retention."
  - *Implication*: Explicitly documents that data governance on Vertex AI is Google Cloud's responsibility, with a link to Google's policy page. No equivalent section was added for Bedrock.
  - *Source*: [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

- **Microsoft Foundry**: The "Features not supported" section simplified endpoint references by removing path details (e.g., `Admin API (/v1/organizations/* endpoints)` → `Admin API`). A Claude Code migration tip was added (same as other platforms).
  - *Source*: [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md)

### Claude Platform on AWS — New Limitations Documented

The section previously titled "Features not currently available" is renamed to "Features not supported". Four new limitations were added:

> "- **Webhooks:** Not available on Claude Platform on AWS.\n- **Claude Managed Agents multiagent orchestration:** Only one agent per session is currently supported on Claude Platform on AWS.\n- **Claude Managed Agents self-hosted sandboxes:** Only the `cloud` environment type is supported.\n- **MCP tunnels:** Only MCP servers exposed over the public internet are supported."

- *Implication*: Developers planning multiagent architectures or self-hosted MCP/sandbox deployments on Claude Platform on AWS should note these constraints. Webhooks are also explicitly unavailable. The Claude Agent SDK mention was removed from the Managed Agents description.
- *Source*: [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws.md)

### Platform Availability Table Updates (Features Overview)

Two changes to platform availability flags in the features overview table:

- **Batch Processing**: Removed Amazon Bedrock and Vertex AI from the availability column. The table now shows `claudeApi claudePlatformAws` only (previously included `bedrock vertexAi`).
- **Fine-grained Tool Streaming**: Azure AI availability moved from `azureAiBeta` to `azureAi`, indicating the feature reached GA status on that platform.
- **Prompt Caching (1hr)**: Amazon Bedrock added to availability (consistent with the prompt-caching.md change above).
- *Source*: [Features Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

### Files API — C# SDK Examples Significantly Updated

C# code examples throughout the Files API documentation were rewritten to use strongly-typed SDK classes rather than anonymous objects:

- `File.OpenRead(...)` replaced by a `BinaryContent { Stream, FileName, ContentType }` object for file uploads.
- `"claude-opus-4-6"` string replaced by `Messages::Model.ClaudeOpus4_6` enum.
- `"user"` string replaced by `Role.User` enum.
- `new[] { "files-api-2025-04-14" }` replaced by `[AnthropicBeta.FilesApi2025_04_14]`.
- `new object[] { new { type = "document", ... } }` anonymous objects replaced by `new List<BetaContentBlockParam>` with typed `BetaTextBlockParam` and `BetaRequestDocumentBlock`.
- File download now uses stream-based async copy instead of `WriteAllBytesAsync`.
- TypeScript examples updated from `anthropic.beta.*` to `client.beta.*` variable naming.
- *Implication*: C# developers should update code using the Files API to match the new typed API surface if upgrading the SDK.
- *Source*: [Files API](https://platform.claude.com/docs/en/build-with-claude/files.md)

### Java SDK Updated to 2.33.0

All platform-specific Java SDK packages were bumped from `2.32.0` to `2.33.0` across all cloud provider integration pages:
- `anthropic-java-bedrock` (Amazon Bedrock current + legacy)
- `anthropic-java-vertex` (Vertex AI)
- `anthropic-java-foundry` (Microsoft Foundry)
- `anthropic-java-aws` (Claude Platform on AWS)

- *Implication*: Update your Gradle/Maven dependency version to `2.33.0` for the latest Java SDK on all platforms.
- *Sources*: [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock.md), [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md), [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md), [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws.md)

### Claude Code Migration Tip Added to All Cloud Provider Pages

A new `<Tip>` callout was added to Amazon Bedrock, Amazon Bedrock (legacy), Vertex AI, Microsoft Foundry, and Claude Platform on AWS pages:

> "Upgrading to a newer Claude model? In Claude Code, run `/claude-api migrate` to apply model ID swaps and breaking parameter changes across your codebase. The skill detects which cloud platform your code targets and adjusts model ID formats and feature changes for that platform."

- *Implication*: The `/claude-api migrate` Claude Code skill is now documented as a first-class migration tool for all cloud platforms. This links to the new `claude-api-skill` documentation.

## Minor Changes

- **adaptive-thinking.md**: Wording cleanup — "contact our sales team" → "contact Anthropic sales"; "we recommend passing" → "pass" (imperative style). (+2/-2)
- **batch-processing.md**: Availability note updated from "is not available" to "is not currently available" for Amazon Bedrock, Vertex AI, and Microsoft Foundry. (+1/-1)
- **cache-diagnostics.md**: Diagnostic description updated — "when prefill is very fast" → "when the response starts very quickly". (+1/-1)
- **extended-thinking.md**: Same wording changes as `adaptive-thinking.md` (shared content). (+2/-2)
- **fast-mode.md**: Claude Platform on AWS limitation note changed from "is not available" to "is not currently available". (+1/-1)
- **pdf-support.md**: New note added clarifying that on Amazon Bedrock and Vertex AI, only base64-encoded PDF sources are currently available (URL and Files API sources are not). (+4/-0)
- **vision.md**: Same note added as `pdf-support.md` — only base64-encoded image sources are available on Bedrock and Vertex AI. (+4/-0)

## Migration Notes

- **Batch Processing on Bedrock/Vertex AI**: The feature overview table no longer lists Batch Processing as available on Amazon Bedrock or Vertex AI. Developers relying on this combination should verify current availability status, as this may reflect a documentation correction rather than a feature removal.
- **ZDR on Amazon Bedrock**: The note "Zero data retention (ZDR) is available. To enable ZDR for your account, contact AWS support." was removed from `claude-in-amazon-bedrock.md`. Developers who relied on this guidance should consult AWS support or Amazon Bedrock documentation directly for current ZDR status.
- **Files API C# examples**: If using the C# SDK for the Files API, update to use `BinaryContent` for uploads and the stream-based download pattern shown in the updated examples.

## Notable Details

- The Vertex AI page now explicitly documents that data governance is Google Cloud's responsibility, while the Amazon Bedrock ZDR note was simultaneously *removed*. This asymmetry is worth noting for compliance-sensitive deployments.
- The categorization of unsupported Bedrock/Vertex features into groups (Input sources, Server-side tools, Agent infrastructure, API endpoints) is more precise than the previous flat list, and explicitly names the `advisor` tool as a server-side tool not available on those platforms.
- "Claude Managed Agents" as a top-level unsupported feature on Bedrock remains listed, separate from the "Agent infrastructure" category, suggesting it refers to the higher-level Managed Agents product rather than just the agent tooling.
- Vertex AI's supported highlights include the Web search tool, which is absent from both Bedrock integration pages — the only server-side tool listed as supported on Vertex.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| claude-on-vertex-ai.md | Modified | SIGNIFICANT | +30/-4 | New Data retention section, Supported/unsupported feature restructure, Java SDK 2.33.0, migration tip |
| claude-on-amazon-bedrock-legacy.md | Modified | SIGNIFICANT | +22/-5 | Supported/unsupported feature restructure with links, Java SDK 2.33.0 |
| claude-platform-on-aws.md | Modified | SIGNIFICANT | +22/-14 | 4 new limitations, section renamed, API surface description updated, Java SDK 2.33.0 |
| claude-in-amazon-bedrock.md | Modified | SIGNIFICANT | +19/-16 | Feature restructure, ZDR note removed, Java SDK 2.33.0, migration tip |
| files.md | Modified | SIGNIFICANT | +26/-25 | C# SDK examples updated to typed API; TypeScript `anthropic.` → `client.` |
| claude-in-microsoft-foundry.md | Modified | SIGNIFICANT | +10/-6 | Java SDK 2.33.0, endpoint path details removed from unsupported list, migration tip |
| overview.md | Modified | SIGNIFICANT | +3/-3 | Batch processing removed from Bedrock/Vertex; 1hr cache added to Bedrock; tool streaming Azure GA |
| prompt-caching.md | Modified | SIGNIFICANT | +3/-3 | 1-hour cache now available on Amazon Bedrock (both integrations) |
| vision.md | Modified | MINOR | +4/-0 | Note added: only base64 sources on Bedrock/Vertex AI |
| pdf-support.md | Modified | MINOR | +4/-0 | Note added: only base64 sources on Bedrock/Vertex AI |
| adaptive-thinking.md | Modified | MINOR | +2/-2 | Wording cleanup only |
| extended-thinking.md | Modified | MINOR | +2/-2 | Wording cleanup only (same content as adaptive-thinking) |
| cache-diagnostics.md | Modified | MINOR | +1/-1 | "prefill is very fast" → "response starts very quickly" |
| batch-processing.md | Modified | MINOR | +1/-1 | Added "not currently" qualifier to Bedrock/Vertex unavailability |
| fast-mode.md | Modified | MINOR | +1/-1 | Added "not currently" qualifier to Claude Platform on AWS unavailability |

---
*Generated from Claude API documentation changes detected on 2026-05-21*
