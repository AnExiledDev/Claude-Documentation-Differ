# Claude API Documentation Changes - February 9, 2026

## TL;DR
Anthropic has launched **Fast Mode** for Claude Opus 4.6 (research preview) with a new `speed` parameter, delivering up to 2.5x faster output generation at 6x pricing. The API now exposes **per-iteration token usage breakdowns** for multi-turn tool use and compaction, new **fast mode rate limit headers**, and a new `"managed"` user role for organization administration.

## API Changes

### Fast Mode Parameter (Research Preview)

The Messages API now supports a `speed` parameter to control inference speed:

> **New parameter:** `speed: "standard" | "fast"` (optional)
>
> The inference speed mode for this request. `"fast"` enables high output-tokens-per-second inference.

**Beta header required:** `anthropic-beta: fast-mode-2026-02-01`

Fast mode enables significantly faster output token generation (up to 2.5x faster) on Claude Opus 4.6 at premium pricing. The speed benefits are focused on **output tokens per second (OTPS)**, not time to first token (TTFT).

```python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    speed="fast",
    betas=["fast-mode-2026-02-01"],
    messages=[{"role": "user", "content": "Refactor this module..."}]
)
```

The response now includes a `speed` field in the `usage` object indicating which speed was actually used:

```json
{
  "usage": {
    "input_tokens": 523,
    "output_tokens": 1842,
    "speed": "fast"
  }
}
```

**Key details:**
- Same model weights and behavior (not a different model)
- Separate dedicated rate limits from standard Opus
- Invalidates prompt cache when switching between speeds
- Not available with Batch API or Priority Tier
- Currently Opus 4.6 only

### Per-Iteration Token Usage (Beta)

The API now exposes detailed per-iteration token breakdowns via the `iterations` field in the usage object. This is a `BetaIterationsUsage` array containing either `BetaMessageIterationUsage` or `BetaCompactionIterationUsage` objects.

> **New field:** `iterations: BetaIterationsUsage`
>
> Per-iteration token usage breakdown. Each entry represents one sampling iteration, with its own input/output token counts and cache statistics. This allows you to:
> - Determine which iterations exceeded long context thresholds (>=200k tokens)
> - Calculate the true context window size from the last iteration
> - Understand token accumulation across server-side tool use loops

Each iteration object includes:
- `input_tokens`: Input tokens for this iteration
- `output_tokens`: Output tokens for this iteration
- `cache_creation_input_tokens`: Tokens used to create cache
- `cache_read_input_tokens`: Tokens read from cache
- `cache_creation`: Breakdown by TTL (`ephemeral_5m_input_tokens`, `ephemeral_1h_input_tokens`)
- `type`: Either `"message"` or `"compaction"`

This is especially valuable for agentic workflows with multiple tool use rounds, allowing developers to understand exactly how tokens accumulate across iterations and identify which iterations triggered long context pricing tiers.

### Usage and Cost Reporting Updates

The Admin API now supports filtering and grouping by `speed` for fast mode usage tracking:

**Get Messages Usage Report:**
- New `group_by` option: `"speed"` (requires `fast-mode-2026-02-01` beta header)
- New filter parameter: `speeds: ["standard" | "fast"]`
- New response field: `speed: "standard" | "fast"` in usage results

**Get Cost Report:**
- New response field: `speed: "standard" | "fast"` in cost results (when grouping by speed)

```bash
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2026-02-01T00:00:00Z&\
ending_at=2026-02-08T00:00:00Z&\
group_by[]=speed&\
group_by[]=model&\
bucket_width=1d" \
  --header "anthropic-beta: fast-mode-2026-02-01" \
  --header "x-api-key: $ADMIN_API_KEY"
```

### New User Role: "managed"

The Admin API now supports a new `"managed"` role for organization users and invites:

- User creation/update endpoints now accept `role: "managed"`
- User and invite list responses now show `"managed"` as a possible role value
- Role enum updated from "2 more" to "3 more" (including `"admin"`, `"claude_code_user"`, and now `"managed"`)

This appears alongside existing roles: `"user"`, `"developer"`, `"billing"`, `"admin"`, and `"claude_code_user"`.

## Rate Limits & Pricing

### Fast Mode Pricing

Fast mode pricing is **6x standard rates** for prompts ≤200K tokens:

| Context window | Input | Output |
|:---------------|:------|:-------|
| ≤ 200K input tokens | $30 / MTok | $150 / MTok |
| > 200K input tokens | $60 / MTok | $225 / MTok |

Fast mode pricing **stacks with other multipliers**:
- Prompt caching multipliers apply on top of fast mode pricing
- Data residency (US-only) multipliers apply on top of fast mode pricing

> Fast mode is not available with the [Batch API](#batch-processing).

### Fast Mode Rate Limits

Fast mode has **dedicated rate limits** separate from standard Opus limits. Unlike standard speed (which has separate limits for ≤200K and >200K contexts), fast mode uses a **single rate limit** covering the full context range.

**New response headers:**
- `anthropic-fast-input-tokens-limit`: Maximum fast mode input tokens per minute
- `anthropic-fast-input-tokens-remaining`: Remaining fast mode input tokens
- `anthropic-fast-input-tokens-reset`: Time when the fast mode input token limit resets
- `anthropic-fast-output-tokens-limit`: Maximum fast mode output tokens per minute
- `anthropic-fast-output-tokens-remaining`: Remaining fast mode output tokens
- `anthropic-fast-output-tokens-reset`: Time when the fast mode output token limit resets

When fast mode rate limits are exceeded, the API returns a `429` error with a `retry-after` header. The SDKs automatically retry up to 2 times by default.

## New Documentation Pages

### Fast Mode (Research Preview)

**Path:** `/docs/en/build-with-claude/fast-mode.md`

Comprehensive guide to the new fast mode feature, including:
- How fast mode works (same model, faster inference)
- Basic usage with code examples in Shell, Python, TypeScript, Ruby, Go, and Java
- Pricing details and multiplier stacking
- Rate limit information and dedicated headers
- Automatic retry behavior and fallback strategies
- Considerations for prompt caching, model support, and API compatibility
- Integration with Usage and Cost APIs

Key callout: Fast mode is currently in **research preview** with limited availability. Interested customers must [join the waitlist](https://claude.com/fast-mode) to request access.

## Hidden Gems

### Prompt Cache Invalidation by Speed

The prompt caching documentation now explicitly states that switching between `speed: "fast"` and standard speed **invalidates the prompt cache**:

> | **Speed setting** | ✓ | ✘ | ✘ | Switching between [`speed: "fast"` and standard speed](/docs/en/build-with-claude/fast-mode) invalidates system and message caches |

This means fast and standard speed requests do not share cached prefixes. Applications using prompt caching should be aware that alternating between speeds will not benefit from previous cache entries.

### Fallback Patterns for Fast Mode

The fast mode documentation includes sophisticated fallback patterns for handling rate limits across multiple SDKs. The pattern is:
1. Try with `speed: "fast"`
2. On 429 error, retry without speed parameter (falls back to standard)
3. On 5xx errors, retry with exponential backoff

This suggests Anthropic expects fast mode capacity to be more constrained initially and recommends graceful degradation strategies.

### Continuous Token Replenishment

Fast mode rate limits use "continuous token replenishment" rather than fixed-window rate limiting. The documentation notes that `retry-after` delays are "typically short" when fast mode limits are exceeded, suggesting sub-minute recovery times.

## Technical Details

### Beta Header Format

Fast mode requires the beta header:
```
anthropic-beta: fast-mode-2026-02-01
```

In SDKs, this is specified as:
```python
betas=["fast-mode-2026-02-01"]
```

### Speed Parameter Behavior

- Omitting `speed` parameter defaults to standard speed
- Sending `speed: "fast"` with unsupported models returns an error
- The response always includes `usage.speed` to confirm which speed was used
- Speed setting is per-request (not a workspace or API key configuration)

### Iterations Usage Structure

The `BetaIterationsUsage` type is a union of:
- `BetaMessageIterationUsage` (type: `"message"`) - Regular sampling iterations
- `BetaCompactionIterationUsage` (type: `"compaction"`) - Context compaction iterations

Both include identical fields for token counts and cache statistics, with only the `type` field differentiating them.

### SDK Support

Fast mode is documented with native support in:
- Python SDK
- TypeScript SDK
- Ruby SDK
- Go SDK
- Java SDK (examples provided)

All SDKs support the `betas` parameter for beta feature opt-in.

---

*Generated from Claude API documentation changes detected on February 9, 2026*
