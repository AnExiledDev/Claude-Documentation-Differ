# Claude Code Documentation Changes — 2026-05-15

## Summary

Four documentation pages were updated to reflect a behavior change in how Claude Code selects the small/fast model for background tasks on third-party cloud deployments (Bedrock, Vertex AI, and Foundry). The default small/fast model for these providers has been changed from a pinned Haiku model ID to the same model as the primary model, with guidance on how to opt back into Haiku via `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

## Significant Changes

### Configuration — Bedrock Default Model Behavior

- **Small/fast model default changed to primary model on Bedrock**: The default small/fast model (used for background tasks like session title generation) on Amazon Bedrock has changed from the pinned Haiku model ID `us.anthropic.claude-haiku-4-5-20251001-v1:0` to "Same as primary model". New explanatory text was added:
  > Background tasks such as session title generation use the small/fast model, normally a Haiku-class model. On Bedrock, Claude Code defaults this to the primary model because Haiku may not be enabled in every account or region. To use Haiku for background tasks, set `ANTHROPIC_DEFAULT_HAIKU_MODEL` to a model ID that is available in your account.
  - *Implication*: Bedrock users who relied on Haiku being silently used for background tasks will now consume primary model (Sonnet) tokens for those tasks. To restore Haiku for background tasks, explicitly set `ANTHROPIC_DEFAULT_HAIKU_MODEL`.
  - *Source*: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md)

- **`ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` comment clarified**: The inline code comment and the `env-vars.md` description for this variable were updated to reflect that the variable has no effect on Bedrock unless `ANTHROPIC_DEFAULT_HAIKU_MODEL` (or the deprecated `ANTHROPIC_SMALL_FAST_MODEL`) is also set.
  > On Bedrock, this only takes effect when `ANTHROPIC_DEFAULT_HAIKU_MODEL` or the deprecated `ANTHROPIC_SMALL_FAST_MODEL` is also set, since Bedrock otherwise uses the primary model for background tasks
  - *Implication*: Setting `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` alone on Bedrock is now a no-op; it must be paired with a Haiku model variable.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

## Minor Changes

- **[google-vertex-ai.md]**: Default small/fast model changed from `claude-haiku-4-5@20251001` to "Same as primary model". Added the same background-task explanation as Bedrock, directing users to set `ANTHROPIC_DEFAULT_HAIKU_MODEL` to opt into Haiku for background tasks. (+3/-1 lines) [AI override: thematically the same behavior change as the SIGNIFICANT Bedrock update, warrants a mention]
- **[microsoft-foundry.md]**: Added explanatory paragraph noting that Foundry defaults the small/fast model to the primary model because not every account has a Haiku deployment, and that `ANTHROPIC_DEFAULT_HAIKU_MODEL` should be set to re-enable Haiku for background tasks. (+2/-0 lines)
- **[env-vars.md]**: Updated description of `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` to document the conditional behavior on Bedrock. (+1/-1 lines)

## Migration Notes

- **Bedrock, Vertex AI, and Foundry users — background task model change**: If your cost accounting or quota management assumed Haiku was being used for background tasks on these providers, that is no longer the default. Set `ANTHROPIC_DEFAULT_HAIKU_MODEL` to an available Haiku model ID in your account/project to restore the previous behavior.
- **`ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` is now a conditional no-op**: On Bedrock, this environment variable only takes effect when a Haiku model is explicitly configured via `ANTHROPIC_DEFAULT_HAIKU_MODEL` or `ANTHROPIC_SMALL_FAST_MODEL`.

## Notable Details

- The change is consistent across all three major third-party cloud providers (Bedrock, Vertex AI, Foundry), suggesting a deliberate policy decision to avoid silent failures when Haiku is not provisioned in a user's cloud environment.
- `ANTHROPIC_SMALL_FAST_MODEL` is explicitly labeled `[DEPRECATED]` in `env-vars.md`; the replacement path for Haiku background tasks on cloud providers is `ANTHROPIC_DEFAULT_HAIKU_MODEL`.
- On Bedrock specifically, the code comment wording shifted from "Override the region for the small/fast model (Haiku)" to "Override the AWS region for the small/fast model (Bedrock and Mantle)" — the provider scope is now stated explicitly in the comment, and the model class name is dropped from the label since Haiku is no longer the assumed default.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| amazon-bedrock.md | Modified | SIGNIFICANT | +6/-3 | Default small/fast model changed to primary model; `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` comment clarified |
| google-vertex-ai.md | Modified | MINOR | +3/-1 | Default small/fast model changed to primary model; background task explanation added |
| microsoft-foundry.md | Modified | MINOR | +2/-0 | Background task model fallback explanation added |
| env-vars.md | Modified | MINOR | +1/-1 | `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` description updated with Bedrock conditional behavior |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-15*
