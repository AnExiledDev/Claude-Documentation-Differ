# Claude API Documentation Changes — 2026-05-17

## Summary

The largest change is a major expansion of the Tool Runner documentation: C#, Go, Java, and PHP SDKs are now documented alongside the existing Python, TypeScript, and Ruby coverage, and two new advanced sections clarify lifecycle semantics and automatic context management. The parallel tool use page gains a new "Execution semantics" section. Across all cloud platform pages, the Java SDK was bumped from version 2.30.0 to 2.32.0.

## Significant Changes

### Tool Runner (SDKs)

- **C#, Go, Java, and PHP tool runner support documented**: The tool runner beta, previously documented for Python, TypeScript, and Ruby only, now includes full examples for four additional SDKs.
  > "The tool runner is currently in beta and available in the [Python SDK](https://github.com/anthropics/anthropic-sdk-python/blob/main/tools.md), [TypeScript SDK](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/helpers.md#tool-helpers), [C# SDK](https://github.com/anthropics/anthropic-sdk-csharp/blob/main/examples/ToolRunnerExample/Program.cs), [Go SDK](https://github.com/anthropics/anthropic-sdk-go/blob/main/tools.md), [Java SDK](https://github.com/anthropics/anthropic-sdk-java/blob/main/anthropic-java-example/src/main/java/com/anthropic/example/BetaToolRunnerExample.java), [PHP SDK](https://github.com/anthropics/anthropic-sdk-php/blob/main/examples/beta/beta_tool_runner.php), and [Ruby SDK](https://github.com/anthropics/anthropic-sdk-ruby/blob/main/helpers.md#3-auto-looping-tool-runner-beta)."
  - *Implication*: Developers using C#, Go, Java, or PHP can now use the managed agentic loop abstraction without writing their own tool dispatch code. Each SDK has idiomatic patterns: Go uses `jsonschema:` struct tags, Java uses `@JsonClassDescription`/`@JsonPropertyDescription` annotations, C# uses `BetaRunnableTool` delegates, PHP uses `BetaRunnableTool` closures.
  - *Source*: [tool-runner.md](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner.md)

- **New section: "Taking over message history"**: Explains how and when developers can override the runner's automatic message-history management. The runner now has a documented lifecycle with an explicit state-modification signal.
  > "By default, the runner manages conversation state for you: after each turn, it appends the assistant message and any tool results to its own message history. You take over message history when you want to retry a turn (discard the response and resend), inject a follow-up message, or build the tool result yourself."
  > "When you take over for an iteration, the runner does not append the assistant message or tool results from that turn. You become responsible for keeping the conversation valid: append the assistant message and a tool result yourself (if you want the turn to count), modify state conditionally so the loop can still exit when there are no tool calls, and pass `max_iterations` to bound the loop. All seven SDKs support `max_iterations`."
  - *Implication*: The `max_iterations` parameter is now mentioned as available in all seven SDKs. The trigger for skipping auto-append is SDK-specific: in Python it's calling `append_messages()`, in TypeScript/PHP it's calling `setMessagesParams()` or `pushMessages()`, in Java it's `setNextParams()`, in C# it's `SetParams()` or `PushMessages()`. Go is an exception — it always appends unconditionally regardless of param mutation.
  - *Source*: [tool-runner.md](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner.md)

- **New section: "Automatic context management"**: Documents compaction support within the tool runner for long-running agentic tasks.
  > "For long-running agentic tasks, the tool runner supports automatic [compaction](/docs/en/build-with-claude/context-editing#client-side-compaction-sdk), which generates summaries when token usage exceeds a threshold so the conversation can continue beyond context window limits."
  - *Implication*: This was previously noted only in a `<Tip>` callout that has now been removed; the feature is now documented as a formal subsection under Advanced Usage, alongside the lifecycle diagram.
  - *Source*: [tool-runner.md](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner.md)

- **Tool runner lifecycle sequence diagram added**: A Mermaid diagram now illustrates the per-iteration flow between caller code, the ToolRunner, and the Messages API, making the state-modification branching explicit.
  - *Implication*: Developers implementing custom retry or injection logic can now refer to a canonical diagram rather than inferring behavior from prose.
  - *Source*: [tool-runner.md](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner.md)

- **Streaming examples added for C#, Go, and Java**: Coverage for streaming responses within the tool runner loop is extended to the newly documented SDKs. PHP streaming is noted as "not currently available."
  - *Implication*: C# uses `runner.Streaming()`, Go uses `NewToolRunnerStreaming` / `runner.AllStreaming(ctx)`, Java uses `runner.streaming()` returning a `StreamResponse` that must be closed after use.
  - *Source*: [tool-runner.md](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner.md)

### Parallel Tool Use

- **New section: "Execution semantics"**: Clarifies that tool calls within a single assistant turn are unordered and can be dispatched concurrently, sequentially, or in any order.
  > "Tool calls in a single assistant turn are unordered. You can run them concurrently (`Promise.all`, `asyncio.gather`), sequentially, or in any order. Claude doesn't assume one call in the batch has completed before another. Claude issues dependent calls across separate turns."
  - *Implication*: Removes ambiguity about whether ordering matters when dispatching parallel tool calls. Developers don't need to detect dependent calls in advance — returning `is_error: true` with the natural error message is sufficient; Claude will reissue the failed call after the prerequisite completes.
  - *Source*: [parallel-tool-use.md](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use.md)

- **New troubleshooting entry: "Calls in a batch appear to depend on each other"**: Added to the troubleshooting section with actionable guidance.
  > "If a tool call fails because it depends on another call in the same batch, return `is_error: true` with the natural error message (you don't need to explain the dependency). Claude recovers and reissues the call. Don't switch to sequential execution; that adds latency and masks the issue. To reduce occurrences, add this to your system prompt: 'Only batch tool calls that are independent of each other.'"
  - *Implication*: The recommended mitigation is a system prompt hint, not a code-level change.
  - *Source*: [parallel-tool-use.md](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use.md)

### Advisor Tool

- **Conciseness instruction placement changed**: The recommended location for output-length guidance moved from the system prompt to the user message, and the target word count shifted from "under 100 words" to approximately 80 words.
  > "The most effective placement Anthropic tested is a line in the user message:
  > `(Advisor: please keep your guidance under 80 words — I need a focused starting point, not a comprehensive plan.)`"
  - Previously: "The advisor should respond in under 100 words and use enumerated steps, not explanations." (system prompt)
  - *Implication*: Agent frameworks should prepend this line to the user message programmatically, not the system prompt. The limit is described as a soft constraint — "ask for roughly 80 percent of your true ceiling." A new `<Note>` callout discloses that in Anthropic's testing this instruction increased advisor call frequency, but net cost was still lower.
  - *Source*: [advisor-tool.md](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md)

### Get Started

- **CLI quickstart tab restructured**: The step ordering for the CLI tab changed — "Install the CLI" is now the first step, followed by a new "Authenticate" step using `ant auth login` (OAuth browser flow). Previously the tab showed "Set your API key" first.
  > "This opens a browser-based OAuth flow. After authorizing, confirm your credential with: `ant auth status`. On a remote host without a browser, pass `--no-browser` to get a URL you can open on another device, then paste the returned code back into the terminal. If `ANTHROPIC_API_KEY` is set in your environment, it takes precedence over the login credentials."
  - *Implication*: The CLI now supports account-based OAuth login as the primary auth path, with API key as an override. The prerequisite "An API key" was also removed from the Prerequisites section, signaling that CLI users no longer need to obtain a key manually.
  - *Source*: [get-started.md](https://platform.claude.com/docs/en/get-started.md)

## Minor Changes

- **claude-in-amazon-bedrock.md**: Java SDK dependency `anthropic-java-bedrock` bumped from 2.30.0 → 2.32.0 (+2/-2 lines)
- **claude-in-microsoft-foundry.md**: Java SDK dependency `anthropic-java-foundry` bumped from 2.30.0 → 2.32.0 (+2/-2 lines)
- **claude-on-amazon-bedrock-legacy.md**: Java SDK dependency `anthropic-java-bedrock` bumped from 2.30.0 → 2.32.0 (+2/-2 lines)
- **claude-on-vertex-ai.md**: Java SDK dependency `anthropic-java-vertex` bumped from 2.30.0 → 2.32.0 (+2/-2 lines)
- **claude-platform-on-aws.md**: Java SDK dependency `anthropic-java-aws` bumped from 2.30.0 → 2.32.0 (+2/-2 lines)
- **managed-agents/quickstart.md**: Anthropic CLI Linux binary version bumped from 1.7.0 → 1.8.0; Java SDK bumped from 2.30.0 → 2.32.0 (+2/-2 lines)

## Notable Details

- The `advisor-tool.md` change also corrects "Amazon Bedrock" → "AWS Bedrock" in the platform availability statement and "nonzero" → "non-zero" in the caching description — minor wording normalization.
- The tool runner's `@beta_tool` decorator description was simplified: the full inline JSON schema example (showing how `calculate_sum` maps to its JSON schema) was removed and replaced with a one-line summary. This is purely editorial.
- The Ruby streaming example was updated to use a nested `stream.each` block pattern, aligning it with the new multi-SDK streaming shape.
- The Go SDK's tool runner behavior differs from all other SDKs: modifying `runner.Params` does **not** suppress the runner's automatic append. This is documented as a deliberate SDK-level difference, not a bug.
- Error interception capabilities differ by SDK: Go and Java runners don't expose a pre-send hook; C# uses `BetaToolError`; PHP must use `pushMessages()` to bypass auto-append and inject a custom error block.
- Java SDK `anthropic-java` version 2.32.0 also appears in the get-started.md quickstart Gradle/Maven examples (previously 2.30.0).

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| tool-runner.md | Modified | SIGNIFICANT | +1382/-115 | Expanded to 7 SDKs; new lifecycle semantics, "Taking over message history", and "Automatic context management" sections |
| parallel-tool-use.md | Modified | SIGNIFICANT | +21/-2 | New "Execution semantics" section; new troubleshooting entry for dependent batched calls |
| advisor-tool.md | Modified | SIGNIFICANT | +13/-5 | Conciseness instruction moved to user message; word limit changed; platform name fix |
| get-started.md | Modified | SIGNIFICANT | +16/-11 | CLI tab restructured with OAuth `ant auth login`; API key prerequisite removed; Java SDK 2.32.0 |
| claude-in-amazon-bedrock.md | Modified | MINOR | +2/-2 | Java SDK `anthropic-java-bedrock` 2.30.0 → 2.32.0 |
| claude-in-microsoft-foundry.md | Modified | MINOR | +2/-2 | Java SDK `anthropic-java-foundry` 2.30.0 → 2.32.0 |
| claude-on-amazon-bedrock-legacy.md | Modified | MINOR | +2/-2 | Java SDK `anthropic-java-bedrock` 2.30.0 → 2.32.0 |
| claude-on-vertex-ai.md | Modified | MINOR | +2/-2 | Java SDK `anthropic-java-vertex` 2.30.0 → 2.32.0 |
| claude-platform-on-aws.md | Modified | MINOR | +2/-2 | Java SDK `anthropic-java-aws` 2.30.0 → 2.32.0 |
| managed-agents/quickstart.md | Modified | MINOR | +2/-2 | CLI binary 1.7.0 → 1.8.0; Java SDK 2.30.0 → 2.32.0 |

---
*Generated from Claude API documentation changes detected on 2026-05-17*
