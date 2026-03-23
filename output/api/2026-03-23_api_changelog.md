# Claude API Documentation Changes — 2026-03-23

## Summary

Eight SDK documentation pages received updates, consisting primarily of adjustments to `hidelines` display attributes on code blocks and a set of substantive code correctness fixes in the Ruby SDK documentation. No new API endpoints, parameters, models, or breaking changes were introduced.

## Significant Changes

### SDKs

- **Ruby SDK: Fixed inconsistent variable naming in code examples**: Multiple examples throughout the Ruby SDK docs used `client` as a variable name when the initialized variable was `anthropic`. Additionally, two code blocks were missing their initialization preamble entirely.
  > Before: `client.beta.messages.tool_runner(`
  > After: `anthropic.beta.messages.tool_runner(`

  > Before (pagination): `page = client.messages.batches.list(limit: 20)`
  > After (pagination): added `require "anthropic"` / `anthropic = Anthropic::Client.new` then `page = anthropic.messages.batches.list(limit: 20)`

  > Before (prose): "you can make requests using `client.request`"
  > After (prose): "you can make requests using `anthropic.request`"

  - *Implication*: Developers copying these examples would have received `NameError: undefined local variable or method 'client'` at runtime. The corrected examples now work as shown.
  - *Source*: [Ruby SDK](https://platform.claude.com/docs/en/api/sdks/ruby.md)

## Notable Details

- **`hidelines` attribute adjustments across all modified pages**: The `hidelines` attribute on fenced code blocks controls which line ranges are collapsed/hidden in the rendered documentation UI. This round of changes recalibrated these ranges across Python, TypeScript, PHP, Ruby, and the beta-headers, client-sdks, errors, and openai-sdk pages. For example, TypeScript blocks that previously hid lines `1..4` now hide `1..2`, exposing the import line in the rendered view. These are display-only changes with no effect on the underlying API or SDK behavior.
  - *Affected pages*: [beta-headers](https://platform.claude.com/docs/en/api/beta-headers.md), [client-sdks](https://platform.claude.com/docs/en/api/client-sdks.md), [errors](https://platform.claude.com/docs/en/api/errors.md), [openai-sdk](https://platform.claude.com/docs/en/api/openai-sdk.md), [PHP SDK](https://platform.claude.com/docs/en/api/sdks/php.md), [Python SDK](https://platform.claude.com/docs/en/api/sdks/python.md), [Ruby SDK](https://platform.claude.com/docs/en/api/sdks/ruby.md), [TypeScript SDK](https://platform.claude.com/docs/en/api/sdks/typescript.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| sdks/ruby.md | Modified | +18/-14 | Fixed `client` → `anthropic` variable naming; added missing init code in tool use and pagination examples |
| sdks/python.md | Modified | +11/-11 | `hidelines` range adjustments on 11 code blocks |
| sdks/php.md | Modified | +7/-7 | `hidelines` range adjustments on 7 code blocks |
| sdks/typescript.md | Modified | +7/-7 | `hidelines` range adjustments on 7 code blocks |
| client-sdks.md | Modified | +3/-3 | `hidelines` range adjustments for TypeScript, Go, and Java examples |
| beta-headers.md | Modified | +2/-2 | `hidelines` range adjustments for Python and TypeScript examples |
| errors.md | Modified | +2/-2 | `hidelines` range adjustments for Python and TypeScript examples |
| openai-sdk.md | Modified | +1/-1 | Python `hidelines` range extended from `1..8` to `1..9` |

---
*Generated from Claude API documentation changes detected on 2026-03-23*
