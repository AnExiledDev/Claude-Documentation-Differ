# Claude API Documentation Changes — 2026-05-01

## Summary

One page was modified: the API release notes, documenting the retirement of the 1M token context window beta for Claude Sonnet 4.5 and Claude Sonnet 4. Requests from affected integrations that exceed 200k tokens will now return an error. Migration to Claude Sonnet 4.6 or Claude Opus 4.6 is required to retain 1M token context access.

## Significant Changes

### Context Window / Beta Feature Retirement

- **1M Token Context Window Beta Retired for Claude Sonnet 4.5 and Claude Sonnet 4**: The `context-1m-2025-08-07` beta header is no longer functional on Claude Sonnet 4.5 and Claude Sonnet 4 as of April 30, 2026. Requests that exceed the standard 200k-token limit will now return an error.
  > We've retired the 1M token context window beta (`context-1m-2025-08-07`) for Claude Sonnet 4.5 and Claude Sonnet 4. The beta header now has no effect on these models, and requests exceeding the standard 200k-token context window return an error. To use the 1M context window, migrate to Claude Sonnet 4.6 or Claude Opus 4.6, where it's generally available at standard pricing with no beta header required.
  - *Implication*: Any production code passing the `anthropic-beta: context-1m-2025-08-07` header with Claude Sonnet 4.5 or Claude Sonnet 4 and submitting contexts over 200k tokens will now receive errors. Immediate migration to Claude Sonnet 4.6 or Claude Opus 4.6 is required to avoid service disruption. On the new models, the 1M context window is generally available with no beta header and no special pricing.
  - *Source*: [Release Notes Overview](https://platform.claude.com/docs/en/release-notes/overview.md)

## Migration Guidance

- **Retire `context-1m-2025-08-07` beta header**: Remove the beta header from requests targeting Claude Sonnet 4.5 or Claude Sonnet 4, and update the model to `claude-sonnet-4-6` or `claude-opus-4-6`. The 1M context window is available by default on these models.

  ```python
  # Before (breaks on Sonnet 4 / Sonnet 4.5 as of April 30, 2026)
  client.messages.create(
      model="claude-sonnet-4-5",
      extra_headers={"anthropic-beta": "context-1m-2025-08-07"},
      max_tokens=4096,
      messages=[...]
  )

  # After (1M context GA on Sonnet 4.6 / Opus 4.6, no beta header needed)
  client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=4096,
      messages=[...]
  )
  ```

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| release-notes/overview.md | Modified | +3 / -0 | Added April 30, 2026 entry retiring the 1M context window beta for Claude Sonnet 4.5 and Claude Sonnet 4 |

---
*Generated from Claude API documentation changes detected on 2026-05-01*
