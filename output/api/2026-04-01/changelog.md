# Claude API Documentation Changes — 2026-04-01

## Summary

Three pages were updated with a single behavioral clarification: the `context-1m-2025-08-07` beta retirement on April 30, 2026 will silently ignore the header rather than return a 400 error — but requests that exceed the standard 200k-token context window will still error. This correction appears consistently across the Agent SDK Python docs, TypeScript docs, and the release notes.

## Significant Changes

### Agent SDK / Beta Header Retirement Behavior

- **`context-1m-2025-08-07` retirement: header ignored, not rejected**: Documentation previously stated that using this beta header with Claude Sonnet 4.5 or Sonnet 4 after April 30, 2026 would return a 400 error. The docs now clarify that the header itself will have no effect — but any request whose prompt exceeds the standard 200k-token context window will return an error.

  > **Before:** "Requests using this header with Claude Sonnet 4.5 or Sonnet 4 will return a 400 error."
  >
  > **After:** "Passing this header with Claude Sonnet 4.5 or Sonnet 4 has no effect, and requests that exceed the standard 200k-token context window return an error."

  - *Implication*: Developers who continue passing the `context-1m-2025-08-07` header after April 30 won't get an immediate 400 on every request — instead, only prompts that actually exceed 200k tokens will fail. Regardless, migration to Claude Sonnet 4.6 or Opus 4.6 is the correct path for 1M context support.
  - *Source (Python SDK)*: [Agent SDK — Python](https://platform.claude.com/docs/en/agent-sdk/python.md)
  - *Source (TypeScript SDK)*: [Agent SDK — TypeScript](https://platform.claude.com/docs/en/agent-sdk/typescript.md)
  - *Source (Release Notes)*: [Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `agent-sdk/python.md` | Modified | +1/-1 | Clarified `context-1m-2025-08-07` retirement behavior: header ignored, not 400 |
| `agent-sdk/typescript.md` | Modified | +1/-1 | Same clarification as Python SDK |
| `release-notes/overview.md` | Modified | +1/-1 | Same clarification in March 30, 2026 release note entry |

---
*Generated from Claude API documentation changes detected on 2026-04-01*
