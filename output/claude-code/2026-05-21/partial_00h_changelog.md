# Claude Code Documentation Changes — 2026-05-21

## Summary

Seven pages were updated with no new or removed pages. The most substantive changes are: documentation of a new `ScheduleWakeup` tool that backs self-paced `/loop` iteration timing, expanded clarification of interrupt-vs-redirect behavior distinguishing `Esc` from typing-and-pressing-Enter, and tightened platform/subscription restrictions on the `/desktop` command and the `/loop` maintenance prompt.

## Significant Changes

### New Tool: `ScheduleWakeup`

- **`ScheduleWakeup` tool added to tools reference**: A new internal tool is now documented that handles the timing engine behind self-paced `/loop` iterations. Claude calls it automatically at the end of each loop iteration to choose the next wakeup time (between one minute and one hour). Users do not call it directly.
  > "Reschedules the next iteration of a self-paced `/loop`. Claude calls this at the end of each iteration to pick when the next one runs, between one minute and one hour out; you don't call it directly. The pending wakeup appears in `session_crons` in Stop hook input. Not available on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry, where a `/loop` prompt with no interval runs on a fixed schedule instead."
  - *Implication*: This tool is not available on Bedrock, Vertex AI, or Foundry — on those platforms, `/loop` without an explicit interval runs on a fixed schedule rather than self-pacing. The distinction between dynamic and fixed scheduling is now explicitly surfaced in the tool table.
  - *Source*: [Tools Reference](https://code.claude.com/docs/en/tools-reference.md)

### Interrupt vs. Redirect: Two Modes Documented

- **`Esc` and `Enter` now distinguished as separate interaction modes**: The "Interrupt and steer" section in `how-claude-code-works.md` was rewritten from a single paragraph to a two-bullet list that explicitly separates the two interrupt behaviors.
  > "* **Press `Esc`** to stop Claude immediately. The running tool call is canceled and Claude waits for your next instruction.\n* **Type a correction and press `Enter`** to send it without stopping the running tool. Claude reads it as soon as the current action completes and adjusts before deciding its next step."
  - *Implication*: This corrects prior documentation that implied typing a correction always stopped Claude. Pressing Enter mid-run now queues the correction rather than interrupting; only `Esc` provides an immediate stop. Developers writing UI guidance or training materials should update accordingly.
  - *Source*: [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works.md)

### `/desktop` Command: Subscription Requirement Clarified

- **`/desktop` now requires a Claude subscription, not just macOS or Windows**: Both the commands reference table and the `desktop.md` prose were updated to specify that `/desktop` is unavailable with API key authentication or on Bedrock, Vertex, or Foundry.
  > (commands.md) "Continue the current session in the Claude Code Desktop app. Requires macOS or Windows and a Claude subscription. Alias: `/app`"
  > (desktop.md) "This command is available on macOS and Windows when you are signed in with a Claude subscription. It is not available with API key authentication or on Bedrock, Vertex, or Foundry."
  - *Implication*: Enterprise and cloud-provider users (Bedrock, Vertex, Foundry) and API-key-only setups cannot use `/desktop` to hand off sessions to the Desktop app. The note in the commands availability header was also updated to add "when signed in with a Claude subscription" to the `/desktop` condition.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md), [Desktop](https://code.claude.com/docs/en/desktop.md)

### `/loop` Maintenance Prompt Availability Broadened

- **Built-in maintenance prompt now described as a partial rollout, not just a platform restriction**: The `scheduled-tasks.md` note was reworded from listing specific excluded platforms to stating the feature is not yet universally available.
  > "The built-in maintenance prompt isn't available to everyone yet, and isn't supported on Bedrock, Vertex AI, or Microsoft Foundry. Where it isn't active, `/loop` with no prompt prints the usage message instead."
  - *Implication*: The prior wording implied the maintenance prompt worked for all non-Bedrock/Vertex/Foundry users. The new wording acknowledges it is still rolling out — some claude.ai users may also not have access. A companion Note was also added clarifying that `loop.md` follows the same availability constraint: where the maintenance prompt is inactive, the `loop.md` file is not read.
  - *Source*: [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks.md)

### `/loop` Command Description Updated

- **`/loop` command entry links to availability anchor**: The command table description for `/loop` now links to a specific anchor for the maintenance prompt availability note and rewords the fallback behavior.
  > "Omit the prompt and, [where available](/en/scheduled-tasks#run-the-built-in-maintenance-prompt), Claude runs an autonomous maintenance check or the prompt in `.claude/loop.md`."
  - *Implication*: The inline link surfaces the availability caveat directly from the command table, reducing confusion for users on unsupported platforms.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

## Minor Changes

- **[desktop-quickstart.md]**: Interrupt/redirect wording updated to match the new two-mode explanation — typing and pressing Enter sends without stopping; the stop button interrupts immediately (+1/-1 lines).
- **[desktop.md]**: Same redirect-vs-stop clarification applied to the main Desktop "Use the prompt box" section. Also received the `/desktop` subscription restriction update (+2/-2 lines).
- **[hooks.md]**: `session_crons` description now lists `ScheduleWakeup` alongside `CronCreate` and `/loop` as a source of session-scoped scheduled wakeups (+1/-1 lines).

## Notable Details

- The `ScheduleWakeup` tool is documented as "not available on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry" — this directly explains *why* self-paced `/loop` (dynamic interval selection) only works on anthropic-hosted infrastructure. On other providers, `/loop` without an interval still works but uses a fixed schedule.
- The `hooks.md` change adding `ScheduleWakeup` to `session_crons` confirms that pending self-paced wakeups are visible in the Stop hook payload, enabling hook scripts to inspect or react to upcoming loop iterations.
- The majority of the diff in `tools-reference.md` (+42/-41 lines) is a column-width reformat of the entire tool table; the only semantic change is the insertion of the new `ScheduleWakeup` row.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| tools-reference.md | Modified | SIGNIFICANT | +42/-41 | New `ScheduleWakeup` tool added; table column reformatted |
| scheduled-tasks.md | Modified | SIGNIFICANT | +5/-1 | Maintenance prompt availability broadened; `loop.md` availability note added |
| how-claude-code-works.md | Modified | SIGNIFICANT | +4/-1 | Interrupt vs. redirect clarified: Esc stops immediately, Enter queues correction |
| commands.md | Modified | SIGNIFICANT | +3/-3 | `/desktop` requires subscription; `/loop` links to availability anchor |
| desktop.md | Modified | MINOR | +2/-2 | Redirect wording update; `/desktop` subscription and platform restrictions |
| desktop-quickstart.md | Modified | MINOR | +1/-1 | Redirect wording update matching new two-mode behavior |
| hooks.md | Modified | MINOR | +1/-1 | `ScheduleWakeup` added to `session_crons` source list |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-21*
