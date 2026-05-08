# Claude API Documentation Changes — 2026-02-19

## Summary

Claude Sonnet 4.6 launched on February 17, 2026, with a full migration guide added covering breaking changes from Sonnet 4.5 and Claude 3.x. Several tools — including code execution, web fetch, programmatic tool calling, tool search, and memory tool — graduated from beta to general availability. Two previously deprecated models (`claude-3-7-sonnet-20250219` and `claude-3-5-haiku-20241022`) reached their retirement date of February 19, 2026.

---

## Significant Changes

### Models

- **Claude Sonnet 4.6 is now available**: `claude-sonnet-4-6` is listed as a current model alongside Opus 4.6 and Haiku 4.5. Priced at $3/MTok input and $15/MTok output (same as Sonnet 4.5).
  > "Claude Sonnet 4.6 combines strong intelligence with fast performance, featuring improved agentic search capabilities and free code execution when used with web search or web fetch."
  - *Implication*: Sonnet 4.6 defaults to `high` effort, unlike Sonnet 4.5 which had no effort parameter. Migrating users should explicitly set `output_config: { effort: "low" }` to match prior latency and cost behavior.
  - *Source*: [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

- **Two models retired today**: `claude-3-7-sonnet-20250219` and `claude-3-5-haiku-20241022` have reached their February 19, 2026 retirement date. Requests to these models will now fail.
  > Deprecated model retirement date: `February 19, 2026`
  - *Implication*: Any integrations still using these model IDs must switch to a supported model immediately. Recommended replacements are `claude-opus-4-6` (for Sonnet 3.7) and `claude-haiku-4-5-20251001` (for Haiku 3.5).
  - *Source*: [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations.md)

- **Sonnet 4.6 knowledge cutoff**: Training data cutoff is January 2026; reliable knowledge cutoff is August 2025.
  - *Source*: [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

### Migration Guide (New Sonnet 4.6 Section — +329 Lines)

A comprehensive Sonnet 4.6 migration section was added to the migration guide. This is the largest change in this diff.

- **Breaking: Assistant message prefilling removed**: Prefilling assistant messages now returns a `400` error on Sonnet 4.6 (as is already the case on Opus 4.6).
  > "Prefilling assistant messages returns a 400 error on Sonnet 4.6. Use structured outputs, system prompt instructions, or `output_config.format` instead."
  - *Implication*: Any code that sets a last-turn assistant message (e.g., starting a response with `{`) to control output format must migrate. Common alternatives: structured outputs, `output_config.format`, or direct system prompt instructions.
  - *Source*: [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **Breaking: Tool parameter JSON escaping may differ**: JSON string escaping in tool call arguments may differ from Sonnet 4.5 (e.g., Unicode escape handling, forward slash escaping). Standard JSON parsers (`json.loads()`, `JSON.parse()`) handle this transparently; only custom string-based parsers are affected.
  - *Source*: [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **Recommended: Set effort explicitly when migrating from Sonnet 4.5**: Sonnet 4.6 defaults to `effort: "high"`, which may increase latency vs. Sonnet 4.5 if left unset.
  > "Sonnet 4.6 defaults to an effort level of `high`, in contrast to Sonnet 4.5 which had no effort parameter. Consider adjusting the effort parameter as you migrate."
  ```python
  # Recommended for users migrating without extended thinking
  response = client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=8192,
      output_config={"effort": "low"},
      messages=[{"role": "user", "content": "Your prompt here"}],
  )
  ```
  - *Source*: [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **Recommended: Remove `fine-grained-tool-streaming-2025-05-14` beta header**: Fine-grained tool streaming is now GA on Sonnet 4.6 and requires no header.
  - *Source*: [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **Recommended: Migrate `output_format` to `output_config.format`**: The `output_format` parameter is deprecated. Use `output_config.format` for structured outputs.
  ```python
  # Before
  response = client.messages.create(output_format={"type": "json_schema", "schema": {...}}, ...)
  # After
  response = client.messages.create(output_config={"format": {"type": "json_schema", "schema": {...}}}, ...)
  ```
  - *Source*: [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

### Tools

- **Code execution is now free when combined with web tools**: When `web_search_20260209` or `web_fetch_20260209` is included in an API request, code execution incurs no additional charges beyond standard token costs.
  > "Code execution is free when used with web search or web fetch. When either tool is included in your API request, there are no additional charges for code execution beyond standard input and output token costs."
  - *Implication*: Developers using web search or web fetch can add sandboxed code execution to filter and process results at no extra per-execution cost.
  - *Source*: [What's new in Claude 4.6](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6.md), [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

- **Web search and web fetch support dynamic filtering (new tool versions)**: Opus 4.6 and Sonnet 4.6 can now write and execute code to filter search/fetch results before they reach the context window.
  > "Claude can write and execute code to filter results before they reach the context window, keeping only relevant information and improving accuracy while reducing token consumption. To enable dynamic filtering, use the `web_search_20260209` or `web_fetch_20260209` tool versions."
  - *Implication*: Upgrading to the new tool version strings is required to enable dynamic filtering; older tool versions remain supported.
  - *Source*: [What's new in Claude 4.6](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6.md)

- **Multiple tools graduate to GA** (no beta header required):
  - Code execution tool
  - Web fetch tool
  - Programmatic tool calling
  - Tool search tool
  - Tool use examples
  - Memory tool
  - Web search tool (already noted in the February 17 release notes)
  - *Implication*: Remove any beta headers previously required for these features. The `fine-grained-tool-streaming-2025-05-14` header can also be dropped.
  - *Source*: [What's new in Claude 4.6](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6.md), [Release notes overview](https://platform.claude.com/docs/en/release-notes/overview.md)

### Agent SDK

- **Secure deployment page: section renamed to "Threat model"**: The section "What are we protecting against?" has been renamed to "## Threat model" and updated to reference Claude Opus 4.6 specifically.
  > "Agents can take unintended actions due to prompt injection (instructions embedded in content they process) or model error. Claude models are designed to resist this, and as analyzed in the model card, Claude Opus 4.6 is the most robust frontier model available."
  - *Implication*: Cosmetic rename with a minor content update; no behavior changes. Developers should review to confirm the threat model still matches their deployment requirements.
  - *Source*: [Secure deployment](https://platform.claude.com/docs/en/agent-sdk/secure-deployment.md)

- **Agent SDK hosting page: FAQ section heading level corrected**: `# FAQ` changed to `## FAQ` (heading hierarchy fix, no content changes).
  - *Source*: [Hosting](https://platform.claude.com/docs/en/agent-sdk/hosting.md)

### Pricing

- **Pricing table updated with Claude Sonnet 4.6 rows**: Sonnet 4.6 added to all pricing tables (base, batch, long context, tool use).
  - Base: $3/MTok input, $15/MTok output
  - Batch: $1.50/MTok input, $7.50/MTok output
  - Long context (>200K tokens): $6/MTok input, $22.50/MTok output
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

### System Prompts

- **Claude Sonnet 4.6 system prompt published** (February 17, 2026): The claude.ai/mobile system prompt for Sonnet 4.6 is now documented. Notable differences vs. the Opus 4.6 system prompt:
  - Sonnet 4.6's reliable knowledge cutoff is listed as **August 2025** (vs. May 2025 for Opus 4.6).
  - Product listing includes "Claude in Powerpoint" as a new beta product alongside Chrome, Excel, and Cowork.
  - The `<responding_to_mistakes_and_criticism>` and `<evenhandedness>` instruction blocks are included in the Sonnet 4.6 system prompt.
  - *Source*: [System prompts](https://platform.claude.com/docs/en/release-notes/system-prompts.md)

### Release Notes

- **February 17, 2026 entry added** to the release notes overview: Documents Sonnet 4.6 launch, code execution going free with web tools, web search/programmatic tool calling going GA, and other tools graduating to GA.
  - *Source*: [Release notes overview](https://platform.claude.com/docs/en/release-notes/overview.md)

---

## Migration Guidance

### Migrating to Claude Sonnet 4.6 from Sonnet 4.5

**Breaking changes:**

1. **Remove assistant message prefills** — returns `400` on Sonnet 4.6. Use structured outputs or system prompt instructions instead.
2. **Verify tool parameter parsing** — JSON escaping may differ. Use standard JSON parsers (`json.loads()` / `JSON.parse()`).
3. **Set effort explicitly** — Sonnet 4.6 defaults to `high` effort; set `output_config: { effort: "low" }` to match Sonnet 4.5 latency/cost profile if not using extended thinking.

**Recommended cleanup:**
- Remove `fine-grained-tool-streaming-2025-05-14` beta header
- Replace `output_format` with `output_config.format`

### Retiring Models — Action Required Today

`claude-3-7-sonnet-20250219` and `claude-3-5-haiku-20241022` are retired as of 2026-02-19. Migrate to:
- `claude-opus-4-6` — recommended replacement for Sonnet 3.7
- `claude-haiku-4-5-20251001` — recommended replacement for Haiku 3.5

---

## Notable Details

- **Sonnet 4.6 effort default differs from all prior Sonnet models**: This is the first Sonnet model with a non-null default effort level (`high`). Operators not explicitly setting effort will see higher latency than with Sonnet 4.5 out of the box.
- **New web tool version strings**: Dynamic filtering requires `web_search_20260209` and `web_fetch_20260209`. These are distinct from prior tool versions; existing tool version strings still work but won't support dynamic filtering.
- **1M token context window for Sonnet 4.6 (beta)**: Available via the `context-1m-2025-08-07` beta header; long context pricing applies above 200K input tokens.
- **Sonnet 4.6 supports adaptive thinking**: Sonnet 4.6 also supports `thinking: {type: "adaptive"}` for computer use and agentic workloads; Sonnet 4.6 continues to support manual extended thinking with `budget_tokens` via the `interleaved-thinking-2025-05-14` header (unlike Opus 4.6, where this header is deprecated).
- **Guardrails documentation (minor)**: The four `strengthen-guardrails` pages (`handle-streaming-refusals`, `increase-consistency`, `keep-claude-in-character`, `reduce-prompt-leak`) and `content-moderation.md` each received minor model reference updates (likely Sonnet 4.6 added to examples). No new behavioral guidance.
- **`intro.md` updated**: Minor reference updates consistent with Claude 4.6 family availability.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `models/migration-guide.md` | Modified | +329/-2 | Full Sonnet 4.6 migration guide added: breaking changes, recommended changes, effort tuning, checklist |
| `release-notes/system-prompts.md` | Modified | +129/-2 | Claude Sonnet 4.6 system prompt published (Feb 17, 2026) |
| `about-claude/models/overview.md` | Modified | +39/-39 | Model listing updated to include Sonnet 4.6 as current model |
| `about-claude/pricing.md` | Modified | +26/-7 | Sonnet 4.6 added to all pricing tables |
| `about-claude/models/whats-new-claude-4-6.md` | Modified | +28/-3 | Added: code execution free with web tools, dynamic filtering, GA tool list |
| `agent-sdk/secure-deployment.md` | Modified | +16/-16 | "What are we protecting against?" renamed to "Threat model" |
| `about-claude/model-deprecations.md` | Modified | +18/-17 | Sonnet 4.6 added to model status table; deprecated models updated |
| `release-notes/overview.md` | Modified | +6/-0 | February 17, 2026 entry added |
| `about-claude/models/choosing-a-model.md` | Modified | +4/-4 | Model selection matrix updated to include Sonnet 4.6 |
| `agent-sdk/hosting.md` | Modified | +4/-4 | FAQ section heading level corrected (# → ##) |
| `agent-sdk/python.md` | Modified | +2/-2 | Minor model reference update |
| `intro.md` | Modified | +2/-2 | Minor model reference update |
| `test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md` | Modified | +3/-3 | Minor model reference update |
| `test-and-evaluate/strengthen-guardrails/reduce-prompt-leak.md` | Modified | +2/-2 | Minor model reference update |
| `about-claude/use-case-guides/content-moderation.md` | Modified | +7/-7 | Minor model reference update |
| `test-and-evaluate/strengthen-guardrails/increase-consistency.md` | Modified | +1/-1 | Minor model reference update |
| `test-and-evaluate/strengthen-guardrails/keep-claude-in-character.md` | Modified | +1/-1 | Minor model reference update |

---
*Generated from Claude API documentation changes detected on 2026-02-19*
