# Claude API Documentation Changes — 2026-04-17

## Summary

Claude Opus 4.7 launched on April 16, 2026, introducing several API breaking changes versus Opus 4.6: extended thinking budgets are removed, sampling parameters (`temperature`, `top_p`, `top_k`) now return a 400 error if set to non-default values, and thinking content is omitted from responses by default. A new tokenizer increases token counts by up to 35% for the same input text. Two new features arrive with the model: a new `xhigh` effort level and task budgets (beta).

---

## Significant Changes

### New Model: Claude Opus 4.7

- **Model launch (`claude-opus-4-7`)**: Anthropic's most capable generally available model, positioned for complex reasoning, agentic coding, knowledge work, and vision tasks. Priced at `$5 / $25` per MTok input/output — identical to Opus 4.6.
  > "Claude Opus 4.7 is our most capable generally available model to date. It is highly autonomous and performs exceptionally well on long-horizon agentic work, knowledge work, vision tasks, and memory tasks."
  - *Implication*: Drop-in pricing replacement for Opus 4.6, but API-level breaking changes require code changes before upgrading (see Migration Guidance below).
  - *Source*: [What's new in Claude Opus 4.7](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7.md)

- **New tokenizer**: Opus 4.7 uses a different tokenizer than all prior models. The same input text may produce **up to ~35% more tokens** (1x–1.35x multiplier, varying by content).
  > "Opus 4.7 uses a new tokenizer compared to previous models, contributing to its improved performance on a wide range of tasks. This new tokenizer may use up to 35% more tokens for the same fixed text."
  - *Implication*: `/v1/messages/count_tokens` will return different counts for Opus 4.7 vs. Opus 4.6 for the same prompt. Update `max_tokens` budgets, compaction triggers, and any client-side token estimation logic. The 1M context window now holds fewer words/characters (~555k words / ~2.5M unicode chars, compared to ~750k words / ~3.4M unicode chars on Opus 4.6).
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md), [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

- **Extended thinking not supported**: The `thinking: {type: "extended"}` / `budget_tokens` API is removed on Opus 4.7. Adaptive thinking is the only supported thinking-on mode.
  > "`Extended thinking` column: **No** [for Claude Opus 4.7]"
  - *Implication*: Setting `thinking: {type: "enabled", budget_tokens: N}` on Opus 4.7 returns a **400 error**. Adaptive thinking is off by default; set `thinking: {type: "adaptive"}` explicitly to enable it.
  - *Source*: [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

### Breaking API Changes (Opus 4.7)

- **Extended thinking budgets removed**: `thinking: {type: "enabled", budget_tokens: N}` returns a 400 error. Switch to adaptive thinking with the effort parameter to control thinking depth.
  ```python
  # Before (Opus 4.6)
  thinking = {"type": "enabled", "budget_tokens": 32000}

  # After (Opus 4.7)
  thinking = {"type": "adaptive"}
  output_config = {"effort": "high"}
  ```
  - *Source*: [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **Sampling parameters removed**: Setting `temperature`, `top_p`, or `top_k` to any non-default value returns a **400 error** on Opus 4.7. Omit these parameters entirely.
  > "Starting with Claude Opus 4.7, setting `temperature`, `top_p`, or `top_k` to any non-default value will return a 400 error. The safest migration path is to omit these parameters entirely from requests."
  - *Implication*: This is a breaking change when migrating from any 3.x model or Opus 4.1, which accepted sampling parameters. Note: `temperature = 0` never guaranteed identical outputs anyway.
  - *Source*: [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **Thinking content omitted by default (silent change)**: On Opus 4.7, thinking blocks appear in the response stream but the `thinking` field is **empty** unless the caller explicitly opts in with `display: "summarized"`. No error is raised; this is a silent behavioral change from Opus 4.6.
  ```python
  # To restore summarized thinking content:
  thinking = {
      "type": "adaptive",
      "display": "summarized",  # or "omitted" (new default)
  }
  ```
  > "If your product streams reasoning to users, the new default will appear as a long pause before output begins. Set `'display': 'summarized'` to restore visible progress during thinking."
  - *Implication*: Products that surface reasoning to users will silently break — users will see a long pause with no output. Must opt in with `display: "summarized"`.
  - *Source*: [What's new in Claude Opus 4.7](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7.md)

### New Features (Opus 4.7)

- **New `xhigh` effort level**: Adds a new tier above `high` to the effort parameter's existing scale (`low`, `medium`, `high`, `xhigh`, `max`). Recommended as the starting point for coding and agentic use cases.
  > "Start with the new `xhigh` effort level for coding and agentic use cases, and use a minimum of `high` effort for most intelligence-sensitive use cases."
  - *Implication*: At `max` or `xhigh` effort, set `max_tokens` to at least 64k as a starting point to give the model room to think and act.
  - *Source*: [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

- **Task budgets (beta)**: New `task_budget` field inside `output_config` lets callers give Claude an advisory token budget across a full agentic loop (thinking + tool calls + tool results + output). Set beta header `task-budgets-2026-03-13` to enable.
  ```python
  response = client.beta.messages.create(
      model="claude-opus-4-7",
      max_tokens=128000,
      output_config={
          "effort": "high",
          "task_budget": {"type": "tokens", "total": 128000},
      },
      messages=[...],
      betas=["task-budgets-2026-03-13"],
  )
  ```
  > "This is not a hard cap; it's a suggestion that the model is aware of. This is distinct from `max_tokens`, which is a hard per-request cap on generated tokens... while `task_budget` is an advisory cap across the full agentic loop."
  - *Implication*: Distinct from `max_tokens` — the model sees the task budget and uses it to self-pace. Minimum value: 20k tokens. Use `task_budget` for self-moderating agentic loops; use `max_tokens` as a hard per-request ceiling. Reserve for token-bound workloads; omit for open-ended quality-sensitive tasks.
  - *Source*: [What's new in Claude Opus 4.7](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7.md)

- **High-resolution image support**: Opus 4.7 is the first Claude model supporting images up to **2576px / 3.75MP** on the long edge (up from 1568px / 1.15MP on prior models). No beta header or opt-in required.
  > "Full-resolution images can use up to approximately 3x more image tokens than on prior models (up to 4,784 tokens per image, compared to the previous cap of roughly 1,600 tokens per image)."
  - *Implication*: Image token costs can increase by up to 3x at full resolution. Downsample before sending if the additional fidelity is not needed. Additionally, pointing/bounding-box coordinates are now **1:1 with actual pixels** — remove any scale-factor conversion code.
  - *Source*: [What's new in Claude Opus 4.7](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7.md)

### Beta Headers Graduating to GA

Three previously-beta features are now generally available on Opus 4.7 and should have their beta headers removed:

- **Effort parameter**: Remove `betas=["effort-2025-11-24"]`. The effort parameter is now GA; requests also no longer need the beta SDK namespace (`client.beta.messages.create` → `client.messages.create`).
- **Fine-grained tool streaming**: Remove `betas=["fine-grained-tool-streaming-2025-05-14"]`.
- **Interleaved thinking**: Remove `betas=["interleaved-thinking-2025-05-14"]`. Adaptive thinking automatically enables interleaved thinking on Opus 4.7 and Opus 4.6.

> "Note that the migration also moves from `client.beta.messages.create` to `client.messages.create`. Adaptive thinking and effort are GA features and do not require the beta SDK namespace or any beta headers."
  - *Source*: [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)

### Model Deprecations

- **Claude Opus 4 (`claude-opus-4-20250514`) deprecated**: Retirement scheduled for **June 15, 2026**. Recommended replacement: `claude-opus-4-7`.
- **Claude Sonnet 4 (`claude-sonnet-4-20250514`) deprecated**: Retirement scheduled for **June 15, 2026**. Recommended replacement: `claude-sonnet-4-6`.
  > "Claude Sonnet 4 (`claude-sonnet-4-20250514`) and Claude Opus 4 (`claude-opus-4-20250514`) are deprecated and will be retired on June 15, 2026."
  - *Implication*: Deprecated on April 14, 2026. Developers have roughly 60 days to migrate before requests to these models will fail.
  - *Source*: [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations.md), [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview.md)

- **Claude Haiku 3 (`claude-3-haiku-20240307`)**: Retirement date updated to **April 20, 2026** (minor correction from previously stated April 19). Recommended replacement: `claude-haiku-4-5-20251001`.
  - *Source*: [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations.md)

### Pricing Updates

- **Claude Opus 4.7 added to pricing tables**: Same rates as Opus 4.6 — `$5 / MTok` input, `$25 / MTok` output, `$6.25 / MTok` 5m cache write, `$10 / MTok` 1h cache write, `$0.50 / MTok` cache reads. Batch API: `$2.50 / $12.50` per MTok.
- **Data residency pricing now covers Opus 4.7**: The 1.1x multiplier for US-only inference (`inference_geo`) now explicitly applies to Opus 4.7 and Opus 4.6 and newer models.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

---

## New Pages

- **[whats-new-claude-4-7.md](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7.md)** — Complete summary of Claude Opus 4.7 at launch: new model specs, high-resolution image support, `xhigh` effort level, task budgets (beta), four breaking changes, capability improvements (knowledge work, memory, vision), and behavior changes. Includes before/after migration code for the breaking changes.

---

## Migration Guidance

The migration guide was substantially updated (+222/-37 lines) to document the Opus 4.7 upgrade path. Key required changes when upgrading from Opus 4.6:

- **Remove extended thinking budgets**:
  ```python
  # Before (Opus 4.6)
  client.messages.create(
      model="claude-opus-4-6",
      thinking={"type": "enabled", "budget_tokens": 32000},
      ...
  )
  # After (Opus 4.7)
  client.messages.create(
      model="claude-opus-4-7",
      thinking={"type": "adaptive"},
      output_config={"effort": "high"},
      ...
  )
  ```

- **Remove all sampling parameters**: Delete `temperature`, `top_p`, and `top_k` from any request to Opus 4.7.

- **Opt in to thinking display if needed**: If your UI shows reasoning content, add `"display": "summarized"` to the `thinking` object.

- **Update `max_tokens`**: Due to the new tokenizer (up to 35% more tokens per request) and high-resolution image token increases (up to 3x), increase `max_tokens` headroom across your request payloads, including compaction triggers. At `xhigh` or `max` effort, start at 64k tokens.

- **Remove scale-factor conversion for image coordinates**: Coordinates are now 1:1 with actual pixels on Opus 4.7.

- **Cybersecurity workloads**: Requests involving prohibited or high-risk security topics may receive refusals. Apply to the [Cyber Verification Program](https://claude.com/form/cyber-use-case) for reduced restrictions on legitimate security work.

For a complete migration checklist, see the [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md).

---

## Notable Details

- **`output_config.format` deprecation reminder**: The old `output_format` parameter for structured outputs is deprecated; use `output_config={"format": {...}}`. It remains functional but will be removed in a future model release.
- **Claude Managed Agents exempt from API breaking changes**: The migration guide explicitly notes: "These breaking changes apply to the Messages API only. If you use Claude Managed Agents, there are no breaking API changes for Claude Opus 4.7."
- **Batch API 300k output beta now includes Opus 4.7**: The `output-300k-2026-03-24` beta header applies to Opus 4.7, Opus 4.6, and Sonnet 4.6 on the Message Batches API.
- **Claude API skill for automated migration**: The migration guide introduces `/claude-api migrate` as a Claude Code command that can apply the Opus 4.7 migration changes (model ID swap, breaking parameter changes, prefill removal, effort calibration) automatically across a codebase.
- **System prompt updated for Opus 4.7**: The claude.ai / mobile app system prompt now identifies the current model as Claude Opus 4.7 and references product offerings including Claude Cowork, Claude in Chrome, Claude in Excel, and Claude in PowerPoint as beta products.
- **Opus 4.7 on AWS Bedrock in research preview**: Available as `anthropic.claude-opus-4-7` through "Claude in Amazon Bedrock" (research preview, `us-east-1` only, requires account executive access).

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `about-claude/models/whats-new-claude-4-7.md` | New | +165 | Full Opus 4.7 launch overview: features, breaking changes, behavior changes |
| `about-claude/models/migration-guide.md` | Modified | +222/-37 | Added Opus 4.7 migration guide; replaced Opus 4.6 migration section |
| `release-notes/system-prompts.md` | Modified | +155/-0 | Added full Claude Opus 4.7 system prompt (April 16, 2026) |
| `about-claude/models/overview.md` | Modified | +33/-31 | Opus 4.7 added as current recommended model; Opus 4.6 migration section replaced |
| `about-claude/pricing.md` | Modified | +14/-7 | Opus 4.7 added to model and batch pricing tables; tokenizer note added |
| `about-claude/model-deprecations.md` | Modified | +9/-8 | Opus 4.7 added as Active; Opus 4 / Sonnet 4 deprecated (June 15, 2026 retirement) |
| `release-notes/overview.md` | Modified | +4/-1 | April 16, 2026 entry: Claude Opus 4.7 launch |
| `about-claude/models/choosing-a-model.md` | Modified | +4/-4 | Updated recommended model references to Opus 4.7 |
| `get-started.md` | Modified | +9/-9 | Model name/reference updates |
| `about-claude/use-case-guides/legal-summarization.md` | Modified | +4/-14 | Model reference updates |
| `test-and-evaluate/develop-tests.md` | Modified | +11/-11 | Model reference updates |
| `test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md` | Modified | +7/-7 | Model reference updates |
| `intro.md` | Modified | +1/-1 | Model reference update |
| `about-claude/use-case-guides/content-moderation.md` | Modified | +1/-1 | Model reference update |
| `about-claude/use-case-guides/customer-support-chat.md` | Modified | +1/-1 | Model reference update |
| `test-and-evaluate/strengthen-guardrails/increase-consistency.md` | Modified | +1/-1 | Model reference update |
| `test-and-evaluate/strengthen-guardrails/reduce-prompt-leak.md` | Modified | +1/-1 | Model reference update |
| `resources/overview.md` | Modified | +2/-2 | Model reference updates |

---

*Generated from Claude API documentation changes detected on 2026-04-17*
