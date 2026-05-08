# Claude API Documentation Changes - February 11, 2026

## TL;DR
Server tools now run in a loop on Anthropic's servers with clearer `pause_turn` handling guidance, compaction gets smarter prompt caching strategies to preserve system prompt caches, and the documentation clarifies the server-side sampling loop's 10-iteration limit.

## API Changes

### Server Tools Sampling Loop Details

The documentation now explicitly reveals that server tools run in a **server-side sampling loop** that can execute multiple tool calls before returning:

> **New detail**: "The server runs a sampling loop that may execute multiple tool calls before returning a response."

**Why this matters**: This clarifies that when you use server tools (web search, web fetch), Claude can chain multiple tool executions automatically without client intervention—but there's a limit.

### Server-Side Loop Iteration Limit

**Critical detail uncovered**: The server-side sampling loop has a **default limit of 10 iterations**:

> "The server-side sampling loop has a default limit of 10 iterations. If Claude reaches this limit while executing server tools, the API returns a response with `stop_reason="pause_turn"`."

**Implications**:
- Your server tool workflows can automatically chain up to 10 tool executions
- After 10 iterations, you'll get `pause_turn` and need to continue the conversation
- This may return a `server_tool_use` block without a corresponding `server_tool_result`

## Stop Reason Handling

### pause_turn Now Fully Documented

The `pause_turn` stop reason documentation has been significantly expanded with implementation details:

**Updated definition**:
> "Returned when the server-side sampling loop reaches its iteration limit while executing [server tools] like web search or web fetch. The default limit is 10 iterations per request."

**Key behavior change documented**:
> "When this happens, the response may contain a `server_tool_use` block without a corresponding `server_tool_result`. To let Claude finish processing, continue the conversation by sending the response back as-is."

### Improved Code Examples

New code examples show the proper pattern for handling `pause_turn`:

```python
def handle_server_tool_conversation(client, user_query, tools, max_continuations=5):
    """
    Handle server tool conversations that may require multiple continuations.

    The server runs a sampling loop when executing server tools. If the loop
    reaches its iteration limit, the API returns pause_turn. Continue the
    conversation by sending the response back to let Claude finish.
    """
    messages = [{"role": "user", "content": user_query}]

    for _ in range(max_continuations):
        response = client.messages.create(
            model="claude-opus-4-6",
            messages=messages,
            tools=tools
        )

        if response.stop_reason != "pause_turn":
            # Claude finished processing - return the final response
            return response

        # pause_turn: add the assistant's response and continue
        # pause_turn: replace the full message list to maintain alternating roles
        messages = [
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": response.content}
        ]

    # Reached max continuations - return the last response
    return response
```

**Developer guidance added**:
> "Your application should handle `pause_turn` in any agent loop that uses server tools. Simply add the assistant's response to your messages array and make another API request to let Claude continue."

## Prompt Caching

### New Strategy: Maximizing Cache Hits with System Prompts

A new section reveals an advanced caching optimization technique for compaction:

> **New section**: "#### Maximizing cache hits with system prompts"

**The problem explained**:
> "When compaction occurs, the summary becomes new content that needs to be written to the cache. Without additional cache breakpoints, this would also invalidate any cached system prompt, requiring it to be re-cached along with the compaction summary."

**The solution**:
> "To maximize cache hit rates, add a `cache_control` breakpoint at the end of your system prompt. This keeps the system prompt cached separately from the conversation, so when compaction occurs:
> - The system prompt cache remains valid and is read from cache
> - Only the compaction summary needs to be written as a new cache entry"

### Updated Guidance

**Before**: "You may add a `cache_control` breakpoint on compaction blocks, which caches the full system prompt along with the summarized content."

**After**: "You can add a `cache_control` breakpoint on compaction blocks to cache the summarized content."

**Why this matters**: This is a significant performance optimization for long-running conversations with compaction. By separating system prompt caching from conversation caching, you avoid re-caching large system prompts every time compaction occurs, saving both latency and costs.

### Example Code Pattern

```python
response = client.beta.messages.create(
    betas=["compact-2026-01-12"],
    model="claude-opus-4-6",
    max_tokens=4096,
    system=[
        {
            "type": "text",
            "text": "You are a helpful coding assistant...",
            "cache_control": {"type": "ephemeral"}  # Cache the system prompt separately
        }
    ],
    messages=messages,
    context_management={
        "edits": [{"type": "compact_20260112"}]
    }
)
```

**Additional note**:
> "This approach is particularly beneficial for long system prompts, as they remain cached even across multiple compaction events throughout a conversation."

## Technical Details

### Compaction + Prompt Caching Integration

The documentation now explicitly states that compaction works well with prompt caching:

> "Compaction works well with [prompt caching](/docs/en/build-with-claude/prompt-caching)."

This confirms these beta features are designed to work together, not as separate systems.

### Image Alt Text Improvements

The compaction flow diagram now has much more descriptive alt text:

**Before**: `![Compaction flow diagram](/docs/images/compaction-flow.svg)`

**After**: `![Flow diagram showing the compaction process: when input tokens exceed the trigger threshold, Claude generates a summary in a compaction block and continues the response with the compacted context](/docs/images/compaction-flow.svg)`

### Code Block Formatting

Minor cleanup: removed unnecessary `-text` suffix from code block markers in the compaction summarization prompt example.

## Hidden Gems

### Server Tools Execution Model

The wording change from "Server tools follow a different workflow:" to "Server tools follow a different workflow **where Anthropic's servers handle tool execution in a loop**:" reveals that this is fundamentally different from client-side tool use. The server maintains the execution loop, not your application.

### Alternating Role Pattern

The `pause_turn` example code shows an interesting pattern where messages are **replaced** rather than appended:

```python
# pause_turn: replace the full message list to maintain alternating roles
messages = [
    {"role": "user", "content": user_query},
    {"role": "assistant", "content": response.content}
]
```

This suggests that for server tools, maintaining the alternating user/assistant pattern by resetting the messages array is the recommended approach, rather than building up a long conversation history.

### Default Continuation Recommendation

The new example uses `max_continuations=5` as a suggested default for handling `pause_turn` loops. Combined with the 10-iteration server-side limit, this means a complex server tool workflow could theoretically execute up to 50 total iterations (5 client continuations × 10 server iterations each).

---

*Generated from Claude API documentation changes detected on February 11, 2026*
