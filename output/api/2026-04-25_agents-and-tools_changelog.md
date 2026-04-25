# Claude API Documentation Changes — 2026-04-25

## Summary

Documentation for the Agents & Tools section has been updated to recommend `claude-opus-4-7` in place of `claude-opus-4-6` across all tool use and agentic loop examples. Beta header requirements were removed from the Files API and Skills API calls, indicating those APIs have graduated from requiring explicit beta opt-in. The "Build a tool-using agent" tutorial gained comprehensive bash/shell code examples (both raw `curl` and the `ant` CLI) for all five agentic-loop rings.

## Significant Changes

### Models

- **`claude-opus-4-7` is now the recommended model for tool use**: All code examples across tool use documentation — define tools, strict tool use, parallel tool use, server tools, tool runner, handle tool calls, and the agentic loop tutorial — have been updated from `claude-opus-4-6` to `claude-opus-4-7`.
  - *Implication*: Developers following the documentation examples or copy-pasting quickstart code will now reference the latest Opus model. Update any pinned model strings to `claude-opus-4-7`.
  - *Source*: [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools.md), [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use.md), [Parallel tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use.md), and others

- **Opus 4 and Sonnet 4 marked deprecated in parallel tool use guidance**: The system prompt guidance for parallel tool use previously read "For Claude 4 models (Opus 4, and Sonnet 4)"; it now reads "For Claude 4 models (Opus 4 (deprecated), and Sonnet 4 (deprecated))".
  > For Claude 4 models (Opus 4 (deprecated), and Sonnet 4 (deprecated)), add this to your system prompt: `For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially.`
  - *Implication*: This confirms the claude-opus-4 and claude-sonnet-4 (-20250514) model versions are now deprecated. Developers still on those versions should migrate.
  - *Source*: [Parallel tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use.md)

- **Sonnet 3.7 model-specific behavior guidance removed**: A troubleshooting section noting that Claude Sonnet 3.7 may need stronger prompting or the `token-efficient-tools-2025-02-19` beta header for parallel tool use has been deleted.
  - *Implication*: Developers on Sonnet 3.7 should upgrade to Claude 4 models. The guidance to try the beta header no longer appears in the docs.
  - *Source*: [Parallel tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use.md)

### Tool Use — New Constraint

- **Claude Mythos Preview does not support forced tool use**: A new note was added to the `tool_choice` section of the Define Tools page:
  > [Claude Mythos Preview](https://anthropic.com/glasswing) does not support forced tool use. Requests with `tool_choice: {"type": "any"}` or `tool_choice: {"type": "tool", "name": "..."}` return a 400 error on this model. Use `tool_choice: {"type": "auto"}` (the default) or `tool_choice: {"type": "none"}` and rely on prompting to influence tool selection.
  - *Implication*: Any application that hard-codes forced tool selection and wants to run on the Mythos Preview model must switch to `auto` or `none` and use prompting instead. This is a behavior difference from all other current models.
  - *Source*: [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools.md)

### Beta API Graduation — Headers No Longer Required

- **Files API beta header removed from SDK examples**: The `betas: ["files-api-2025-04-14"]` parameter has been removed from all SDK code examples that call `client.beta.files.upload()`, `client.beta.files.download()`, and `client.beta.files.GetMetadata()`. Affected SDKs: Python, TypeScript, Go, and PHP.

  Before (Python):
  ```python
  file_content = client.beta.files.download(
      file_id=file_id, betas=["files-api-2025-04-14"]
  )
  ```
  After:
  ```python
  file_content = client.beta.files.download(file_id=file_id)
  ```
  - *Implication*: The Files API no longer requires passing the beta string in SDK calls. Developers with existing code that passes `betas=["files-api-2025-04-14"]` should remove it; the parameter may cause issues or simply be ignored.
  - *Source*: [Agent skills quickstart](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart.md), [Code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

- **Skills API beta header removed**: The `betas=["skills-2025-10-02"]` parameter was removed from `client.beta.skills.list()` calls in both Python and TypeScript examples.

  Before (TypeScript):
  ```typescript
  const skills = await client.beta.skills.list({
    source: "anthropic",
    betas: ["skills-2025-10-02"]
  });
  ```
  After:
  ```typescript
  const skills = await client.beta.skills.list({
    source: "anthropic"
  });
  ```
  - *Implication*: The Skills API no longer requires an explicit beta opt-in string. Remove `betas: ["skills-2025-10-02"]` from any existing code.
  - *Source*: [Agent skills quickstart](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart.md)

### Agentic Loop Tutorial — New Shell Examples

- **Bash/cURL and `ant` CLI examples added for all five agentic rings**: The "Build a tool-using agent" tutorial has been substantially expanded (+633/−248 lines). Full working bash examples using raw `curl` and the `ant` CLI tool have been added for every ring:
  - Ring 1: Single tool, single turn
  - Ring 2: The agentic loop (conversation history + `while` loop)
  - Ring 3: Multiple tools, parallel calls (batch `tool_result` responses)
  - Ring 4: Error handling (`is_error: true` on failed tool results)
  - Ring 5: Tool Runner SDK abstraction (stub only — Tool Runner is not available for CLI/shell)

  The bash examples now appear before the Python tab. Each ring also gained labeled `Output` code blocks showing expected terminal output.

  > Ring 5: The Tool Runner SDK abstraction is available in the Python, TypeScript, and Ruby SDKs. The ant CLI exposes the Messages API directly and has no equivalent helper. Switch to the Python or TypeScript tab to see Ring 5, or keep the Ring 4 loop as your CLI implementation.

  - *Implication*: Developers using shell scripts or the `ant` CLI now have complete, runnable reference implementations for building agents without an SDK dependency.
  - *Source*: [Build a tool-using agent](https://platform.claude.com/docs/en/agents-and-tools/tool-use/build-a-tool-using-agent.md)

### Strict Tool Use — CLI Examples Added

- **`ant` CLI tab added to strict tool use quick start**: The cURL tab was previously labeled "Shell"; it is now labeled "cURL". A new "CLI" tab using the `ant` tool was added alongside cURL for the quick start and the validated tool inputs use case.
  - *Implication*: Developers using the `ant` CLI can now test strict mode (`strict: true`) without writing SDK code.
  - *Source*: [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use.md)

### Define Tools — CLI Example Added

- **`ant` CLI example added for `input_examples` feature**: A new "CLI" code tab was added to the `input_examples` documentation section.
  - *Implication*: The `input_examples` field (for providing schema-validated example inputs in tool definitions) can now be tested via the CLI without writing SDK code.
  - *Source*: [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools.md)

## Migration Guidance

- **Remove beta header from Files API calls**: If you're passing `betas=["files-api-2025-04-14"]` to any `client.beta.files.*` method, remove it:
  ```python
  # Before
  client.beta.files.download(file_id=file_id, betas=["files-api-2025-04-14"])
  # After
  client.beta.files.download(file_id=file_id)
  ```

- **Remove beta header from Skills API calls**: If you're passing `betas=["skills-2025-10-02"]` to `client.beta.skills.list()`, remove it:
  ```python
  # Before
  client.beta.skills.list(source="anthropic", betas=["skills-2025-10-02"])
  # After
  client.beta.skills.list(source="anthropic")
  ```

- **Update forced tool use for Mythos Preview**: If targeting Claude Mythos Preview, replace `tool_choice: {"type": "any"}` or `tool_choice: {"type": "tool", "name": "..."}` with `tool_choice: {"type": "auto"}` and add explicit prompting.

## Notable Details

- All code examples in the `tool-runner.md` doc were also bumped from `claude-opus-4-6` to `claude-opus-4-7`, including the `beta.messages.tool_runner()` / `beta.messages.toolRunner()` calls across Python, TypeScript, and Ruby.
- The `handle-tool-calls.md` example JSON response was also updated to show `claude-opus-4-7` as the model field, keeping the documentation self-consistent.
- The `build-a-tool-using-agent.md` bash examples use `jq` for JSON manipulation, with explicit comments noting that cross-turn `messages` array management in shell requires JSON tooling beyond what the `ant` CLI's single-call `--transform` scope covers.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `agents-and-tools/tool-use/build-a-tool-using-agent.md` | Modified | +633/−248 | Added bash/cURL and `ant` CLI examples for all five agentic rings |
| `agents-and-tools/tool-use/strict-tool-use.md` | Modified | +109/−24 | Added CLI tab examples; model updated to 4.7; cURL tab renamed |
| `agents-and-tools/tool-use/define-tools.md` | Modified | +42/−8 | Model updated to 4.7; CLI example for input_examples; Mythos forced tool use restriction note |
| `agents-and-tools/tool-use/parallel-tool-use.md` | Modified | +15/−21 | Model updated to 4.7; Opus 4 and Sonnet 4 marked deprecated; Sonnet 3.7 guidance removed |
| `agents-and-tools/tool-use/server-tools.md` | Modified | +14/−14 | Model updated to 4.7 across all SDK examples |
| `agents-and-tools/tool-use/tool-runner.md` | Modified | +19/−19 | Model updated to 4.7 across Python, TypeScript, and Ruby examples |
| `agents-and-tools/tool-use/code-execution-tool.md` | Modified | +7/−13 | Removed `betas: ["files-api-2025-04-14"]` from TypeScript, Go, and PHP examples |
| `agents-and-tools/agent-skills/quickstart.md` | Modified | +4/−9 | Removed beta header parameters from skills.list() and files.download() |
| `agents-and-tools/tool-use/handle-tool-calls.md` | Modified | +1/−1 | Model in example JSON updated to claude-opus-4-7 |

---
*Generated from Claude API documentation changes detected on 2026-04-25*
