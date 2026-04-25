# Claude API Documentation Changes — 2026-04-25

## Summary

The Managed Agents memory feature has graduated out of Research Preview and received a significant architectural overhaul: memory stores are now mounted as filesystem directories inside agent containers rather than being accessible through dedicated `memory_*` tools. Alongside this, the `overview.md` page confirms a 5× rate limit increase for Create endpoints (60 → 300 req/min), and the quickstart CLI and Java SDK versions were bumped.

---

## Significant Changes

### Managed Agents — Memory

#### Memory exits Research Preview

Memory stores no longer require a separate research-preview beta header and are no longer gated behind an access request. The old `<Tip>` block calling memory "a Research Preview feature" has been removed. The overview page confirms it:

> Certain features ([outcomes](/docs/en/managed-agents/define-outcomes) and [multiagent](/docs/en/managed-agents/multi-agent)) are in research preview.

Memory is now a generally-available beta feature alongside the rest of the Managed Agents API — only the `managed-agents-2026-04-01` beta header is required.

- *Implication*: All API accounts can use memory stores without a separate access request.
- *Source*: [Managed Agents Overview](https://platform.claude.com/docs/en/managed-agents/overview.md)

---

#### Memory stores are now filesystem mounts, not dedicated tools

The previous model exposed six dedicated memory tools (`memory_list`, `memory_search`, `memory_read`, `memory_write`, `memory_edit`, `memory_delete`). That model has been replaced. Memory stores are now mounted inside the session container as a directory under `/mnt/memory/`, and the agent reads and writes them with the same standard file tools it uses everywhere else.

> Each attached store is mounted inside the session's container as a directory under `/mnt/memory/`, and the agent reads and writes it with the standard [agent toolset](/docs/en/managed-agents/tools). Writes are persisted back to the store and stay in sync across sessions that share it. A short description of each mount (path, access mode, store `description`, and any `instructions`) is automatically added to the system prompt.

The removed "Memory tools" table listed: `memory_list`, `memory_search`, `memory_read`, `memory_write`, `memory_edit`, `memory_delete`.

- *Implication*: Agents no longer need dedicated tool calls for memory access. The agent toolset (`agent_toolset_20260401`) is now **required** for memory store interactions — it must be enabled at agent creation time. The event stream will show standard `agent.tool_use` / `agent.tool_result` events for file operations on `/mnt/memory/` paths, not memory-specific events.
- *Source*: [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

---

#### `prompt` field renamed to `instructions` on session memory store resource

When attaching a memory store to a session via `resources[]`, the field for providing session-specific guidance was `prompt`. It is now `instructions`.

Before:
```json
{
  "type": "memory_store",
  "memory_store_id": "$store_id",
  "access": "read_write",
  "prompt": "User preferences and project context. Check before starting any task."
}
```

After:
```json
{
  "type": "memory_store",
  "memory_store_id": "$store_id",
  "access": "read_write",
  "instructions": "User preferences and project context. Check before starting any task."
}
```

This rename applies to all SDK languages (Python, TypeScript, Go, Java, C#, Ruby, PHP). The corresponding SDK property names (`Prompt` → `Instructions`, `prompt` → `instructions`) have been updated accordingly in all code examples.

- *Implication*: **Breaking change for code in beta.** Any session creation payloads using `"prompt"` on a memory store resource must be updated to `"instructions"`.
- *Source*: [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

---

#### Memory stores can only be attached at session creation time

A new constraint is now explicitly documented:

> Unlike file and repository resources, memory stores can only be attached at session creation time; adding or removing one from a running session is not supported.

- *Implication*: Developers must plan all required memory stores before starting a session. Attempting to attach one mid-session is unsupported.
- *Source*: [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

---

#### `memories.write` (upsert) replaced by `memories.create` (create-only)

The previous `memories.write` endpoint created a memory or overwrote an existing one at the same path. That operation has been removed. `memories.create` is now documented as create-only and will not overwrite existing content:

> `memories.create` creates a memory at a given `path`. Create does not overwrite; to change an existing memory, use [`memories.update`](#update-a-memory).

The previous "Safe writes (optimistic concurrency)" subsection — which described `precondition: {"type": "not_exists"}` on `memories.write` — has also been removed.

- *Implication*: **Breaking change for code in beta.** Code calling `memories.write` (Python), `memoryStores.memories.write` (TypeScript), or equivalent must switch to `memories.create` for initial writes and `memories.update` for modifications. The upsert pattern is no longer available as a single operation.
- *Source*: [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

---

#### `memories.update` HTTP method changed: `PATCH` → `POST`

The curl examples for `memories.update` and the safe-edit with `content_sha256` precondition previously used `PATCH`. They now use `POST`:

Before: `curl -X PATCH "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id"`

After: `curl -s -X POST "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id"`

- *Implication*: **Breaking change for raw HTTP callers.** SDK users are likely insulated from this change, but anyone constructing HTTP requests directly must update the method.
- *Source*: [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

---

#### New `memories.list` parameters: `order_by` and `depth`

The `memories.list` endpoint now supports two additional parameters shown in all SDK examples:

- `order_by` — sort results (example shows `"path"`)
- `depth` — limit directory traversal depth (example uses `2`)

The response items now expose a `type` field alongside `path` (previously only path, size, and SHA were shown).

```python
page = client.beta.memory_stores.memories.list(
    store.id,
    path_prefix="/",
    order_by="path",
    depth=2,
)
for item in page.data:
    print(item.type, item.path)
```

- *Implication*: Enables directory-style browsing of memory store contents. The `type` field allows distinguishing files from directory entries.
- *Source*: [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

---

#### New section: Manage memory stores (list, archive, delete stores)

A new top-level `## Manage memory stores` section documents store-level lifecycle operations that were previously undocumented. Two sub-sections are new:

**List stores** — `GET /v1/memory_stores` with an `include_archived` flag:

> List stores in the workspace. Archived stores are excluded by default; pass `include_archived: true` to include them.

```python
for s in client.beta.memory_stores.list(include_archived=True):
    print(s.id, s.name, s.archived_at)
```

**Archive a store** — `POST /v1/memory_stores/{id}/archive`:

> Archiving makes a store read-only and prevents it from being attached to new sessions. Archiving is one-way; there is no unarchive.

```python
client.beta.memory_stores.archive(store.id)
```

To permanently remove a store and all its memories and versions, use `memory_stores.delete`.

- *Implication*: Developers can now manage store lifecycle (list, archive, delete) via the API. Archive is irreversible — use it for stores that should be frozen but retained for auditing.
- *Source*: [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

---

#### New section: Limits

A `## Limits` table is now documented:

| Limit | Value |
| --- | --- |
| Memory stores per organization | 1,000 |
| Memories per store | 2,000 |
| Total storage per store | 100 MB |
| Versions per store | 250,000 |
| Size per memory | 100 kB |
| Version history retention | 30 days |
| Memory stores per session | 8 |
| `instructions` field per attachment | 4,096 characters |

- *Implication*: Previously undocumented limits are now visible. Contact support for higher limits.
- *Source*: [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

---

#### Memory version retention policy clarified

> Versions belong to the store (not the individual memory) and survive even after the memory itself is deleted, so the audit trail stays complete. Versions are retained for 30 days; however, the recent versions are always kept regardless of age, so memories that change infrequently may retain history beyond 30 days.

The previous wording stated versions "accumulate for the lifetime of the parent memory" — it was ambiguous whether versions outlived their parent memory. They do. A new clarification also notes there is no dedicated restore endpoint; roll back by reading a version and re-writing its content with `memories.update` or `memories.create`.

- *Implication*: Audit trails are complete even for deleted memories. Developers building rollback workflows must implement a read-then-write pattern rather than a dedicated restore call.
- *Source*: [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

---

#### New prompt injection security warning

A new `<Warning>` block was added to the "Attach a memory store" section:

> Memory stores attach with `read_write` access by default. If the agent processes untrusted input (user-supplied prompts, fetched web content, or third-party tool output), a successful prompt injection could write malicious content into the store. Later sessions then read that content as trusted memory. Use `read_only` for reference material, shared lookups, and any store the agent does not need to modify.

- *Implication*: This is an important security consideration for any agent that processes third-party or user-supplied content. Reference stores should default to `read_only`.
- *Source*: [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

---

#### Redact: current head version cannot be redacted

A constraint on the `memory_versions.redact` operation is now documented:

> A version that is the current head of a live memory cannot be redacted. Write a new version first (or delete the memory), then redact the old one.

- *Implication*: To scrub the current content of a live memory, you must first overwrite it (creating a new head version), then redact the old version.
- *Source*: [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

---

### Managed Agents — Rate Limits

#### Create endpoint rate limit increased 5×: 60 → 300 req/min

> | Create endpoints (agents, sessions, environments, etc.) | 300 requests per minute |

Previously 60 requests per minute.

- *Implication*: High-throughput applications creating many sessions or agents per minute can now do so without rate-limit throttling that previously kicked in after ~1 req/sec.
- *Source*: [Managed Agents Overview](https://platform.claude.com/docs/en/managed-agents/overview.md)

---

### CLI and SDK Version Bumps

- **Anthropic CLI (`ant`)**: Linux/WSL install example updated from version `1.0.0` to `1.3.2`.
- **Java SDK**: Gradle dependency updated from `anthropic-java:2.20.0` to `anthropic-java:2.27.0`.
- **macOS CLI install**: The `xattr -d com.apple.quarantine` post-install step for macOS has been removed from the quickstart.
- *Source*: [Quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart.md)

---

## Migration Guidance

### `prompt` → `instructions` on memory store resource attachment

```python
# Before
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    resources=[{
        "type": "memory_store",
        "memory_store_id": store.id,
        "prompt": "Check this store before every task.",
    }],
)

# After
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    resources=[{
        "type": "memory_store",
        "memory_store_id": store.id,
        "instructions": "Check this store before every task.",
    }],
)
```

### `memories.write` → `memories.create` + `memories.update`

```python
# Before — write was an upsert (create or overwrite)
client.beta.memory_stores.memories.write(
    memory_store_id=store.id,
    path="/prefs/formatting.md",
    content="Always use tabs.",
)

# After — create for new paths, update for existing ones
client.beta.memory_stores.memories.create(
    store.id,
    path="/prefs/formatting.md",
    content="Always use tabs.",
)

# To update existing content by ID
client.beta.memory_stores.memories.update(
    mem.id,
    memory_store_id=store.id,
    content="Updated: use 2-space indent.",
)
```

### HTTP method for `memories.update` changed from `PATCH` to `POST`

```bash
# Before
curl -X PATCH "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id" ...

# After
curl -X POST "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id" ...
```

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| managed-agents/memory.md | Modified | +1339/-1011 | Major overhaul: filesystem-mount model replaces dedicated memory tools; `prompt`→`instructions`; `write` removed; new list/archive/limits sections |
| managed-agents/overview.md | Modified | +2/-2 | Memory removed from research preview; Create rate limit raised from 60 to 300 req/min |
| managed-agents/quickstart.md | Modified | +2/-8 | CLI version 1.0.0→1.3.2, Java SDK 2.20.0→2.27.0, removed macOS unquarantine step |

---
*Generated from Claude API documentation changes detected on 2026-04-25*
