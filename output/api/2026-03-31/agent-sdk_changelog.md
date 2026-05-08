# Claude API Documentation Changes — 2026-03-31

## Summary

Two Agent SDK reference pages (Python and TypeScript) were updated to document the retirement of the `context-1m-2025-08-07` beta feature, effective April 30, 2026. Developers using this beta header with Claude Sonnet 4.5 or Claude Sonnet 4 must migrate to Claude Sonnet 4.6 or Opus 4.6 to retain 1M-token context window access.

## Significant Changes

### Agent SDK — Beta Feature Retirement

- **`context-1m-2025-08-07` beta retired on April 30, 2026**: The documentation for the `SdkBeta` type in both the Python and TypeScript Agent SDKs has been updated from an informational `<Note>` to a `<Warning>`, and the description of compatible models and the beta's purpose has been removed. The warning now states that requests using this beta value will return a `400` error after the retirement date.

  > The `context-1m-2025-08-07` beta is retired as of April 30, 2026. Requests using this header with Claude Sonnet 4.5 or Sonnet 4 will return a 400 error. To use a 1M-token context window, migrate to Claude Sonnet 4.6 or Claude Opus 4.6, which include 1M context at standard pricing with no beta header required.

  - *Implication*: Any Agent SDK code that passes `'context-1m-2025-08-07'` in the `betas` option when targeting Claude Sonnet 4.5 or Claude Sonnet 4 will begin failing with HTTP 400 errors on or after April 30, 2026. Migration to `claude-sonnet-4-6` or `claude-opus-4-6` is required — no beta header is needed on those models.
  - *Source (Python)*: [Agent SDK Python Reference](https://platform.claude.com/docs/en/agent-sdk/python.md)
  - *Source (TypeScript)*: [Agent SDK TypeScript Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

- **TypeScript `QueryOptions.betas` field description simplified**: The inline description for the `betas` field in the `QueryOptions` table was updated from `Enable beta features (e.g., ['context-1m-2025-08-07'])` to simply `Enable beta features`, removing the now-retired example value.
  - *Implication*: Minor documentation cleanup; no behavioral change, but confirms the old example value should no longer be used.
  - *Source*: [Agent SDK TypeScript Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

- **TypeScript `SdkBeta` compatibility table removed**: The table listing `context-1m-2025-08-07` with its description and compatible models (Claude Sonnet 4.5, Claude Sonnet 4) has been removed entirely, replaced by the retirement warning.
  - *Implication*: The `SdkBeta` type literal (`"context-1m-2025-08-07"`) remains in the TypeScript type definition for now, but its use is explicitly discouraged and will soon be error-producing.

## Migration Guidance

- **Migrate off `context-1m-2025-08-07` before April 30, 2026**: Update model references and remove the beta header from `ClaudeAgentOptions` / `QueryOptions`.

  ```python
  # Python — Before
  result = await claude_code(prompt="...", options=ClaudeCodeOptions(
      model="claude-sonnet-4-5",
      betas=["context-1m-2025-08-07"],
  ))

  # Python — After (1M context included by default, no beta needed)
  result = await claude_code(prompt="...", options=ClaudeCodeOptions(
      model="claude-sonnet-4-6",
  ))
  ```

  ```typescript
  // TypeScript — Before
  await query({
    prompt: "...",
    model: "claude-sonnet-4-5",
    betas: ["context-1m-2025-08-07"],
  });

  // TypeScript — After
  await query({
    prompt: "...",
    model: "claude-sonnet-4-6",
  });
  ```

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `agent-sdk/python.md` | Modified | +4 / -4 | `context-1m-2025-08-07` note replaced with retirement warning |
| `agent-sdk/typescript.md` | Modified | +4 / -8 | `context-1m-2025-08-07` compatibility table and note replaced with retirement warning; `betas` field description simplified |

---
*Generated from Claude API documentation changes detected on 2026-03-31*
