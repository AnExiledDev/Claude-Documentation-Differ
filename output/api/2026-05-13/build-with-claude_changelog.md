# Claude API Documentation Changes — 2026-05-13

## Summary

A new **Claude Platform on AWS** documentation page (1,065 lines) introduces a separate AWS Marketplace integration where Anthropic operates the inference infrastructure — distinct from Amazon Bedrock. Feature availability tables across the platform overview were updated to include this new platform. Several correctness fixes were made to Bedrock legacy regional endpoint examples, the `ant` CLI's `--format yaml` flag was replaced with `--raw-output` across all code examples, and the streaming docs clarify that multiple `message_delta` events may be emitted.

---

## Significant Changes

### New Platform: Claude Platform on AWS

- **New integration available via AWS Marketplace**: Claude Platform on AWS is a new offering where Anthropic (not AWS) operates the inference stack, but billing and access flow through your AWS account. It provides the full Anthropic platform experience — Messages API, Agent Skills, code execution, and beta features — with same-day feature parity with the Claude API.

  > "Claude Platform on AWS gives you the full Anthropic platform experience, including the Messages API, Agent Skills, code execution, and beta features, accessible through your AWS account. Unlike Amazon Bedrock, where AWS operates the inference stack, Anthropic operates Claude Platform on AWS."

  Key operational details:
  - **Base URL:** `aws-external-anthropic.{region}.api.aws`
  - **Authentication:** AWS IAM / SigV4 (primary) or API key via `ANTHROPIC_AWS_API_KEY`
  - **SDK client:** New platform-specific class (e.g., `AnthropicAWS` in Python), in beta
  - **Workspace ID:** Required per request; format `wrkspc_01...`; set via `ANTHROPIC_AWS_WORKSPACE_ID`
  - **Setup requirement:** AWS outbound web identity federation must be enabled once per account via `aws iam enable-outbound-web-identity-federation`
  - **Beta features:** `anthropic-beta` headers pass through (unlike Bedrock where they are unsupported)
  - **Agent Skills:** Available (beta) — not available on Bedrock
  - **Zero Data Retention:** Available on request; inference may route outside AWS
  - **AWS PrivateLink** is supported

  Short-term API keys (12-hour TTL) can be generated using AWS-published token-generator libraries for JavaScript, Python, and Java.

  > "**When to choose Bedrock:** Organizations in regulated industries that require FedRAMP High, IL4, IL5, or HIPAA-ready compliance, or that need AWS to be the sole data processor, should use Claude in Amazon Bedrock."

  - *Implication*: Developers needing same-day access to beta features, Agent Skills, or the standard Anthropic API surface but wanting AWS IAM authentication and AWS Marketplace billing now have a supported path that doesn't require waiting for Bedrock's feature release cycle.
  - *Source*: [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws.md)

---

### Platform Availability Tables

- **Claude Platform on AWS added as a platform column across all feature tables**: The features overview now includes `claudePlatformAws` availability markers for every feature. A new platform labels legend was added:

  > "**Platform labels:** Claude API (Anthropic first-party) · Claude Platform on AWS (Anthropic-operated on AWS) · Bedrock (AWS-operated) · Vertex AI (Google-operated) · Microsoft Foundry (Anthropic-operated on Azure)"

  Notable additions to Claude Platform on AWS availability:
  - All model capabilities (context windows, adaptive thinking, batch processing, citations, data residency, effort, extended thinking, PDF support, search results, structured outputs)
  - All server-side tools (Advisor tool [beta], code execution, web fetch, web search)
  - All client-side tools (bash, computer use [beta], memory, text editor)

  - *Implication*: The feature matrix now signals Claude Platform on AWS as a first-class platform. Developers can evaluate exactly which features are supported before migrating workloads.
  - *Source*: [Features Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

- **Effort parameter now supports Claude Sonnet 4.6**: The effort parameter description was updated.

  > "Supported on Opus 4.7, Opus 4.6, Sonnet 4.6, and Opus 4.5."

  Previously listed only Opus 4.7, Opus 4.6, and Opus 4.5.
  - *Implication*: Developers using Sonnet 4.6 can now use `effort` to tune token usage/thoroughness trade-offs.
  - *Source*: [Features Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

---

### Batch Processing

- **Extended output (300k tokens) now available on Claude Platform on AWS**: The note for the `output-300k-2026-03-24` beta header was updated.

  > "Extended output is available on the Message Batches API only, not the synchronous Messages API. It is supported on the Claude API and Claude Platform on AWS, and is not available on Amazon Bedrock, Vertex AI, or Microsoft Foundry."

  - *Implication*: Developers using Claude Platform on AWS can now generate batch outputs up to 300,000 tokens (vs. the standard 64k–128k cap) for book-length drafts, large code scaffolds, and exhaustive data extraction.
  - *Source*: [Batch Processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing.md)

---

### Streaming

- **Multiple `message_delta` events may now be emitted**: The stream response structure description changed from "A `message_delta` event" to "One or more `message_delta` events."

  > "3. One or more `message_delta` events"

  - *Implication*: Parsers that assumed exactly one `message_delta` event per stream response should be updated to handle multiple occurrences.
  - *Source*: [Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming.md)

- **Streaming recovery section extended to "Claude 4.6 and later"**: Previously titled "Claude 4.6", the section now covers 4.6 and later models, with a clarification on the recovery strategy:

  > "For Claude 4.6 and later models, the same capture-and-resume strategy applies, but step 2 changes: instead of placing the partial response in an assistant message, add a user message that instructs the model to continue from where it left off."

  - *Implication*: The recovery pattern for interrupted streams differs from 4.5 and earlier — developers building retry logic for 4.6+ models need the user-message continuation pattern.
  - *Source*: [Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming.md)

- **Extended thinking streaming examples updated to adaptive thinking on Opus 4.7**: Code examples across C#, Go, and Java were updated from `enabledThinking(16000)` on Opus 4.6 to `ThinkingConfigAdaptive` with `Display.SUMMARIZED` on Opus 4.7.
  - *Implication*: The canonical streaming + extended thinking example now uses adaptive thinking, which is the recommended mode for Opus 4.7.
  - *Source*: [Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming.md)

---

### Compaction (Beta)

- **PHP field rename: `pauseAfterCompaction` → `pause_after_compaction`**: The PHP compaction example now uses snake_case for the pause field.

  > ```php
  > 'pause_after_compaction' => true
  > ```
  
  Previously documented as `'pauseAfterCompaction' => true`.

  - *Implication*: PHP SDK users of compaction with pause-after-compaction enabled need to update the field name to `pause_after_compaction`.
  - *Source*: [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction.md)

- **PHP SDK note on `compaction` stop reason**: A note was added clarifying that the PHP SDK does not yet expose a typed constant for the `compaction` stop reason and developers should compare the string value directly.
  - *Source*: [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction.md)

---

### Amazon Bedrock (Legacy) — Regional Endpoint Correction

- **CRIS regional endpoint examples corrected**: The documentation previously instructed removing the `global.` prefix to use regional endpoints. It now correctly instructs replacing `global.` with a regional prefix (e.g., `us.`). All SDK examples were updated.

  Before:
  > "To use regional endpoints, remove the `global.` prefix from the model ID"
  > ```python
  > model="anthropic.claude-opus-4-6-v1",  # No global. prefix
  > ```

  After:
  > "To use regional endpoints, replace the `global.` prefix with a regional prefix such as `us.`:"
  > ```python
  > model="us.anthropic.claude-opus-4-6-v1",  # Regional prefix
  > ```

  - *Implication*: Existing code using the old "no prefix" pattern may have been routing incorrectly. The correct identifier for US regional CRIS is `us.anthropic.claude-opus-4-6-v1`, not `anthropic.claude-opus-4-6-v1`.
  - *Source*: [Claude on Amazon Bedrock (Legacy)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy.md)

- **Regional availability updated**: "Australia" replaced with "Asia-Pacific" in the CRIS regional availability list.
  - *Source*: [Claude on Amazon Bedrock (Legacy)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy.md)

- **Global endpoints default model list corrected**: Default global models now listed as Opus 4.6, Sonnet 4.6, and Sonnet 4.5 (previously listed as Opus 4.6, Sonnet 4.5, and "Sonnet 4 (deprecated)").
  - *Source*: [Claude on Amazon Bedrock (Legacy)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy.md)

- **Cross-reference to Claude Platform on AWS added**: The introductory note now links to Claude Platform on AWS as an alternative with same-day feature access, and includes a pointer to a migration guide.
  - *Source*: [Claude on Amazon Bedrock (Legacy)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy.md)

---

### Microsoft Foundry

- **"Azure Entra ID" renamed to "Microsoft Entra ID" throughout**: All references to "Azure Entra ID" in authentication section headings, code comments, and notes were updated to "Microsoft Entra ID". Section headings also adjusted (from h2 to h3 for the auth section).
  - *Source*: [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md)

- **Claude Opus 4.1 added to Foundry model table**: The model listing now includes `claude-opus-4-1` with its default deployment name.
  - *Source*: [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md)

- **SDK support note expanded**: Previously noted Go and Ruby as unsupported, pointing users to Python/TypeScript. Now points users to C#, Java, PHP, Python, or TypeScript for full Foundry support.
  - *Source*: [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md)

- **PHP code example fixed**: The PHP Entra ID authentication example now shows how to obtain the token:
  ```php
  // Obtain an Entra ID access token, for example via the Azure CLI:
  //   az account get-access-token --resource https://cognitiveservices.azure.com \
  //     --query accessToken -o tsv
  $token = getenv('AZURE_ACCESS_TOKEN');
  ```
  Previously the example referenced `$token` without defining it.
  - *Source*: [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md)

---

### Amazon Bedrock (New Integration)

- **Section headings renamed for consistency**: "Feature availability" → "Feature support"; "Observability" → "Monitoring and logging".
- **Messages API endpoint corrected**: Listed as `/anthropic/v1/messages` (previously shown as `/v1/messages` in the feature list).
- **Cross-reference to Claude Platform on AWS** added to the introductory note.
  - *Source*: [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock.md)

---

### Handling Stop Reasons

- **`max_tokens` note corrected for Python SDK**: The `model_context_window_exceeded` example was updated from `max_tokens=64000` to `max_tokens=20000` with a comment that the Python SDK requires streaming for values above ~21k.

  > ```python
  > max_tokens=20000,  # Python SDK requires streaming for max_tokens above ~21k
  > ```

  - *Implication*: Python developers using non-streaming requests should stay at or below ~21k `max_tokens`; larger values require enabling streaming.
  - *Source*: [Handling Stop Reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons.md)

---

### `ant` CLI: `--format yaml` replaced with `--raw-output`

Across multiple documentation pages, the `ant` CLI flag `--transform X --format yaml` was updated to `--transform X --raw-output`. This affects code examples in:
- `adaptive-thinking.md`, `batch-processing.md`, `compaction.md`, `fast-mode.md`

  Before: `--transform id --format yaml`
  After: `--transform id --raw-output`

  - *Implication*: The `ant` CLI now uses `--raw-output` to emit a plain scalar value rather than YAML-formatted output. Update any scripts using the old flag.

---

## Minor Changes

- **adaptive-thinking.md**: CLI flag updated `--format yaml` → `--raw-output` (+1/-1)
- **embeddings.md**: Minor single-line change (+1/-1)
- **search-results.md**: One line removed (+0/-1)
- **working-with-messages.md**: Small addition (+3/-1)
- **context-editing.md**: Section heading casing change "Using with the Memory Tool" → "Using with the memory tool" (+11/-10)
- **pdf-support.md**: Section heading casing normalized ("Amazon Bedrock PDF Support" → "Amazon Bedrock PDF support", etc.) (+7/-9)
- **skills-guide.md**: Section heading casing normalized throughout (+68/-70)
- **vision.md**: Minor updates (+4/-4)
- **files.md**: Minor updates (+3/-3)
- **effort.md**: Minor updates (+5/-5)
- **context-windows.md**: Minor updates (+7/-7)
- **extended-thinking.md**: Minor updates (+5/-5)
- **structured-outputs.md**: Minor updates (+5/-5)
- **claude-on-vertex-ai.md**: "now generally available" → "available"; Java example updated to `VertexBackend.builder()` pattern; references to Claude Platform on AWS added (+39/-26)

---

## New Pages

- **claude-platform-on-aws.md** — Full documentation for Claude Platform on AWS: a new Anthropic-operated integration accessible through AWS Marketplace, supporting the full Messages API surface, beta features, Agent Skills, SigV4/API key authentication, and AWS PrivateLink. [View](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws.md)

---

## Migration Notes

- **Compaction (PHP)**: Rename `pauseAfterCompaction` → `pause_after_compaction` in context management edit params.
- **Bedrock Legacy CRIS regional endpoints**: Use `us.anthropic.claude-opus-4-6-v1` (not `anthropic.claude-opus-4-6-v1`) for US regional routing. The old "no prefix" pattern was incorrect.
- **`ant` CLI**: Replace `--format yaml` with `--raw-output` when extracting scalar values from command output.
- **Python SDK non-streaming**: Keep `max_tokens` at or below ~21k for non-streaming requests; use streaming for larger output budgets.

---

## Notable Details

- The overview page beta classification description was narrowed: beta headers are now explicitly scoped to "the Claude API and Claude Platform on AWS" — confirming that Bedrock and Vertex AI do not support `anthropic-beta` headers by design.
- The pricing reference links on Bedrock legacy and Vertex AI were updated from `#third-party-platform-pricing` to `#cloud-platform-pricing`, suggesting the pricing page reorganized its anchor structure.
- Claude Platform on AWS uses a **separate capacity pool** from both the first-party Claude API and Amazon Bedrock, enabling workload distribution and failover between platforms.
- The compaction page notes that Claude Mythos Preview (`claude-mythos-preview`) is a supported model for compaction alongside Opus 4.7, Opus 4.6, and Sonnet 4.6.

---

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| claude-platform-on-aws.md | New | SIGNIFICANT | +1065 | New AWS Marketplace integration with Anthropic-operated infrastructure |
| prompt-caching.md | Modified | SIGNIFICANT | +218/-227 | C# code examples refactored to top-level statement style; no API changes |
| skills-guide.md | Modified | SIGNIFICANT | +68/-70 | Section heading casing normalized throughout |
| streaming.md | Modified | SIGNIFICANT | +48/-49 | "Claude 4.6 and later" clarification; multiple message_delta events; thinking examples updated to adaptive |
| fast-mode.md | Modified | SIGNIFICANT | +39/-37 | CLI flag updated; code example refinements |
| overview.md | Modified | SIGNIFICANT | +35/-33 | Claude Platform on AWS added to all feature tables; platform labels added; Effort updated for Sonnet 4.6 |
| claude-on-vertex-ai.md | Modified | SIGNIFICANT | +39/-26 | Claude Platform on AWS references; Java VertexBackend.builder() pattern; "generally available" wording removed |
| claude-in-microsoft-foundry.md | Modified | SIGNIFICANT | +33/-29 | Azure→Microsoft Entra rename; PHP example fixed; Opus 4.1 added; SDK support expanded |
| claude-on-amazon-bedrock-legacy.md | Modified | SIGNIFICANT | +25/-27 | CRIS regional endpoint code corrected; Asia-Pacific region update; Claude Platform on AWS cross-reference |
| context-editing.md | Modified | SIGNIFICANT | +11/-10 | Section heading casing: "Memory Tool" → "memory tool" |
| compaction.md | Modified | SIGNIFICANT | +19/-12 | PHP `pause_after_compaction` rename; PHP stop reason note; initial message fix |
| pdf-support.md | Modified | SIGNIFICANT | +7/-9 | Section heading casing normalized |
| context-windows.md | Modified | SIGNIFICANT | +7/-7 | Minor updates |
| batch-processing.md | Modified | SIGNIFICANT | +4/-4 | Extended output now available on Claude Platform on AWS; CLI flag updated |
| claude-in-amazon-bedrock.md | Modified | SIGNIFICANT | +4/-4 | Section heading renames; endpoint corrected; Platform on AWS cross-reference |
| vision.md | Modified | SIGNIFICANT | +4/-4 | Minor updates |
| effort.md | Modified | SIGNIFICANT | +5/-5 | Minor updates |
| extended-thinking.md | Modified | SIGNIFICANT | +5/-5 | Minor updates |
| structured-outputs.md | Modified | SIGNIFICANT | +5/-5 | Minor updates |
| files.md | Modified | SIGNIFICANT | +3/-3 | Minor updates |
| handling-stop-reasons.md | Modified | SIGNIFICANT | +3/-7 | max_tokens corrected; duplicate note removed |
| working-with-messages.md | Modified | MINOR | +3/-1 | Small addition |
| adaptive-thinking.md | Modified | MINOR | +1/-1 | CLI flag updated |
| embeddings.md | Modified | MINOR | +1/-1 | Minor change |
| search-results.md | Modified | MINOR | +0/-1 | One line removed |

---
*Generated from Claude API documentation changes detected on 2026-05-13*
