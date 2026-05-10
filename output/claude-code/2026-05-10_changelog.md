# Claude Code Documentation Changes — 2026-05-10

## Summary

One page was modified: the error reference expanded the "Auto mode cannot determine the safety of an action" section from a single failure case (classifier overloaded) to three distinct failure cases. Two new error messages were added to the quick-lookup table, and recovery instructions were added for each new case.

## Significant Changes

### Error Reference

- **Auto mode classifier failure: three cases now documented**: The section previously described only one failure mode (classifier model overloaded). It now covers three separate failure scenarios with distinct error messages, explanations, and remediation steps.
  > The model that auto mode uses to classify actions could not produce a decision, so auto mode did not approve the action automatically. The message you see depends on why the classifier failed.
  - *Implication*: Developers debugging stalled auto mode workflows can now identify which of the three failure modes they are hitting and apply the correct fix, rather than assuming it is always a transient overload.
  - *Source*: [Error reference](https://code.claude.com/docs/en/errors.md)

- **New error: unparseable classifier response**: Documents a new error message for when the classifier returns a response that cannot be parsed.
  > ```
  > Auto mode could not evaluate this action and is blocking it for safety — run with --debug for details
  > ```
  > **What to do:**
  > * Retry the action; this usually succeeds on the next attempt
  > * Run `claude --debug` and repeat the action to see the underlying classifier response in the debug log
  - *Implication*: `--debug` is now the recommended first diagnostic step for this failure mode, exposing the raw classifier output.
  - *Source*: [Error reference](https://code.claude.com/docs/en/errors.md)

- **New error: classifier context window exceeded**: Documents a new error message for when the conversation transcript has grown larger than the classifier's context window.
  > ```
  > Auto mode classifier transcript exceeded context window — falling back to manual approval (try /compact to reduce conversation size)
  > ```
  > In an interactive session, auto mode falls back to a normal permission prompt for that action so you can approve or deny it manually. In non-interactive mode the run aborts because the transcript only grows and retrying cannot succeed.
  - *Implication*: This is a deterministic failure in headless/non-interactive mode — the run aborts and cannot recover without reducing conversation size. The fix is to run `/compact` before the context window is exhausted. This is especially relevant for long-running agentic sessions.
  - *Source*: [Error reference](https://code.claude.com/docs/en/errors.md)

- **"Skip the classifier" note broadened**: The clarification that reads, searches, and edits inside the working directory bypass the auto mode classifier was previously scoped to "during the outage" (the overload case only). It now reads "in all of these cases", applying to all three failure modes.
  > Reads, searches, and edits inside your working directory skip the classifier, so they keep working in all of these cases.
  - *Implication*: File read/search/edit operations remain unblocked even when the classifier fails for any reason, not just during API overloads.
  - *Source*: [Error reference](https://code.claude.com/docs/en/errors.md)

## Notable Details

- The section introduction was reworded from "auto mode blocked the action instead of approving it unchecked" to "auto mode did not approve the action automatically." This is a more neutral and accurate description of the classifier's role.
- The error lookup table at the top of the page now has two additional rows for the new messages, giving users a direct jump link to the relevant section. Previously only the overloaded-model variant was listed.
- The non-interactive (headless) mode behavior is explicitly called out for the context-window case: the run aborts rather than falling back to a prompt. This is a meaningful behavioral distinction for CI/automation users.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| errors.md | Modified | +31 / -3 | Expanded auto mode classifier failure documentation to cover three distinct error cases: overloaded model (existing), unparseable response (new), and context window exceeded (new) |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-10*
