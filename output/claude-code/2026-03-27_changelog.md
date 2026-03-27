# Claude Code Documentation Changes — 2026-03-27

## Summary

Nine pages were modified in this update (240 additions, 136 deletions), with no new or removed pages. The largest changes land in the hooks system: the reference page gained a complete hook-resolution walkthrough and documentation for the new `if` field for per-handler filtering, while the hooks guide adds a corresponding new section. The settings page was significantly revised with several new settings entries and a Windows managed-settings migration notice tied to v2.1.75.

## Significant Changes

### Hooks

- **New `if` field for per-hook-handler filtering**: Hook handlers now support an `if` field using permission rule syntax to filter which tool calls spawn a given handler. Unlike `matcher` (which filters at the matcher-group level by tool name), `if` evaluates the tool name and arguments together, allowing finer-grained process-spawn avoidance.
  > "`if`: Permission rule syntax to filter when this hook runs, such as `'Bash(git *)'` or `'Edit(*.ts)'`. The hook only spawns if the tool call matches the pattern. Only evaluated on tool events: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, and `PermissionRequest`. On other events, a hook with `if` set never runs."
  - *Implication*: Developers can now skip spawning a hook process entirely when the command arguments don't match, reducing overhead for hooks that should only run on specific patterns (for example, blocking `rm -rf` without spawning a script for every `rm` call).
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **Hook resolution walkthrough added to reference**: The hooks reference page added a step-by-step "How a hook resolves" section with an annotated diagram (`hook-resolution.svg`) tracing the full sequence: event fires → matcher checks → `if` condition checks → handler runs → Claude Code acts on result.
  > "The `if` condition `'Bash(rm *)'` matches because the command starts with `rm`, so this handler spawns. If the command had been `npm test`, the `if` check would fail and `block-rm.sh` would never run, avoiding the process spawn overhead. The `if` field is optional; without it, every handler in the matched group runs."
  - *Implication*: The walkthrough clarifies the two-level filtering (matcher then `if`) and when hooks do and do not fire.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **Hooks guide: new section on `if` field filtering**: The hooks guide added a new subsection covering the `if` field, with examples showing how it works in combination with `matcher`.
  - *Implication*: New users setting up hooks via the guide will now see `if` field filtering presented as part of the standard workflow.
  - *Source*: [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)

### Configuration / Settings

- **`showClearContextOnPlanAccept` setting added**: A new boolean setting controls whether the "clear context" option appears on the plan accept screen. It defaults to `false`, meaning the option is now hidden by default.
  > "`showClearContextOnPlanAccept` — Show the 'clear context' option on the plan accept screen. Defaults to `false`. Set to `true` to restore the option."
  - *Implication*: Users who relied on clearing context after accepting a plan must now opt back in by setting this to `true`.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`feedbackSurveyRate` setting added**: A new setting controls the probability (0–1) that a session quality survey appears after a session ends.
  > "`feedbackSurveyRate` — Probability (0–1) that the session quality survey appears when eligible. Set to `0` to suppress entirely. Useful when using Bedrock, Vertex, or Foundry where the default sample rate does not apply."
  - *Implication*: Bedrock, Vertex, and Foundry deployments can now explicitly suppress or tune survey frequency.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`fastModePerSessionOptIn` setting added**: When `true`, fast mode does not persist across sessions and users must re-enable it with `/fast` each session.
  > "`fastModePerSessionOptIn` — When `true`, fast mode does not persist across sessions. Each session starts with fast mode off, requiring users to enable it with `/fast`. The user's fast mode preference is still saved."
  - *Implication*: Administrators can enforce explicit per-session opt-in to fast mode, useful for cost control.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **`spinnerTipsOverride` setting added**: Organizations can now replace or supplement built-in spinner tips with custom strings.
  > "`spinnerTipsOverride` — Override spinner tips with custom strings. `tips`: array of tip strings. `excludeDefault`: if `true`, only show custom tips; if `false` or absent, custom tips are merged with built-in tips."
  - *Implication*: Enterprise deployments can use the spinner tip area to surface organization-specific guidance.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **Legacy Windows managed settings path deprecated as of v2.1.75**: A new warning block in the settings page documents a required migration for Windows administrators.
  > "The legacy Windows path `C:\ProgramData\ClaudeCode\managed-settings.json` is no longer supported as of v2.1.75. Administrators who deployed settings to that location must migrate files to `C:\Program Files\ClaudeCode\managed-settings.json`."
  - *Implication*: Windows enterprise deployments on v2.1.75+ that have not migrated will silently stop receiving managed settings.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Directory Explorer

- **"API credentials" example added to `.worktreeinclude` documentation**: The `.claude` directory explorer page added a new section in the `.worktreeinclude` example showing `config/secrets.json` listed under an `# API credentials` comment.
  > ```
  > # API credentials
  > config/secrets.json
  > ```
  - *Implication*: The explorer now explicitly documents that `.worktreeinclude` supports credential file patterns alongside the pre-existing `.env` example.
  - *Source*: [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory.md)

### MCP

- **Clearer `--` separator guidance for stdio server commands**: The MCP page was updated to more prominently explain that all `claude mcp add` options must come before the server name, and `--` separates the server name from the command passed to the MCP server.
  > "All options (`--transport`, `--env`, `--scope`, `--header`) must come **before** the server name. The `--` (double dash) then separates the server name from the command and arguments that get passed to the MCP server."
  - *Implication*: Reduces a common configuration error where server-level flags are misinterpreted as Claude CLI flags.
  - *Source*: [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp.md)

## Notable Details

- The hooks reference `if` field documentation explicitly notes that on non-tool events (e.g., `SessionStart`, `Stop`), a hook handler with `if` set **never runs** — this is a silent no-op, not an error. Developers adding `if` conditions to non-tool event hooks will find those handlers inactive.
- `showClearContextOnPlanAccept` defaults to `false`, which is a behavior change: the "clear context" option after plan acceptance was previously visible and is now hidden unless opted in.
- The Windows managed settings migration (`C:\ProgramData` → `C:\Program Files`) is scoped to v2.1.75+. Installations below that version are unaffected but must plan for the migration.
- `interactive-mode.md` lost exactly 4 lines with no additions and no new sections, consistent with removal of a deprecated note or shortcut entry.
- `env-vars.md` had a single-line change (+1/-1), most likely a wording correction to an existing variable description rather than a new variable.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| claude-directory.md | Modified | +48/-17 | Added "API credentials" section to `.worktreeinclude` example; expanded explorer entries |
| hooks-guide.md | Modified | +33/-0 | New section documenting `if` field for per-handler filtering |
| settings.md | Modified | +63/-59 | New settings: `showClearContextOnPlanAccept`, `feedbackSurveyRate`, `fastModePerSessionOptIn`, `spinnerTipsOverride`; Windows legacy path deprecation warning added |
| hooks.md | Modified | +41/-20 | New hook resolution walkthrough with diagram; `if` field documented in common handler fields table |
| monitoring-usage.md | Modified | +25/-25 | Content reorganized; equal additions/deletions indicate rewriting rather than net expansion |
| mcp.md | Modified | +17/-8 | Clarified `--` separator for stdio server commands; plugin MCP section updated |
| common-workflows.md | Modified | +12/-2 | Minor workflow step additions |
| interactive-mode.md | Modified | +0/-4 | Removed content (deprecated note or shortcut entry) |
| env-vars.md | Modified | +1/-1 | Single-line wording correction |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-27*
