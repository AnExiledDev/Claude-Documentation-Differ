# Claude Code Documentation Changes — 2026-02-27

## Summary

28 pages were modified across the Claude Code documentation with no pages added or removed across two update runs. The most substantive changes are a terminology shift from "headless mode" to "non-interactive mode" (aligning with the Agent SDK framing), the addition of a plugin marketplace submission portal, new environment variables for disabling adaptive reasoning and fast mode, and broad code block formatting standardization across dozens of pages.

---

## Significant Changes

### Terminology

- **"Headless mode" renamed to "Non-interactive mode"**: All references to "headless mode" for running Claude via `-p` in scripts or CI have been replaced with "non-interactive mode." The `headless.md` page itself was already retitled "Run Claude Code programmatically" in a prior update, but this change brings the prose throughout the docs into alignment.
  > Before: `"Once you're effective with one Claude, multiply your output with parallel sessions, headless mode, and fan-out patterns."`
  > After: `"Once you're effective with one Claude, multiply your output with parallel sessions, non-interactive mode, and fan-out patterns."`
  - *Implication*: The `headless.md` note states "The CLI was previously called 'headless mode'" — developers should update any internal documentation or onboarding materials that use the old term.
  - *Source*: [Best Practices](https://code.claude.com/docs/en/best-practices.md), [Run Claude Code programmatically](https://code.claude.com/docs/en/headless.md)

- **CLI terminology updated from "REPL" to "session"**: The CLI reference table description for `claude` changed from "Start interactive REPL" to "Start interactive session", and `claude "query"` from "Start REPL with initial prompt" to "Start interactive session with initial prompt."
  > Before: `| \`claude\` | Start interactive REPL |`
  > After: `| \`claude\` | Start interactive session |`
  - *Implication*: Minor but signals Anthropic is moving away from REPL as the conceptual model toward "sessions" as the primary abstraction.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

### Configuration

- **New `CLAUDE_CODE_DISABLE_FAST_MODE` environment variable**: Setting `CLAUDE_CODE_DISABLE_FAST_MODE=1` disables fast mode entirely at the environment level. This supplements the existing admin-level controls in the Console and Claude AI admin settings.
  > `"Another option to disable fast mode entirely is to set CLAUDE_CODE_DISABLE_FAST_MODE=1. See Environment variables."`
  - *Implication*: Operators can now disable fast mode without admin UI access — useful for CI environments, LLM gateway setups, or scripted deployments where fast mode behavior is undesirable.
  - *Source*: [fast-mode.md](https://code.claude.com/docs/en/fast-mode.md), [settings.md](https://code.claude.com/docs/en/settings.md)

- **New `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` environment variable documented**: The model configuration page gained explicit documentation for disabling adaptive reasoning on Opus 4.6 and Sonnet 4.6, reverting to the fixed thinking budget controlled by `MAX_THINKING_TOKENS`.
  > `"To disable adaptive reasoning on Opus 4.6 and Sonnet 4.6 and revert to the previous fixed thinking budget, set CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1. When disabled, these models use the fixed budget controlled by MAX_THINKING_TOKENS."`
  - *Implication*: Useful for teams that need cost-predictable or latency-deterministic behavior who want to opt out of the dynamic effort allocation introduced with Opus/Sonnet 4.6.
  - *Source*: [Model Configuration](https://code.claude.com/docs/en/model-config.md)

- **Permissions link corrected in Best Practices**: The "Configure permissions" section linked to `/en/settings` for permission configuration guidance; it now correctly points to `/en/permissions`. Similarly, the sandboxing link was simplified from `/en/sandboxing#sandboxing` to `/en/sandboxing`.
  - *Implication*: Developers following the best practices guide will now land on the dedicated permissions page rather than the general settings page.
  - *Source*: [Best Practices](https://code.claude.com/docs/en/best-practices.md)

### Plugins

- **Official plugin marketplace submission portal added**: A new section "Submit your plugin to the official marketplace" was added to the plugin creation guide, with direct links to the in-app submission forms.
  > `"To submit a plugin to the official Anthropic marketplace, use one of the in-app submission forms: Claude.ai: claude.ai/settings/plugins/submit — Console: platform.claude.com/plugins/submit"`
  - *Implication*: Developers who have built plugins now have a documented, official channel to submit them to Anthropic's curated marketplace, rather than only distributing via self-hosted marketplaces.
  - *Source*: [Create Plugins](https://code.claude.com/docs/en/plugins.md), [Discover and Install Plugins](https://code.claude.com/docs/en/discover-plugins.md)

---

## Notable Details

- **VS Code docs: capitalization and intro text**: The VS Code extension page standardized bullet list items to sentence case throughout ("Click" → "click", "Available" → "available", etc.) and added a brief "Before installing, make sure you have:" intro sentence before the prerequisites list. These are editorial, not functional.

- **Best practices "Related resources" simplified**: The "Related resources" section at the bottom of the best practices page changed from a visual `CardGroup` component to a plain markdown bulleted list. Same links, different presentation.

- **headless.md "Next steps" simplified**: Same pattern as above — the CardGroup of links at the bottom of the programmatic usage page was replaced with a plain bulleted list.

- **Code block syntax annotations widespread**: Across at least 10 pages, bare triple-backtick code fences (` ``` `) were updated to include language and theme annotations (e.g., `` ```text  theme={null} ``, `` ```bash  theme={null} ``, `` ```json  theme={null} ``). This is a rendering/formatting change that affects how code blocks display in the documentation system but has no impact on content.

- **Bold formatting removed from CLAUDE.md description**: In best-practices.md, the phrase "**it can't infer from code alone**" lost its bold emphasis: now "it can't infer from code alone". Minor editorial cleanup.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| best-practices.md | Modified | +24/-37 | "Headless mode" → "non-interactive mode"; link fix to /permissions; CardGroup → list; code block formatting |
| headless.md | Modified | +4/-17 | Next steps CardGroup → bulleted list (net line reduction) |
| vs-code.md | Modified | +18/-16 | Capitalization standardization throughout; added prerequisites intro text |
| quickstart.md | Modified | +30/-30 | Content restructuring (equal add/remove) |
| interactive-mode.md | Modified | +11/-11 | Code block formatting standardization |
| sub-agents.md | Modified | +8/-8 | Code block formatting standardization |
| plugins.md | Modified | +8/-1 | New "Submit your plugin to the official marketplace" section |
| agent-teams.md | Modified | +9/-9 | Code block formatting standardization |
| cli-reference.md | Modified | +8/-6 | "REPL" → "session" terminology; added intro sentence; capitalization fixes |
| model-config.md | Modified | +3/-1 | Added `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` env var documentation |
| discover-plugins.md | Modified | +6/-1 | Official marketplace submission forms documented |
| settings.md | Modified | +5/-3 | Added `CLAUDE_CODE_DISABLE_FAST_MODE` to env vars table; minor edits |
| fast-mode.md | Modified | +2/-0 | Added note on `CLAUDE_CODE_DISABLE_FAST_MODE=1` as opt-out option |
| skills.md | Modified | +7/-7 | Code block formatting standardization |
| hooks-guide.md | Modified | +4/-4 | Code block formatting standardization |
| desktop.md | Modified | +2/-0 | Minor additions |
| gitlab-ci-cd.md | Modified | +3/-3 | Minor edits |
| keybindings.md | Modified | +2/-2 | Minor edits |
| plugins-reference.md | Modified | +3/-3 | Minor edits |
| hooks.md | Modified | +1/-1 | Minor edit |
| github-actions.md | Modified | +1/-1 | Minor edit |
| common-workflows.md | Modified | +1/-1 | Minor edit |
| costs.md | Modified | +1/-1 | Minor edit |
| sandboxing.md | Modified | +1/-1 | Minor edit |
| statusline.md | Modified | +1/-1 | Minor edit |
| troubleshooting.md | Modified | +2/-2 | Minor edits |
| claude-code-on-the-web.md | Modified | +1/-1 | Minor edit |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-27*
