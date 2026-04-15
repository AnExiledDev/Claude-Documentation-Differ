# Claude Code Documentation Changes — 2026-04-15

## Summary

Five pages were modified with a net addition of 77 lines. The largest change is a significant rewrite of the `REVIEW.md` customization guide in the Code Review docs, expanding it from a simple example into detailed tuning guidance. Additionally, two new environment variables for cloud session identification were documented, and sandbox Unix socket behavior on Linux/WSL2 was clarified.

## Significant Changes

### Features

- **Cloud session linking via `CLAUDE_CODE_REMOTE_SESSION_ID`**: Cloud sessions on claude.ai now expose their session ID through an environment variable, enabling Claude to embed traceable links to the session transcript in PR bodies, commit messages, Slack posts, or generated reports.
  > Each cloud session has a transcript URL on claude.ai, and the session can read its own ID from the `CLAUDE_CODE_REMOTE_SESSION_ID` environment variable. Use this to put a traceable link in PR bodies, commit messages, Slack posts, or generated reports so a reviewer can open the run that produced them.
  >
  > ```bash
  > echo "https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID}"
  > ```
  - *Implication*: Hooks and setup scripts can now construct direct audit-trail links from any cloud session output back to the run that produced it.
  - *Source*: [Claude Code on the Web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

- **`CLAUDE_CODE_REMOTE` env var for cloud detection**: A companion variable, set automatically to `true` when Claude Code runs as a cloud session.
  > Set automatically to `true` when Claude Code is running as a cloud session. Read this from a hook or setup script to detect whether you are in a cloud environment.
  - *Implication*: Hooks and startup scripts can now branch on local vs. cloud execution without relying on heuristics.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_TMUX_TRUECOLOR` for 24-bit color in tmux**: New opt-in variable to enable truecolor output inside tmux, which previously clamped to 256 colors by default.
  > Set to `1` to allow 24-bit truecolor output inside tmux. By default, Claude Code clamps to 256 colors when `$TMUX` is set because tmux does not pass through truecolor escape sequences unless configured to. Set this after adding `set -ga terminal-overrides ',*:Tc'` to your `~/.tmux.conf`.
  - *Implication*: Users with properly configured tmux truecolor pass-through can now get full color fidelity without workarounds.
  - *Source*: [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

### Code Review

- **`REVIEW.md` reframed as highest-priority system prompt injection**: The documentation now explicitly describes `REVIEW.md` as injected verbatim into every review agent's system prompt at highest priority, replacing the previous framing of both config files as "additive on top of the default correctness checks."
  > `REVIEW.md` is a file at your repository root that overrides how Code Review behaves on your repo. Its contents are injected into the system prompt of every agent in the review pipeline as the highest-priority instruction block, taking precedence over the default review guidance.
  - *Implication*: Teams can reliably enforce repo-specific severity calibration, nit caps, and skip rules — with the expectation these instructions supersede Claude's defaults.
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

- **`REVIEW.md` `@` import syntax is not expanded**: The docs now explicitly state that `@` file-import syntax (used in `CLAUDE.md`) does not work in `REVIEW.md`.
  > Because it's pasted verbatim, `REVIEW.md` is plain instructions: [`@` import syntax](/en/memory#import-additional-files) is not expanded, and referenced files are not read into the prompt. Put the rules you want enforced directly in the file.
  - *Implication*: Teams cannot reuse `@`-import patterns from `CLAUDE.md`; all rules must be stated inline in `REVIEW.md`.
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

- **New "What you can tune" section with 7 structured tuning categories**: The prior simple example list has been replaced with actionable guidance across: Severity, Nit volume, Skip rules, Repo-specific checks, Verification bar, Re-review convergence, and Summary shape.

  Notable highlights:
  - **Re-review convergence**: Instruct Claude to suppress new nits after the first review and post Important findings only, preventing style churn across revision rounds.
    > A rule like "after the first review, suppress new nits and post Important findings only" stops a one-line fix from reaching round seven on style alone.
  - **Verification bar**: Require a `file:line` citation before a finding is posted to reduce false positives.
    > "behavior claims need a `file:line` citation in the source, not an inference from naming" cuts false positives that would otherwise cost the author a round trip.
  - **Summary shape**: Request a tally line (e.g., `2 factual, 4 style`) at the top of the review body so authors understand the shape of feedback before the details.
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

- **Review results now include a summary in the review body**: A behavioral clarification was added to the how-it-works description.
  > The results are deduplicated, ranked by severity, and posted as inline comments on the specific lines where issues were found, **with a summary in the review body**.
  - *Implication*: Reviewers can read a top-level summary without scanning all inline comments.
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

- **Spend-cap troubleshooting section added**: New guidance explains what happens when a review is skipped because the monthly spend cap has been reached.
  > When your organization's monthly spend cap is reached, Code Review posts a single comment on the PR explaining that the review was skipped. Reviews resume automatically at the start of the next billing period, or immediately when an admin raises the cap at [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage).
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

- **Dashboard cost figures clarified as estimates**: A note was added to the analytics section.
  > Dashboard cost figures are estimates for monitoring activity; for invoice-accurate spend, refer to your Anthropic bill.
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

### Configuration

- **Sandbox Unix socket settings clarified for Linux and WSL2**: Both `network.allowUnixSockets` and `network.allowAllUnixSockets` received platform-specific annotations.

  | Setting | Before | After |
  |---------|--------|-------|
  | `network.allowUnixSockets` | "Unix socket paths accessible in sandbox" | Now marked **(macOS only)**; explicitly ignored on Linux and WSL2 where seccomp cannot inspect socket paths |
  | `network.allowAllUnixSockets` | "Allow all Unix socket connections in sandbox" | Now notes this is the **only** way to permit Unix sockets on Linux/WSL2, since it bypasses the seccomp filter that blocks `socket(AF_UNIX, ...)` calls |

  > On Linux and WSL2 this is the only way to permit Unix sockets, since it skips the seccomp filter that otherwise blocks `socket(AF_UNIX, ...)` calls.
  - *Implication*: Linux and WSL2 users who previously set `network.allowUnixSockets` with specific paths were likely getting no effect; `network.allowAllUnixSockets: true` is required on those platforms.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Integrations

- **JetBrains diff tool options clarified**: The `/config` diff tool guidance now names both options explicitly.

  Before: *"Set the diff tool to `auto` for automatic IDE detection"*

  After:
  > Set the diff tool to `auto` to show diffs in the IDE, or `terminal` to keep them in the terminal.
  - *Implication*: The `terminal` option was previously undocumented in this context; users who prefer terminal-based diffs now have a documented path.
  - *Source*: [JetBrains](https://code.claude.com/docs/en/jetbrains.md)

## Notable Details

- The `CLAUDE.md` description in the Code Review customization section was semantically repositioned. Previously both files were described as "additive on top of default correctness checks." Now they "differ in how strongly they influence the review" — `CLAUDE.md` violations appear as nits, `REVIEW.md` is injected as highest-priority instructions. This is a meaningful distinction for teams deciding which file to use for enforcement vs. context.
- The link from "nit-level" in the CLAUDE.md description now anchors to `#severity-levels`, pointing to a dedicated severity-levels section on the Code Review page.
- The "Keep it focused" note added at the end of the REVIEW.md section signals an intentional design principle: length dilutes the rules that matter most.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `code-review.md` | Modified | +61 / -24 | Major rewrite of REVIEW.md guidance; new tuning categories, revised example, spend-cap troubleshooting, review summary in body |
| `claude-code-on-the-web.md` | Modified | +10 / -0 | New section: linking artifacts to cloud sessions via `CLAUDE_CODE_REMOTE_SESSION_ID` |
| `env-vars.md` | Modified | +3 / -0 | Added `CLAUDE_CODE_REMOTE`, `CLAUDE_CODE_REMOTE_SESSION_ID`, and `CLAUDE_CODE_TMUX_TRUECOLOR` |
| `settings.md` | Modified | +2 / -2 | Clarified Unix socket sandbox settings: `allowUnixSockets` is macOS-only; `allowAllUnixSockets` required on Linux/WSL2 |
| `jetbrains.md` | Modified | +1 / -1 | Clarified `auto` vs `terminal` diff tool options |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-15*
