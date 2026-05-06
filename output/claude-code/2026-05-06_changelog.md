# Claude Code Documentation Changes — 2026-05-06

## Summary

Fifteen reference pages were updated to document features shipping in Claude Code v2.1.129. The most significant changes are: a new `skillOverrides` settings key for controlling skill visibility without editing SKILL.md files; a new `--plugin-url` CLI flag for loading plugins from remote URLs; LLM gateway model discovery changed from automatic to opt-in via `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY`; fine-grained tool streaming now enabled by default for direct Anthropic API connections; and a breaking-with-deprecation plugin manifest schema change that moves `themes` and `monitors` under an `experimental` key.

---

## Significant Changes

### Skills

- **New `skillOverrides` setting (v2.1.129+)**: A new settings key controls skill visibility from settings files without editing the skill's `SKILL.md` frontmatter. Useful for shared project repos or MCP-provided skills you don't own.
  > Per-skill visibility overrides keyed by skill name. Value is `"on"`, `"name-only"`, `"user-invocable-only"`, or `"off"`. Lets you hide or collapse a skill without editing its SKILL.md. Does not apply to plugin skills, which are managed through `/plugin`. The `/skills` menu writes these to `.claude/settings.local.json`.

  | Value | Listed to Claude | In `/` menu |
  |:---|:---|:---|
  | `"on"` | Name and description | Yes |
  | `"name-only"` | Name only | Yes |
  | `"user-invocable-only"` | Hidden | Yes |
  | `"off"` | Hidden | Hidden |

  - *Implication*: Allows hiding or compressing skill descriptions to reclaim context budget. Setting low-priority skills to `"name-only"` frees token budget for skills Claude actually needs to reason about.
  - *Source*: [Skills](https://code.claude.com/docs/en/skills.md), [Settings](https://code.claude.com/docs/en/settings.md)

- **`/skills` menu now writes `skillOverrides`**: The `/skills` interactive list gained a `Space` keyboard shortcut for toggling visibility states.
  > List available skills. Press `t` to sort by token count. Press `Space` to hide a skill from Claude or the `/` menu, then `Enter` to save

  - *Implication*: Skill visibility management is now interactive — no manual JSON editing required. Changes persist to `.claude/settings.local.json`.
  - *Source*: [Commands](https://code.claude.com/docs/en/commands.md)

### Plugins

- **New `--plugin-url` CLI flag**: Fetches a plugin `.zip` archive from a URL for a single session, without requiring a local directory or permanent installation.
  > Fetch a plugin `.zip` archive from a URL for this session only. Each flag takes one URL. Repeat the flag for multiple plugins. Example: `claude --plugin-url https://example.com/plugin.zip`

  - *Implication*: Enables testing CI-built plugin artifacts or staging releases without touching the local plugin cache. The same trust considerations apply as for any plugin source.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md), [Plugins](https://code.claude.com/docs/en/plugins.md)

- **`themes` and `monitors` moved under `experimental` key in `plugin.json`** (breaking schema change with deprecation path): These plugin manifest fields must now be declared under `"experimental": { ... }`. The top-level keys still work but trigger a `claude plugin validate` warning; a future release will require the new path.
  > Components under the `experimental` key, `themes` and `monitors`, have a manifest schema that may change between releases while they stabilize. Where you declare them is a separate migration: the top level still works, `claude plugin validate` warns, and a future release will require `experimental.*`.

  Before:
  ```json
  {
    "themes": "./themes/",
    "monitors": "./monitors.json"
  }
  ```

  After:
  ```json
  {
    "experimental": {
      "themes": "./themes/",
      "monitors": "./monitors.json"
    }
  }
  ```

  - *Implication*: Plugin authors should migrate `plugin.json` manifests now. Run `claude plugin validate` to identify affected plugins. Inline monitor declarations (`monitors` key at top level) must also move to `experimental.monitors`.
  - *Source*: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

### Environment Variables

- **`CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` (new; default off)**: Controls whether the `/model` picker is populated from your LLM gateway's `/v1/models` endpoint. **This is a default behavior change**: discovery was automatic in v2.1.126–v2.1.128; it is now opt-in as of v2.1.129.
  > Set to `1` to populate the `/model` picker from your gateway's `/v1/models` endpoint when `ANTHROPIC_BASE_URL` points at an Anthropic-compatible gateway such as LiteLLM, Kong, or an internal proxy. Off by default because gateways backed by a shared API key would otherwise show every user every model the key can access. Discovered models are still filtered by the `availableModels` allowlist.

  - *Implication*: Users who relied on automatic discovery in v2.1.126–2.1.128 must now set `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` explicitly. Multi-tenant deployments benefit from the new default. Min version bumped from v2.1.126 to v2.1.129.
  - *Source*: [Env Vars](https://code.claude.com/docs/en/env-vars.md), [LLM Gateway](https://code.claude.com/docs/en/llm-gateway.md)

- **`CLAUDE_CODE_ENABLE_FINE_GRAINED_TOOL_STREAMING` behavior changed (now on by default)**: Previously this was an explicit opt-in. It is now enabled by default for direct Anthropic API connections.
  > Controls whether tool call inputs stream from the API as Claude generates them. With this off, a large tool input such as a long file write arrives only after Claude finishes generating it, which can look like it's hanging. Enabled by default for direct Anthropic API connections. Set to `0` to opt out. Set to `1` to force-enable even when the server-side default is off. Has no effect on Bedrock, Vertex, Foundry, or gateway connections.

  - *Implication*: Large file writes and other tool calls will now stream progressively by default on direct API connections, reducing the appearance of hanging. Set to `0` to restore the prior buffered behavior.
  - *Source*: [Env Vars](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE` (new)**: Opt-in automatic background upgrades for Homebrew and WinGet installations.
  > Set to `1` to let Claude Code run your package manager's upgrade command in the background when a new version is available. Applies to Homebrew and WinGet installations. Other package managers continue to show the upgrade command without running it.

  - *Implication*: Homebrew and WinGet users can opt into the same auto-update experience as native installs. On WinGet, upgrades may fail while Claude Code is running because Windows locks the executable — Claude Code falls back to showing the manual command in that case.
  - *Source*: [Setup](https://code.claude.com/docs/en/setup.md), [Env Vars](https://code.claude.com/docs/en/env-vars.md)

- **`CLAUDE_CODE_FORCE_SYNC_OUTPUT` (new)**: Force-enables DEC private mode 2026 synchronized output for terminals that support BSU/ESU but don't respond to the capability probe.
  > Set to `1` to force-enable DEC private mode 2026 synchronized output when your terminal supports it but is not auto-detected. Useful for emulators such as Emacs `eat` that implement BSU/ESU but do not reply to the capability probe. Has no effect under tmux.

  - *Implication*: Addresses rendering artifacts in Emacs `eat` and similar terminal emulators without requiring tmux.
  - *Source*: [Env Vars](https://code.claude.com/docs/en/env-vars.md)

### Configuration & Settings

- **`--settings` flag: merging behavior now explicitly documented**: The description now states that values passed via `--settings` override matching keys from settings files while leaving unset keys at their file-based values.
  > Path to a settings JSON file or an inline JSON string. Values you set here override the same keys in your `settings.json` files for this session. Keys you omit keep their file-based values. See settings precedence.

  - *Implication*: Clarifies that `--settings` is a partial overlay, not a full replacement — important when using inline JSON in CI to pass targeted per-run overrides.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md), [Settings](https://code.claude.com/docs/en/settings.md)

### Interactive Mode

- **Command history search default scope changed to all projects**: The `Ctrl+R` reverse history search now defaults to searching across all projects rather than the current session. This restores behavior from before v2.1.124.
  > Search defaults to prompts from all projects. Press `Ctrl+S` to cycle the scope through this session, this project, and all projects.

  - *Implication*: The previous default (current session only) was a regression introduced in v2.1.124. The fix restores breadth-first search; `Ctrl+S` now narrows the scope.
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

### Monitoring

- **PR counter now includes merge requests and MCP-triggered PRs**: The `claude_code.pull_request.count` OTel metric definition was broadened.
  > Incremented when Claude Code creates a pull request or merge request through a shell command or an MCP tool.

  - *Implication*: OTel dashboards tracking pull request activity will now also capture GitLab merge requests and PRs created via MCP tools, providing a more complete picture.
  - *Source*: [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage.md)

---

## Notable Details

- **LLM gateway min version bumped to v2.1.129**: The minimum Claude Code version for gateway model discovery (when opted in) increased from v2.1.126 to v2.1.129 in the docs, reflecting the behavioral change from auto to opt-in.
- **`skillOverrides` cross-referenced in context management docs**: Both `features-overview.md` and `how-claude-code-works.md` now point to `skillOverrides` as the recommended way to reduce context cost for third-party skills, alongside the existing `disable-model-invocation: true` frontmatter approach.
- **Setup page softened "require manual updates" to "require manual updates by default"**: This wording change in `setup.md` reflects the new `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE` opt-in for Homebrew and WinGet.
- **Plugin "Path behavior rules" updated**: The rules section in `plugins-reference.md` now consistently refers to `experimental.themes` and `experimental.monitors`, keeping it in sync with the schema migration.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| plugins-reference.md | Modified | +26/-20 | New "Experimental components" section; `themes`/`monitors` moved to `experimental.*` key; `--plugin-url` listed as session load method |
| skills.md | Modified | +27/-1 | New "Override skill visibility from settings" section documenting `skillOverrides`; cross-ref added to skill budget guidance |
| env-vars.md | Modified | +4/-1 | Three new env vars (`CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY`, `CLAUDE_CODE_FORCE_SYNC_OUTPUT`, `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE`); `FINE_GRAINED_TOOL_STREAMING` default changed to on |
| setup.md | Modified | +6/-2 | Homebrew/WinGet auto-update opt-in via `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE`; caveats for WinGet and Linux package managers |
| plugins.md | Modified | +6/-0 | `--plugin-url` usage example for testing zip-packaged plugins from a URL |
| settings.md | Modified | +2/-1 | New `skillOverrides` setting entry; `--settings` layer precedence clarified |
| cli-reference.md | Modified | +2/-1 | New `--plugin-url` flag; `--settings` description expanded |
| llm-gateway.md | Modified | +1/-1 | Gateway model discovery changed to opt-in; min version updated to v2.1.129 |
| model-config.md | Modified | +1/-1 | Updated reference to gateway discovery being opt-in |
| commands.md | Modified | +1/-1 | `/skills` updated with `Space` shortcut for `skillOverrides` |
| features-overview.md | Modified | +1/-1 | Cross-reference to `skillOverrides` added for context cost management |
| how-claude-code-works.md | Modified | +1/-1 | Cross-reference to `skillOverrides` added |
| interactive-mode.md | Modified | +1/-1 | History search default scope changed to all projects (pre-2.1.124 behavior restored) |
| monitoring-usage.md | Modified | +1/-1 | PR counter broadened to include merge requests and MCP-created PRs |
| headless.md | Modified | +1/-1 | `--plugin-url` listed alongside `--plugin-dir` in bare mode table |

---

*Generated from Claude Code CLI documentation changes detected on 2026-05-06*
