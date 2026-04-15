# Claude API Documentation Changes — 2026-04-15

## Summary

Claude Sonnet 4 and Claude Opus 4 have been marked as deprecated as of April 14, 2026, with retirement dates varying by platform. Vertex AI multi-region endpoints now officially support the EU (`eu`) region in addition to the US. The refusal stop-reason fallback recommendation was updated to point to Haiku 4.5 rather than the now-deprecated Sonnet 4.

## Significant Changes

### Model Deprecations

- **Claude Sonnet 4 and Claude Opus 4 deprecated (April 14, 2026)**: Both models now carry deprecation warnings across all relevant documentation pages. Retirement dates differ by platform:
  - **Amazon Bedrock**: retiring October 14, 2026
  - **Vertex AI**: retiring September 14, 2026

  > `Claude Sonnet 4 <Tooltip tooltipContent="Deprecated as of April 14, 2026. Retiring October 14, 2026.">⚠️</Tooltip>`

  > `Claude Opus 4 <Tooltip tooltipContent="Deprecated as of April 14, 2026. Retiring October 14, 2026.">⚠️</Tooltip>`

  - *Implication*: Developers using `claude-sonnet-4-20250514` or `claude-opus-4-20250514` (and their Bedrock/Vertex equivalents) should plan migrations to supported models such as Sonnet 4.5, Opus 4.5, or Opus 4.6 before the respective retirement dates.
  - *Source*: [Claude on Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md), [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md), [Context Windows](https://platform.claude.com/docs/en/build-with-claude/context-windows.md), [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md), [Search Results](https://platform.claude.com/docs/en/build-with-claude/search-results.md), [Multilingual Support](https://platform.claude.com/docs/en/build-with-claude/multilingual-support.md)

### Vertex AI — EU Multi-Region Endpoint Now Available

- **EU multi-region endpoint (`eu`) is now generally available**: Previously described as "coming soon", the European Union multi-region endpoint is now documented as active alongside the existing US endpoint. All SDK code examples have been updated to reflect both options.

  > `Multi-region endpoints: Dynamic routing within a geographic area (for example, the United States or the European Union) for data residency with high availability`

  > `Set the region parameter to a multi-region identifier: "us" for the United States or "eu" for the European Union. The SDK routes requests to the corresponding multi-region endpoint (https://aiplatform.us.rep.googleapis.com or https://aiplatform.eu.rep.googleapis.com)`

  - *Implication*: Developers requiring EU data residency with high availability can now use `region="eu"` (or equivalent in their SDK) to route requests through `https://aiplatform.eu.rep.googleapis.com`. The 10% pricing premium over global endpoints applies to both multi-region options.
  - *Source*: [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md)

### Refusal Stop Reason — Fallback Model Updated

- **Tip for `refusal` stop reasons now recommends Haiku 4.5 instead of Sonnet 4**: The guidance for developers experiencing frequent `refusal` stop reasons with Sonnet 4.5 or Opus 4.1 previously suggested Sonnet 4 as a fallback. This has been updated to Haiku 4.5 (`claude-haiku-4-5-20251001`), consistent with Sonnet 4's deprecation.

  > Before: `you can try updating your API calls to use Sonnet 4 (claude-sonnet-4-20250514), which has different usage restrictions`
  >
  > After: `you can try updating your API calls to use Haiku 4.5 (claude-haiku-4-5-20251001), which has different usage restrictions`

  - *Implication*: Any internal runbooks or automation referencing Sonnet 4 as a `refusal` fallback should be updated to Haiku 4.5.
  - *Source*: [Handling Stop Reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons.md)

### Workspaces Console UI Copy

- **"Add Workspace" renamed to "Create workspace"**: The step in the workspace creation flow has been relabeled to match updated Claude Console UI text.
  - *Implication*: Minor UI label change; no functional impact.
  - *Source*: [Workspaces](https://platform.claude.com/docs/en/build-with-claude/workspaces.md)

## Notable Details

- The Vertex AI multi-region endpoint description previously listed only `us` as an active region with `eu` as "coming soon". The diff shows both the prose and all SDK code comments updated in a single pass across Python, TypeScript, C#, Go, Java, PHP, and Ruby examples — indicating a coordinated release of the EU endpoint.
- The deprecation tooltips on Bedrock and Vertex AI use different retirement dates for the same models (October 14 vs. September 14, 2026), reflecting platform-specific deprecation timelines.
- The `search-results.md` compatibility list now links Opus 4 and Sonnet 4 entries directly to the model deprecations page, giving developers a consistent path to migration information.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| claude-on-vertex-ai.md | Modified | +14/-14 | EU multi-region endpoint GA; Sonnet 4 and Opus 4 marked deprecated |
| claude-on-amazon-bedrock.md | Modified | +6/-6 | Sonnet 4 and Opus 4 marked deprecated with retirement date |
| extended-thinking.md | Modified | +2/-2 | Updated model lists to note Sonnet 4 and Opus 4 as deprecated |
| search-results.md | Modified | +2/-2 | Linked Opus 4 and Sonnet 4 to deprecation page |
| workspaces.md | Modified | +2/-2 | Renamed "Add Workspace" to "Create workspace" in UI step |
| context-windows.md | Modified | +1/-1 | Added "(deprecated)" label to Sonnet 4 in context window table prose |
| handling-stop-reasons.md | Modified | +1/-1 | Updated `refusal` stop reason fallback from Sonnet 4 to Haiku 4.5 |
| multilingual-support.md | Modified | +1/-1 | Added "(deprecated)" label to Opus 4 and Sonnet 4 in benchmark table header |

---
*Generated from Claude API documentation changes detected on 2026-04-15*
