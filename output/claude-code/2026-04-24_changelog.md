# Claude Code Documentation Changes — 2026-04-24

## Summary

Seven pages were modified with 126 additions and 3 deletions. The most significant additions are a new experimental "forked subagents" capability (allowing subagents to inherit full conversation context), a new `ENABLE_PROMPT_CACHING_1H` environment variable documented across all three cloud providers (Bedrock, Vertex AI, Foundry), and the v2.1.119 release changelog entry covering 40+ fixes and features.

## Significant Changes

### Subagents — Forked Conversations (Experimental)

- **New fork mode for subagents**: A forked subagent inherits the entire conversation history, system prompt, tools, and model from the parent session rather than starting fresh. Enabled by setting `CLAUDE_CODE_FORK_SUBAGENT=1`. Requires Claude Code v2.1.117 or later.
  > "A fork is a subagent that inherits the entire conversation so far instead of starting fresh. This drops the input isolation that subagents otherwise provide: a fork sees the same system prompt, tools, model, and message history as the main session, so you can hand it a side task without re-explaining the situation."
  - *Implication*: Useful when a named subagent would need too much background context, or when running several parallel approaches from the same starting point. The fork's tool calls stay out of the main conversation; only its final result is returned.
  - *Source*: [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md)

- **Fork mode changes three behaviors**: (1) The general-purpose built-in subagent is replaced by a fork; named subagents like Explore still spawn as before. (2) All subagent spawns run in the background. (3) The `/fork` command spawns a fork rather than acting as an alias for `/branch`.
  > "When fork mode is enabled, every subagent spawn runs in the background regardless of the `background` field. Forks still surface permission prompts in your terminal as they occur instead of pre-approving; named subagents follow the pre-approval flow above."
  - *Source*: [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md)

- **Fork panel UI**: Running forks appear in a panel below the prompt with keyboard controls (`↑`/`↓` to navigate rows, `Enter` to open a fork's transcript and send follow-up messages, `x` to dismiss or stop, `Esc` to return to prompt).
  - *Source*: [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md)

- **Prompt cache sharing**: Because a fork's system prompt and tool definitions are identical to the parent's, its first request reuses the parent's prompt cache, making forking cheaper than a fresh subagent for same-context tasks.
  > "Because a fork's system prompt and tool definitions are identical to the parent, its first request reuses the parent's prompt cache. This makes forking cheaper than spawning a fresh subagent for tasks that need the same context."
  - *Source*: [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md)

- **Fork limitations**: Fork mode works only in interactive sessions — disabled in non-interactive/headless mode and the Agent SDK. A fork cannot spawn further forks. `isolation: "worktree"` is still available when the Agent tool spawns a fork.
  - *Source*: [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md)

### Prompt Caching — 1-Hour TTL Option

- **New `ENABLE_PROMPT_CACHING_1H` environment variable**: Now documented across Amazon Bedrock, Google Vertex AI, and Microsoft Azure Foundry. Setting this to `1` requests a 1-hour prompt cache TTL instead of the default 5-minute TTL.
  > "Optional: Request 1-hour prompt cache TTL instead of the 5-minute default — `export ENABLE_PROMPT_CACHING_1H=1`"
  > "cache writes with a 1-hour TTL are billed at a higher rate than 5-minute writes."
  - *Implication*: Longer cache retention reduces re-computation costs for long sessions, but comes at a higher write billing rate. Teams should weigh session length and cache hit patterns before enabling.
  - *Source*: [amazon-bedrock.md](https://code.claude.com/docs/en/amazon-bedrock.md), [google-vertex-ai.md](https://code.claude.com/docs/en/google-vertex-ai.md), [microsoft-foundry.md](https://code.claude.com/docs/en/microsoft-foundry.md)

- **Google Vertex AI prompt caching description updated**: The Vertex AI docs previously stated caching is supported "when you specify the `cache_control` ephemeral flag"; this has been simplified to "enabled automatically", and now explicitly documents both `DISABLE_PROMPT_CACHING=1` and `ENABLE_PROMPT_CACHING_1H=1` in the same paragraph.
  - *Source*: [google-vertex-ai.md](https://code.claude.com/docs/en/google-vertex-ai.md)

- **Microsoft Foundry gains a prompt caching section**: A new paragraph and code block explain caching defaults and the 1-hour TTL option — this provider had no caching documentation previously.
  - *Source*: [microsoft-foundry.md](https://code.claude.com/docs/en/microsoft-foundry.md)

### Commands & Environment Variables

- **`/fork` command updated**: The `/branch` command entry now notes that when `CLAUDE_CODE_FORK_SUBAGENT` is set, `/fork` is no longer an alias for `/branch` — it instead spawns a forked subagent.
  > "When `CLAUDE_CODE_FORK_SUBAGENT` is set, `/fork` instead spawns a forked subagent and is no longer an alias for this command"
  - *Implication*: Developers relying on `/fork` as a branch alias need to be aware of this behavioral shift when the env var is active.
  - *Source*: [commands.md](https://code.claude.com/docs/en/commands.md)

- **`CLAUDE_CODE_FORK_SUBAGENT` added to env-vars reference**: Full description added to the environment variables table documenting the fork subagent feature, its effect on `/fork`, and the constraint to interactive mode.
  - *Source*: [env-vars.md](https://code.claude.com/docs/en/env-vars.md)

### Release — v2.1.119 (April 23, 2026)

The changelog page gained 54 lines covering the v2.1.119 release. Key highlights from the entry:

- **`/config` settings persistence**: Theme, editor mode, verbose, etc. now persist to `~/.claude/settings.json` and participate in project/local/policy override precedence (previously session-only).
- **`prUrlTemplate` setting**: Points the footer PR badge at a custom code-review URL instead of github.com.
- **`CLAUDE_CODE_HIDE_CWD`**: New env var to hide the working directory in the startup logo.
- **`--from-pr` expanded**: Now accepts GitLab merge-request, Bitbucket pull-request, and GitHub Enterprise PR URLs in addition to github.com.
- **`--print` mode honors agent frontmatter**: `tools:` and `disallowedTools:` in agent definitions are now respected in non-interactive `--print` mode, matching interactive behavior.
- **`--agent <name>` honors `permissionMode`**: Built-in agents' `permissionMode` frontmatter field is now applied when invoked via `--agent`.
- **PowerShell auto-approval**: PowerShell tool commands can now be auto-approved in permission mode, matching existing Bash behavior.
- **Hooks `duration_ms`**: `PostToolUse` and `PostToolUseFailure` hook inputs now include `duration_ms` (tool execution time, excluding permission prompts and PreToolUse hooks).
- **Parallel MCP reconfiguration**: Subagent and SDK MCP server reconfiguration now connects servers in parallel instead of serially.
- **OpenTelemetry enhancements**: `tool_result` and `tool_decision` events now include `tool_use_id`; `tool_result` also includes `tool_input_size_bytes`.
- **Status line additions**: stdin JSON now includes `effort.level` and `thinking.enabled`.
- **Security fix**: `blockedMarketplaces` now correctly enforces `hostPattern` and `pathPattern` entries.
- **Vertex AI tool search disabled by default**: Tool search is now off by default on Vertex AI to avoid an unsupported beta header error (opt in with `ENABLE_TOOL_SEARCH`).
- **Numerous bug fixes**: Including CRLF paste issues, kitty keyboard protocol multi-line paste, Glob/Grep tools disappearing when Bash is denied, MCP OAuth errors, `${ENV_VAR}` substitution in MCP server headers, worktree stale reuse, `TaskList` ordering, and more.

*Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

## Notable Details

- The `ENABLE_PROMPT_CACHING_1H` env var is a new billing control point. The docs are explicit that 1-hour TTL writes cost more — developers using this on high-traffic deployments should monitor cache write costs.
- Fork mode explicitly notes that prompt cache is **shared** between the fork and the main session, which is unique behavior not present in named subagents (which have separate caches). This makes the feature particularly cost-efficient for context-heavy parallel tasks.
- The Vertex AI change silently clarifies that prompt caching no longer requires explicit `cache_control` ephemeral flag — it's now "enabled automatically", which may indicate a documentation catch-up to a behavior change that was already in place.
- The `/config` persistence change in v2.1.119 is noteworthy: settings configured interactively now round-trip through `settings.json` and the full precedence chain, meaning project-level policy can now override user theme/editor/verbose settings.
- `owner/repo#N` shorthand links in output now use the git remote's host (fixing a hardcoded github.com assumption), enabling correct links for GitHub Enterprise and other hosts.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| sub-agents.md | Modified | +56 / -0 | Added full "Fork the current conversation" section with UI controls, comparison table, and limitations |
| changelog.md | Modified | +54 / -0 | Added v2.1.119 release entry (April 23, 2026) with ~40 features and fixes |
| microsoft-foundry.md | Modified | +6 / -0 | Added prompt caching section documenting `ENABLE_PROMPT_CACHING_1H=1` |
| amazon-bedrock.md | Modified | +4 / -1 | Added `ENABLE_PROMPT_CACHING_1H=1` env var; updated billing note |
| google-vertex-ai.md | Modified | +4 / -1 | Added `ENABLE_PROMPT_CACHING_1H=1`; simplified caching description to "enabled automatically" |
| commands.md | Modified | +1 / -1 | Updated `/branch` entry to document `/fork` behavior change when `CLAUDE_CODE_FORK_SUBAGENT` is set |
| env-vars.md | Modified | +1 / -0 | Added `CLAUDE_CODE_FORK_SUBAGENT` to environment variables reference table |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-24*
