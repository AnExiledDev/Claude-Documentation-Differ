# Claude API Documentation Changes — 2026-04-17

## Summary

This update introduces Claude Opus 4.7 across the `build-with-claude` documentation, adding a new **Task Budgets** beta feature for agentic token management, a new `xhigh` effort level, high-resolution image support, and a significant new prompt engineering section dedicated to Opus 4.7. Several breaking behavioral changes apply to Claude Opus 4.7: manual `budget_tokens` thinking is rejected with a 400 error, and thinking display now defaults to `"omitted"` rather than `"summarized"`. Code examples across 20+ pages have been updated from `claude-opus-4-6` to `claude-opus-4-7`.

---

## Significant Changes

### New Beta Feature: Task Budgets

- **`task_budget` in `output_config` (public beta, Claude Opus 4.7 only)**: A new advisory token budget for the full agentic loop, enabling the model to self-regulate token spend and finish gracefully as the budget is consumed. Activated via the `task-budgets-2026-03-13` beta header.

  > Task budgets let you tell Claude how many tokens it has for a full agentic loop, including thinking, tool calls, tool results, and output. The model sees a running countdown and uses it to prioritize work and finish gracefully as the budget is consumed.

  **Key details:**
  - Added to `output_config` as `task_budget: {type: "tokens", total: <N>}`
  - Optional `remaining` field carries budget across context compaction (e.g., when conversation history is summarized between turns)
  - Minimum `total` is **20,000 tokens**; values below return a 400 error
  - Budget is a **soft hint, not a hard cap** — Claude may briefly exceed it; `max_tokens` remains the enforced ceiling
  - The countdown tracks tokens Claude *sees this turn* (new output + new tool results), not cumulative payload size across turns
  - Too small a budget for the task can cause refusal-like behavior or early stopping
  - Supported in Python, TypeScript, Go, Java, C#, PHP, Ruby SDKs

  ```python
  response = client.beta.messages.create(
      model="claude-opus-4-7",
      max_tokens=128000,
      output_config={
          "effort": "high",
          "task_budget": {"type": "tokens", "total": 64000},
      },
      messages=[...],
      betas=["task-budgets-2026-03-13"],
  )
  ```

  - *Implication*: Enables cost and latency ceilings for multi-turn agentic loops without hard-cutting generation mid-response.
  - *Source*: [Task Budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets.md)

---

### Models: Claude Opus 4.7

- **Adaptive thinking is the only supported thinking mode on Claude Opus 4.7**: Manual `thinking: {type: "enabled", budget_tokens: N}` is **rejected with a 400 error** on Opus 4.7. Use `thinking: {type: "adaptive"}` with the `effort` parameter instead. Thinking is off by default unless `thinking: {type: "adaptive"}` is set explicitly.

  > On Claude Opus 4.7, adaptive thinking is the **only** supported thinking mode; manual `thinking: {type: "enabled", budget_tokens: N}` is no longer accepted.

  - *Implication*: Callers migrating from Opus 4.6 who pass `budget_tokens` will receive 400 errors and must update to adaptive mode.
  - *Source*: [Adaptive Thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md), [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md)

- **`thinking.display` defaults to `"omitted"` on Claude Opus 4.7** (changed from `"summarized"` on Opus 4.6): Thinking blocks appear in responses but their `thinking` field is empty unless you opt in. Set `display: "summarized"` explicitly to receive thinking summaries.

  > On Claude Opus 4.7, `thinking.display` defaults to `"omitted"`. Thinking blocks still appear in the response stream, but their `thinking` field is empty unless you explicitly opt in. This is a silent change from Claude Opus 4.6, where the default was `"summarized"`. To restore summarized thinking text on Claude Opus 4.7, set `thinking.display` to `"summarized"` explicitly.

  ```python
  thinking = {
      "type": "adaptive",
      "display": "summarized",
  }
  ```

  - *Implication*: Applications that relied on the default thinking summary text will silently receive empty thinking blocks on Opus 4.7 unless `display: "summarized"` is set.
  - *Source*: [Adaptive Thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md)

- **Claude Opus 4.7 added to structured outputs generally available list**: Structured outputs (`output_config.format` JSON outputs and `strict: true` tool use) are now GA on the Claude API for Claude Opus 4.7. On Amazon Bedrock, Opus 4.7 is available through the research preview endpoint, not the standard catalog.

  - *Source*: [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

---

### Effort Parameter: New `xhigh` Level

- **New `xhigh` effort level (Claude Opus 4.7 only)**: A new effort tier between `high` and `max`, positioned as the recommended default for coding and agentic workloads. The API default remains `high`; `xhigh` must be set explicitly.

  > | Level | Description | Typical use case |
  > |-------|-------------|------------------|
  > | `xhigh` | Extended capability for long-horizon work. Available on Claude Opus 4.7. | Long-running agentic and coding tasks (over 30 minutes) with token budgets in the millions |

  - Recommended starting point for coding, agentic search, repeated tool calling, and exploratory tasks
  - Comes with meaningfully higher token usage than `high`
  - At `xhigh` or `max` effort, set `max_tokens` to at least 64k to give the model room to think

  > **Start with `xhigh` for coding and agentic use cases**, and use `high` as the minimum for most intelligence-sensitive workloads. Step down to `medium` for cost-sensitive workloads, or up to `max` only when your evals show measurable headroom at `xhigh`.

  - *Implication*: `xhigh` is a new option that did not exist before; code that enumerates effort levels or validates against known values will need updating.
  - *Source*: [Effort](https://platform.claude.com/docs/en/build-with-claude/effort.md)

- **New section: Recommended effort levels for Claude Opus 4.7**: The effort page now contains model-specific guidance for Opus 4.7, including the stricter enforcement of effort at `low` and `medium` compared to Opus 4.6.

  > Claude Opus 4.7 also respects effort levels more strictly than Claude Opus 4.6, especially at `low` and `medium`. At lower effort levels, the model scopes its work to what was asked rather than going above and beyond.

  - *Source*: [Effort](https://platform.claude.com/docs/en/build-with-claude/effort.md)

---

### Vision: High-Resolution Image Support on Claude Opus 4.7

- **Increased max image resolution on Claude Opus 4.7**: Maximum resolution increased to **2576px on the long edge** (up from 1568px on all other models), with a new per-image token cap of ~4784 tokens (up from ~1568). High-resolution support is **automatic — no beta header required**.

  > Claude Opus 4.7 is the first Claude model with high-resolution image support. The maximum image resolution is 2576 pixels on the long edge, up from 1568 px on prior models. This unlocks performance gains on vision-heavy workloads and is particularly valuable for computer use, screenshot understanding, and document analysis.

  **Token cost comparison at Claude Opus 4.7's $5/M input token price:**
  | Image size | Tokens (Opus 4.7) | Cost / image |
  |---|---|---|
  | 1920×1080 px | ~2765 | ~$0.014 |
  | 2000×1500 px | ~4000 | ~$0.020 |

  - *Implication*: High-res images on Opus 4.7 use up to ~3x more tokens than on prior models. Downsample before uploading if fidelity is not needed.
  - *Source*: [Vision](https://platform.claude.com/docs/en/build-with-claude/vision.md)

- **Image limits section reorganized**: The "Basics and limits" section was renamed to "General limits" and expanded with explicit per-model image-per-request limits:
  - 20 images per message on claude.ai
  - 100 per API request for models with 200k-token context windows
  - 600 per API request for all other models
  - Max 8000×8000 px per image; reduced to 2000×2000 px when >20 images are in a single request

  - *Source*: [Vision](https://platform.claude.com/docs/en/build-with-claude/vision.md)

---

### Prompt Engineering: New Claude Opus 4.7 Section

- **Major new section "Prompting Claude Opus 4.7"** added to the prompting best practices page, with 12 subsections covering behavioral changes and tuning guidance for the new model. Key highlights:

  - **Response length**: Opus 4.7 calibrates verbosity to task complexity rather than defaulting to a fixed verbosity. Prompt explicitly for conciseness or elaboration if needed.

  - **Tool use triggering**: Opus 4.7 uses tools *less* than Opus 4.6, relying more on internal reasoning. Raising effort to `high` or `xhigh` increases tool usage in agentic contexts.

  - **Literal instruction following**: Opus 4.7 is more literal and explicit — it will not silently generalize an instruction from one item to another, nor infer requests not made. Good for structured pipelines; may require prompt updates for cases that relied on implicit generalization.

  - **Subagent spawning**: Opus 4.7 spawns fewer subagents by default, but this is steerable through prompting.

  - **Design and frontend defaults**: Opus 4.7 has a default "house style" (warm cream backgrounds, serif type, terracotta accents). Generic style overrides shift to a different fixed palette; use explicit color/type specs or a "propose options first" approach to get variety.

  - **Code review harnesses**: Opus 4.7 has higher recall and precision than prior models for bug-finding (reported as 11pp better recall on a hard internal eval). However, conservative review prompts ("only report high-severity issues") may be followed more literally, reducing *measured* recall. Prompt for coverage at the finding stage rather than asking the model to self-filter.

  - **Computer use**: Works up to **2576px / 3.75MP** resolution. 1080p recommended for performance/cost balance; 720p or 1366×768 for cost-sensitive workloads.

  - **Interactive coding products**: Opus 4.7 reasons more after user turns than in autonomous loops, which improves long-horizon coherence but uses more tokens. Recommend `xhigh` or `high` effort and reducing required user interactions.

  - *Source*: [Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

---

### Amazon Bedrock: Claude Opus 4.7 Availability

- **Claude Opus 4.7 is not available through the standard Bedrock model catalog**: A note was added to the `claude-on-amazon-bedrock.md` page clarifying that Opus 4.7 must be accessed through the research preview endpoint.

  > Claude Opus 4.7 is available on AWS through Claude in Amazon Bedrock, currently in research preview. It is not available through the standard Bedrock model catalog documented on this page.

  - *Source*: [Claude on Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md)

- **Claude Opus 4.7 model ID added to the Bedrock research preview table**: The model ID `anthropic.claude-opus-4-7` is now documented in the research preview model listing.

  - *Source*: [Claude in Amazon Bedrock (research preview)](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock-research-preview.md)

---

## New Pages

- **[task-budgets.md]** — Documents the new `task_budget` parameter in `output_config`, including how the token countdown works across agentic loop turns, how to carry budget across context compaction using the `remaining` field, how to measure baseline token usage before setting a budget, and interaction with `max_tokens` and `effort`. Includes SDK examples for Python, TypeScript, Go, Java, C#, PHP, and Ruby. [View](https://platform.claude.com/docs/en/build-with-claude/task-budgets.md)

---

## Notable Details

- **`xhigh` effort in the adaptive thinking table**: The effort-to-thinking-behavior table now includes `xhigh`: "Claude always thinks deeply with extended exploration. Available on Claude Opus 4.7." This aligns with `max` being documented as also now available on Claude Mythos Preview in addition to the existing models.

- **Manual thinking rejected on Opus 4.7 with a 400**: This is not just a deprecation — it's an immediate breaking change. Code passing `thinking: {type: "enabled"}` to `claude-opus-4-7` will fail. Affected: any caller using `extended-thinking`, `budget_tokens`, or the older thinking configuration.

- **Interleaved thinking on Opus 4.7**: Interleaved thinking (thinking between tool calls) is automatically enabled in adaptive mode on Claude Opus 4.7, matching Mythos Preview behavior.

- **Model example updates**: Code examples across ~20 pages (streaming, structured outputs, batch processing, token counting, citations, PDF support, etc.) were updated to use `claude-opus-4-7` as the primary example model, reflecting the shift in recommended baseline.

- **Claude Code Analytics model field updated**: The `model_breakdown[].model` example value was updated from `claude-opus-4-6` to `claude-opus-4-7` in the Claude Code Analytics API docs.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| task-budgets.md | New | +515 | New task budget beta feature for agentic loops |
| prompt-engineering/claude-prompting-best-practices.md | Modified | +165/-8 | Added 12-subsection "Prompting Claude Opus 4.7" section |
| vision.md | Modified | +83/-62 | High-res image support on Opus 4.7; limits section reorganized |
| compaction.md | Modified | +109/-107 | Model example updates |
| skills-guide.md | Modified | +129/-129 | Model example updates |
| streaming.md | Modified | +64/-64 | Model example updates |
| structured-outputs.md | Modified | +68/-68 | Claude Opus 4.7 added to GA list; model example updates |
| prompt-caching.md | Modified | +59/-58 | Model example updates |
| effort.md | Modified | +35/-14 | New `xhigh` level; new Opus 4.7 guidance section |
| pdf-support.md | Modified | +35/-35 | Model example updates |
| claude-on-vertex-ai.md | Modified | +33/-32 | Model example updates |
| token-counting.md | Modified | +42/-42 | Model example updates |
| context-editing.md | Modified | +44/-44 | Model example updates |
| working-with-messages.md | Modified | +43/-43 | Model example updates |
| adaptive-thinking.md | Modified | +52/-39 | Claude Opus 4.7 added; only adaptive mode on Opus 4.7 documented |
| handling-stop-reasons.md | Modified | +27/-27 | Model example updates |
| search-results.md | Modified | +25/-24 | Model example updates |
| extended-thinking.md | Modified | +15/-17 | Opus 4.7 breaking changes documented; `display` default note added |
| claude-on-amazon-bedrock.md | Modified | +8/-1 | Note added: Opus 4.7 not in standard Bedrock catalog |
| files.md | Modified | +12/-12 | Model example updates |
| usage-cost-api.md | Modified | +11/-11 | Model example updates |
| citations.md | Modified | +10/-10 | Model example updates |
| claude-in-microsoft-foundry.md | Modified | +20/-19 | Model example updates; tab label renamed Shell→cURL |
| batch-processing.md | Modified | +61/-60 | Model example updates |
| claude-in-amazon-bedrock-research-preview.md | Modified | +1/-0 | Claude Opus 4.7 model ID added to research preview table |
| administration-api.md | Modified | +5/-5 | Model example updates |
| claude-code-analytics-api.md | Modified | +5/-5 | Model breakdown example updated to Opus 4.7 |
| data-residency.md | Modified | +5/-5 | Model example updates |
| overview.md | Modified | +5/-5 | Model example updates |
| context-windows.md | Modified | +2/-2 | Model example updates |
| fast-mode.md | Modified | +2/-2 | Model example updates |
| api-and-data-retention.md | Modified | +1/-1 | Model example update |
| embeddings.md | Modified | +1/-1 | Model example update |

---
*Generated from Claude API documentation changes detected on 2026-04-17*
