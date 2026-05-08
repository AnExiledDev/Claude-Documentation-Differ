# Claude API Documentation Changes — 2026-03-15

## Summary

Two Agent SDK reference pages (Python and TypeScript) were updated to clarify the behavior of the `context-1m-2025-08-07` beta flag. Claude Opus 4.6 and Sonnet 4.6 now have a 1M token context window natively, making the beta flag a no-op for those models. The flag remains necessary for Claude Sonnet 4.5 and Sonnet 4.

## Significant Changes

### Agent SDK — Context Window Beta Flag Clarification

- **`context-1m-2025-08-07` no longer applies to Claude Opus 4.6 and Sonnet 4.6**: Both the Python and TypeScript Agent SDK reference pages have been updated to note that Opus 4.6 and Sonnet 4.6 include a 1M token context window by default. Passing `context-1m-2025-08-07` in the `betas` field has no effect on those models.

  > Claude Opus 4.6 and Sonnet 4.6 have a 1M token context window. Including `context-1m-2025-08-07` has no effect on those models.

  - *Implication*: Developers targeting Opus 4.6 or Sonnet 4.6 no longer need to include `context-1m-2025-08-07` in their `betas` configuration. The flag is still required to unlock the 1M-token context window on Claude Sonnet 4.5 and Sonnet 4.
  - *Source (Python)*: [Agent SDK Python Reference](https://platform.claude.com/docs/en/agent-sdk/python.md)
  - *Source (TypeScript)*: [Agent SDK TypeScript Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

- **TypeScript compatible model list corrected**: The `SdkBeta` compatibility table previously listed Claude Opus 4.6 as a model that requires `context-1m-2025-08-07` to enable the 1M context window. Opus 4.6 has been removed from that table, reflecting that the flag is unnecessary for it.

  > | `'context-1m-2025-08-07'` | Enables the 1 million token context window. | Claude Sonnet 4.5, Claude Sonnet 4 |

  - *Implication*: The TypeScript SDK docs now accurately reflect which models need the beta flag vs. which have 1M context natively. No code changes are required — the behavior was already correct; only the documentation was incorrect.
  - *Source*: [Agent SDK TypeScript Reference](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/agent-sdk/python.md` | Modified | +5 / -1 | Added note clarifying `context-1m-2025-08-07` has no effect on Opus 4.6 / Sonnet 4.6 |
| `docs/api/en/agent-sdk/typescript.md` | Modified | +5 / -1 | Removed Opus 4.6 from beta flag compatibility table; added clarifying note |

---
*Generated from Claude API documentation changes detected on 2026-03-15*
