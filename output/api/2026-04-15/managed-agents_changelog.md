# Claude API Documentation Changes — 2026-04-15

## Summary

All nine Managed Agents documentation pages were updated. The primary change is a CLI flag rename from `--environment` to `--environment-id` across the `ant` CLI tool. The Files API documentation additionally drops the `files-api-2025-04-14` beta header requirement and adds new CLI examples for file listing and download operations.

## Significant Changes

### Agent SDK (Managed Agents)

- **CLI flag renamed: `--environment` → `--environment-id`**: The `ant beta:sessions create` command's flag for specifying an environment has been renamed across all managed-agents documentation.
  > ```bash
  > # Before
  > ant beta:sessions create \
  >   --agent "$AGENT_ID" \
  >   --environment "$ENVIRONMENT_ID"
  >
  > # After
  > ant beta:sessions create \
  >   --agent "$AGENT_ID" \
  >   --environment-id "$ENVIRONMENT_ID"
  > ```
  - *Implication*: Any scripts or automation using the `ant` CLI to create sessions must update the flag name. This is a breaking change for CLI users only — the REST API (`environment` field in the JSON body) is unaffected.
  - *Source*: [Sessions](https://platform.claude.com/docs/en/managed-agents/sessions.md), [Onboarding](https://platform.claude.com/docs/en/managed-agents/onboarding.md), [Files](https://platform.claude.com/docs/en/managed-agents/files.md), [GitHub](https://platform.claude.com/docs/en/managed-agents/github.md), [MCP Connector](https://platform.claude.com/docs/en/managed-agents/mcp-connector.md), [Vaults](https://platform.claude.com/docs/en/managed-agents/vaults.md), [Multi-agent](https://platform.claude.com/docs/en/managed-agents/multi-agent.md), [Define Outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes.md), [Migration](https://platform.claude.com/docs/en/managed-agents/migration.md)

### Files API (Managed Agents)

- **`files-api-2025-04-14` beta header no longer required for session-scoped file operations**: When listing or downloading files scoped to a managed-agent session, the cURL examples now show only `managed-agents-2026-04-01` in the `anthropic-beta` header, dropping the previously required `files-api-2025-04-14` value.
  > ```bash
  > # Before
  > curl -fsSL "https://api.anthropic.com/v1/files?scope_id=sesn_abc123" \
  >   -H "anthropic-beta: managed-agents-2026-04-01,files-api-2025-04-14"
  >
  > # After
  > curl -fsSL "https://api.anthropic.com/v1/files?scope_id=sesn_abc123" \
  >   -H "anthropic-beta: managed-agents-2026-04-01"
  > ```
  - *Implication*: The Files API is now fully subsumed under the `managed-agents-2026-04-01` beta umbrella for session-scoped operations. Developers can simplify their headers when using the Files API within managed-agent sessions.
  - *Source*: [Files](https://platform.claude.com/docs/en/managed-agents/files.md)

- **New CLI examples for listing and downloading session-scoped files**: The `ant` CLI commands for file operations are now documented alongside the existing cURL, Python, and TypeScript examples.
  > ```bash
  > # List files associated with a session
  > ant beta:files list --scope-id sesn_abc123 \
  >   --beta files-api-2025-04-14 \
  >   --beta managed-agents-2026-04-01
  >
  > # Download a file
  > ant beta:files download --file-id "$FILE_ID" --output output.txt
  > ```
  - *Implication*: Note that the CLI `list` command still passes `files-api-2025-04-14` explicitly via `--beta` flags, while the REST API no longer requires it — suggesting the CLI handles beta negotiation differently than direct API calls.
  - *Source*: [Files](https://platform.claude.com/docs/en/managed-agents/files.md)

- **New CLI example for mounting multiple files**: A YAML CLI code block was added to the multi-file mounting section, matching the existing JSON and Python examples.
  > ```yaml
  > resources:
  >   - type: file
  >     file_id: file_abc123
  >     mount_path: /workspace/data.csv
  >   - type: file
  >     file_id: file_def456
  >     mount_path: /workspace/config.json
  > ```
  - *Source*: [Files](https://platform.claude.com/docs/en/managed-agents/files.md)

## Migration Guidance

- **`ant` CLI session creation**: Replace `--environment` with `--environment-id` in all `ant beta:sessions create` invocations.
  ```bash
  # Before
  ant beta:sessions create --agent "$AGENT_ID" --environment "$ENVIRONMENT_ID"

  # After
  ant beta:sessions create --agent "$AGENT_ID" --environment-id "$ENVIRONMENT_ID"
  ```

- **Beta headers for session-scoped Files API calls**: If you were including `files-api-2025-04-14` in your `anthropic-beta` header for file listing/download within managed-agent sessions, it can now be removed.
  ```bash
  # Before
  -H "anthropic-beta: managed-agents-2026-04-01,files-api-2025-04-14"

  # After
  -H "anthropic-beta: managed-agents-2026-04-01"
  ```

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| managed-agents/files.md | Modified | +27/-4 | Added CLI examples for file listing/download; removed `files-api-2025-04-14` beta header requirement; added multi-file mount YAML example |
| managed-agents/sessions.md | Modified | +1/-1 | CLI flag renamed `--environment` → `--environment-id` |
| managed-agents/onboarding.md | Modified | +1/-1 | CLI flag renamed `--environment` → `--environment-id` |
| managed-agents/define-outcomes.md | Modified | +1/-1 | CLI flag renamed `--environment` → `--environment-id` |
| managed-agents/github.md | Modified | +1/-1 | CLI flag renamed `--environment` → `--environment-id` |
| managed-agents/mcp-connector.md | Modified | +1/-1 | CLI flag renamed `--environment` → `--environment-id` |
| managed-agents/migration.md | Modified | +1/-1 | CLI flag renamed `--environment` → `--environment-id` |
| managed-agents/multi-agent.md | Modified | +1/-1 | CLI flag renamed `--environment` → `--environment-id` |
| managed-agents/vaults.md | Modified | +1/-1 | CLI flag renamed `--environment` → `--environment-id` |

---
*Generated from Claude API documentation changes detected on 2026-04-15*
