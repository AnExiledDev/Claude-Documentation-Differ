# Claude API Documentation Changes — 2026-05-09

## Summary

Two pages were modified. The primary change is a substantial rewrite of the "Get started with Claude" quickstart guide (+82/-32 lines), which adds a new CLI tab, updates all code examples to use `claude-opus-4-7`, raises the Java SDK's required JDK version to 25, and references `anthropic-java:2.30.0`. The MCP connector page received a single-line edit (likely a wording or URL fix).

## Significant Changes

### Get Started Guide

- **New CLI Tab in Quickstart**: A new "CLI" tab has been added to the multi-language quickstart, showing how to use the Anthropic `ant` CLI tool to make API calls.
  > ```bash
  > brew install anthropics/tap/ant
  > ```
  > ```bash
  > ant messages create \
  >   --model claude-opus-4-7 \
  >   --max-tokens 1000 \
  >   --message '{ role: user, content: "..." }'
  > ```
  - *Implication*: Developers can now follow the official quickstart using the first-party CLI without writing any code; the CLI tab sits alongside cURL, Python, TypeScript, and Java.
  - *Source*: [Get started with Claude](https://platform.claude.com/docs/en/get-started.md)

- **All Quickstart Examples Updated to `claude-opus-4-7`**: Every code sample in the get-started page (cURL, CLI, Python, TypeScript, Java) now targets `claude-opus-4-7` as the default model.
  - *Implication*: New developers following the quickstart will be directed to Claude Opus 4.7 rather than an older model.
  - *Source*: [Get started with Claude](https://platform.claude.com/docs/en/get-started.md)

- **Java Quickstart Requires JDK 25 and `anthropic-java:2.30.0`**: The Java setup step now explicitly requires JDK 25 or later, and the Gradle/Maven build file examples pin the SDK to version `2.30.0`.
  > ```
  > You need a JDK (25 or later) and either Gradle or Maven on your PATH.
  > ```
  > ```kotlin
  > implementation("com.anthropic:anthropic-java:2.30.0")
  > ```
  - *Implication*: Java developers setting up a new project from the quickstart will need JDK 25. Projects targeting older JDKs must configure the toolchain manually and may need to pin an older SDK version.
  - *Source*: [Get started with Claude](https://platform.claude.com/docs/en/get-started.md)

## Notable Details

- The quickstart's "Next steps" section now leads with a card for "Working with the Messages API" (`/docs/en/build-with-claude/working-with-messages`) before the broader features cards, signalling a deliberate onboarding path toward multi-turn conversation patterns.
- The MCP connector page change was exactly 1 line added and 1 line removed; no functional API behavior was altered. No coverage warranted beyond noting it occurred.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/get-started.md` | Modified | +82 / -32 | Added CLI tab, updated all examples to `claude-opus-4-7`, Java JDK 25 requirement, `anthropic-java:2.30.0` |
| `docs/api/en/agents-and-tools/mcp-connector.md` | Modified | +1 / -1 | Minor one-line edit; no functional change |

---
*Generated from Claude API documentation changes detected on 2026-05-09*
