# Claude API Documentation Changes — 2026-05-19

## Summary

One page was modified: the Computer Use tool documentation received substantial additions (+46/-4 lines). The update adds a new "Diagnose click issues" troubleshooting section, benchmarked extended thinking effort recommendations per model, macOS Retina display handling guidance, prompt caching strategy for long agent loops, and a new best practices blog link. Several minor wording improvements were also made.

## Significant Changes

### Computer Use Tool

- **Benchmarked extended thinking effort recommendations**: New guidance documents which `effort` settings perform best for computer use tasks, based on internal benchmarking.
  > **Claude Opus 4.7:** use `high` as the default; use `low` for high-throughput or cost-sensitive workloads.
  > **Claude Sonnet 4.6 and Claude Opus 4.6:** use `medium` as the default (best accuracy-to-cost ratio). Avoid `max`, which adds token cost without improving accuracy on UI tasks. On these models, `low` uses *fewer* output tokens than disabling thinking entirely (fewer mistakes mean fewer retries), making it a strong option for cost-sensitive loops.
  - *Implication*: Developers running computer use in production can now apply model-specific effort tuning to reduce cost without sacrificing click accuracy.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

- **New "Diagnose click issues" troubleshooting section**: A structured table mapping click failure symptoms to likely causes and remediation steps, plus a note on model-level precision differences.
  > | Symptom | Likely cause | Try |
  > |---------|--------------|-----|
  > | Clicks consistently offset in one direction | `display_width_px`/`display_height_px` don't match the image dimensions actually sent, or the image exceeds API limits and is silently downscaled | Ensure display dimensions exactly match the resized screenshot; pre-downscale to fit within API limits |
  > | Clicks land in the right area but miss the target | Target is very small, detail was lost downscaling a 4K+ source, or aspect ratio was distorted | Set `enable_zoom: true`; capture at lower DPI or crop to the relevant region; preserve aspect ratio when resizing |
  > | Claude clicks the wrong element entirely | Ambiguous instruction, or visually similar elements nearby | Use positional prompts ("the blue Submit button in the bottom-right"); break the interaction into smaller steps |
  > | Accuracy is consistently poor | Screenshots sent above API limits, or resolution too low | Pre-downscale to fit within limits; try 1280x720 as a baseline |

  The section also clarifies relative model click precision:
  > **Model choice affects click precision.** Claude Sonnet 4.6 is more mechanically precise at clicking than Claude Opus 4.6 and is more robust when screenshots require heavy downscaling. Claude Opus 4.7 narrows that gap: its click precision is roughly comparable to Sonnet 4.6, and its higher resolution limit means less downscaling is needed.
  - *Implication*: Developers experiencing unreliable clicks now have a systematic diagnostic guide rather than needing to trial-and-error common causes.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

- **macOS Retina display handling note**: New note clarifying how Retina's 2× device pixel ratio interacts with coordinate mapping.
  > **macOS Retina displays** capture screenshots at a device pixel ratio of 2, so the image is twice the resolution of the logical screen coordinates. Either downscale the screenshot by 2x before sending, or halve the coordinates Claude returns before issuing the click.
  - *Implication*: Developers building computer use on macOS will encounter this commonly; missing this causes all clicks to be offset by a factor of 2.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

- **Prompt caching strategy for long agent loops**: New "Manage screenshot history for prompt caching" section documenting how to bound context size while keeping the cache prefix stable.
  > Long agent loops accumulate screenshots quickly (roughly 1,000–1,800 input tokens each). To keep [prompt caching](/docs/en/build-with-claude/prompt-caching) effective while bounding context:
  > - Place one `cache_control` breakpoint after the system prompt and tool definitions, and up to three more on the most recent `tool_result` blocks, advancing them each turn.
  > - Prune old screenshots in *batches*, not one each turn. Dropping a screenshot every turn changes the prefix every turn and invalidates the cache. A reasonable default is to keep the last 3 screenshots and prune every 25 turns, so the prefix stays byte-identical between prune events.
  - *Implication*: Batch-pruning on a fixed schedule (e.g., every 25 turns) rather than continuously is a non-obvious requirement to avoid cache invalidation — developers building long-running agentic loops should update their context management accordingly.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

- **Instruction ordering tip**: New item #6 added to the best practices list.
  > When constructing a user turn's `content` array, place the instruction text *before* the screenshot image. Providing the target description before the image is processed improves click accuracy.
  - *Implication*: A simple reordering of content array elements can measurably improve click reliability at no additional cost.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

## Minor Changes

- **computer-use-tool.md**: Minor wording updates — "The example above" → "The preceding example", "xml tags" → "XML tags", internal anchor link improvement for "Quick start" reference, "guidance below" → "guidance that follows". (+46/-4 lines total, bulk of changes are the significant additions above)

## Notable Details

- A new card link was added to the page footer pointing to an external blog post: [Best practices in detail](https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude), described as "Benchmarked recommendations for resolution, thinking effort, and context management." This suggests Anthropic has published companion benchmarking data outside the API docs.
- The `enable_zoom: true` parameter is referenced in the new click diagnostics table as a mitigation for small targets — this capability is mentioned in context without dedicated documentation in this diff, so developers interested in its full specification should consult the broader tool parameter reference.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| computer-use-tool.md | Modified | SIGNIFICANT | +46/-4 | Added click diagnostics table, extended thinking effort benchmarks, macOS Retina note, prompt caching screenshot strategy, instruction ordering tip, and new best-practices blog card |

---
*Generated from Claude API documentation changes detected on 2026-05-19*
