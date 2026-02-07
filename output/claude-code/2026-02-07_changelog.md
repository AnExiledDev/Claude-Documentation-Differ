# Claude Code CLI Documentation Changes - February 7, 2026

## TL;DR
Major new capabilities revealed: Auto Memory system for persistent learnings across sessions, two new hook events (`TeammateIdle` and `TaskCompleted`) for enforcing quality gates in agent teams, conversation summarization as an alternative to rewinding, and enhanced subagent control with spawning restrictions and per-subagent MCP servers.

## New Features & Capabilities

### **Auto Memory - Claude's Persistent Learning System**
Claude Code can now automatically save learnings, patterns, and insights across sessions in a dedicated memory directory. This is a significant shift from the previous ephemeral-only model:

> **Auto memory** is a persistent directory where Claude records learnings, patterns, and insights as it works. Unlike CLAUDE.md files that contain instructions you write for Claude, auto memory contains notes Claude writes for itself based on what it discovers during sessions.

**What gets saved:**
- Project patterns (build commands, test conventions, code style)
- Debugging insights (solutions to tricky problems, common error causes)
- Architecture notes (key files, module relationships, important abstractions)
- Your preferences (communication style, workflow habits, tool choices)

**Technical details:**
- Stored per-project at `~/.claude/projects/<project>/memory/`
- Main entrypoint is `MEMORY.md` (first 200 lines loaded at session start)
- Additional topic files (e.g., `debugging.md`, `api-conventions.md`) loaded on demand
- Gradual rollout; opt-in with `CLAUDE_CODE_DISABLE_AUTO_MEMORY=0`
- Control via `/memory` command or direct instructions like "remember that we use pnpm, not npm"

### **Agent Team Quality Gates - TeammateIdle and TaskCompleted Hooks**
Two new hook events enable enforcement of quality requirements before teammates stop working or tasks complete:

**`TeammateIdle` hook:**
> Runs when an [agent team](/en/agent-teams) teammate is about to go idle after finishing its turn. Use this to enforce quality gates before a teammate stops working, such as requiring passing lint checks or verifying that output files exist.
>
> When a `TeammateIdle` hook exits with code 2, the teammate receives the stderr message as feedback and continues working instead of going idle.

**`TaskCompleted` hook:**
> Runs when a task is being marked as completed. This fires in two situations: when any agent explicitly marks a task as completed through the TaskUpdate tool, or when an [agent team](/en/agent-teams) teammate finishes its turn with in-progress tasks.
>
> When a `TaskCompleted` hook exits with code 2, the task is not marked as completed and the stderr message is fed back to the model as feedback.

**Example use cases:**
- Enforce passing tests before task completion
- Verify build artifacts exist before teammate goes idle
- Require lint checks to pass
- Ensure documentation is updated

Both hooks use exit code control only (not JSON decision control) and receive teammate/task context in their JSON input.

### **Conversation Summarization - Targeted Context Management**
A new "Summarize from here" option in the rewind menu provides targeted context compression as an alternative to full conversation/code restoration:

> **Summarize from here**: compress the conversation from this point forward into a summary, freeing context window space

**How it differs from restore:**
- Messages before selected message stay intact
- Selected message and subsequent messages get replaced with AI-generated summary
- No files on disk are changed
- Original messages preserved in session transcript for reference
- Can provide optional instructions to guide summary focus

This is similar to `/compact` but targeted - keep early context in full detail and only compress parts using too much space. Useful for:
> Freeing context space: summarize a verbose debugging session from the midpoint forward, keeping your initial instructions intact

### **Enhanced Subagent Control**

**Restrict which subagents can be spawned:**
New `Task(agent_type)` syntax in the `tools` field allows allowlisting which subagent types can be spawned:

```yaml
tools: Task(worker, researcher), Read, Bash
```

> This is an allowlist: only the `worker` and `researcher` subagents can be spawned. If the agent tries to spawn any other type, the request fails and the agent sees only the allowed types in its prompt.

**Per-subagent MCP servers:**
Subagents can now have their own MCP server configurations via the `mcpServers` frontmatter field:

> [MCP servers](/en/mcp) available to this subagent. Each entry is either a server name referencing an already-configured server (e.g., `"slack"`) or an inline definition with the server name as key and a full [MCP server config](/en/mcp#configure-mcp-servers) as value

**Additional subagent configuration options:**
- `maxTurns`: Maximum number of agentic turns before stopping
- `skills`: Preload specific skills into subagent context at startup
- `delegate` permission mode: Coordination-only mode for agent team leads (restricts to team management tools)

### **Skills from Additional Directories**
Skills can now be loaded from directories added via `--add-dir`:

> Skills defined in `.claude/skills/` within directories added via `--add-dir` are loaded automatically and picked up by live change detection, so you can edit them during a session without restarting.

## Behavior Changes

### **Session Memory Model Clarification**
Updated documentation now clarifies that sessions are "independent" rather than "ephemeral":

- **Before:** "Sessions are ephemeral. Unlike claude.ai, Claude Code has no persistent memory between sessions. Each new session starts fresh."
- **After:** "Sessions are independent. Each new session starts with a fresh context window, without the conversation history from previous sessions. Claude can persist learnings across sessions using auto memory."

### **SubagentStop Hook Matcher Support**
`SubagentStop` hooks now support matchers to target specific agent types:

- **Before:** "SubagentStop fires for all subagent completions regardless of matcher values"
- **After:** Both `SubagentStart` and `SubagentStop` support matchers on agent type name

### **Dynamic Skill Character Budget**
The skill metadata character budget is now dynamic rather than static:

- **Before:** "Maximum number of characters for skill metadata (default: 15000)"
- **After:** "The budget scales dynamically at 2% of the context window, with a fallback of 16,000 characters"

The `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable now "overrides" rather than simply setting the limit.

## Removed Content

### **Bedrock Output Token Configuration**
An entire section on recommended output token settings for Amazon Bedrock has been removed:

**Removed section:**
- "5. Output token configuration"
- Recommended settings: `CLAUDE_CODE_MAX_OUTPUT_TOKENS=4096` and `MAX_THINKING_TOKENS=1024`
- Detailed explanation of why these values were recommended for Bedrock's throttling behavior

This suggests either:
1. Bedrock's throttling behavior has changed, making these recommendations unnecessary
2. Claude Code now handles this configuration automatically
3. The recommendations were causing confusion or were no longer accurate

## Hidden Gems

### **New Session End Reason**
The `SessionEnd` hook matcher now includes a new session end reason: `bypass_permissions_disabled`. This suggests there's a bypass permissions mode that can be enabled/disabled, and sessions terminate when it gets disabled.

### **Auto Memory Rollout Control**
The double-negative environment variable naming (`CLAUDE_CODE_DISABLE_AUTO_MEMORY=0` to enable) suggests this was initially planned as an opt-out feature that became opt-in. The gradual rollout mechanism indicates this is a significant feature being carefully deployed.

### **Conversation Forking vs. Summarization**
Documentation now explicitly distinguishes between forking (creating a new branch) and summarizing (staying in same session):

> If you want to branch off and try a different approach while preserving the original session intact, use [fork](/en/how-claude-code-works#resume-or-fork-sessions) instead (`claude --continue --fork-session`).

This clarifies two distinct use cases for managing session state.

## Technical Details

### **Hook Input Schema Additions**
New JSON input fields for hooks:

**TeammateIdle:**
- `teammate_name`: Name of teammate about to go idle
- `team_name`: Name of the team

**TaskCompleted:**
- `task_id`: Identifier of task being completed
- `task_subject`: Title of the task
- `task_description`: Detailed description (may be absent)
- `teammate_name`: Name of teammate completing task (may be absent)
- `team_name`: Name of team (may be absent)

### **CLI Agent Flag Enhancements**
The `--agents` flag now supports these additional fields:
- `disallowedTools`: Array of tool names to explicitly deny
- `skills`: Array of skill names to preload into subagent context
- `mcpServers`: Array of MCP servers for the subagent
- `maxTurns`: Maximum agentic turns limit

The documentation notes that `tools` now "Supports [`Task(agent_type)`](/en/sub-agents#restrict-which-subagents-can-be-spawned) syntax" for spawn restrictions.

### **Memory File Loading Behavior**
Clarified hierarchy for CLAUDE.md file loading:

> CLAUDE.md files in the directory hierarchy above the working directory are loaded in full at launch. CLAUDE.md files in child directories load on demand when Claude reads files in those directories. Auto memory loads only the first 200 lines of `MEMORY.md`.

### **Delegate Permission Mode**
New `delegate` permission mode added to the permission modes table:

> Coordination-only mode for [agent team](/en/agent-teams) leads. Restricts to team management tools

This wasn't previously documented as a distinct permission mode.

---
*Generated from Claude Code CLI documentation changes detected on February 7, 2026*
