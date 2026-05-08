# Claude API Documentation Changes — 2026-03-05

## Summary

The dominant change in this update is a significant pruning and reordering of the model enumeration across all API reference pages and SDK docs — the listed model count dropped from "19 more" to "12 more" variants, with several older Claude 3.x and duplicate Sonnet 4 aliases removed. Alongside this, the Java SDK was bumped to v2.15.0, a breaking API change appeared in the PHP SDK's retry configuration, and the Go SDK's overview page dropped its standalone Streaming section. Code examples across all SDK documentation pages were annotated with `nocheck` and `hidelines` rendering directives.

---

## Significant Changes

### Models

- **Model enumeration pruned and reordered across all API reference pages**: The `model` parameter's listed variants dropped from `"19 more"` to `"12 more"` in the type union shown in all API reference pages. Models removed from the enumeration include `claude-opus-4-5-20251101`, `claude-3-7-sonnet-latest`, `claude-3-7-sonnet-20250219`, `claude-3-5-haiku-latest`, `claude-3-5-haiku-20241022`, `claude-4-opus-20250514`, `claude-4-sonnet-20250514`, `claude-3-opus-latest`, and `claude-3-opus-20240229`. The model `claude-opus-4-1` and `claude-opus-4-1-20250805` are now listed explicitly and placed higher in the enumeration order.

  > Before: `UnionMember0 = "claude-opus-4-6" or "claude-sonnet-4-6" or "claude-opus-4-5-20251101" or 19 more`
  > After: `UnionMember0 = "claude-opus-4-6" or "claude-sonnet-4-6" or "claude-haiku-4-5" or 12 more`

  - *Implication*: The enumerated list in the API reference now reflects a narrower set of actively supported model aliases. Developers relying on removed aliases (e.g., `claude-3-opus-latest`, `claude-3-5-haiku-latest`) should migrate to current named models.
  - *Source*: [Messages API](https://platform.claude.com/docs/en/api/messages.md), [Beta Messages API](https://platform.claude.com/docs/en/api/beta/messages.md)

- **Model descriptions updated**: Several model description strings were revised to be more consistent and neutral.

  | Model | Old Description | New Description |
  |-------|----------------|-----------------|
  | `claude-sonnet-4-6` | "Frontier intelligence at scale — built for coding, agents, and enterprise workflows" | "Best combination of speed and intelligence" |
  | `claude-haiku-4-5` / `claude-haiku-4-5-20251001` | "Hybrid model, capable of near-instant responses and extended thinking" | "Fastest model with near-frontier intelligence" |
  | `claude-sonnet-4-5` / `claude-sonnet-4-5-20250929` | "Our best model for real-world agents and coding" | "High-performance model for agents and coding" |
  | `claude-opus-4-1` / `claude-opus-4-1-20250805` | "Our most capable model" | "Exceptional model for specialized complex tasks" |
  | `claude-opus-4-0` / `claude-opus-4-20250514` | "Our most capable model" | "Powerful model for complex tasks" |
  | `claude-3-haiku-20240307` | "Our previous most fast and cost-effective" | "Fast and cost-effective model" |

  - *Implication*: These are description-only changes with no behavioral impact, but they distinguish `claude-opus-4-1` (specialized) from `claude-opus-4-0` (general complex tasks) more clearly.
  - *Source*: [Messages API](https://platform.claude.com/docs/en/api/messages.md)

### SDKs

- **Java SDK bumped to v2.15.0**: The `anthropic-java` library version was updated from `2.14.0` (in `sdks/java.md`) and `2.11.1` (in `client-sdks.md`) to `2.15.0`.

  > ```kotlin
  > // Before
  > implementation("com.anthropic:anthropic-java:2.14.0")
  > // After
  > implementation("com.anthropic:anthropic-java:2.15.0")
  > ```

  - *Implication*: Update your `build.gradle` or `pom.xml` to use `2.15.0` to get the latest Java SDK.
  - *Source*: [Java SDK](https://platform.claude.com/docs/en/api/sdks/java.md), [Client SDKs](https://platform.claude.com/docs/en/api/client-sdks.md)

- **PHP SDK: Retry configuration API changed**: The constructor signature for configuring `maxRetries` in the PHP SDK has changed. It now uses a `RequestOptions` wrapper rather than a direct named argument.

  > ```php
  > // Before
  > $client = new Client(maxRetries: 0);
  >
  > // After
  > $client = new Client(requestOptions: RequestOptions::with(maxRetries: 0));
  > ```

  - *Implication*: This is a **breaking change** for PHP SDK users who configure retries at client instantiation time. Update to use `RequestOptions::with(maxRetries: ...)`.
  - *Source*: [PHP SDK](https://platform.claude.com/docs/en/api/sdks/php.md)

- **Go SDK: Streaming section removed from SDK overview**: The `## Streaming` section (with a full streaming code example using `Messages.NewStreaming`) was removed from `sdks/go.md`. Streaming documentation is still accessible via the API reference pages.

  - *Implication*: The Go SDK overview page no longer includes a standalone streaming example. Developers looking for Go streaming examples should refer to the [API reference](https://platform.claude.com/docs/en/api/go/messages.md).
  - *Source*: [Go SDK](https://platform.claude.com/docs/en/api/sdks/go.md)

- **Client SDKs quick installation tabs reordered**: The Quick Installation tab order in `client-sdks.md` changed — C# and Go tabs moved earlier (after Python and TypeScript), with PHP added as a new dedicated tab. Java, Go, and Ruby example code was removed from the Quick Start section; the Quick Start now shows only Python, TypeScript, and C# examples. The C# example gained an additional `using Anthropic.Models.Messages;` import.

  - *Implication*: The client-sdks overview page now more prominently features C# and Go in the installation quick-start flow, and includes PHP in the tab list.
  - *Source*: [Client SDKs](https://platform.claude.com/docs/en/api/client-sdks.md)

### OpenAI Compatibility

- **OpenAI SDK quick start example now uses environment variable for API key**: The Python quick-start example changed from a hardcoded placeholder string to `os.environ.get("ANTHROPIC_API_KEY")`, and now includes `import os`. The extended thinking Python example was also expanded to include full client setup code.

  > ```python
  > # Before
  > client = OpenAI(api_key="ANTHROPIC_API_KEY", ...)
  >
  > # After
  > import os
  > client = OpenAI(api_key=os.environ.get("ANTHROPIC_API_KEY"), ...)
  > ```

  - *Implication*: The documentation now demonstrates better security practice by reading the API key from an environment variable.
  - *Source*: [OpenAI SDK compatibility](https://platform.claude.com/docs/en/api/openai-sdk.md)

---

## Migration Guidance

### PHP SDK Retry Configuration

The PHP SDK `Client` constructor no longer accepts `maxRetries` as a direct argument. Wrap retry options using `RequestOptions::with()`:

```php
// Before
$client = new Client(maxRetries: 0);

// After
use Anthropic\RequestOptions;
$client = new Client(requestOptions: RequestOptions::with(maxRetries: 0));
```

### Removed Model Aliases

The following model aliases have been removed from the documented enumeration and may indicate deprecation or consolidation. If your code passes these strings directly, verify they still resolve via the API or migrate to current aliases:

- `claude-3-opus-latest`, `claude-3-opus-20240229`
- `claude-3-7-sonnet-latest`, `claude-3-7-sonnet-20250219`
- `claude-3-5-haiku-latest`, `claude-3-5-haiku-20241022`
- `claude-opus-4-5-20251101`
- `claude-4-opus-20250514`, `claude-4-sonnet-20250514` (alternate naming aliases)

---

## Notable Details

- **Code block rendering annotations added broadly**: All SDK documentation pages (`sdks/csharp.md`, `sdks/go.md`, `sdks/java.md`, `sdks/php.md`, `sdks/python.md`, `sdks/ruby.md`, `sdks/typescript.md`) had their code blocks annotated with `nocheck` (suppresses linting in the docs renderer) and `hidelines={...}` (collapses boilerplate lines in the rendered view). This is a documentation rendering improvement with no API behavior change.

- **Python SDK batch results example improved**: The `sdks/python.md` batch results example now includes proper import and `batch_id` assignment before calling `client.messages.batches.results(batch_id)`, making the snippet self-contained.

- **Ruby SDK examples made self-contained**: All Ruby code examples in `sdks/ruby.md` now include `require "anthropic"` and client instantiation (`anthropic = Anthropic::Client.new`) at the top, making them directly runnable without context.

- **`errors.md` Python streaming example**: The streaming helper code example in `errors.md` was tagged `nocheck`, indicating the example may use abbreviated patterns not valid as standalone code.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `python/messages.md` | Modified | +427/-847 | Model list pruned (19→12), descriptions updated |
| `python/beta.md` / `python/beta/messages.md` | Modified | +391/-776 | Model list pruned, descriptions updated |
| `typescript/messages.md` | Modified | +280/-616 | Model list pruned, descriptions updated |
| `ruby/messages.md` | Modified | +278/-616 | Model list pruned, descriptions updated |
| `messages.md` | Modified | +277/-613 | Model list pruned, descriptions updated |
| `typescript/beta.md` / `typescript/beta/messages.md` | Modified | +256/-564 | Model list pruned, descriptions updated |
| `ruby/beta.md` / `ruby/beta/messages.md` | Modified | +254/-564 | Model list pruned, descriptions updated |
| `beta.md` / `beta/messages.md` | Modified | +253/-561 | Model list pruned, descriptions updated |
| `go/messages.md` | Modified | +225/-502 | Model list pruned, descriptions updated |
| `csharp/messages.md` | Modified | +198/-450 | Model list pruned, descriptions updated |
| `java/messages.md` | Modified | +198/-450 | Model list pruned, descriptions updated |
| `client-sdks.md` | Modified | +117/-88 | Tab reorder, Java v2.15.0, Quick Start simplified |
| `python/completions.md` | Modified | +108/-213 | Model list pruned |
| `sdks/go.md` | Modified | +186/-149 | Streaming section removed, code block annotations |
| `sdks/java.md` | Modified | +49/-49 | Java SDK v2.15.0, `nocheck` annotations |
| `sdks/typescript.md` | Modified | +28/-25 | `hidelines` annotations |
| `sdks/python.md` | Modified | +29/-20 | `hidelines`/`nocheck` annotations, batch example improved |
| `sdks/ruby.md` | Modified | +18/-6 | Self-contained `require` + client added to examples |
| `sdks/csharp.md` | Modified | +14/-14 | `nocheck` annotations |
| `sdks/php.md` | Modified | +12/-4 | Retry API change, PHP examples made self-contained |
| `openai-sdk.md` | Modified | +23/-6 | API key from env var, `nocheck` annotations, expanded examples |
| `errors.md` | Modified | +3/-2 | `nocheck`/`hidelines` code annotations |
| `beta-headers.md` | Modified | +1/-1 | `hidelines` on TypeScript code block |

---

*Generated from Claude API documentation changes detected on 2026-03-05*
