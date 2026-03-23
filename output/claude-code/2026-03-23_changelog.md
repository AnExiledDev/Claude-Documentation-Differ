# Claude Code Documentation Changes — 2026-03-23

## Summary

One page was modified in this update: the permissions reference page received a new paragraph clarifying the precedence relationship between blocking hooks and allow rules. No pages were added or removed.

## Significant Changes

### Configuration

- **Blocking hooks override allow rules**: The permissions docs now explicitly state that a `PreToolUse` hook exiting with code 2 stops a tool call *before* permission rules are evaluated — meaning a blocking hook can prevent a call that an allow rule would otherwise permit. This is the inverse of the existing behavior documented for hooks returning `"allow"` (which still respect deny rules).
  > A blocking hook also takes precedence over allow rules. A hook that exits with code 2 stops the tool call before permission rules are evaluated, so the block applies even when an allow rule would otherwise let the call proceed. To run all Bash commands without prompts except for a few you want blocked, add `"Bash"` to your allow list and register a PreToolUse hook that rejects those specific commands. See [Block edits to protected files](/en/hooks-guide#block-edits-to-protected-files) for a hook script you can adapt.
  - *Implication*: This documents a practical pattern — broadly allow a tool (e.g., `"Bash"`) to suppress prompts, then use a `PreToolUse` hook to selectively block specific commands. Previously only the `"allow"` → deny-rule interaction was documented; this adds the complementary blocking direction.
  - *Source*: [Configure permissions](https://code.claude.com/docs/en/permissions.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/claude-code/en/permissions.md` | Modified | +2 / -0 | Added paragraph clarifying that exit-code-2 hooks take precedence over allow rules, with a pattern for selective Bash blocking |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-23*
