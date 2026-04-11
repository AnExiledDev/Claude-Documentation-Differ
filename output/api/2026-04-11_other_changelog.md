# Claude API Documentation Changes — 2026-04-11

## Summary

Three pages were modified: the platform release notes gained a new April 9, 2026 section announcing the **advisor tool** in public beta, and the pricing and legal summarization pages each received a minor single-line update (likely model name corrections).

## Significant Changes

### New Tools

- **Advisor Tool — Public Beta**: A new server-side tool that lets developers pair a faster "executor" model with a higher-intelligence "advisor" model. The advisor model provides strategic guidance mid-generation, enabling long-horizon agentic workloads to approach advisor-quality output while the bulk of token generation runs at executor-model rates.
  > "Pair a faster executor model with a higher-intelligence advisor model that provides strategic guidance mid-generation, so long-horizon agentic workloads get close to advisor-solo quality while the bulk of token generation happens at executor-model rates."
  - *Implication*: Developers can now reduce cost-per-output-token on complex agentic tasks without fully sacrificing reasoning quality by delegating generation to a cheaper model and reserving the capable model for strategic checkpoints.
  - *Beta header required*: `advisor-tool-2026-03-01`
  - *Source*: [Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

## Notable Details

- The pricing page and legal summarization guide each had exactly one line added and one removed (+1/-1). Given that both pages reference specific model identifiers (e.g., `claude-opus-4-6`) in pricing tables and code examples, these changes were most likely minor model name or version string corrections with no semantic impact on pricing or behavior.
- The advisor tool documentation is linked from release notes but the advisor tool page itself (`/docs/en/agents-and-tools/tool-use/advisor-tool`) is not yet included in this diff workspace — developers should check that page directly for full integration details.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| release-notes/overview.md | Modified | +4 / -1 | Added April 9, 2026 section: advisor tool public beta launch |
| about-claude/pricing.md | Modified | +1 / -1 | Minor line update (likely model name correction) |
| about-claude/use-case-guides/legal-summarization.md | Modified | +1 / -1 | Minor line update (likely model name correction) |

---
*Generated from Claude API documentation changes detected on 2026-04-11*
