# Claude Code Documentation Changes — 2026-02-21

## Summary

The largest update in this batch is a substantial expansion of the Desktop reference page (`desktop.md`), adding 238 lines of new content covering two new capabilities: live app preview with dev server configuration, and GitHub pull request monitoring with auto-fix and auto-merge. Permission mode names were renamed throughout all three modified pages, and Windows ARM64 support status was updated from limited to fully supported.

## Significant Changes

### Features

- **Live App Preview**: A new "Preview your app" section documents an embedded browser that Claude can use to verify its own changes. Claude starts a dev server automatically, takes screenshots, inspects the DOM, clicks elements, fills forms, and iterates on issues it finds.
  > "Claude can start a dev server and open an embedded browser to verify its changes. This works for frontend web apps as well as backend servers: Claude can test API endpoints, view server logs, and iterate on issues it finds."
  - *Implication*: Developers can now let Claude self-verify UI and API changes without manual browser testing between iterations. Auto-verify is on by default and can be disabled per-project via `.claude/launch.json`.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Code Review from Diff View**: A new "Review your code" section documents a **Review code** button in the diff view toolbar that triggers Claude to evaluate pending changes and leave inline comments.
  > "The review focuses on high-signal issues: compile errors, definite logic errors, security vulnerabilities, and obvious bugs. It does not flag style, formatting, pre-existing issues, or anything a linter would catch."
  - *Implication*: Claude performs a targeted pre-commit review scoped to the current diff, not the full codebase.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Pull Request Monitoring with Auto-fix and Auto-merge**: A new section documents CI status tracking after a PR is opened. Claude polls GitHub CLI for check results and can automatically fix failures or merge once all checks pass.
  > "Auto-merge: when enabled, Claude merges the PR once all checks pass. The merge method is squash."
  > "PR monitoring requires the GitHub CLI (`gh`) to be installed and authenticated on your machine."
  - *Implication*: Requires `gh` CLI installed and authenticated. Auto-merge uses squash only and depends on the GitHub repository having auto-merge enabled in its settings.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

### Configuration

- **Preview Server Configuration via `.claude/launch.json`**: A new "Configure preview servers" section with a full field reference documents how Claude stores and uses dev server configuration. Supports multiple servers, port conflict handling, environment variables, and `program` vs `runtimeExecutable` distinctions.
  > "Claude automatically detects your dev server setup and stores the configuration in `.claude/launch.json` at the root of the folder you selected when starting the session."
  > "Don't put secrets here since this file is committed to your repo. Secrets set in your shell profile are inherited automatically."
  - *Implication*: `.claude/launch.json` is committed to the repository. The `autoPort` field controls port conflict behavior: `true` picks a free port, `false` fails with an error, and omitting it prompts interactively.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Permission Mode Renames**: All four Desktop permission modes were renamed throughout the documentation:
  - `Ask` → `Ask permissions`
  - `Code` → `Auto accept edits`
  - `Act` → `Bypass permissions`
  - `Plan` is now explicitly called `Plan mode`
  > "Start with Ask permissions to see exactly what Claude does, then move to Auto accept edits or Plan mode as you get comfortable."
  - *Implication*: The underlying `settings.json` keys (`default`, `acceptEdits`, `plan`, `bypassPermissions`) are unchanged. Only the display names changed.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Managed Settings Key Renamed**: The enterprise managed settings key for disabling bypass permissions mode was shortened.
  > Previously: `permissions.disableBypassPermissionsMode`
  > Now: `disableBypassPermissionsMode`
  - *Implication*: Organizations using this managed setting in their settings file should update the key name.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **`MAX_THINKING_TOKENS` Behavior on Opus Clarified**: The documentation now notes that on Opus models, `MAX_THINKING_TOKENS` is ignored except for `0` due to adaptive reasoning.
  > "On Opus, `MAX_THINKING_TOKENS` is ignored except for `0` because adaptive reasoning controls thinking depth instead."
  - *Implication*: Setting a non-zero `MAX_THINKING_TOKENS` budget has no effect when using Opus; only setting it to `0` disables thinking.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

### Platform Support

- **Windows ARM64 Now Fully Supported**: The previous note that ARM64 devices require remote sessions was removed. ARM64 is now listed as fully supported.
  > Previously: "For Windows ARM64, [download here]... Local sessions are not available on ARM64 devices, so use remote sessions instead."
  > Now: "For Windows ARM64, [download here]." (limitation language removed entirely)
  > Troubleshooting entry updated to: "ARM64: Windows ARM64 devices are fully supported."
  - *Implication*: Developers on Windows ARM64 hardware can now use local sessions.
  - *Source*: [Desktop Quickstart](https://code.claude.com/docs/en/desktop-quickstart.md)

- **Windows Git Requirement Clarified**: Git is now described as required for the Code tab to function on Windows (not just for session isolation), with an updated link to the Windows-specific Git download.
  > "On Windows, Git is required for the Code tab to work: download Git for Windows, install it, and restart the app."
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Cowork Tab Available on Windows**: The Cowork tab limitation was updated to note it requires Apple Silicon on macOS specifically, but is available on all supported Windows hardware.
  > "The Cowork tab requires Apple Silicon (M1 or later) on macOS. On Windows, Cowork is available on all supported hardware."
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

### Navigation and Links

- **Model Reference Updated**: Links to model comparison pages were updated from `/en/overview#models` to `/en/model-config#available-models` in both `desktop.md` and `desktop-quickstart.md`.
  - *Source*: [Desktop Quickstart](https://code.claude.com/docs/en/desktop-quickstart.md), [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Desktop App Link in Overview**: The "Learn more about the desktop app" link on the overview page was updated from `/en/desktop#get-started` to `/en/desktop-quickstart`.
  - *Source*: [Overview](https://code.claude.com/docs/en/overview.md)

- **Cloud Environment Anchor Fixed**: The link to cloud environment configuration was corrected from `#cloud-environments` to `#cloud-environment`.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

## Notable Details

- The compact command reference in `desktop.md` was changed from the prose phrase `"compact this conversation"` to the slash command `/compact`, aligning it with actual CLI syntax.
- SSH session documentation was reordered: the prerequisite ("Claude Code must be installed on the remote machine") now appears before the list of supported features rather than after.
- The admin console entry previously labeled "Disable Act mode" was renamed to "Disable Bypass permissions mode" to match the new permission mode naming.
- Windows Event Viewer log path was corrected from `Event Viewer → Application` to `Event Viewer → Windows Logs → Application` in both the CLI flag equivalents table and the bug-filing instructions.
- The quickstart intro sentence was updated to explicitly state the desktop app includes Claude Code and that Node.js or the CLI need not be installed separately to use the desktop app.
- A note was added to the managed settings section pointing to `allowManagedPermissionRulesOnly` and `allowManagedHooksOnly` in the permissions reference, indicating these managed-only settings now have dedicated documentation.
- Code block theme attributes in `overview.md` were changed from `theme={null}` (with two spaces before) to `theme={null} theme={null}` (duplicated attribute). This appears to be a rendering artifact with no user-facing impact.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| desktop.md | Modified | +238/-53 | Added app preview and PR monitoring features; renamed permission modes; new `.claude/launch.json` configuration reference; Windows ARM64 and Cowork tab updates; managed settings key renamed |
| desktop-quickstart.md | Modified | +18/-12 | Updated intro to list live preview and PR monitoring; removed ARM64 limitations note; clarified Git requirement on Windows; updated model link and permission mode names |
| overview.md | Modified | +6/-6 | Updated desktop app link to point to quickstart; changed code block theme attribute formatting |
