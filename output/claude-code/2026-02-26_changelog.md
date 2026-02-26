# Claude Code Documentation Changes — 2026-02-26

## Summary

Two pages were modified in this update. The most significant change is to the auto memory feature: it is now enabled by default (previously under gradual rollout), with new toggle controls in `/memory`, `settings.json`, and a clarified explanation of environment variable precedence. The `/copy` command also received an updated description reflecting a new interactive code block picker.

## Significant Changes

### Features

- **`/copy` command now supports interactive code block selection**: The description for `/copy` was updated to reflect new behavior when code blocks are present in the last response.
  > Copy the last response to clipboard. When code blocks are present, shows an interactive picker to select individual code blocks or the full response
  - *Implication*: Developers can now selectively copy individual code blocks rather than the entire assistant response, reducing friction when working with multi-block outputs.
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

- **Auto memory is now enabled by default**: The gradual rollout phase has ended. The documentation note was updated from an opt-in instruction to a statement of default availability.
  > Auto memory is enabled by default. To toggle it on or off, use `/memory` and select the auto-memory toggle.
  - *Implication*: Users who previously had no auto memory because they were not in the rollout will now have it active. Those who want to disable it must do so explicitly.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

### Configuration

- **`autoMemoryEnabled` setting added to `settings.json`**: Auto memory can now be disabled globally (user settings) or per-project (project settings) via a new `autoMemoryEnabled` key.
  > Disable auto memory for all projects by adding `autoMemoryEnabled` to your user settings:
  > ```json
  > // ~/.claude/settings.json
  > { "autoMemoryEnabled": false }
  > ```
  > Disable auto memory for a single project by adding `autoMemoryEnabled` to the project settings:
  > ```json
  > // .claude/settings.json
  > { "autoMemoryEnabled": false }
  > ```
  - *Implication*: Teams can now disable auto memory at the project level via committed configuration, giving consistent behavior across contributors without relying on per-user environment variables.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

- **`CLAUDE_CODE_DISABLE_AUTO_MEMORY` environment variable precedence clarified**: The variable now explicitly takes precedence over both the `/memory` toggle and `settings.json`. The old confusing "double-negative logic" explanation (`DISABLE=0` meaning "don't disable") was removed.
  > Override all other settings with the `CLAUDE_CODE_DISABLE_AUTO_MEMORY` environment variable. This takes precedence over both the `/memory` toggle and `settings.json`, making it useful for CI or managed environments.
  - *Implication*: CI pipelines and managed environments can reliably suppress auto memory writes using the environment variable, regardless of what any settings file specifies.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

## Notable Details

- The `/memory` file selector now also exposes an **auto-memory toggle** directly in the UI, complementing the settings file and environment variable controls. This gives three discrete control layers with a clear precedence order: environment variable > `settings.json` > UI toggle.
- The old documentation described `CLAUDE_CODE_DISABLE_AUTO_MEMORY=0` as the opt-in mechanism during gradual rollout. That instruction has been removed entirely, reflecting that the feature is no longer gated behind a rollout.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `interactive-mode.md` | Modified | +1 / -1 | Updated `/copy` command description to document interactive code block picker |
| `memory.md` | Modified | +19 / -3 | Auto memory now default-enabled; added `autoMemoryEnabled` settings key; clarified env var precedence; added `/memory` UI toggle |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-26*
