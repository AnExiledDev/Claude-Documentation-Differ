# Claude API Documentation Changes — 2026-05-21

## Summary

This update introduces self-hosted sandboxes as a new environment type for Managed Agents, enabling tool execution on customer-controlled infrastructure. The MCP connector documentation gains a comprehensive field reference, per-tool enable/disable controls, and improved error handling. Several SDK type names were renamed across Go, Java, and C# SDKs.

---

## Significant Changes

### Self-Hosted Sandboxes (New Capability)

- **Self-hosted sandbox environments**: Agents can now run tool execution on customer-owned infrastructure instead of Anthropic-managed cloud containers. Orchestration remains on Anthropic's side while the code, filesystem, and network egress stay within the customer's environment.
  > "Self-hosted sandboxes keep the orchestration on Anthropic's side but move tool execution into infrastructure you control, so the agent's code, filesystem, and network egress never leave your environment."
  - *Implication*: Enables compliance and data-residency use cases. Customer creates a `self_hosted` environment type via API, generates an environment key, and runs an environment worker that polls Anthropic's work queue and executes tool calls locally.
  - Supported worker architectures: always-on (polling) and webhook-triggered (wakes on `session.status_run_started`).
  - Pre-built workers available in the CLI (`ant`) and all SDKs. Platform-specific guides linked for Cloudflare, Daytona, Modal, and Vercel.
  - **Not yet available** on Claude Platform on AWS.
  - *Source*: [Self-hosted sandboxes](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes.md)

- **Self-hosted sandboxes security model**: New dedicated page documenting the shared responsibility model.
  > "Anthropic secures the control plane across all environments: session and work queue integrity, multi-tenant isolation, and agent-context minimization. When you self-host, the following responsibilities fall to you."
  - Customer responsibilities include: container image hardening, network egress controls, `ANTHROPIC_ENVIRONMENT_KEY` storage and rotation, workload isolation, tool-execution blast radius, and log retention.
  - The `ANTHROPIC_ENVIRONMENT_KEY` is scoped to one environment's work queue; Anthropic cannot instantly revoke a leaked key.
  - *Source*: [Security model](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security.md)

### Sessions — Mid-Session Agent Configuration Updates

- **Updating the agent configuration mid-session**: Sessions now support updating `agent.tools` and `agent.mcp_servers` (including permission policies) without creating a new agent version. Updates are session-local and do not propagate back to the underlying agent definition.
  > "You can update a session's `agent.tools` and `agent.mcp_servers`, including permission policies, mid-session without creating a new agent version. Updates are session-local and do not propagate back to the underlying agent."
  - Semantics are full replacement: the provided array replaces the existing value entirely. To preserve existing entries, `GET` the session first, modify the array, then `POST` the update.
  - The session must be `idle` to accept an update; interrupt the session if it is running.
  - *Implication*: Developers can adjust tool access or permission policies between turns without versioning the agent.
  - *Source*: [Start a session](https://platform.claude.com/docs/en/managed-agents/sessions.md)

### MCP Connector — New Documentation Sections

- **`mcp_servers` field reference**: New reference table documenting all fields with constraints.
  > "An agent can declare up to 20 MCP servers. Server names must be unique within the array. Every `mcp_servers` entry must be referenced by an `mcp_toolset` in the `tools` array, and every `mcp_toolset` must reference a declared server. The API rejects agent definitions with unreferenced servers or dangling toolsets."
  - Fields: `type` (required, must be `"url"`), `name` (required, 1–255 chars, used as `mcp_server_name`), `url` (required, up to 2048 chars).
  - *Source*: [MCP connector](https://platform.claude.com/docs/en/managed-agents/mcp-connector.md)

- **Configure which MCP tools are available**: New section documenting per-tool enable/disable control via `default_config` and `configs` on `mcp_toolset`.
  > "By default all tools exposed by the MCP server are enabled. To enable only specific tools, set `default_config.enabled` to `false` and explicitly enable the tools you want."
  - *Implication*: Useful when a server exposes many tools but the agent needs only a subset, or to prevent newly added server tools from being automatically available.

- **MCP tool output handling**: Large MCP tool outputs are now automatically managed.
  > "When an MCP tool output exceeds 100k tokens, it is automatically written to a file in the sandbox. The model receives a truncated preview with the file path and can read the full content from there."

- **Handle connection and authentication failures**: New section with a typed error table replacing the previous prose description.

  | Error type | Meaning |
  |---|---|
  | `mcp_connection_failed_error` | The MCP server could not be reached (network error, timeout, or non-authentication HTTP failure). |
  | `mcp_authentication_failed_error` | The MCP server was reached but rejected the credential from the attached vault. |

  - Credential matching is now documented explicitly: the vault credential's `mcp_server_url` must exactly match the agent's `mcp_servers[].url`, including scheme and trailing slash.
  - *Implication*: Developers can now distinguish network vs. auth failures for targeted remediation.
  - *Source*: [MCP connector](https://platform.claude.com/docs/en/managed-agents/mcp-connector.md)

- **MCP tunnels now supported**: Managed Agents can now connect to private MCP servers via MCP tunnels in addition to remote HTTP servers.
  > "Claude Managed Agents connects to remote MCP servers that expose an HTTP endpoint, or to private MCP servers through [MCP tunnels](/docs/en/agents-and-tools/mcp-tunnels/overview)."

### Multi-Agent — MCP Server Configuration

- **Connect agents to MCP servers**: New comprehensive section documenting how MCP servers and vault credentials interact in multi-agent sessions.
  > "MCP servers are agent-scoped (each agent definition declares its own servers and tools), while vault credentials are session-scoped (`vault_ids` passed at session creation apply to every thread)."
  - Each agent in a multiagent roster declares its own MCP servers; the coordinator does not automatically share subagent servers.
  - A single `vault_ids` list at session creation supplies credentials to all threads.
  - Agents also now explicitly share vault credentials in addition to the container and filesystem.
  - *Source*: [Multiagent sessions](https://platform.claude.com/docs/en/managed-agents/multi-agent.md)

### Events and Streaming — New Events

- **`user.tool_result` event (self-hosted only)**: For sessions using `self_hosted` environments, the integration is responsible for providing `agent_toolset` results. The SDK helpers and CLI handle this automatically; custom workers must implement it directly.
  - *Source*: [Events and streaming](https://platform.claude.com/docs/en/managed-agents/events-and-streaming.md)

- **`session.updated` event**: Emitted when a session update request changes at least one field. Includes only the changed fields. Updates apply on the next turn.
  - *Source*: [Events and streaming](https://platform.claude.com/docs/en/managed-agents/events-and-streaming.md)

### Overview — Feature Status and ZDR Clarification

- **Environment concept expanded**: The "Environment" concept now covers both cloud containers and self-hosted sandboxes.
  > "Configuration for where sessions run: an Anthropic-managed cloud container, or a self-hosted sandbox on your own infrastructure"

- **Beta feature list updated**: Outcomes and multiagent are no longer listed as beta/research preview. MCP tunnels and "dreaming" are now listed as the research-preview features requiring access requests.

- **ZDR and HIPAA BAA eligibility clarified**:
  > "Claude Managed Agents is not currently eligible for Zero Data Retention or HIPAA Business Associate Agreement (BAA) coverage. You retain control over this data: you can delete sessions, and separately delete any files you uploaded, at any time through the API."
  - *Implication*: Developers with ZDR or HIPAA BAA requirements should check the [API and data retention](https://www.anthropic.com/docs/en/manage-claude/api-and-data-retention#feature-eligibility) page for self-hosted sandbox eligibility.
  - *Source*: [Overview](https://platform.claude.com/docs/en/managed-agents/overview.md)

### SDK Type Renames (Go, Java, C#, PHP)

Several SDK types were renamed for consistency. These affect code that references the types directly.

**Go SDK**:
- `BetaManagedAgentsUrlmcpServerParams` → `BetaManagedAgentsURLMCPServerParams`
- `BetaManagedAgentsUrlmcpServerParamsTypeURL` → `BetaManagedAgentsURLMCPServerParamsTypeURL`
- `UnrestrictedNetworkParam` → `BetaUnrestrictedNetworkParam`
- `BetaCloudConfigParams` (direct) → `BetaEnvironmentNewParamsConfigUnion` with `OfCloud` field
- `BetaManagedAgentsMultiagentCoordinatorParams` / `BetaAgentNewParamsMultiagentUnion` → `BetaManagedAgentsMultiagentParams`
- `BetaManagedAgentsRosterAgentParams` / `BetaManagedAgentsRosterEntryUnion` → `BetaManagedAgentsAgentParams` / `BetaManagedAgentsMultiagentRosterEntryParamsUnion`
- `BetaManagedAgentsMemoryStoreResourceParams` → `BetaManagedAgentsMemoryStoreResourceParam`
- `SendEventsParamsUnion` → `BetaManagedAgentsEventParamsUnion`
- `BetaMemoryStores.Archive()` now requires an explicit `BetaMemoryStoreArchiveParams{}` argument
- `BetaMemoryStoreMemoryNewParams.Content` is now a pointer (`anthropic.String(...)`)
- `BetaMemoryStoreMemoryUpdateParams.Precondition` union type → `BetaManagedAgentsPreconditionParam` with explicit `Type` field

**Java SDK**:
- `BetaManagedAgentsUrlmcpServerParams` → `BetaManagedAgentsUrlMcpServerParams`
- `UnrestrictedNetwork` → `BetaUnrestrictedNetwork`
- `BetaManagedAgentsMultiagentCoordinatorParams` → `BetaManagedAgentsMultiagentParams`
- `BetaManagedAgentsRosterAgentParams` → `BetaManagedAgentsAgentParams`
- `BetaManagedAgentsMemoryStoreResourceParams` → `BetaManagedAgentsMemoryStoreResourceParam`
- `StreamEvents` → `BetaManagedAgentsStreamSessionEvents`
- `ThreadStreamParams` → `EventStreamParams`
- `MemoryUpdateParams.Precondition` → `BetaManagedAgentsPrecondition`
- `MemoryListParams.OrderBy.PATH` enum → string `"path"` / `MemoryListParams.OrderBy` string

**C# SDK**:
- `UnrestrictedNetwork` → `BetaUnrestrictedNetwork`
- `BetaManagedAgentsMultiagentCoordinatorParams` → `BetaManagedAgentsMultiagentParams`
- `BetaManagedAgentsRosterAgentParams` removed; agents now passed as plain ID strings
- `BetaManagedAgentsMemoryStoreResourceParams` → `BetaManagedAgentsMemoryStoreResourceParam`
- `ContentSha256Precondition` → `BetaManagedAgentsPrecondition`
- Paginated responses: `.Data` property iteration replaced with `await foreach` + `.Paginate()`

**PHP SDK**:
- `BetaManagedAgentsUrlmcpServerParams` → `BetaManagedAgentsURLMCPServerParams`

*Sources*: [Environments](https://platform.claude.com/docs/en/managed-agents/environments.md), [MCP connector](https://platform.claude.com/docs/en/managed-agents/mcp-connector.md), [Multi-agent](https://platform.claude.com/docs/en/managed-agents/multi-agent.md), [Memory](https://platform.claude.com/docs/en/managed-agents/memory.md), [Permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies.md), [Events and streaming](https://platform.claude.com/docs/en/managed-agents/events-and-streaming.md)

---

## Minor Changes

- **[cloud-containers.md]**: Renamed page heading from "Container reference" to "Cloud container reference"; added note that specs apply to `cloud` environments only, not self-hosted sandboxes. (+3/-1)
- **[files.md]**: CLI command renamed from `beta:sessions:resources create` to `beta:sessions:resources add`; C# resource listing updated to use `Paginate()` with a three-way `Match` covering `memory_store`; file download code examples marked `nocheck`. (+13/-12)
- **[github.md]**: Go/Java/C# SDK type renames for URL MCP server params; C# resource listing updated to use paginated loop. (+12/-8)
- **[quickstart.md]**: `ant` CLI version bumped `1.8.0` → `1.9.1`; Java SDK version bumped `2.32.0` → `2.33.0`; self-hosted sandbox tip added to environment creation step; SDK type fixes. (+17/-14)
- **[agent-setup.md]**: Go SDK code example: removed unused `Type` field from `BetaManagedAgentsModelConfigParams`; fixed indentation. (+2/-3)
- **[skills.md]**: Minor wording/formatting adjustments. (+4/-4)
- **[tools.md]**: Minor wording/formatting adjustments. (+6/-4)
- **[vaults.md]**: Minor wording/formatting adjustments. (+9/-8)

---

## New Pages

- **[self-hosted-sandboxes.md]** — Full guide for running Managed Agent sessions in customer-controlled sandboxes. Covers environment worker setup, always-on and webhook-triggered architectures, sandbox filesystem layout (`/workspace`, `/mnt/session/outputs`), SDK/CLI configuration reference, and platform-specific integration guides. [View](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes.md)
- **[self-hosted-sandboxes-security.md]** — Shared responsibility security model for self-hosted sandbox environments, covering customer obligations for container hardening, network egress, key management, workload isolation, and data retention. [View](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security.md)

---

## Migration Notes

- **Go SDK — `BetaEnvironmentNewParamsConfigUnion`**: Environment creation in Go must now wrap the `BetaCloudConfigParams` inside a `BetaEnvironmentNewParamsConfigUnion{OfCloud: &...}` discriminated union. Direct assignment of `BetaCloudConfigParams` to `Config` no longer compiles.

- **Go SDK — `BetaManagedAgentsURLMCPServerParams`**: Any code using `BetaManagedAgentsUrlmcpServerParams` (lowercase `url`) must be updated to `BetaManagedAgentsURLMCPServerParams` (uppercase `URL`).

- **Go/Java SDK — `SendEventsParamsUnion` / `StreamEvents`**: Go callers must replace `SendEventsParamsUnion` with `BetaManagedAgentsEventParamsUnion`. Java callers must replace `StreamEvents` with `BetaManagedAgentsStreamSessionEvents` in stream iteration type assertions.

- **C#/Java SDK — `BetaUnrestrictedNetwork`**: Replace `UnrestrictedNetwork` / `new UnrestrictedNetwork()` with `BetaUnrestrictedNetwork` / `new BetaUnrestrictedNetwork()`.

- **C# SDK — Paginated resource listing**: Replace synchronous `foreach` over `.Data` with `await foreach` over `.Paginate()` when iterating session resources and memory stores.

- **CLI — `beta:sessions:resources` subcommand**: The `create` subcommand has been renamed to `add`. Update any scripts that call `ant beta:sessions:resources create`.

---

## Notable Details

- The `ANTHROPIC_ENVIRONMENT_KEY` for self-hosted environments is scoped to a single environment's work queue, not the whole workspace. Running untrusted workloads that could exfiltrate this key gives them access only to sessions in that one environment.
- The `mcp_server_name` in the `tools` array and the `name` field in `mcp_servers` must match exactly; it also appears on MCP tool events in the session event stream, making it useful for debugging.
- The `session.updated` event is emitted only when at least one field actually changes; no-op updates do not produce an event.
- The `user.tool_result` event is exclusive to `self_hosted` environments: cloud-container sessions never require this event because Anthropic's container handles tool execution internally.
- Outcomes and multiagent are no longer listed as research-preview features in the overview, suggesting they have graduated to general availability or broader access.

---

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| sessions.md | Modified | SIGNIFICANT | +849/-523 | Mid-session agent config updates; major SDK example updates |
| multi-agent.md | Modified | SIGNIFICANT | +409/-37 | New "Connect agents to MCP servers" section; SDK type renames |
| self-hosted-sandboxes.md | New | SIGNIFICANT | +1464/-0 | New: self-hosted sandbox environments guide |
| mcp-connector.md | Modified | SIGNIFICANT | +72/-10 | Field reference, tool filtering, error types, MCP tunnels support |
| self-hosted-sandboxes-security.md | New | SIGNIFICANT | +23/-0 | New: shared responsibility security model |
| memory.md | Modified | SIGNIFICANT | +27/-22 | Go/Java/C# SDK type renames and API changes |
| environments.md | Modified | SIGNIFICANT | +24/-16 | Scoped to cloud environments; SDK type fixes; links to self-hosted page |
| quickstart.md | Modified | SIGNIFICANT | +17/-14 | CLI 1.9.1, Java SDK 2.33.0; self-hosted tip; SDK type fixes |
| github.md | Modified | SIGNIFICANT | +12/-8 | Go/Java/C# SDK type renames |
| permission-policies.md | Modified | SIGNIFICANT | +12/-12 | Go/Java/PHP SDK type renames |
| files.md | Modified | SIGNIFICANT | +13/-12 | CLI command rename; C# pagination; `nocheck` examples |
| overview.md | Modified | SIGNIFICANT | +7/-4 | Self-hosted sandboxes added; ZDR/BAA clarification; beta feature list updated |
| events-and-streaming.md | Modified | SIGNIFICANT | +7/-5 | New `user.tool_result` and `session.updated` events; Go/Java type renames |
| tools.md | Modified | SIGNIFICANT | +6/-4 | Minor wording/formatting |
| vaults.md | Modified | SIGNIFICANT | +9/-8 | Minor wording/formatting |
| cloud-containers.md | Modified | SIGNIFICANT | +3/-1 | Renamed heading; cloud-only scope note |
| agent-setup.md | Modified | SIGNIFICANT | +2/-3 | Go SDK code cleanup |
| skills.md | Modified | SIGNIFICANT | +4/-4 | Minor wording/formatting |

---

*Generated from Claude API documentation changes detected on 2026-05-21*
