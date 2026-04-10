# Claude Code Documentation Changes — 2026-04-10

## Summary

78 pages were modified in this update. The dominant change is the addition of a machine-readable `<AgentInstructions>` block to every page, embedding a documentation feedback API endpoint for AI agents. Beyond that infrastructure change, version 2.1.98 (April 9) adds substantial features: a new Monitor tool for background process streaming, a Google Vertex AI interactive setup wizard, two new security-oriented environment variables, a new CLI flag for prompt-cache optimization, and expanded keybinding support for fullscreen scroll actions. Several documentation sections were also substantively expanded with new guidance on compaction behavior, CLAUDE.md maintenance, and voice dictation troubleshooting.

---

## Significant Changes

### New Features

- **Monitor tool**: A new built-in tool (`Monitor`) is now documented in `tools-reference.md`. It runs a command in the background and feeds each output line back to Claude mid-conversation — enabling Claude to tail logs, poll CI jobs, watch directories, or track any long-running script without pausing the session.

  > "The Monitor tool lets Claude watch something in the background and react when it changes, without pausing the conversation."

  - *Implication*: Developers can now ask Claude to watch a process and react when something changes, all in the same conversation. Monitor uses the same permission rules as Bash. Not available on Bedrock, Vertex, or Foundry. Requires v2.1.98+.
  - *Source*: [Tools reference](https://code.claude.com/docs/en/tools-reference.md)

- **`--exclude-dynamic-system-prompt-sections` CLI flag**: A new print-mode flag moves per-machine sections of the system prompt (working directory, environment info, memory paths, git status) into the first user message instead. This improves prompt-cache hit rates when many users run the same headless task from different machines.

  > "Improves prompt-cache reuse across different users and machines running the same task. Only applies with the default system prompt; ignored when `--system-prompt` or `--system-prompt-file` is set. Use with `-p` for scripted, multi-user workloads"

  - *Implication*: Teams running Claude Code as an automated pipeline across many machines can reduce token costs through better caching without changing their system prompts.
  - *Source*: [CLI reference](https://code.claude.com/docs/en/cli-reference.md)

- **`/setup-vertex` command**: A new slash command is now documented for configuring Google Vertex AI authentication, project, region, and model pins through an interactive wizard. It is only visible when `CLAUDE_CODE_USE_VERTEX=1` is set.

  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

### Cloud Provider Integrations

- **Google Vertex AI interactive setup wizard** (`google-vertex-ai.md`): The Vertex AI setup page was substantially reorganized. The old single "Setup" section was replaced with three new sections: "Sign in with Vertex AI" (a wizard-driven quick-start flow accessible from the login screen), "Set up manually" (the prior env-var-based approach, now clearly separated for CI/enterprise use), and "Startup model checks" (v2.1.94+ behavior).

  > "If you have Google Cloud credentials and want to start using Claude Code through Vertex AI, the login wizard walks you through it. You complete the GCP-side prerequisites once per project; the wizard handles the Claude Code side."

  > "After you've signed in, run `/setup-vertex` any time to reopen the wizard and change your credentials, project, region, or model pins."

  - *Implication*: First-time Vertex AI users can now configure Claude Code without manually setting environment variables — the wizard handles auth, project/region detection, model availability checks, and persisting config to `settings.json`.
  - *Source*: [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai.md)

- **Amazon Bedrock restructured setup** (`amazon-bedrock.md`): The Bedrock page received parallel restructuring. "Set up with the interactive wizard" and "Setup" sections were replaced by "Sign in with Bedrock" (new wizard-first flow), "Set up manually" (env-var approach), and "Startup model checks". The model-pin warning was also updated to reflect the fallback behavior:

  > "Claude Code \[falls back\] to the previous version at startup when the latest is unavailable, but pinning lets you control when your users move to a new model."

  The "Startup model checks" section documents that v2.1.94+ verifies model accessibility at startup and prompts to update stale pins, while falling back silently for unpinned models.

  - *Source*: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md)

### Security & Environment Variables

- **`CLAUDE_CODE_PERFORCE_MODE`** (new env var): When set to `1`, `Edit`, `Write`, and `NotebookEdit` fail with a `p4 edit <file>` hint if the target file lacks the owner-write bit. Perforce clears this bit on synced files until `p4 edit` opens them, so this prevents Claude Code from bypassing Perforce change tracking.

  - *Implication*: Developers working in Perforce-managed codebases can now enforce correct change-tracking behavior rather than silently overwriting read-only files.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_SCRIPT_CAPS`** (new env var): A JSON object (used alongside `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`) that limits how many times specific scripts may be invoked per session. Keys are substrings matched against command text; values are integer call limits.

  > "For example, `{\"deploy.sh\": 2}` allows `deploy.sh` to be called at most twice. Matching is substring-based so shell-expansion tricks like `./scripts/deploy.sh $(evil)` still count against the cap."

  - *Implication*: Admins deploying Claude Code in automated or multi-user environments can set hard limits on dangerous script invocations as a defense-in-depth control.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` expanded**: The description for this existing variable was updated to document new Linux-specific behavior: when set, Bash subprocesses now run in an isolated PID namespace, preventing child processes from reading host process environments via `/proc`. Side effect: `ps`, `pgrep`, and `kill` cannot see or signal host processes from within the sandboxed subprocess.

  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

### Keyboard Shortcuts

- **New `Scroll` context in keybindings** (`keybindings.md`): A new `### Scroll actions` section documents scroll and text-selection actions available in fullscreen rendering mode. Includes `scroll:lineUp/Down`, `scroll:pageUp/Down`, `scroll:halfPageUp/Down`, `scroll:fullPageUp/Down`, `scroll:top`, `scroll:bottom`, `selection:copy` (`Ctrl+Shift+C` / `Cmd+C`), and `selection:clear`.

  - *Implication*: Users in fullscreen mode can now rebind scroll and selection actions via `~/.claude/keybindings.json`.
  - *Source*: [Customize keyboard shortcuts](https://code.claude.com/docs/en/keybindings.md)

### Documentation Guidance

- **"What survives compaction"** (`context-window.md`): A new `## What survives compaction` section with a reference table explains exactly what happens to each instruction mechanism after `/compact` runs.

  | Mechanism | After compaction |
  |:--|:--|
  | System prompt and output style | Unchanged |
  | Project-root CLAUDE.md and unscoped rules | Re-injected from disk |
  | Rules with `paths:` frontmatter | Lost until matching file is read again |
  | Invoked skill bodies | Re-injected, capped at 5,000 tokens/skill and 25,000 total |

  - *Implication*: Developers who rely on path-scoped rules or nested CLAUDE.md files across long sessions should be aware these are summarized away by compaction and only reload when a matching file is next read.
  - *Source*: [Explore the context window](https://code.claude.com/docs/en/context-window.md)

- **"When to add to CLAUDE.md"** (`memory.md`): A new subsection provides specific trigger conditions for adding to CLAUDE.md:

  > "Add to it when: Claude makes the same mistake a second time; a code review catches something Claude should have known about this codebase; you type the same correction or clarification into chat that you typed last session; a new teammate would need the same context to be productive."

  - *Source*: [How Claude remembers your project](https://code.claude.com/docs/en/memory.md)

- **"Build your setup over time"** (`features-overview.md`): A new subsection provides a decision table mapping observable triggers to the appropriate extension mechanism (CLAUDE.md, skill, MCP server, subagent, hook, or plugin). Helps users understand when to reach for each tool rather than configuring everything upfront.

  - *Source*: [Extend Claude Code](https://code.claude.com/docs/en/features-overview.md)

- **Voice dictation troubleshooting** (`voice-dictation.md`): Added a new `### Terminal not listed in macOS Microphone settings` troubleshooting section with `tccutil reset Microphone <bundle-id>` instructions for resetting TCC permissions when a terminal app does not appear in System Settings.

  - *Source*: [Voice dictation](https://code.claude.com/docs/en/voice-dictation.md)

### Terminology & Wording Changes

- **Plugin "commands" renamed to "skills"** in `discover-plugins.md` and `desktop.md`: Several references to plugin "commands" were updated to "skills" to align with current nomenclature. For example, the desktop.md description of the plugin panel changed from "their commands" to "their skills", and discover-plugins.md changed "Plugins that add commands and agents" to "Plugins that add skills and agents".

- **Worktree cleanup clarification** (`common-workflows.md`): The description of automatic subagent worktree cleanup was updated to include untracked files as a blocking condition. Previously the doc stated orphaned worktrees were removed if they had "no modifications to tracked files and no unpushed commits"; the updated text adds "no untracked files" to the criteria.

  - *Implication*: Subagent worktrees with new (never-staged) files are now correctly documented as excluded from automatic cleanup.
  - *Source*: [Common workflows](https://code.claude.com/docs/en/common-workflows.md)

### Infrastructure

- **Universal `<AgentInstructions>` block added to all 78 pages**: Every documentation page now includes a machine-readable feedback instruction block near the top, directing AI agents to submit actionable feedback via `POST https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback`. This is not user-visible content but is visible to LLMs reading the raw documentation.

  > "If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to: `https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback`"

  - *Implication*: This is a documentation quality-feedback loop targeting AI agents that consume the docs (e.g., when Claude Code fetches documentation for context). Each page instructs agents to report issues they detect.

---

## Notable Details

- **Costs page — workspace rate limits**: `costs.md` now notes that for organizations with custom rate limits, Claude Code traffic in the auto-created "Claude Code" workspace counts toward org-wide API rate limits, and admins can set a workspace-level rate limit cap via the Claude Console to protect other production workloads.

- **Bedrock pin warning softened**: The warning about model pinning in `amazon-bedrock.md` was revised. The old text stated that unpinned aliases "may attempt to use a newer model version that isn't available in your Bedrock account, breaking existing users." The new text explains the fallback behavior more accurately: Claude Code falls back to the previous version and shows a notice, so "breaking" is the wrong framing.

- **Monitor tool unavailability**: The Monitor tool is explicitly documented as unavailable on Amazon Bedrock, Google Vertex AI, and Microsoft Foundry — only available when using Anthropic's API directly or via Claude.ai.

- **Changelog entry for v2.1.97** (April 8): The changelog update also documented the prior day's release, including focus view toggle (`Ctrl+O`) in `NO_FLICKER` mode, `refreshInterval` status line setting, and numerous fullscreen/no-flicker rendering fixes.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| env-vars.md | Modified | +200/-188 | Added `AgentInstructions` block; added `CLAUDE_CODE_PERFORCE_MODE` and `CLAUDE_CODE_SCRIPT_CAPS`; updated `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` description with Linux PID namespace detail; column width reformatting throughout |
| google-vertex-ai.md | Modified | +46/-4 | New "Sign in with Vertex AI" wizard section, "Region configuration" renamed/restructured, "Set up manually" replaces old "Setup", new "Startup model checks" section |
| cli-reference.md | Modified | +74/-63 | Added `--exclude-dynamic-system-prompt-sections` flag; column width reformatting throughout |
| changelog.md | Modified | +70/-0 | Added v2.1.98 (April 9) and v2.1.97 (April 8) release notes |
| keybindings.md | Modified | +50/-20 | Added `Scroll` context with scroll and selection actions for fullscreen mode |
| amazon-bedrock.md | Modified | +39/-12 | New "Sign in with Bedrock" wizard section, "Set up manually" replaces "Setup", new "Startup model checks" section, softened pin warning |
| voice-dictation.md | Modified | +33/-1 | New "Terminal not listed in macOS Microphone settings" troubleshooting section |
| tools-reference.md | Modified | +28/-0 | New "Monitor tool" section documenting the Monitor tool (v2.1.98+) |
| features-overview.md | Modified | +27/-1 | New "Build your setup over time" decision table subsection |
| context-window.md | Modified | +29/-1 | New "What survives compaction" reference table |
| plugin-marketplaces.md | Modified | +24/-13 | AgentInstructions block; other wording updates |
| memory.md | Modified | +24/-1 | New "When to add to CLAUDE.md" subsection with specific triggers |
| plugins-reference.md | Modified | +30/-21 | Removed "Inside your plugin directory" section; AgentInstructions block |
| discover-plugins.md | Modified | +15/-5 | Terminology: "commands" → "skills" throughout |
| sub-agents.md | Modified | +15/-3 | AgentInstructions block; minor wording |
| costs.md | Modified | +12/-0 | Added note about workspace rate limits for Claude Code API workspace |
| mcp.md | Modified | +12/-0 | AgentInstructions block |
| commands.md | Modified | +11/-0 | Added `/setup-vertex` command entry |
| common-workflows.md | Modified | +11/-1 | Worktree cleanup now documented to also check for untracked files |
| desktop.md | Modified | +11/-1 | Plugin panel: "commands" → "skills" |
| third-party-integrations.md | Modified | +11/-1 | AgentInstructions block |
| hooks.md | Modified | +13/-3 | AgentInstructions block; minor wording |
| output-styles.md | Modified | +13/-3 | AgentInstructions block; minor wording |
| fullscreen.md | Modified | +13/-1 | AgentInstructions block |
| plugins.md | Modified | +13/-3 | AgentInstructions block; minor wording |
| skills.md | Modified | +14/-2 | AgentInstructions block |
| settings.md | Modified | +14/-2 | AgentInstructions block |
| model-config.md | Modified | +12/-2 | AgentInstructions block |
| hooks-guide.md | Modified | +12/-2 | AgentInstructions block |
| interactive-mode.md | Modified | +11/-1 | AgentInstructions block |
| permission-modes.md | Modified | +11/-1 | AgentInstructions block |
| *60 other pages* | Modified | +10/-0 each | AgentInstructions block only |

---

*Generated from Claude Code CLI documentation changes detected on 2026-04-10*
