# Claude Code Documentation Changes — 2026-05-20

## Summary

Three new documentation pages were added: a dedicated sessions management reference, a prompt library, and a guide for CLI maintainers to emit plugin installation hints. The checkpointing and interactive-mode pages were updated to clarify the dual behavior of `Esc`+`Esc`, and the plugin-marketplaces validation section was restructured to distinguish marketplace-level from plugin-level validation.

## Significant Changes

### Plugin Ecosystem

- **New: Plugin Hints Protocol for CLI Maintainers**: A new page documents how CLI and SDK authors can prompt Claude Code users to install an official plugin. The mechanism uses a self-closing XML tag written to stderr when `CLAUDECODE=1` is detected.
  > "Your CLI writes a one-line marker to stderr when it detects it is running inside Claude Code. Claude Code reads the marker, strips it from the output, and shows the user a one-time install prompt."
  > "Claude Code strips the hint line from the command output before sending it to the model, so the marker never appears in the conversation and is not counted toward token usage."
  - *Protocol format*: `<claude-code-hint v="1" type="plugin" value="example-cli@claude-plugins-official" />` — three required attributes (`v`, `type`, `value`), gated on the `CLAUDECODE` env var
  - *Scope restriction*: Only plugins in official Anthropic-controlled marketplaces (e.g., `claude-plugins-official`) trigger the prompt; hints pointing to community or third-party marketplaces are silently dropped
  - *Frequency limits*: Once per plugin (never re-prompted regardless of user's answer) and once per session across all CLIs
  - *Implication*: CLI maintainers working with an Anthropic partner contact can wire their tools to surface plugin discovery to Claude Code users without modifying prompt output or token usage
  - *Source*: [Plugin Hints](https://code.claude.com/docs/en/plugin-hints.md)

- **Updated: Plugin Marketplace Validation Scope Clarified**: The `claude plugin validate` / `/plugin validate` command's behavior when run against a marketplace directory versus a plugin directory is now explicitly distinguished.
  > "When pointed at a marketplace directory, the validator checks `marketplace.json` only: schema, duplicate plugin names, source path traversal, and version mismatches against each referenced `plugin.json`."
  > "To validate an individual plugin's `plugin.json` and its skill, agent, command, and hook files, run the command against the plugin directory itself, for example `claude plugin validate ./plugins/my-plugin`."
  - Error table rows for `YAML frontmatter failed to parse` and `Invalid JSON syntax (hooks.json)` now note they are "Reported only when validating a plugin directory"
  - The troubleshooting entry for "marketplace can't be loaded" was updated to specify that frontmatter validation requires running against each plugin directory, not the marketplace root
  - *Implication*: Marketplace authors who expected `validate .` to catch frontmatter errors in their plugins will need to run the validator separately against each plugin subdirectory
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

### Session Management

- **New: Sessions Reference Page**: A dedicated page covering all aspects of session lifecycle in the CLI, consolidating what was previously scattered across other pages.
  > "A session is a saved conversation tied to a project directory. Claude Code stores it locally as you work, so you can resume where you left off, branch to try a different approach, or switch between tasks."
  - Covers `--continue`, `--resume`, `--resume <name>`, `--from-pr <number>`, and `/resume` in a single reference table
  - Documents the session picker's keyboard shortcuts including `Ctrl+W` (widen to all worktrees), `Ctrl+A` (all projects), `Ctrl+B` (filter by branch), and PR URL paste-to-search
  - Documents `/branch` and `--fork-session` for creating diverging conversation copies
  - Transcript location: `~/.claude/projects/<project>/<session-id>.jsonl`; configurable retention via `cleanupPeriodDays`; suppression via `CLAUDE_CODE_SKIP_PROMPT_HISTORY` or `--no-session-persistence`
  - Session naming via `claude -n <name>`, `/rename`, or automatic naming from accepted plan content
  - *Implication*: Developers managing parallel workstreams have a single authoritative reference for session navigation and naming
  - *Source*: [Sessions](https://code.claude.com/docs/en/sessions.md)

### Checkpointing

- **Updated: `Esc`+`Esc` Behavior Clarified**: The checkpointing page previously implied double-`Esc` always opened the rewind menu. A new `<Note>` block clarifies the input-state dependency.
  > "If the prompt input contains text, double `Esc` clears it instead of opening the menu. The cleared text is saved to your input history, so press `Up` to recall it after you finish in the rewind menu."
  - *Implication*: Users who were confused by `Esc`+`Esc` not opening the rewind menu (because they had text in the prompt) now have explicit documentation explaining the fallback behavior
  - *Source*: [Checkpointing](https://code.claude.com/docs/en/checkpointing.md)

### Features

- **New: Prompt Library**: A new page provides a searchable collection of copy-paste prompts organized by SDLC phase (Discover, Design, Build, Ship, Operate) and role (PM, design, ops, security, docs, etc.). Prompts cover onboarding, code understanding, planning, implementation, testing, review, refactoring, debugging, incidents, and compliance workflows — each with placeholder slots and links to related documentation.
  - *Implication*: Teams onboarding to Claude Code have a structured prompt catalog as a starting point, with role-specific filtering (e.g., PM-only prompts for spec drafting, ops-only prompts for incident response)
  - *Source*: [Prompt Library](https://code.claude.com/docs/en/prompt-library.md)

## Minor Changes

- **interactive-mode.md**: `Ctrl+C` description updated from "Cancel current input or generation" to "Interrupt, or clear input" with expanded context (first press clears prompt input; second press exits Claude Code when nothing is running). `Esc`+`Esc` description updated from "Rewind or summarize" to "Clear input draft, or rewind" to reflect the input-state-dependent dual behavior (+2/-2 lines)

## New Pages

- **plugin-hints.md** — Protocol reference for CLI/SDK maintainers to emit `<claude-code-hint />` tags that trigger Claude Code plugin install prompts. Covers tag format, code examples in Node.js/Python/Go/Shell, placement recommendations, user-facing UI, enforcement rules, and how to get a plugin into the official marketplace. [View](https://code.claude.com/docs/en/plugin-hints.md)
- **prompt-library.md** — Interactive prompt library with copy-paste prompts tagged by SDLC phase and role. Implemented as a React component with filter/search UI in docs. [View](https://code.claude.com/docs/en/prompt-library.md)
- **sessions.md** — Complete CLI session management reference: resuming sessions by flag/name/PR, the `/resume` session picker with keyboard shortcuts, session naming, branching with `/branch` and `--fork-session`, context management commands, and transcript export/storage details. [View](https://code.claude.com/docs/en/sessions.md)

## Notable Details

- The plugin hints protocol explicitly gates on the `CLAUDECODE` environment variable (not a new variable — it already existed — but this is the first documentation of a programmatic use case for it beyond Claude's own internal detection).
- The `--from-pr <number>` flag for resuming sessions linked to pull requests is documented in the new sessions page; this capability was not prominently surfaced before.
- In the sessions picker, pasting a GitHub, GitHub Enterprise, GitLab, or Bitbucket PR/MR URL into the search field finds the session that created it — a useful workflow for returning to the context where a PR was opened.
- `Ctrl+B` in the session picker filters by current branch (not to be confused with `Ctrl+B` in the main interface which backgrounds bash commands).
- The `checkpointing.md` note cross-links to the new sessions page (`/en/sessions#branch-a-session`) for fork-based alternatives to summarize, indicating the sessions page is intended as the canonical reference for session branching.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| plugin-hints.md | New | SIGNIFICANT | +148 | Plugin hint protocol for CLI maintainers |
| sessions.md | New | SIGNIFICANT | +125 | Dedicated session management reference |
| prompt-library.md | New | SIGNIFICANT | +1389 | Copy-paste prompt library by SDLC phase and role |
| plugin-marketplaces.md | Modified | SIGNIFICANT | +12/-10 | Validation command scope clarified for marketplace vs plugin directories |
| checkpointing.md | Modified | SIGNIFICANT | +7/-1 | `Esc`+`Esc` input-state behavior documented with new Note block |
| interactive-mode.md | Modified | MINOR | +2/-2 | `Ctrl+C` and `Esc`+`Esc` descriptions updated |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-20*
