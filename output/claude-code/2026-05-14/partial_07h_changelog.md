# Claude Code Documentation Changes — 2026-05-14

## Summary

One page was modified: `agent-view.md`. The update documents new startup flags for `claude agents` that set per-session defaults for permission mode, model, and effort, and a new section covering how settings, plugins, and MCP server configuration flags are inherited by all dispatched sessions.

## Significant Changes

### Features

- **`claude agents` now accepts `--permission-mode`, `--model`, and `--effort` at startup**: Previously, these defaults had to be set per-session or via directory settings. Developers can now open agent view with a single command that applies those values to every session dispatched from it.
  > To set defaults for every session you dispatch from agent view, pass any of `--permission-mode`, `--model`, or `--effort` when opening it:
  > ```bash
  > claude agents --permission-mode plan --model opus --effort high
  > ```
  > The active defaults appear in the footer below the dispatch input.
  - *Implication*: Useful for CI-style workflows where all parallel sessions should share the same model or safety mode without requiring per-session flags.
  - *Source*: [Agent View](https://code.claude.com/docs/en/agent-view.md)

- **New "Settings, plugins, and MCP servers" section for `claude agents`**: Agent view now explicitly accepts the full set of configuration flags from `claude` — `--settings`, `--add-dir`, `--plugin-dir`, `--mcp-config`, and `--strict-mcp-config`. These flags apply to agent view itself and are forwarded to every session it dispatches.
  > Agent view accepts the same configuration flags as `claude` for loading settings, plugins, MCP servers, and additional directories. Each flag applies to agent view itself and is passed through to every session you dispatch from it, so a plugin or MCP server you load this way is available in those sessions too.

  | Flag | Effect |
  |---|---|
  | `--settings <file-or-json>` | Override settings for agent view and dispatched sessions |
  | `--add-dir <path>` | Grant file access to an additional directory |
  | `--plugin-dir <path>` | Load a plugin from a local directory |
  | `--mcp-config <file-or-json>` | Load MCP servers from a config file or JSON string |
  | `--strict-mcp-config` | Use only the MCP servers from `--mcp-config`, ignoring other MCP configuration |

  > Repeat `--add-dir`, `--plugin-dir`, or `--mcp-config` once per value. The space-separated form, such as `--add-dir a b c`, is not supported with `claude agents`.
  - *Implication*: Developers running agent view in CI or isolated environments can now load custom MCP configs and restrict plugin/server scope without modifying global settings.
  - *Source*: [Agent View](https://code.claude.com/docs/en/agent-view.md)

- **`bypassPermissions`/`auto` restriction clarified to cover both invocation paths**: The earlier docs only mentioned `claude --bg`. The updated text makes clear the same guard applies to `claude agents --permission-mode` as well.
  > Using `bypassPermissions` or `auto` is refused until you have accepted that mode by running `claude` with it once interactively, since those modes let a session you aren't watching act without approval. The same applies whether you pass the mode to `claude agents` or to `claude --bg --permission-mode`.
  - *Implication*: No behavioral change — this is a documentation clarification confirming the restriction is consistent across invocation paths.
  - *Source*: [Agent View](https://code.claude.com/docs/en/agent-view.md)

## Notable Details

- The section previously titled **"Permission mode and settings"** was renamed to **"Permission mode, model, and effort"** to reflect that model and effort level are now also configurable at the agent view level. Internal anchor links (`#permission-mode-and-settings` → `#permission-mode-model-and-effort`) were updated accordingly. Any external bookmarks or cross-references to the old anchor will silently break.
- The "Set the model" section gained a forward reference: *"To override it for the whole agent view session, pass `--model` when opening agent view."* This links the per-session model override workflow to the new startup flag.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| agent-view.md | Modified | SIGNIFICANT | +35/-5 | New `claude agents` startup flags for permission mode, model, effort; new section on settings/plugins/MCP config inheritance |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-14*
