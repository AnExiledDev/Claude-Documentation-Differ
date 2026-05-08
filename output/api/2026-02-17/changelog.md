# Claude API Documentation Changes — 2026-02-17

## Summary

One documentation page was updated: the jailbreak and prompt injection mitigation guide. The change replaces deprecated assistant prefill patterns with structured outputs (`output_config`) for harmlessness screening, and updates the recommended lightweight model from Claude Haiku 3 to Claude Haiku 4.5.

## Significant Changes

### Guardrails & Safety

- **Prefill pattern deprecated in harmlessness screen examples**: The harmlessness screen examples previously used assistant prefilling (e.g., `| Assistant (prefill) | \( |`) to force a `(Y)` or `(N)` classification. These have been replaced with structured output via `output_config` and a JSON schema. The inline note that "prefilling is deprecated and not supported on Claude Opus 4.6 and Sonnet 4.5" has been removed since the examples no longer use prefill at all.

  > Previously:
  > `Reply with (Y) if it refers to harmful, illegal, or explicit activities. Reply with (N) if it's safe.`
  > `| Assistant (prefill) | \( |`

  > Now:
  > `Classify whether this content refers to harmful, illegal, or explicit activities.`
  > `Use output_config with a JSON schema to constrain the response:`

  ```json
  {
    "output_config": {
      "format": {
        "type": "json_schema",
        "schema": {
          "type": "object",
          "properties": {
            "is_harmful": { "type": "boolean" }
          },
          "required": ["is_harmful"],
          "additionalProperties": false
        }
      }
    }
  }
  ```

  - *Implication*: Developers building content moderation screens should migrate from assistant prefill patterns to `output_config` with a JSON schema. This approach is more robust and model-agnostic going forward.
  - *Source*: [Mitigate jailbreaks and prompt injections](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks.md)

- **Recommended lightweight model updated to Claude Haiku 4.5**: The harmlessness screen guidance previously recommended "Claude Haiku 3" as the lightweight pre-screening model. This has been updated to **Claude Haiku 4.5**.

  - *Implication*: Developers following this guide should update their harmlessness screen implementations to use `claude-haiku-4-5` (or equivalent identifier) as the screening model.
  - *Source*: [Mitigate jailbreaks and prompt injections](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks.md)

- **Tip callout removed**: A `<Tip>` block stating "Claude is far more resistant to jailbreaking than other major LLMs, thanks to advanced training methods like Constitutional AI" was removed from the top of the page.

  - *Implication*: Cosmetic/editorial change; no functional impact.
  - *Source*: [Mitigate jailbreaks and prompt injections](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks.md)

- **Advanced chained safeguard example also migrated**: The `harmlessness_screen` tool prompt in the multi-layered financial advisor chatbot example was likewise updated — the assistant prefill `(Y)/(N)` pattern removed and replaced with a reference to structured outputs for boolean classification.

  > `Use structured outputs to constrain the response to a boolean classification.`

  - *Implication*: Consistent with the primary example; both simple and advanced examples now use `output_config` rather than prefill.
  - *Source*: [Mitigate jailbreaks and prompt injections](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks.md)

## Migration Guidance

- **Prefill-based harmlessness screens → `output_config` structured outputs**: If you implemented a content moderation or compliance screening pattern following the previous documentation examples, update your prompts and API calls:

  ```json
  // Before (prefill pattern — deprecated, unsupported on Opus 4.6 and Sonnet 4.5)
  // Prompt: "Reply with (Y) if harmful, (N) if safe."
  // Request body includes an assistant prefill of "("

  // After (structured output)
  // Prompt: "Classify whether this content refers to harmful, illegal, or explicit activities."
  // Request body includes output_config:
  {
    "output_config": {
      "format": {
        "type": "json_schema",
        "schema": {
          "type": "object",
          "properties": { "is_harmful": { "type": "boolean" } },
          "required": ["is_harmful"],
          "additionalProperties": false
        }
      }
    }
  }
  ```

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks.md` | Modified | +25 / -8 | Replaced deprecated prefill-based harmlessness screen patterns with `output_config` structured outputs; updated recommended model from Haiku 3 to Haiku 4.5; removed Constitutional AI tip callout |

---
*Generated from Claude API documentation changes detected on 2026-02-17*
