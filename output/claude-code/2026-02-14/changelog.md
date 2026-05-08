# Claude Code Documentation Changes — 2026-02-14

## Summary

The Desktop app documentation has been restructured with a new quickstart guide and significantly expanded reference documentation. The most notable additions are SSH session support, enhanced enterprise configuration details, and new model restriction capabilities for administrators. Minor changes include terminology updates (Team → Teams) and a new `/desktop` CLI command.

## Significant Changes

### Desktop App

- **New desktop quickstart guide**: A dedicated getting started page now separates installation and first-session workflows from the comprehensive reference documentation
  > "The desktop app gives you Claude Code with a graphical interface: visual diff review, parallel sessions with Git worktree isolation, file attachments, and the ability to run long-running tasks remotely."
  - *Implication*: New users have a clearer onboarding path; the main desktop.md page now serves as a reference rather than tutorial
  - *Source*: [Get started with the desktop app](https://code.claude.com/docs/en/desktop-quickstart.md)

- **SSH session support**: Desktop now supports connecting to remote machines over SSH for running Claude Code on cloud VMs, dev containers, or servers
  > "To add an SSH connection, click the environment dropdown before starting a session and select **+ Add SSH connection**. The dialog asks for: Name, SSH Host, SSH Port, Identity File"
  - *Implication*: Developers can work on codebases that require specific hardware or dependencies without running locally. SSH sessions support connectors, plugins, and MCP servers.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Worktree location customization**: Users can now configure where Git worktrees are stored, changing from `~/.claude-worktrees/` to `<project-root>/.claude/worktrees/` by default
  > "Worktrees are stored in `<project-root>/.claude/worktrees/` by default. You can change this to a custom directory in Settings → Claude Code under 'Worktree location'."
  - *Implication*: Project-scoped worktree storage prevents cluttering the home directory and improves cleanup
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Continue in another surface**: New menu for moving sessions between Desktop, web, and IDE environments
  > "The **Continue in** menu, accessible from the VS Code icon in the bottom right of the session toolbar, lets you move your session to another surface"
  - *Implication*: Seamless workflow transitions—start in Desktop for visual diff review, move to web for remote continuation, or open in IDE
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Windows ARM64 support (remote only)**: Windows ARM64 builds are now available, but local sessions are not supported
  > "For Windows ARM64, download here. Local sessions are not available on ARM64 devices, so use remote sessions instead."
  - *Implication*: Windows ARM devices can run Desktop but must use cloud sessions instead of local execution
  - *Source*: [Get started with the desktop app](https://code.claude.com/docs/en/desktop-quickstart.md)

### Enterprise Configuration

- **Expanded enterprise configuration section**: Desktop documentation now includes comprehensive enterprise deployment details previously scattered across support articles
  > "Organizations on Teams or Enterprise plans can manage desktop app behavior through admin console controls, managed settings files, and device management policies."
  - *Implication*: Enterprise admins have a single reference for MDM policies, deployment options, SSO configuration, and data handling
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

- **Model restriction controls**: Administrators can restrict which models users can select using the `availableModels` setting
  > "When `availableModels` is set, users cannot switch to models not in the list via `/model`, `--model` flag, Config tool, or `ANTHROPIC_MODEL` environment variable."
  - *Implication*: Enables cost control and compliance by limiting access to expensive models like Opus. The Default option always remains available.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

- **Managed settings precedence clarified**: Distinction between settings for CLI/IDE vs Desktop-specific controls
  > "Remote managed settings uploaded through the admin console currently apply to CLI and IDE sessions only. For Desktop-specific restrictions, use the admin console controls above."
  - *Implication*: Admins need to use different mechanisms for Desktop vs CLI/IDE restrictions
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

### CLI and Interactive Features

- **New `/desktop` command**: CLI sessions can now be handed off to the Desktop app (macOS and Windows only)
  > "Hand off the current CLI session to the Claude Code Desktop app (macOS and Windows only)"
  - *Implication*: Enables workflow transitions from terminal to GUI without losing context
  - *Source*: [Interactive mode](https://code.claude.com/docs/en/interactive-mode.md)

- **Enhanced CLI comparison table**: Desktop documentation now includes detailed feature parity table comparing CLI and Desktop capabilities
  - *Implication*: Developers can make informed choices about which interface to use for specific workflows
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

## New Pages

- **desktop-quickstart.md** — Installation and first-session tutorial for the Desktop app, separate from the comprehensive reference documentation. [View](https://code.claude.com/docs/en/desktop-quickstart.md)

## Notable Details

- **Terminology standardization**: "Team" plan references updated to "Teams" throughout documentation (chrome.md, slack.md, desktop-quickstart.md)
- **Troubleshooting reorganization**: Desktop troubleshooting section restructured with clearer headings including "403 or authentication errors", "Blank or stuck screen on launch", and platform-specific issues
- **Documentation structure shift**: desktop.md title changed from "Claude Code on desktop" to "Use Claude Code Desktop", indicating a shift from overview to reference documentation
- **Removed "preview" status**: The note "Claude Code on desktop is currently in preview" has been removed from desktop.md
- **Default model table clarification**: model-config.md now explicitly states default models for Max/Team/Pro vs API users when using `availableModels` restrictions

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| desktop.md | Modified | +237/-182 | Major restructure: added SSH sessions, enterprise config details, CLI comparison table; split installation to quickstart |
| desktop-quickstart.md | New | +131 | New getting started guide for Desktop installation and first session |
| model-config.md | Modified | +43/-0 | Added `availableModels` restriction feature with default model behavior and merge rules |
| overview.md | Modified | +7/-4 | Added Windows ARM64 download link, updated Desktop workflow descriptions |
| interactive-mode.md | Modified | +1/-0 | Added `/desktop` command to built-in commands table |
| settings.md | Modified | +1/-0 | Added `availableModels` setting to settings reference table |
| best-practices.md | Modified | +1/-1 | Updated link reference from "Claude Desktop" to "Claude Code desktop app" |
| chrome.md | Modified | +1/-1 | Standardized "Team" to "Teams" plan naming |
| slack.md | Modified | +1/-1 | Standardized "Team" to "Teams" plan naming |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-14*
