# Claude Code Documentation Changes — 2026-03-12

## Summary

13 pages were modified across sub-agents, settings, hooks, MCP, memory, and plugin marketplace documentation. The most significant additions are MCP server scoping for subagents, a configurable `autoMemoryDirectory` setting, a new `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` environment variable, and a behavior change to MCP tool search (now enabled by default). The "Safe autonomous mode" section covering `--dangerously-skip-permissions` was removed from best-practices documentation.

## Significant Changes

### Sub-Agents

- **MCP servers can now be scoped to individual subagents**: The `mcpServers` field in subagent frontmatter now supports two entry modes — inline server definitions (connected when the subagent starts, disconnected when it finishes) and string references that reuse an already-configured server from the parent session.
  > "Use the `mcpServers` field to give a subagent access to MCP servers that aren't available in the main conversation. Inline servers defined here are connected when the subagent starts and disconnected when it finishes."
  > "To keep an MCP server out of the main conversation entirely and avoid its tool descriptions consuming context there, define it inline here rather than in `.mcp.json`. The subagent gets the tools; the parent conversation does not."
  - *Implication*: Developers can attach MCP servers (e.g., Playwright) exclusively to a subagent without polluting the parent conversation's context window. Inline definitions follow the same schema as `.mcp.json` entries (`stdio`, `http`, `sse`, `ws`), keyed by server name.
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

- **Full model IDs accepted in the `model` field**: In addition to aliases (`sonnet`, `opus`, `haiku`), the `model` field in subagent frontmatter (and the `--agents` CLI flag) now accepts full model IDs such as `claude-opus-4-6`.
  > "Model to use: `sonnet`, `opus`, `haiku`, a full model ID (for example, `claude-opus-4-6`), or `inherit`. Defaults to `inherit`"
  > "Full model ID: Use a full model ID such as `claude-opus-4-6` or `claude-sonnet-4-6`. Accepts the same values as the `--model` flag"
  - *Implication*: Subagents can now be pinned to specific versioned model releases rather than floating aliases. This change is consistent with the changelog entry for 2.1.74 that fixed full model IDs being silently ignored in agent config.
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md), [CLI reference](https://code.claude.com/docs/en/cli-reference.md)

### Memory

- **New `autoMemoryDirectory` setting**: Auto memory can now be redirected to a custom directory via the `autoMemoryDirectory` key in user, local, or policy settings.
  > "To store auto memory in a different location, set `autoMemoryDirectory` in your user or local settings."
  > "This setting is accepted from policy, local, and user settings. It is not accepted from project settings (`.claude/settings.json`) to prevent a shared project from redirecting auto memory writes to sensitive locations."
  - *Implication*: Useful for teams that want to consolidate memory files or store them on a shared volume. The security restriction — blocked in project-level settings — prevents supply-chain abuse via committed `.claude/settings.json` files.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md), [Settings](https://code.claude.com/docs/en/settings.md)

### Hooks

- **SessionEnd hooks have a documented timeout with a configurable override**: SessionEnd hooks default to a 1.5-second budget covering both session exit and `/clear`. A new environment variable `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` allows increasing this limit. Per-hook `timeout` values are still capped by this budget.
  > "SessionEnd hooks have a default timeout of 1.5 seconds. This applies to both session exit and `/clear`. If your hooks need more time, set the `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` environment variable to a higher value in milliseconds. Any per-hook `timeout` setting is also capped by this value."
  ```bash
  CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000 claude
  ```
  - *Implication*: Hooks that perform cleanup tasks (e.g., syncing files, logging) and were silently truncated at exit now have a documented path to request more time. Both this env var and per-hook `timeout` must be set appropriately.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md), [Settings](https://code.claude.com/docs/en/settings.md)

### MCP Tool Search

- **Tool search is now enabled by default**: Previously, tool search activated only when MCP tools exceeded 10% of context (`auto` mode). It is now enabled by default for all sessions, with automatic disablement when `ANTHROPIC_BASE_URL` points to a non-first-party host (since most proxies do not forward `tool_reference` blocks).
  > "Tool search is enabled by default: MCP tools are deferred and discovered on demand. When `ANTHROPIC_BASE_URL` points to a non-first-party host, tool search is disabled by default because most proxies do not forward `tool_reference` blocks. Set `ENABLE_TOOL_SEARCH` explicitly if your proxy does."

  Updated `ENABLE_TOOL_SEARCH` behavior table:

  | Value | Behavior |
  |-------|----------|
  | (unset) | Enabled by default; disabled when `ANTHROPIC_BASE_URL` is a non-first-party host |
  | `true` | Always enabled, including for non-first-party `ANTHROPIC_BASE_URL` |
  | `auto` | Activates when MCP tools exceed 10% of context |
  | `auto:<N>` | Activates at a custom threshold (e.g., `auto:5` for 5%) |
  | `false` | Disabled; all MCP tools loaded upfront |

  - *Implication*: Users on direct Anthropic API connections get deferred MCP tool loading automatically. Users behind proxies (e.g., AWS Bedrock, corporate API gateways) will have tool search disabled by default and must set `ENABLE_TOOL_SEARCH=true` only if their proxy properly forwards `tool_reference` blocks.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md), [Settings](https://code.claude.com/docs/en/settings.md)

### Configuration

- **`CLAUDE_CODE_ENABLE_TASKS` semantics changed**: The environment variable no longer toggles between the task tracking system and the old TODO list. It now enables task tracking specifically in non-interactive (`-p`) mode. Tasks remain on by default in interactive mode.
  > "Set to `true` to enable the task tracking system in non-interactive mode (the `-p` flag). Tasks are on by default in interactive mode."
  - *Implication*: The previous "revert to previous TODO list via `CLAUDE_CODE_ENABLE_TASKS=false`" path is gone. Automation scripts using `-p` that want task tracking must now explicitly set this to `true`. The corresponding note in the interactive-mode docs was also removed.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md), [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

- **`strictKnownMarketplaces` + `extraKnownMarketplaces` combined usage documented**: A new "Using both together" subsection clarifies that `strictKnownMarketplaces` is a policy gate (controls what users may add) but does not itself register any marketplaces. To both restrict and pre-register a marketplace, both keys must be set in `managed-settings.json`.
  > "`strictKnownMarketplaces` is a policy gate: it controls what users may add but does not register any marketplaces. To both restrict and pre-register a marketplace for all users, set both in `managed-settings.json`."
  - *Implication*: Administrators who set only `strictKnownMarketplaces` expecting marketplaces to be available automatically need to also add `extraKnownMarketplaces`. The same clarification is echoed as a Note in the plugin-marketplaces page.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md), [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

### Plugin Marketplaces

- **Relative path resolution clarified**: Relative plugin source paths resolve from the marketplace root (the directory containing `.claude-plugin/`), not from the location of `marketplace.json` inside `.claude-plugin/`. Using `../` to escape this directory is explicitly prohibited.
  > "Paths resolve relative to the marketplace root, which is the directory containing `.claude-plugin/`. In the example above, `./plugins/my-plugin` points to `<repo>/plugins/my-plugin`, even though `marketplace.json` lives at `<repo>/.claude-plugin/marketplace.json`. Do not use `../` to climb out of `.claude-plugin/`."
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

- **Git URL source no longer requires `.git` suffix**: The `url` field in the `url` source type now accepts URLs without the `.git` suffix, enabling compatibility with Azure DevOps and AWS CodeCommit repository URLs.
  > "Required. Full git repository URL (`https://` or `git@`). The `.git` suffix is optional, so Azure DevOps and AWS CodeCommit URLs without the suffix work"
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

- **Validation error message updated**: The `claude plugin validate` error for path traversal changed from `plugins[0].source: Path traversal not allowed` to `plugins[0].source: Path contains ".."`, with the solution text pointing to the Relative paths documentation section.
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

### Plugins

- **`--plugin-dir` local plugins take precedence over same-named marketplace plugins**: During a session started with `--plugin-dir`, the local development copy of a plugin now overrides any installed marketplace plugin of the same name. The only exception is marketplace plugins force-enabled by managed settings.
  > "When a `--plugin-dir` plugin has the same name as an installed marketplace plugin, the local copy takes precedence for that session. This lets you test changes to a plugin you already have installed without uninstalling it first. Marketplace plugins force-enabled by managed settings are the only exception and cannot be overridden."
  - *Implication*: Plugin developers can iterate without uninstall/reinstall cycles. Enterprise force-enabled plugins are exempt, preserving policy enforcement.
  - *Source*: [Plugins](https://code.claude.com/docs/en/plugins.md)

### Interactive Mode

- **`/context` command now surfaces optimization suggestions**: The command description was updated to reflect that it also displays optimization suggestions for context-heavy tools, memory bloat, and capacity warnings.
  > "Visualize current context usage as a colored grid. Shows optimization suggestions for context-heavy tools, memory bloat, and capacity warnings"
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

- **`messageSelector` gains Ctrl+P / Ctrl+N keybindings**: The message selector now supports Emacs-style navigation shortcuts in addition to arrow keys and Vi-style keys.
  - `messageSelector:up`: `Up`, `K`, **`Ctrl+P`** (new)
  - `messageSelector:down`: `Down`, `J`, **`Ctrl+N`** (new)
  - *Source*: [Keybindings](https://code.claude.com/docs/en/keybindings.md)

### Code Review Billing

- **Code Review billed separately from plan usage**: The pricing section now explicitly states that Code Review is billed via "extra usage" and does not count against a plan's included usage.
  > "Code Review usage is billed separately through extra usage and does not count against your plan's included usage."
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

## Removed Content

- **"Safe autonomous mode" section removed from best-practices**: The 10-line section documenting `--dangerously-skip-permissions` and its risks (including a warning about prompt injection and sandboxing guidance) was removed from best-practices documentation. The CLI flag itself remains functional but is no longer surfaced in this context.
  - *Source*: [Best Practices](https://code.claude.com/docs/en/best-practices.md)

## Notable Details

- The `autoMemoryDirectory` setting is explicitly blocked in project settings (`.claude/settings.json`) but accepted in policy, local, and user settings. This asymmetry is intentional and security-motivated — it prevents a malicious repository from redirecting auto-memory writes to sensitive paths.
- The MCP tool search default change from `auto` to always-on is a potentially breaking change for users behind API proxies. The proxy detection is based on `ANTHROPIC_BASE_URL` pointing to a non-first-party host — any custom base URL triggers the fallback-to-disabled behavior.
- `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` acts as a global budget: per-hook `timeout` values are capped by it. Setting only per-hook timeouts without this env var still results in the 1.5s kill.
- The GitHub repository stat changes in `changelog.md` (stars 77k → 77.1k, PRs 337 → 338) reflect live metadata rendered into the page and carry no documentation significance.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| sub-agents.md | Modified | +29/-1 | New `mcpServers` scoping section; full model IDs now accepted in `model` field |
| settings.md | Modified | +23/-2 | `autoMemoryDirectory` setting added; `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` env var documented; `CLAUDE_CODE_ENABLE_TASKS` and `ENABLE_TOOL_SEARCH` descriptions updated; `strictKnownMarketplaces` + `extraKnownMarketplaces` combined usage guidance added |
| plugin-marketplaces.md | Modified | +18/-12 | Relative path resolution clarified; git URL `.git` suffix now optional; validation error message updated; `strictKnownMarketplaces` note added |
| memory.md | Modified | +10/-0 | `autoMemoryDirectory` setting documented with security rationale |
| hooks.md | Modified | +6/-0 | `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` documented; 1.5s default timeout and per-hook cap explained |
| best-practices.md | Modified | +0/-10 | "Safe autonomous mode" (`--dangerously-skip-permissions`) section removed |
| mcp.md | Modified | +4/-3 | Tool search now on by default; proxy detection disables it; `ENABLE_TOOL_SEARCH` value table updated |
| interactive-mode.md | Modified | +1/-2 | `/context` shows optimization suggestions; `CLAUDE_CODE_ENABLE_TASKS=false` revert note removed |
| plugins.md | Modified | +2/-0 | `--plugin-dir` local plugins override same-named marketplace plugins |
| keybindings.md | Modified | +2/-2 | `Ctrl+P`/`Ctrl+N` added to `messageSelector` navigation |
| cli-reference.md | Modified | +1/-1 | `model` field updated to document full model ID support |
| code-review.md | Modified | +1/-1 | Code Review billing clarified as separate extra usage |
| changelog.md | Modified | +2/-2 | Repository star count (77k → 77.1k) and open PR count (337 → 338) updated |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-12*
