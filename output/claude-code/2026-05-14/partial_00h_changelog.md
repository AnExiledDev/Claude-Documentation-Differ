# Claude Code Documentation Changes — 2026-05-14

## Summary

Claude Code version 2.1.141 was released on May 13, 2026, with approximately 50 new features and bug fixes including new environment variables, CLI flags, and UI improvements. The Output Styles documentation was substantially restructured with a new step-by-step authoring guide and a comparison table replacing verbose prose. Several pages received targeted clarifications around permissions precedence, hooks scope, and settings inheritance.

## Significant Changes

### Release Notes

- **Version 2.1.141 released (May 13, 2026)**: A large release covering new capabilities, behavioral fixes, and platform-specific patches across CLI, MCP, Bedrock, and VS Code.

  Key additions:
  > * Added `terminalSequence` field to hook JSON output so hooks can emit desktop notifications, window titles, and bells without a controlling terminal
  > * Added `CLAUDE_CODE_PLUGIN_PREFER_HTTPS` to clone GitHub plugin sources over HTTPS instead of SSH, for environments without a GitHub SSH key
  > * Added `ANTHROPIC_WORKSPACE_ID` environment variable for workload identity federation — scopes the minted token to a specific workspace when the federation rule covers more than one
  > * Added `claude agents --cwd <path>` to scope the session list to a directory
  > * `/feedback` can now include recent sessions (last 24 hours or 7 days) for issues spanning more than the current session
  > * Rewind menu: added "Summarize up to here" to compress earlier context while keeping recent turns intact
  > * Background agents launched via `/bg` or `←←` now preserve the current permission mode instead of reverting to default

  Notable bug fixes:
  > * Fixed background side-queries sending an unavailable Haiku model ID on Bedrock/Vertex/Foundry/gateway when no `ANTHROPIC_SMALL_FAST_MODEL` override is set — now falls back to the main-loop model
  > * Fixed `/model` in one session silently changing the autocompact threshold in other concurrent sessions
  > * Fixed hooks receiving a non-existent `transcript_path` after `EnterWorktree` switches the working directory
  > * Fixed prompt suggestions being silently disabled when an output style was configured
  > * Fixed MCP HTTP/SSE servers returning 403 on connect showing as "failed" instead of "needs auth"
  > * Bedrock: `awsCredentialExport` now always runs when configured instead of being skipped when ambient AWS credentials resolve, fixing auth for cross-account access

  - *Implication*: Developers using Bedrock/Vertex/Foundry should note the Haiku fallback fix and the `awsCredentialExport` always-run behavior change for cross-account setups. The `ANTHROPIC_WORKSPACE_ID` variable is relevant to organizations using workload identity federation.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Documentation / Output Styles

- **Output Styles page restructured**: The page was substantially rewritten. The custom style creation section now uses a step-by-step format with a working example. The "Comparisons to related features" section was replaced with a compact comparison table. A new "Related resources" section was added, and the `keep-coding-instructions` frontmatter field is now explained more clearly upfront.

  The new intro text makes the `keep-coding-instructions` decision explicit:
  > A custom output style adds your instructions to the system prompt and lets you choose whether to keep Claude Code's built-in software engineering instructions. Keep them when you're changing how Claude communicates but still coding, like always answering with a diagram. Leave them out when Claude isn't doing software engineering at all, like a writing assistant or data analyst.

  The new comparison table (replacing separate prose subsections):
  > | Feature                  | How it works                                                 | Use it when                                                             |
  > | :----------------------- | :----------------------------------------------------------- | :---------------------------------------------------------------------- |
  > | Output styles            | Modifies the system prompt                                   | You want a different role, tone, or default response format every turn  |
  > | CLAUDE.md                | Adds a user message after the system prompt                  | Claude should always know your project conventions and codebase context |
  > | `--append-system-prompt` | Appends to the system prompt without removing anything       | You want a one-off addition for a single invocation                     |
  > | Agents                   | Runs a subagent with its own system prompt, model, and tools | You want a separately scoped helper for a focused task                  |
  > | Skills                   | Loads task-specific instructions when invoked or relevant    | You have a reusable workflow                                            |

  - *Implication*: The restructuring makes the `keep-coding-instructions` flag more discoverable and the feature comparison easier to scan. The new example in the creation steps uses a "Diagrams first" style with `keep-coding-instructions: true`.
  - *Source*: [Output Styles](https://code.claude.com/docs/en/output-styles.md)

### Settings Precedence Clarifications

- **Settings scope interaction examples updated**: Two examples in the settings precedence section were changed from permission-based examples to scalar-setting examples, with an explicit note that permission rules behave differently (they merge, not override).

  Old text referenced permissions in both examples:
  > For example, if a permission is allowed in user settings but denied in project settings, the project setting takes precedence and the permission is blocked.

  New text uses `spinnerTipsEnabled` and `permissions.defaultMode` as examples and redirects to the permissions page:
  > For example, if your user settings set `spinnerTipsEnabled` to `true` and project settings set it to `false`, the project value applies. Permission rules behave differently because they merge across scopes rather than override. See [Settings precedence](#settings-precedence).

  The summary bullet was also made more precise:
  > **Inheritance**: Settings merge across scopes; scalar values from higher-priority scopes override, and arrays concatenate

  - *Implication*: This clarifies a common point of confusion: permissions don't simply "override" — they merge. Developers building configs that mix user and project-level permission rules should review the [permissions page](https://code.claude.com/docs/en/permissions.md) for the full model.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

## Minor Changes

- **admin-setup.md**: Added a note that several features (Claude Code on the web, Routines, Code Review, Remote Control, Chrome extension) require a Claude.ai account and are not available through Console API keys or cloud-provider credentials alone. Also updated the API provider intro to note that choice affects "which Claude Code features your developers can use." (+3/-1 lines)

- **agent-view.md**: The backgrounding documentation now explicitly mentions [monitors](/en/tools-reference#monitor-tool) alongside subagents and background commands as items that do not transfer when backgrounding from an interactive session. (+1/-1 lines)

- **hooks-guide.md**: Clarified `disableAllHooks` scope — hooks configured in managed settings still run unless `disableAllHooks` is also set there. Previous text implied the setting was global. (+1/-1 lines)

- **memory.md**: Fixed the CLAUDE.md load-order table — "User instructions" row now appears before "Project instructions" to match actual load order (broadest to most specific). The intro text was updated to say "from broadest scope to most specific, so a project instruction appears in context after a user instruction." (+2/-2 lines)

- **permissions.md**: Expanded the scope-precedence example to clarify bidirectionality: a user-level deny also blocks a project-level allow, because deny rules from any scope are evaluated before allow rules. (+1/-1 lines)

- **plugins.md**: Clarified that `--plugin-dir` cannot override plugins that managed settings force-*disable* (not just force-enable, as previously stated). (+1/-1 lines)

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| changelog.md | Modified | SIGNIFICANT | +64/-0 | v2.1.141 release notes added |
| output-styles.md | Modified | SIGNIFICANT | +66/-90 | Page restructured: step-by-step creation guide, comparison table, new Related resources section |
| settings.md | Modified | SIGNIFICANT | +4/-4 | Scope interaction examples updated; clarified scalar vs. array merging behavior |
| admin-setup.md | Modified | MINOR | +3/-1 | Added note about Claude.ai-required features for Bedrock/Vertex/Foundry deployments |
| memory.md | Modified | MINOR | +2/-2 | CLAUDE.md table row order corrected to match actual load order |
| agent-view.md | Modified | MINOR | +1/-1 | Monitors added to backgrounding transfer list |
| hooks-guide.md | Modified | MINOR | +1/-1 | `disableAllHooks` managed-settings scope clarified |
| permissions.md | Modified | MINOR | +1/-1 | Deny-rule bidirectionality made explicit |
| plugins.md | Modified | MINOR | +1/-1 | `--plugin-dir` override limitation extended to force-disabled plugins |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-14*
