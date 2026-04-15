# Claude Code Documentation Changes — 2026-04-15

## Summary

Four pages received minor documentation clarifications with no new pages added or removed. The changes address two distinct topics: Windows shell-detection troubleshooting (updated identically across overview, quickstart, and setup pages) and a behavioral note about the routines `/fire` endpoint `text` field being freeform and unparsed.

## Significant Changes

### Windows Installation

- **Expanded shell-detection troubleshooting for Windows**: Three pages (overview, quickstart, setup) received an identical update that adds CMD-specific error guidance and clearer prompt-format descriptions for both shells.

  Before:
  > If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. Use the PowerShell command above instead. Your prompt shows `PS C:\` when you're in PowerShell.

  After:
  > If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. If you see `'irm' is not recognized as an internal or external command`, you're in CMD, not PowerShell. Your prompt shows `PS C:\` when you're in PowerShell and `C:\` without the `PS` when you're in CMD.

  - *Implication*: Users who accidentally run the CMD installer (`install.cmd`) from PowerShell (or run the PowerShell `irm`-based command from CMD) now get bidirectional diagnostic help. The `'irm' is not recognized` case was previously unaddressed.
  - *Source*: [Overview](https://code.claude.com/docs/en/overview.md), [Quickstart](https://code.claude.com/docs/en/quickstart.md), [Setup](https://code.claude.com/docs/en/setup.md)

### Routines

- **Clarified `/fire` endpoint `text` field is freeform and unparsed**: The description of the optional `text` request body parameter was reworded to explicitly document that its value is passed as a literal string — not interpreted as structured data.

  Before:
  > The request body accepts an optional `text` field that's appended to the routine's configured prompt as a one-shot user turn.

  After:
  > The request body accepts an optional `text` field for run-specific context such as an alert body or a failing log, passed to the routine alongside its saved prompt. The value is freeform text and is not parsed: if you send JSON or another structured payload, the routine receives it as a literal string.

  - *Implication*: Developers who send structured data (e.g., a JSON alert payload) in the `text` field should serialize it to a string on the caller's side. The routine will not parse it — it receives the raw bytes as typed text.
  - *Source*: [Routines](https://code.claude.com/docs/en/routines.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| overview.md | Modified | +1/-1 | Added CMD `irm` error hint and bidirectional prompt-format descriptions for Windows |
| quickstart.md | Modified | +1/-1 | Same Windows shell-detection update as overview.md |
| setup.md | Modified | +1/-1 | Same Windows shell-detection update as overview.md |
| routines.md | Modified | +1/-1 | Clarified `/fire` endpoint `text` field is freeform, unparsed text |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-15*
