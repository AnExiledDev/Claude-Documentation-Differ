# Claude API Documentation Changes — 2026-05-15

## Summary

Four tool-use documentation pages were updated to remove references to deprecated and retired models — primarily Claude Sonnet 3.7, Haiku 3.5, and older Claude 3.x models. The most significant change in `computer-use-tool.md` removes the `thinking` parameter from the reference implementation's `sampling_loop` function, reflecting that extended thinking for computer use is no longer model-specific. Claude Opus 4 and Claude Sonnet 4 are now formally marked as deprecated in the tool use system prompt token table.

---

## Significant Changes

### Computer Use Tool

- **Removed `thinking` parameter from `sampling_loop` reference implementation**: The `thinking_budget` parameter has been removed from the `sampling_loop` function signature, along with the conditional thinking setup block and the `thinking=thinking` argument passed to `client.beta.messages.create`. This parameter was previously used specifically with Claude Sonnet 3.7.
  > `-    thinking_budget: int | None = None,`
  > `-    thinking = None`
  > `-    if thinking_budget:`
  > `-        thinking = {"type": "enabled", "budget_tokens": thinking_budget}`
  > `-            thinking=thinking,`
  - *Implication*: Developers using the reference implementation who relied on `thinking_budget` in `sampling_loop` must remove that parameter from their call sites. Extended thinking for computer use is now addressed separately from the tool version logic.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

- **`text_editor_type` conditional logic removed; hardcoded to `text_editor_20250728`**: The reference implementation previously selected the text editor tool type dynamically based on the tool version string. This has been replaced with a hardcoded `"text_editor_20250728"` value.
  > `-        {"type": text_editor_type, "name": "str_replace_based_edit_tool"},`
  > `+        {"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"},`
  - *Implication*: Implementations copying from the reference code should update to use `text_editor_20250728` directly, removing the conditional branch.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

- **Beta header model list updated — Claude Sonnet 3.7 removed**: The `computer-use-2025-01-24` beta header model list no longer includes Claude Sonnet 3.7. Claude Sonnet 4 and Claude Opus 4 are now explicitly marked as deprecated in this list.
  > `- "computer-use-2025-01-24"` for Claude Sonnet 4.5, Claude Haiku 4.5, Claude Opus 4.1, Claude Sonnet 4 ([deprecated]), and Claude Opus 4 ([deprecated])
  - *Implication*: Developers still targeting Sonnet 3.7 for computer use should migrate to a supported model. The deprecation markers on Sonnet 4 and Opus 4 signal those are also on an end-of-life path.
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

- **Enhanced action availability wording generalized**: The description of enhanced computer use actions (`scroll`, `left_click_drag`, `right_click`, `middle_click`) has been updated from "Available in Claude 4 models and Claude Sonnet 3.7" to "Available on all models that support computer use."
  > `-Available in Claude 4 models and Claude Sonnet 3.7:`
  > `+Available on all models that support computer use:`
  - *Implication*: Documentation now reflects that these actions are broadly available rather than tied to specific model versions. The inline "Scroll down (Claude 4/3.7):" label in examples was similarly simplified to "Scroll down:".
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

- **Limitations section de-versioned**: Items 2, 4, and 5 in the known limitations list have been rewritten to remove Sonnet 3.7-specific language. The scrolling limitation now describes the capability generally; the spreadsheet limitation drops the Sonnet 3.7 framing and gives guidance applicable to all models. Item 2 replaces "Claude Sonnet 3.7 introduces the thinking capability" with "Extended thinking can help you understand the model's reasoning."
  - *Source*: [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

### Tool Use Overview — Model Support Table

- **Deprecated/retired model cleanup in system prompt token table**: Several older models have been removed or relabeled in the tool use system prompt token reference table.
  - Claude Opus 4 and Claude Sonnet 4: now marked `[deprecated]`
  - Claude Sonnet 3.7: **row removed**
  - Claude Haiku 3.5: relabeled `[retired, except on Bedrock and Vertex AI]`
  - Claude Haiku 3, Claude Sonnet 3, Claude Opus 3: **rows removed**
  > `+| Claude Haiku 3.5 ([retired, except on Bedrock and Vertex AI](/docs/en/about-claude/model-deprecations)) | ...`
  - *Implication*: The tool use system prompt table now only lists actively supported models (plus those with explicit deprecation/retirement notices). Developers on Claude 3.x or early Claude 4 models should plan migration to current 4.x models.
  - *Source*: [Tool Use Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md)

---

## Minor Changes

- **code-execution-tool.md**: Removed Claude Sonnet 3.7 and Claude Haiku 3.5 from the supported models table for the code execution tool. The note about `code_execution_20250522` (legacy Python-only version) was reworded from declarative to conditional phrasing ("If you're still using the legacy…"). (+1/-3 lines)

- **text-editor-tool.md**: Removed the `text_editor_20250124` (Claude Sonnet 3.7 [deprecated]) row from the text editor tool pricing table. (+0/-1 lines)

---

## Migration Notes

- **Remove `thinking_budget` from `sampling_loop` call sites**: If your computer use implementation passed `thinking_budget` to `sampling_loop` based on the reference code, remove that parameter. The thinking setup block it controlled has been deleted.
- **Hardcode `text_editor_20250728` in computer use tool configs**: Replace any dynamic `text_editor_type` selection logic copied from the reference implementation with the static value `"text_editor_20250728"`.
- **Migrate off Claude Sonnet 3.7 for all tool use**: Sonnet 3.7 has been removed from the supported model lists for computer use, code execution, and text editor tools. Use Claude Sonnet 4.5+ or Claude Opus 4.5+ for current tool use capabilities.
- **Migrate off Claude 3 models for tool use**: Claude Haiku 3, Sonnet 3, and Opus 3 rows have been removed from the tool use system prompt token table, indicating these models are no longer in scope for tool use documentation support.

---

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| computer-use-tool.md | Modified | SIGNIFICANT | +8/-24 | Removed thinking parameter, text_editor_type logic, Sonnet 3.7 references; updated beta header model list and limitations |
| overview.md | Modified | SIGNIFICANT | +3/-7 | Removed Claude 3.x rows and Haiku 3.5 from token table; deprecated Opus 4 and Sonnet 4 |
| code-execution-tool.md | Modified | MINOR | +1/-3 | Removed Sonnet 3.7 and Haiku 3.5 from supported models; reworded legacy tool note |
| text-editor-tool.md | Modified | MINOR | +0/-1 | Removed text_editor_20250124 / Sonnet 3.7 from pricing table |

---
*Generated from Claude API documentation changes detected on 2026-05-15*
