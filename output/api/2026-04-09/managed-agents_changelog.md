# Claude API Documentation Changes — 2026-04-09

## Summary

Anthropic has published full documentation for **Claude Managed Agents**, a new beta product that provides a managed agent harness and infrastructure for running Claude as an autonomous agent. This release adds 20 new pages covering everything from initial setup through advanced features like multi-agent orchestration, persistent memory, and outcome-driven evaluation. All endpoints require the new `managed-agents-2026-04-01` beta header.

---

## Significant Changes

### New Product: Claude Managed Agents (Beta)

Claude Managed Agents is a fully managed infrastructure layer that eliminates the need to build your own agent loop, tool execution sandbox, or conversation history management. Developers create reusable **agents** (configurations) and **environments** (containers), then launch **sessions** that run the agent inside that environment.

> "Claude Managed Agents provides the harness and infrastructure for running Claude as an autonomous agent. Instead of building your own agent loop, tool execution, and runtime, you get a fully managed environment where Claude can read files, run commands, browse the web, and execute code securely. The harness supports built in prompt caching, compaction, and other performance optimizations for high quality, efficient agent outputs."

- *Implication*: Developers who currently implement their own `while True: messages.create(...)` loops can offload the agent loop, sandboxing, and conversation history to Anthropic infrastructure.
- *Source*: [Overview](https://platform.claude.com/docs/en/managed-agents/overview.md)

---

### API: New Endpoints

All new endpoints are under `/v1/` and require `anthropic-beta: managed-agents-2026-04-01`. The SDK sets this header automatically.

#### Agents — `/v1/agents`

Agents are versioned, reusable configurations. Every update to an agent creates a new version; sessions can be pinned to a specific version.

| Endpoint | Description |
|---|---|
| `POST /v1/agents` | Create an agent (model, system prompt, tools, MCP servers, skills) |
| `GET /v1/agents` | List agents |
| `GET /v1/agents/:id` | Retrieve an agent |
| `PATCH /v1/agents/:id` | Update an agent (increments version) |
| `POST /v1/agents/:id/archive` | Archive an agent (read-only; existing sessions continue) |
| `GET /v1/agents/:id/versions` | List all versions of an agent |

Agent configuration fields:

| Field | Notes |
|---|---|
| `name` | Required |
| `model` | Required. All Claude 4.5+ models supported. Pass as object `{"id": "...", "speed": "fast"}` to use fast mode. |
| `system` | System prompt |
| `tools` | Pre-built toolset, MCP toolsets, or custom tools |
| `mcp_servers` | Array of remote MCP server declarations (URL + name; no auth at this level) |
| `skills` | Anthropic pre-built or custom skills |
| `callable_agents` | Other agent IDs this agent may invoke (multi-agent, research preview) |
| `metadata` | Arbitrary key-value pairs |

- *Source*: [Define your agent](https://platform.claude.com/docs/en/managed-agents/agent-setup.md)

#### Environments — `/v1/environments`

Environments define the container configuration where sessions run. Multiple sessions share the same environment definition but each gets its own isolated container instance.

| Endpoint | Description |
|---|---|
| `POST /v1/environments` | Create an environment |
| `GET /v1/environments` | List environments |
| `GET /v1/environments/:id` | Retrieve an environment |

Environment `config` options:
- **`packages`**: Pre-install `apt`, `cargo`, `gem`, `go`, `npm`, or `pip` packages. Packages are cached across sessions sharing the same environment.
- **`networking`**: `unrestricted` (default, full outbound except blocklist) or `limited` (explicit `allowed_hosts` allowlist, with optional booleans `allow_mcp_servers` and `allow_package_managers`).

> "For production deployments, use `limited` networking with an explicit `allowed_hosts` list. Follow the principle of least privilege by granting only the minimum network access your agent requires."

- *Source*: [Cloud environment setup](https://platform.claude.com/docs/en/managed-agents/environments.md)

#### Sessions — `/v1/sessions`

Sessions are running agent instances. Creating a session provisions the container but does not start work; execution is triggered by sending events.

| Endpoint | Description |
|---|---|
| `POST /v1/sessions` | Create a session (references agent ID + environment ID) |
| `GET /v1/sessions` | List sessions |
| `GET /v1/sessions/:id` | Retrieve session + status |
| `POST /v1/sessions/:id/events` | Send events (user messages, interrupts, tool results) |
| `GET /v1/sessions/:id/events` | List all past events |
| `GET /v1/sessions/:id/stream` | Stream events via SSE |
| `POST /v1/sessions/:id/resources` | Add a resource (file, GitHub repo, memory store) to a running session |
| `GET /v1/sessions/:id/resources` | List session resources |
| `DELETE /v1/sessions/:id/resources/:resource_id` | Remove a resource |
| `GET /v1/sessions/:id/threads` | List agent threads (multi-agent, research preview) |
| `GET /v1/sessions/:id/threads/:thread_id/stream` | Stream a specific agent thread |

Sessions support version pinning:

```python
# Latest version (default)
session = client.beta.sessions.create(agent=agent.id, environment_id=environment.id)

# Pinned to a specific version
session = client.beta.sessions.create(
    agent={"type": "agent", "id": agent.id, "version": 1},
    environment_id=environment.id,
)
```

Session statuses: `idle` → `running` → `idle` (or `rescheduling` on transient error, `terminated` on unrecoverable error).

- *Source*: [Start a session](https://platform.claude.com/docs/en/managed-agents/sessions.md)

#### Vaults — `/v1/vaults`

Vaults are a credential store for MCP OAuth and static bearer tokens. Auth is separated from agent definitions to keep secrets out of reusable configurations.

| Endpoint | Description |
|---|---|
| `POST /v1/vaults` | Create a vault (per-user credential container) |
| `POST /v1/vaults/:id/credentials` | Add a credential (MCP OAuth with auto-refresh, or static bearer) |

Credential types:
- `mcp_oauth`: OAuth 2.0, with optional `refresh` block (Anthropic handles token refresh). Supports `none`, `client_secret_basic`, `client_secret_post` auth methods.
- `static_bearer`: Fixed bearer token / API key.

> "Secret fields (`token`, `access_token`, `refresh_token`, `client_secret`) are write-only. They are never returned in API responses."

Reference a vault at session creation via `vault_ids: [vault.id]`.

- *Source*: [Authenticate with vaults](https://platform.claude.com/docs/en/managed-agents/vaults.md)

#### Memory Stores — `/v1/memory_stores` *(Research Preview)*

Memory stores give agents persistent, cross-session memory. The agent automatically reads stores before each task and writes learnings when done.

| Endpoint | Description |
|---|---|
| `POST /v1/memory_stores` | Create a memory store |
| `POST /v1/memory_stores/:id/memories` | Write a memory |
| `GET /v1/memory_stores/:id/memories` | List memories (with optional `path_prefix`) |
| `GET /v1/memory_stores/:id/memories/:memory_id` | Read a memory |
| `PATCH /v1/memory_stores/:id/memories/:memory_id` | Edit a memory |
| `DELETE /v1/memory_stores/:id/memories/:memory_id` | Delete a memory |

Limits: 8 stores per session, 100 KB per memory. Memory tools available inside a session: `memory_list`, `memory_search`, `memory_read`, `memory_write`, `memory_edit`, `memory_delete`.

- *Source*: [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

---

### Events System

Communication is event-based. Events use a `{domain}.{action}` naming convention.

**User events** (what you send):

| Type | Description |
|---|---|
| `user.message` | Text message to the agent |
| `user.interrupt` | Stop agent mid-execution |
| `user.custom_tool_result` | Response to a custom tool call |
| `user.tool_confirmation` | Approve/deny a tool call (when `always_ask` policy is set) |
| `user.define_outcome` | Define an outcome rubric (research preview) |

**Agent events** (what you receive):

| Type | Description |
|---|---|
| `agent.message` | Agent text response |
| `agent.thinking` | Extended thinking content |
| `agent.tool_use` / `agent.tool_result` | Pre-built tool execution |
| `agent.mcp_tool_use` / `agent.mcp_tool_result` | MCP tool execution |
| `agent.custom_tool_use` | Agent requesting your custom tool; respond with `user.custom_tool_result` |
| `agent.thread_context_compacted` | Conversation history was compacted |

**Session events**: `session.status_running`, `session.status_idle` (with `stop_reason`), `session.error` (with `retry_status`), `session.status_terminated`

**Span events** for token usage: `span.model_request_end` includes `model_usage` with `input_tokens` and `output_tokens`.

> "Only events emitted after the stream is opened are delivered, so open the stream before sending events to avoid a race condition."

- *Source*: [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming.md)

---

### Tools

#### Pre-built Agent Toolset (`agent_toolset_20260401`)

The default toolset includes 8 built-in tools, all enabled by default:

| Tool | Name | Description |
|---|---|---|
| Bash | `bash` | Execute shell commands |
| Read | `read` | Read files |
| Write | `write` | Write files |
| Edit | `edit` | String replacement in files |
| Glob | `glob` | File pattern matching |
| Grep | `grep` | Regex text search |
| Web fetch | `web_fetch` | Fetch URL content |
| Web search | `web_search` | Search the web |

Tools can be selectively disabled via `configs: [{name: "web_fetch", enabled: false}]` or a whitelist approach using `default_config: {enabled: false}` plus explicit per-tool enables.

- *Source*: [Tools](https://platform.claude.com/docs/en/managed-agents/tools.md)

#### Permission Policies

Two policies govern whether server-side tools execute automatically or require approval:

| Policy | Default for | Behavior |
|---|---|---|
| `always_allow` | Agent toolset | Executes automatically |
| `always_ask` | MCP toolset | Session emits `session.status_idle`; wait for `user.tool_confirmation` |

Policies can be overridden globally (`default_config.permission_policy`) or per-tool (via the `configs` array). MCP tools default to `always_ask` intentionally — new tools added to an MCP server won't auto-execute without explicit opt-in.

- *Source*: [Permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies.md)

#### Custom Tools

Custom tools follow the same JSON Schema definition as Messages API tools. When the agent calls a custom tool, it emits `agent.custom_tool_use`; the application executes the tool and responds with `user.custom_tool_result`.

- *Source*: [Tools — Custom tools](https://platform.claude.com/docs/en/managed-agents/tools.md)

#### MCP Connector

MCP servers are declared on the agent definition (name + URL, no auth) and authenticated at session creation via vault IDs. Only remote MCP servers with HTTP streamable transport are supported.

- *Source*: [MCP connector](https://platform.claude.com/docs/en/managed-agents/mcp-connector.md)

---

### Session Resources

Three resource types can be mounted at session creation (or added to a running session):

| Type | Description |
|---|---|
| `file` | Upload via Files API, mount at a path in the container. Max 100 files per session. |
| `github_repository` | Clone a GitHub repo into the container. Repos are cached for faster future sessions. |
| `memory_store` | Attach a memory store (research preview). `access` can be `read_write` (default) or `read_only`. |

- *Sources*: [Adding files](https://platform.claude.com/docs/en/managed-agents/files.md), [Accessing GitHub](https://platform.claude.com/docs/en/managed-agents/github.md), [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

---

### Multi-Agent Orchestration *(Research Preview)*

An agent can declare `callable_agents` — a list of other agent IDs it may invoke. All agents share the container filesystem but each runs in an isolated **thread** with its own context window and conversation history.

> "Only one level of delegation is supported: the coordinator can call other agents, but those agents cannot call agents of their own."

Thread-level events stream at `/v1/sessions/:id/threads/:thread_id/stream`. The primary session stream (`/v1/sessions/:id/stream`) shows a condensed view of all thread activity.

- *Source*: [Multiagent sessions](https://platform.claude.com/docs/en/managed-agents/multi-agent.md)

---

### Outcomes *(Research Preview)*

Outcomes shift a session from conversational to goal-directed. The agent works autonomously, self-evaluating against a rubric and iterating until the outcome is satisfied.

Requires additional beta header: `managed-agents-2026-04-01-research-preview`.

Send a `user.define_outcome` event with:
- `description`: What to produce
- `rubric`: Inline text or a Files API file ID — scored criteria the agent must meet
- `max_iterations`: Optional (default 3, max 20)

The harness provisions a separate grader in its own context window. Evaluation outcomes:

| Result | Description |
|---|---|
| `satisfied` | Session goes idle |
| `needs_revision` | Agent iterates |
| `max_iterations_reached` | Agent may run one final pass, then idles |
| `failed` | Rubric fundamentally mismatched the task |
| `interrupted` | `user.interrupt` was sent during evaluation |

- *Source*: [Define outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes.md)

---

### Skills

Skills are reusable, filesystem-based resources that supply domain-specific expertise to an agent. They load on demand and only consume context when invoked.

Two types:
- **`anthropic`** pre-built skills: `xlsx`, `pptx`, `docx`, `pdf` document handling
- **`custom`** skills: Organization-authored, versioned (pin with `version: "latest"` or a specific version string)

Maximum 20 skills per session across all agents in a multi-agent session.

- *Source*: [Skills](https://platform.claude.com/docs/en/managed-agents/skills.md)

---

### SDK Support

All 7 SDK languages have full Managed Agents support under `client.beta.*`:

| SDK | Namespace pattern |
|---|---|
| Python | `client.beta.agents`, `client.beta.sessions`, `client.beta.environments`, etc. |
| TypeScript | `client.beta.agents`, `client.beta.sessions`, etc. |
| Go | `client.Beta.Agents`, `client.Beta.Sessions`, etc. |
| Java | `client.beta().agents()`, `client.beta().sessions()`, etc. |
| C# | `client.Beta.Agents`, `client.Beta.Sessions`, etc. |
| Ruby | `client.beta.agents`, `client.beta.sessions`, etc. |
| PHP | `$client->beta->agents`, `$client->beta->sessions`, etc. |

The SDK sets the `managed-agents-2026-04-01` beta header automatically on all beta namespace calls.

---

### CLI (`ant`)

A new first-party CLI named `ant` is introduced for managing Managed Agents resources.

Install:
- Homebrew (macOS): `brew install anthropics/tap/ant`
- curl (Linux/WSL): Download from GitHub releases
- Go: `go install github.com/anthropics/anthropic-cli/cmd/ant@latest`

Key commands mirror the API: `ant beta:agents create`, `ant beta:sessions create`, `ant beta:sessions stream`, `ant beta:vaults create`, `ant beta:memory-stores create`, etc.

- *Source*: [Quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart.md)

---

### Cloud Container Specifications

Pre-installed runtimes:

| Language | Version |
|---|---|
| Python | 3.12+ |
| Node.js | 20+ |
| Go | 1.22+ |
| Rust | 1.77+ |
| Java | 21+ |
| Ruby | 3.3+ |
| PHP | 8.3+ |
| C/C++ | GCC 13+ |

Container specs: Ubuntu 22.04 LTS, x86_64, up to 8 GB RAM, up to 10 GB disk. SQLite is available; PostgreSQL and Redis run as clients only (no servers).

- *Source*: [Container reference](https://platform.claude.com/docs/en/managed-agents/cloud-containers.md)

---

### Rate Limits

| Operation | Limit |
|---|---|
| Create endpoints (agents, sessions, environments, etc.) | 60 requests per minute |
| Read endpoints (retrieve, list, stream, etc.) | 600 requests per minute |

Organization-level spend limits and tier-based limits also apply.

- *Source*: [Overview](https://platform.claude.com/docs/en/managed-agents/overview.md)

---

## New Pages

- **overview.md** — Product overview: what Managed Agents is, core concepts, when to use it, rate limits, and branding guidelines. [View](https://platform.claude.com/docs/en/managed-agents/overview.md)
- **quickstart.md** — Step-by-step guide to create an agent, environment, and first session with code examples in 8 languages + CLI. [View](https://platform.claude.com/docs/en/managed-agents/quickstart.md)
- **onboarding.md** — How to prototype and test agents visually in the Claude Console before writing code. [View](https://platform.claude.com/docs/en/managed-agents/onboarding.md)
- **agent-setup.md** — Full agent configuration reference: fields, CRUD operations, versioning, archiving. [View](https://platform.claude.com/docs/en/managed-agents/agent-setup.md)
- **sessions.md** — Session lifecycle, version pinning, vault attachment, status model, list/retrieve operations. [View](https://platform.claude.com/docs/en/managed-agents/sessions.md)
- **environments.md** — Container configuration: packages, networking modes, environment CRUD. [View](https://platform.claude.com/docs/en/managed-agents/environments.md)
- **tools.md** — Built-in toolset reference, selective enable/disable, custom tool definitions and best practices. [View](https://platform.claude.com/docs/en/managed-agents/tools.md)
- **events-and-streaming.md** — Full event taxonomy, SSE streaming, interrupt handling, custom tool result flow. [View](https://platform.claude.com/docs/en/managed-agents/events-and-streaming.md)
- **mcp-connector.md** — How to declare MCP servers on an agent and supply credentials via vaults at session creation. [View](https://platform.claude.com/docs/en/managed-agents/mcp-connector.md)
- **vaults.md** — Vault and credential management: mcp_oauth (with auto-refresh) and static_bearer credential types. [View](https://platform.claude.com/docs/en/managed-agents/vaults.md)
- **files.md** — Uploading files via the Files API and mounting them in session containers; dynamic add/remove on running sessions. [View](https://platform.claude.com/docs/en/managed-agents/files.md)
- **github.md** — Mounting GitHub repositories as session resources; token permissions and multi-repo patterns. [View](https://platform.claude.com/docs/en/managed-agents/github.md)
- **permission-policies.md** — `always_allow` vs. `always_ask` policies; how to override defaults per-toolset or per-tool. [View](https://platform.claude.com/docs/en/managed-agents/permission-policies.md)
- **skills.md** — Attaching Anthropic pre-built or custom organization skills to agents. [View](https://platform.claude.com/docs/en/managed-agents/skills.md)
- **observability.md** — Debugging with Console timeline, raw event retrieval, error and token usage tracking. [View](https://platform.claude.com/docs/en/managed-agents/observability.md)
- **multi-agent.md** — Multi-agent orchestration using `callable_agents`, session threads, and per-thread streaming. *(Research Preview)* [View](https://platform.claude.com/docs/en/managed-agents/multi-agent.md)
- **memory.md** — Persistent memory stores across sessions: create/attach/read/write/version memories. *(Research Preview)* [View](https://platform.claude.com/docs/en/managed-agents/memory.md)
- **define-outcomes.md** — Outcome-driven sessions with rubric-based grading and iterative self-evaluation. *(Research Preview)* [View](https://platform.claude.com/docs/en/managed-agents/define-outcomes.md)
- **cloud-containers.md** — Container reference: pre-installed runtimes, databases, utilities, and container specs. [View](https://platform.claude.com/docs/en/managed-agents/cloud-containers.md)
- **migration.md** — Migration guide from a Messages API agent loop or Claude Agent SDK to Managed Agents. [View](https://platform.claude.com/docs/en/managed-agents/migration.md)

---

## Notable Details

- **Beta header versioning**: The header `managed-agents-2026-04-01` encodes an API date. This follows Anthropic's pattern for beta features and signals the feature set may evolve. Research preview features (`outcomes`, `multiagent`, `memory`) require a second header: `managed-agents-2026-04-01-research-preview`.
- **Model support**: The docs specify "All Claude 4.5 and later models are supported." The quickstart uses `claude-sonnet-4-6`. `claude-opus-4-6` with fast mode is mentioned via `{"id": "claude-opus-4-6", "speed": "fast"}`.
- **Agent toolset type string**: The toolset identifier `agent_toolset_20260401` is also date-stamped, suggesting Anthropic plans to version the toolset independently.
- **MCP toolset defaults to `always_ask`**: Unlike the agent toolset (which auto-runs), MCP tools require explicit confirmation by default. This is a deliberate security posture: new tools added to an MCP server won't auto-execute without the developer updating the permission policy.
- **Vault scoping warning**: Vaults are workspace-scoped — any API key holder can use a vault to authorize an agent session. The docs warn to delete the vault or credential to revoke access, not just remove it from agent configuration.
- **No-op update detection**: Agent updates that produce no change (identical field values) do not generate a new version and return the current version unchanged. This is useful for idempotent deployment pipelines.
- **GitHub repo caching**: GitHub repositories mounted as session resources are cached, so subsequent sessions using the same repo start faster.
- **MCP auth failure behavior**: If vault credentials for an MCP server are invalid, the session still creates successfully. A `session.error` event is emitted at runtime, and the session can continue without the MCP. Retries happen on the next `idle` → `running` transition.
- **Branding restriction**: The docs explicitly prohibit using the name "Claude Code" or "Claude Cowork" for partner integrations that embed Managed Agents.
- **Outcome grader isolation**: The grader that evaluates artifacts runs in a separate context window from the agent, explicitly to prevent the agent's reasoning from influencing the evaluation.

---

## Changes by Page

| Page | Type | Summary |
|------|------|---------|
| managed-agents/overview.md | New | Product overview, concepts, rate limits, branding guidelines |
| managed-agents/quickstart.md | New | End-to-end guide, all 8 SDKs + CLI |
| managed-agents/onboarding.md | New | Console prototype-to-code workflow |
| managed-agents/agent-setup.md | New | Agent CRUD, versioning, archiving |
| managed-agents/sessions.md | New | Session lifecycle, vault auth, status states |
| managed-agents/environments.md | New | Container config, packages, networking |
| managed-agents/tools.md | New | Built-in toolset, custom tools, best practices |
| managed-agents/events-and-streaming.md | New | Event taxonomy, SSE streaming, interrupt/confirm |
| managed-agents/mcp-connector.md | New | MCP server declaration and vault-based auth |
| managed-agents/vaults.md | New | Credential store: OAuth + bearer tokens |
| managed-agents/files.md | New | Files API integration, session resource management |
| managed-agents/github.md | New | GitHub repo mounting, token permissions |
| managed-agents/permission-policies.md | New | `always_allow` vs `always_ask`, per-tool overrides |
| managed-agents/skills.md | New | Anthropic + custom skills, 20-per-session limit |
| managed-agents/observability.md | New | Console tracing, raw events, token tracking |
| managed-agents/multi-agent.md | New | `callable_agents`, session threads (research preview) |
| managed-agents/memory.md | New | Persistent memory stores across sessions (research preview) |
| managed-agents/define-outcomes.md | New | Rubric-based outcome evaluation, grader loop (research preview) |
| managed-agents/cloud-containers.md | New | Container specs, pre-installed runtimes and tools |
| managed-agents/migration.md | New | Migration from Messages API loop and Agent SDK |

---

*Generated from Claude API documentation changes detected on 2026-04-09*
