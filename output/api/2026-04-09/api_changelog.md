# Claude API Documentation Changes — 2026-04-09

## Summary

This release documents the launch of **Claude Managed Agents** — a beta platform for running stateful, versioned AI agents in managed cloud containers — along with four new beta APIs (`/v1/agents`, `/v1/sessions`, `/v1/environments`, `/v1/vaults`), a new official CLI SDK (`ant`), and a new model identifier `claude-mythos-preview`. Across the existing beta Messages and Message Batches APIs, `stop_details` is added to response objects and a new `output-300k-2026-03-24` beta header is registered. The diff spans 411 new pages and 292 modified pages (+155,716 / −3,990 lines), primarily due to cross-SDK mirroring of the new Managed Agents API reference across Python, TypeScript, Go, Java, Ruby, C#, and the CLI.

---

## Significant Changes

### Claude Managed Agents — New Beta APIs

A new managed infrastructure layer called **Claude Managed Agents** introduces four coordinated beta API resources, all gated behind the single header `managed-agents-2026-04-01`.

#### Agents API — `POST /v1/agents`

- **New versioned agent configurations**: Agents are reusable, versioned objects that bundle a model, optional MCP server connections, skills, and metadata.
  > `model: BetaManagedAgentsModel or BetaManagedAgentsModelConfigParams` — Model identifier. Accepts the model string, e.g. `claude-opus-4-6`, or a `model_config` object for additional configuration control
  > `skills: optional array of BetaManagedAgentsSkillParams` — Skills available to the agent. Maximum 20.
  > `mcp_servers: optional array of BetaManagedAgentsURLMCPServerParams` — MCP servers this agent connects to. Maximum 20.
  - *Implication*: Agents are versioned; callers can pin a session to a specific agent version or always use the latest.
  - *Source*: [Agents API](https://platform.claude.com/docs/en/api/beta/agents/create.md)

- **Model speed mode**: Agent configs support a `speed` field on the model config object.
  > `speed: optional "standard" or "fast"` — Inference speed mode. `fast` provides significantly faster output token generation at premium pricing. Not all models support `fast`; invalid combinations are rejected at create time.
  - *Implication*: The `fast` mode (previously `fast-mode-2026-02-01` beta) is now surfaced as a first-class model config parameter for Managed Agents.

#### Sessions API — `POST /v1/sessions`

- **Stateful agent sessions in cloud containers**: Sessions run an agent inside a managed container, accepting GitHub repository or Files API file mounts and optional vault credential injection.
  > `resources: optional array of BetaManagedAgentsGitHubRepositoryResourceParams or BetaManagedAgentsFileResourceParams` — Resources (e.g. repositories, files) to mount into the session's container.
  > `vault_ids: optional array of string` — Vault IDs for stored credentials the agent can use during the session.

- **GitHub repository resource**: Sessions can mount a repository with branch or commit-level checkout control.
  > `checkout: optional BetaManagedAgentsBranchCheckout or BetaManagedAgentsCommitCheckout` — Branch or commit to check out. Defaults to the repository's default branch.
  > `mount_path: optional string` — Mount path in the container. Defaults to `/workspace/<repo-name>`.

- **Files API file resource**: Files uploaded via the Files API can be injected directly into a session container.
  > `mount_path: optional string` — Mount path in the container. Defaults to `/mnt/session/uploads/<file_id>`.

- **SSE event stream**: Sessions expose a streaming endpoint `GET /v1/sessions/{id}/events/stream` returning 17+ typed event variants including user messages, tool confirmations, and interrupts.
  > `BetaManagedAgentsStreamSessionEvents = BetaManagedAgentsUserMessageEvent or BetaManagedAgentsUserInterruptEvent or BetaManagedAgentsUserToolConfirmationEvent or 17 more`
  - *Implication*: Developers can observe agent activity in real-time over SSE without polling.
  - *Source*: [Sessions API](https://platform.claude.com/docs/en/api/beta/sessions/create.md), [Stream Events](https://platform.claude.com/docs/en/api/beta/sessions/events/stream.md)

#### Environments API — `POST /v1/environments`

- **Container templates for sessions**: Environments define reusable container configuration. The only documented config type at launch is `"cloud"`.
  > `config: optional BetaCloudConfigParams` — Request params for `cloud` environment configuration. Fields default to null; on update, omitted fields preserve the existing value.
  - *Source*: [Environments API](https://platform.claude.com/docs/en/api/beta/environments/create.md)

#### Vaults API — `POST /v1/vaults`

- **Credential storage for agents**: Vaults store named credentials that can be injected into sessions, keeping secrets out of agent definitions.
  > A vault that stores credentials for use by agents during sessions.
  > `display_name: string` — Human-readable name for the vault. 1-255 characters.
  - *Source*: [Vaults API](https://platform.claude.com/docs/en/api/beta/vaults/create.md), [Vault Credentials](https://platform.claude.com/docs/en/api/beta/vaults/credentials.md)

#### Managed Agents Beta Header

- **New endpoint-scoped beta header**: Unlike per-request beta flags, all Managed Agents endpoints share a single beta header:
  > `| /v1/agents`, `/v1/sessions`, `/v1/environments` | `managed-agents-2026-04-01` |`
  - *Implication*: Developers must include `anthropic-beta: managed-agents-2026-04-01` on all Managed Agents requests. This header does not apply to `/v1/messages`.
  - *Source*: [Beta Headers](https://platform.claude.com/docs/en/api/beta-headers.md)

---

### Models

- **New model: `claude-mythos-preview`**: Added to the enumerated model list across all Messages API, Token Counting API, and Message Batches API endpoints (both beta and non-beta namespaces).
  > `"claude-mythos-preview"` — New class of intelligence, strongest in coding and cybersecurity
  - *Implication*: `claude-mythos-preview` is now a valid `model` parameter value in all message-creation endpoints. The preview suffix suggests this may be an early-access identifier.

- **`claude-opus-4-6` description updated**: The model description changed from "Most intelligent model for building agents and coding" to:
  > `"claude-opus-4-6"` — Frontier intelligence for long-running agents and coding
  - *Implication*: Wording change only; no capability or parameter change. May reflect a repositioning relative to the new `claude-mythos-preview` model.

---

### Messages API — New `stop_details` Field

- **Structured refusal information added to responses**: `BetaMessage` now includes a `stop_details` field (object count increased from 7 to 8 fields) and it appears in streaming `delta` objects as well.
  > `stop_details: BetaRefusalStopDetails` — Structured information about a refusal.
  > `category: "cyber" or "bio"` — The policy category that triggered the refusal. `null` when the refusal doesn't map to a named category.
  > `explanation: string` — Human-readable explanation of the refusal. This text is not guaranteed to be stable. `null` when no explanation is available for the category.
  > `type: "refusal"`
  - *Implication*: Developers can now programmatically detect and distinguish refusals triggered by cybersecurity versus biosecurity policies, rather than inferring from stop reason alone. The `explanation` field is explicitly not guaranteed stable — do not parse it as a structured value.
  - *Source*: [Beta Messages Create](https://platform.claude.com/docs/en/api/beta/messages/create.md)

---

### New Beta Header: `output-300k-2026-03-24`

- **`output-300k-2026-03-24` beta header added to all endpoint enumerations**: This new beta flag appears in the `AnthropicBeta` union across Messages, Message Batches, Token Counting, Files, and all new Managed Agents endpoints.
  > `"output-300k-2026-03-24"`
  - *Implication*: This header likely enables a 300K output token limit, extending beyond the existing `output-128k-2025-02-19`. No additional documentation was found in this diff; consult beta feature documentation when available.
  - *Source*: [Beta Types](https://platform.claude.com/docs/en/api/beta.md)

---

### Files API Update

- **New `scope_id` filter on `GET /v1/files`**: The list files endpoint gains a `scope_id` query parameter.
  > `scope_id: optional string` — Filter by scope ID. Only returns files associated with the specified scope (e.g., a session ID).
  - *Implication*: Files uploaded in the context of a Managed Agents session can now be enumerated by session ID, supporting cleanup and audit workflows.
  - *Source*: [Files List](https://platform.claude.com/docs/en/api/beta/files/list.md)

---

### New `ant` CLI SDK

- **Official command-line SDK added**: A new `ant` CLI binary is documented, providing terminal access to all Claude API resources.
  > The `ant` CLI provides access to the Claude API from your terminal. Every API resource is exposed as a subcommand, with output formatting, response filtering, and support for YAML or JSON file input that make it practical for both interactive exploration and automation.
  - Installed via Homebrew (`brew install anthropics/tap/ant`), curl (Linux/WSL), or `go install`
  - Reads `ANTHROPIC_API_KEY` from environment
  - Supports `--transform` for response field extraction without separate JSON tooling
  - List endpoints paginate automatically
  - Claude Code understands how to use `ant` natively
  - *Implication*: The CLI exposes the Managed Agents API as `ant beta:agents`, `ant beta:sessions`, etc. across all new resource types.
  - *Source*: [CLI SDK](https://platform.claude.com/docs/en/api/sdks/cli.md)

---

### API Reference Example Fixes

- **`?beta=true` removed from curl examples**: Example HTTP snippets for Models API (`GET /v1/models`), Messages API (`POST /v1/messages`), Token Counting (`POST /v1/messages/count_tokens`), and Message Batches API (`GET /v1/messages/batches`) no longer append `?beta=true` to the URL.
  - *Implication*: The `?beta=true` query parameter was never part of the stable API surface — it was a documentation artifact. Developers who replicated these examples verbatim should remove it.

- **`claude-mythos-preview` used in count_tokens example**: The token counting curl example was updated to use `claude-mythos-preview` as the model value.

---

### Beta Headers Page Updated

- **Shell and CLI code examples repositioned**: The `curl` Shell example and new `ant` CLI example are now shown first in the code group, before the Python and TypeScript examples.
- **New "Endpoint-specific headers" section**: Documents that some beta features apply at the endpoint level rather than per-request, with `managed-agents-2026-04-01` as the current example.
  - *Source*: [Beta Headers](https://platform.claude.com/docs/en/api/beta-headers.md)

---

### API Overview Page Updated

- **Explicitly lists all current beta APIs**: The overview now enumerates the beta API surface with descriptions:
  > Files API, Skills API, Agents API, Sessions API, Environments API
  - *Source*: [API Overview](https://platform.claude.com/docs/en/api/overview.md)

---

## New Pages

The following new API reference sections were added. The Managed Agents API reference is mirrored across all SDK languages (Python, TypeScript, Go, Java, Ruby, C#) and the CLI — only the canonical REST reference is listed here.

- **`en_api_beta_agents.md`** — Agents API REST reference: create, list, retrieve, update, archive, version management. [View](https://platform.claude.com/docs/en/api/beta/agents.md)
- **`en_api_beta_sessions.md`** — Sessions API REST reference: create, list, retrieve, update, archive, delete, events (stream/send/list), resources (add/list/retrieve/update/delete). [View](https://platform.claude.com/docs/en/api/beta/sessions.md)
- **`en_api_beta_environments.md`** — Environments API REST reference: create, list, retrieve, update, archive, delete. [View](https://platform.claude.com/docs/en/api/beta/environments.md)
- **`en_api_beta_vaults.md`** — Vaults API REST reference: create, list, retrieve, update, archive, delete, credentials CRUD. [View](https://platform.claude.com/docs/en/api/beta/vaults.md)
- **`en_api_sdks_cli.md`** — Full CLI (`ant`) SDK documentation: installation, authentication, usage patterns, request building, response transforms. [View](https://platform.claude.com/docs/en/api/sdks/cli.md)
- **`en_api_cli_beta.md`** and sub-pages — CLI reference for all beta Managed Agents, Files, Messages, Models, Sessions, Skills, and Vaults endpoints via the `ant` CLI. [View](https://platform.claude.com/docs/en/api/cli/beta.md)

---

## Notable Details

- **Vaults beta header**: The Vaults API (`/v1/vaults`) shares the `managed-agents-2026-04-01` header; the endpoint is not listed explicitly in the beta headers table but is part of the Managed Agents platform.
- **Skills beta header unchanged**: The Skills API continues to use `skills-2025-10-02` — it is distinct from the Managed Agents beta header even though skills can be attached to agents.
- **`BetaMessage` field count change**: `BetaMessage = object { id, container, content, 8 more }` (was `7 more`). The new field is `stop_details`.
- **Session events streaming returns a 20+ variant union**: `BetaManagedAgentsStreamSessionEvents` includes `UserMessageEvent`, `UserInterruptEvent`, `UserToolConfirmationEvent`, and at least 17 others, covering the full lifecycle of an agent session.
- **Agent model config `speed` field is beta-time validated**: Invalid model/speed combinations are rejected at create time, not at inference time.
- **`explanation` in `BetaRefusalStopDetails` is explicitly unstable**: The documentation states it is "not guaranteed to be stable" and warns `null` when no explanation is available. Do not rely on this string for production logic.
- **Files API `scope_id` ties to Managed Agents**: The new filter enables scoping file listings to a session — this is the linkage between the Files API and the Sessions API for resource cleanup.

---

## Changes by Page

| Page | Type | Summary |
|------|------|---------|
| `en_api_beta/agents.md` + sub-pages | New | Agents API reference (all CRUD + versioning) |
| `en_api_beta/sessions.md` + sub-pages | New | Sessions API reference (CRUD + events + resources) |
| `en_api_beta/environments.md` + sub-pages | New | Environments API reference (CRUD) |
| `en_api_beta/vaults.md` + sub-pages | New | Vaults + Credentials API reference (CRUD) |
| `en_api_sdks_cli.md` | New | Full CLI SDK documentation page |
| `en_api_cli/beta.md` + ~50 sub-pages | New | CLI reference for all beta endpoints |
| `{python,typescript,go,java,ruby,csharp}/beta/agents` etc. | New | SDK-specific Managed Agents reference (×6 languages) |
| `en_api_beta.md` | Modified | Added `output-300k-2026-03-24` to `AnthropicBeta` union |
| `en_api_beta_messages_create.md` | Modified | Added `claude-mythos-preview` model; added `stop_details` to `BetaMessage`; added `stop_details` to streaming delta |
| `en_api_beta_messages_batches.md` | Modified | Added `claude-mythos-preview`; added `output-300k-2026-03-24` beta header; removed retrieve section (moved to sub-page) |
| `en_api_messages_create.md` | Modified | Added `claude-mythos-preview` model; updated `claude-opus-4-6` description |
| `en_api_messages_batches.md` | Modified | Added `claude-mythos-preview`; added `output-300k-2026-03-24`; curl example cleanup |
| `en_api_beta_files_list.md` | Modified | Added `scope_id` query parameter |
| `en_api_beta-headers.md` | Modified | Added CLI example; added endpoint-specific headers section for `managed-agents-2026-04-01` |
| `en_api_overview.md` | Modified | Updated to list all beta APIs including Managed Agents |
| `en_api_client-sdks.md` | Modified | Added CLI (`ant`) as an official SDK with install instructions |
| `en_api_beta_skills.md` / `_versions.md` | Modified | Updated `AnthropicBeta` union to include `output-300k-2026-03-24` |
| All `{sdk}/beta/messages_create.md` pages | Modified | `claude-mythos-preview` + `stop_details` + `output-300k-2026-03-24` propagated across Python, TypeScript, Go, Java, Ruby, C# |

---

*Generated from Claude API documentation changes detected on 2026-04-09*
