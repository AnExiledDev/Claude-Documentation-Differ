# Documentation Diff Report

**Comparing:** `415fac4ecda4d937aa8970c61ceb42b29c2767a8` → `HEAD`
**Generated:** 2026-03-25T01:04:56.438711+00:00

## Summary

- New pages: 1
- Removed pages: 0
- Modified pages: 6

## New Pages

- `docs/api/en/agent-sdk/tool-search.md`

## Modified Pages

### `docs/api/en/agent-sdk/custom-tools.md`

+586 / -613 lines

**New sections:**
- # Give Claude custom tools
- ## Quick reference
- ## Create a custom tool
- ### Weather tool example
- # Define a tool: name, description, input schema, handler
- # Return a content array - Claude sees this as the tool result
- # Wrap the tool in an in-process MCP server
- ### Call a custom tool
- # ResultMessage is the final message after all tool calls complete
- ### Add more tools
- # Define a second tool for the same server
- # 'hours' isn't in the schema - read it with .get() to make it optional
- # Rebuild the server with both tools in the array
- ### Add tool annotations
- ## Control tool access
- ### Tool name format
- ### Configure allowed tools
- ## Handle errors
- # Return the failure as a tool result so Claude can react to it.
- # is_error marks this as a failed call rather than odd-looking data.
- # Catching here keeps the agent loop alive. An uncaught exception
- # would end the whole query() call.
- ## Return images and resources
- ### Images
- # Define a tool that fetches an image from a URL and returns it to Claude
- ### Resources
- ## Example: unit converter
- # z.enum() in TypeScript becomes an "enum" constraint in JSON Schema.
- # The dict schema has no equivalent, so full JSON Schema is required.
- ## Next steps
- ## Related documentation

**Removed sections:**
- # Custom Tools
- ## Creating Custom Tools
- # Define a custom tool using the @tool decorator
- # Call weather API
- # Create an SDK MCP server with the custom tool
- ## Using Custom Tools
- ### Tool Name Format
- ### Configuring Allowed Tools
- # Use the custom tools with Claude
- # Add other tools as needed
- # Extract and print response
- ### Multiple Tools Example
- # Define multiple tools using the @tool decorator
- # Translation logic here
- # Search logic here
- # Allow only specific tools with streaming input
- # "mcp__utilities__search_web" is NOT allowed
- ## Type Safety with Python
- # Simple type mapping - recommended for most cases
- # Access arguments with type hints for IDE support
- # For more complex schemas, you can use JSON Schema format
- # Process with advanced schema validation
- ## Error Handling
- ## Example Tools
- ### Database Query Tool
- ### API Gateway Tool
- # For complex schemas with enums, use JSON Schema format
- ### Calculator Tool
- # Use a safe math evaluation library in production
- ## Related Documentation

### `docs/api/en/agent-sdk/mcp.md`

+8 / -67 lines

**Removed sections:**
- ### Alternative: Change the permission mode
- ### How it works
- ### Configure tool search

### `docs/api/en/agent-sdk/python.md`

+66 / -5 lines

**New sections:**
- #### `ToolAnnotations`
- # Drain the interrupted task's messages (including its ResultMessage)
- # subtype is "error_during_execution" for interrupted tasks
- # Now receive the new response
- # Option 1: dict literal (recommended, no import needed)
- # Option 2: constructor-style (returns a plain dict)
- # config.budget_tokens would raise AttributeError

**Removed sections:**
- # Process the new response

### `docs/api/en/agent-sdk/typescript.md`

+46 / -3 lines

**New sections:**
- #### `ToolAnnotations`
- ### `SDKLocalCommandOutputMessage`

### `docs/api/en/agent-sdk/user-input.md`

+8 / -6 lines

### `docs/api/en/build-with-claude/context-editing.md`

+183 / -384 lines

**Removed sections:**
- # ...
- # The SDK logs compaction events when verbose logging is enabled.
- # You'll see messages like:
- # Token usage 105000 has exceeded the threshold of 100000. Performing compaction.
- # Compaction complete. New token usage: 2500
