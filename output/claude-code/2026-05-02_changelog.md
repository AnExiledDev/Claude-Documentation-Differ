# Claude Code Documentation Changes — 2026-05-02

## Summary

One documentation page was modified with a single line change. The `agents` field example in the plugin manifest reference was updated from a directory string to an explicit array of file paths, aligning it with the documented pattern used for the `commands` field.

## Significant Changes

### Configuration

- **Plugin manifest `agents` field: directory string → array of file paths**: The example value for the `agents` key in the plugin manifest changed from a bare directory string to an explicit array containing a specific agent file path.

  Before:
  > `"agents": "./custom/agents/"`

  After:
  > `"agents": ["./custom/agents/reviewer.md"]`

  - *Implication*: This brings the `agents` field into parity with `commands`, which already used an array format (`["./custom/commands/special.md"]`). Developers authoring plugin manifests should use an array of explicit file paths for `agents` rather than a directory glob string. Whether directory strings remain valid is not addressed by this change; the example now demonstrates explicit enumeration.
  - *Source*: [plugins-reference.md](https://code.claude.com/docs/en/plugins-reference.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/claude-code/en/plugins-reference.md` | Modified | +1/-1 | `agents` manifest example updated from directory string to array of file paths |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-02*
