# Claude API Documentation Changes — 2026-04-23

## Summary

One page was updated in the Managed Agents (beta) documentation. The primary change adds a new "Resuming an idle session" section to the session event stream reference, documenting session persistence behavior, container checkpointing, and the 30-day checkpoint retention limit.

## Significant Changes

### Managed Agents — Session Lifecycle

- **Session resumption and container checkpointing documented**: The event stream page now explains how idle sessions are checkpointed and how to resume them. When a session goes idle, its full container state (filesystem, installed packages, and agent-created files) is preserved via a checkpoint. Resuming is done by sending a standard `user.message` event to the existing session ID — no new API endpoint is needed.

  > Sessions persist between interactions. Conversation history is preserved unless the session is explicitly deleted. When a session goes idle, its container is checkpointed, preserving the full container state, including the filesystem, installed packages, and any files the agent created.

  - *Implication*: Developers can build workflows that pause and resume across days or weeks without re-running setup steps (installing packages, generating files, etc.), as long as they resume within the checkpoint window.
  - *Source*: [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming.md)

- **30-day checkpoint retention limit**: A `<Note>` block clarifies that while conversation history persists indefinitely (until explicitly deleted), container checkpoints expire 30 days after the session's last activity.

  > While session history is persisted until deleted, checkpoints are only preserved for 30 days after the session's last activity. If your workflow requires the full container state (files, installed tools, and so on) to persist beyond 30 days, send periodic `user.message` events to reset the inactivity timer before the checkpoint expires.

  - *Implication*: Long-lived workflows that depend on the container state (not just conversation history) must send a keep-alive `user.message` event before the 30-day window closes, or risk losing the checkpointed filesystem. This is a meaningful operational constraint for any persistent agent use case.
  - *Source*: [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming.md)

  **Resume example (Python):**
  ```python
  # Resume a previously created session by ID
  client.beta.sessions.events.send(
      "sesn_01...",
      events=[
          {
              "type": "user.message",
              "content": [
                  {
                      "type": "text",
                      "text": "Now run the tests against the changes you made earlier.",
                  },
              ],
          },
      ],
  )
  ```

## Notable Details

- **Event description tense correction**: The descriptions for `agent.tool_use`, `agent.mcp_tool_use`, and `agent.custom_tool_use` in the event types table were updated from past tense ("invoked") to present tense ("invokes"). This is a documentation wording fix with no API behavior change.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| managed-agents/events-and-streaming.md | Modified | +31/-3 | Added "Resuming an idle session" section with checkpoint/persistence details and 30-day retention note |

---
*Generated from Claude API documentation changes detected on 2026-04-23*
