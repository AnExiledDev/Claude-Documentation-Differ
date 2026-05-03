# Claude API Documentation Changes — 2026-05-03

## Summary

Three pages were updated, all focused on Claude Managed Agents. The changes clarify data retention and data residency limitations for Managed Agents, and add new Console observability and debugging guidance to the events-and-streaming reference.

## Significant Changes

### Managed Agents

- **ZDR exclusion for Claude Managed Agents**: The Zero Data Retention (ZDR) documentation now explicitly lists Managed Agents as a non-eligible surface, noting that session transcripts can be deleted manually but there is no automatic deletion.
  > "Claude Managed Agents is a stateful resource. You can delete session transcripts, but there is no automatic deletion."
  - *Implication*: Developers relying on ZDR for compliance must be aware that Managed Agent sessions are stateful and outside automatic ZDR coverage.
  - *Source*: [API and Data Retention](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention.md)

- **`inference_geo` not supported in Managed Agents**: The data residency page now includes a note clarifying that the `inference_geo` per-request parameter is not available for Managed Agents sessions, though Workspace-level geo configuration is still honored.
  > "Claude Managed Agents does not support the `inference_geo` parameter, but respects the Workspace geo configured in Console."
  - *Implication*: Developers cannot pin inference geography on a per-request basis within Managed Agent sessions; geo control must be set at the workspace level via the Console.
  - *Source*: [Data Residency](https://platform.claude.com/docs/en/build-with-claude/data-residency.md)

- **Console observability for agent sessions**: The events-and-streaming page now includes a `## Console observability` section describing a visual timeline interface in the Claude Console for inspecting Managed Agent sessions.
  > "Navigate to the Claude Managed Agents section in the Console to see: **Session list** — All sessions with their status, creation time, and model; **Tracing view** — A chronological view of events (content, timestamps, token usage) within a session. These are only accessible to Developers and Admins; **Tool execution** — Details of each tool call and its result"
  - *Implication*: Developers and admins can inspect session activity, token usage, and tool execution visually without querying the API directly. Tracing view access is role-restricted.
  - *Source*: [Events and Streaming](https://platform.claude.com/docs/en/managed-agents/events-and-streaming.md)

- **Debugging tips section added**: A new `## Debugging tips` section at the end of the events-and-streaming reference provides guidance on diagnosing common Managed Agent issues.
  > "**Check session events** — Session errors are conveyed through the `session.error` event; **Review tool results** — Tool execution failures often explain unexpected agent behavior; **Track token usage** — Monitor token consumption to optimize prompts and reduce costs; **Use system prompts** — Add logging instructions to the system prompt to make the agent explain its reasoning"
  - *Implication*: Consolidates operational debugging guidance in one place; developers encountering unexpected agent behavior have a structured starting point.
  - *Source*: [Events and Streaming](https://platform.claude.com/docs/en/managed-agents/events-and-streaming.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `build-with-claude/api-and-data-retention.md` | Modified | +1 / -0 | Noted Managed Agents is excluded from ZDR with no automatic deletion |
| `build-with-claude/data-residency.md` | Modified | +4 / -0 | Noted `inference_geo` is unsupported in Managed Agents; workspace geo applies |
| `managed-agents/events-and-streaming.md` | Modified | +16 / -1 | Added Console observability and debugging tips sections |

---
*Generated from Claude API documentation changes detected on 2026-05-03*
