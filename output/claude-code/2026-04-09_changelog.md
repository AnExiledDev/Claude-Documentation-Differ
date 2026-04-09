# Claude Code Documentation Changes — 2026-04-09

## Summary

Version 2.1.97 was released on April 8, 2026, bringing a new `/autofix-pr` command, status line improvements, and a large batch of bug fixes across permissions, MCP, `NO_FLICKER` mode, and session transcripts. Documentation was also updated to formally introduce Mobile as a supported platform, clarify the semantics of `allowed-tools` in skills, and expand troubleshooting guidance for Windows users.

## Significant Changes

### New Command: `/autofix-pr`

- **`/autofix-pr [prompt]` added to built-in commands**: This new command spawns a Claude Code on the web session that watches the current branch's open PR and pushes fixes when CI fails or reviewers leave comments.

  > Spawn a Claude Code on the web session that watches the current branch's PR and pushes fixes when CI fails or reviewers leave comments. Detects the open PR from your checked-out branch with `gh pr view`; to watch a different PR, check out its branch first. By default the remote session is told to fix every CI failure and review comment; pass a prompt to give it different instructions, for example `/autofix-pr only fix lint and type errors`. Requires the `gh` CLI and access to Claude Code on the web.

  - *Implication*: Developers can now trigger unattended PR remediation directly from the terminal without opening a browser. The optional `[prompt]` argument allows scoping fixes (e.g., lint-only). The `claude-code-on-the-web.md` page was also updated to list this as a way to enable auto-fix:
    > **From your terminal**: run `/autofix-pr` while on the PR's branch. Claude Code detects the open PR with `gh`, spawns a web session, and turns on auto-fix in one step
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md) | [Claude Code on the Web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

### Mobile Added as a Platform

- **Mobile platform formally documented in the platforms comparison table**: The platforms overview now lists Mobile as a distinct surface alongside CLI, Desktop, VS Code, JetBrains, and Web.

  > | Mobile | Starting and monitoring tasks while away from your computer | Cloud sessions from the Claude app for iOS and Android, Remote Control for local sessions, Dispatch to Desktop on Pro and Max |

  The prose summary was also updated:
  > Mobile is a thin client into those same cloud sessions or into a local session via Remote Control, and can send tasks to Desktop with Dispatch.

  - *Implication*: This is the first time Mobile has appeared in the platform comparison table. It clarifies Mobile's role as a session-starting and monitoring surface (not a full development environment) and calls out its three modes: cloud sessions, Remote Control for local sessions, and Dispatch to Desktop.
  - *Source*: [Platforms and Integrations](https://code.claude.com/docs/en/platforms.md)

### Skills: `allowed-tools` Semantics Clarified, Content Lifecycle Documented

- **"Restrict tool access" section replaced by two new sections**: The prior section used `allowed-tools` as a tool restriction mechanism (the example showed a `safe-reader` skill). The documentation now corrects this and restructures the content into two distinct sections.

  **New section — "Skill content lifecycle":**
  > When you or Claude invoke a skill, the rendered `SKILL.md` content enters the conversation as a single message and stays there for the rest of the session. Claude Code does not re-read the skill file on later turns, so write guidance that should apply throughout a task as standing instructions rather than one-time steps.
  >
  > Auto-compaction preserves invoked skills. When the conversation is summarized to free context, Claude Code re-attaches the most recent invocation of each skill after the summary (truncated if the skill is very large). If you invoke the same skill more than once, only the latest copy is carried forward through compaction.

  **New section — "Pre-approve tools for a skill":**
  > The `allowed-tools` field grants permission for the listed tools while the skill is active, so Claude can use them without prompting you for approval. It does not restrict which tools are available: every tool remains callable, and your permission settings still govern tools that are not listed.
  >
  > To block a skill from using certain tools, add deny rules in your permission settings instead.

  The example was changed from a read-only `safe-reader` skill to a `commit` skill that pre-approves specific git Bash commands:
  ```yaml
  name: commit
  description: Stage and commit the current changes
  disable-model-invocation: true
  allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
  ```

  - *Implication*: This is a semantic correction — `allowed-tools` never restricted tool access; it granted pre-approval. Developers who were using `allowed-tools` expecting it to prevent tool use should instead configure deny rules in permission settings.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

### Status Line: `refreshInterval`, `workspace.git_worktree`, and `FORCE_HYPERLINK`

- **`refreshInterval` setting and `workspace.git_worktree` field added** (v2.1.97): The status line now supports periodic refresh and exposes git worktree context:

  > Added `refreshInterval` status line setting to re-run the status line command every N seconds
  > Added `workspace.git_worktree` to the status line JSON input, set when the current directory is inside a linked git worktree

  The mock input test example in the docs was updated to reflect these additions:
  > `echo '{"model":{"display_name":"Opus"},"workspace":{"current_dir":"/home/user/project"},"context_window":{"used_percentage":25},"session_id":"test-session-abc"}' | ./statusline.sh`

  - *Implication*: The `workspace` and `session_id` fields are now part of the standard status line JSON schema. Scripts that read these inputs should handle the new fields.

- **`FORCE_HYPERLINK` workaround documented for Windows Terminal**: A new troubleshooting entry explains how to override OSC 8 hyperlink auto-detection when link text appears but isn't clickable:

  > If link text appears but isn't clickable, Claude Code may not have detected hyperlink support in your terminal. This commonly affects Windows Terminal and other emulators not in the auto-detection list. Set the `FORCE_HYPERLINK` environment variable to override detection before launching Claude Code.

  Both Bash (`FORCE_HYPERLINK=1 claude`) and PowerShell (`$env:FORCE_HYPERLINK = "1"; claude`) forms are provided.

  - *Source*: [Status Line](https://code.claude.com/docs/en/statusline.md)

### Troubleshooting: Windows Certificate Revocation Error

- **New workaround for `CRYPT_E_REVOCATION_OFFLINE` on Windows**: Added as step 4 in the TLS certificate error section:

  > On Windows, bypass certificate revocation checks if you see `CRYPT_E_REVOCATION_OFFLINE (0x80092013)`. This means curl reached the server but your network blocks the certificate revocation lookup, which is common behind corporate firewalls. Add `--ssl-revoke-best-effort` to the install command.

  The `winget install Anthropic.ClaudeCode` alternative is called out as a way to avoid curl entirely.

  - *Implication*: This addresses a common corporate network install failure that would previously require manual diagnosis.
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

### Version 2.1.97 Release Notes

The official changelog entry for 2.1.97 (April 8, 2026) covers a large set of fixes and improvements. Key items by category:

**NO_FLICKER mode fixes:**
- Focus view toggle (`Ctrl+O`) added, showing prompt, one-line tool summary with edit diffstats, and final response
- Fixed copying wrapped URLs inserting spaces at line breaks
- Fixed scroll rendering artifacts inside zellij
- Fixed crash when hovering over MCP tool results
- Fixed memory leak from API retries leaving stale streaming state
- Fixed slow mouse-wheel scrolling on Windows Terminal
- Fixed custom status line not displaying on terminals shorter than 24 rows
- Fixed Shift+Enter and Alt/Cmd+arrow shortcuts in Warp
- Fixed Korean/Japanese/Unicode text becoming garbled when copied on Windows

**Permissions and security fixes:**
- Fixed `--dangerously-skip-permissions` being silently downgraded to accept-edits mode after approving a write to a protected path
- Fixed and hardened Bash tool permissions (env-var prefix and network redirect checks)
- Fixed permission rules with names matching JavaScript prototype properties (e.g. `toString`) causing `settings.json` to be silently ignored
- Fixed managed-settings allow rules remaining active after admin removal until process restart
- Fixed `permissions.additionalDirectories` changes not applying mid-session
- Fixed removing a directory from `settings.permissions.additionalDirectories` revoking access to the same directory passed via `--add-dir`

**MCP fixes:**
- Fixed HTTP/SSE connections accumulating ~50 MB/hr of unreleased buffers on reconnect
- Fixed OAuth `oauth.authServerMetadataUrl` not being honored on token refresh after restart (affects ADFS and similar IdPs)

**Session and transcript fixes:**
- Fixed several `/resume` picker issues (uneditable sessions, Ctrl+A wiping search, empty list navigation, task status replacing conversation summary, cross-project staleness)
- Fixed file-edit diffs disappearing on `--resume` when the edited file was larger than 10KB
- Fixed `--resume` cache misses and lost mid-turn input
- Fixed messages typed while Claude is working not being persisted to the transcript
- Fixed compaction writing duplicate multi-MB subagent transcript files on prompt-too-long retries

**Other improvements:**
- Accept Edits mode now auto-approves filesystem commands prefixed with safe env vars or process wrappers (e.g. `LANG=C rm foo`, `timeout 5 mkdir out`)
- Auto mode and bypass-permissions mode now auto-approve sandbox network access prompts
- `sandbox.network.allowMachLookup` now takes effect on macOS
- Pasted and attached images are now compressed to the same token budget as images read via the Read tool
- Slash command and `@`-mention completion now triggers after CJK sentence punctuation (no space needed before `/` or `@` in Japanese/Chinese input)
- Bridge sessions now show local git repo, branch, and working directory on the claude.ai session card
- 429 retries now apply exponential backoff as a minimum when `Retry-After` is very small
- Fixed rate-limit upgrade options disappearing after context compaction
- Fixed `claude plugin update` reporting "already at the latest version" for git-based marketplace plugins with newer remote commits
- Fixed slash command picker breaking when a plugin's frontmatter `name` is a YAML boolean keyword
- Updated `/claude-api` skill to cover Managed Agents alongside the Claude API

- *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

## Notable Details

- The `/claude-api` skill description was updated: it previously mentioned "Agent SDK reference for Python and TypeScript" and auto-activation on `claude_agent_sdk` imports. The new description drops the `claude_agent_sdk` import trigger and instead lists "Managed Agents" as a topic area. This aligns with the v2.1.97 note: "Updated `/claude-api` skill to cover Managed Agents alongside the Claude API."
- The `platforms.md` description now explicitly calls out Mobile in its tagline (was: "CLI, Desktop, VS Code, JetBrains, web, and integrations"; now: "CLI, Desktop, VS Code, JetBrains, web, **mobile**, and integrations").
- The `allowed-tools` semantic correction in skills.md is significant: the previous example (`safe-reader`) incorrectly implied `allowed-tools` was a restriction mechanism. The replacement example (`commit`) correctly demonstrates it as a pre-approval list. This is a documentation accuracy fix, not a behavior change.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| changelog.md | Modified | +49/-0 | Added v2.1.97 release entry with 40+ fixes and improvements |
| commands.md | Modified | +72/-71 | Added `/autofix-pr` command; table column width reformatting |
| skills.md | Modified | +19/-6 | Replaced "Restrict tool access" with "Skill content lifecycle" and "Pre-approve tools for a skill"; corrected `allowed-tools` semantics |
| statusline.md | Modified | +16/-1 | Updated mock input example; added `FORCE_HYPERLINK` OSC 8 troubleshooting guidance |
| platforms.md | Modified | +11/-9 | Added Mobile as a platform row and updated prose; added mobile to further reading links |
| troubleshooting.md | Modified | +6/-0 | Added Windows `CRYPT_E_REVOCATION_OFFLINE` certificate revocation workaround |
| claude-code-on-the-web.md | Modified | +1/-0 | Added `/autofix-pr` as a terminal-based way to enable PR auto-fix |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-09*
