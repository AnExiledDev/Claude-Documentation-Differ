# Claude Code Documentation Changes — 2026-04-21

## Summary

Ten pages were modified with a net +82/-10 lines. The most substantial changes are a large expansion of the `.claude` directory reference page (new navigation, decision, and troubleshooting sections), a new `sshConfigs` managed setting for distributing SSH connections across teams, and minor documentation additions covering non-code folder use and VS Code extended thinking interaction.

## Significant Changes

### Configuration

- **New `sshConfigs` setting for team SSH distribution**: Administrators can now pre-configure SSH remote connections in a managed settings file. These connections appear in every user's Desktop environment dropdown as read-only entries that cannot be edited or deleted through the app.
  > "Administrators can distribute SSH connections to team members by adding `sshConfigs` to a managed settings file. Connections defined this way appear in each user's environment dropdown automatically and are shown as managed, so users can select them but cannot edit or delete them in the app."

  Example config entry:
  ```json
  {
    "sshConfigs": [
      {
        "id": "shared-dev-vm",
        "name": "Shared Dev VM",
        "sshHost": "user@dev.example.com",
        "sshPort": 22,
        "sshIdentityFile": "~/.ssh/id_ed25519",
        "startDirectory": "~/projects"
      }
    ]
  }
  ```
  Required fields: `id`, `name`, `sshHost`. Optional: `sshPort`, `sshIdentityFile`, `startDirectory`. Users can also add `sshConfigs` to their own `~/.claude/settings.json` for personal connections added through the UI dialog. When set in managed settings, connections are read-only for users.
  - *Implication*: Teams can now centrally manage remote development environments without requiring each developer to manually configure connections in the Desktop app.
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md), [Settings](https://code.claude.com/docs/en/settings.md)

### `.claude` Directory Reference — Major Expansion

- **Windows path clarification**: The page now explicitly states that `~/.claude` resolves to `%USERPROFILE%\.claude` on Windows.
  > "On Windows, `~/.claude` resolves to `%USERPROFILE%\.claude`."
  - *Implication*: Removes ambiguity for Windows users setting `CLAUDE_CONFIG_DIR` or locating global config files.
  - *Source*: [Claude Directory](https://code.claude.com/docs/en/claude-directory.md)

- **New "Choose the right file" decision table**: A new `## Choose the right file` section maps common customization goals to the correct configuration file, scope, and reference page:

  | You want to | Edit | Scope |
  |---|---|---|
  | Give Claude project context and conventions | `CLAUDE.md` | project or global |
  | Allow or block specific tool calls | `settings.json` `permissions` or `hooks` | project or global |
  | Run a script before or after tool calls | `settings.json` `hooks` | project or global |
  | Set environment variables for the session | `settings.json` `env` | project or global |
  | Keep personal overrides out of git | `settings.local.json` | project only |
  | Add a prompt or capability you invoke with `/name` | `skills/<name>/SKILL.md` | project or global |
  | Define a specialized subagent with its own tools | `agents/*.md` | project or global |
  | Connect external tools over MCP | `.mcp.json` | project only |
  | Change how Claude formats responses | `output-styles/*.md` | project or global |

  - *Implication*: Directly addresses the common new-user confusion about which file to edit for which purpose, especially the `settings.json` vs. `CLAUDE.md` split.
  - *Source*: [Claude Directory](https://code.claude.com/docs/en/claude-directory.md)

- **New "Troubleshoot configuration" section**: A new `## Troubleshoot configuration` section provides a 13-row diagnostic table covering the most common misconfiguration symptoms, their causes, and fixes. Topics covered: hook matcher case-sensitivity and format, the `~/.claude.json` vs `~/.claude/settings.json` distinction, `settings.local.json` precedence, skill folder structure, subdirectory `CLAUDE.md` load timing, subagent memory inheritance, `SessionEnd` hooks, MCP config file placement and approval, relative vs. absolute paths in MCP server config, MCP env var propagation, and Bash `rm` permission rule literal-matching.

  Selected entries:
  > "Hook never fires → `matcher` value is lowercase, for example `"bash"` → Matching is case-sensitive. Tool names are capitalized: `Bash`, `Edit`, `Write`, `Read`."
  > "Permissions, hooks, or env set globally are ignored → Configuration was added to `~/.claude.json` → `~/.claude.json` holds app state and UI toggles. `permissions`, `hooks`, and `env` belong in `~/.claude/settings.json`. These are two different files."
  > "Hooks are in a standalone `.claude/hooks.json` file → There is no standalone hooks file. Define hooks under the `"hooks"` key in `settings.json`."

  - *Implication*: The `~/.claude.json` vs `~/.claude/settings.json` confusion is one of the most reported Claude Code support issues; its documentation here should reduce those tickets. The case-sensitive matcher tip is also a frequently missed requirement.
  - *Source*: [Claude Directory](https://code.claude.com/docs/en/claude-directory.md)

### Features

- **New "Work in notes and non-code folders" workflow**: A new `## Work in notes and non-code folders` section documents using Claude Code outside software repositories.
  > "Claude Code works in any directory. Run it inside a notes vault, a documentation folder, or any collection of markdown files to search, edit, and reorganize content the same way you would code."
  > "Claude reads files fresh on each tool call, so it sees edits you make in another application the next time it reads that file."
  - *Implication*: Clarifies that `.claude/` and `CLAUDE.md` coexist with other tools' config directories without conflict, making Claude Code viable for personal knowledge management and non-engineering workflows.
  - *Source*: [Common Workflows](https://code.claude.com/docs/en/common-workflows.md)

### Integrations

- **VS Code: Extended thinking block keyboard shortcut documented**: The prompt-box feature description for extended thinking was expanded to describe how reasoning output appears in the conversation.
  > "Claude's reasoning appears in the conversation as collapsed blocks: click a block to read it, or press `Ctrl+O` to expand or collapse every thinking block in the session."
  - *Implication*: `Ctrl+O` as a bulk toggle for all thinking blocks in the session is newly documented — useful for reviewing lengthy reasoning traces.
  - *Source*: [VS Code](https://code.claude.com/docs/en/vs-code.md)

### Enterprise

- **ZDR request: direct contact sales link added**: The Zero Data Retention enablement instructions previously pointed only to an account team contact. A direct link to the Anthropic sales contact form is now listed as an alternative.
  > "To request ZDR for Claude Code on Claude for Enterprise, [contact sales](https://www.anthropic.com/contact-sales) or your Anthropic account team."
  - *Implication*: Organizations without an existing Anthropic account team relationship now have a self-service path to initiate ZDR.
  - *Source*: [Zero Data Retention](https://code.claude.com/docs/en/zero-data-retention.md)

## Notable Details

- **URL anchor encoding fixes** (`best-practices.md`, `commands.md`, `sub-agents.md`, `statusline.md`): Internal links to the `/btw` and `/statusline` command anchors were updated to use percent-encoded slugs (`#side-questions-with-%2Fbtw`, `#use-the-%2Fstatusline-command`). This is a correctness fix for documentation renderers that encode slash characters in anchor IDs. No content changed.
- **Plugin path trailing slash removed** (`claude-directory.md`): `~/.claude/plugins/` was corrected to `~/.claude/plugins` in the file reference table. Minor, but relevant for shell scripts that do path matching or stat checks on this directory.
- **`## Explore the directory` section created**: The previous introductory paragraph ("This page is an interactive explorer: click files in the tree…") was split out into its own heading section. The interactive `<ClaudeExplorer />` component is unchanged; only the heading structure was reorganized to support the new sections on the same page.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| claude-directory.md | Modified | +42/-3 | Windows path note added; "Explore the directory" section created; "Choose the right file" decision table added; "Troubleshoot configuration" diagnostic table added; plugin path trailing slash removed |
| desktop.md | Modified | +24/-0 | New `sshConfigs` team SSH pre-configuration section with JSON example; `sshConfigs` added to managed settings reference table |
| settings.md | Modified | +1/-0 | New `sshConfigs` setting entry in the available settings reference table |
| common-workflows.md | Modified | +8/-0 | New "Work in notes and non-code folders" workflow section |
| vs-code.md | Modified | +1/-1 | Extended thinking collapsed blocks and `Ctrl+O` bulk-toggle shortcut documented |
| zero-data-retention.md | Modified | +1/-1 | Direct contact sales link added alongside account team for ZDR requests |
| statusline.md | Modified | +2/-2 | URL anchor encoding fix for `/statusline` command links |
| sub-agents.md | Modified | +1/-1 | URL anchor encoding fix for `/btw` command link |
| best-practices.md | Modified | +1/-1 | URL anchor encoding fix for `/btw` command link |
| commands.md | Modified | +1/-1 | URL anchor encoding fix for `/btw` command link |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-21*
