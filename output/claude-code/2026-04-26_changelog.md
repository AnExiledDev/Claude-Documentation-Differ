# Claude Code Documentation Changes — 2026-04-26

## Summary

Five documentation pages were updated, covering terminal theme customization, Desktop app UI navigation renames, SSH auto-install behavior, and routines/scheduled task management changes. The largest addition is a comprehensive color token reference for terminal themes. Several UI element names changed (Schedule → Routines, Prompt field → Instructions, Frequency → Schedule), indicating a Desktop app update.

## Significant Changes

### Terminal Theming

- **Full color token reference added to `terminal-config`**: A new accordion section documents every overridable token in `~/.claude/themes/*.json`, with grouped subsections and a combined example.

  > "Below is the full list of customizations you can set in `overrides`. The interactive editor in `/theme` shows the same tokens with a live preview, including a small number of internal tokens not covered here."

  The new token groups documented are:

  | Group | Notable tokens |
  |---|---|
  | Text and accent colors | `claude`, `text`, `inverseText`, `inactive`, `subtle`, `permission`, `remember` |
  | Status colors | `success`, `error`, `warning`, `merged` |
  | Input box and mode indicators | `promptBorder`, `planMode`, `autoAccept`, `bashBorder`, `ide`, `fastMode` |
  | Diff rendering | `diffAdded`, `diffRemoved`, `diffAddedDimmed`, `diffRemovedDimmed`, `diffAddedWord`, `diffRemovedWord` |
  | Fullscreen mode | `userMessageBackground`, `selectionBg` |
  | Shimmer variants and subagent colors | `claudeShimmer`, `warningShimmer`, `<color>_FOR_SUBAGENTS_ONLY` (8 colors) |

  - *Implication*: Developers can now fine-tune every color in the terminal UI without guessing token names; the `/theme` editor provides live preview for the same tokens.
  - *Source*: [terminal-config.md](https://code.claude.com/docs/en/terminal-config.md)

### Desktop App — UI Navigation Renames

- **"Schedule" page renamed to "Routines"**: The sidebar entry, task list, and button labels have changed throughout the Desktop app.

  - Old: Click **Schedule** in the sidebar → **New task** → **New local task** / **New remote task**
  - New: Click **Routines** in the sidebar → **New routine** → **Local** / **Remote**
  - "Prompt" field renamed to **Instructions**; "Frequency" section renamed to **Schedule options**
  - "Toggle repeats" renamed to **Status** (toggle between Active and Paused)
  - Edit form: "prompt, frequency" → "instructions, schedule"

  - *Implication*: Documentation links and any internal tooling that references the old "Schedule" UI label will be out of date after this Desktop release.
  - *Source*: [desktop-scheduled-tasks.md](https://code.claude.com/docs/en/desktop-scheduled-tasks.md), [routines.md](https://code.claude.com/docs/en/routines.md)

- **"Customize" button added to sidebar**: A single entry point for connectors, skills, and plugins.

  > "To manage connectors, skills, and plugins in one place, click **Customize** in the sidebar."

  - *Source*: [desktop.md](https://code.claude.com/docs/en/desktop.md)

### Desktop App — Tab Structure Clarified

- **Three-tab structure documented**: The Desktop app introduction was rewritten to describe the three top-level tabs.

  > "The Claude Desktop app has three tabs: **Chat** for conversations, **Cowork** for Dispatch and longer agentic work, and **Code** for software development. This page is the reference for the Code tab."

  - *Implication*: Cowork is now a named peer tab alongside Chat and Code; troubleshooting Git errors now points users to the Cowork tab rather than a "Cowork session."
  - *Source*: [desktop.md](https://code.claude.com/docs/en/desktop.md)

### SSH — Automatic Claude Code Installation

- **Desktop auto-installs Claude Code on remote machines**: The requirement for manual installation on SSH targets has been lifted.

  Previously:
  > "Claude Code must be installed on the remote machine."

  Now:
  > "Desktop installs Claude Code on the remote machine automatically the first time you connect."

  This change appears in both `desktop.md` (SSH sessions section) and `desktop-quickstart.md` (SSH step).

  - *Implication*: Users no longer need to manually SSH in and install Claude Code before adding a remote machine in the Desktop app.
  - *Source*: [desktop-quickstart.md](https://code.claude.com/docs/en/desktop-quickstart.md), [desktop.md](https://code.claude.com/docs/en/desktop.md)

### Scheduled Tasks — Behavioral and UI Updates

- **One-time (self-disabling) tasks documented**:

  > "'remind me at 3pm tomorrow to check the deploy' creates a one-time task that disables itself after it fires."

  - *Implication*: One-time tasks via natural language have been possible but are now explicitly documented.
  - *Source*: [desktop-scheduled-tasks.md](https://code.claude.com/docs/en/desktop-scheduled-tasks.md)

- **Folder trust required before saving a task**: New requirement documented.

  > "A folder is required before you can save the task. If you haven't trusted that folder yet, Desktop prompts you to trust it before saving."

  - *Source*: [desktop-scheduled-tasks.md](https://code.claude.com/docs/en/desktop-scheduled-tasks.md)

- **Skipped run detail now available**: History now shows hover-to-reveal reasons for skipped runs.

  > "Hover a skipped entry to see why: your computer was asleep, the previous run was still in progress, or other scheduled tasks were already running. Click **Show more** to load older entries."

  - *Source*: [desktop-scheduled-tasks.md](https://code.claude.com/docs/en/desktop-scheduled-tasks.md)

- **Task deletion restricted to UI only**: Previously, Claude could delete tasks via conversation. Now:

  > "To delete a task, use the **Delete** button on its detail page."

  - *Source*: [desktop-scheduled-tasks.md](https://code.claude.com/docs/en/desktop-scheduled-tasks.md)

- **Hourly stagger description simplified**: "Each task gets a fixed offset of up to 10 minutes" → "Each task gets a small delay of a few minutes." The deterministic property is preserved.
  - *Source*: [desktop-scheduled-tasks.md](https://code.claude.com/docs/en/desktop-scheduled-tasks.md)

### Routines — Permissions Step Reorganized

- **"Review connectors and permissions" step replaces "Review connectors"**: Unrestricted branch push permission moved from the repository step into a dedicated permissions tab.

  > "Under Permissions, enable **Allow unrestricted branch pushes** for any repository where Claude should be able to push to existing branches instead of only `claude/`-prefixed ones."

  Also added a new explicit warning about connector tool access:

  > "Claude can use every tool from an included connector, including writes, without asking for permission during a run."

  - *Implication*: Users setting up routines should review both tabs — connectors and permissions — before saving, especially if granting write access.
  - *Source*: [routines.md](https://code.claude.com/docs/en/routines.md)

- **"Create from the Desktop app" subsection removed**: Navigation instructions are now inline in the "Create a routine" section. Equivalent functionality documented in `desktop-scheduled-tasks.md`.
  - *Source*: [routines.md](https://code.claude.com/docs/en/routines.md)

### Desktop App — Auto Mode Availability

- **Auto mode requirements extracted to a dedicated anchor**: Previously inline in the permission mode table, the plan/model requirements are now in a separate paragraph with the anchor `#auto-mode-availability`, and the table cell now links to it.

  > "Auto mode is a research preview available on Max, Team, Enterprise, and API plans. It is not available on Pro plans or third-party providers. On Team, Enterprise, and API plans it requires Claude Sonnet 4.6, Opus 4.6, or Opus 4.7. On Max plans it requires Claude Opus 4.7."

  - *Implication*: Deep-linking to `#auto-mode-availability` is now reliable.
  - *Source*: [desktop.md](https://code.claude.com/docs/en/desktop.md)

### Desktop App — Preview Pane Supports Video

- **Video files added to preview pane**: "HTML, PDF, and image files" updated to include video throughout `desktop.md`.

  > "The preview pane can also open static HTML files, PDFs, images, and videos from your project. Click an HTML, PDF, image, or video path in the chat to open it in preview."

  - *Source*: [desktop.md](https://code.claude.com/docs/en/desktop.md)

### Desktop App — `--allowedTools` / `--disallowedTools` CLI Comparison Updated

- **Clarified that settings-file rules still apply**: Previously listed as "Not available in Desktop"; now reads:

  > "No per-session equivalent. Permission rules in settings files still apply."

  - *Implication*: Allowlists and blocklists configured in `.claude/settings.json` or `settings.local.json` are honored by Desktop sessions even though the CLI flags have no UI equivalent.
  - *Source*: [desktop.md](https://code.claude.com/docs/en/desktop.md)

## Notable Details

- **Version note relocated in `desktop.md`**: The minimum version requirement (Claude Desktop v1.2581.0) was moved from the page introduction to the "Arrange your workspace" section, scoping it to pane layout/terminal/file editor/view modes rather than the entire page.
- **Windows Code tab prerequisite added**: First-time Windows users now see an explicit requirement for Git for Windows before the Code tab works, with a restart step.
- **Managed settings paragraph in `desktop.md` reordered**: The paragraph clarifying that remotely pushed managed settings apply to CLI/IDE only (not Desktop) now appears *before* the paragraph on `permissions.disableBypassPermissionsMode`, making the scope restriction easier to find.
- **Routines URL now explicit**: The "Create a routine" section now links directly to `https://claude.ai/code/routines`.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| terminal-config.md | Modified | +86 / -0 | Added full color token reference accordion with 6 subsections |
| desktop.md | Modified | +35 / -35 | Tab structure, SSH auto-install, video preview, Auto mode anchor, UI renames |
| desktop-scheduled-tasks.md | Modified | +25 / -30 | Routines UI rename, one-time tasks, folder trust, skip reasons, deletion change |
| routines.md | Modified | +8 / -8 | Permissions step added, "Create from Desktop" section removed, nav updated |
| desktop-quickstart.md | Modified | +1 / -1 | SSH auto-install of Claude Code documented |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-26*
