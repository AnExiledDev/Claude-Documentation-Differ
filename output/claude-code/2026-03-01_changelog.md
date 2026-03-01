# Claude Code Documentation Changes — 2026-03-01

## Summary

Six pages were modified with no additions or removals. The most substantial change is a near-complete rewrite of the `interactive-mode.md` built-in commands reference, expanding it from ~25 entries to a comprehensive 50+ command reference with aliases and improved descriptions. A third bundled skill (`/debug`) is now documented, and a consistent terminology shift from "slash commands" to "commands" runs across all six pages.

---

## Significant Changes

### Interactive Mode Commands Reference Overhaul

- **Built-in commands table comprehensively expanded**: The `interactive-mode.md` commands reference was rewritten. The previous version was described as covering "commonly used commands but not all available options." The new version is framed as a complete reference, with the caveat that some commands are conditionally visible.

  > "Type `/` in Claude Code to see all available commands, or type `/` followed by any letters to filter. Not all commands are visible to every user. Some depend on your platform, plan, or environment. For example, `/desktop` only appears on macOS and Windows, `/upgrade` and `/privacy-settings` are only available on Pro and Max plans, and `/terminal-setup` is hidden when your terminal natively supports its keybindings."

  Argument notation is now explicit: `<arg>` for required, `[arg]` for optional.
  - *Implication*: Developers can now reference the docs instead of running `/` in the CLI to discover available commands. Platform- and plan-gated commands are explicitly identified.
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

- **New commands documented for the first time**:

  | Command | Purpose |
  |---|---|
  | `/add-dir <path>` | Add a working directory to the current session |
  | `/agents` | Manage [agent](/en/sub-agents) configurations |
  | `/chrome` | Configure Claude in Chrome settings |
  | `/diff` | Interactive diff viewer: uncommitted changes and per-turn diffs, navigable with arrow keys |
  | `/extra-usage` | Configure extra usage to keep working when rate limits are hit |
  | `/fast [on\|off]` | Toggle fast mode on or off |
  | `/feedback [report]` | Submit feedback (alias: `/bug`) |
  | `/fork [name]` | Fork the current conversation at this point |
  | `/hooks` | Manage hook configurations for tool events |
  | `/ide` | Manage IDE integrations and show status |
  | `/insights` | Generate a report on sessions: project areas, interaction patterns, friction points |
  | `/install-github-app` | Set up Claude GitHub Actions for a repository |
  | `/install-slack-app` | Install the Claude Slack app via browser OAuth |
  | `/keybindings` | Open or create the keybindings configuration file |
  | `/login` / `/logout` | Sign in or out of your Anthropic account |
  | `/mobile` | Show QR code to download the Claude mobile app (aliases: `/ios`, `/android`) |
  | `/output-style [style]` | Switch output styles: Default, Explanatory, Learning, or custom |
  | `/passes` | Share a free week of Claude Code (only visible if account is eligible) |
  | `/plugin` | Manage Claude Code plugins |
  | `/pr-comments [PR]` | Fetch and display GitHub PR comments (requires `gh` CLI) |
  | `/privacy-settings` | View/update privacy settings (Pro and Max only) |
  | `/release-notes` | View the full changelog in-session |
  | `/remote-control` | Make the session available for remote control from claude.ai (alias: `/rc`) |
  | `/remote-env` | Configure the default remote environment for teleport sessions |
  | `/review` | Review a pull request for quality, correctness, and security (requires `gh` CLI) |
  | `/sandbox` | Toggle sandbox mode (supported platforms only) |
  | `/security-review` | Analyze pending branch changes for security vulnerabilities |
  | `/skills` | List available skills |
  | `/stickers` | Order Claude Code stickers |
  | `/terminal-setup` | Configure terminal keybindings (only shown in terminals that need it) |
  | `/upgrade` | Open the upgrade page to switch to a higher plan tier |
  | `/vim` | Toggle between Vim and Normal editing modes |

  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

- **Existing commands updated with aliases and improved descriptions**:

  | Command | Update |
  |---|---|
  | `/clear` | Added aliases `/reset`, `/new`; description adds "free up context" |
  | `/config` | Added alias `/settings` |
  | `/copy` | Description clarified to "Copy the last assistant response" |
  | `/desktop` | Added alias `/app`; description updated to "Continue the current session in the Claude Code Desktop app" |
  | `/exit` | Added alias `/quit` |
  | `/memory` | Expanded: now covers auto-memory enable/disable and viewing auto-memory entries |
  | `/permissions` | Added alias `/allowed-tools` |
  | `/resume` | Added alias `/continue` |
  | `/rewind` | Now links to `/en/checkpointing`; added alias `/checkpoint` |
  | `/statusline` | Expanded: "Describe what you want, or run without arguments to auto-configure from your shell prompt" |
  | `/theme` | Expanded: documents light/dark variants, colorblind-accessible (daltonized) themes, and ANSI themes |
  | `/usage` | Removed "For subscription plans only" qualifier |

  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

- **`/teleport` removed from the reference table**: The prior entry — "`/teleport` — Resume a remote session from claude.ai (subscribers only)" — no longer appears. Its functionality maps to `/remote-control` (alias `/rc`) and `/remote-env`. `/todos` was also silently removed from the table.
  - *Implication*: Developers relying on `/teleport` should use `/remote-control` instead.
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

---

### Bundled Skills

- **`/debug` added as a third bundled skill**: Previously only `/simplify` and `/batch` were listed as bundled skills. `/debug` is now formally included.

  > "`/debug [description]`: troubleshoots your current Claude Code session by reading the session debug log. Optionally describe the issue to focus the analysis."

  - *Implication*: `/debug` was previously documented only in the interactive-mode commands table. Its promotion to bundled skill indicates it runs as a prompt-based agent — capable of spawning agents and reading files — rather than fixed CLI logic.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

- **Bundled skills architecturally distinguished from built-in commands**: A new paragraph explains how bundled skills differ from built-in commands like `/clear` or `/compact`.

  > "Unlike [built-in commands](/en/interactive-mode#built-in-commands), which execute fixed logic directly, bundled skills are prompt-based: they give Claude a detailed playbook and let it orchestrate the work using its tools. This means bundled skills can spawn parallel agents, read files, and adapt to your codebase."

  - *Implication*: Bundled skills are flexible but model-dependent; built-in commands are deterministic. This matters when reasoning about reliability and predictability.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

- **Anthropic SDK developer platform skill documented**: A new note describes a skill that activates automatically — no invocation required.

  > "Claude Code also includes a bundled developer platform skill that activates automatically when your code imports the Anthropic SDK. You don't need to invoke it manually."

  - *Implication*: Developers building on the Anthropic SDK get context-aware assistance loaded automatically at session start without any configuration.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md)

- **`features-overview.md` calls out all three bundled skills**: The Skills tab description now explicitly names `/simplify`, `/batch`, and `/debug`.

  > "Claude Code ships with [bundled skills](/en/skills#bundled-skills) like `/simplify`, `/batch`, and `/debug` that work out of the box."

  - *Source*: [Features Overview](https://code.claude.com/docs/en/features-overview.md)

---

### Terminology: "Slash Commands" → "Commands"

A consistent rename runs across all six modified pages, replacing "slash commands" and "custom slash commands" with "commands" in descriptive prose. The CLI flag `--disable-slash-commands` keeps its name (it is an identifier, not prose), but its description was updated to match.

| File | Old text | New text |
|---|---|---|
| `cli-reference.md` | "Disable all skills and **slash commands** for this session" | "Disable all skills and **commands** for this session" |
| `features-overview.md` | "invoke skills with a **slash command** like `/deploy`" | "invoke skills with a **command** like `/deploy`" |
| `hooks-guide.md` | "cannot trigger **slash commands** or tool calls" | "cannot trigger **commands** or tool calls" |
| `overview.md` | "Create **custom slash commands** to package repeatable workflows" | "Create **custom commands**" |
| `skills.md` (subtitle) | "Includes custom **slash commands**" | "Includes custom **commands** and bundled skills" |
| `skills.md` (note) | "Custom **slash commands** have been merged into skills" | "Custom **commands** have been merged into skills" |

- *Implication*: This is a documentation framing change only. The `/` invocation prefix and all existing commands are behaviorally unchanged.

---

## Notable Details

- The `interactive-mode.md` intro now explicitly notes that bundled skills (`/simplify`, `/batch`, `/debug`) appear alongside built-in commands in the `/` picker: "Claude Code also ships with [bundled skills](/en/skills#bundled-skills) like `/simplify`, `/batch`, and `/debug` that appear alongside built-in commands when you type `/`."
- `/diff` is described as showing "per-turn diffs" — diffs scoped to individual Claude turns — alongside the standard `git diff`. Left/right arrows switch between modes; up/down browse files.
- `/output-style` documents three built-in output modes: **Default** (standard), **Explanatory** (adds educational commentary on implementation choices), and **Learning** (pauses for hands-on practice). Custom output styles are also supported via `/en/output-styles#create-a-custom-output-style`.
- `/insights` generates a report covering "project areas, interaction patterns, and friction points" — a session analytics command with no previous documentation.
- `/passes` for sharing a free week of Claude Code is "only visible if your account is eligible," indicating the CLI applies per-account visibility logic.
- The `metadata.json` timestamp advanced from `00:25` to `06:18` UTC on 2026-03-01; page counts are unchanged (59 total, 58 successful, 1 failed).

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `interactive-mode.md` | Modified | +67 / -35 | Full rewrite of built-in commands table; 50+ commands with aliases, argument notation, and doc links |
| `skills.md` | Modified | +9 / -3 | `/debug` added as third bundled skill; prompt-based architecture explained; SDK auto-skill noted |
| `features-overview.md` | Modified | +2 / -2 | Bundled skills named explicitly; "slash command" → "command" |
| `cli-reference.md` | Modified | +1 / -1 | `--disable-slash-commands` description: "slash commands" → "commands" |
| `hooks-guide.md` | Modified | +1 / -1 | Hook limitation wording: "slash commands" → "commands" |
| `overview.md` | Modified | +1 / -1 | "custom slash commands" → "custom commands" |

---

*Generated from Claude Code CLI documentation changes detected on 2026-03-01*
