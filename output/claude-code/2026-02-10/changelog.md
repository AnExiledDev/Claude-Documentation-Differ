# Claude Code CLI Documentation Changes - February 10, 2026

## TL;DR
**Latest Update (6:28 AM):** Claude Code Desktop now officially supports **Act mode** - a fully autonomous execution mode that bypasses all permission checks for both file edits and terminal commands.

**Earlier Update (12:28 AM):** The Claude Code overview documentation received a major restructure focused on real-world use cases and developer workflows. The changes reveal **CLI composability with Unix pipes**, **agent teams for parallel work**, explicit mentions of the **Agent SDK for custom workflows**, and clarification around **Enterprise seat types**.

## New Features & Capabilities

### **Act Mode - Fully Autonomous Execution** ⚡ NEW (6:28 AM)
A new execution mode has been added to Claude Code Desktop that enables completely autonomous operation without permission prompts.

> **Act**: Claude runs without permission checks, automatically executing file edits and terminal commands. Only use this mode in trusted environments.

**Why it matters:** This represents the most autonomous mode available in Claude Code, going beyond even "Code" mode (which still asks for terminal command approval). It's designed for scenarios where maximum speed and automation are needed, such as CI/CD pipelines, containerized development environments, or sandboxed testing scenarios.

**Safety & Access Controls:**
The documentation includes a prominent warning:

> Act runs in `bypassPermissions` mode, which disables all permission checks and should only be used in isolated environments like containers or VMs where Claude Code cannot cause damage. This mode is disabled by default. For personal accounts, enable it in [Claude Code personal settings](https://claude.ai/settings/claude-code). For Team and Enterprise plans, admins must enable it in [Claude Code admin settings](https://claude.ai/admin-settings/claude-code). Act mode does not persist across sessions.

**Access Control Layers:**
- Disabled by default across all account types
- Personal accounts: Must enable in Claude Code personal settings
- Team/Enterprise: Requires admin enablement in admin settings
- Mode does **not persist** across sessions (must be re-enabled each time)

**Mode Comparison Matrix:**

| Mode | File Edits | Terminal Commands | Use Case |
|------|------------|-------------------|----------|
| **Ask** | Manual approval | Manual approval | Recommended for new users |
| **Code** | Auto-approved | Manual approval | Faster iteration with trust |
| **Plan** | Manual approval (after planning) | Manual approval | Complex tasks needing review |
| **Act** | Auto-approved | Auto-approved | ⚠️ Isolated environments only |

---

### **Unix Philosophy & CLI Composability**
The documentation now explicitly showcases Claude Code's scriptability with real Unix-style examples that weren't previously highlighted:

> ```bash
> # Monitor logs and get alerted
> tail -f app.log | claude -p "Slack me if you see any anomalies"
>
> # Automate translations in CI
> claude -p "translate new strings into French and raise a PR for review"
>
> # Bulk operations across files
> git diff main --name-only | claude -p "review these changed files for security issues"
> ```

These examples demonstrate that Claude Code can consume piped input and integrate seamlessly with existing shell workflows - a powerful feature that wasn't emphasized before.

### **Multi-Agent Teams**
New documentation reveals a multi-agent orchestration capability:

> Spawn [multiple Claude Code agents](/en/sub-agents) that work on different parts of a task simultaneously. A lead agent coordinates the work, assigns subtasks, and merges results.

This suggests Claude Code now supports or will support parallel agent execution with coordination - a significant architectural capability for complex tasks.

### **Agent SDK for Custom Workflows**
The documentation now prominently features the Agent SDK as a first-class extension point:

> For fully custom workflows, the [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) lets you build your own agents powered by Claude Code's tools and capabilities, with full control over orchestration, tool access, and permissions.

This positions the Agent SDK as the path for teams building custom automation beyond what the CLI provides.

## Behavior Changes

### **Installation Auto-Update Behavior**
The documentation now clearly distinguishes between installation methods and their update behavior:

- **Native Install (Recommended)**: Auto-updates in the background
- **Homebrew**: Does NOT auto-update - requires manual `brew upgrade claude-code`
- **WinGet**: Does NOT auto-update - requires manual `winget upgrade Anthropic.ClaudeCode`

> Native installations automatically update in the background to keep you on the latest version.

versus

> Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.

This is critical for security-conscious teams who need to understand their update posture.

### **Enterprise Seat Clarity**
The web access availability section was updated with more precise seat type language:

**Before:** `* **Enterprise users**`

**After:** `* **Enterprise users** with premium seats or Chat + Claude Code seats`

This reveals that not all Enterprise users automatically get web access - specific seat types are required.

## Hidden Gems

### **Container/VM-First Positioning** 🔍 NEW (6:28 AM)
The emphasis on "isolated environments like containers or VMs" for Act mode suggests Claude Code is being positioned for use in cloud development environments, DevContainers, and similar sandboxed setups - aligning with the industry trend toward cloud-based IDEs and ephemeral development environments.

### **Multi-Layer Governance Model** 🔍 NEW (6:28 AM)
The combination of admin settings + user settings + session non-persistence shows a thoughtful security model. Even if accidentally enabled at the admin level, users must still opt-in, and it resets every session. This reveals enterprise-grade governance thinking.

### **Chrome Integration Mention**
Buried in the "Use Claude Code everywhere" table is a reference to Chrome integration:

> | Debug live web applications | [Chrome](/en/chrome) |

This suggests a browser extension or protocol for connecting Claude Code to Chrome for live debugging and web app testing - a capability that could enable visual testing and DOM manipulation.

### **Git Worktree Support**
The Desktop app description mentions "parallel sessions via git worktrees":

> a standalone application with diff review, parallel sessions via git worktrees, and the ability to launch cloud sessions.

This indicates the Desktop app can manage multiple concurrent Claude Code sessions using Git's worktree feature - useful for working on multiple branches simultaneously.

### **iOS App Support**
The documentation now confirms Claude Code runs on the iOS app:

> Start a task on your laptop and pick it up on your phone. [Claude Code on the web](/en/claude-code-on-the-web) and the [Claude iOS app](https://apps.apple.com/app/claude-by-anthropic/id6473753684) run sessions on cloud infrastructure

This means you can literally continue coding sessions from a mobile device - remarkable for asynchronous workflows.

## Documentation Structure Changes

### **Removed Sections**
The following sections were completely removed from the overview:
- "Why developers love Claude Code" - removed marketing fluff
- "Additional resources" - consolidated elsewhere

### **New Sections Added**
These new sections represent a shift toward practical examples:
- "What you can do" - accordion-based use cases
- "Monitor logs and get alerted" - Unix pipe example
- "Automate translations in CI" - CI/CD example
- "Bulk operations across files" - batch processing example

### **Retitled Sections**
- "Get started in 30 seconds" → "Get started" (dropped time claim)
- "What Claude Code does for you" → "What you can do" (user-empowering framing)

## Technical Details

### **Act Mode Implementation** 🔧 NEW (6:28 AM)
- **Internal name:** `bypassPermissions` mode
- **Capabilities:** Auto-executes both file edits AND terminal commands
- **Persistence:** Does not persist across sessions (safety feature)
- **Access control layers:**
  1. Global default: Disabled
  2. Admin level: Must be enabled in organization settings (Team/Enterprise)
  3. User level: Individual opt-in required in personal settings
  4. Session level: Must be selected per session (no persistence)

### **Third-Party Provider Support**
The installation section now explicitly mentions third-party integrations for certain surfaces:

> The Terminal CLI and VS Code also support [third-party providers](/en/third-party-integrations).

This confirms that while most surfaces require Claude subscriptions, the CLI and VS Code can work with AWS Bedrock, GCP Vertex AI, or other providers.

### **Skills = Custom Slash Commands**
The documentation clarifies that "skills" are packaged slash commands:

> Create [custom slash commands](/en/skills) to package repeatable workflows your team can share, like `/review-pr` or `/deploy-staging`.

This reveals the skills system is essentially a way to create reusable Claude Code prompts accessible via `/` commands.

### **Hooks for Automation**
Hooks are described as before/after action automation:

> [Hooks](/en/hooks) let you run shell commands before or after Claude Code actions, like auto-formatting after every file edit or running lint before a commit.

This is essentially a pre-commit/post-commit style system but for Claude Code's own actions.

## Unified Cross-Platform Experience

A new section emphasizes consistency across surfaces:

> Each surface connects to the same underlying Claude Code engine, so your CLAUDE.md files, settings, and MCP servers work across all of them.

This is important for teams that want to standardize configuration - a `CLAUDE.md` file works whether you're in the terminal, VS Code, the web, or the desktop app.

---

## Strategic Implications

### Act Mode Release (6:28 AM update)
The addition of Act mode reveals several strategic directions:

1. **Automation-first workflows**: Claude Code is moving toward supporting fully automated development workflows where human-in-the-loop would be a bottleneck.

2. **Enterprise security posture**: The granular permission controls and explicit warnings show Anthropic is thinking about enterprise security requirements and compliance frameworks.

3. **DevOps integration potential**: Act mode enables integration with CI/CD pipelines, automated testing frameworks, and infrastructure-as-code workflows where manual approvals aren't feasible.

4. **Safety-by-default philosophy**: Despite adding a powerful autonomous mode, it's opt-in at multiple levels and doesn't persist - showing commitment to safe defaults even as capabilities expand.

### Overview Restructure (12:28 AM update)
This documentation update represents a maturation from "why you should try this" to "here's how to use it effectively." The emphasis on Unix composability, multi-agent workflows, and the Agent SDK suggests Anthropic is positioning Claude Code as infrastructure for automation, not just an interactive coding assistant. The explicit examples of piping logs and chaining with git commands indicate serious production use cases are emerging.

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-10*
*Two updates: 12:28 AM (overview restructure) and 6:28 AM (Act mode addition)*
