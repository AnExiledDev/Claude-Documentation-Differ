# Claude API Documentation Changes — 2026-03-21

## Summary

Six documentation pages were updated with no new or removed pages. The most substantive changes are a new "Deserializing params" section in the Go SDK docs, version bumps across the Go (v1.27.1), Java (2.18.0), and Ruby (1.25.0) SDKs, and a meaningful policy clarification in the beta headers warning (breaking changes will now come *with* notice).

## Significant Changes

### Beta Features Policy

- **Breaking changes in beta features now come with notice**: The warning text in the beta headers documentation was updated from "Have breaking changes without notice" to "Have breaking changes with notice."
  > - Have breaking changes with notice
  - *Implication*: This signals a policy shift — developers using beta features can now expect advance notification before breaking changes are made, rather than receiving no warning.
  - *Source*: [Beta Headers](https://platform.claude.com/docs/en/api/beta-headers.md)

### Go SDK — New `param.SetJSON` / Deserializing Params

- **New "Deserializing params" section documents round-trip JSON support**: The Go SDK documentation adds a full section explaining how to reconstruct `Param` types (e.g., `MessageNewParams`, `ToolUnionParam`) from stored or forwarded JSON. Because typed union fields like `OfBashTool20250124` are nil after a plain `json.Unmarshal`, the pattern requires both `UnmarshalJSON` and `param.SetJSON` together.
  > Param types (types ending in `Param`, such as `MessageNewParams` or `ToolUnionParam`) are designed for outgoing requests only. They marshal correctly to JSON but do not fully support round-trip deserialization. If you unmarshal raw JSON into a param struct, typed union fields like `OfBashTool20250124` will be nil even when the underlying JSON is valid.
  >
  > If you need to reconstruct params from raw JSON (for example, from a database, middleware, or a previous request), call `UnmarshalJSON` to populate non-union fields, then use `param.SetJSON` to attach the raw bytes for correct re-serialization.
  - *Implication*: Developers building middleware, proxies, or pipelines that serialize and re-send `MessageNewParams` (including tool use) should adopt this two-step pattern to avoid silently dropping union-typed tool fields. Requires Go SDK v1.20.0 or later.
  - *Source*: [Go SDK](https://platform.claude.com/docs/en/api/sdks/go.md)

### SDK Version Bumps

- **Go SDK**: Pinned version updated from `v1.19.0` → `v1.27.1`; minimum Go runtime requirement raised from **1.22+** to **1.23+**.
  - *Implication*: Projects pinning the Go SDK version should update their `go get` command. Projects running Go 1.22 will need to upgrade their Go toolchain.
  - *Source*: [Go SDK](https://platform.claude.com/docs/en/api/sdks/go.md) · [Client SDKs](https://platform.claude.com/docs/en/api/client-sdks.md)

- **Java SDK**: Version updated from `2.15.0` → `2.18.0` in both Gradle and Maven dependency snippets.
  - *Implication*: Update `build.gradle` or `pom.xml` to pull in three minor releases of fixes and features.
  - *Source*: [Java SDK](https://platform.claude.com/docs/en/api/sdks/java.md) · [Client SDKs](https://platform.claude.com/docs/en/api/client-sdks.md)

- **Ruby SDK**: Gem version constraint updated from `~> 1.19.0` → `~> 1.25.0`.
  - *Implication*: Update the Gemfile version pin to receive six minor releases of updates.
  - *Source*: [Ruby SDK](https://platform.claude.com/docs/en/api/sdks/ruby.md)

### Rate Limits — Fast Mode Wording Clarification

- **Fast Mode described as a beta feature explicitly**: The rate-limits page reworded the Fast Mode description to label it as `(beta: research preview)` and reorganized how the `speed: "fast"` parameter is referenced.
  > When using [fast mode](/docs/en/build-with-claude/fast-mode) (beta: research preview) with `speed: "fast"` on Opus 4.6, dedicated rate limits apply that are separate from standard Opus rate limits.
  - *Implication*: No functional rate limit changes; this is a clarification that Fast Mode on Opus 4.6 is a beta/research-preview feature.
  - *Source*: [Rate Limits](https://platform.claude.com/docs/en/api/rate-limits.md)

## Notable Details

- The Go SDK section "Accessing raw response data (e.g. response headers)" was renamed to "Accessing raw response data (for example, response headers)" — an editorial style change with no functional impact.
- The `param.SetJSON` function was available since Go SDK v1.20.0 but is newly documented; teams already on v1.20.0+ can use it immediately without upgrading further.
- The Go minimum runtime bump (1.22 → 1.23) is reflected in both the Go SDK page and the compatibility table on the Client SDKs page, keeping them consistent.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| sdks/go.md | Modified | +63 / -4 | New "Deserializing params" section, SDK bump v1.19.0→v1.27.1, Go runtime requirement 1.22→1.23 |
| client-sdks.md | Modified | +3 / -3 | Java SDK version 2.15.0→2.18.0, Go runtime requirement 1.22→1.23 |
| sdks/java.md | Modified | +2 / -2 | Java SDK version 2.15.0→2.18.0 in Gradle/Maven snippets |
| beta-headers.md | Modified | +1 / -1 | Beta breaking-change policy: "without notice" → "with notice" |
| rate-limits.md | Modified | +1 / -1 | Fast Mode described as beta research preview, wording clarified |
| sdks/ruby.md | Modified | +1 / -1 | Ruby SDK gem version ~> 1.19.0 → ~> 1.25.0 |

---
*Generated from Claude API documentation changes detected on 2026-03-21*
