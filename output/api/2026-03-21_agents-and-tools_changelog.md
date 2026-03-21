# Claude API Documentation Changes — 2026-03-21

## Summary

Three pages in the agents-and-tools section received minor documentation formatting updates. All changes are cosmetic or documentation-rendering fixes — no API parameters, endpoints, models, or behaviors changed.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| agents-and-tools/tool-use/code-execution-tool.md | Modified | +9/-4 | Added self-contained shell setup commands to bash examples; punctuation fix |
| agents-and-tools/agent-skills/quickstart.md | Modified | +1/-1 | Added `nocheck` flag to a Shell code block |
| agents-and-tools/mcp-connector.md | Modified | +1/-1 | Added `nocheck` flag to a TypeScript code block |

## Notable Details

- **Shell example self-containment** (`code-execution-tool.md`): Three `bash Shell` code blocks gained `hidelines` rendering directives along with setup commands (`cd "$(mktemp -d)"` and `printf 'name,value\nfoo,1\nbar,2\n' > data.csv`). These lines create a temporary working directory and sample CSV file before running `curl` commands against the Files API. The lines are hidden in the rendered docs but make examples copy-paste runnable without prior file setup. *Source*: [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

- **`nocheck` code block flags**: Both `agent-skills/quickstart.md` and `mcp-connector.md` had `nocheck` appended to a code fence (`\`\`\`bash Shell nocheck` and `\`\`\`typescript nocheck`). This is a docs-platform directive to skip syntax/lint checking on those blocks — no user-facing change. *Sources*: [Agent Skills Quickstart](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart.md), [MCP Connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md)

- **Minor punctuation fix** (`code-execution-tool.md`): An em-dash in a prose sentence was replaced with a comma: `"context window—improving accuracy"` → `"context window, improving accuracy"`. No semantic change.

---
*Generated from Claude API documentation changes detected on 2026-03-21*
