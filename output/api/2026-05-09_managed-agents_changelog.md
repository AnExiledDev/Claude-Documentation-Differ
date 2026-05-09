# Claude API Documentation Changes — 2026-05-09

## Summary

Three Managed Agents documentation pages were updated. The most significant change is the renaming of the `callable_agents` field to `multiagent`, along with updated update-semantics for that field. SDK and CLI version numbers were also bumped in the quickstart guide.

## Significant Changes

### Managed Agents API

- **`callable_agents` renamed to `multiagent`**: The agent configuration field for multi-agent orchestration has been renamed from `callable_agents` to `multiagent`. The description has shifted from a flat list of invokable agents to a "coordinator declaration" construct, and the research preview / access-request gate has been removed from the documentation.
  > Old: `` `callable_agents` | Other agents this agent can invoke for multi-agent orchestration. This is a research preview feature; request access to try it. ``
  >
  > New: `` `multiagent` | A coordinator declaration listing the agents this agent can delegate to. See Multiagent sessions. ``
  - *Implication*: Any existing code or saved agent definitions using `callable_agents` will need to be updated to `multiagent`. The removal of the research-preview gate suggests this feature is now generally available under the `managed-agents-2026-04-01` beta header.
  - *Source*: [agent-setup.md](https://platform.claude.com/docs/en/managed-agents/agent-setup.md)

- **`multiagent` has distinct update semantics**: When updating an agent, `multiagent` is no longer treated as a plain array field. It is now documented as a structured object that is replaced as a whole — including its internal `agents` roster — when updated. Passing `null` clears it entirely.
  > Old: `` **Array fields** (`tools`, `mcp_servers`, `skills`, `callable_agents`) are fully replaced by the new array. To clear an array field entirely, pass `null` or an empty array. ``
  >
  > New: `` **Array fields** (`tools`, `mcp_servers`, `skills`) are fully replaced by the new array. To clear an array field entirely, pass `null` or an empty array. ``
  > `` **`multiagent`** is replaced as a whole, including its `agents` roster. Pass `null` to clear it. ``
  - *Implication*: The `multiagent` field is no longer a simple array but a structured object with an `agents` sub-field. Partial updates are not supported; the entire `multiagent` object must be supplied on each update.
  - *Source*: [agent-setup.md](https://platform.claude.com/docs/en/managed-agents/agent-setup.md)

### SDKs and CLI

- **`ant` CLI version bumped to 1.7.0**: The Linux manual install snippet in the quickstart now references version `1.7.0` (previously `1.3.2`). The code block was also annotated with `nocheck` to prevent CI validation of the pinned version string.
  - *Source*: [quickstart.md](https://platform.claude.com/docs/en/managed-agents/quickstart.md)

- **`anthropic-java` SDK bumped to 2.30.0**: The Gradle dependency version for the Java SDK has been updated from `2.27.0` to `2.30.0`.
  > `implementation("com.anthropic:anthropic-java:2.30.0")`
  - *Implication*: Developers following the quickstart should use version `2.30.0` of the Java SDK.
  - *Source*: [quickstart.md](https://platform.claude.com/docs/en/managed-agents/quickstart.md)

## Migration Guidance

- **`callable_agents` → `multiagent`**: Update any agent creation or update requests that include the `callable_agents` field. The field is now `multiagent` and wraps the agent list in a coordinator declaration object (with an `agents` roster). Consult the [multi-agent documentation](https://platform.claude.com/docs/en/managed-agents/multi-agent.md) for the full schema.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| managed-agents/agent-setup.md | Modified | +6 / -4 | `callable_agents` renamed to `multiagent`; update semantics clarified |
| managed-agents/quickstart.md | Modified | +3 / -3 | `ant` CLI bumped to 1.7.0; `anthropic-java` bumped to 2.30.0 |
| managed-agents/multi-agent.md | Modified | +1 / -1 | Minor wording: "list" → "roster" (no functional change) |

---
*Generated from Claude API documentation changes detected on 2026-05-09*
