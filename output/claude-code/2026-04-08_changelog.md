# Claude Code Documentation Changes — 2026-04-08

## Summary

This update is dominated by a major new feature: Amazon Bedrock Mantle endpoint support, documented across four pages (amazon-bedrock, env-vars, model-config, troubleshooting). Alongside this, the `~/.claude` directory reference gained a full new "Application data" section covering transcript storage, retention, and data clearing, and hooks documentation was overhauled to clarify how debug output reaches developers. Version 2.1.94 changelog entries also landed.

---

## Significant Changes

### Features

- **Amazon Bedrock Mantle Endpoint**: A new AWS endpoint that serves Claude models using the native Anthropic API shape (rather than the Bedrock Invoke API), while reusing existing AWS credentials and IAM permissions. Requires Claude Code v2.1.94 or later.

  > *"Mantle is an Amazon Bedrock endpoint that serves Claude models through the native Anthropic API shape rather than the Bedrock Invoke API. It uses the same AWS credentials, IAM permissions, and `awsAuthRefresh` configuration described earlier on this page."*

  Activation is as simple as:
  ```bash
  export CLAUDE_CODE_USE_MANTLE=1
  export AWS_REGION=us-east-1
  ```

  - Run `/status` to confirm; the provider line reads `Amazon Bedrock (Mantle)` when active.
  - Mantle model IDs use the `anthropic.` prefix without a version suffix (e.g. `anthropic.claude-haiku-4-5`), distinct from the standard Bedrock catalog.
  - **Mixed-mode supported**: Setting both `CLAUDE_CODE_USE_BEDROCK=1` and `CLAUDE_CODE_USE_MANTLE=1` lets Claude Code route requests to whichever endpoint has the requested model, with `/status` showing `Amazon Bedrock + Amazon Bedrock (Mantle)`.
  - **Gateway support**: Use `CLAUDE_CODE_SKIP_MANTLE_AUTH=1` to disable client-side SigV4 signing when routing through an LLM gateway.
  - *Implication*: Enterprise/team users with existing Bedrock deployments can opt into the native API shape without new credentials; model IDs with `anthropic.` prefix listed in `availableModels` are automatically routed to Mantle.
  - *Source*: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md)

- **`UserPromptSubmit` hook: `sessionTitle` output field**: Hooks responding to `UserPromptSubmit` events can now set the session title by returning `sessionTitle` in `hookSpecificOutput`, equivalent to running `/rename`.

  > *"`sessionTitle`: Sets the session title, same effect as `/rename`. Use to name sessions automatically based on the prompt content"*

  ```json
  {
    "hookSpecificOutput": {
      "hookEventName": "UserPromptSubmit",
      "additionalContext": "My additional context here",
      "sessionTitle": "My session title"
    }
  }
  ```

  - *Implication*: Hooks can now programmatically name sessions as they start, useful for auto-labeling sessions by project, ticket number, or prompt keyword.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

- **Code review: Rate and reply to findings**: GitHub PR review comments from Claude now include pre-attached 👍/👎 reactions for one-click feedback.

  > *"Each review comment from Claude arrives with 👍 and 👎 already attached so both buttons appear in the GitHub UI for one-click rating. Click 👍 if the finding was useful or 👎 if it was wrong or noisy. Anthropic collects reaction counts after the PR merges and uses them to tune the reviewer."*

  - Replying inline to a comment does not re-trigger Claude; to get a fresh review without pushing, use `@claude review once` as a top-level PR comment.
  - *Implication*: Direct in-PR feedback loop for improving review quality over time.
  - *Source*: [Code review](https://code.claude.com/docs/en/code-review.md)

- **Plugin skills: stable invocation name via frontmatter**: When a skill path points to a directory containing `SKILL.md` directly (e.g. `"skills": ["./"]`), the `name` field in the frontmatter is now used as the invocation name rather than the directory basename.

  > *"When a skill path points to a directory that contains a `SKILL.md` directly, for example `'skills': ['./']` pointing to the plugin root, the frontmatter `name` field in `SKILL.md` determines the skill's invocation name. This gives a stable name regardless of the install directory."*

  - *Implication*: Plugin skills now have portable, install-path-independent invocation names; previously the name depended on where the plugin was cloned.
  - *Source*: [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md)

- **Output styles: plugins can ship styles**: Plugins can now include an `output-styles/` directory, making output styles a distributable plugin component.

  > *"[Plugins](/en/plugins-reference) can also ship output styles in an `output-styles/` directory."*

  - *Source*: [Output styles](https://code.claude.com/docs/en/output-styles.md)

---

### Configuration & Environment Variables

- **Three new Mantle environment variables** added to the env-vars reference:

  | Variable | Purpose |
  |---|---|
  | `CLAUDE_CODE_USE_MANTLE` | Enable the Mantle endpoint (set to `1` or `true`) |
  | `ANTHROPIC_BEDROCK_MANTLE_BASE_URL` | Override the default Mantle endpoint URL |
  | `CLAUDE_CODE_SKIP_MANTLE_AUTH` | Skip client-side auth for proxy/gateway setups |

  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **Timeout variables now document their defaults**: `API_TIMEOUT_MS`, `BASH_DEFAULT_TIMEOUT_MS`, `BASH_MAX_TIMEOUT_MS`, `MCP_TIMEOUT`, and `MCP_TOOL_TIMEOUT` now include explicit default values in their descriptions. Notably:
  - `API_TIMEOUT_MS` now documents a **maximum value of 2147483647**; values above this overflow the underlying timer and cause requests to fail immediately.
  - `BASH_DEFAULT_TIMEOUT_MS`: default 120000 (2 minutes)
  - `BASH_MAX_TIMEOUT_MS`: default 600000 (10 minutes)
  - `MCP_TIMEOUT`: default 30000 (30 seconds)
  - `MCP_TOOL_TIMEOUT`: default 100000000 (~28 hours)
  - *Implication*: The `API_TIMEOUT_MS` overflow warning is a meaningful safety note — values set higher than ~2.1 billion will silently break rather than extend the timeout.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **Default effort level changed for most users**: The effort level documentation was updated to reflect that only Pro and Max subscribers default to medium effort; all other users (API key, Team, Enterprise, Bedrock, Vertex AI, Foundry) now default to **high effort**.

  > *"The default effort level depends on your plan. Pro and Max subscribers default to medium effort. All other users default to high effort: API key, Team, Enterprise, and third-party provider (Bedrock, Vertex AI, Foundry) users."*

  - Also: "ultrathink" in a prompt now has no effect if the session is already at high or max effort.
  - *Implication*: This is a behavioral change for non-Pro/Max users — they will consume more tokens per request by default without any configuration change.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

---

### Hooks Debugging Overhaul

The hooks documentation received a significant rewrite around how hook output reaches developers, replacing "verbose mode (`Ctrl+O`)" with a more precise model using the debug log file.

- **Hook stdout behavior clarified**: Plain stdout on exit 0 now goes to the **debug log**, not the verbose transcript.

  > *"For most events, stdout is written to the debug log but not shown in the transcript."*

  Previously the docs said stdout was "only shown in verbose mode (`Ctrl+O`)". This is a documentation correction that reflects actual runtime behavior.

- **Non-blocking errors (non-0, non-2 exit codes)**: The transcript now shows a one-line `<hook name> hook error` notice instead of sending stderr to verbose mode.

  > *"Any other exit code is a non-blocking error for most hook events. The transcript shows a one-line `<hook name> hook error` notice and execution continues. The full stderr is written to the debug log."*

- **New debug guidance**: The recommended debug workflow now uses `--debug-file`:

  > *"Start Claude Code with `claude --debug-file /tmp/claude.log` to write to a known path, then `tail -f /tmp/claude.log` in another terminal. If you started without that flag, run `/debug` mid-session to enable logging and find the log path."*

- **`suppressOutput` JSON field**: The description was corrected from "hides stdout from verbose mode output" to "omits stdout from the debug log".

- **Exit code 1 clarification** — a new warning block was added:

  > *"For most hook events, only exit code 2 blocks the action. Claude Code treats exit code 1 as a non-blocking error and proceeds with the action, even though 1 is the conventional Unix failure code. If your hook is meant to enforce a policy, use `exit 2`. The exception is `WorktreeCreate`, where any non-zero exit code aborts worktree creation."*

  - *Implication*: Hook authors relying on `exit 1` to block actions were silently broken; only `exit 2` blocks. This is important for policy-enforcement hooks.
  - *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md), [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)

---

### Data Storage & Privacy

- **New `~/.claude` Application Data section**: The `claude-directory.md` reference gained a comprehensive new section documenting every file Claude Code writes at runtime, organized into "swept automatically" (default: 30 days) and "not swept" (persist until deleted) categories.

  Swept automatically:
  | Path | Contents |
  |---|---|
  | `projects/<project>/<session>.jsonl` | Full conversation transcript |
  | `projects/<project>/<session>/tool-results/` | Large spilled tool outputs |
  | `file-history/<session>/` | Pre-edit file snapshots for checkpoint restore |
  | `plans/` | Plan mode plan files |
  | `debug/` | Per-session debug logs |
  | `paste-cache/`, `image-cache/` | Large pastes and attached images |

  Not swept (persists until manually deleted):
  | Path | Contents |
  |---|---|
  | `history.jsonl` | Every typed prompt with timestamp; used for up-arrow recall |
  | `statsig/` | Feature-flag cache and stable anonymous device ID |
  | `stats-cache.json` | Token/cost counts shown by `/cost` |
  | `todos/` | Legacy per-session task lists (no longer written; safe to delete) |

  - **Plaintext storage warning**: Transcripts are not encrypted at rest. Credentials read from `.env` files or printed by commands are written to `projects/<project>/<session>.jsonl`. Options to reduce exposure: lower `cleanupPeriodDays`, use `--no-session-persistence` in headless mode, or use permission rules to deny credential file reads.
  - *Source*: [`.claude` directory](https://code.claude.com/docs/en/claude-directory.md)

- **Data usage page updated**: The local caching description was updated to point to the new Application Data section and confirm transcripts are stored in plaintext:

  > *"Claude Code clients store session transcripts locally in plaintext under `~/.claude/projects/` for 30 days by default (configurable via `cleanupPeriodDays`) to enable session resumption."*

  - *Source*: [Data usage](https://code.claude.com/docs/en/data-usage.md)

---

### Keybindings & UI

- **`Ctrl+L` rebinding**: `Ctrl+L` was previously bound to `app:redraw` ("Redraw the screen"). It is now bound to `chat:clearInput` ("Clear prompt input — clears typed text, keeps conversation history"). The redraw action (`app:redraw`) is now **unbound** by default.

  > *"`chat:clearInput` | Ctrl+L | Clear prompt input"*

  - *Implication*: Users who relied on `Ctrl+L` to repaint the terminal will need to rebind `app:redraw` manually. The new default aligns with shell readline behavior where `Ctrl+L` clears the line.
  - *Source*: [Keybindings](https://code.claude.com/docs/en/keybindings.md)

---

### Troubleshooting

- **New "Model not found or not accessible" entry**: Step-by-step guide for resolving model resolution errors, including priority order for where the model setting is read and how to clear a stale value.

  > *"To clear a stale value, remove the `model` field from your settings or unset `ANTHROPIC_MODEL`, and Claude Code will fall back to the default model for your account."*

  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

- **macOS Keychain login failure guidance**: Added step-by-step fix for macOS-specific login failures when the login Keychain is locked or out of sync.

  > *"On macOS, login can also fail when the Keychain is locked or its password is out of sync with your account password... Run `claude doctor` to check Keychain access. To unlock the Keychain manually, run `security unlock-keychain ~/Library/Keychains/login.keychain-db`."*

  - *Source*: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

---

### Other Notable Details

- **`--resume` cross-worktree improvement**: The `/resume` picker now directly resumes sessions from other worktrees of the same repository, without requiring a `cd` first. The docs previously said it would "print a `cd` command".
  - *Source*: [Common workflows](https://code.claude.com/docs/en/common-workflows.md)

- **Ultraplan: explicit third-party provider exclusion**: Ultraplan documentation now states it is unavailable when using Amazon Bedrock, Google Cloud Vertex AI, or Microsoft Foundry (runs on Anthropic's cloud infrastructure). Also now requires v2.1.91 or later.
  - *Source*: [Ultraplan](https://code.claude.com/docs/en/ultraplan.md)

- **Plugin cache cleanup timing**: Orphaned plugin versions (after update or uninstall) are now documented as removed automatically **7 days later**, with an explanation that the grace period supports concurrent sessions using the old version.
  - *Source*: [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md)

- **Installed plugins path added to "What's not shown"**: `~/.claude/plugins/` now appears in the file table with a description of what it stores and a link to plugin caching docs.
  - *Source*: [`.claude` directory](https://code.claude.com/docs/en/claude-directory.md)

- **VS Code troubleshooting anchor**: An explicit `<a id="troubleshooting" />` anchor was added before the "Fix common issues" section, enabling direct links to VS Code troubleshooting.
  - *Source*: [VS Code](https://code.claude.com/docs/en/vs-code.md)

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| amazon-bedrock.md | Modified | +80/-0 | Full Mantle endpoint documentation: setup, model selection, dual-mode, gateway routing, env vars, and error reference |
| claude-directory.md | Modified | +62/-5 | New Application Data section covering all runtime-written files, retention, plaintext warning, and data clearing guide |
| changelog.md | Modified | +28/-0 | Version 2.1.94 release notes |
| troubleshooting.md | Modified | +24/-0 | New "Model not found" section; macOS Keychain login fix |
| hooks.md | Modified | +11/-5 | Debug log clarifications, exit-code-1 warning block, `sessionTitle` output field, `suppressOutput` correction |
| hooks-guide.md | Modified | +5/-3 | Debug workflow rewrite: transcript summary vs. debug log distinction |
| env-vars.md | Modified | +8/-5 | Three new Mantle variables; default values added to timeout variables |
| keybindings.md | Modified | +8/-7 | `Ctrl+L` rebound from `app:redraw` to `chat:clearInput`; `app:redraw` unbound |
| model-config.md | Modified | +7/-3 | Mantle model IDs section; effort level default changed for non-Pro/Max users |
| plugins-reference.md | Modified | +3/-0 | Skill frontmatter name behavior; orphaned version cleanup timing |
| plugins.md | Modified | +6/-6 | JSON indentation fix in quickstart example |
| code-review.md | Modified | +6/-0 | New "Rate and reply to findings" section with 👍/👎 feedback |
| output-styles.md | Modified | +2/-1 | Plugins can ship output styles |
| vs-code.md | Modified | +2/-0 | Added `#troubleshooting` anchor |
| ultraplan.md | Modified | +2/-2 | Version requirement (v2.1.91+); third-party provider exclusion noted |
| data-usage.md | Modified | +1/-1 | Local caching description updated with plaintext/path/cleanup details |
| common-workflows.md | Modified | +1/-1 | `--resume` cross-worktree behavior clarified |
| context-window.md | Modified | +2/-2 | Hook stdout description corrected: debug log, not verbose mode |
| how-claude-code-works.md | Modified | +1/-1 | Sessions described as plaintext JSONL; link to new Application Data section |
| interactive-mode.md | Modified | +1/-1 | `Ctrl+L` description updated to match rebinding |

---

*Generated from Claude Code CLI documentation changes detected on 2026-04-08*
