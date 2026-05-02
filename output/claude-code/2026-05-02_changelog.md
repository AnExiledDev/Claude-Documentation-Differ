# Claude Code Documentation Changes — 2026-05-02

## Summary

One new page documents the `claude-cli://` deep link feature for opening pre-filled Claude Code sessions from URLs. Alongside this, the VS Code extension gained a parallel URI handler for opening editor tabs. Several existing pages received substantial additions: plan mode got dedicated approval-flow documentation, model configuration gained a new `ultrathink` keyword section, headless mode gained scripting examples, and hooks-guide gained an auto-approval pattern for `PermissionRequest`. The largest single change is a near-total rewrite of `common-workflows.md`, which sheds ~600 lines of content that was migrated to dedicated pages (worktrees, sessions, permission-modes, headless) and now acts as a concise index page.

---

## Significant Changes

### Features

- **Deep links (`claude-cli://` URL scheme)**: A new page documents how to launch Claude Code sessions from clickable URLs, shell scripts, and browser integrations. Links carry a working directory (`cwd`) and a pre-filled prompt (`q`) or a GitHub repo slug (`repo`) that resolves to the most-recently-used local clone.
  > "A deep link is a `claude-cli://` URL that opens Claude Code in a new terminal window. The URL can carry a working directory and a prompt to pre-fill."
  > "The prompt is populated but not sent until you press Enter."
  - Parameters: `q` (up to 5,000 chars, URL-encoded), `cwd` (absolute path), `repo` (GitHub `owner/name` slug). `cwd` takes precedence over `repo` when both are supplied.
  - Requires Claude Code **v2.1.91 or later**.
  - Handler is registered automatically on first interactive session; to suppress, set `disableDeepLinkRegistration: "disable"` in `settings.json`.
  - Supported terminal emulators documented per OS: iTerm2/Ghostty/kitty/Alacritty/WezTerm/Terminal.app on macOS; `$TERMINAL` / `x-terminal-emulator` on Linux; Windows Terminal / PowerShell / `cmd.exe` on Windows.
  - *Implication*: Runbooks, alerts, and wiki pages can now embed one-click investigation links into any repo, as long as the platform renders `claude-cli://` scheme links (GitHub-rendered Markdown strips non-HTTP schemes — the workaround is a code block).
  - *Source*: [Launch sessions from links](https://code.claude.com/docs/en/deep-links.md)

- **VS Code tab URI handler**: The VS Code extension now documents a `vscode://anthropic.claude-code/open` URI handler that opens a new Claude Code editor tab, with optional `prompt` (pre-fill text) and `session` (ID to resume) query parameters. Platform invocation examples for macOS, Linux, and Windows are included.
  > "Use it to open a new Claude Code tab from your own tooling: a shell alias, a browser bookmarklet, or any script that can open a URL."
  - *Implication*: Complements the CLI's `claude-cli://` handler — use `vscode://` to open a graphical editor tab, `claude-cli://` to open a terminal session.
  - *Source*: [Use Claude Code in VS Code](https://code.claude.com/docs/en/vs-code.md)

- **`ultrathink` keyword**: Model configuration documents a new in-prompt keyword that requests deeper reasoning on a single turn without changing the session effort level.
  > "Include `ultrathink` anywhere in your prompt to request deeper reasoning on that turn without changing your session effort setting. Claude Code recognizes the keyword and adds an in-context instruction. The effort level sent to the API is unchanged."
  - Other phrases ("think", "think hard", "think more") are explicitly noted as **not** recognized as keywords — they pass through as ordinary text.
  - *Implication*: Provides a lightweight way to get deeper reasoning on a single prompt without a persistent effort change or `/effort` command.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

- **Extended thinking controls table**: A new "Extended thinking" section in `model-config.md` consolidates the controls for toggling thinking per session, setting the global default, and disabling it entirely.
  > | Control | How to set it |
  > |---|---|
  > | Toggle for the current session | Press `Option+T` on macOS or `Alt+T` on Windows and Linux |
  > | Set the global default | Run `/config` and toggle thinking mode. Saved as `alwaysThinkingEnabled` in `~/.claude/settings.json` |
  > | Disable regardless of effort | Set `MAX_THINKING_TOKENS=0` |
  - *Implication*: Previously scattered across settings and environment-variable references; now one authoritative location.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

### Configuration

- **Plan mode approval flow**: `permission-modes.md` gained two subsections describing what happens after Claude presents a plan.
  > "From that prompt you can: Approve and start in auto mode / Approve and accept edits / Approve and review each edit manually / Keep planning with feedback / Refine with Ultraplan for browser-based review."
  - `Ctrl+G` opens the proposed plan in the default text editor for inline edits before Claude proceeds.
  - When `showClearContextOnPlanAccept` is enabled, each approve option also offers to clear planning context first.
  - The new "Set plan mode as the default" subsection shows the `permissions.defaultMode: "plan"` setting in `.claude/settings.json`.
  - *Implication*: The approval flow was previously undocumented in the reference; developers relying on plan mode now have a complete description of the handoff options.
  - *Source*: [Choose a permission mode](https://code.claude.com/docs/en/permission-modes.md)

- **Hooks: auto-approve `PermissionRequest`**: `hooks-guide.md` gained a new "Auto-approve specific permission prompts" section with a working example that auto-approves `ExitPlanMode` by returning `{"hookSpecificOutput": {"hookEventName": "PermissionRequest", "decision": {"behavior": "allow"}}}`. Also documents the `updatedPermissions` / `setMode` field for switching permission mode at approval time.
  - *Implication*: Enables automation where plan-mode approval is handled programmatically, without manual `Enter` per plan.
  - *Source*: [Automate workflows with hooks](https://code.claude.com/docs/en/hooks-guide.md)

### Documentation Restructuring

- **`common-workflows.md` near-rewrite (+85/−589 lines)**: The page shed the bulk of its content — previously migrated to dedicated pages — and is now a concise recipe index.
  - Removed sections: "Use Plan Mode for safe code analysis" (→ `permission-modes.md`), "Run parallel Claude Code sessions with Git worktrees" (→ `/en/worktrees`), "Name your sessions" / "Use the session picker" (→ `/en/sessions`), "Use extended thinking" (→ `model-config.md`), "Use specialized subagents" (→ `sub-agents.md`), "Get notified when Claude needs your attention" (→ `hooks-guide.md`).
  - Added "Prompt recipes" grouping for the everyday-task sections (codebase overview, bugs, refactoring, tests, PRs, docs, images, file references).
  - "Run Claude on a schedule" now shows a comparison table of scheduling options (Routines, Desktop, GitHub Actions, `/loop`) rather than step-by-step instructions.
  - Remaining workflow sections ("Resume previous conversations", "Run parallel sessions with worktrees", "Plan before editing", "Delegate research to subagents", "Pipe Claude into scripts") are now one-paragraph overviews with links to the canonical pages.
  - *Implication*: The page is now an entry point, not a feature reference. Cross-links to dedicated pages are authoritative for each topic.
  - *Source*: [Common workflows](https://code.claude.com/docs/en/common-workflows.md)

- **`headless.md` scripting examples added**: Two new examples under the "Examples" section:
  - "Pipe data through Claude" — `cat build-error.txt | claude -p '...' > output.txt`, noting that `--output-format json` adds cost metadata per invocation.
  - "Add Claude to a build script" — a `package.json` script that pipes `git diff main` into Claude as a typo linter, using escaped double quotes for Windows portability.
  - *Source*: [Run Claude Code programmatically](https://code.claude.com/docs/en/headless.md)

### Naming and Terminology

- **"AWS Bedrock" → "Amazon Bedrock"**: Section headers and inline text updated to the official product name across `github-actions.md`, `gitlab-ci-cd.md`, `code-review.md`, `costs.md`, and `remote-control.md`.
  - *Source*: [GitHub Actions](https://code.claude.com/docs/en/github-actions.md), [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd.md)

- **"Plan Mode" → "plan mode"**: `best-practices.md` lowercased "Plan Mode" to "plan mode" throughout — title, code fence labels (`(plan mode)`, `(default mode)`), and inline references. The link target also moved from `common-workflows#use-plan-mode-for-safe-code-analysis` to `permission-modes#analyze-before-you-edit-with-plan-mode`.
  - *Source*: [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices.md)

- **Internal link migrations**: Multiple pages updated links away from `common-workflows` anchors to the dedicated pages that now own those topics:
  - `common-workflows#run-parallel-claude-code-sessions-with-git-worktrees` → `/en/worktrees` (agent-teams.md, cli-reference.md, commands.md)
  - `common-workflows#copy-gitignored-files-to-worktrees` → `/en/worktrees#copy-gitignored-files-into-worktrees` (claude-directory.md)
  - `how-claude-code-works#resume-or-fork-sessions` → `sessions#branch-a-session` (checkpointing.md)

---

## New Pages

- **[deep-links.md](https://code.claude.com/docs/en/deep-links.md)** — Full reference for the `claude-cli://` URL scheme: building links with `q`/`cwd`/`repo` parameters, embedding in runbooks, triggering from shell on macOS/Linux/Windows, platform handler registration locations, and troubleshooting (link does nothing, plain-text render, wrong terminal, home directory fallback).

---

## Notable Details

- The deep link `repo` parameter only resolves to paths where `claude` has been run at least once — it does not clone. If there are multiple clones or worktrees, it picks the one used most recently.
- GitHub-rendered Markdown strips `claude-cli://` links entirely (only the label text is visible, with the URL removed). The workaround is placing the URL in a code block.
- `ultrathink` is the only in-prompt keyword that Claude Code recognizes; "think", "think hard", "think more" are noted explicitly as not recognized.
- `best-practices.md` removed the `claude --continue` / `claude --resume` code block from the "Resume conversations" section; the same information remains in `sessions.md`. Developers who referenced best-practices for session commands should consult that page directly.
- `skills.md` example SKILL.md now uses `## Current changes` and `## Instructions` as concrete section headers, making the starter template more copy-pasteable.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| deep-links.md | New | +192 | Full reference for `claude-cli://` URL scheme |
| common-workflows.md | Modified | +85/−589 | Near-rewrite: condensed to recipe index, content moved to dedicated pages |
| settings.md | Modified | +78/−78 | Table reformatting (no content change) |
| skills.md | Modified | +50/−45 | Updated SKILL.md example with `## Current changes` and `## Instructions` sections |
| tools-reference.md | Modified | +37/−37 | Reformatting (no content change) |
| vs-code.md | Modified | +32/−8 | Added "Launch a VS Code tab from other tools" with `vscode://anthropic.claude-code/open` URI handler |
| headless.md | Modified | +26/−0 | Added "Pipe data through Claude" and "Add Claude to a build script" examples |
| permission-modes.md | Modified | +17/−1 | Added "Review and approve a plan" and "Set plan mode as the default" subsections |
| model-config.md | Modified | +17/−3 | Added `ultrathink` keyword docs and "Extended thinking" controls table |
| best-practices.md | Modified | +17/−23 | "Plan Mode" → "plan mode" throughout; condensed session resume section with link to sessions page |
| hooks-guide.md | Modified | +13/−0 | Added "Auto-approve specific permission prompts" with `PermissionRequest` hook example |
| github-actions.md | Modified | +10/−10 | "AWS Bedrock" → "Amazon Bedrock" |
| gitlab-ci-cd.md | Modified | +10/−10 | "AWS Bedrock" → "Amazon Bedrock" |
| how-claude-code-works.md | Modified | +4/−12 | Removed session picker detail (moved to sessions page) |
| claude-directory.md | Modified | +18/−18 | Updated `.worktreeinclude` link to `/en/worktrees` |
| remote-control.md | Modified | +8/−8 | "AWS Bedrock" → "Amazon Bedrock"; minor wording |
| desktop.md | Modified | +3/−3 | Minor link/wording updates |
| glossary.md | Modified | +2/−2 | Minor corrections |
| sub-agents.md | Modified | +2/−2 | Link updates |
| agent-teams.md | Modified | +1/−1 | Updated worktree link to `/en/worktrees` |
| checkpointing.md | Modified | +1/−1 | Fork session link → `/en/sessions#branch-a-session` |
| cli-reference.md | Modified | +1/−1 | Updated `--worktree` flag link to `/en/worktrees` |
| code-review.md | Modified | +1/−1 | "AWS Bedrock" → "Amazon Bedrock" |
| commands.md | Modified | +1/−1 | Updated `/batch` worktree link to `/en/worktrees` |
| costs.md | Modified | +1/−1 | "AWS Bedrock" → "Amazon Bedrock" |
| errors.md | Modified | +1/−1 | Minor update |
| hooks.md | Modified | +1/−1 | Minor update |
| legal-and-compliance.md | Modified | +1/−1 | Minor update |
| monitoring-usage.md | Modified | +1/−1 | Minor update |
| overview.md | Modified | +1/−1 | Minor update |
| zero-data-retention.md | Modified | +1/−1 | Minor update |

---

*Generated from Claude Code CLI documentation changes detected on 2026-05-02*
