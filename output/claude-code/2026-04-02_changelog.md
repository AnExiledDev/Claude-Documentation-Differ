# Claude Code Documentation Changes — 2026-04-02

## Summary

Five documentation pages were updated in this batch with no new or removed pages. The most substantive changes are: a new `best` model alias added to the model configuration reference, a new "1M token context window" section in the Amazon Bedrock docs, and a rollback of the default primary model from Sonnet 4.6 to Sonnet 4.5 on both Amazon Bedrock and Google Vertex AI. The CLI reference also received a clarification that `--help` does not enumerate all available flags.

## Significant Changes

### Model Configuration

- **New `best` model alias**: A `best` alias has been added to the model alias table, pointing to the most capable available model (currently equivalent to `opus`). The `default` alias description was also tightened to clarify it is a special reset value rather than a model alias.
  > `best` — Uses the most capable available model, currently equivalent to `opus`
  > `default` — Special value that clears any model override and reverts to the recommended model for your account type. Not itself a model alias
  - *Implication*: Developers can now use `--model best` as a stable alias for the highest-capability model without tracking specific version names. The `default` clarification prevents potential confusion where users set `--model default` expecting a specific model.
  - *Source*: [Model Config](https://code.claude.com/docs/en/model-config.md)

### Amazon Bedrock

- **Default primary model rolled back to Sonnet 4.5**: The default primary model for Bedrock changed from `global.anthropic.claude-sonnet-4-6` to `us.anthropic.claude-sonnet-4-5-20250929-v1:0`. The small/fast model (Haiku 4.5) is unchanged.
  > Primary model: `us.anthropic.claude-sonnet-4-5-20250929-v1:0`
  - *Implication*: Bedrock users without a pinned model will now run on Sonnet 4.5. Pinning is required to use Sonnet 4.6 or the 1M context variants.
  - *Source*: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md)

- **1M token context window support documented**: A new section explains that Claude Opus 4.6 and Sonnet 4.6 support the 1M token context window on Amazon Bedrock. Claude Code enables the extended context automatically when a 1M model variant is selected. To opt in manually for a pinned model, append `[1m]` to the model ID.
  > Claude Code automatically enables the extended context window when you select a 1M model variant. To enable the 1M context window for your pinned model, append `[1m]` to the model ID.
  - *Implication*: Bedrock users can now access 1M context capacity without switching providers, using a simple suffix on the model ID pin (e.g., `claude-sonnet-4-6[1m]`).
  - *Source*: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md)

### Google Vertex AI

- **Default primary model rolled back to Sonnet 4.5**: The default primary model for Vertex AI changed from `claude-sonnet-4-6` to `claude-sonnet-4-5@20250929`. The small/fast model (Haiku 4.5) is unchanged.
  > Primary model: `claude-sonnet-4-5@20250929`
  - *Implication*: Vertex AI users without a pinned model will use Sonnet 4.5 as the default. Pinning is required to use Sonnet 4.6.
  - *Source*: [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai.md)

- **`VERTEX_REGION_CLAUDE_*` variable coverage wording softened**: The statement "Each model version has its own `VERTEX_REGION_CLAUDE_*` variable" was changed to "Most model versions have a corresponding `VERTEX_REGION_CLAUDE_*` variable."
  - *Implication*: Not every model has a dedicated region variable; the prior wording set an incorrect expectation. Developers should check the environment variables reference for the current list.
  - *Source*: [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai.md)

### GitHub Actions

- **Vertex AI example updated to Sonnet 4.5**: The GitHub Actions Vertex AI workflow example was updated to use `claude-sonnet-4-5@20250929` (from `claude-sonnet-4@20250514`) and the region environment variable was renamed from `VERTEX_REGION_CLAUDE_3_7_SONNET` to `VERTEX_REGION_CLAUDE_4_5_SONNET`.
  - *Implication*: Copy-paste example code now references a current, valid model ID and the correct region variable name, avoiding silent misconfiguration.
  - *Source*: [GitHub Actions](https://code.claude.com/docs/en/github-actions.md)

### CLI Reference

- **`--help` completeness caveat added**: The CLI flags section intro now states that `claude --help` does not list every available flag and that a flag's absence from `--help` does not mean it is unavailable.
  > `claude --help` does not list every flag, so a flag's absence from `--help` does not mean it is unavailable.
  - *Implication*: Developers should consult the full CLI reference docs rather than relying on `--help` output to discover all flags.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

## Notable Details

- The Bedrock default model changed format as well as version: the previous value `global.anthropic.claude-sonnet-4-6` used a floating global-inference prefix with no dated suffix, while the new default `us.anthropic.claude-sonnet-4-5-20250929-v1:0` uses the standard `us.` regional prefix and a pinned dated version. This may indicate a policy preference for explicit, dated version IDs in default configurations.
- The simultaneous rollback to Sonnet 4.5 on both Bedrock and Vertex AI, paired with the introduction of explicit 1M context window documentation for Sonnet 4.6, suggests Sonnet 4.6 is being positioned as an opt-in model for users who need extended context, while Sonnet 4.5 remains the stable default.
- The `best` and `default` alias clarifications formalize the alias semantics: `default` resets to account-recommended behavior (not a model itself), `best` always resolves to maximum capability, and named aliases (`sonnet`, `opus`, `haiku`) target model families.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| amazon-bedrock.md | Modified | +12/-5 | Added 1M context window section; default primary model changed to Sonnet 4.5; fixed link formatting in references |
| model-config.md | Modified | +2/-1 | Added `best` model alias; clarified `default` alias description |
| google-vertex-ai.md | Modified | +5/-5 | Default primary model changed to Sonnet 4.5; softened `VERTEX_REGION_CLAUDE_*` variable coverage wording |
| github-actions.md | Modified | +2/-2 | Updated Vertex AI example to Sonnet 4.5 model ID and corrected region env var name |
| cli-reference.md | Modified | +1/-1 | Added caveat that `--help` does not list all available flags |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-02*
