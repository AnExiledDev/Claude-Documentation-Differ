# Claude API Documentation Changes — 2026-04-09

## Summary

This update documents the launch of Claude Managed Agents in public beta and the `ant` CLI tool, both announced on April 8, 2026. The pricing page was significantly restructured to introduce Managed Agents billing (tokens + session runtime), and the migration guide received a major expansion covering Claude Opus 4.6 and Sonnet 4.6 upgrades across all supported SDKs.

## Significant Changes

### Claude Managed Agents

- **Claude Managed Agents launched in public beta**: A fully managed agent harness for running Claude as an autonomous agent with secure sandboxing, built-in tools, and server-sent event streaming. All endpoints require the `managed-agents-2026-04-01` beta header.
  > "We've launched **Claude Managed Agents** in public beta, a fully managed agent harness for running Claude as an autonomous agent with secure sandboxing, built-in tools, and server-sent event streaming. Create agents, configure containers, and run sessions through the API."
  - *Implication*: Developers can now delegate orchestration and infrastructure management to Anthropic rather than building their own agent loops.
  - *Source*: [Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

- **New Managed Agents pricing model**: Managed Agents sessions are billed on two dimensions — tokens (at standard model rates) and session runtime.
  > "Session runtime: $0.08 per session-hour. Runtime is measured to the millisecond and accrues only while the session's status is `running`. Time spent `idle` (waiting for your next message or a tool confirmation), `rescheduling`, or `terminated` does not count toward runtime."
  - *Implication*: Idle time is not billed; developers should design sessions to minimize unnecessary `running` state. Session runtime replaces Code Execution container-hour billing within Managed Agents sessions.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

- **Pricing modifiers that do NOT apply to Managed Agents**: The Batch API discount, fast mode premium, data residency multiplier, long context premium, and third-party platform pricing all do not apply to Managed Agents sessions.
  > "The following Messages API modifiers do **not** apply to Claude Managed Agents sessions: Batch API discount (Sessions are stateful and interactive. There is no batch mode.), Fast mode premium, Data residency multiplier, Long context premium, Third-party platform pricing."
  - *Implication*: Managed Agents sessions use a separate billing model; cost calculations for existing Messages API workflows do not translate directly.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

### New `ant` CLI Tool

- **`ant` CLI launched**: A command-line client for the Claude API that enables faster interaction with the API, native integration with Claude Code, and versioning of API resources in YAML files.
  > "We've launched the **`ant` CLI**, a command-line client for the Claude API that enables faster interaction with the Claude API, native integration with Claude Code, and versioning of API resources in YAML files."
  - *Implication*: Developers can now interact with the Claude API from the terminal and script workflows without SDK setup. The get-started page now includes a CLI tab alongside cURL, Python, TypeScript, and Java.
  - *Source*: [Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

### Models

- **Claude Mythos Preview announced**: Available as a gated research preview for defensive cybersecurity work as part of Project Glasswing. Access is invitation-only with no self-serve sign-up.
  > "Claude Mythos Preview is offered separately as a research preview model for defensive cybersecurity workflows as part of Project Glasswing. Access is invitation-only and there is no self-serve sign-up."
  - *Implication*: This model is not accessible through standard API credentials; developers interested must apply through Project Glasswing.
  - *Source*: [Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

- **Messages API now available on Amazon Bedrock (research preview)**: A new endpoint at `/anthropic/v1/messages` on Bedrock uses the same request shape as the first-party Claude API, available in `us-east-1`.
  > "The Messages API is now available on Amazon Bedrock as a research preview. The new Claude in Amazon Bedrock endpoint at `/anthropic/v1/messages` uses the same request shape as the first-party Claude API and runs on AWS-managed infrastructure with zero operator access."
  - *Implication*: Developers can use first-party Claude API request shapes on Bedrock infrastructure without adapting to Bedrock-specific formats. Contact an Anthropic account executive to request access.
  - *Source*: [Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

### Migration Guide — Claude 4.6

- **Comprehensive Claude 4.6 migration guide added**: The migration guide was substantially expanded (+77 lines) to cover Opus 4.6 and Sonnet 4.6 upgrades with breaking changes, recommended changes, and a migration checklist. Multi-language examples are provided for Python, TypeScript, C#, Go, Java, PHP, and Ruby.

  **Breaking changes documented:**
  - **Prefill removal**: Prefilling assistant messages returns a `400` error on Claude 4.6 models. Migrate to structured outputs, system prompt instructions, or `output_config.format`.
  - **Tool parameter quoting**: Claude 4.6 may produce different JSON string escaping in tool call arguments. Standard JSON parsers handle this automatically; custom string parsers may need updates.

  **Recommended (non-breaking) changes documented:**
  - Migrate `thinking: {type: "enabled", budget_tokens: N}` → `thinking: {type: "adaptive"}` with the effort parameter (`budget_tokens` is deprecated on 4.6).
  - Remove `effort-2025-11-24` beta header (effort is now GA).
  - Remove `fine-grained-tool-streaming-2025-05-14` beta header (now GA).
  - Remove `interleaved-thinking-2025-05-14` beta header (adaptive thinking enables interleaved thinking automatically on Opus 4.6).
  - Migrate `output_format` → `output_config.format` (old parameter deprecated).

  > "Note that the migration also moves from `client.beta.messages.create` to `client.messages.create`. Adaptive thinking and effort are GA features and do not require the beta SDK namespace or any beta headers."
  - *Implication*: Developers upgrading to claude-opus-4-6 or claude-sonnet-4-6 should work through this checklist before deploying to production.
  - *Source*: [Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **Sonnet 4.6 effort default warning**: Sonnet 4.6 defaults to `high` effort, unlike Sonnet 4.5 which had no effort parameter.
  > "Sonnet 4.6 defaults to an effort level of `high`, in contrast to Sonnet 4.5 which had no effort parameter. Consider adjusting the effort parameter as you migrate from Sonnet 4.5 to Sonnet 4.6. If not explicitly set, you may experience higher latency with the default effort level."
  - *Implication*: Migrations from Sonnet 4.5 that don't explicitly set effort may see increased latency. Set `output_config: {effort: "low"}` to match prior behavior.
  - *Source*: [Migration Guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

### Pricing Page Restructuring

- **"Agent use case pricing examples" section removed**: The previous sections (`## Agent use case pricing examples`, `### Customer support agent example`, `### General agent workflow pricing`) were replaced by the new `## Claude Managed Agents pricing` section with formal token + session runtime billing documentation.
  - *Implication*: The Managed Agents billing model is now officially documented with concrete rates rather than illustrative examples.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

- **Claude Opus 4.6 and Sonnet 4.6 added to all pricing tables**: Model pricing, batch processing, and tool use system prompt token count tables now include Claude Opus 4.6 ($5/$25 per MTok) and Claude Sonnet 4.6 ($3/$15 per MTok).
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

### Get Started / Introduction

- **Get started page updated to `claude-opus-4-6`**: All quickstart examples now use `claude-opus-4-6` as the default model, replacing prior model IDs. A new CLI tab (using `ant`) was added alongside existing cURL, Python, TypeScript, and Java tabs.
  - *Source*: [Get Started](https://platform.claude.com/docs/en/get-started.md)

- **Intro page updated with Claude Managed Agents comparison table**: The intro page now presents a side-by-side table comparing the Messages API and Claude Managed Agents, and prominently lists Claude Opus 4.6, Sonnet 4.6, and Haiku 4.5 as the latest generation.
  - *Source*: [Intro to Claude](https://platform.claude.com/docs/en/intro.md)

## Notable Details

- **`managed-agents-2026-04-01` beta header required**: All Claude Managed Agents API endpoints require this header. This follows the established beta header pattern (cf. `effort-2025-11-24`, `output-300k-2026-03-24`).
- **Session runtime billing granularity**: Runtime is measured to the millisecond, not rounded to the nearest minute or hour. Only `running` status accrues charges — `idle`, `rescheduling`, and `terminated` states do not.
- **Managed Agents worked example**: The pricing page includes a concrete one-hour coding session example showing $0.705 total ($0.25 input + $0.375 output + $0.08 runtime) with a variant showing savings from prompt caching ($0.525 total).
- **Use-case guide and guardrail pages updated**: Several use-case guides (content moderation, legal summarization, ticket routing) and guardrail pages (increase-consistency, reduce-latency, reduce-prompt-leak) received minor model reference updates (+1–5 / -1–4 lines), likely updating model IDs referenced in examples.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| models/migration-guide.md | Modified | +77/-3 | Major expansion: Opus 4.6 and Sonnet 4.6 migration sections with breaking changes, recommended changes, multi-SDK code examples, and migration checklist |
| pricing.md | Modified | +56/-32 | New Claude Managed Agents pricing section (tokens + $0.08/session-hour runtime); old agent use-case examples replaced; 4.6 models added to all pricing tables |
| get-started.md | Modified | +73/-7 | Updated to claude-opus-4-6 as default model; new CLI tab added using `ant` |
| intro.md | Modified | +8/-0 | Added Messages API vs Managed Agents comparison table; updated latest model listings to 4.6 |
| release-notes/overview.md | Modified | +9/-1 | Added April 8 (Managed Agents launch, `ant` CLI) and April 7 (Claude Mythos Preview, Messages API on Bedrock) entries |
| models/overview.md | Modified | +7/-3 | Added claude-opus-4-6 and claude-sonnet-4-6 to latest models comparison table |
| models/whats-new-claude-4-6.md | Modified | +3/-3 | Minor updates to Claude 4.6 feature page |
| use-case-guides/content-moderation.md | Modified | +5/-4 | Model reference updates (added Claude Opus 4.6 cost estimate) |
| use-case-guides/legal-summarization.md | Modified | +2/-2 | Model reference updates |
| use-case-guides/ticket-routing.md | Modified | +2/-2 | Model reference updates |
| strengthen-guardrails/increase-consistency.md | Modified | +1/-1 | Model reference update |
| strengthen-guardrails/reduce-latency.md | Modified | +2/-2 | Model reference updates |
| strengthen-guardrails/reduce-prompt-leak.md | Modified | +1/-1 | Model reference update |

---
*Generated from Claude API documentation changes detected on 2026-04-09*
