# Claude API Documentation Changes — 2026-05-11

## Summary

Six pages in the Managed Agents documentation section were updated with a mix of meaningful clarifications and editorial polish. The most developer-relevant changes are: a behavioral clarification that agent updates only generate a new version when the configuration actually changes, C# SDK examples updated to use typed enum values instead of raw strings, and an explicit naming of the required beta header.

## Significant Changes

### Agent SDK — C# Typed Enums

- **C# SDK: `Type` fields now use enum constants instead of raw strings**: Code examples in `sessions.md` and `skills.md` have been updated to use typed enum values for the `Type` parameter in agent and skill params.
  > ```csharp
  > // Before
  > Type = "agent"
  > // After
  > Type = Anthropic.Models.Beta.Sessions.Type.Agent
  > ```
  > ```csharp
  > // Before
  > new BetaManagedAgentsAnthropicSkillParams { Type = "anthropic", SkillID = "xlsx" }
  > // After
  > new BetaManagedAgentsAnthropicSkillParams { Type = BetaManagedAgentsAnthropicSkillParamsType.Anthropic, SkillID = "xlsx" }
  > ```
  - *Implication*: C# developers should migrate from raw string literals to the typed enum constants shown in the updated examples. Using string literals may still compile but won't benefit from type safety.
  - *Source*: [Sessions](https://platform.claude.com/docs/en/managed-agents/sessions.md), [Skills](https://platform.claude.com/docs/en/managed-agents/skills.md)

### Agent Versioning Behavior

- **Agent updates generate a new version only when configuration changes**: The update operation description was qualified to clarify that a new version is not created on every PATCH call — only when the submitted configuration differs from the current state.
  > Before: "Updating an agent generates a new version."
  > After: "Updating an agent generates a new version when the configuration changes."
  - *Implication*: Developers who monitor `agent.version` to detect changes should be aware that no-op updates will not increment the version number.
  - *Source*: [Agent Setup](https://platform.claude.com/docs/en/managed-agents/agent-setup.md)

### Permission Policies — `always_ask` Clarification

- **`always_ask` policy description rewritten for clarity**: The previous description referenced internal event names (`session.status_idle`, `user.tool_confirmation`) without context. The new text describes the behavior in plain language and cross-references the confirmation request flow.
  > Before: "The session emits a `session.status_idle` event and waits for a `user.tool_confirmation` event before executing."
  > After: "The session pauses and waits for your approval before executing. See [Respond to confirmation requests](#respond-to-confirmation-requests) for the event flow."
  - *Implication*: No behavior change; this is a documentation improvement. The linked section provides the full event-based flow for developers who need the implementation details.
  - *Source*: [Permission Policies](https://platform.claude.com/docs/en/managed-agents/permission-policies.md)

### Beta Header Explicitly Named

- **Required beta header now explicitly identified in the overview**: The getting-started checklist previously referred to "the beta header above" by implication. It now names the header value directly.
  > Before: "The beta header above on all requests"
  > After: "The `managed-agents-2026-04-01` beta header on all requests"
  - *Implication*: All Managed Agents API requests must include `anthropic-beta: managed-agents-2026-04-01`. This was always required; the docs now state it unambiguously in the prerequisites list.
  - *Source*: [Overview](https://platform.claude.com/docs/en/managed-agents/overview.md)

### `description` Field Explicitly Listed as a Scalar Field

- **`description` added to the scalar fields list in agent update docs**: The documentation of which fields are "scalar" (replaced on update, clearable with `null`) previously listed `model`, `system`, `name`, etc.` The `description` field is now explicitly named.
  > Before: "`model`, `system`, `name`, etc."
  > After: "`model`, `system`, `name`, `description`"
  - *Implication*: Confirms that `description` follows the same update semantics as other scalar fields — it can be cleared by passing `null`.
  - *Source*: [Agent Setup](https://platform.claude.com/docs/en/managed-agents/agent-setup.md)

### Outcomes and Multiagent Features Status

- **Research preview features relabeled as "beta (research preview)"**: The outcomes and multiagent features were previously described as being in "research preview"; they are now described as "in beta (research preview)".
  > "Certain features (outcomes and multiagent) are in beta (research preview)."
  - *Source*: [Overview](https://platform.claude.com/docs/en/managed-agents/overview.md)

## Notable Details

- **Memory store size unit formatting**: `100KB (~25K tokens)` was corrected to `100 kB (~25k tokens)` (SI-style lowercase). The limit itself is unchanged.
- **Memory version retention language softened**: "may retain" and "may be deleted" phrasing replaced with "might retain" and "might be deleted" throughout `memory.md`, signaling that the 30-day retention window is not a strict guarantee in either direction.
- **"file systems" → "filesystems"**: The overview now uses the single-word form when describing stateful session persistence.
- **"comprehensive set of built-in tools" → "set of built-in tools"**: The word "comprehensive" was removed from the tools description in the overview. Minor editorial change with no API impact.
- **Session status table punctuation**: Trailing periods added to the `running`, `rescheduling`, and `terminated` status descriptions in the session lifecycle table. Formatting only.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| managed-agents/overview.md | Modified | +11/-11 | Beta header named explicitly, list formatting updated, "research preview" → "beta (research preview)" |
| managed-agents/sessions.md | Modified | +5/-5 | C# SDK typed enum for `Type` field, link text update, status table punctuation |
| managed-agents/memory.md | Modified | +4/-4 | Size unit formatting, wording softened ("may" → "might"), restore instructions reworded |
| managed-agents/agent-setup.md | Modified | +3/-3 | Versioning clarified (only on config change), `description` added to scalar fields list |
| managed-agents/skills.md | Modified | +2/-2 | C# SDK typed enums for `Type` in skill params |
| managed-agents/permission-policies.md | Modified | +1/-1 | `always_ask` description rewritten with plain language and cross-reference |

---
*Generated from Claude API documentation changes detected on 2026-05-11*
