# Claude Code Documentation Changes — 2026-03-20

## Summary

Ten documentation pages were updated with no new or removed pages (19 additions, 11 deletions total). The most substantive changes document a new `resume` trigger for `SessionEnd` hooks (fired when switching sessions via interactive `/resume`), an `effort` frontmatter field for skills and subagents enabling per-component reasoning budget overrides, and a new workspace trust requirement section for the status line feature.

---

## Significant Changes

### Hooks

- **New `SessionEnd` reason: `resume`**: Interactive `/resume` session switching now fires `SessionEnd` hooks with `reason: "resume"`. Previously, switching sessions was not documented as a trigger, and existing reason values could not match it.

  > `| resume | Session switched via interactive /resume |`

  The matcher value tables in both `hooks.md` and `hooks-guide.md` were updated:

  > `SessionEnd` — why the session ended — `clear`, **`resume`**, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`

  - *Implication*: Hook authors who need to run cleanup only on true session exit (not on session switching) should add an explicit `reason != "resume"` guard. Those who want to respond specifically to session switches can now match on `resume`.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md), [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)

- **`CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` scope expanded to include `/resume`**: The environment variable description now explicitly lists three triggers: session exit, `/clear`, and switching sessions via interactive `/resume`.

  > `Maximum time in milliseconds for SessionEnd hooks to complete (default: 1500). Applies to session exit, /clear, and switching sessions via interactive /resume.`

  - *Implication*: Operators who rely on this timeout budget should be aware it now also applies to the `/resume` path, and may need to increase the value if `/resume` is frequent and hooks do non-trivial work.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

---

### Model Configuration

- **Effort level now settable in skill and subagent frontmatter**: A new `effort` method was added to the effort-setting documentation, and the precedence chain was updated to clarify how frontmatter interacts with environment variables and session-level settings.

  > `Skill and subagent frontmatter: set effort in a skill or subagent markdown file to override the effort level when that skill or subagent runs`

  Updated precedence description:

  > `The environment variable takes precedence over all other methods, then your configured level, then the model default. Frontmatter effort applies when that skill or subagent is active, overriding the session level but not the environment variable.`

  - *Implication*: Individual subagents and skills can now pin their own effort level (e.g., `low` for speed-sensitive exploratory agents, `max` for deep reasoning tasks) without changing the session-wide setting. The environment variable remains the highest-priority override and cannot be overridden by frontmatter.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

---

### Subagents

- **New `effort` frontmatter field**: The supported frontmatter fields table gains an `effort` entry.

  > `| effort | No | Effort level when this subagent is active. Overrides the session effort level. Default: inherits from session. Options: low, medium, high, max (Opus 4.6 only) |`

  - *Implication*: Subagent definition files can now include `effort: low` (or `medium`, `high`, `max`) to pin the reasoning budget for that agent's entire run, independent of what the parent session uses.
  - *Source*: [Create custom subagents](https://code.claude.com/docs/en/sub-agents.md)

- **`--agents` CLI flag now documents `effort`, `background`, and `isolation`**: The flag description was extended to include three previously undocumented accepted fields.

  > `The --agents flag accepts JSON with the same frontmatter fields as file-based subagents: description, prompt, tools, disallowedTools, model, permissionMode, mcpServers, hooks, maxTurns, skills, memory, effort, background, and isolation.`

  - *Implication*: Ephemeral CLI-defined agents (used in automation or quick testing) can now configure effort, background execution mode, and worktree isolation without writing a subagent file to disk.
  - *Source*: [Create custom subagents](https://code.claude.com/docs/en/sub-agents.md)

- **Memory configuration UI label renamed**: The quickstart walkthrough's memory step changed the option label from "**Enable**" to "**User scope**".

  > `Select User scope to give the subagent a persistent memory directory at ~/.claude/agent-memory/.`

  - *Implication*: This reflects a UI label change in the `/agents` interactive wizard. Users following the walkthrough should look for "User scope" rather than "Enable".
  - *Source*: [Create custom subagents](https://code.claude.com/docs/en/sub-agents.md)

---

### Status Line

- **Workspace trust requirement documented**: A new "Workspace trust required" section was added to the troubleshooting part of the status line page, explaining that `statusLine` only executes after accepting the workspace trust dialog — the same requirement as hooks and other shell-executing settings.

  > `The status line command only runs if you've accepted the workspace trust dialog for the current directory. Because statusLine executes a shell command, it requires the same trust acceptance as hooks and other shell-executing settings.`
  >
  > `If trust isn't accepted, you'll see the notification statusline skipped · restart to fix instead of your status line output. Restart Claude Code and accept the trust prompt to enable it.`

  - *Implication*: Users who configure a status line in a new directory and see no output (or a blank bar) should check for the `statusline skipped · restart to fix` notification rather than debugging their script. Restarting Claude Code and accepting the trust prompt resolves it.
  - *Source*: [Customize your status line](https://code.claude.com/docs/en/statusline.md)

---

### Plugins & Marketplaces

- **New reserved marketplace name: `knowledge-work-plugins`**: Added to the list of names reserved for official Anthropic use in the plugin marketplaces documentation.

  > Reserved names now include: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, **`knowledge-work-plugins`**, `life-sciences`

  - *Implication*: Third-party marketplace authors using `knowledge-work-plugins` as their marketplace name must rename it to avoid rejection.
  - *Source*: [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

- **Settings doc removes hard-coded marketplace source type count**: The description changed from "The allowlist supports **seven** marketplace source types" to "The allowlist supports **multiple** marketplace source types".

  - *Implication*: Cosmetic wording change, likely anticipating additional source types without requiring a doc update to the count.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`/reload-plugins` description corrected in two pages**: Both `plugins.md` and `discover-plugins.md` changed "reloads **commands**, skills, agents, hooks..." to "reloads **plugins**, skills, agents, hooks...", correcting an inaccurate term.

  - *Source*: [Plugins](https://code.claude.com/docs/en/plugins.md), [Discover plugins](https://code.claude.com/docs/en/discover-plugins.md)

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| statusline.md | Modified | +5 / -0 | New "Workspace trust required" troubleshooting section |
| hooks.md | Modified | +3 / -2 | Added `resume` to `SessionEnd` matcher values and reason table; expanded timeout scope description |
| sub-agents.md | Modified | +3 / -2 | Added `effort` frontmatter field; expanded `--agents` field list; renamed memory UI option |
| model-config.md | Modified | +2 / -1 | Added frontmatter as an effort-setting method; updated precedence chain description |
| hooks-guide.md | Modified | +1 / -1 | Added `resume` to `SessionEnd` matcher values |
| env-vars.md | Modified | +1 / -1 | Expanded `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` scope to include `/resume` |
| plugin-marketplaces.md | Modified | +1 / -1 | Added `knowledge-work-plugins` to reserved marketplace names |
| plugins.md | Modified | +1 / -1 | Corrected `/reload-plugins` description: "commands" → "plugins" |
| discover-plugins.md | Modified | +1 / -1 | Corrected `/reload-plugins` description: "commands" → "plugins" |
| settings.md | Modified | +1 / -1 | Changed "seven" to "multiple" for marketplace source type count |

---

*Generated from Claude Code CLI documentation changes detected on 2026-03-20*
