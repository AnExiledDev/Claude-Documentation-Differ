# Claude Code Documentation Changes - February 5, 2026

## TL;DR

Major experimental feature launch: **Agent Teams** enable coordinated multi-session workflows with peer-to-peer messaging and shared task management. Opus 4.6 introduces **adaptive reasoning** with adjustable effort levels, replacing fixed thinking token budgets. The plugin system becomes more flexible with optional manifests, and new limitations are documented around Zero Data Retention and 1M context windows.

## New Features & Capabilities

### 🚀 Agent Teams (Experimental)

The headline addition is a complete new page documenting **Agent Teams** - a system for orchestrating multiple Claude Code instances working together with automated coordination.

> Agent teams let you coordinate multiple Claude Code instances working together. One session acts as the team lead, coordinating work, assigning tasks, and synthesizing results. Teammates work independently, each in its own context window, and communicate directly with each other.

**Key capabilities revealed:**
- **Enable with flag**: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` environment variable or settings.json
- **Two display modes**: In-process (works anywhere) or split panes (requires tmux or iTerm2)
- **New CLI flag**: `--teammate-mode` to control display mode (auto, in-process, or tmux)
- **Delegate mode**: New permission mode accessible via Shift+Tab that restricts leads to coordination-only tools
- **Shared task list**: File-locked task system with dependency management stored in `~/.claude/tasks/{team-name}/`
- **Direct messaging**: Teammates can message each other (not just report to lead) via mailbox system
- **Plan approval workflow**: Teammates can be required to plan before implementing, with lead autonomously approving/rejecting

**Architecture details:**
- Teams stored in `~/.claude/teams/{team-name}/config.json`
- Teammates are full Claude Code sessions with independent context windows
- ~7x token usage multiplier when teammates run in plan mode
- One team per session; no nested teams allowed

**Known limitations documented:**
- No session resumption with in-process teammates (`/resume` and `/rewind` don't restore them)
- Task status can lag behind actual completion
- Split panes not supported in VS Code integrated terminal, Windows Terminal, or Ghostty
- Cleanup must be done by lead, not teammates

### 🧠 Opus 4.6 Adaptive Reasoning & Effort Levels

Opus 4.6 introduces a fundamentally different thinking model that dynamically allocates reasoning tokens:

> Additionally, Opus 4.6 introduces adaptive reasoning: instead of a fixed thinking token budget, the model dynamically allocates thinking based on your [effort level](/en/model-config#adjust-effort-level) setting.

**New effort level controls:**
- Three levels: **low**, **medium**, **high** (default)
- Configure via `/model` (with left/right arrows), `CLAUDE_CODE_EFFORT_LEVEL` environment variable, or `effortLevel` in settings
- `MAX_THINKING_TOKENS` is ignored on Opus 4.6 (except when set to 0 to disable thinking entirely)

**Model availability clarified:**
> * **Max and Teams**: defaults to Opus 4.6
> * **Pro**: defaults to Opus 4.6 in Claude Code
> * **Enterprise**: Opus 4.6 is available but not the default

**1M context window restriction:**
> For Opus 4.6, the 1M context window is available for API and Claude Code pay-as-you-go users. Pro, Max, Teams, and Enterprise subscription users do not have access to Opus 4.6 1M context at launch.

This is a significant limitation - subscription users can't access Opus 4.6's extended context despite it being their default model.

## Behavior Changes

### Plugin Manifests Now Optional

Previously, `plugin.json` was described as "required." Now it's optional:

> The manifest is optional. If omitted, Claude Code auto-discovers components in [default locations](#file-locations-reference) and derives the plugin name from the directory name.

The manifest documentation updated:
- **Before**: "Required: plugin manifest"
- **After**: "Plugin metadata and configuration (optional)"

This significantly simplifies plugin development - you can drop a `commands/` or `skills/` directory and go.

### Thinking Token Budget Changes

**Before**: Fixed 31,999 token budget when thinking enabled
**After**: Opus 4.6 uses adaptive reasoning based on effort level; other models still use fixed 31,999 budget

The documentation now explicitly distinguishes behavior:
> **With Opus 4.6**, thinking uses adaptive reasoning: the model dynamically allocates thinking tokens based on the [effort level](/en/model-config#adjust-effort-level) you select (low, medium, high). This is the recommended way to tune the tradeoff between speed and reasoning depth.
>
> **With other models**, thinking uses a fixed budget of up to 31,999 tokens from your output budget.

### Permission Mode Cycling with Agent Teams

When agent teams are active, Shift+Tab cycles through an additional mode:

> When an [agent team](/en/agent-teams) is active, the cycle also includes Delegate Mode.

The cycle becomes: Normal → Auto-Accept → Plan → Delegate → Normal (when teams active).

### Status Line Behavior Clarifications

The documentation removed helper function examples and clarified optional fields:

**Fields that may be absent** (not present in JSON at all):
- `vim`: only present when vim mode enabled
- `agent`: only present with `--agent` flag or agent settings

**Fields that may be null**:
- `context_window.current_usage`: null before first API call in a session

This helps developers write more robust status line scripts without checking for undefined helper functions.

## Hidden Gems

### Zero Data Retention Blocks Analytics Contributions

A new warning reveals an important limitation for privacy-focused organizations:

> Contribution metrics are not available for organizations with [Zero Data Retention](/en/data-usage#data-retention) enabled. The analytics dashboard will show usage metrics only.

If you've enabled Zero Data Retention for compliance, you lose the ability to track which developers are contributing code via Claude Code.

### Plugin Scope Explanation

The `--scope` flag for plugin installation finally gets documented behavior:

> Scope determines which settings file the installed plugin is added to. For example, --scope project writes to `enabledPlugins` in .claude/settings.json, making the plugin available to everyone who clones the project repository.

This clarifies project-level vs user-level plugin installation mechanics.

### Three Ways to Run Parallel Sessions

The documentation now lists three approaches (previously two):

**Before**: Claude Desktop + Claude Code on the web
**After**: Claude Desktop + Claude Code on the web + **Agent teams**

Agent teams are positioned as the automated coordination option, distinct from manual parallel session management.

### Subagent Memory Field Behavior

Subtle clarification on what the `memory` field does:

- **Before**: "designates a persistent directory for the subagent to write to"
- **After**: "gives the subagent a persistent directory that survives across conversations"

The new wording emphasizes survival across sessions, not just write access.

### LiteLLM Security Note

Documentation previously said "we have not audited its security." Now updated to:

> This project is unaffiliated with Anthropic and has not been audited for security.

The passive voice change subtly distances Anthropic from security responsibility while keeping the warning.

## New Documentation Pages

### `docs/en/agent-teams.md`

A comprehensive 380-line guide covering:
- When to use agent teams vs subagents (comparison table included)
- Setup and configuration (display modes, tmux/iTerm2 requirements)
- Team architecture (lead, teammates, task list, mailbox system)
- Control mechanisms (delegate mode, plan approval, task claiming with file locks)
- Use case examples (parallel code review, competing hypotheses debugging)
- Best practices (context, task sizing, avoiding file conflicts)
- Troubleshooting section for common issues
- Detailed limitations list

The page reveals agent teams are **experimental** and disabled by default, suggesting this is a preview/beta feature for power users.

## Technical Details

### New CLI Flags

- `--teammate-mode`: Control agent team display mode (auto/in-process/tmux)

### New Environment Variables

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`: Enable agent teams feature
- `CLAUDE_CODE_EFFORT_LEVEL`: Set Opus 4.6 effort level (low/medium/high)

### New Permission Mode

- `delegate`: Coordination-only mode restricting leads to team management tools (spawning, messaging, shutdown, task management)

### New File Locations

- `~/.claude/teams/{team-name}/config.json`: Team configuration with members array
- `~/.claude/tasks/{team-name}/`: Shared task list directory

### Debug Command Update

Plugin debugging is now accessible in the TUI:

> Use `claude --debug` (or `/debug` within the TUI) to see plugin loading details

Previously only mentioned the CLI flag.

### Auto-compaction Alignment

Documentation now explicitly notes that `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` percentage:

> This percentage aligns with the `context_window.used_percentage` field available in [status line](/en/statusline)

This helps developers coordinate compaction triggers with status line monitoring.

## Cost Implications

The documentation adds explicit token cost warnings:

> Agent teams use approximately 7x more tokens than standard sessions when teammates run in plan mode, because each teammate maintains its own context window and runs as a separate Claude instance.

This is a crucial cost consideration - agent teams can quickly consume 7x your normal budget.

---

*Analysis: This update reveals Claude Code is expanding into multi-agent coordination territory with experimental Agent Teams, while Opus 4.6's adaptive reasoning represents a significant shift from fixed token budgets to dynamic allocation. The optional plugin manifests lower the barrier to extension development, but new restrictions around 1M context for subscription users and Zero Data Retention's impact on analytics show the complexity of scaling these features across different user tiers.*

---
*Generated from documentation changes detected on 2026-02-05*
