# Claude Code Documentation Changes — 2026-03-17

## Summary

Two pages were modified with no additions or removals. The primary change is the addition of release notes for Claude Code **v2.1.77** (March 17, 2026), a large release covering token limit increases, new commands, Agent SDK behavior changes, ~25 bug fixes, and performance improvements. A minor documentation correction was also made to the plugin marketplaces reference table.

---

## Significant Changes

### Release 2.1.77 — New Version Entry

The changelog received 47 new lines documenting the v2.1.77 release. Changes span token limits, new commands, Agent SDK behavior, security fixes, and performance.

#### Token Limit Increases

- **Higher output token limits for Opus 4.6 and Sonnet 4.6**: Default max output tokens for Claude Opus 4.6 raised to 64k; the upper bound for both Opus 4.6 and Sonnet 4.6 raised to 128k.
  > "Increased default maximum output token limits for Claude Opus 4.6 to 64k tokens, and the upper bound for Opus 4.6 and Sonnet 4.6 models to 128k tokens"
  - *Implication*: Agents and long-form tasks on these models can now produce significantly longer single responses without hitting output limits.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

#### New Features

- **`allowRead` sandbox filesystem setting**: A new `allowRead` option permits re-allowing read access within regions previously blocked by `denyRead`, enabling more granular sandbox configuration.
  > "Added `allowRead` sandbox filesystem setting to re-allow read access within `denyRead` regions"
  - *Implication*: Operators can now allow-list specific paths inside broader deny rules rather than choosing between full access or full denial.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`/copy` with optional index**: The `/copy` command now accepts an integer argument — `/copy N` copies the Nth-latest assistant response.
  > "`/copy` now accepts an optional index: `/copy N` copies the Nth-latest assistant response"
  - *Implication*: Easier retrieval of earlier responses in a session without scrolling.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`/fork` renamed to `/branch`**: The session-branching command is now `/branch`; `/fork` continues to work as an alias.
  > "Renamed `/fork` to `/branch` (`/fork` still works as an alias)"
  - *Implication*: Scripts or workflows using `/fork` continue to work, but `/branch` is now the canonical name going forward.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Sessions auto-named from plan content**: When a user accepts a plan, the session is now automatically named from the plan's heading or content.
  > "Sessions are now auto-named from plan content when you accept a plan"
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Background bash task output cap (5 GB)**: Background bash tasks are now killed when their output exceeds 5 GB, preventing runaway processes from filling disk.
  > "Background bash tasks are now killed if output exceeds 5GB, preventing runaway processes from filling disk"
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`apiKeyHelper` slow-response notice**: A notice is shown when `apiKeyHelper` takes longer than 10 seconds, surfacing what was previously a silent block on the main loop.
  > "Show a notice when `apiKeyHelper` takes longer than 10s, preventing it from blocking the main loop"
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

#### Agent SDK Behavior Changes

- **`Agent` tool drops `resume` parameter**: The `resume` parameter has been removed from the `Agent` tool. Continuing a previously spawned agent now requires `SendMessage({to: agentId})`.
  > "The Agent tool no longer accepts a `resume` parameter — use `SendMessage({to: agentId})` to continue a previously spawned agent"
  - *Implication*: Any agent code or prompts using `Agent({resume: ...})` must be updated. This is a breaking change for that pattern.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`SendMessage` auto-resumes stopped agents**: `SendMessage` now automatically resumes a stopped agent in the background rather than returning an error.
  > "`SendMessage` now auto-resumes stopped agents in the background instead of returning an error"
  - *Implication*: Multi-agent workflows become more resilient — callers no longer need to handle the stopped-agent error case explicitly.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

#### Performance Improvements

- **Faster macOS startup (~60 ms)**: Keychain credential reads now happen in parallel with module loading.
  > "Faster startup on macOS (~60ms) by reading keychain credentials in parallel with module loading"
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Faster `--resume` for large sessions**: Up to 45% faster loading and ~100–150 MB less peak memory on fork-heavy or very large sessions.
  > "Faster `--resume` on fork-heavy and very large sessions — up to 45% faster loading and ~100-150MB less peak memory"
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

#### Bug Fixes — Security & Correctness

- **`PreToolUse` hook `"allow"` bypassing deny rules (security fix)**: Returning `"allow"` from a `PreToolUse` hook could bypass `deny` permission rules, including enterprise managed settings. This is now corrected.
  > "Fixed PreToolUse hooks returning `\"allow\"` bypassing `deny` permission rules, including enterprise managed settings"
  - *Implication*: Hook authors relying on this bypass behavior must update their hooks. This affects enterprise policy enforcement.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`--resume` silently truncating conversation history**: A race condition between memory-extraction writes and the main transcript caused recent history to be dropped on resume.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` not stripping beta tool-schema fields**: Beta fields were leaking into requests, causing proxy gateways to reject them.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **"Always Allow" on compound bash commands**: Commands like `cd src && npm test` were saved as a single rule for the full string instead of per-subcommand, producing dead rules and repeated permission prompts.
  > "Fixed 'Always Allow' on compound bash commands (e.g. `cd src && npm test`) saving a single rule for the full string instead of per-subcommand, leading to dead rules and repeated permission prompts"
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **`git-subdir` plugin cache collision in monorepos**: Plugins at different subdirectories of the same monorepo commit were colliding in the shared plugin cache.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Claude Desktop using wrong API key (OAuth vs. CLI key)**: Desktop sessions were incorrectly using the terminal CLI's configured API key instead of OAuth credentials.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

#### Bug Fixes — UI & Terminal

- **Auto-updater memory accumulation**: Repeatedly opening and closing the slash-command overlay triggered overlapping binary downloads, accumulating tens of gigabytes of memory.
- **Write tool CRLF conversion**: Files with CRLF line endings were silently having their endings converted when overwritten or created in CRLF directories.
- **Clipboard copy in tmux**: Copy was silently failing; the copy toast now indicates whether to paste with `⌘V` or tmux `prefix+]`.
- **IDE integration not auto-connecting in tmux/screen**: Fixed failure to auto-connect when Claude Code is launched inside tmux or screen.
- **Hyperlinks opening twice**: Fixed double-open on Cmd+click in VS Code, Cursor, and other xterm.js-based terminals.
- **Vim mode**: Backspace and Delete not working in NORMAL mode; status line not updating when vim mode is toggled.
- **CJK character rendering**: Characters bleeding into adjacent UI elements when clipped at the right edge.
- **iTerm2**: Session crash when selecting text in tmux over SSH; auto mode not detecting iTerm2 for native split-pane teammates.
- **Ordered list numbers** not rendering in terminal UI.
- **Arrow keys switching tabs in dialogs**: `←`/`→` were accidentally switching tabs in settings, permissions, and sandbox dialogs while navigating lists.
- **Stale-worktree cleanup race condition**: Cleanup could delete an agent worktree just resumed from a previous crash.
- **Input deadlock**: Opening `/mcp` or similar dialogs while the agent is running could deadlock input.
- **Progress message memory growth**: Progress messages were surviving compaction in long-running sessions, causing memory growth over time.
- **Cost/token tracking in non-streaming mode**: Costs and token usage were not tracked when the API fell back to non-streaming mode.
- **Bash tool errors on paths with spaces**: The Bash tool was reporting errors for successful commands when the system temp directory path contained spaces.
- **Paste lost when typing immediately after pasting**.
- **Ctrl+D in `/feedback` input**: First press was deleting forward instead of the second press exiting the session.
- **0-byte image drag**: Dragging a 0-byte image file into the prompt caused an API error.
- **Teammate panes not closing** when the leader exits.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

#### CLI / Plugin Tooling

- **Improved `claude plugin validate`**: Now checks skill, agent, and command frontmatter plus `hooks/hooks.json`, catching YAML parse errors and schema violations in addition to basic structure.
  > "Improved `claude plugin validate` to check skill, agent, and command frontmatter plus `hooks/hooks.json`, catching YAML parse errors and schema violations"
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Headless plugin installation + `CLAUDE_CODE_PLUGIN_SEED_DIR`**: Headless mode plugin installation now correctly composes with the seed directory environment variable.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

- **Improved Esc to abort non-streaming API requests**: Esc now more reliably cancels in-flight non-streaming API calls.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

#### VS Code Integration

- **Plan preview tab titles use plan heading**: Tab titles for plan previews now use the plan's heading instead of the generic "Claude's Plan".
- **`macOptionClickForcesSelection` hint in footer**: When option+click doesn't trigger native selection on macOS, the footer now surfaces the relevant VS Code setting.
  - *Source*: [changelog.md](https://code.claude.com/docs/en/changelog.md)

---

### Plugin Marketplaces — `url` Source Field Correction

The plugin sources reference table was updated to remove a constraint stating that `url` source URLs must end in `.git`.

- **Before**: `url (must end .git)` in the Fields column for the `url` source type
- **After**: `url` — the `.git` suffix requirement is removed

  > "| `url` | object | `url`, `ref?`, `sha?` | Git URL source |"

  - *Implication*: The documentation now accurately reflects that git URL sources are not restricted to `.git`-suffixed URLs. Operators using non-`.git` URLs that were held back by this note can now proceed with confidence.
  - *Source*: [plugin-marketplaces.md](https://code.claude.com/docs/en/plugin-marketplaces.md)

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +47 / -0 | Added v2.1.77 release entry (March 17, 2026) with ~25 bug fixes, new features, and perf improvements |
| plugin-marketplaces.md | Modified | +8 / -8 | Table reformatting; removed erroneous `.git` suffix requirement from `url` plugin source field |

---

*Generated from Claude Code CLI documentation changes detected on 2026-03-17*
