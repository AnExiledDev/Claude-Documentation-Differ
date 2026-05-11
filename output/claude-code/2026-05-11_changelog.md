# Claude Code Documentation Changes — 2026-05-11

## Summary

Four new documentation pages were added covering parallel agent execution (`agents.md`), git worktrees (`worktrees.md`), the new `/goal` command (`goal.md`), and Claude Code on Claude Platform on AWS (`claude-platform-on-aws.md`). Version 2.1.139 shipped with agent view (research preview), the `/goal` autonomous-completion command, hook improvements, and a large set of bug fixes. The tools reference received a major expansion with per-tool behavior sections for nine tools and two newly documented tools (`PushNotification`, `RemoteTrigger`).

---

## Significant Changes

### New Features

- **`/goal` command — autonomous multi-turn completion**: A new `/goal` command sets a completion condition and Claude works turn-by-turn until a small fast model (Haiku by default) confirms the condition is met.
  > "The `/goal` command sets a completion condition and Claude keeps working toward it without you prompting each step. After each turn, a small fast model checks whether the condition holds. If not, Claude starts another turn instead of returning control to you."
  - Conditions can be up to 4,000 characters. Accepts `clear`, `stop`, `off`, `reset`, `none`, and `cancel` as aliases for clearing. Works non-interactively via `claude -p "/goal <condition>"`.
  - Implemented as a session-scoped wrapper around a prompt-based Stop hook. If `disableAllHooks` is set in managed policy settings, `/goal` is unavailable. Goals are restored on `--resume` / `--continue` (condition carries over; turn count and token-spend baseline reset).
  - *Implication*: Developers can describe a verifiable end state (e.g., "all tests pass and lint is clean") and let Claude iterate across turns without re-prompting.
  - *Source*: [Keep Claude working toward a goal](https://code.claude.com/docs/en/goal.md)

- **`--worktree` / `-w` flag — isolated parallel sessions**: Claude Code can now launch directly into an isolated git worktree, enabling multiple concurrent sessions without file collisions.
  > "Pass `--worktree` or `-w` to create an isolated worktree and start Claude in it. By default, the worktree is created under `.claude/worktrees/<value>/` at your repository root, on a new branch named `worktree-<value>`."
  - Supports branching from `origin/HEAD` (default), local `HEAD` (via `worktree.baseRef: "head"` in settings), or a specific PR (`claude --worktree "#1234"`).
  - A `.worktreeinclude` file (gitignore syntax) copies gitignored files (e.g., `.env`) into every new worktree automatically.
  - Subagents can get their own worktrees via `isolation: worktree` in subagent frontmatter.
  - Non-git VCS (SVN, Perforce, Mercurial) can hook in via new `WorktreeCreate` and `WorktreeRemove` hooks.
  - *Implication*: Parallel Claude sessions, `/batch` jobs, and subagents can all work on isolated file trees without manual git management.
  - *Source*: [Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees.md)

- **Agent view (v2.1.139, Research Preview)**: Single-screen dashboard for all background Claude Code sessions, opened with `claude agents`. Requires v2.1.139 or later. Administrators can disable it org-wide with the `disableAgentView` managed setting.
  > "Added agent view (Research Preview): a single list of every Claude Code session — running, blocked on you, or done. Run `claude agents` to get started."
  - *Source*: [Manage agents with agent view](https://code.claude.com/docs/en/agent-view.md)

- **Claude Platform on AWS — new provider**: Anthropic-operated Claude API with AWS authentication (SigV4 or workspace API key), IAM access control, and AWS Marketplace billing. Opt-in even when AWS credentials are present; Bedrock and Foundry take routing precedence.
  - Enabled with `CLAUDE_CODE_USE_ANTHROPIC_AWS=1`. Requires `ANTHROPIC_AWS_WORKSPACE_ID`. Base URL derived from `AWS_REGION` as `https://aws-external-anthropic.{region}.api.aws`.
  - Model aliases (`opus`, `sonnet`) resolve to the same latest versions as the direct Anthropic API (Opus 4.7, Sonnet 4.6).
  - Supports corporate proxy/LLM gateway via `ANTHROPIC_AWS_BASE_URL`; set `CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH=1` when the gateway adds SigV4 itself.
  - *Implication*: Organizations already on AWS can route Claude Code through AWS Marketplace billing and IAM access controls without using Bedrock.
  - *Source*: [Claude Code on Claude Platform on AWS](https://code.claude.com/docs/en/claude-platform-on-aws.md)

---

### Tools Reference Expansion

- **Per-tool behavior sections added**: The tools reference expanded from a table-only reference into a detailed behavior guide, with new `##`-level sections for Agent, Edit, Glob, Grep, NotebookEdit, Read, WebFetch, WebSearch, and Write.

  Notable behaviors now explicitly documented:

  | Tool | Key behavior documented |
  |------|------------------------|
  | **Bash** | Output >30,000 chars saved to a file; Claude receives path + preview. Hard ceiling 150,000 chars via `BASH_MAX_OUTPUT_LENGTH`. |
  | **Edit** | Requires read-before-edit. `cat` and `sed -n` in Bash satisfy this; `head`/`tail` do not. `old_string` must be unique or `replace_all: true`. |
  | **Write** | Requires prior read of existing files before overwriting; new files are exempt. |
  | **Glob** | Results capped at 100 files, sorted by modification time. Ignores `.gitignore` by default (unlike Grep). |
  | **Grep** | Built on ripgrep; uses ripgrep regex, not POSIX. Three output modes: `files_with_matches` (default), `content`, `count`. Respects `.gitignore`. |
  | **Read** | Large images resized before sending. PDFs >10 pages require `pages` parameter, max 20 pages per call. |
  | **WebFetch** | Converts HTML to Markdown via a small fast model before returning to Claude — lossy by design. Caches 15 min. Redirects to different hosts are reported rather than followed automatically. |
  | **WebSearch** | Up to 8 internal backend searches per call. Results are titles/URLs only; WebFetch follows up to read pages. Not available on Amazon Bedrock. |
  | **Agent** | Parent sees only the subagent's final text result. Background subagents auto-deny any tool call that would otherwise prompt. |
  | **NotebookEdit** | Targets cells by `cell_id`, not string matching. Three modes: `replace`, `insert`, `delete`. Uses `Edit(...)` path format for permission rules. |

  - *Source*: [Tools reference](https://code.claude.com/docs/en/tools-reference.md)

- **New "Configure tools with permission rules and hooks" section**: Consolidates all rule formats in one table, making the `ToolName(specifier)` syntax explicit for each tool. Notably: an `Edit(...)` allow rule also grants read access to the same path implicitly.
  > "All of these accept the same rule format, `ToolName(specifier)`. The specifier depends on the tool, and several tools share a format."
  - *Source*: [Tools reference](https://code.claude.com/docs/en/tools-reference.md)

- **Two tools newly documented in the table**: `PushNotification` (sends desktop/phone push notifications; not available on Bedrock, Vertex, or Foundry) and `RemoteTrigger` (backs the `/schedule` command; requires Pro/Max/Team/Enterprise, not available on Bedrock/Vertex/Foundry).

---

### Hooks Updates

- **`ExitPlanMode` hook input schema documented**: The `ExitPlanMode` tool now has a documented hook input schema. Claude Code injects `plan` (Markdown content) and `planFilePath` (disk path) into the hook input, since the model only passes `allowedPrompts`.
  > "Claude writes the plan to a file on disk before calling the tool, so the literal `tool_input` from the model only carries `allowedPrompts`. Claude Code injects the plan content and file path before passing the input to hooks."
  - In `PostToolUse`, read `tool_response.plan` for the approved plan content rather than re-reading the file from disk.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **`agent_type` clarified for custom subagents**: For custom subagents, `agent_type` in hook payloads is the `name` field from the agent's frontmatter, not the filename. `SubagentStart` documentation and `SubagentStop` docs were both updated.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **`SubagentStop` behavior clarified**: `SubagentStop` hooks do not support `additionalContext`. Returning `decision: "block"` with a `reason` keeps the subagent running and delivers `reason` as its next instruction. To inject context into the parent session after a subagent returns, use a `PostToolUse` hook on the `Agent` tool instead.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **Model field and env var clarification added**: Only `SessionStart` hooks receive a `model` field. There is no `$CLAUDE_MODEL` environment variable. A hook process can read `$ANTHROPIC_MODEL` if set in the shell, but that value does not update when `/model` is used mid-session.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **Hook `args: string[]` exec form (v2.1.139)**: A new `args: string[]` field for hooks spawns the command directly without a shell, so path placeholders never need quoting.

- **`continueOnBlock` for `PostToolUse` hooks (v2.1.139)**: New option — set `continueOnBlock: true` to feed the hook's rejection reason back to Claude and continue the turn instead of stopping.

- **`/goal` cross-reference added to Stop hooks**: A tip was added to the Stop hook section noting that `/goal` is a built-in shortcut for a session-scoped prompt-based Stop hook.

---

### Background Subagent Permission Model Clarified

The documentation for how background subagents handle permissions was corrected. The previous text implied permissions were "pre-approved before launch." The current documentation states:
> "Background subagents run concurrently while you continue working. They run with the permissions already granted in the session and auto-deny any tool call that would otherwise prompt."

The fork vs. named subagent comparison table was also updated: the Permissions row now reads "Auto-denied when running in the background" instead of "Pre-approved before launch, then auto-denied."

- *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

---

### Permissions Warning Updated

The `Read`/`Edit` deny rule warning was expanded. It previously stated these rules only apply to built-in file tools (not Bash subprocesses). It now clarifies that the rules also cover file commands Claude Code recognizes in Bash (`cat`, `head`, `tail`, `sed`):
> "Read and Edit deny rules apply to Claude's built-in file tools and to file commands Claude Code recognizes in Bash, such as `cat`, `head`, `tail`, and `sed`. They do not apply to arbitrary subprocesses that read or write files indirectly, like a Python or Node script that opens files itself."

- *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

---

### Debug Configuration Table Updated

The troubleshooting row for "Hook never fires — standalone hooks file" was updated to reflect that plugins *can* use a separate `hooks/hooks.json`, while regular user/project config cannot:
> "There is no standalone hooks file for project or user config. Define hooks under the `'hooks'` key in `settings.json`. Only plugins load a separate `hooks/hooks.json`."

- *Source*: [Debug your config](https://code.claude.com/docs/en/debug-your-config.md)

---

### New Environment Variables (Claude Platform on AWS)

Five new environment variables documented:

| Variable | Purpose |
|---|---|
| `CLAUDE_CODE_USE_ANTHROPIC_AWS` | Enable Claude Platform on AWS provider |
| `ANTHROPIC_AWS_WORKSPACE_ID` | Required workspace ID, sent as `anthropic-workspace-id` header |
| `ANTHROPIC_AWS_API_KEY` | Workspace API key (takes precedence over SigV4) |
| `ANTHROPIC_AWS_BASE_URL` | Override endpoint URL (proxy/gateway support) |
| `CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH` | Skip client-side SigV4 when gateway handles signing |

`ENABLE_PROMPT_CACHING_1H` was updated to include Claude Platform on AWS in its description.

`BASH_MAX_OUTPUT_LENGTH` description was corrected: large outputs are now saved to a file and Claude receives the file path plus a preview (not "middle-truncated").

- *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

---

### API Key Behavior Change (v2.1.139)

Remote Control, `/schedule`, claude.ai MCP connectors, and notification preferences are now disabled when `ANTHROPIC_API_KEY`, `apiKeyHelper`, or `ANTHROPIC_AUTH_TOKEN` is set, even if a Claude.ai login also exists.
> "Remote Control, `/schedule`, claude.ai MCP connectors, and notification preferences are now disabled when `ANTHROPIC_API_KEY` / `apiKeyHelper` / `ANTHROPIC_AUTH_TOKEN` is set, even if a Claude.ai login also exists. Unset the API key to use these features."

- *Implication*: Teams mixing API key auth with claude.ai subscriptions will lose access to scheduled tasks and Remote Control unless they unset the API key variable.

---

### MCP Updates (v2.1.139)

- MCP stdio servers now receive `CLAUDE_PROJECT_DIR` in their environment (matching hooks). Plugin configs can reference `${CLAUDE_PROJECT_DIR}` in commands.
- `/mcp` Reconnect now picks up `.mcp.json` edits without a restart, and shows the HTTP status and URL when reconnecting fails.
- Remote MCP server reconnect retry on transient failures is now enabled for all users.
- HTTP/SSE MCP servers: response bodies capped at 16 MB per SSE frame to prevent unbounded memory growth.

---

### LLM Gateway — Claude Platform on AWS Section Added

A new "Claude Platform on AWS through a gateway" subsection was added with an example:

```bash
export ANTHROPIC_AWS_BASE_URL=https://litellm-server:4000/anthropic-aws
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH=1
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
```

- *Source*: [LLM gateway](https://code.claude.com/docs/en/llm-gateway.md)

---

## New Pages

- **[agents.md](https://code.claude.com/docs/en/agents.md)** — Comparison overview for all parallel execution approaches: subagents, agent view, agent teams, worktrees, and `/batch`. Includes a decision matrix (who coordinates, do workers communicate, do tasks touch the same files) and explains how to check on running work via `claude agents`, `/agents`, and `/tasks`.

- **[worktrees.md](https://code.claude.com/docs/en/worktrees.md)** — Full reference for the `--worktree` / `-w` flag, `.worktreeinclude`, subagent worktree isolation, cleanup behavior, manual git worktree management, and non-git VCS hooks (`WorktreeCreate`, `WorktreeRemove`).

- **[goal.md](https://code.claude.com/docs/en/goal.md)** — Reference for the `/goal` command, including condition syntax, status checking, early clearing, non-interactive use, how the evaluator works (session-scoped prompt-based Stop hook on Haiku), and requirements (hooks must not be globally disabled).

- **[claude-platform-on-aws.md](https://code.claude.com/docs/en/claude-platform-on-aws.md)** — Setup guide for routing Claude Code through the Anthropic-operated Claude API with AWS authentication and AWS Marketplace billing. Covers SigV4 and workspace API key auth, model pinning, proxy/gateway routing, Agent SDK integration, and troubleshooting common errors.

---

## Notable Details

- **`BASH_MAX_OUTPUT_LENGTH` behavior change**: The description changed from "middle-truncated" to a file-based approach — large outputs are saved to a file in the session directory and Claude receives the path plus a short preview, up to a 150,000-character hard ceiling. Scripts or hooks that relied on seeing truncated output inline should be updated.

- **Subagent `name` vs. filename**: The `name` frontmatter field (not the `.md` filename) is now explicitly documented as what appears in `agent_type` in hook payloads and `SubagentStart` matchers. Teams filtering subagent hook events by type should verify their matchers use the frontmatter `name`.

- **`/loop` self-paced termination**: In self-paced loop mode, Claude can now end the loop itself by not scheduling the next wakeup once the task is provably complete. Fixed-interval loops continue until manually stopped or after 7 days.

- **Data usage — Claude Platform on AWS**: Telemetry, error reporting, and feedback all default OFF for Claude Platform on AWS (same behavior as Bedrock, Vertex, and Foundry). Session quality surveys and WebFetch domain safety checks remain ON regardless of provider.

- **VS Code shortcut (v2.1.139)**: Press `Cmd/Ctrl+Shift+T` to reopen the most recently closed session tab in VS Code. Configurable via `claudeCode.enableReopenClosedSessionShortcut`.

- **Subagent API headers (v2.1.139)**: API requests from subagents now carry `x-claude-code-agent-id` / `x-claude-code-parent-agent-id` headers. OTEL spans include `agent_id` / `parent_agent_id` attributes. Useful for tracing multi-agent workflows.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| tools-reference.md | Modified | +207/-41 | Major expansion: per-tool behavior sections for 9 tools, new permission rule format table, 2 new tools |
| changelog.md | Modified | +53/-0 | v2.1.139 release notes |
| agents.md | New | +52 | Parallel execution approach comparison and decision guide |
| claude-platform-on-aws.md | New | +341 | Setup guide for Anthropic API via AWS Marketplace |
| goal.md | New | +138 | `/goal` command reference |
| worktrees.md | New | +161 | `--worktree` flag, `.worktreeinclude`, subagent isolation, cleanup |
| hooks.md | Modified | +24/-6 | ExitPlanMode schema, agent_type clarification, SubagentStop behavior, model field note |
| third-party-integrations.md | Modified | +12/-2 | Claude Platform on AWS added to provider comparison table |
| env-vars.md | Modified | +9/-4 | 5 new AWS platform vars, BASH_MAX_OUTPUT_LENGTH correction |
| llm-gateway.md | Modified | +11/-0 | Claude Platform on AWS gateway example added |
| sub-agents.md | Modified | +11/-11 | Background subagent permission model clarified |
| debug-your-config.md | Modified | +18/-18 | Hooks standalone file row updated for plugin exception |
| data-usage.md | Modified | +9/-9 | Claude Platform on AWS column added |
| scheduled-tasks.md | Modified | +3/-1 | Reference to `/goal` added; self-paced loop termination note |
| commands.md | Modified | +3/-0 | Parallel work paragraph; `/goal` entry in command table |
| agent-view.md | Modified | +4/-1 | Links to new agents.md comparison page |
| model-config.md | Modified | +2/-2 | Claude Platform on AWS added to alias resolution and pinning sections |
| permissions.md | Modified | +1/-1 | Read/Edit deny rule warning expanded to cover Bash file commands |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-11*
