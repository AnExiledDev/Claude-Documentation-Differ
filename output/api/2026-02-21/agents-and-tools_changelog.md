# Claude API Documentation Changes — 2026-02-21

## Summary

The programmatic tool calling documentation was updated to reflect a new tool version identifier (`code_execution_20260120`, replacing `code_execution_20250825`), and web search and web fetch tools were removed from the list of tools that cannot be called programmatically, indicating they now support programmatic invocation. New guidance was also added across two pages explaining how to handle multi-environment scenarios when the code execution tool is combined with client-provided execution tools such as bash.

## Significant Changes

### Tool Use

- **New programmatic tool calling version: `code_execution_20260120`**: The tool version string used for programmatic tool calling has been updated from `code_execution_20250825` to `code_execution_20260120`. This affects the `type` field in tool definitions, the `allowed_callers` field values, and the `caller` field in API responses. All code examples (curl, Python, TypeScript) in the programmatic tool calling documentation have been updated to use the new version string.
  > `"allowed_callers": ["code_execution_20260120"]`
  - *Implication*: Developers using programmatic tool calling must update their `type` field in tool definitions and any `allowed_callers` or `caller` references from `code_execution_20250825` to `code_execution_20260120`. The troubleshooting tip was also updated: "Verify your tool definition includes `"allowed_callers": ["code_execution_20260120"]`".
  - *Source*: [Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md)

- **Web search and web fetch now support programmatic invocation**: The documentation previously listed web search and web fetch among the tools that "cannot currently be called programmatically." Both have been removed from that list. Only MCP connector tools remain explicitly unsupported for programmatic calling.
  - *Implication*: Developers can now configure web search and web fetch tools with `allowed_callers` to enable Claude to invoke them from within a code execution container, enabling lower-latency multi-tool workflows involving web retrieval.
  - *Source*: [Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md)

- **New section: Using code execution with other execution tools**: A new section was added to the code execution tool documentation explaining that when Claude has access to both the Anthropic-managed code execution tool and a client-provided execution tool (such as bash or a custom REPL), it operates across two separate, isolated environments. The documentation provides a recommended system prompt to help Claude distinguish between the environments.
  > When you provide code execution alongside client-provided tools that also run code (such as a bash tool or custom REPL), Claude is operating in a multi-computer environment. The code execution tool runs in Anthropic's sandboxed container, while your client-provided tools run in a separate environment that you control. Claude can sometimes confuse these environments, attempting to use the wrong tool or assuming state is shared between them.

  The recommended system prompt snippet:
  ```text
  When multiple code execution environments are available, be aware that:
  - Variables, files, and state do NOT persist between different execution environments
  - Use the code_execution tool for general-purpose computation in Anthropic's sandboxed environment
  - Use client-provided execution tools (e.g., bash) when you need access to the user's local system, files, or data
  - If you need to pass results between environments, explicitly include outputs in subsequent tool calls rather than assuming shared state
  ```
  - *Implication*: Developers building agents that combine code execution with bash or a REPL tool should add explicit system prompt instructions to prevent Claude from confusing the two environments or assuming shared state. This is particularly relevant when web search or web fetch is also enabled, as those tools activate code execution automatically and can create an implicit second container environment.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

- **Bash tool: new callout for multi-environment awareness**: A new note was added to the "Combining with other tools" section of the bash tool documentation, cross-referencing the new code execution guidance.
  > If you're also using the code execution tool, Claude has access to two separate execution environments: your local bash session and Anthropic's sandboxed container. State is not shared between them. See Using code execution with other execution tools for guidance on prompting Claude to distinguish between environments.
  - *Implication*: Developers using both the bash tool and the code execution tool in the same session should be aware that environment state (files, variables, working directory) is not shared between them. The note links directly to the new guidance section.
  - *Source*: [Bash Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool.md)

## Notable Details

- The `code_execution_20260120` version string appears to follow a date-based versioning scheme (YYYYMMDD). The previous version `code_execution_20250825` dates to August 2025; the new version dates to January 20, 2026. This is a versioned tool identifier used in the `type` field of tool definitions and is distinct from the model version.
- The web search and web fetch removal from the "unsupported tools" list aligns with earlier documentation noting that these tools "enable code execution automatically" — they were already integrated with code execution, and full programmatic calling support has now been formalized.
- The code execution tool page itself still shows `code_execution_20250825` in its own model compatibility table and usage examples. The version bump to `20260120` applies specifically to the programmatic tool calling feature, not to standard code execution usage.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| [programmatic-tool-calling.md](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md) | Modified | +24 / -26 | Tool version updated from `code_execution_20250825` to `code_execution_20260120` throughout; web search and web fetch removed from list of unsupported programmatic tools |
| [code-execution-tool.md](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md) | Modified | +16 / -0 | New section added: "Using code execution with other execution tools" with multi-environment guidance and recommended system prompt |
| [bash-tool.md](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool.md) | Modified | +4 / -0 | New note added warning that bash tool and code execution tool operate in separate, non-shared environments |
