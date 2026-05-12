# Claude Code Documentation Changes — 2026-05-12

## Summary

Five documentation pages were updated in this batch. The most significant changes are a new security restriction on `bypassPermissions` mode (blocked when running as root/sudo) and a documentation-wide shift in hook examples toward using exec form (`"args": []`) to avoid shell quoting pitfalls with path variables.

## Significant Changes

### Permission Modes

- **`bypassPermissions` now blocked for root/sudo on Linux and macOS**: The `--dangerously-skip-permissions` (alias: `--permission-mode bypassPermissions`) flag will refuse to start when Claude Code detects it is running as root or under `sudo`.
  > `--dangerously-skip-permissions cannot be used with root/sudo privileges for security reasons`
  - *Implication*: Automated pipelines running Claude Code as root with `bypassPermissions` will break. The recommended path is to use the [dev container](/en/devcontainer) configuration, which runs as a non-root user. The check is automatically skipped inside a recognized sandbox environment.
  - *Source*: [permission-modes.md](https://code.claude.com/docs/en/permission-modes.md)

### Hooks — Exec Form Now Recommended for Path Variables

- **Hook examples updated to prefer exec form for `$CLAUDE_PROJECT_DIR` and `$CLAUDE_PLUGIN_ROOT` paths**: All code examples that previously quoted the project dir variable as `"\"$CLAUDE_PROJECT_DIR\""` in shell-form hook commands now use `"${CLAUDE_PROJECT_DIR}"` combined with an explicit `"args": []` field to invoke exec form instead.

  Before:
  > `"command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-rm.sh"`

  After:
  > `"command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh",`  
  > `"args": []`

  The security best-practices section was also updated:
  > **Use absolute paths**: specify full paths for scripts. In exec form, use `${CLAUDE_PROJECT_DIR}` and the path needs no quoting. In shell form, wrap it in double quotes
  - *Implication*: Exec form (triggered by adding `"args": []`) bypasses the shell entirely, eliminating quoting errors caused by spaces or special characters in paths. Developers with existing hooks using the old quoted style should migrate to exec form. Five distinct hook examples across `hooks.md` were updated.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md)

## Minor Changes

- **`hooks-guide.md`**: Troubleshooting tip for "command not found" now recommends using `${CLAUDE_PROJECT_DIR}` (curly-brace form) and explicitly mentions adding `"args": []` to switch to exec form as an alternative to shell quoting (+1/-1). [Source](https://code.claude.com/docs/en/hooks-guide.md)

- **`plugins-reference.md`**: `${CLAUDE_PLUGIN_ROOT}` variable description updated to recommend exec form with `args` for hook commands, reserving double-quote wrapping for shell-form hooks and monitor commands (+1/-1). [Source](https://code.claude.com/docs/en/plugins-reference.md)

- **`claude-directory.md`**: Added `projects/<project>/<session>/subagents/` to the `~/.claude/` file paths table, documenting that subagent conversation transcripts are stored there and cleaned up alongside the parent session transcript (+1/-0). [Source](https://code.claude.com/docs/en/claude-directory.md)

## Notable Details

- The root/sudo restriction in `bypassPermissions` mode is a **new runtime enforcement**, not just documentation. The error message is a hard failure, not a warning. Developers using CI containers with elevated privileges need to act.
- The exec-form migration across hook examples is consistent and appears intentional — five separate examples were updated in `hooks.md` alone. This signals that the project is moving away from fragile shell-quoting patterns as the recommended default for path-bearing hook commands.
- The `subagents/` directory entry in `claude-directory.md` provides the first explicit documentation of where subagent transcripts live on disk and their cleanup lifecycle (co-removed with the parent session).

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| hooks.md | Modified | SIGNIFICANT | +11/-6 | Exec form examples for path variables; updated security best-practices wording |
| permission-modes.md | Modified | SIGNIFICANT | +8/-0 | New root/sudo restriction for bypassPermissions mode |
| hooks-guide.md | Modified | MINOR | +1/-1 | Troubleshooting tip updated with exec form recommendation |
| plugins-reference.md | Modified | MINOR | +1/-1 | `${CLAUDE_PLUGIN_ROOT}` guidance updated for exec vs shell form |
| claude-directory.md | Modified | MINOR | +1/-0 | Added subagents/ transcript directory to file paths table |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-12*
