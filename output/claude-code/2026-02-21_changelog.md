# Claude Code Documentation Changes — 2026-02-21

## Summary

Two pages were updated to clarify the `--worktree` flag documentation. The changes add the short alias `-w` to the flag's description while simultaneously updating the inline code examples to use the long-form `--worktree` flag instead of the previously used `-w` shorthand.

## Significant Changes

### CLI Flags

- **`--worktree` now documented with `-w` short alias**: Both the Common Workflows and VS Code pages now describe the flag as `--worktree` (`-w`), making the alias discoverable. The inline code examples were updated to use `--worktree` (the long form) rather than `-w`, making examples more self-explanatory for readers encountering the flag for the first time.

  > Use the `--worktree` (`-w`) flag to create an isolated worktree and start Claude in it. The value you pass becomes the worktree directory name and branch name

  Before this change, the description referenced only `--worktree` while the code examples used `-w`, which was inconsistent. The updated examples now match the long-form flag name:

  ```bash
  # Before
  claude -w feature-auth
  claude -w bugfix-123
  claude -w

  # After
  claude --worktree feature-auth
  claude --worktree bugfix-123
  claude --worktree
  ```

  - *Implication*: Developers reading the docs for the first time will see the canonical flag name in examples rather than the short alias, reducing confusion. The short alias `-w` is still supported and now explicitly documented.
  - *Source*: [Common Workflows](https://code.claude.com/docs/en/common-workflows.md), [VS Code](https://code.claude.com/docs/en/vs-code.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| common-workflows.md | Modified | +4/-4 | Added `-w` alias to `--worktree` description; updated code examples from `-w` to `--worktree` |
| vs-code.md | Modified | +2/-2 | Added `-w` alias to `--worktree` description; updated code example from `-w` to `--worktree` |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-21*
