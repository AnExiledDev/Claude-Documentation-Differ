# Claude Code Documentation Changes — 2026-02-26

## Summary

One page was modified: the "Claude Code on the web" page. The primary change removes the `&` prefix syntax for launching remote web sessions from the terminal, replacing it entirely with the `--remote` flag. Associated terminology, section names, and code examples were updated throughout.

## Significant Changes

### Features / CLI Interface

- **`&` prefix syntax removed; `--remote` is now the sole terminal-to-web method**: The `&` message prefix for spawning remote web sessions from within Claude Code has been dropped. All documentation now directs users to `claude --remote "<task>"` as the canonical way to start a web session from the terminal.

  Old approach:
  > `& Fix the authentication bug in src/auth/login.ts`

  New approach:
  > ```bash
  > claude --remote "Fix the authentication bug in src/auth/login.ts"
  > ```

  - *Implication*: Developers using the `&` shorthand in scripts or workflows will need to migrate to `claude --remote`. The `--remote` flag was already documented as an alternative; it is now the only supported path.
  - *Source*: [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

- **"Tips for background tasks" section renamed to "Tips for remote tasks"**: The subsection containing workflow tips (plan-locally-execute-remotely, parallel task runs) was renamed to reflect the shift away from `&`-prefix "background" framing toward explicit `--remote` invocations.

  > Old: `#### Tips for background tasks` → New: `#### Tips for remote tasks`

  - *Implication*: The rename signals a conceptual clarification — these are remote cloud sessions, not background processes attached to a local terminal session.
  - *Source*: [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

- **Session handoff note updated**: The note clarifying one-way session handoff was reworded to remove the `&` reference and reframe scope.

  Old:
  > `The [`&` prefix](#from-terminal-to-web) creates a *new* web session with your current conversation context.`

  New:
  > `The `--remote` flag creates a *new* web session for your current repository.`

  - *Implication*: The phrasing change also shifts the framing — the new session is scoped to a *repository*, not a conversation context, which may indicate that `--remote` does not carry over local conversation history the way `&` previously did.
  - *Source*: [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

- **Parallel task example updated**: The parallel tasks tip previously showed `&` prefix commands run from within Claude Code; it now uses three separate `claude --remote` shell invocations.

  Old:
  > ```
  > & Fix the flaky test in auth.spec.ts
  > & Update the API documentation
  > & Refactor the logger to use structured output
  > ```

  New:
  > ```bash
  > claude --remote "Fix the flaky test in auth.spec.ts"
  > claude --remote "Update the API documentation"
  > claude --remote "Refactor the logger to use structured output"
  > ```

  - *Implication*: Each remote task is now a discrete shell command, which integrates more naturally into scripts and CI pipelines than the in-REPL `&` prefix.
  - *Source*: [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

## Notable Details

- **"iOS app" → "mobile app"**: Two references to "the Claude iOS app" were changed to "the Claude mobile app", broadening the language to include Android users (the Android app was already mentioned in the page intro). No functional change.

- **`/remote-env` note cleaned up**: The note about selecting a default environment from the terminal previously referenced both `&` and `--remote`; it now references only `--remote`. This keeps the `/remote-env` documentation consistent with the removal of `&`.

- **Plan-then-execute example is now self-contained**: The code example for the "plan locally, execute remotely" pattern previously used `& Execute the migration plan we discussed` — referencing the current conversation as context. The new example uses `claude --remote "Execute the migration plan in docs/migration-plan.md"`, pointing to a specific file path. This reflects that `--remote` starts a fresh session without conversation history, so the task prompt must be self-contained.

- **Intro paragraph reworded**: The summary description of the terminal↔web workflow changed from `send tasks from your terminal to run on the web with the & prefix` to `kick off new tasks on the web from your terminal with --remote`, consistently retiring the `&` framing across the entire page.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `claude-code-on-the-web.md` | Modified | +17 / -23 | Removed `&` prefix syntax throughout; `--remote` flag is now the sole method for launching remote web sessions from the terminal; tips section renamed from "background tasks" to "remote tasks" |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-26*
