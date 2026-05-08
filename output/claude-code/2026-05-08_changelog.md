# Claude Code Documentation Changes — 2026-05-08

## Summary

Ten documentation pages were modified with 141 additions and 1,267 deletions. The bulk of the deletions are cosmetic: large inline React/JSX `InstallConfigurator` components were removed from `overview.md` and `quickstart.md`, leaving readable documentation content intact. The substantive changes add new controlled settings, new environment variables, expand Bedrock/Vertex streaming support, and clarify skills behavior in subagents.

## Significant Changes

### Configuration

- **New `parentSettingsBehavior` setting**: Controls how managed settings from embedding hosts (Agent SDK, IDE extensions) interact with admin-deployed managed tiers. Requires Claude Code v2.1.133+.
  > `"first-wins"`: the parent-supplied settings are dropped and only the admin tier applies. `"merge"`: the parent-supplied settings apply under the admin tier, filtered so they can tighten policy but not loosen it. Has no effect when no admin tier is deployed. Default: `"first-wins"`.
  - *Implication*: Organizations using both MDM-deployed managed settings and the Agent SDK or IDE extensions can now choose whether host-supplied settings are silently dropped or applied as a subordinate layer.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **New `worktree.baseRef` setting**: Determines which ref new worktrees branch from when using `--worktree`, `EnterWorktree`, or subagent isolation.
  > `"fresh"` (default) branches from `origin/<default-branch>` for a clean tree matching the remote. `"head"` branches from your current local `HEAD`, so unpushed commits and feature-branch state are present in the worktree.
  - *Implication*: Teams that rely on worktrees for testing in-progress work can now persist local commits into worktrees without first pushing them.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **New sandbox binary path settings (`bwrapPath`, `socatPath`)**: Managed-settings-only keys (Linux/WSL2) that override automatic PATH detection for bubblewrap and socat binaries used by the sandbox.
  > Overrides automatic detection via `PATH`. Only honored from managed settings, not from user or project settings. Useful when `bwrap` is installed at a non-standard location in managed environments.
  - *Implication*: Admins can pin sandbox binaries to controlled paths, preventing unexpected version changes.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Desktop / Enterprise

- **New `sshHostAllowlist` managed setting**: Restricts Desktop SSH sessions to an approved set of hostnames. An empty array disables SSH entirely.
  > Administrators can limit Desktop's SSH sessions to an approved set of hosts by adding `sshHostAllowlist` to a managed settings file. Patterns are case-insensitive. `*` matches any host, and `*.example.com` matches `example.com` and any subdomain.
  ```json
  {
    "sshHostAllowlist": ["*.devboxes.example.com", "bastion.example.com"]
  }
  ```
  > `sshHostAllowlist` is read from managed settings only; values in user or project settings are ignored. Only the Claude Desktop app honors this setting; the Claude Code CLI and IDE extensions do not read it, and it does not restrict `ssh` commands run through the Bash tool.
  - *Implication*: Enterprise admins can enforce SSH connection controls for Desktop without affecting CLI or IDE extension sessions. This setting governs Desktop connections only, not network egress — pair it with network or zero-trust controls for a hard boundary.
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

### Environment Variables

- **New `CLAUDE_EFFORT` env var**: Set automatically in Bash tool subprocesses and hook commands to the current effort level for the turn.
  > Set automatically in Bash tool subprocesses and hook commands to the active effort level for the turn: `low`, `medium`, `high`, `xhigh`, or `max`. Matches the `effort.level` field passed to hooks. Only set when the current model supports the effort parameter.
  - *Implication*: Hook scripts and Bash tool commands can now branch on the current effort tier without parsing hook JSON.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **New `MCP_CONNECT_TIMEOUT_MS` env var**: Configures how long the first query waits for MCP servers to connect before snapshotting the tool list. Default: 5000 ms.
  > Servers still pending at the deadline keep connecting in the background but won't appear until the next query. Distinct from `MCP_TIMEOUT`, which bounds an individual server's connect attempt. Most relevant to non-interactive sessions that issue a single query and need slow-connecting servers to be visible.
  - *Implication*: Non-interactive pipelines (`-p`) can tune MCP startup latency without disabling the connection wait entirely via `MCP_CONNECTION_NONBLOCKING`.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_ENABLE_FINE_GRAINED_TOOL_STREAMING` scope expanded to Bedrock and Vertex**: Previously documented as having no effect on Bedrock, Vertex, Foundry, or gateway connections. Bedrock and Vertex now receive per-model support.
  > On Bedrock and Vertex, enabled per model where the deployed container supports it. Set to `1` to force on when routing through a proxy via `ANTHROPIC_BASE_URL`, `ANTHROPIC_VERTEX_BASE_URL`, or `ANTHROPIC_BEDROCK_BASE_URL`. Off by default on Foundry and gateway connections.
  - *Implication*: Bedrock and Vertex users may see streaming tool inputs enabled for supported models without opting in; set to `0` to opt out if needed.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

### Hooks

- **New `effort` field in hook event payloads**: Hook events that fire within a tool-use context now receive an `effort` object alongside existing common fields.
  > Object with a `level` field holding the active effort level for the turn: `"low"`, `"medium"`, `"high"`, `"xhigh"`, or `"max"`. If the requested effort exceeds what the current model supports, this is the downgraded level the model actually used. Present for events such as `PreToolUse`, `PostToolUse`, `Stop`, and `SubagentStop` when the current model supports the effort parameter. The level is also available to hook commands and the Bash tool as the `$CLAUDE_EFFORT` environment variable.
  - *Implication*: Hooks can implement effort-conditional logic (e.g., skip expensive post-processing on low-effort turns).
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

### CLI Flags

- **`--worktree` / `-w` gains GitHub PR-targeting**: Passing `#<number>` or a full GitHub PR URL now fetches and branches the worktree from that PR.
  > Pass `#<number>` or a GitHub pull request URL to fetch that PR from `origin` and branch the worktree from it.
  - *Implication*: Reviewers can spin up an isolated worktree for a specific PR with a single flag argument.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **`--plugin-url` accepts space-separated URLs in a single quoted argument**: Previously the flag documented only the repeat-flag pattern.
  > Repeat the flag for multiple plugins, or pass space-separated URLs in a single quoted value.
  - *Implication*: Shell scripts that build plugin URL lists can pass them as a single string instead of constructing multiple flag instances.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

### Subagents & Skills

- **Skills behavior in subagents clarified**: The `skills` field controls preloading only, not which skills a subagent can invoke. Unlisted skills remain accessible via the Skill tool.
  > The full content of each listed skill is injected into the subagent's context at startup. This field controls which skills are preloaded, not which skills the subagent can access: without it, the subagent can still discover and invoke project, user, and plugin skills through the Skill tool during execution. To prevent a subagent from invoking skills entirely, omit `Skill` from the `tools` list or add it to `disallowedTools`.
  - *Implication*: The previous documentation implied subagents were fully isolated from unlisted skills. That was incorrect; only preloading is restricted by the `skills` field.
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

- **`tools` field documentation updated**: Clarifies that listing `Skill` in the tools array does not preload skills; use the dedicated `skills` field instead.
  > To preload Skills into context, use the `skills` field rather than listing `Skill` here.
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

## Notable Details

- `overview.md` and `quickstart.md` each lost ~550+ lines of embedded React/JSX (`InstallConfigurator`, `Experiment` A/B test wrapper). The readable documentation prose and headings are unchanged; these were UI components inlined into MDX source that are now presumably loaded from a shared module.
- The worktree settings section intro was trimmed from "Use these settings to reduce disk usage and startup time in large monorepos" to just "Configure how `--worktree` creates and manages git worktrees." The new `worktree.baseRef` setting has nothing to do with disk or startup performance, making the old framing inaccurate.
- `plugins.md` was updated with explicit multi-URL examples for `--plugin-url`, mirroring the CLI reference change.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| settings.md | Modified | +92/-88 | New `parentSettingsBehavior`, `worktree.baseRef`, `bwrapPath`, `socatPath` settings; table reformatting |
| desktop.md | Modified | +23/-6 | New `sshHostAllowlist` section and managed settings table entry |
| overview.md | Modified | +0/-634 | Removed inline React `InstallConfigurator` and `Experiment` A/B test components |
| quickstart.md | Modified | +0/-524 | Removed inline React `InstallConfigurator` component |
| env-vars.md | Modified | +3/-1 | New `CLAUDE_EFFORT` and `MCP_CONNECT_TIMEOUT_MS` vars; updated `CLAUDE_CODE_ENABLE_FINE_GRAINED_TOOL_STREAMING` scope |
| hooks.md | Modified | +8/-7 | New `effort` field added to common hook event fields table |
| plugins.md | Modified | +9/-1 | Added multi-URL examples for `--plugin-url` |
| sub-agents.md | Modified | +3/-3 | Clarified `skills` preloading vs Skill tool invocation distinction |
| cli-reference.md | Modified | +2/-2 | Updated `--worktree` (PR targeting) and `--plugin-url` (space-separated URLs) |
| features-overview.md | Modified | +1/-1 | Clarified subagent skill discovery behavior |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-08*
