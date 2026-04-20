# Claude Code Documentation Changes — 2026-04-20

## Summary

Three pages were modified in this update. The primary substantive change marks agent-based hooks (`type: "agent"`) as experimental across both the hooks reference and hooks guide pages. The setup page received a minor markup cleanup with no content impact.

## Significant Changes

### Configuration — Hooks

- **Agent hooks marked experimental**: Both the hooks reference and hooks guide now carry an explicit warning that `type: "agent"` hooks are experimental and subject to change. The warning recommends command hooks for production workflows.

  In `hooks.md` and `hooks-guide.md`, the agent hook inline description now reads:
  > `"type": "agent"`: spawn a subagent that can use tools like Read, Grep, and Glob to verify conditions before returning a decision. **Agent hooks are experimental and may change.**

  A `<Warning>` block was also added directly before the "Agent-based hooks" section in both files:
  > Agent hooks are experimental. Behavior and configuration may change in future releases. For production workflows, prefer [command hooks].

  - *Implication*: Developers relying on `type: "agent"` hooks in production should be aware that the API and behavior are not yet stable. The docs now explicitly direct production use cases toward `type: "command"` hooks instead.
  - *Source*: [hooks.md](https://code.claude.com/docs/en/hooks.md), [hooks-guide.md](https://code.claude.com/docs/en/hooks-guide.md)

## Notable Details

- **setup.md markup cleanup**: Code block attributes in the installation examples were cleaned up — repeated `theme={null}` attributes (appearing four times each) were reduced to a single `theme={null}`. This is a documentation source markup fix with no visible change to the rendered page.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| hooks.md | Modified | +5/-1 | Added experimental warning to agent hooks section and inline description |
| hooks-guide.md | Modified | +5/-1 | Added experimental warning to agent hooks section and inline description |
| setup.md | Modified | +5/-5 | Removed duplicate `theme={null}` attributes from code block markup |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-20*
