# Claude Code Documentation Changes — 2026-03-05

## Summary

16 documentation pages were modified in this update, corresponding to the Claude Code 2.1.69 release. The most significant changes are: a new `InstructionsLoaded` hook event, a new `/reload-plugins` command for hot-reloading plugins without restart, a new `git-subdir` plugin source type, fixed OAuth callback port support for MCP servers, and clarifications that system prompt file flags work in both interactive and print modes.

## Significant Changes

### Hooks

- **New `InstructionsLoaded` hook event**: A new lifecycle event fires whenever a `CLAUDE.md` or `.claude/rules/*.md` file is loaded into context — at session start for eager files and again when files are lazily loaded (nested directory traversal, path-glob matches, or `include` directives).
  > "Fires when a CLAUDE.md or .claude/rules/*.md file is loaded into context. This event fires at session start for eagerly-loaded files and again later when files are lazily loaded... The hook does not support blocking or decision control. It runs asynchronously for observability purposes."
  - Input schema includes `file_path`, `memory_type` (User/Project/Local/Managed), `load_reason` (`session_start`, `nested_traversal`, `path_glob_match`, `include`), `globs`, `trigger_file_path`, and `parent_file_path`.
  - Only `type: "command"` hooks are supported. `InstructionsLoaded` is in the no-matcher-support group — adding a `matcher` field is silently ignored.
  - *Implication*: Enables audit logging and compliance tracking for which instruction files load, when, and why — particularly useful for debugging path-specific or conditional rules.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **New `agent_id` and `agent_type` fields in hook common input**: When hooks fire inside a subagent or a session using `--agent`, two additional fields are now included in every hook's JSON input.
  > "`agent_id`: Unique identifier for the subagent. Present only when the hook fires inside a subagent call. Use this to distinguish subagent hook calls from main-thread calls. `agent_type`: Agent name (for example, 'Explore' or 'security-reviewer'). Present when the session uses `--agent` or the hook fires inside a subagent."
  - *Implication*: Hooks can now distinguish subagent-originated events from main-thread events, enabling more precise filtering and logging in multi-agent workflows.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **`TeammateIdle` and `TaskCompleted` hooks gain JSON decision control**: Previously these hooks only supported exit code 2 to signal a blocking condition. They now also accept a JSON response `{"continue": false, "stopReason": "..."}` to terminate the teammate entirely instead of cycling it back for another run.
  > "TeammateIdle hooks support two ways to control teammate behavior: Exit code 2: the teammate receives the stderr message as feedback and continues working instead of going idle. JSON `{"continue": false, "stopReason": "..."}`: stops the teammate entirely, matching Stop hook behavior. The stopReason is shown to the user."
  - The decision reference table row for these events changed from "Exit code only" to "Exit code or `continue: false`".
  - *Implication*: Hooks can now cleanly terminate teammates when a quality gate failure should be terminal rather than retriable.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **`SessionStart` restricted to `type: "command"` hooks**: The documentation now explicitly states that only command hooks are supported for the `SessionStart` event.
  > "SessionStart runs on every session, so keep these hooks fast. Only `type: 'command'` hooks are supported."
  - *Implication*: HTTP, prompt, and agent hook types on `SessionStart` are not supported. Review existing configurations if you've attempted to use those types here.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

### Plugins

- **New `/reload-plugins` command**: Plugins can now be hot-reloaded during an active session without restarting Claude Code.
  > "To activate all pending plugin changes without restarting, run `/reload-plugins`. Claude Code reloads all active plugins and reports what was loaded. If any LSP servers were added or updated, it will let you know those require a restart to take effect."
  - Commands, hooks, and most plugin changes take effect immediately; LSP server changes still require a full restart.
  - *Source*: [Discover plugins](https://code.claude.com/docs/en/discover-plugins.md)

- **New Security section for plugins**: A new top-level section explicitly documents the trust level required for plugins and marketplaces.
  > "Plugins and marketplaces are highly trusted components that can execute arbitrary code on your machine with your user privileges. Only install plugins and add marketplaces from sources you trust."
  - *Source*: [Discover plugins](https://code.claude.com/docs/en/discover-plugins.md)

- **New `git-subdir` plugin source type**: Plugin marketplaces can now reference plugins stored in a subdirectory of a git repository using a sparse, partial clone — minimizing bandwidth for monorepos.
  > "Use `git-subdir` to point to a plugin that lives inside a subdirectory of a git repository. Claude Code uses a sparse, partial clone to fetch only the subdirectory, minimizing bandwidth for large monorepos."
  - Fields: `url` (required; supports GitHub shorthand and SSH), `path` (required; subdirectory path), `ref` (optional branch/tag), `sha` (optional commit pin).
  - *Implication*: Organizations with monorepo structures can publish plugins without splitting them into separate repositories.
  - *Source*: [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

- **New `pathPattern` for `strictKnownMarketplaces`**: Administrators can now restrict filesystem-based marketplace sources using regex path patterns, in addition to the existing `hostPattern` for URL-based sources.
  > "Allow filesystem-based marketplaces from a specific directory using regex pattern matching on the path"
  ```json
  { "strictKnownMarketplaces": [{ "source": "pathPattern", "pathPattern": "^/opt/approved/" }] }
  ```
  - *Source*: [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

### MCP

- **Fixed OAuth callback port (`--callback-port`)**: MCP servers that require a pre-registered redirect URI can now use a fixed port instead of Claude Code's default random port selection.
  > "By default, Claude Code picks a random available port for the OAuth callback. Use `--callback-port` to fix the port so it matches a pre-registered redirect URI of the form `http://localhost:PORT/callback`. You can use `--callback-port` on its own (with dynamic client registration) or together with `--client-id` (with pre-configured credentials)."
  ```bash
  claude mcp add --transport http --callback-port 8080 my-server https://mcp.example.com/mcp
  ```
  - Also available via JSON config: `"oauth": {"callbackPort": 8080}` in `claude mcp add-json`.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

### CLI Reference

- **System prompt file flags now work in interactive mode**: The documentation previously stated `--system-prompt-file` and `--append-system-prompt-file` were print mode only. This restriction has been removed from the docs.
  > "Claude Code provides four flags for customizing the system prompt. All four work in both interactive and non-interactive modes."
  - The "Modes" column was removed from the flags comparison table, and example commands no longer require `-p`.
  - *Implication*: Developers can load system prompts from files in interactive sessions without using `claude -p`.
  - *Source*: [CLI reference](https://code.claude.com/docs/en/cli-reference.md)

### Remote Control

- **New `--name` flag for `remote-control`**: Custom session titles can now be set when starting a Remote Control session, making sessions identifiable by name in the claude.ai/code session list.
  > "`--name 'My Project'`: set a custom session title visible in the session list at claude.ai/code. You can also pass the name as a positional argument: `claude remote-control 'My Project'`"
  - Also available from within an existing session: `/remote-control My Project`.
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

### Skills

- **New `${CLAUDE_SKILL_DIR}` substitution variable**: Skills can now reference their own directory in `SKILL.md` content regardless of the current working directory.
  > "`${CLAUDE_SKILL_DIR}`: The directory containing the skill's `SKILL.md` file. For plugin skills, this is the skill's subdirectory within the plugin, not the plugin root. Use this in bash injection commands to reference scripts or files bundled with the skill, regardless of the current working directory."
  - *Implication*: Skills with bundled scripts can use `${CLAUDE_SKILL_DIR}/scripts/helper.sh` reliably instead of relying on a fixed working directory.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

- **New `/claude-api` bundled skill**: A new built-in skill loads Claude API and Anthropic SDK reference material for the project's language (Python, TypeScript, Java, Go, Ruby, C#, PHP, or cURL), and activates automatically when code imports `anthropic`, `@anthropic-ai/sdk`, or `claude_agent_sdk`.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

### Status Line

- **New worktree and agent fields in status line data**: Status line scripts now receive worktree context when running in a `--worktree` session, plus the active agent name.
  - New fields: `worktree.name`, `worktree.path`, `worktree.branch`, `worktree.original_cwd`, `worktree.original_branch` (all present only during `--worktree` sessions); `agent.name` (present when using `--agent`).
  - *Implication*: Status line scripts can surface which worktree is active, which branch it tracks, and where it originated — useful for parallel multi-worktree workflows.
  - *Source*: [Customize your status line](https://code.claude.com/docs/en/statusline.md)

### Permissions

- **Settings precedence expanded with explicit managed-settings note**: The permissions precedence section was rewritten as a numbered list and now explicitly states that managed settings override even command-line arguments.
  > "1. Managed settings: cannot be overridden by any other level, including command line arguments... If a tool is denied at any level, no other level can allow it. For example, a managed settings deny cannot be overridden by `--allowedTools`, and `--disallowedTools` can add restrictions beyond what managed settings define."
  - *Implication*: Confirms that `--allowedTools` cannot bypass managed policy denials — important for enterprise deployments relying on policy enforcement.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

### Interactive Mode

- **`Ctrl+U` exits bash mode on empty prompt**: In addition to `Escape` and `Backspace`, pressing `Ctrl+U` on an empty `!` prompt now exits bash mode.
  > "Exit with Escape, Backspace, or Ctrl+U on an empty prompt"
  - *Source*: [Interactive mode](https://code.claude.com/docs/en/interactive-mode.md)

### Model Configuration

- **Effort level visible in UI without opening `/model`**: The current effort level is now displayed next to the logo and spinner.
  > "The current effort level is also displayed next to the logo and spinner (for example, 'with low effort'), so you can confirm which setting is active without opening `/model`."
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

### Memory

- **Debugging tip cross-references `InstructionsLoaded` hook**: A new tip in the memory troubleshooting section directs users to the `InstructionsLoaded` hook for diagnosing which instruction files load and when.
  > "Use the `InstructionsLoaded` hook to log exactly which instruction files are loaded, when they load, and why. This is useful for debugging path-specific rules or lazy-loaded files in subdirectories."
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

## Notable Details

- The hooks lifecycle diagram image was updated to a new CDN asset (`rsuu-ovdPNos9Dnn` → `JWoaQLhotXStH4d2`). The alt text changed from "with WorktreeCreate and WorktreeRemove as standalone setup and teardown events" to "with WorktreeCreate, WorktreeRemove, and InstructionsLoaded as standalone async events" — signaling that `InstructionsLoaded` is now visually represented as a separate, async lifecycle point.
- The `strictKnownMarketplaces` description was refined from "using regex pattern matching" to "using regex pattern matching on the host" to distinguish the existing `hostPattern` from the newly added `pathPattern`.
- The 2.1.69 changelog notes that `--model claude-opus-4-0` and `--model claude-opus-4-1` were resolving to deprecated Opus versions — this has been fixed. Developers using pinned model aliases by number should retest their configurations.
- Sonnet 4.5 users on Pro/Max/Team Premium are being automatically migrated to Sonnet 4.6 per the 2.1.69 changelog.
- The 2.1.69 changelog confirms that `sandbox.enableWeakerNetworkIsolation` is a new macOS-only setting for allowing Go programs (e.g., `gh`, `gcloud`, `terraform`) to verify TLS certificates when using a custom MITM proxy with `httpProxyPort`. This setting is not yet in the main settings reference page.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| en_changelog.md | Modified | +105/-1 | Version 2.1.69 release notes added |
| en_hooks.md | Modified | +101/-45 | New `InstructionsLoaded` event, `agent_id`/`agent_type` fields, `TeammateIdle`/`TaskCompleted` JSON decision control, `SessionStart` command-only note |
| en_settings.md | Modified | +68/-64 | Settings documentation restructured |
| en_plugin-marketplaces.md | Modified | +64/-8 | New `git-subdir` source type, `pathPattern` for managed marketplace restrictions |
| en_mcp.md | Modified | +23/-0 | Fixed OAuth callback port (`--callback-port`) with dynamic or pre-configured credentials |
| en_hooks-guide.md | Modified | +20/-19 | Event table updated to include `InstructionsLoaded` |
| en_cli-reference.md | Modified | +15/-15 | System prompt flags work in all modes, "Modes" column removed from comparison table |
| en_discover-plugins.md | Modified | +16/-0 | `/reload-plugins` command section added, new Security section |
| en_statusline.md | Modified | +13/-0 | Worktree fields and `agent.name` added to available status line data |
| en_permissions.md | Modified | +9/-1 | Precedence rewritten as numbered list; managed settings override CLI args clarified |
| en_remote-control.md | Modified | +8/-5 | `--name` flag for custom session titles (CLI and `/remote-control` command) |
| en_skills.md | Modified | +8/-7 | `${CLAUDE_SKILL_DIR}` substitution variable, `/claude-api` bundled skill documented |
| en_memory.md | Modified | +4/-0 | Tip added pointing to `InstructionsLoaded` hook for debugging instruction file loading |
| en_interactive-mode.md | Modified | +2/-0 | `/reload-plugins` added to commands table; `Ctrl+U` added as bash mode exit method |
| en_model-config.md | Modified | +1/-1 | Effort level now shown next to logo/spinner |
| en_server-managed-settings.md | Modified | +1/-1 | Minor wording update |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-05*
