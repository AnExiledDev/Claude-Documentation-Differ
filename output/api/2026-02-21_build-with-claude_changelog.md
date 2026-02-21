# Claude API Documentation Changes — 2026-02-21

## Summary

The largest change in this update is a substantial rewrite of the prompt caching documentation, which introduces **automatic caching** as a new, simpler method alongside the existing explicit `cache_control` breakpoints. Several model status entries were also updated to reflect that Claude Sonnet 3.7 and Claude Haiku 3.5 have now retired (as of February 19, 2026), and Claude Haiku 3 has entered deprecation with a retirement date of April 19, 2026. Fast mode pricing was simplified to a single rate across the full context window, and fast mode was added to the ZDR-eligible feature list.

---

## Significant Changes

### Prompt Caching

- **New: Automatic caching via top-level `cache_control` parameter**: The prompt caching page has been reorganized to document a new, simpler way to enable caching. Instead of attaching `cache_control` to individual content blocks, developers can now pass a single `cache_control` field at the top level of the request body. The system automatically places the cache breakpoint on the last cacheable block and advances it as conversations grow.

  > **Automatic caching is the simplest way to enable prompt caching. Instead of placing `cache_control` on individual content blocks, add a single `cache_control` field at the top level of your request body. The system automatically applies the cache breakpoint to the last cacheable block.**

  The updated FAQ answer for "How do I enable prompt caching?" now reads:

  > The easiest way is to add `"cache_control": {"type": "ephemeral"}` at the top level of your request body (automatic caching). Alternatively, include at least one `cache_control` breakpoint on individual content blocks (explicit cache breakpoints).

  - *Implication*: Multi-turn conversation caching no longer requires manually updating `cache_control` markers as the conversation grows; the system manages breakpoint advancement automatically.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **Automatic caching: multi-turn conversation behavior documented**: The update adds a table describing exactly how the cache pointer moves on each successive request:

  | Request | Content | Cache behavior |
  |---------|---------|----------------|
  | Request 1 | System + User:A + Asst:B + **User:C** ◀ cache | Everything written to cache |
  | Request 2 | System + User:A + Asst:B + User:C + Asst:D + **User:E** ◀ cache | System through User:C read from cache; Asst:D + User:E written to cache |
  | Request 3 | System + User:A + Asst:B + User:C + Asst:D + User:E + Asst:F + **User:G** ◀ cache | System through User:E read from cache; Asst:F + User:G written to cache |

  - *Implication*: Developers can now understand precisely which tokens incur cache-write vs. cache-read charges on each turn without instrumenting their own tracking.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **TTL support for automatic caching documented**: Automatic caching defaults to a 5-minute TTL. The 1-hour TTL is available at 2x the base input token price via `"cache_control": {"type": "ephemeral", "ttl": "1h"}`.
  - *Implication*: TTL selection works the same way for automatic caching as for explicit breakpoints; no new pricing tiers are introduced.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **Automatic caching edge cases and error conditions documented**:

  > - If the last block already has an explicit `cache_control` with the same TTL, automatic caching is a no-op.
  > - If the last block has an explicit `cache_control` with a different TTL, the API returns a 400 error.
  > - If 4 explicit block-level breakpoints already exist, the API returns a 400 error (no slots left for automatic caching).
  > - If the last block is not eligible as an automatic cache breakpoint target, the system silently walks backwards to find the nearest eligible block. If none is found, caching is skipped.

  - *Implication*: The slot limit (4 breakpoints total) applies across both automatic and explicit breakpoints combined. Mixing both methods requires staying within this limit.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **Automatic caching availability**: Available on the Claude API and Azure AI Foundry (preview). Amazon Bedrock and Google Vertex AI support is listed as coming later.

  > Automatic caching is available on the Claude API and Azure AI Foundry (preview). Support for Amazon Bedrock and Google Vertex AI is coming later.

  - *Implication*: Bedrock and Vertex AI users must continue to use explicit block-level `cache_control` until support is extended to those platforms.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **Explicit cache breakpoints documented as a separate, named method**: The previous content under "How to implement prompt caching" has been restructured into a distinct section titled "Explicit cache breakpoints," clarifying that block-level `cache_control` is now one of two supported approaches. The "Understanding cache breakpoint costs" subsection has been moved from that section into "Caching strategies and considerations."
  - *Implication*: The page structure now clearly distinguishes automatic vs. explicit caching paths, which may affect linked documentation, tutorials, and internal tooling that referenced the old section headings.
  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **Workspace-level cache isolation note updated**: References to "Azure" in the cache isolation warning have been updated to "Azure AI Foundry (preview)" throughout the document.

  > Starting February 5, 2026, prompt caching will use workspace-level isolation instead of organization-level isolation. Caches will be isolated per workspace, ensuring data separation between workspaces within the same organization. This change applies to the Claude API and Azure AI Foundry (preview); Amazon Bedrock and Google Vertex AI will maintain organization-level cache isolation.

  - *Source*: [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md)

- **Overview page: "Automatic prompt caching" added to the Context management feature table**: A new row appears in the overview table linking to the automatic caching section:

  > **Automatic prompt caching**: Simplify prompt caching to a single API parameter. The system automatically caches the last cacheable block in your request, moving the cache point forward as conversations grow. — Claude API and Azure AI Foundry (preview)

  - *Source*: [Build with Claude Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

---

### Fast Mode

- **Pricing simplified: single rate replaces tiered context-window pricing**: Fast mode previously charged 6x standard Opus rates for prompts ≤200K tokens and 12x for prompts >200K tokens. The documentation now states a single rate across the full context window.

  Before:
  > Fast mode is priced at 6x standard Opus rates for prompts ≤200K tokens, and 12x standard Opus rates for prompts > 200K tokens.

  | Context window | Input | Output |
  |:---------------|:------|:-------|
  | ≤ 200K input tokens | $30 / MTok | $150 / MTok |
  | > 200K input tokens | $60 / MTok | $225 / MTok |

  After:
  > Fast mode is priced at 6x standard Opus rates across the full context window.

  | Input | Output |
  |:------|:-------|
  | $30 / MTok | $150 / MTok |

  - *Implication*: Requests with >200K input tokens are now priced the same as shorter requests ($30/$150 per MTok), representing a significant cost reduction for large-context fast-mode usage.
  - *Source*: [Fast Mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode.md)

- **Fast mode listed as ZDR-eligible**: A new note was added to the fast mode page, and fast mode was added to the ZDR-eligible endpoints table in the zero-data-retention page.

  > This feature is Zero Data Retention (ZDR) eligible. When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.

  The ZDR table entry reads:
  > | Fast Mode | `/v1/messages` (with `speed: "fast"`) | Same Messages API endpoint with faster inference. ZDR applies regardless of speed setting. |

  - *Implication*: Organizations with ZDR agreements can now use fast mode without that usage being excluded from their data retention commitments.
  - *Source*: [Fast Mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode.md), [Zero Data Retention](https://platform.claude.com/docs/en/build-with-claude/zero-data-retention.md)

---

### Model Deprecations and Retirements

Both the Amazon Bedrock and Google Vertex AI model tables were updated with the following status changes (effective February 19, 2026):

- **Claude Sonnet 3.7**: Status changed from "Deprecated as of October 28, 2025" to **"Retired as of February 19, 2026"** on both Bedrock and Vertex AI.
- **Claude Haiku 3.5**: Status changed from "Deprecated as of December 19, 2025" to **"Retired as of February 19, 2026"** on both Bedrock and Vertex AI.
- **Claude Haiku 3**: Previously listed with no deprecation notice. Now marked **"Deprecated as of February 19, 2026. Retiring April 19, 2026."** on both Bedrock and Vertex AI.

  - *Implication*: Applications using Claude Sonnet 3.7 or Claude Haiku 3.5 on Bedrock or Vertex AI should already have migrated. Applications using Claude Haiku 3 have until April 19, 2026 to migrate before that model is retired.
  - *Source*: [Claude on Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md), [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

---

### Overview Page: Azure AI Availability Corrections

Several features in the Build with Claude overview were listed as generally available on Azure AI (`azureAi`) and have been corrected to beta (`azureAiBeta`). Affected features:

**Model capabilities:**
- Adaptive thinking
- Batch processing
- Citations
- Effort
- Extended thinking
- PDF support
- Search results

**Tools (server-side):**
- Code execution
- Memory
- Web fetch
- Web search

**Tools (client-side):**
- Bash
- Text editor

**Tool infrastructure:**
- Fine-grained tool streaming
- Programmatic tool calling
- Tool search

**Context management:**
- Prompt caching (5m)
- Prompt caching (1hr)
- Token counting

  - *Implication*: These features on Azure AI Foundry are in preview/beta status, not GA. Developers building production applications on Azure should verify feature stability and SLA coverage with Anthropic before relying on these capabilities.
  - *Source*: [Build with Claude Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

---

### Overview Page: New Introductory Navigation Section

A new introductory paragraph was added at the top of the overview page, grouping the API surface into five named areas and providing onboarding guidance:

> Claude's API surface is organized into five areas:
> - **Model capabilities:** Control how Claude reasons and formats responses.
> - **Tools:** Let Claude take actions on the web or in your environment.
> - **Tool infrastructure:** Handles discovery and orchestration at scale.
> - **Context management:** Keeps long-running sessions efficient.
> - **Files and assets:** Manage the documents and data you provide to Claude.
>
> If you're new, start with model capabilities and tools. Return to the other sections when you're ready to optimize cost, latency, or scale.

  - *Implication*: Purely editorial; no API behavior changed. The "Files & assets" section heading was also renamed to "Files and assets" (ampersand replaced by "and").
  - *Source*: [Build with Claude Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md)

---

## Notable Details

- The prompt caching page code examples for automatic caching were updated across all four supported SDK languages (curl/Shell, Python, TypeScript, Java), showing the simplified top-level `cache_control` syntax without block-level nesting.
- The `Supported models` section for prompt caching was promoted from a subsection under "How to implement prompt caching" to a top-level `##` section, and the wording was updated to: "Prompt caching (both automatic and explicit) is currently supported on:..."
- The best practices, use-case optimization, and troubleshooting subsections were moved from under the old "How to implement prompt caching" hierarchy into the new "Caching strategies and considerations" top-level section, with one addition: "Start with automatic caching for multi-turn conversations. It handles breakpoint management automatically."

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `prompt-caching.md` | Modified | +245 / -132 | Major rewrite introducing automatic caching as a first-class method; restructured sections; new code examples for all SDKs |
| `overview.md` | Modified | +31 / -20 | New navigation intro; "Automatic prompt caching" added to context management table; Azure AI availability corrected to beta for ~15 features |
| `fast-mode.md` | Modified | +8 / -5 | ZDR eligibility note added; pricing simplified from tiered to single rate |
| `claude-on-amazon-bedrock.md` | Modified | +3 / -3 | Sonnet 3.7 and Haiku 3.5 marked retired; Haiku 3 marked deprecated with April 19, 2026 retirement date |
| `claude-on-vertex-ai.md` | Modified | +3 / -3 | Same deprecation/retirement status updates as Bedrock |
| `zero-data-retention.md` | Modified | +1 / -0 | Fast mode added to ZDR-eligible endpoints table |
