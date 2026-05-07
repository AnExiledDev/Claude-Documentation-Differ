# Claude API Documentation Changes — 2026-05-07

## Summary

Six pages in the agents-and-tools documentation were updated with the same internal link change: the "API and data retention" reference URL was moved from `/docs/en/build-with-claude/` to `/docs/en/manage-claude/`. One page (`code-execution-tool.md`) also includes a PHP SDK example fix, removing named-parameter syntax from `files->retrieveMetadata()` and `files->download()` calls.

## Significant Changes

### Documentation Structure

- **"API and data retention" page relocated**: The cross-reference link to the ZDR/HIPAA eligibility documentation was updated from `/docs/en/build-with-claude/api-and-data-retention` to `/docs/en/manage-claude/api-and-data-retention` across all six agents-and-tools pages.
  > For ZDR eligibility across all features, see [API and data retention](/docs/en/manage-claude/api-and-data-retention).
  - *Implication*: Developers following inbound links from these pages to the data retention policy will reach the new URL path. Any direct bookmarks or links to the old `/build-with-claude/api-and-data-retention` path may need updating.
  - *Affected pages*: [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md), [MCP Connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md), [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md), [Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md), [Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md), [Strict Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use.md)

### PHP SDK — Files API

- **Named parameters removed from `files->retrieveMetadata()` and `files->download()`**: The PHP code example in the code execution tool docs was updated to use positional arguments instead of named parameter syntax for the beta Files API methods.
  > ```php
  > // Before
  > $fileMetadata = $client->beta->files->retrieveMetadata(fileID: $fileId);
  > $fileContent = $client->beta->files->download(fileID: $fileId);
  >
  > // After
  > $fileMetadata = $client->beta->files->retrieveMetadata($fileId);
  > $fileContent = $client->beta->files->download($fileId);
  > ```
  - *Implication*: PHP developers using the beta Files API should use positional arguments when calling `retrieveMetadata()` and `download()`. This aligns the PHP SDK example with standard positional-argument calling conventions.
  - *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| agents-and-tools/agent-skills/overview.md | Modified | +1/-1 | Updated data retention link path |
| agents-and-tools/mcp-connector.md | Modified | +1/-1 | Updated data retention link path |
| agents-and-tools/tool-use/code-execution-tool.md | Modified | +4/-4 | Updated data retention link path; fixed PHP SDK named-parameter syntax |
| agents-and-tools/tool-use/computer-use-tool.md | Modified | +1/-1 | Updated data retention link path |
| agents-and-tools/tool-use/programmatic-tool-calling.md | Modified | +1/-1 | Updated data retention link path |
| agents-and-tools/tool-use/strict-tool-use.md | Modified | +1/-1 | Updated data retention link path |

---
*Generated from Claude API documentation changes detected on 2026-05-07*
