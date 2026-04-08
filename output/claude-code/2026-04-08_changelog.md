# Claude Code Documentation Changes — 2026-04-08

## Summary

This update splits the Claude Code on the web documentation into a new dedicated quickstart (`web-quickstart.md`) and a restructured reference page. A new `CCR_FORCE_BUNDLE` environment variable enables cloud sessions for non-GitHub repositories. Version 2.1.96 shipped a fix for a Bedrock authentication regression. Smaller additions include a troubleshooting entry for auto-compaction thrashing, a corrected status line cache pattern, and two previously undocumented commands (`/teleport`, `/web-setup`) added to the command reference.

---

## Significant Changes

### Web Features

- **New web quickstart page**: A dedicated getting-started guide for Claude Code on the web replaces what was previously buried inside the main reference page. It walks through connecting GitHub, creating a cloud environment, submitting tasks, and reviewing diffs — including a comparison table of all four execution surfaces (On the web / Remote Control / Terminal CLI / Desktop app) and a troubleshooting section for common setup failures.
  > "Run Claude Code in the cloud from your browser or phone. Connect a GitHub repository, submit a task, and review the PR without local setup."
  - *Implication*: Operators and teams should link to `/en/web-quickstart` for onboarding; the existing `claude-code-on-the-web` page is now a reference for advanced configuration.
  - *Source*: [Get started with Claude Code on the web](https://code.claude.com/docs/en/web-quickstart.md)

- **Web reference page major restructure**: `claude-code-on-the-web.md` was reorganized around reference rather than onboarding. Key structural additions:
  - **"GitHub authentication options"** — new table comparing GitHub App (per-repo authorization) vs `/web-setup` (`gh` CLI token sync).
  - **"What's available in cloud sessions"** — explicit table listing which repo-committed config carries over (`.claude/skills/`, `.mcp.json`, repo hooks) vs what does not (user `~/.claude/CLAUDE.md`, user-level MCP servers added via `claude mcp add`, API tokens, AWS SSO).
  - **"Resource limits"** — cloud sessions now document explicit ceilings: 4 vCPUs, 16 GB RAM, 30 GB disk.
  - **"Allow specific domains"** — new section covering Custom network access, including `*.` wildcard subdomain syntax.
  - **Removed sections**: "What is Claude Code on the web?", "Who can use it?", "Best practices", "Pricing and rate limits" (now folded into Limitations), and per-category domain lists (collapsed into accordions).
  > "Cloud sessions start from a fresh clone of your repository. Anything committed to the repo is available. Anything you've installed or configured only on your own machine is not."
  - *Implication*: Old section anchors are broken. `#cloud-environment` → `#the-cloud-environment`, `#managing-sessions` → `#work-with-sessions`, `#deleting-sessions` → `#delete-sessions`, `#requirements-for-teleporting` → `#teleport-requirements`.
  - *Source*: [Use Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

- **Send local repositories without GitHub**: `claude --remote` now automatically bundles and uploads a local repository when GitHub access isn't configured. A new `CCR_FORCE_BUNDLE=1` environment variable forces this path even when GitHub is available.
  > "When you run `claude --remote` from a repository that isn't connected to GitHub, Claude Code bundles your local repository and uploads it directly to the cloud session. The bundle includes your full repository history across all branches, plus any uncommitted changes to tracked files."
  Limits: repository under 100 MB; untracked files not included; sessions created from a bundle can't push back to a remote without GitHub auth.
  - *Implication*: Teams on GitLab, Bitbucket, or local-only repos can now use `--remote` cloud sessions for read/analyze workflows, with the trade-off that push-back requires GitHub.
  - *Source*: [Use Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

- **`--remote` behavior clarified**: The documentation now explicitly states that `--remote` clones from GitHub at your current branch — local commits not yet pushed to GitHub won't be visible in the VM. Also clarified that `--remote` and `--remote-control` are unrelated:
  > "`--remote` creates cloud sessions. `--remote-control` is unrelated: it exposes a local CLI session for monitoring from the web."
  - *Source*: [Use Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

- **Cloud context management documented**: A new "Manage context" subsection documents which commands work inside cloud sessions. `/compact` (with optional focus) and `/context` work; `/clear` does not (start a new session from the sidebar instead). Also documents `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` and `CLAUDE_CODE_AUTO_COMPACT_WINDOW` for tuning compaction in cloud environments.
  - *Source*: [Use Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

- **`--teleport` vs `/teleport` distinguished**: The "From web to terminal" section now documents both the CLI flag and the in-session command, and explicitly distinguishes teleport from resume:
  > "`--teleport` is distinct from `--resume`. `--resume` reopens a conversation from this machine's local history and doesn't list cloud sessions; `--teleport` pulls a cloud session and its branch."
  A new subsection also explains when teleport is unavailable: API key, Bedrock, Vertex AI, and Microsoft Foundry users cannot teleport because it requires a claude.ai subscription.
  - *Source*: [Use Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

---

### Bug Fixes & Release Notes

- **Version 2.1.96 — Bedrock auth regression fix**: A regression introduced in 2.1.94 caused Bedrock requests to fail with `403 "Authorization header is missing"` when using `AWS_BEARER_TOKEN_BEDROCK` or `CLAUDE_CODE_SKIP_BEDROCK_AUTH`. This is now fixed.
  > "Fixed Bedrock requests failing with `403 \"Authorization header is missing\"` when using `AWS_BEARER_TOKEN_BEDROCK` or `CLAUDE_CODE_SKIP_BEDROCK_AUTH` (regression in 2.1.94)"
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

### Troubleshooting

- **New: Auto-compaction thrashing error**: A new troubleshooting entry covers the case where a file or tool output immediately refills the context window after compaction, causing Claude Code to stop retrying to avoid infinite API loops.
  > "If you see `Autocompact is thrashing: the context refilled to the limit...`, automatic compaction succeeded but a file or tool output immediately refilled the context window several times in a row. Claude Code stops retrying to avoid wasting API calls on a loop that isn't making progress."
  Recovery options: read the oversized file in smaller chunks, run `/compact` with a focus to drop the large output, delegate large-file work to a subagent, or run `/clear` if the earlier conversation is no longer needed.
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

---

### Configuration & Settings

- **MCP scopes: "Choosing the right scope" section replaced with summary table**: The verbose prose section was replaced with a concise table and clarified descriptions for each scope. An example JSON block now shows exactly what `~/.claude.json` looks like after adding a local-scoped server.

  | Scope | Loads in | Shared with team | Stored in |
  |---|---|---|---|
  | Local | Current project only | No | `~/.claude.json` |
  | Project | Current project only | Yes, via version control | `.mcp.json` in project root |
  | User | All your projects | No | `~/.claude.json` |

  - *Source*: [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp.md)

- **Desktop local environment editor for secrets**: The `env` field documentation in `launch.json` now points to the desktop's **local environment editor** (gear icon in the prompt box dropdown) for managing dev server secrets. Previously the docs said to use the shell profile.
  > "To pass secrets to your dev server, set them in the [local environment editor](#local-sessions) instead."
  The local environment editor stores variables encrypted on disk and applies them to both Claude sessions and preview servers.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Desktop `MAX_THINKING_TOKENS` clarification**: On Opus 4.6 and Sonnet 4.6, any `MAX_THINKING_TOKENS` value other than `0` is ignored due to adaptive reasoning. To use a fixed thinking budget on these models, also set `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. The variable should now be set in the local environment editor, not the shell profile.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Desktop plan mode description corrected**: Plan mode was previously described as "analyzes your code and creates a plan without modifying files or running commands." It now reads "reads files and runs commands to explore, then proposes a plan without editing your source code" — acknowledging that read-only commands (like `npm test --dry-run`) can run in plan mode.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **`CLAUDE_CONFIG_DIR` noted in directory reference**: The `.claude` directory page now states that when `CLAUDE_CONFIG_DIR` is set, every `~/.claude` path documented on that page lives under that directory instead.
  - *Source*: [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory.md)

- **New env var `CCR_FORCE_BUNDLE`**: Set to `1` to force `claude --remote` to bundle and upload the local repository even when GitHub access is available.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **Hardware requirements updated**: Setup page now specifies x64 or ARM64 processor alongside the existing 4 GB+ RAM requirement.
  - *Source*: [Setup](https://code.claude.com/docs/en/setup.md)

---

### Commands

- **`/teleport` and `/web-setup` added to command reference**: Both commands were previously absent from the built-in commands table.
  - `/teleport`: "Pull a Claude Code on the web session into this terminal: opens a picker, then fetches the branch and conversation. Also available as `/tp`. Requires a claude.ai subscription."
  - `/web-setup`: "Connect your GitHub account to Claude Code on the web using your local `gh` CLI credentials. `/schedule` prompts for this automatically if GitHub isn't connected."
  - *Source*: [Built-in commands](https://code.claude.com/docs/en/commands.md)

---

### Status Line

- **Cache file naming fix for concurrent sessions**: The caching example in the status line docs was updated to derive the cache filename from `session_id` (from the JSON input) rather than a fixed path. The previous approach caused concurrent sessions in different repositories to share stale git state.
  > "The cache filename needs to be stable across status line invocations within a session, but unique across sessions so concurrent sessions in different repositories don't read each other's cached git state. Process-based identifiers like `$$`, `os.getpid()`, or `process.pid` change on every invocation and defeat the cache. Use the `session_id` from the JSON input instead."
  Cache file is now `/tmp/statusline-git-cache-$SESSION_ID` across all three language examples (Bash, Python, Node.js).
  - *Source*: [Customize your status line](https://code.claude.com/docs/en/statusline.md)

---

### Skills

- **Argument quoting behavior documented**: The skills reference now notes that indexed arguments use shell-style quoting.
  > "Indexed arguments use shell-style quoting, so wrap multi-word values in quotes to pass them as a single argument. For example, `/my-skill \"hello world\" second` makes `$0` expand to `hello world` and `$1` to `second`. The `$ARGUMENTS` placeholder always expands to the full argument string as typed."
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

---

### Authentication

- **Browser login code fallback documented**: The authentication page now documents that if the browser shows a login code instead of redirecting back after sign-in, users should paste it into the terminal at the `Paste code here if prompted` prompt.
  - *Source*: [Authentication](https://code.claude.com/docs/en/authentication.md)

---

## New Pages

- **[web-quickstart.md](https://code.claude.com/docs/en/web-quickstart.md)** — Step-by-step guide to getting started with Claude Code on the web: connecting GitHub (browser and terminal paths), creating cloud environments, submitting tasks, reviewing diffs, and creating PRs. Includes a surface comparison table and setup troubleshooting.

---

## Notable Details

- **Agent SDK links switched to relative paths**: Multiple pages (`headless.md`, `github-actions.md`, `gitlab-ci-cd.md`, `legal-and-compliance.md`, `cli-reference.md`, `overview.md`) updated Agent SDK references from `platform.claude.com/docs/en/agent-sdk/...` to relative `/en/agent-sdk/...`, indicating the Agent SDK docs are now co-hosted under the Claude Code documentation domain.

- **Devcontainer first-run instructions added**: `devcontainer.md` now includes a post-build step: open a terminal with `` Ctrl+` `` and run `claude` to authenticate. Small addition that addresses a common first-run gap.

- **`.claude` directory cleanup tables expanded**: The "Kept until you delete them" table (formerly "Not swept") now explicitly includes `stats-cache.json` and `backups/` as items to consider clearing, while `statsig/` and `downloads/` were removed from that list. The `debug/` directory entry now clarifies it is only written when `--debug` or `/debug` is active.

- **Default allowed domains updated**: The new `claude-code-on-the-web.md` adds several domains to the Trusted allowlist that were absent before: `docs.claude.com` (Anthropic services), `downloads.sentry-cdn.com` and `api.honeycomb.io` (cloud monitoring), `fonts.googleapis.com` and `fonts.gstatic.com` (content delivery), `pkg.stainless.com` and `binaries.prisma.sh` (development tools), and `repo.maven.apache.org` and `kotlinlang.org` (JVM package managers).

- **Slack prerequisites updated**: The requirements table now lists "premium seats or Chat + Claude Code seats" for Enterprise, where previously only "premium seats" appeared.

- **`cleanupPeriodDays` wording clarified**: The settings reference changed "Sessions inactive for longer than this period" to "Session files older than this period" — a small but more accurate description of what gets cleaned up.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| web-quickstart.md | New | +203 | New getting-started guide for Claude Code on the web |
| claude-code-on-the-web.md | Modified | +575/-547 | Major restructure: new quickstart split out, resource limits, local bundle support, context management, network access overhaul |
| claude-directory.md | Modified | +31/-28 | Renamed cleanup sections; CLAUDE_CONFIG_DIR note; expanded clear-data table |
| mcp.md | Modified | +25/-18 | Replaced "Choosing the right scope" section with summary table and JSON example |
| desktop.md | Modified | +18/-16 | Local environment editor for secrets; MAX_THINKING_TOKENS clarification; plan mode description fix |
| troubleshooting.md | Modified | +11/-0 | New: auto-compaction thrashing error and recovery steps |
| statusline.md | Modified | +7/-4 | Cache file naming fix: use session_id for concurrent-session safety |
| web-scheduled-tasks.md | Modified | +7/-5 | Minor wording and link anchor updates |
| slack.md | Modified | +7/-7 | Updated prerequisites (Chat + Claude Code seats); fixed sharing link anchor |
| overview.md | Modified | +8/-8 | Agent SDK links made relative; web onboarding link updated to web-quickstart |
| commands.md | Modified | +3/-1 | Added /teleport and /web-setup; fixed /remote-env anchor |
| setup.md | Modified | +6/-6 | Added ARM64 processor requirement; code block formatting |
| headless.md | Modified | +4/-4 | Agent SDK links made relative |
| changelog.md | Modified | +4/-0 | Version 2.1.96: Bedrock auth regression fix |
| cli-reference.md | Modified | +3/-3 | Agent SDK and structured-outputs links made relative |
| how-claude-code-works.md | Modified | +2/-0 | Link to new thrashing error troubleshooting entry |
| devcontainer.md | Modified | +2/-0 | First-run instructions added after container build |
| skills.md | Modified | +2/-0 | Shell-style quoting behavior for indexed arguments |
| authentication.md | Modified | +2/-0 | Browser login code fallback note |
| github-enterprise-server.md | Modified | +2/-2 | /teleport → --teleport; updated teleport requirements anchor |
| data-usage.md | Modified | +2/-2 | Session deletion link updated to new anchor |
| env-vars.md | Modified | +1/-0 | Added CCR_FORCE_BUNDLE variable |
| settings.md | Modified | +1/-1 | Clarified cleanupPeriodDays description |
| ultraplan.md | Modified | +2/-2 | Updated cloud-environment anchor links |
| fast-mode.md | Modified | +1/-1 | "extra usage credits" → "extra usage" |
| github-actions.md | Modified | +1/-1 | Agent SDK link made relative |
| gitlab-ci-cd.md | Modified | +1/-1 | Agent SDK link made relative |
| legal-and-compliance.md | Modified | +1/-1 | Agent SDK link made relative |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-08*
