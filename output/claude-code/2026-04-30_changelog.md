# Claude Code Documentation Changes — 2026-04-30

## Summary

One troubleshooting page was updated with 14 new lines and no deletions. The changes add a new Windows-specific installation error section and a PATH configuration note for non-bash shells (fish, Nushell).

## Significant Changes

### Troubleshooting

- **New Windows install error: file lock during download**: Added a new error entry and full troubleshooting section for the PowerShell installer failing with `The process cannot access the file ... because it is being used by another process`.
  > If the PowerShell installer fails with `Failed to download binary: The process cannot access the file ... because it is being used by another process`, the installer couldn't write to `%USERPROFILE%\.claude\downloads`. This usually means a previous install attempt is still running, or antivirus software is scanning a partially downloaded binary in that folder.

  The documented fix is to close any other PowerShell installer windows, wait for antivirus scans to release the file, then delete the downloads folder and re-run:
  ```powershell
  Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\downloads"
  irm https://claude.ai/install.ps1 | iex
  ```
  - *Implication*: Windows users hitting this error (commonly triggered by antivirus or a stalled prior install) now have a documented recovery path.
  - *Source*: [Troubleshoot installation and login](https://code.claude.com/docs/en/troubleshoot-install.md)

- **PATH guidance extended to fish and Nushell**: The section covering PATH configuration after installation now explicitly mentions non-bash shells.
  > For other shells such as fish or Nushell, add `~/.local/bin` to your PATH using your shell's own configuration syntax, then restart your terminal.
  - *Implication*: Users of fish or Nushell who follow the Linux/macOS install guide will see a direct callout rather than needing to infer the configuration themselves.
  - *Source*: [Troubleshoot installation and login](https://code.claude.com/docs/en/troubleshoot-install.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| troubleshoot-install.md | Modified | +14 / -0 | New Windows file-lock error section; PATH note for fish/Nushell |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-30*
