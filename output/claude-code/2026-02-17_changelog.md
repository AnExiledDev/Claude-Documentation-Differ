# Claude Code Documentation Changes — 2026-02-17

## Summary

Three documentation pages received updates focused on plugin marketplace management and version control. The most significant changes introduce new capabilities for plugin versioning, release channel management, and marketplace-level component control through strict mode configuration.

## Significant Changes

### Plugin Marketplace Configuration

- **Strict mode documentation expanded**: The `strict` field now has comprehensive documentation explaining how it controls component authority between `plugin.json` and marketplace entries.
  > `strict: true` (default): `plugin.json` is the authority. The marketplace entry can supplement it with additional components, and both sources are merged.
  > `strict: false`: The marketplace entry is the entire definition. If the plugin also has a `plugin.json` that declares components, that's a conflict and the plugin fails to load.
  - *Implication*: Marketplace operators can now choose between allowing plugin authors to control components (strict mode on) or taking full control themselves (strict mode off). This enables curated marketplaces that restructure plugins differently than authors intended.
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

- **Plugin source types formalized in table**: Documentation now includes a comprehensive table showing all five plugin source types with their fields and notes.
  > | Source | Type | Fields | Notes |
  > | Relative path | `string` (e.g. `"./my-plugin"`) | — | Local directory within the marketplace repo. Must start with `./` |
  > | `github` | object | `repo`, `ref?`, `sha?` | |
  > | `url` | object | `url` (must end .git), `ref?`, `sha?` | Git URL source |
  > | `npm` | object | `package`, `version?`, `registry?` | Installed via `npm install` |
  > | `pip` | object | `package`, `version?`, `registry?` | Installed via pip |
  - *Implication*: Developers now have clear guidance on all supported plugin distribution methods and their specific requirements.
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

- **Marketplace vs plugin source distinction clarified**: New note explicitly differentiates between marketplace sources (where the catalog lives) and plugin sources (where individual plugins are fetched from).
  > **Marketplace source** — where to fetch the `marketplace.json` catalog itself. Set when users run `/plugin marketplace add` or in `extraKnownMarketplaces` settings. Supports `ref` (branch/tag) but not `sha`.
  > **Plugin source** — where to fetch an individual plugin listed in the marketplace. Set in the `source` field of each plugin entry inside `marketplace.json`. Supports both `ref` (branch/tag) and `sha` (exact commit).
  - *Implication*: This resolves potential confusion about pinning behavior at different levels of the plugin distribution system.
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

### Version Resolution and Release Channels

- **New release channel setup documentation**: Comprehensive new section explaining how to create "stable" and "latest" release channels using multiple marketplaces pointing to different refs.
  > To support "stable" and "latest" release channels for your plugins, you can set up two marketplaces that point to different refs or SHAs of the same repo. You can then assign the two marketplaces to different user groups through managed settings.
  - *Implication*: Organizations can now implement sophisticated rollout strategies with early-access and stable tracks for different user groups. This requires the plugin's `plugin.json` to declare different versions at each ref or commit.
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

- **Version precedence warning added**: New warning clarifies that `plugin.json` version always wins over marketplace version.
  > When possible, avoid setting the version in both places. The plugin manifest always wins silently, which can cause the marketplace version to be ignored. For relative-path plugins, set the version in the marketplace entry. For all other plugin sources, set it in the plugin manifest.
  - *Implication*: Developers should choose one location for version declarations to avoid silent conflicts and ensure updates work correctly.
  - *Source*: [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

### Plugin Caching and File Resolution

- **Simplified external dependency guidance**: Documentation removed "Option 2: Restructure your marketplace" approach, leaving only symlinks as the recommended solution.
  - *Removed content*: The previous documentation suggested setting plugin source to `"./"` with `strict: false` to copy the entire marketplace root, giving plugins access to sibling directories.
  - *Implication*: This simplification suggests symlinks are the preferred pattern for sharing files across plugins. The restructuring approach may have been deprecated or found to be less maintainable.
  - *Source*: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

- **Plugin definition clarified**: New introductory sentence provides clear terminology.
  > A **plugin** is a self-contained directory of components that extends Claude Code with custom functionality. Plugin components include skills, agents, hooks, MCP servers, and LSP servers.
  - *Implication*: Sets clear expectations about plugin scope and capabilities upfront.
  - *Source*: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

- **Caching behavior documentation condensed**: Removed detailed explanation of five source types from caching section (now covered in plugin sources section).
  - *Implication*: Reduces duplication between plugin-marketplaces.md and plugins-reference.md documentation.
  - *Source*: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

- **Version management warning in plugin reference**: New warning emphasizes the importance of version bumping for cache invalidation.
  > Claude Code uses the version to determine whether to update your plugin. If you change your plugin's code but don't bump the version in `plugin.json`, your plugin's existing users won't see your changes due to caching.
  - *Implication*: Plugin developers must remember to bump versions or users won't receive updates due to caching behavior.
  - *Source*: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

## Notable Details

- **Code block formatting cleaned up**: The overview.md file had duplicate `theme={null}` attributes removed from bash, PowerShell, batch, and shell code blocks. This appears to be a formatting cleanup with no functional impact.
- **Relative path plugin installation note refined**: Removed suggestion to "restructure your marketplace so the shared directory is inside the plugin source path" from the installation note, keeping only the symlinks recommendation.
- **Plugin cache location documented**: Explicitly states that marketplace plugins are copied to `~/.claude/plugins/cache` for versioning and security.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| plugin-marketplaces.md | Modified | +132/-15 | Added strict mode documentation, version resolution/release channels section, plugin source types table, and marketplace vs plugin source clarification |
| plugins-reference.md | Modified | +13/-44 | Simplified external dependency guidance to symlinks-only, removed duplicate caching documentation, added version management warning |
| overview.md | Modified | +5/-5 | Cleaned up duplicate theme attributes in code blocks |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-17*
