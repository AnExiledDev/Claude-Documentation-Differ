# Claude API Documentation Changes — 2026-04-17

## Summary

All Managed Agents documentation examples have been updated from `claude-sonnet-4-6` to `claude-opus-4-7` as the recommended model across every SDK and language. Alongside this, the "API Reference" navigation link in the managed-agents overview was corrected, CLI code blocks received a `nocheck` annotation across multiple pages, and one dangling link to a session events stream schema was removed.

## Significant Changes

### Models

- **Default example model upgraded to `claude-opus-4-7`**: Every Managed Agents code example that previously specified `claude-sonnet-4-6` now uses `claude-opus-4-7`. The change is applied consistently across all eight supported SDK languages (CLI, Python, TypeScript, C#, Go, Java, PHP, Ruby).

  > ```python
  > agent = client.beta.agents.create(
  >     name="Coding Assistant",
  >     model="claude-opus-4-7",   # was claude-sonnet-4-6
  >     ...
  > )
  > ```

  - *Implication*: Developers copying examples from the docs will now provision agents on Opus 4.7 by default. Those intentionally targeting Sonnet 4.6 should verify their pinned model IDs are correct before following updated walkthroughs.
  - *Sources*: [Quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart.md), [Agent Setup](https://platform.claude.com/docs/en/managed-agents/agent-setup.md), [Tools](https://platform.claude.com/docs/en/managed-agents/tools.md), [Migration](https://platform.claude.com/docs/en/managed-agents/migration.md), [Multi-Agent](https://platform.claude.com/docs/en/managed-agents/multi-agent.md), [GitHub](https://platform.claude.com/docs/en/managed-agents/github.md), [MCP Connector](https://platform.claude.com/docs/en/managed-agents/mcp-connector.md), [Skills](https://platform.claude.com/docs/en/managed-agents/skills.md), [Permission Policies](https://platform.claude.com/docs/en/managed-agents/permission-policies.md)

### Documentation / Navigation

- **API Reference card link corrected**: The "API Reference" card on the managed-agents overview now links to `/docs/en/managed-agents/sessions` (the managed-agents sessions page) instead of `/docs/en/api/beta/sessions` (an older beta API path).

  > ```diff
  > -  <Card title="API Reference" icon="code-brackets" href="/docs/en/api/beta/sessions">
  > +  <Card title="API Reference" icon="code-brackets" href="/docs/en/managed-agents/sessions">
  > ```

  - *Implication*: The top-level entry point for Managed Agents API reference now points within the managed-agents documentation section, resolving a navigation inconsistency.
  - *Source*: [Overview](https://platform.claude.com/docs/en/managed-agents/overview.md)

- **Session events API reference link removed**: The events-and-streaming page dropped a sentence linking to `/docs/en/api/beta/sessions/events/stream` for the full event schema. No replacement link was added.

  > ```diff
  > -See the [session events API reference](/docs/en/api/beta/sessions/events/stream) for the full schema of each event type.
  > ```

  - *Implication*: The removed path was likely the same stale beta API URL corrected in the overview. Developers looking for event type schemas should consult the managed-agents sessions and events-and-streaming pages directly.
  - *Source*: [Events and Streaming](https://platform.claude.com/docs/en/managed-agents/events-and-streaming.md)

- **Onboarding placeholder IDs replaced with realistic examples**: The onboarding page replaced `agent_01XXXXXXXXXXXXXXXXXXXXXX` and `env_01XXXXXXXXXXXXXXXXXXXXXX` with plausible-looking example IDs (`agent_01J8XkN5uT3vHpLqRfWdY2`, `env_01K2mPsT7hNwR4jXuLvCqD8`) across all SDK examples.

  - *Implication*: The new IDs reflect the actual ID format returned by the API, making it easier for developers to recognize what a real response looks like.
  - *Source*: [Onboarding](https://platform.claude.com/docs/en/managed-agents/onboarding.md)

## Notable Details

- **`nocheck` annotation added to CLI code blocks**: Numerous `bash CLI` fenced code blocks across 10 pages were changed to `bash CLI nocheck`. This is a documentation tooling annotation — it signals to the docs CI/testing pipeline that these CLI examples should not be executed automatically (likely because they reference environment variables and real resource IDs). It has no effect on the actual API or CLI behavior.

  Affected pages: [Define Outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes.md), [Memory](https://platform.claude.com/docs/en/managed-agents/memory.md), [Migration](https://platform.claude.com/docs/en/managed-agents/migration.md), [Multi-Agent](https://platform.claude.com/docs/en/managed-agents/multi-agent.md), [Observability](https://platform.claude.com/docs/en/managed-agents/observability.md), [Permission Policies](https://platform.claude.com/docs/en/managed-agents/permission-policies.md), [Sessions](https://platform.claude.com/docs/en/managed-agents/sessions.md), [Skills](https://platform.claude.com/docs/en/managed-agents/skills.md), [Vaults](https://platform.claude.com/docs/en/managed-agents/vaults.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| migration.md | Modified | +30/-29 | Model updated to `claude-opus-4-7` in all SDK examples; `nocheck` on CLI block |
| onboarding.md | Modified | +19/-19 | Placeholder IDs replaced with example IDs; `nocheck` on CLI block |
| permission-policies.md | Modified | +19/-19 | Model updated to `claude-opus-4-7` across all examples; `nocheck` on CLI block |
| tools.md | Modified | +18/-18 | Model updated to `claude-opus-4-7` across all examples |
| multi-agent.md | Modified | +13/-13 | Model updated to `claude-opus-4-7`; `nocheck` on CLI blocks |
| agent-setup.md | Modified | +11/-11 | Model updated to `claude-opus-4-7` across all SDK examples |
| memory.md | Modified | +10/-9 | `nocheck` annotation added to CLI code blocks |
| skills.md | Modified | +10/-10 | Model updated to `claude-opus-4-7`; `nocheck` on CLI block |
| github.md | Modified | +9/-9 | Model updated to `claude-opus-4-7` across all examples |
| mcp-connector.md | Modified | +9/-9 | Model updated to `claude-opus-4-7` across all examples |
| quickstart.md | Modified | +9/-9 | Model updated to `claude-opus-4-7` across all SDK examples |
| sessions.md | Modified | +7/-7 | `nocheck` annotation added to CLI code blocks |
| observability.md | Modified | +2/-2 | `nocheck` annotation added to CLI code blocks |
| define-outcomes.md | Modified | +3/-3 | `nocheck` annotation added to CLI code blocks |
| overview.md | Modified | +1/-1 | API Reference card link corrected to managed-agents/sessions |
| vaults.md | Modified | +1/-1 | `nocheck` annotation added to CLI code block |
| events-and-streaming.md | Modified | +0/-2 | Removed stale link to beta sessions events stream schema |

---
*Generated from Claude API documentation changes detected on 2026-04-17*
