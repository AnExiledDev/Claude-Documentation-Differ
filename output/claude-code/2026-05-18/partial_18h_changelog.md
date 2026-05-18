# Claude Code Documentation Changes — 2026-05-18

## Summary

Two pages were modified in this update. The statusline documentation received a substantive expansion covering a Windows + Git Bash path-escaping issue, while the Desktop documentation added one new limitation bullet describing terminal-dialog commands unavailable in the Code tab.

## Significant Changes

### Configuration

- **Windows status line: Git Bash backslash path issue documented**: The statusline Windows configuration section now explicitly warns that Git Bash treats unquoted backslashes as escape characters. A Windows-style path such as `C:\Users\username\script.mjs` will have its separators silently stripped before the script runner sees the command, causing a silent failure.
  > "Git Bash treats unquoted backslashes as escape characters, so a Windows-style path such as `C:\Users\username\script.mjs` reaches the script runner with its separators removed and the command fails without a visible error. Write file paths in the `command` string with forward slashes, as shown in the examples below. The `~` shorthand also works and expands to your Windows home directory."
  - *Implication*: Windows users whose status line scripts silently fail with Git Bash installed should switch all backslashes in the `command` path to forward slashes. This was a previously undocumented failure mode with no visible error.
  - *Source*: [statusline.md](https://code.claude.com/docs/en/statusline.md)

- **Windows status line troubleshooting bullet added**: A new troubleshooting item in the statusline docs cross-links the backslash issue directly from the troubleshooting checklist.
  > "On Windows with Git Bash installed, backslashes in the `command` path are likely being consumed as escape characters before the script runs. Use forward slashes in the path. See Windows configuration."
  - *Implication*: Users hitting silent status line failures on Windows now have a dedicated diagnostic step pointing to the root cause and fix.
  - *Source*: [statusline.md](https://code.claude.com/docs/en/statusline.md)

## Minor Changes

- **desktop.md**: Added one limitation bullet clarifying that terminal-dialog commands (`/permissions`, `/config`, `/agents`, `/doctor`) are unavailable in the Desktop Code tab and reply with `isn't available in this environment`. Workaround is to edit settings files directly or use the standalone CLI. (+1/-0 lines)

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| statusline.md | Modified | SIGNIFICANT | +6/-1 | Windows Git Bash backslash path-escaping issue documented; troubleshooting bullet added |
| desktop.md | Modified | MINOR | +1/-0 | Terminal-dialog commands listed as a Desktop Code tab limitation |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-18*
