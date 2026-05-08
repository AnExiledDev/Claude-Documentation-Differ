# Claude API Documentation Changes — 2026-02-21

## Summary

Three pages were updated: the intro page reorganized its onboarding flow by replacing the "Get started" section with a new "Recommended path for new developers" structured sequence, the quickstart guide updated its example model to `claude-opus-4-6`, and the release notes page added a February 19, 2026 entry covering automatic prompt caching, model retirements, and a new deprecation announcement.

## Significant Changes

### Getting Started / Onboarding

- **Intro page: "Get started" section replaced with "Recommended path for new developers"**: The previous unstructured "## Get started" section on the intro page was removed and replaced with a new `<Steps>`-based sequence that explicitly walks new developers through four ordered steps.

  > Follow these steps to go from zero to a working Claude integration.
  >
  > 1. Make your first API call
  > 2. Understand the Messages API
  > 3. Choose the right model
  > 4. Explore features and tools

  - *Implication*: The onboarding path is now more prescriptive, directing developers through the Messages API guide and models overview before exploring additional features. The structure makes the recommended learning order explicit rather than presenting a flat set of links.
  - *Source*: [Intro to Claude](https://platform.claude.com/docs/en/intro.md)

- **Quickstart: example model updated to `claude-opus-4-6`**: All code samples in the quickstart guide (cURL, Python, TypeScript, Java) now use `claude-opus-4-6` as the example model identifier. The example task was also reframed as building a "simple web search assistant."

  > Run this command to create a simple web search assistant

  - *Implication*: Developers copying the quickstart code will now reference `claude-opus-4-6` by default, reflecting the current recommended model. The example response outputs in the docs have been updated to match.
  - *Source*: [Get started with Claude](https://platform.claude.com/docs/en/get-started.md)

### Release Notes

- **February 19, 2026 entry added**: A new dated section was added to the release notes overview covering three items:

  1. **Automatic caching for the Messages API** — A new `cache_control` field that automatically caches the last cacheable block and moves the cache point forward as conversations grow, removing the need for manual breakpoint management. Available on the Claude API and Azure AI Foundry (preview).

     > Add a single `cache_control` field to your request body and the system automatically caches the last cacheable block, moving the cache point forward as conversations grow. No manual breakpoint management required. Works alongside existing block-level cache control for fine-grained optimization.

  2. **Claude Sonnet 3.7 and Claude Haiku 3.5 retired** — Models `claude-3-7-sonnet-20250219` and `claude-3-5-haiku-20241022` have been retired. Requests to these models now return an error. The recommended replacements are Claude Sonnet 4.6 and Claude Haiku 4.5 respectively. Researchers can request continued access via the External Researcher Access Program.

  3. **Claude Haiku 3 deprecation announced** — Model `claude-3-haiku-20240307` is deprecated with retirement scheduled for April 19, 2026. Migration to Claude Haiku 4.5 is recommended.

  - *Implication*: Any production integrations still using `claude-3-7-sonnet-20250219` or `claude-3-5-haiku-20241022` are broken as of this date and require immediate model updates. The Haiku 3 deprecation gives approximately two months for migration.
  - *Source*: [Claude Developer Platform Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

## Migration Guidance

- **Immediate action required**: Integrations using `claude-3-7-sonnet-20250219` (Claude Sonnet 3.7) or `claude-3-5-haiku-20241022` (Claude Haiku 3.5) will now receive errors. Migrate to `claude-sonnet-4-6` and `claude-haiku-4-5` respectively.
- **Planned action required by April 19, 2026**: Integrations using `claude-3-haiku-20240307` (Claude Haiku 3) should migrate to `claude-haiku-4-5` before the retirement date.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/intro.md` | Modified | +29 / -18 | Replaced "Get started" section with structured "Recommended path for new developers" 4-step sequence |
| `docs/api/en/get-started.md` | Modified | +14 / -11 | Updated example model to `claude-opus-4-6`; reframed quickstart as a web search assistant |
| `docs/api/en/release-notes/overview.md` | Modified | +5 / -0 | Added February 19, 2026 entry: automatic caching launch, Sonnet 3.7 and Haiku 3.5 retirements, Haiku 3 deprecation announcement |
