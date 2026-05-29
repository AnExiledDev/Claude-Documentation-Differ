# Claude API Documentation Changes — 2026-05-29

## Summary

All Managed Agents documentation has been updated to use `claude-opus-4-8` as the default model, replacing `claude-opus-4-7` across every SDK example. Alongside the model bump, the `ant` CLI was updated to v1.10.0, the Java SDK to v2.35.0, fast mode for Claude Opus 4.6 was deprecated, and a new clarifying note was added to the self-hosted sandboxes page.

## Significant Changes

### Models

- **Claude Opus 4.8 is now the default model for Managed Agents**: All code examples across the Managed Agents documentation have been updated from `claude-opus-4-7` to `claude-opus-4-8`. This affects every SDK (CLI, Python, TypeScript, C#, Go, Java, PHP, Ruby) across all 10 pages.
  > `"model": "claude-opus-4-8"`
  - *Implication*: Agents created using documentation examples will now target Claude Opus 4.8. Existing agents pinned to `claude-opus-4-7` continue to work; this change is documentation-only.
  - *Source*: [Agent Setup](https://platform.claude.com/docs/en/managed-agents/agent-setup.md), [Quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart.md), and all other Managed Agents pages.

- **Fast mode deprecation for Claude Opus 4.6**: The fast mode tip in the agent setup guide was rewritten to reflect the new model hierarchy and announce a deprecation.
  > "To use \<NextOpus /\>, Claude Opus 4.7, or Claude Opus 4.6 with [fast mode](/docs/en/build-with-claude/fast-mode), pass `model` as an object, for example: `{"id": "claude-opus-4-8", "speed": "fast"}`. Fast mode for Claude Opus 4.6 is deprecated as of the \<NextOpus /\> launch and will be removed approximately 30 days later."
  - *Implication*: Developers using `{"id": "claude-opus-4-6", "speed": "fast"}` should migrate to Claude Opus 4.7 or 4.8 fast mode within ~30 days to avoid breakage.
  - *Source*: [Agent Setup](https://platform.claude.com/docs/en/managed-agents/agent-setup.md)

- **Claude Opus 4.8 added to Dreams supported models**: The Dreams (memory distillation) feature now lists `claude-opus-4-8` as a supported model alongside the existing `claude-opus-4-7` and `claude-sonnet-4-6`.
  > "during the research preview `claude-opus-4-8`, `claude-opus-4-7`, and `claude-sonnet-4-6` are supported"
  - *Implication*: The Dreams pipeline can now be run with Claude Opus 4.8 for higher-quality memory distillation. The supported models table was also updated to reflect this.
  - *Source*: [Dreams](https://platform.claude.com/docs/en/managed-agents/dreams.md)

### Self-Hosted Sandboxes

- **New note clarifying model support in self-hosted sandboxes**: A new `<Note>` block was added near the top of the self-hosted sandboxes page.
  > "Self-hosted sandboxes support all Claude models available in Managed Agents, including \<NextOpus /\>. The model is configured on the [agent](/docs/en/managed-agents/agent-setup), not the environment."
  - *Implication*: Clarifies that model selection is agent-level configuration, not sandbox/environment-level. Developers do not need separate sandbox setups for different models.
  - *Source*: [Self-Hosted Sandboxes](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes.md)

### SDKs and Tooling

- **`ant` CLI updated to v1.10.0**: Both the quickstart guide and self-hosted sandboxes page updated the Linux install script and Dockerfile `ARG ANT_VERSION` from `1.9.1` to `1.10.0`.
  > `VERSION=1.10.0`
  - *Implication*: Developers following the Linux install instructions or building custom Docker images should use v1.10.0.
  - *Source*: [Quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart.md), [Self-Hosted Sandboxes](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes.md)

- **Java SDK updated to v2.35.0**: The Gradle dependency example in the quickstart was bumped from `2.33.0` to `2.35.0`.
  > `implementation("com.anthropic:anthropic-java:2.35.0")`
  - *Implication*: Java developers should update their `build.gradle` to pick up the latest SDK version, which includes the `CLAUDE_OPUS_4_8` enum constant (`BetaManagedAgentsModel.CLAUDE_OPUS_4_8`).
  - *Source*: [Quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart.md)

## Migration Notes

- **Fast mode for Claude Opus 4.6 is deprecated** and will be removed approximately 30 days after the Claude Opus 4.8 launch. Update any agent configurations using `{"id": "claude-opus-4-6", "speed": "fast"}` to use `claude-opus-4-7` or `claude-opus-4-8` with fast mode instead.
- **Java SDK enum**: Update `BetaManagedAgentsModel.CLAUDE_OPUS_4_7` to `BetaManagedAgentsModel.CLAUDE_OPUS_4_8` in Java code and upgrade the SDK to `2.35.0`.
- **ant CLI**: Update to v1.10.0 for Linux installs and Docker-based sandbox builds.

## Notable Details

- The documentation uses a `<NextOpus />` MDX component as a placeholder for Claude Opus 4.8, suggesting the model may have a formal name or alias not yet finalized at the time these docs were written.
- The Java SDK went from `2.33.0` to `2.35.0` (skipping `2.34.x`), indicating there may have been an intermediate release not reflected in this doc snapshot.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| self-hosted-sandboxes.md | Modified | SIGNIFICANT | +6/-2 | Added model support note; CLI bumped to 1.10.0 in install script and Dockerfile |
| agent-setup.md | Modified | SIGNIFICANT | +12/-12 | Model → claude-opus-4-8 across all SDKs; fast mode tip updated with 4.6 deprecation |
| dreams.md | Modified | SIGNIFICANT | +12/-12 | Model → claude-opus-4-8 across all SDKs; 4.8 added to supported models table |
| multi-agent.md | Modified | SIGNIFICANT | +18/-18 | Model → claude-opus-4-8 across all SDKs (coordinator agent examples) |
| permission-policies.md | Modified | SIGNIFICANT | +18/-18 | Model → claude-opus-4-8 across all SDKs (two agent examples) |
| tools.md | Modified | SIGNIFICANT | +18/-18 | Model → claude-opus-4-8 across all SDKs (two agent examples) |
| quickstart.md | Modified | SIGNIFICANT | +11/-11 | CLI 1.9.1 → 1.10.0; Java SDK 2.33.0 → 2.35.0; model → claude-opus-4-8 |
| github.md | Modified | SIGNIFICANT | +9/-9 | Model → claude-opus-4-8 across all SDKs |
| mcp-connector.md | Modified | SIGNIFICANT | +9/-9 | Model → claude-opus-4-8 across all SDKs |
| skills.md | Modified | SIGNIFICANT | +9/-9 | Model → claude-opus-4-8 across all SDKs |

---
*Generated from Claude API documentation changes detected on 2026-05-29*
