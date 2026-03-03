# Claude API Documentation Changes — 2026-03-03

## Summary

Five Agent SDK and test/evaluate pages were updated. The most substantive change is a rewrite of the stop-reasons page, which now documents `stop_reason` on TypeScript result messages, enumerates all possible values, and adds a Python workaround via stream events. The migration guide's code examples were updated to reflect the SDK rename from `claude-code-sdk` to `claude-agent-sdk`.

## Significant Changes

### Agent SDK

- **Stop reasons page rewritten**: The `stop-reasons.md` page was substantially restructured (-71/+47 lines). The new version documents direct access to `stop_reason` on TypeScript `ResultMessage` objects, covers how `stop_reason` behaves on error result subtypes, and replaces the old ad-hoc examples with a formal reference table.

  > Direct `stop_reason` access on result messages is currently **TypeScript-only**. The Python SDK's `ResultMessage` does not include this field. For Python, see [Read stop_reason in Python](#read-stop_reason-in-python) for a workaround using stream events.

  New content covers:
  - A reference table of all `stop_reason` values: `end_turn`, `max_tokens`, `stop_sequence`, `refusal`, `tool_use`, `null`
  - A table mapping result subtypes (`success`, `error_max_turns`, `error_max_budget_usd`, `error_max_structured_output_retries`, `error_during_execution`) to their `stop_reason` semantics
  - A `safeQuery` TypeScript pattern for detecting refusals via `stop_reason === "refusal"`, replacing the previous approach of scanning `message_delta` stream events
  - A Python workaround using `include_partial_messages=True` and `StreamEvent` to extract `stop_reason` from `message_delta` events

  - *Implication*: TypeScript developers can now check `message.stop_reason` directly on the result message instead of parsing streaming events. Python developers require the workaround until `ResultMessage` is updated.
  - *Source*: [stop-reasons.md](https://platform.claude.com/docs/en/agent-sdk/stop-reasons.md)

- **Migration guide example labels updated**: The "Breaking changes" section code examples previously used `# BEFORE (v0.0.x)` / `# AFTER (v0.1.0)` labels. These were updated to `# BEFORE (claude-code-sdk)` / `# AFTER (claude-agent-sdk)`, aligning the inline comments with the package-name framing used throughout the rest of the guide.

  - *Implication*: No functional change. The migration steps themselves are unchanged.
  - *Source*: [migration-guide.md](https://platform.claude.com/docs/en/agent-sdk/migration-guide.md)

- **File checkpointing page condensed**: The `file-checkpointing.md` page was reduced by 47 net lines (-53/+6). Content was streamlined but the feature's core API — `enableFileCheckpointing`, `rewindFiles()`, `rewind_files()`, session resume with empty prompt, and CLI `--rewind-files` flag — remains documented.

  - *Implication*: No functional change to the checkpointing API. Developers relying on specific prose sections should review the updated page.
  - *Source*: [file-checkpointing.md](https://platform.claude.com/docs/en/agent-sdk/file-checkpointing.md)

- **TypeScript reference updated**: Minor edits (+5/-5 lines) to `typescript.md`. No new types or functions were added based on line count and section diff analysis.

  - *Source*: [typescript.md](https://platform.claude.com/docs/en/agent-sdk/typescript.md)

### Test and Evaluate

- **Develop tests code examples updated**: The `develop-tests.md` page saw symmetrical edits (+16/-16 lines) with no section changes. The page's Python code examples reference `claude-opus-4-6` as the model used in evaluation patterns (exact match, cosine similarity, ROUGE-L, Likert scale, binary classification, ordinal scale).

  - *Implication*: No structural change to the evaluation guidance. The model name in example code was updated.
  - *Source*: [develop-tests.md](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `agent-sdk/stop-reasons.md` | Modified | +47 / -71 | Page rewritten: new stop_reason reference table, error result subtype table, refusal detection pattern, Python workaround via stream events |
| `agent-sdk/file-checkpointing.md` | Modified | +6 / -53 | Page condensed; checkpointing API unchanged |
| `agent-sdk/migration-guide.md` | Modified | +6 / -6 | Code example labels changed from version numbers to package names |
| `agent-sdk/typescript.md` | Modified | +5 / -5 | Minor edits; no new API surface |
| `test-and-evaluate/develop-tests.md` | Modified | +16 / -16 | Evaluation code examples updated |
