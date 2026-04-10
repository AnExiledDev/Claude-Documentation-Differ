# Claude Code Documentation Changes — 2026-04-10

## Summary

Five pages were updated to document a new `claude-code@latest` Homebrew cask that tracks the latest release channel, alongside the existing `claude-code` stable cask. Install, upgrade, uninstall, and troubleshooting instructions were updated across setup, overview, quickstart, discover-plugins, and troubleshooting pages to reflect both cask options.

## Significant Changes

### Installation & Package Management

- **New `claude-code@latest` Homebrew cask**: Homebrew now offers two casks with distinct update cadences. The original `claude-code` cask targets a stable channel that is typically about a week behind and skips releases with major regressions. The new `claude-code@latest` cask targets the latest channel and delivers new versions as soon as they ship.
  > Homebrew offers two casks. `claude-code` tracks the stable release channel, which is typically about a week behind and skips releases with major regressions. `claude-code@latest` tracks the latest channel and receives new versions as soon as they ship.
  - *Implication*: Developers who want bleeding-edge features can switch to `brew install --cask claude-code@latest`; those who prefer stability can stay on `claude-code`. The choice of cask determines the release channel — the in-app `/config` release channel setting does not apply to Homebrew installs.
  - *Source*: [Setup](https://code.claude.com/docs/en/setup.md), [Overview](https://code.claude.com/docs/en/overview.md), [Quickstart](https://code.claude.com/docs/en/quickstart.md)

- **Homebrew release channel selection via cask name**: The setup docs now explicitly note that Homebrew users select their release channel by choosing a cask, not through the `/config` → Auto-update channel setting.
  > Homebrew installations choose a channel by cask name instead of this setting: `claude-code` tracks stable and `claude-code@latest` tracks latest.
  - *Implication*: Enterprise admins using managed settings to enforce a release channel should be aware this mechanism does not extend to Homebrew installs.
  - *Source*: [Setup](https://code.claude.com/docs/en/setup.md)

- **Uninstall instructions updated for both casks**: The uninstall section in `setup.md` now provides separate `brew uninstall` commands for the stable and latest casks, rather than a single generic command.
  > Remove the Homebrew cask you installed. If you installed the stable cask: `brew uninstall --cask claude-code`. If you installed the latest cask: `brew uninstall --cask claude-code@latest`.
  - *Source*: [Setup](https://code.claude.com/docs/en/setup.md), [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)

## Notable Details

- **`brew cleanup` scope widened**: The upgrade note in `setup.md` changed from `brew cleanup claude-code` (package-specific) to `brew cleanup` (all packages). Developers who relied on the scoped command to reclaim disk space from only Claude Code should note the new command clears cached versions for all Homebrew packages.

- **Plugin troubleshooting updated**: The "unknown command" troubleshooting tip in `discover-plugins.md` now lists `brew upgrade claude-code@latest` as an alternative upgrade command alongside `brew upgrade claude-code`.
  - *Source*: [Discover Plugins](https://code.claude.com/docs/en/discover-plugins.md)

- **Duplicate `theme={null}` markup cleaned up**: Code block attributes in `overview.md` and `setup.md` previously contained up to 31 repetitions of `theme={null}` per block. These were collapsed to a single instance — a rendering artifact fix with no user-visible content impact.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| setup.md | Modified | +19 / -9 | Two-cask Homebrew docs: install, upgrade, channel selection, uninstall; `brew cleanup` scope change |
| overview.md | Modified | +8 / -6 | Two-cask explanation added to Homebrew tab; code block markup cleanup |
| quickstart.md | Modified | +3 / -1 | Two-cask explanation added to Homebrew tab |
| discover-plugins.md | Modified | +1 / -1 | Upgrade troubleshooting hint updated to include `@latest` cask |
| troubleshooting.md | Modified | +1 / -1 | Uninstall hint updated to acknowledge `@latest` cask variant |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-10*
