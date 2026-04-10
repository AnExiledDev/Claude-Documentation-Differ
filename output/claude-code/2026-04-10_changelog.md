# Claude Code Documentation Changes — 2026-04-10

## Summary

Eight pages were modified (102 additions, 23 deletions). The most significant changes are a major overhaul of `/loop` scheduled-task behavior — both the interval and prompt are now optional, with new dynamic-interval and built-in maintenance modes — plus the graduation of server-managed settings from public beta to GA. Additional updates clarify Bash tool `cd` persistence, hooks config structure, automatic screenshot downscaling for computer use, and a Windows TLS error code.

## Significant Changes

### Features

- **`/loop` now supports fully optional arguments and new operating modes**: The command signature changed from `[interval] <prompt>` (prompt required) to `[interval] [prompt]` (both optional). This unlocks two new behaviors alongside the existing fixed-interval mode:

  | What you provide | Example | What happens |
  |---|---|---|
  | Interval + prompt | `/loop 5m check the deploy` | Runs on a fixed cron schedule |
  | Prompt only | `/loop check the deploy` | Claude self-selects the interval each iteration |
  | Nothing (or interval only) | `/loop` | Built-in maintenance prompt runs, or `.claude/loop.md` if present |

  > When you omit the interval, Claude chooses one dynamically instead of running on a fixed cron schedule. After each iteration it picks a delay between one minute and one hour based on what it observed: short waits while a build is finishing or a PR is active, longer waits when nothing is pending.

  - *Implication*: `/loop` can now operate as a continuous autonomous agent with no arguments — useful for PR babysitting or release-branch maintenance without specifying exactly what to check each iteration.
  - *Source*: [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks.md), [Commands](https://code.claude.com/docs/en/commands.md)

- **Built-in maintenance prompt for bare `/loop`**: Omitting the prompt entirely causes Claude to run a built-in maintenance pass on each iteration: continuing unfinished work, tending to the current branch's PR (review comments, CI failures, merge conflicts), and running cleanup passes (bug hunts, simplification) when nothing else is pending.

  > Claude does not start new initiatives outside that scope, and irreversible actions such as pushing or deleting only proceed when they continue something the transcript already authorized.

  - *Implication*: Bare `/loop` is now safe to run on an active branch — Claude won't take unsanctioned destructive actions.
  - *Source*: [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks.md)

- **`loop.md` file for customizing the default `/loop` prompt**: A `loop.md` file at `.claude/loop.md` (project-level) or `~/.claude/loop.md` (user-level) replaces the built-in maintenance prompt when running bare `/loop`. Project-level takes precedence. The file is plain Markdown; content beyond 25,000 bytes is truncated. Edits take effect on the next iteration.

  > A `loop.md` file replaces the built-in maintenance prompt with your own instructions. It defines a single default prompt for bare `/loop`, not a list of separate scheduled tasks, and is ignored whenever you supply a prompt on the command line.

  - *Implication*: Teams can commit `.claude/loop.md` to standardize what autonomous maintenance loops do across contributors — for example, keeping a release branch healthy on a fixed checklist.
  - *Source*: [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks.md)

- **Computer Use: screenshots are downscaled automatically**: A new section documents that Claude Code downscales every screenshot before sending it to the model. There is no setting to change the target size; content that appears too small after downscaling should be enlarged in the app rather than by lowering display resolution.

  > Claude Code downscales every screenshot before sending it to the model. You don't need to lower your display resolution or resize windows on Retina or other high-resolution displays. A 16-inch MacBook Pro at native Retina resolution captures at 3456×2234 and downscales to roughly 1372×887, preserving aspect ratio.

  - *Implication*: Developers on high-DPI displays no longer need to manually reduce resolution or window size for computer-use tasks; the downscaling is transparent and automatic.
  - *Source*: [Computer Use](https://code.claude.com/docs/en/computer-use.md)

### Configuration

- **Bash tool `cd` persistence behavior documented in detail**: The tools reference previously described `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` in a single bullet. It now explains the full behavior: `cd` carries over to subsequent Bash commands as long as the new directory stays within the project root or an added working directory; if it lands outside, Claude Code resets to the project directory and appends `Shell cwd was reset to <dir>` to the tool result.

  > When Claude runs `cd`, the new working directory carries over to later Bash commands as long as it stays inside the project directory or an additional working directory you added with `--add-dir`, `/add-dir`, or `additionalDirectories` in settings. If `cd` lands outside those directories, Claude Code resets to the project directory and appends `Shell cwd was reset to <dir>` to the tool result.

  - *Implication*: Clarifies why `cd` may silently reset — important for debugging bash hook or tool sequences that change directories.
  - *Source*: [Tools Reference](https://code.claude.com/docs/en/tools-reference.md)

- **Hooks guide: concrete multi-event JSON example added**: The instruction for merging a new hook into an existing config previously gave only prose guidance ("merge the `Notification` entry into it"). It now includes a complete JSON example showing `PostToolUse` and `Notification` as sibling keys inside a single `hooks` object.

  > If your settings file already has a `hooks` key, add `Notification` as a sibling of the existing event keys rather than replacing the whole object. Each event name is a key inside the single `hooks` object.

  - *Implication*: Reduces a common misconfiguration where users inadvertently overwrite an existing `PostToolUse` block when adding a `Notification` hook.
  - *Source*: [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)

### Platform / Integrations

- **Server-managed settings graduates from public beta**: The page title changed from "Configure server-managed settings (public beta)" to "Configure server-managed settings". The note no longer says "Features may evolve before general availability," and the limitations section no longer qualifies them as beta-period limitations.

  > Server-managed settings are available for Claude for Teams and Claude for Enterprise customers.

  - *Implication*: Organizations that were waiting on beta stability before deploying centralized config can proceed — this feature is now GA.
  - *Source*: [Server-Managed Settings](https://code.claude.com/docs/en/server-managed-settings.md)

## Notable Details

- **`/loop` on Bedrock, Vertex AI, and Microsoft Foundry behaves differently**: Dynamic-interval mode is unavailable on these platforms — prompts without an explicit interval fall back to a fixed 10-minute schedule. Bare `/loop` with no prompt prints the usage message rather than starting the maintenance loop.

- **`:*` wildcard suffix deprecation quietly reversed**: The permissions page previously stated "the legacy `:*` suffix syntax is equivalent to ` *` but is deprecated." The new text reads: "The `:*` suffix is an equivalent way to write a trailing wildcard. `Bash(ls:*)` matches the same commands as `Bash(ls *)`." The deprecation label is gone. Developers who avoided `:*` based on the old text can now use it freely.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md)

- **Windows TLS troubleshooting covers an additional error code**: `CRYPT_E_NO_REVOCATION_CHECK (0x80092012)` was added alongside the existing `CRYPT_E_REVOCATION_OFFLINE (0x80092013)` as a trigger for using `--ssl-revoke-best-effort` during installation on corporate networks.
  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| scheduled-tasks.md | Modified | +65 / -15 | Major `/loop` rewrite: both args optional, dynamic interval, built-in maintenance prompt, `loop.md` customization |
| hooks-guide.md | Modified | +22 / -1 | Added multi-event JSON example for merging hook configs |
| computer-use.md | Modified | +6 / -0 | New section documenting automatic screenshot downscaling on high-DPI displays |
| server-managed-settings.md | Modified | +3 / -3 | Removed "public beta" label — feature is now GA |
| tools-reference.md | Modified | +3 / -1 | Expanded `cd` carry-over and reset behavior for the Bash tool |
| commands.md | Modified | +1 / -1 | `/loop` signature updated to `[interval] [prompt]` with expanded description |
| permissions.md | Modified | +1 / -1 | Removed `:*` deprecation notice; now documented as a valid equivalent syntax |
| troubleshooting.md | Modified | +1 / -1 | Added `CRYPT_E_NO_REVOCATION_CHECK` to Windows TLS certificate error guidance |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-10*
