# Claude Code Documentation Changes — 2026-05-22

## Summary

One documentation page was modified: two bullet points were deleted from the v2.1.147 release notes in the Claude Code changelog. Both removed entries referenced the `Workflow` tool, suggesting those features were retracted or rolled back from that release.

## Minor Changes

- **changelog.md**: Removed 2 bullet points from the v2.1.147 release notes (+0/-2 lines)

## Notable Details

The two deleted lines from the v2.1.147 changelog section are substantive, despite the small line count:

1. **Workflow tool removal**: The entry `Added the \`Workflow\` tool for deterministic multi-agent orchestration. It is off by default — set \`CLAUDE_CODE_WORKFLOWS=1\` to enable` was removed. This indicates the Workflow tool announcement was retracted from the v2.1.147 release notes — either the feature was rolled back, not yet ready, or incorrectly attributed to this version.

2. **Sandbox hardening removal**: The entry `Hardened REPL and Workflow tool sandboxes against prototype-pollution and thenable-based escapes` was also removed. As this was directly tied to the Workflow tool, its removal is consistent with the retraction of the Workflow tool entry.

Developers who saw the original v2.1.147 notes and planned to use `CLAUDE_CODE_WORKFLOWS=1` should note the feature is no longer documented for this version. The remaining v2.1.147 entries (pinned background sessions, `/code-review` rename, auto-updater improvements, diff rendering, and prompt history deduplication) are unaffected.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| changelog.md | Modified | MINOR | +0/-2 | Removed Workflow tool entries from v2.1.147 release notes |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-22*
