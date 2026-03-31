# Claude API Documentation Changes — 2026-03-31

## Summary

The release notes page was updated with a new March 30, 2026 entry covering two changes: an increase to the `max_tokens` cap on the Message Batches API for Claude Opus 4.6 and Sonnet 4.6, and an announced retirement of the 1M token context window beta for Claude Sonnet 4.5 and Claude Sonnet 4. No pages were added or removed.

## Significant Changes

### API

- **Message Batches API `max_tokens` raised to 300k**: The `max_tokens` cap on the Message Batches API has been increased to 300,000 tokens for Claude Opus 4.6 and Claude Sonnet 4.6. This is available via the `output-300k-2026-03-24` beta header.
  > We've raised the `max_tokens` cap to 300k on the [Message Batches API] for Claude Opus 4.6 and Sonnet 4.6. Include the `output-300k-2026-03-24` beta header to generate longer single-turn outputs for long-form content, structured data, and large code generation tasks.
  - *Implication*: Developers using the Message Batches API can now generate substantially longer outputs per request for batch workloads. Requires opting in with the `output-300k-2026-03-24` beta header.
  - *Source*: [Release Notes Overview](https://platform.claude.com/docs/en/release-notes/overview.md)

### Models / Deprecations

- **1M token context window beta retirement for Claude Sonnet 4.5 and Claude Sonnet 4**: Anthropic has announced that the 1M token context window beta (`context-1m-2025-08-07` header) will be retired for Claude Sonnet 4.5 and Claude Sonnet 4 on **April 30, 2026**. After that date, requests using this header on those models will return a 400 error.
  > We're retiring the 1M token context window beta for Claude Sonnet 4.5 and Claude Sonnet 4 on **April 30, 2026**. After that date, requests that include the `context-1m-2025-08-07` beta header on these models will return a 400 error. To continue using 1M context windows, migrate to [Claude Sonnet 4.6] or [Claude Opus 4.6], which support the full 1M token context window at standard pricing with no beta header required.
  - *Implication*: Applications relying on the `context-1m-2025-08-07` beta header with Sonnet 4.5 or Sonnet 4 must migrate to Claude Sonnet 4.6 or Claude Opus 4.6 before April 30, 2026. Both newer models support 1M context at standard pricing without requiring a beta header.
  - *Source*: [Release Notes Overview](https://platform.claude.com/docs/en/release-notes/overview.md)

## Migration Guidance

**Action required before April 30, 2026:** If your application sends requests to `claude-sonnet-4-5` or `claude-sonnet-4` with the `context-1m-2025-08-07` beta header, those requests will begin returning 400 errors after April 30, 2026. Migrate to Claude Sonnet 4.6 or Claude Opus 4.6, which support the full 1M token context window natively at standard pricing with no beta header.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/release-notes/overview.md` | Modified | +4 / -0 | Added March 30, 2026 release notes entry: Message Batches API 300k `max_tokens` for Opus 4.6/Sonnet 4.6; 1M context window beta retirement notice for Sonnet 4.5 and Sonnet 4 on April 30, 2026 |
