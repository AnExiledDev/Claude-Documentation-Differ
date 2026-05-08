# Claude API Documentation Changes — 2026-04-15

## Summary

One new experimental API endpoint has been added for triggering Claude Code routines over HTTP, and the CLI SDK documentation corrects a flag name in the `ant beta:sessions create` command. These are the only changes in this diff.

---

## Significant Changes

### Claude Code — New Routine Fire API

- **New experimental endpoint: `POST /v1/claude_code/routines/{routine_id}/fire`**: A new HTTP endpoint that programmatically starts a Claude Code routine session on demand and returns the resulting session ID and URL. Designed for use by alerting systems, CI pipelines, and internal tools.

  > "This is an experimental API. Request and response shapes, rate limits, and token semantics may change. Breaking changes ship behind new dated beta header versions, and the two previous header versions continue to work so that callers have time to migrate."

  - *Implication*: Developers can now trigger Claude Code sessions from external systems (e.g., on CI failure or Sentry alert) without human interaction. The endpoint creates a session immediately and returns without waiting for it to complete — callers must poll or visit the session URL to observe results.
  - *Source*: [Trigger a routine via API](https://platform.claude.com/docs/en/api/claude-code/routines-fire.md)

- **Distinct authentication model**: This endpoint uses a **per-routine bearer token** (`sk-ant-oat01-...`) generated in the Claude Code web UI — not an Anthropic API key. The token is scoped to a single routine.

  > "Authenticate with a per-routine bearer token created in the Claude Code web UI rather than an Anthropic API key."

  - *Implication*: Existing `x-api-key` authentication from the Claude Platform will not work here. Integrations must store a separate secret per routine. Tokens are shown only once at generation time.

- **Required beta header**: Every request must include `anthropic-beta: experimental-cc-routine-2026-04-01`. Requests missing this header return `400 invalid_request_error`.

- **Optional `text` request body field**: A freeform string (max 65,536 characters) providing initial context for the run — e.g., an alert body, failing log line, or git diff. The value is passed to the routine as a literal string and is not parsed.

- **Separate path namespace and billing**: This endpoint lives under `/v1/claude_code/...` rather than `/v1/...`, uses Claude Code subscription usage (not Claude Platform API credits), and requires a Pro, Max, Team, or Enterprise plan with Claude Code on the web enabled.

- **Not in the Anthropic SDKs**: Direct HTTP calls are expected; no SDK wrapper is provided.

- **503 vs. 529 for overload**: The overloaded error returns HTTP `503` from this endpoint, whereas the standard Claude Platform returns `529` for the same error type.

  > "The Claude Platform returns 529 for this error type; this endpoint returns 503."

  - *Implication*: Callers should handle `503` as a retryable overload condition on this endpoint, not `529`.

---

### CLI SDK — `--environment` Flag Renamed to `--environment-id`

- **Flag rename in `ant beta:sessions create`**: The `--environment` flag used when creating agent sessions has been renamed to `--environment-id` in the CLI documentation. The change appears in two separate code examples.

  ```diff
  - ant beta:sessions create \
  -   --environment env_01595EKxaaTTGwwY3kyXdtbs \
  + ant beta:sessions create \
  +   --environment-id env_01595EKxaaTTGwwY3kyXdtbs \
      --title "CLI docs test session"
  ```

  - *Implication*: Scripts and CI configurations using `--environment` in `ant beta:sessions create` will need to be updated to `--environment-id`. This is a documentation correction; verify against the actual CLI version in use to confirm when the flag was renamed in the binary.
  - *Source*: [CLI SDK](https://platform.claude.com/docs/en/api/sdks/cli.md)

---

## New Pages

- **`routines-fire.md`** — Full reference for the experimental Claude Code routine fire endpoint, including authentication setup, request/response schemas, error codes, rate limits, and GitHub Actions integration example. [View](https://platform.claude.com/docs/en/api/claude-code/routines-fire.md)

---

## Notable Details

- **Beta header versioning policy documented**: The new page explicitly states that breaking changes ship behind new dated beta header versions and that the two most recent prior versions remain valid during migration. This is the same policy as other Anthropic beta APIs.
- **Rate limit response includes `Retry-After` header**: The `429 rate_limit_error` from the routine fire endpoint carries a `Retry-After` header indicating when the daily run allowance window resets.
- **Idempotency explicitly not supported**: The endpoint creates a new session on every successful request. Webhook retries will create multiple sessions.
- **`routine_id` path parameter has a misleading prefix**: Despite the parameter name, the value is prefixed `trig_` (not `routine_`). This is noted directly in the documentation.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `claude-code/routines-fire.md` | New | +163 | Experimental HTTP endpoint for triggering Claude Code routines programmatically |
| `sdks/cli.md` | Modified | +2/-2 | Renamed `--environment` flag to `--environment-id` in `ant beta:sessions create` examples |

---

*Generated from Claude API documentation changes detected on 2026-04-15*
