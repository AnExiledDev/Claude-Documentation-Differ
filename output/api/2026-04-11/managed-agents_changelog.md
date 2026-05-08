# Claude API Documentation Changes — 2026-04-11

## Summary

Four Managed Agents documentation pages were updated in this batch. Two types of changes are present: a syntax correction to the `--model` flag in `ant` CLI examples across three pages, and a domain change for Claude Agent SDK links in the migration guide.

## Significant Changes

### Managed Agents CLI

- **`--model` flag now requires object syntax**: The `ant beta:agents create` command's `--model` parameter changed from accepting a bare model string to requiring an object with an `id` key. This affects the quickstart, agent-setup, and GitHub integration guides.

  Before:
  > `--model claude-sonnet-4-6`

  After:
  > `--model '{id: claude-sonnet-4-6}'`

  - *Implication*: Developers using the `ant` CLI to create managed agents must update their commands and scripts to pass the model as an object (`{id: <model-name>}`) rather than a plain string. This is a breaking change for existing shell scripts or automation that calls `ant beta:agents create`.
  - *Source*: [quickstart.md](https://platform.claude.com/docs/en/managed-agents/quickstart.md), [agent-setup.md](https://platform.claude.com/docs/en/managed-agents/agent-setup.md), [github.md](https://platform.claude.com/docs/en/managed-agents/github.md)

### Agent SDK Documentation Relocation

- **Claude Agent SDK docs moved to `code.claude.com`**: Two internal relative links to the Agent SDK overview (`/docs/en/agent-sdk/overview`) in the migration guide were updated to absolute URLs pointing to a new domain.

  Before:
  > `[Claude Agent SDK](/docs/en/agent-sdk/overview)`

  After:
  > `[Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview)`

  - *Implication*: The Claude Agent SDK documentation now lives at `https://code.claude.com` rather than under the main platform docs. Developers with bookmarks or internal links to the old relative path should update them. This may indicate a broader reorganization of agent-related documentation onto a dedicated domain.
  - *Source*: [migration.md](https://platform.claude.com/docs/en/managed-agents/migration.md)

## Migration Guidance

- **`ant` CLI `--model` syntax**: Update any scripts that call `ant beta:agents create` with a bare model string:
  ```bash
  # Before
  ant beta:agents create \
    --name "Coding Assistant" \
    --model claude-sonnet-4-6 \
    --system "You are a helpful coding agent." \
    --tool '{type: agent_toolset_20260401}'

  # After
  ant beta:agents create \
    --name "Coding Assistant" \
    --model '{id: claude-sonnet-4-6}' \
    --system "You are a helpful coding agent." \
    --tool '{type: agent_toolset_20260401}'
  ```

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| managed-agents/quickstart.md | Modified | +1/-1 | `--model` flag updated to object syntax |
| managed-agents/agent-setup.md | Modified | +1/-1 | `--model` flag updated to object syntax |
| managed-agents/github.md | Modified | +1/-1 | `--model` flag updated to object syntax |
| managed-agents/migration.md | Modified | +2/-2 | Agent SDK links updated to `code.claude.com` absolute URLs |

---
*Generated from Claude API documentation changes detected on 2026-04-11*
