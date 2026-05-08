# Claude API Documentation Changes — 2026-04-13

## Summary

One page was modified in the managed agents documentation: `managed-agents/files.md`. The changes correct the session ID prefix format (`sess_` → `sesn_`) and update all SDK code examples to require the `managed-agents-2026-04-01` beta header alongside `files-api-2025-04-14` when listing session-scoped files.

## Significant Changes

### Managed Agents — Files API (Beta)

- **Session ID prefix corrected: `sess_` → `sesn_`**: All SDK examples for listing session-scoped files have been updated to use `sesn_abc123` instead of the previously documented `sess_abc123`.
  > ```bash
  > # Before
  > curl -fsSL "https://api.anthropic.com/v1/files?scope_id=sess_abc123"
  > # After
  > curl -fsSL "https://api.anthropic.com/v1/files?scope_id=sesn_abc123"
  > ```
  - *Implication*: Developers using session-scoped file listing should verify they are passing the correct session ID format. If session IDs are obtained from the API directly, no change is required — this corrects documentation to reflect the actual session ID prefix returned by the service.
  - *Source*: [managed-agents/files.md](https://platform.claude.com/docs/en/managed-agents/files.md)

- **`managed-agents-2026-04-01` beta header now required for session-scoped file operations**: Examples for listing files by `scope_id` and downloading session-scoped files now include `managed-agents-2026-04-01` as a required beta header, combined with `files-api-2025-04-14`. Previously, only `files-api-2025-04-14` was shown.
  > ```bash
  > # Before
  > -H "anthropic-beta: files-api-2025-04-14"
  > # After
  > -H "anthropic-beta: managed-agents-2026-04-01,files-api-2025-04-14"
  > ```
  - *Implication*: Requests to list or download files scoped to a managed agent session must now include both beta headers. Requests using only `files-api-2025-04-14` may fail or return unexpected results when scoping by session.
  - *Source*: [managed-agents/files.md](https://platform.claude.com/docs/en/managed-agents/files.md)

  This beta header requirement was updated across **all SDK examples**:

  | SDK | Change |
  |-----|--------|
  | curl | Added `managed-agents-2026-04-01` to `-H "anthropic-beta: ..."` |
  | Python | Added `betas=["managed-agents-2026-04-01"]` to `client.beta.files.list()` |
  | TypeScript | Added `betas: ["managed-agents-2026-04-01"]` to `client.beta.files.list()` |
  | C# | Added `Betas = ["managed-agents-2026-04-01"]` to `FileListParams` |
  | Go | Added `Betas: []anthropic.AnthropicBeta{"managed-agents-2026-04-01"}` to `BetaFileListParams` |
  | Java | Added `.addBeta(AnthropicBeta.of("managed-agents-2026-04-01"))` to `FileListParams.builder()` |
  | PHP | Added `betas: ['managed-agents-2026-04-01']` to `$client->beta->files->list()` |
  | Ruby | Added `betas: ["managed-agents-2026-04-01"]` to `client.beta.files.list()` |

## Migration Guidance

- **Session-scoped file listing**: If you are calling `GET /v1/files?scope_id=<session_id>`, ensure:
  1. The session ID uses the `sesn_` prefix (not `sess_`)
  2. Both beta headers are included:
  ```bash
  -H "anthropic-beta: managed-agents-2026-04-01,files-api-2025-04-14"
  ```

  Python example (updated):
  ```python
  # Before
  files = client.beta.files.list(scope_id="sess_abc123")

  # After
  files = client.beta.files.list(
      scope_id="sesn_abc123",
      betas=["managed-agents-2026-04-01"],
  )
  ```

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| managed-agents/files.md | Modified | +22 / -11 | Session ID prefix corrected (`sess_` → `sesn_`); `managed-agents-2026-04-01` beta header added to all session-scoped file operation examples across 7 SDKs |

---
*Generated from Claude API documentation changes detected on 2026-04-13*
