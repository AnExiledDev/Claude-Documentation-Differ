# Claude API Documentation Changes — 2026-05-29

## Summary

Nine documentation pages were modified with no new or removed pages. The most notable changes are: `claude-opus-4-8` adopted as the standard example model across multiple docs, the "Fast mode" section in the Usage & Cost API drops its "beta:" label, the Get Started guide is substantially revised with a new example prompt and restructured sample outputs, and the Java quickstart now requires JDK 25+.

## Significant Changes

### Models

- **`claude-opus-4-8` as default example model**: Code examples across the data residency, streaming refusals, and get-started guides all now use `claude-opus-4-8` as the model identifier. The rate limits API example response also includes `claude-opus-4-6`, `claude-opus-4-7`, and `claude-opus-4-8` in the model group list alongside `claude-opus-4-5`.
  - *Implication*: Indicates `claude-opus-4-8` is now the current recommended Claude Opus generation for new integrations.
  - *Source*: [Get Started](https://platform.claude.com/docs/en/get-started.md), [Data Residency](https://platform.claude.com/docs/en/manage-claude/data-residency.md), [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api.md), [Handle Streaming Refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md)

### Admin API — Usage & Cost

- **Fast mode exits beta labeling**: The section heading for fast mode usage tracking changed from `#### Fast mode (beta: research preview)` to `#### Fast mode (research preview)`, removing the `beta:` prefix.
  > `#### Fast mode (research preview)`
  - *Implication*: Fast mode (using the `fast-mode-2026-02-01` beta header with the `speed` dimension) is no longer designated "beta" in the docs, though it remains a "research preview." Developers tracking this feature should note it may be approaching broader availability.
  - *Source*: [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api.md)

- **Rate limits model group updated**: The example response for the organization rate limits endpoint now shows a model group spanning five versions:
  > `"claude-opus-4-5"`, `"claude-opus-4-5-20251101"`, `"claude-opus-4-6"`, `"claude-opus-4-7"`, `"claude-opus-4-8"`
  - *Implication*: Confirms that Claude Opus 4.5 through 4.8 share a single rate limit group. Developers building rate limit monitoring should expect this consolidated grouping.
  - *Source*: [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api.md)

### Get Started Guide

- **Guide substantially revised with new example prompt**: The get-started guide (+322/-131 lines) replaces the previous example prompt and sample outputs. The demonstration query is now "What should I search for to find the latest developments in renewable energy?" The previous sections "Search Terms to Use:", "Best Sources to Check:", and "Specific Topics to Explore:" in the sample output have been replaced with a unified `## General Search Terms` section.
  - *Implication*: The sample outputs shown in all language tabs (cURL, CLI, Python, TypeScript, C#, Go, Java) are updated to reflect the new example. The structure and SDK setup steps remain the same.
  - *Source*: [Get Started](https://platform.claude.com/docs/en/get-started.md)

- **Java SDK quickstart requires JDK 25+**: The Java setup step now explicitly states:
  > "You need a JDK (25 or later) and either Gradle or Maven on your PATH."
  The sample `build.gradle.kts` and `pom.xml` both set the Java toolchain to version 25 (`languageVersion = JavaLanguageVersion.of(25)` / `<maven.compiler.release>25</maven.compiler.release>`). The Java source uses `static void main()` and `IO.println()`, consistent with JDK 25's unnamed main methods and new I/O APIs.
  - *Implication*: The Anthropic Java SDK quickstart now targets JDK 25. Developers on older JDK versions will need to upgrade or adapt the examples. Referenced SDK version: `anthropic-java:2.35.0`.
  - *Source*: [Get Started](https://platform.claude.com/docs/en/get-started.md)

### Streaming Refusals

- **All 9 language examples updated to `claude-opus-4-8`**: The streaming refusals implementation guide code samples across cURL, Python, TypeScript, C#, Go, Java, PHP, and Ruby were updated to reference `claude-opus-4-8` (and `Model.ClaudeOpus4_8` / `Model.CLAUDE_OPUS_4_8` in typed SDKs).
  - *Implication*: Consistent with the broader model example refresh; no behavioral changes to the `stop_reason: "refusal"` handling pattern itself.
  - *Source*: [Handle Streaming Refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals.md)

### Data Residency

- **Code examples updated to `claude-opus-4-8`**: The cURL, CLI, Python, and TypeScript examples in the inference geo section now use `claude-opus-4-8`. Model availability note remains: `inference_geo` requires Claude Opus 4.6 / Sonnet 4.6 or later.
  - *Implication*: No change to the `inference_geo` parameter semantics. The minimum supported model generation for data residency controls (`"us"` routing) remains the 4.6 series.
  - *Source*: [Data Residency](https://platform.claude.com/docs/en/manage-claude/data-residency.md)

## Minor Changes

- **authentication.md**: Single line change, likely a model version reference update. (+1/-1)
- **claude-code-analytics-api.md**: Two-line change, likely a model version reference update. (+2/-2)
- **compliance-content-data.md**: Two-line change, likely a model version reference update. (+2/-2)
- **intro.md**: Single line change. (+1/-1)

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| get-started.md | Modified | SIGNIFICANT | +322/-131 | New example prompt, restructured sample outputs, Java now requires JDK 25, all examples use `claude-opus-4-8` |
| handle-streaming-refusals.md | Modified | SIGNIFICANT | +8/-8 | All 9 language code examples updated to `claude-opus-4-8` |
| rate-limits-api.md | Modified | SIGNIFICANT | +5/-3 | Model group in example response expanded to include claude-opus-4-6 through 4-8 |
| data-residency.md | Modified | SIGNIFICANT | +4/-4 | Code examples updated to `claude-opus-4-8` |
| usage-cost-api.md | Modified | SIGNIFICANT | +2/-2 | "Fast mode" heading drops "beta:" prefix; now "(research preview)" only |
| claude-code-analytics-api.md | Modified | MINOR | +2/-2 | Minor update (likely model reference) |
| compliance-content-data.md | Modified | MINOR | +2/-2 | Minor update (likely model reference) |
| authentication.md | Modified | MINOR | +1/-1 | Minor update |
| intro.md | Modified | MINOR | +1/-1 | Minor update |

---
*Generated from Claude API documentation changes detected on 2026-05-29*
