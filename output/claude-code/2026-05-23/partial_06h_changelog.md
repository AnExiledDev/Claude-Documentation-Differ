# Claude Code Documentation Changes — 2026-05-23

## Summary

Three pages were modified with a total of 7 additions and 1 deletion. The changes include a new version entry (2.1.150) in the changelog and a pair of related clarifications about how subagent worktrees choose their base branch.

## Minor Changes

- **changelog.md**: Added version 2.1.150 (May 23, 2026) — "Internal infrastructure improvements (no user-facing changes)" (+4/-0 lines)
- **sub-agents.md**: Clarified the `isolation: worktree` frontmatter field description — subagent worktrees now explicitly documented to branch from the repository's default branch rather than the parent session's `HEAD`, with a link to the base branch configuration section (+1/-1 lines)
- **worktrees.md**: Added a sentence clarifying that subagent worktrees use the same base branch as `--worktree`, defaulting to the repository's default branch unless `worktree.baseRef` is set to `"head"` (+2/-0 lines)

## Notable Details

The sub-agents.md and worktrees.md edits are complementary and address the same behavioral point: when `isolation: worktree` is used on a subagent, the resulting worktree branches from the **repository's default branch** — not the parent session's `HEAD`. Developers who expect subagent worktrees to inherit the parent session's current branch should set `worktree.baseRef: "head"` in their configuration to override this default.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| changelog.md | Modified | MINOR | +4/-0 | Added v2.1.150 entry (internal infra, no user-facing changes) |
| sub-agents.md | Modified | MINOR | +1/-1 | Clarified `isolation: worktree` branches from default branch, not parent HEAD |
| worktrees.md | Modified | MINOR | +2/-0 | Added note that subagent worktrees use same base branch as `--worktree` |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-23*
