# Claude Code Documentation Changes — 2026-05-24

## Summary

Four documentation pages were updated in this batch. The most notable changes are: a new callout in the Code Review page surfacing the `/code-review` terminal command (previously `/simplify`) as a local alternative to the GitHub App, and a streamlined quickstart login flow that removes code-block inline comments in favor of prose. Two minor additions document sandbox behavior for Git worktrees and shell alias availability in Bash commands.

## Significant Changes

### Features

- **`/code-review` command surfaced in Code Review docs**: A new `<Note>` callout was added near the top of the Code Review page to highlight that users can run `/code-review` in a local Claude Code session to review diffs without installing the GitHub App. The note also documents the `--comment` flag for posting inline PR comments, and records a rename history: the command was called `/simplify` before v2.1.147.
  > "To review a diff locally in your terminal without installing the GitHub App, run the `/code-review` command in any Claude Code session. It reports correctness bugs in the current diff at a chosen effort level and can post findings as inline PR comments with `--comment`. The command was named `/simplify` before v2.1.147."
  - *Implication*: Developers who want lightweight local code review without the managed GitHub App now have clear documentation for the built-in command. The rename note (`/simplify` → `/code-review`) is important for users upgrading from v2.1.146 or earlier.
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

- **Code Review "See Also" link updated from Plugins to Commands**: The bottom-of-page related-links section replaced a pointer to the plugin marketplace (`/en/discover-plugins`) with a direct link to the Commands page (`/en/commands`), reflecting the promotion of `/code-review` from a plugin to a first-class built-in command.
  > "* [Commands](/en/commands): run `/code-review` in a local Claude Code session to check a diff before pushing"
  - *Implication*: Users following the Code Review page to find local review options will land on the Commands reference instead of the plugin marketplace.
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

### Documentation

- **Quickstart login flow rewritten for clarity**: The Step 2 "Log in to your account" section was restructured. The two separate `bash` code blocks (one for `claude`, one for `/login`) with inline comments (`# You'll be prompted to log in on first use`, `# Follow the prompts to log in with your account`) were replaced with prose explanation and a single `text`-themed snippet for `/login`. The redundant trailing sentence ("To switch accounts later, use the `/login` command.") was removed since that guidance was moved earlier in the flow.
  > "For Claude subscription or Console accounts, follow the prompts to complete authentication in your browser. To switch accounts later or re-authenticate, type `/login` inside the running session"
  - *Implication*: The login instructions now read more naturally; the `/login` command is explicitly scoped to re-authentication and account switching, which was previously ambiguous.
  - *Source*: [Quickstart](https://code.claude.com/docs/en/quickstart.md)

## Minor Changes

- **sandboxing.md**: Added one bullet documenting Git worktree sandbox behavior — when the working directory is a linked git worktree, the sandbox grants write access to the main repo's shared `.git` directory (for `git commit`, ref updates, index), but blocks writes to `hooks/` and `config` within it. (+1/-0)
- **tools-reference.md**: Added one bullet clarifying that shell aliases and functions defined in startup files (`~/.zshrc`, `~/.bashrc`, `~/.profile`) are captured at session start and applied to every Bash tool command, even though environment variables do not persist between commands. (+1/-0)

## Notable Details

- The `/simplify` → `/code-review` rename (pre-v2.1.147) is documented retroactively in the Code Review page but not yet reflected as a dedicated changelog entry in the Commands page. Users still on older installs should be aware the old command name no longer applies.
- The `tools-reference.md` addition about shell startup files is meaningful: it clarifies an implicit behavior (aliases are available) that contradicts the surrounding paragraph's statement that "environment variables do not persist." The two behaviors are now clearly distinguished.
- The sandboxing worktree note explicitly calls out that `hooks/` and `config` inside the shared `.git` directory remain denied even for linked worktrees — a security-relevant detail for teams using worktree-based workflows with the sandbox enabled.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| code-review.md | Modified | SIGNIFICANT | +5/-1 | Added `/code-review` local command callout; updated See Also link from Plugins to Commands |
| quickstart.md | Modified | SIGNIFICANT | +5/-5 | Rewrote login flow prose; removed inline code comments; clarified `/login` usage |
| sandboxing.md | Modified | MINOR | +1/-0 | Documented sandbox write access for Git worktree shared `.git` directory |
| tools-reference.md | Modified | MINOR | +1/-0 | Documented shell alias/function availability from startup files in Bash commands |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-24*
