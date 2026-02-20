# Claude Code Documentation Changes — 2026-02-20

## Summary

Six pages were modified with no new or removed pages. The most substantive changes are: a new 59-line workflow section documenting desktop notification setup via the `Notification` hook event, and a terminology rename in the plugins quickstart that replaces "commands" with "skills" (including updated file paths and directory names). Four other pages received CDN image URL updates only.

## Significant Changes

### Features

- **New workflow: Desktop notifications when Claude needs attention**: A new section was added to the Common Workflows page explaining how to configure desktop notifications using the `Notification` hook event. Users can set this up via `/hooks`, selecting the `Notification` event with matcher values that include `permission_prompt`, `idle_prompt`, `auth_success`, and `elicitation_dialog`.

  > *macOS:* `osascript -e 'display notification "Claude Code needs your attention" with title "Claude Code"'`
  >
  > *Linux:* `notify-send 'Claude Code' 'Claude Code needs your attention'`
  >
  > *Windows (PowerShell):* `powershell.exe -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')"`

  - *Implication*: Developers running long-running Claude Code tasks can now receive OS-level notifications when Claude finishes or requires input, without watching the terminal. Saving to user settings applies the hook across all projects.
  - *Source*: [Common Workflows](https://code.claude.com/docs/en/common-workflows.md)

### Configuration

- **Plugins: "Commands" renamed to "Skills"**: The plugin quickstart documentation has been updated to reflect a terminology change — what were previously called "commands" are now called "skills". This affects file paths, directory names, section headings, and instructional text throughout the quickstart.

  | Before | After |
  |--------|-------|
  | `commands/hello.md` | `skills/hello/SKILL.md` |
  | `# Hello Command` | `# Hello Skill` |
  | "Commands directory" | "Skills directory" |
  | "try your commands" | "try your skills with `/plugin-name:skill-name`" |

  - *Implication*: Developers building plugins should update their directory layout and file naming to match the new `skills/<name>/SKILL.md` convention. The invocation syntax is now explicitly documented as `/plugin-name:skill-name`.
  - *Source*: [Plugins](https://code.claude.com/docs/en/plugins.md)

## Notable Details

- **CDN image token rotation**: Four pages (`data-usage.md`, `features-overview.md`, `hooks.md`, `how-claude-code-works.md`) had embedded CDN image URLs updated to use a new token (`TBPmHzr19mDCuhZi`), replacing multiple previous tokens. This is an infrastructure change with no content impact — diagrams and screenshots remain the same.
- **`Notification` hook matcher values**: The new notification workflow section documents four specific matcher strings (`permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`) that trigger the hook — a level of specificity that gives developers control over which events fire notifications.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| common-workflows.md | Modified | +59 / -0 | New "Get notified when Claude needs your attention" section with OS-specific notification commands |
| plugins.md | Modified | +8 / -8 | Terminology rename: "commands" → "skills" throughout quickstart (paths, headings, instructions) |
| hooks.md | Modified | +2 / -2 | CDN image URL updates for hooks lifecycle and hook resolution diagrams |
| how-claude-code-works.md | Modified | +2 / -2 | CDN image URL updates for agentic loop and session continuity diagrams |
| data-usage.md | Modified | +1 / -1 | CDN image URL update for data flow diagram |
| features-overview.md | Modified | +1 / -1 | CDN image URL update for context loading diagram |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-20*
