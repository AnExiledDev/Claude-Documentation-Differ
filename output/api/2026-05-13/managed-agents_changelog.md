# Claude API Documentation Changes — 2026-05-13

## Summary

Thirteen managed-agents documentation pages were updated. The most substantive changes are: a new AWS availability note for Managed Agents, Claude Opus 4.7 added to fast mode support, an API schema correction for `stop_reason.event_ids`, a clarification that MCP toolset permission policy uses `default_config.permission_policy`, a skills page restructure (field reference table moved inline before code examples, section renamed), and a Go SDK simplification for the agent parameter. Across eight pages, the CLI `--format yaml` flag was replaced with `--raw-output` in all example code.

## Significant Changes

### Platform Availability

- **Claude Managed Agents now available on AWS**: A new `<Note>` was added to the overview page documenting AWS availability.
  > Claude Managed Agents is also available on Claude Platform on AWS, with some differences in feature availability and session behavior. See [Claude Managed Agents](/docs/en/build-with-claude/claude-platform-on-aws#claude-managed-agents) in the Claude Platform on AWS guide.
  - *Implication*: Developers targeting AWS deployments should review the linked guide for behavioral differences before migrating or building on that platform.
  - *Source*: [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview.md)

### Models

- **Claude Opus 4.7 added to fast mode tip**: The agent-setup page previously described fast mode as applying only to Claude Opus 4.6. It now covers both 4.6 and 4.7, and the example uses the 4.7 model ID.
  > To use Claude Opus 4.6 or Claude Opus 4.7 with fast mode, pass `model` as an object: `{"id": "claude-opus-4-7", "speed": "fast"}`.
  - *Implication*: Agents using fast mode should update their model ID to `claude-opus-4-7` to use the latest generation.
  - *Source*: [Agent setup](https://platform.claude.com/docs/en/managed-agents/agent-setup.md)

### API Schema

- **Agent response now includes a `type` field**: The agent-setup page updated its description of the create-agent response object.
  > The response echoes your configuration and adds `id`, `type`, `version`, `created_at`, `updated_at`, and `archived_at` fields.
  - *Implication*: Code parsing the create-agent response may encounter a new `type` field; it should not break existing parsers but is now officially documented.
  - *Source*: [Agent setup](https://platform.claude.com/docs/en/managed-agents/agent-setup.md)

- **Agent version increment behavior clarified**: The description of when `version` increments was tightened.
  > The `version` starts at 1 and increments each time an update changes the agent. *(previously: "each time you update the agent")*
  - *Implication*: No-op updates may no longer bump the version counter; code that relied on version incrementing on every `PUT` should not assume this.
  - *Source*: [Agent setup](https://platform.claude.com/docs/en/managed-agents/agent-setup.md)

- **`stop_reason.event_ids` path corrected** (permission-policies): The event_ids field for tool confirmation was previously documented under a deeper nesting path.
  > The blocking event IDs are in the `stop_reason.event_ids` array. *(previously: `stop_reason.requires_action.event_ids`)*
  - *Implication*: Any code reading `stop_reason.requires_action.event_ids` to resolve `always_ask` tool confirmations must be updated to `stop_reason.event_ids`.
  - *Source*: [Permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies.md)

- **MCP toolset permission policy field path corrected**: The permission-policies page clarified the correct field path when configuring auto-approval for MCP tools.
  > To auto-approve tools from a trusted MCP server, set `default_config.permission_policy` on the `mcp_toolset` entry. *(previously: `permission_policy`)*
  - *Implication*: Developers configuring MCP toolset permission policies should use `default_config.permission_policy`; using the bare `permission_policy` path may not be honored.
  - *Source*: [Permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies.md)

- **Session deletion now explicitly preserves vaults and skills**: The sessions page expanded its list of independent resources unaffected by session deletion.
  > Files, memory stores, vaults, skills, environments, and agents are independent resources and are not affected by session deletion. *(previously did not mention vaults or skills)*
  - *Implication*: Vaults and skills persist after session deletion; developers do not need to re-create them for subsequent sessions.
  - *Source*: [Sessions](https://platform.claude.com/docs/en/managed-agents/sessions.md)

### Sessions

- **Two-step session lifecycle explicitly documented**: The sessions intro paragraph was rewritten to call out the create-then-send lifecycle.
  > Sessions follow a two-step lifecycle: first create the session to provision its container, then send a user event to start work.
  - *Implication*: Clarifies that a newly created session is idle until a user event is sent; no behavior change, but the docs now match the actual API contract.
  - *Source*: [Sessions](https://platform.claude.com/docs/en/managed-agents/sessions.md)

- **"Starting the session" link target updated**: Internal links that pointed to `#user-events` now point to `#event-types`, matching the current anchor on the events-and-streaming page. This affects the "starting the session" section and the session deletion interrupt note.
  - *Implication*: Deep-linked documentation URLs using the old anchor (`#user-events`) may break; update to `#event-types`.
  - *Source*: [Sessions](https://platform.claude.com/docs/en/managed-agents/sessions.md)

### Skills

- **Skills page restructured — "Enable skills on a session" renamed and field reference moved inline**: The section heading changed from "Enable skills on a session" to "Attach skills to an agent". The `skills` array field reference table (previously a standalone "Skill types" section at the end of the page) is now placed directly before the code examples.
  > Each entry in the `skills` array uses the following fields: `type`, `skill_id`, `version`
  - *Implication*: The page now groups schema documentation and code examples together, making it easier to follow when attaching skills. No API change — purely organizational. The terminology "organization-authored skills" is also replaced with "workspace-authored skills".
  - *Source*: [Skills](https://platform.claude.com/docs/en/managed-agents/skills.md)

### SDKs

- **Go SDK agent parameter simplified in onboarding example**: The Go session creation example was changed to pass `agent` as a plain string (`OfString`) instead of a structured `BetaManagedAgentsAgentParams` object.
  > ```go
  > Agent: anthropic.BetaSessionNewParamsAgentUnion{
  >     OfString: anthropic.String("agent_01J8XkN5uT3vHpLqRfWdY2"),
  > },
  > ```
  *(previously required `OfBetaManagedAgentsAgents` with explicit `Type`, `ID`, and `Version` fields)*
  - *Implication*: Existing Go code using the verbose struct form still works if the SDK accepts it, but new code should use the simpler string form. Developers should verify their SDK version supports `OfString`.
  - *Source*: [Onboarding](https://platform.claude.com/docs/en/managed-agents/onboarding.md)

- **Onboarding step 1 now requires copying environment ID**: The Console onboarding instruction was updated to include the environment ID alongside the agent ID.
  > Copy the agent ID and environment ID from Console. *(previously: "Copy the agent ID from Console output")*
  - *Implication*: Both IDs are required when creating sessions; previously the docs only mentioned the agent ID, which could cause incomplete session creation.
  - *Source*: [Onboarding](https://platform.claude.com/docs/en/managed-agents/onboarding.md)

### CLI

- **`--format yaml` flag replaced with `--raw-output` across all CLI examples**: Eight pages (define-outcomes, files, github, mcp-connector, dreams, vaults, memory, permission-policies) updated their `ant` CLI code snippets to replace `--transform id --format yaml` with `--transform id --raw-output`.
  - *Implication*: The `--format yaml` flag is no longer the correct way to extract scalar values from CLI output. Scripts using `--format yaml` for ID extraction should be updated to `--raw-output`.
  - *Sources*: [Define outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes.md), [Files](https://platform.claude.com/docs/en/managed-agents/files.md), [GitHub](https://platform.claude.com/docs/en/managed-agents/github.md), [MCP Connector](https://platform.claude.com/docs/en/managed-agents/mcp-connector.md), [Dreams](https://platform.claude.com/docs/en/managed-agents/dreams.md), [Vaults](https://platform.claude.com/docs/en/managed-agents/vaults.md), [Memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

## Minor Changes

- **`memory.md`**: Multiple `<CodeGroup>` components updated with `defaultLanguage="CLI"`. Minor wording: "anything the agent learned" → "any state the agent built up"; "The SDKs set" → "The SDK sets"; `memories.update()` → `memories.update` (parentheses removed from method reference). Memory access default clarification reworded to show `read_write` explicitly in the example. (+22/-20 lines)
- **`onboarding.md`**: All multi-language code examples in the session creation block marked as `nocheck` to suppress linting. (+13/-17 lines)
- **`sessions.md`**: All `<CodeGroup>` blocks updated with `defaultLanguage="CLI"`; curl/Python/TypeScript/C#/Go/Java/PHP/Ruby examples marked `nocheck`. "Events and streaming" internal link renamed to "Session event stream". (+35/-29 lines)
- **`permission-policies.md`**: Stray blank line removed from PHP code block; `<CodeGroup>` blocks updated with `defaultLanguage="CLI"`. (+6/-7 lines)
- **`agent-setup.md`**: Fast mode tip updated (see Significant Changes). (+2/-2 lines)
- **`dreams.md`**: CLI flag `--format yaml` → `--raw-output`. (+1/-1 lines)
- **`github.md`**: CLI flag `--format yaml` → `--raw-output`. (+2/-2 lines)
- **`mcp-connector.md`**: CLI flag `--format yaml` → `--raw-output`. (+2/-2 lines)

## Migration Notes

- **`stop_reason.event_ids` path change**: If your application reads `stop_reason.requires_action.event_ids` when handling `always_ask` tool confirmation events, update to `stop_reason.event_ids`. The old path is no longer documented.
- **`default_config.permission_policy` for MCP toolsets**: If you set `permission_policy` directly on an `mcp_toolset` entry, move it under `default_config.permission_policy`.
- **CLI `--raw-output` flag**: Replace any `--transform <expr> --format yaml` patterns in `ant` CLI scripts with `--transform <expr> --raw-output`.
- **Go SDK `OfString` for agent parameter**: Update Go session creation code from the `OfBetaManagedAgentsAgents` struct form to `OfString` for the agent parameter.

## Notable Details

- The `<CodeGroup defaultLanguage="CLI">` attribute was added to a large number of code blocks across sessions, memory, permission-policies, onboarding, and skills. This is a UI hint that defaults the displayed language tab to CLI in the rendered docs — no API behavior change, but indicates the CLI is being treated as the primary interface for these examples.
- The sessions page description changed "running agent instance" to just "agent instance" — subtle wording that acknowledges sessions may be idle (provisioned but not executing).
- Custom skills terminology shifted from "organization" to "workspace" throughout the skills page, consistent with the platform's workspace scoping model.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| sessions.md | Modified | SIGNIFICANT | +35/-29 | Two-step lifecycle docs, `stop_reason.event_ids`, vaults/skills in deletion note, `nocheck` on all code blocks |
| memory.md | Modified | SIGNIFICANT | +22/-20 | `defaultLanguage="CLI"` on CodeGroups, minor wording fixes, `--raw-output` CLI flag |
| onboarding.md | Modified | SIGNIFICANT | +13/-17 | Environment ID added to step 1, Go SDK simplified, code blocks marked `nocheck` |
| skills.md | Modified | SIGNIFICANT | +15/-15 | Section renamed, field reference table moved inline, "workspace" vs "organization" |
| permission-policies.md | Modified | SIGNIFICANT | +6/-7 | `default_config.permission_policy`, `stop_reason.event_ids`, `defaultLanguage="CLI"` |
| overview.md | Modified | SIGNIFICANT | +5/-1 | New AWS availability note |
| define-outcomes.md | Modified | SIGNIFICANT | +3/-3 | CLI `--raw-output` flag across examples |
| files.md | Modified | SIGNIFICANT | +3/-3 | CLI `--raw-output` flag across examples |
| vaults.md | Modified | SIGNIFICANT | +3/-3 | CLI `--raw-output` flag across examples |
| agent-setup.md | Modified | MINOR | +2/-2 | Opus 4.7 fast mode, `type` field in response, version increment wording |
| github.md | Modified | MINOR | +2/-2 | CLI `--raw-output` flag |
| mcp-connector.md | Modified | MINOR | +2/-2 | CLI `--raw-output` flag |
| dreams.md | Modified | MINOR | +1/-1 | CLI `--raw-output` flag |

---
*Generated from Claude API documentation changes detected on 2026-05-13*
