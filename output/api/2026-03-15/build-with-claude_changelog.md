# Claude API Documentation Changes — 2026-03-15

## Summary

The primary theme of this update is the **graduation of the 1M-token context window from beta to GA** for Claude Opus 4.6 and Sonnet 4.6 across all supported platforms. The dedicated beta documentation section (with its multi-language code examples and usage-tier requirement) has been removed and replaced with concise, unified guidance. Companion updates raise the per-request image and PDF page limits from 100 to 600 for 1M-context models, and extend server-side compaction support to Sonnet 4.6.

---

## Significant Changes

### Context Windows

- **1M-token context window is now GA for Opus 4.6 and Sonnet 4.6**: The large `## 1M token context window` section — including multi-language SDK examples and usage-tier gating notes — has been removed from `context-windows.md`. In its place, a compact two-sentence summary communicates the current state clearly:
  > Claude Opus 4.6 and Sonnet 4.6 have a 1M-token context window.
  >
  > Claude Sonnet 4.5 and Sonnet 4 require the `context-1m-2025-08-07` [beta header](/docs/en/api/beta-headers) for requests beyond 200k tokens (available to organizations in [usage tier](/docs/en/api/rate-limits) 4 and those with custom rate limits). Other Claude models have a 200k-token context window.
  - *Implication*: Developers using Opus 4.6 or Sonnet 4.6 no longer need to pass the `context-1m-2025-08-07` beta header, add `betas=["context-1m-2025-08-07"]` in SDK calls, or meet the usage-tier 4 requirement. The extended context is simply available.
  - *Source*: [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md)

- **Context window capacity description updated**: The bullet point describing the context window previously read "200K token capacity". It now reads:
  > **Context window capacity:** The total available context window (up to 1M tokens) represents the maximum capacity for storing conversation history and generating new output from Claude.
  - *Source*: [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md)

- **Context awareness token budget examples updated to 1M**: The `<budget:token_budget>` and `<system_warning>` XML examples used by context-aware models (Sonnet 4.6, Sonnet 4.5, Haiku 4.5) now reflect 1M as the default budget:
  ```xml
  <!-- Before -->
  <budget:token_budget>200000</budget:token_budget>
  <system_warning>Token usage: 35000/200000; 165000 remaining</system_warning>

  <!-- After -->
  <budget:token_budget>1000000</budget:token_budget>
  <system_warning>Token usage: 35000/1000000; 965000 remaining</system_warning>
  ```
  The accompanying note now reads: "The budget is set to 1M tokens (200k for models with a smaller context window)."
  - *Implication*: Context-aware models now receive 1M as their explicit token budget signal by default.
  - *Source*: [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md)

- **Compaction now supports Sonnet 4.6**: Both the `context-windows.md` and `overview.md` pages updated the compaction availability note. Previously listed as "available in beta for Claude Opus 4.6"; now includes Sonnet 4.6:
  > It is currently available in beta for Claude Opus 4.6 and Sonnet 4.6.
  - *Source*: [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md), [Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

### Platform-Specific Context Window Sections

New `### Context window` subsections were added to all three third-party platform guides, explicitly documenting 1M-token availability and payload limits per platform.

- **Amazon Bedrock**: Section renamed from `### 1M token context window` to `### Context window`. Sonnet 4.6 added to the list of 1M-context models. The beta note now scopes to only Sonnet 4.5 and Sonnet 4 (not Opus 4.6 or Sonnet 4.6). A new payload limit note was added:
  > Amazon Bedrock limits request payloads to 20 MB. When sending large documents or many images, you may reach this limit before the token limit.
  - *Source*: [Claude on Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md)

- **Google Vertex AI**: New `### Context window` section added documenting that Opus 4.6, Sonnet 4.6, Sonnet 4.5, and Sonnet 4 all have a 1M-token context window, with Sonnet 4.5 and Sonnet 4 still requiring the beta header. Payload limit documented:
  > Vertex AI limits request payloads to 30 MB. When sending large documents or many images, you may reach this limit before the token limit.
  - *Source*: [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

- **Microsoft Foundry**: New `### Context window` section added for Opus 4.6, Sonnet 4.6, and Sonnet 4.5 (note: Sonnet 4 not listed for Foundry). Sonnet 4.5 still requires the beta header on Foundry.
  > Claude Opus 4.6, Sonnet 4.6, and Sonnet 4.5 have a [1M-token context window](/docs/en/build-with-claude/context-windows) on Microsoft Foundry.
  - *Source*: [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md)

### Vision & PDF — Increased Per-Request Limits

- **Image limit raised from 100 to 600 per API request**: The limit increase applies to models with a 1M-token context window; models with a 200k context window retain the 100-image cap.
  > You can include multiple images in a single request: up to 20 for [claude.ai](https://claude.ai/), and up to 600 for API requests (100 for models with a 200k-token context window).

  The FAQ in `vision.md` is similarly updated:
  > Messages API: Up to 600 images per request (100 for models with a 200k-token context window)

  The note about request size limits was expanded with a Files API recommendation:
  > While the API supports up to 600 images per request, [request size limits](/docs/en/api/overview#request-size-limits) (32&nbsp;MB for standard endpoints; lower on some third-party platforms) can be reached first. For many images, consider uploading with the [Files API](#files-api-image-example) and referencing by `file_id` to keep request payloads small.
  - *Implication*: Applications using 1M-context models can now send significantly more images per request, but the 32 MB payload cap (and lower platform-specific caps) will often be the binding constraint.
  - *Source*: [Vision](https://platform.claude.com/docs/en/build-with-claude/vision.md)

- **PDF page limit raised from 100 to 600**: Same tiering as images — 100 pages for 200k-context models, 600 for 1M-context models. A new tip and Files API suggestion were added:
  > | Maximum pages per request | 600 (100 for models with a 200k-token context window) |

  > Dense PDFs (many small-font pages, complex tables, or heavy graphics) can fill the context window before reaching the page limit. If this happens, try splitting the document into sections.

  > For large PDFs, consider uploading with the [Files API](#option-3-files-api) and referencing by `file_id` to keep request payloads small.
  - *Source*: [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support.md)

- **Vision pricing example model changed**: Token cost table and reference model updated from Claude Opus 4.6 to Claude Sonnet 4.6 (same $3/M input token price).
  - *Source*: [Vision](https://platform.claude.com/docs/en/build-with-claude/vision.md)

- **Context windows page documents combined image/PDF limit**:
  > A single request can include up to 600 images or PDF pages (100 for models with a 200k-token context window). When sending many images or large documents, you may approach [request size limits](/docs/en/api/overview#request-size-limits) before the token limit.
  - *Source*: [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md)

### Features Overview Page

- **1M context window row status updated from beta to GA**: The feature availability indicators changed from `claudeApiBeta bedrockBeta vertexAiBeta azureAiBeta` to `claudeApi bedrock vertexAi azureAiBeta` — the Claude API, Bedrock, and Vertex are now GA; Azure/Foundry remains in beta. The link also changed from the old `#1m-token-context-window` anchor (now removed) to the top-level `context-windows` page.
  - *Source*: [Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

### Zero Data Retention

- **1M context window ZDR entry updated to reflect GA status**: The endpoint row in the ZDR table previously showed the beta header as a required qualifier. It now reads:
  > | 1M Token Context Window | `/v1/messages` | Extended context processing uses the standard Messages API. ZDR applies for all supported models, including beta access on Claude Sonnet 4.5 and Sonnet 4. |
  - *Implication*: ZDR continues to apply for the full 1M context feature, including the remaining beta models.
  - *Source*: [Zero data retention](https://platform.claude.com/docs/en/build-with-claude/zero-data-retention.md)

---

## Notable Details

- **Compaction `context.md` reference de-hardcoded**: The compaction description previously read "may exceed the 200K context window"; it now reads "may exceed the context window" — removing the hardcoded token count to stay accurate as context sizes vary by model. ([Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction.md))

- **Extended thinking context window de-hardcoded**: `extended-thinking.md` previously stated "the token limit becomes your entire context window (200k tokens)"; it now reads "your entire context window" without a specific number. ([Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md))

- **Fast mode rate limit description simplified**: The previous note about separate rate limits for `≤200K` and `>200K` input token requests under fast mode has been removed. Fast mode now has a single unified rate limit description. ([Fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode.md))

- **Data residency Priority Tier note updated**: The example list of pricing multipliers affecting Priority Tier burndown rates removed "long context" as an example, now citing only "prompt caching". This is consistent with long-context no longer being a separately gated/priced beta feature for Opus 4.6 and Sonnet 4.6. ([Data residency](https://platform.claude.com/docs/en/build-with-claude/data-residency.md))

- **Structured outputs code formatting**: Minor Python and TypeScript example reformatting (trailing commas, line breaks in `messages` arrays). No API behavior changes. ([Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md))

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| context-windows.md | Modified | +8/-182 | Removed dedicated 1M beta section; GA for Opus 4.6/Sonnet 4.6 stated inline; updated context awareness examples to 1M; compaction extended to Sonnet 4.6 |
| claude-on-vertex-ai.md | Modified | +10/-0 | New `### Context window` section with 1M support matrix and 30 MB payload limit |
| claude-in-microsoft-foundry.md | Modified | +8/-0 | New `### Context window` section; Opus 4.6, Sonnet 4.6 GA; Sonnet 4.5 still beta |
| structured-outputs.md | Modified | +12/-4 | Code example formatting cleanup only |
| vision.md | Modified | +8/-8 | Image limit raised to 600 (1M models); pricing reference model changed to Sonnet 4.6 |
| pdf-support.md | Modified | +7/-3 | PDF page limit raised to 600 (1M models); tip for dense PDFs; Files API recommendation |
| claude-on-amazon-bedrock.md | Modified | +5/-3 | Renamed section; Sonnet 4.6 added to 1M list; 20 MB payload limit note added |
| extended-thinking.md | Modified | +2/-2 | Removed hardcoded "200k" context window references |
| overview.md | Modified | +2/-2 | 1M context window availability changed from beta to GA on API/Bedrock/Vertex |
| compaction.md | Modified | +1/-1 | Removed hardcoded "200K" context window value |
| data-residency.md | Modified | +1/-1 | Removed "long context" from Priority Tier pricing multiplier example list |
| fast-mode.md | Modified | +1/-1 | Removed separate ≤200K/> 200K rate limit distinction |
| zero-data-retention.md | Modified | +1/-1 | 1M context ZDR entry updated to reflect GA status |
| prompt-caching.md | Modified | +1/-1 | "200K" → "200k" (capitalization) |
| prompt-engineering/claude-prompting-best-practices.md | Modified | +1/-1 | "20K+" → "20k+" (capitalization) |
| skills-guide.md | Modified | +2/-2 | "8MB" → "8&nbsp;MB" (non-breaking space, cosmetic) |

---

*Generated from Claude API documentation changes detected on 2026-03-15*
