# Claude Code Documentation Changes — 2026-03-18

## Summary

Three pages were updated in this cycle. The most substantive change is a new "Invoke subagents explicitly" section in `sub-agents.md` that formalizes three escalation patterns for subagent invocation (natural language, @-mention, and a session-wide `--agent` flag / `agent` setting). The `settings.md` page gains a single new `agent` configuration key, and `changelog.md` was updated with v2.1.78 release notes covering 20+ fixes and additions including a new `StopFailure` hook, a security fix for silent sandbox disablement, and expanded plugin frontmatter support.

---

## Significant Changes

### Subagents — Explicit Invocation Patterns

- **New "Invoke subagents explicitly" section**: The previous single-sentence prompt about requesting a specific subagent has been replaced with a structured section documenting three distinct invocation patterns, escalating from advisory to guaranteed to session-wide.

  > When automatic delegation isn't enough, you can request a subagent yourself. Three patterns escalate from a one-off suggestion to a session-wide default:
  > * **Natural language**: name the subagent in your prompt; Claude decides whether to delegate
  > * **@-mention**: guarantees the subagent runs for one task
  > * **Session-wide**: the whole session uses that subagent's system prompt, tool restrictions, and model via the `--agent` flag or the `agent` setting

  - *Implication*: Developers who need deterministic subagent selection can now use `@agent-<name>` @-mention syntax in the typeahead rather than relying on Claude's automatic delegation. Plugin subagents appear in the typeahead as `<plugin-name>:<agent-name>` and can also be typed manually as `@agent-<plugin-name>:<agent-name>`.
  - *Source*: [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md)

- **`--agent` CLI flag and session-wide invocation documented**: Running the whole session as a named subagent is now formally described, including its interaction with the system prompt and session resume behavior:

  > The subagent's system prompt replaces the default Claude Code system prompt entirely, the same way `--system-prompt` does. `CLAUDE.md` files and project memory still load through the normal message flow. The agent name appears as `@<name>` in the startup header so you can confirm it's active.

  > This works with built-in and custom subagents, and the choice persists when you resume the session.

  For plugin-provided subagents: `claude --agent <plugin-name>:<agent-name>`.

  - *Implication*: The `--agent` flag overrides the `agent` setting when both are present. This enables project-level defaults via `.claude/settings.json` while still allowing per-session overrides from the CLI.
  - *Source*: [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md)

### Configuration — New `agent` Setting

- **`agent` key added to settings reference**: A new top-level setting runs the main session thread as a named subagent, applying its system prompt, tool restrictions, and model to the entire conversation.

  > | `agent` | Run the main thread as a named subagent. Applies that subagent's system prompt, tool restrictions, and model. See [Invoke subagents explicitly](/en/sub-agents#invoke-subagents-explicitly) | `"code-reviewer"` |

  - *Implication*: Teams can commit `.claude/settings.json` with `"agent": "<name>"` to ensure every collaborator's session defaults to a specific subagent configuration — for example, a `code-reviewer` agent with restricted tools and a focused system prompt. The CLI `--agent` flag takes precedence if both are set.
  - *Source*: [settings.md](https://code.claude.com/docs/en/settings.md)

### Release Notes — v2.1.78 (March 17, 2026)

- **`StopFailure` hook event**: New lifecycle hook event fires when a turn ends due to an API error (rate limit, auth failure, etc.), distinct from a normal `Stop`. Allows hook scripts to respond specifically to failure conditions.

- **`${CLAUDE_PLUGIN_DATA}` variable**: Plugin persistent state directory that survives plugin updates. `/plugin uninstall` now prompts before deleting this data.

- **Plugin-shipped agent frontmatter expanded**: `effort`, `maxTurns`, and `disallowedTools` are now supported in frontmatter for plugin-shipped agents.

- **tmux passthrough for terminal notifications**: iTerm2/Kitty/Ghostty popups and the progress bar now reach the outer terminal when running inside tmux, provided `set -g allow-passthrough on` is configured.

- **Streaming response text**: Response text now streams line-by-line as it is generated rather than in larger chunks.

- **Security fix — silent sandbox disable**:
  > **Security:** Fixed silent sandbox disable when `sandbox.enabled: true` is set but dependencies are missing — now shows a visible startup warning.

  Previously, a misconfigured or dependency-missing sandbox could silently fall back to no sandboxing with no user notification.

- **Security fix — protected directories in `bypassPermissions` mode**: `.git`, `.claude`, and other protected directories were writable without a prompt in `bypassPermissions` mode; now fixed.

- **`deny: ["mcp__servername"]` permission enforcement fix**: These permission rules were not removing MCP server tools before sending to the model, allowing the model to see and attempt blocked tools. Now fixed.

- **`sandbox.filesystem.allowWrite` absolute path fix**: Previously required a `//` prefix for absolute paths; now works with standard absolute paths.

- **`ANTHROPIC_CUSTOM_MODEL_OPTION` env var**: Adds a custom entry to the `/model` picker. Optional `_NAME` and `_DESCRIPTION` suffixed variants control the display label and description text.

- **`--worktree` flag now loads skills and hooks**: Previously, skills and hooks from the worktree directory were not loaded when `--worktree` was in use; now fixed.

- **`CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` and `includeGitInstructions` fix**: These were not suppressing the git status section of the system prompt; now fixed.

- **Infinite loop fix**: API errors triggering stop hooks that re-fed blocking errors to the model could cause an infinite loop. Fixed.

- **VSCode fixes**: Brief login screen flash when opening the sidebar while already authenticated; "API Error: Rate limit reached" when selecting Opus (model dropdown no longer offers the 1M context variant to subscribers whose plan tier is unknown).

- *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

---

## Notable Details

- The @-mention syntax for subagents uses the same typeahead UI as file @-mentions. This is newly documented — previously the only documented approach for explicit invocation was natural-language phrasing like "Use the test-runner subagent to...". The @-mention pattern guarantees which subagent runs rather than leaving delegation to Claude's judgment.
- The `--agent` flag is described as architecturally equivalent to `--system-prompt` in terms of system prompt replacement, with the addition of tool restrictions and model selection. This clarifies that it is not a separate mechanism but a named, structured version of `--system-prompt`.
- The v2.1.78 `ANTHROPIC_BETAS` env var fix (silently ignored for Haiku models, now working) enables beta feature testing with smaller/cheaper models — a relevant quality-of-life fix for developers iterating on beta capabilities.
- The `cc log` and `--resume` truncation fix for large sessions (>5 MB) that used subagents addresses a data-loss scenario where conversation history was silently dropped on resume.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `sub-agents.md` | Modified | +41 / -1 | New "Invoke subagents explicitly" section: natural language, @-mention, and `--agent`/`agent` setting session-wide patterns |
| `changelog.md` | Modified | +29 / -0 | Added v2.1.78 release notes (March 17, 2026) |
| `settings.md` | Modified | +1 / -0 | Added `agent` setting to the settings reference table |

---

*Generated from Claude Code CLI documentation changes detected on 2026-03-18*
