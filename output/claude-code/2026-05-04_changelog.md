# Claude Code Documentation Changes — 2026-05-04

## Summary

Three pages were updated with no new or removed pages. The largest change adds new color theme tokens to the terminal configuration reference — including a new "Usage meter and speaker labels" section, additional fullscreen background tokens, and rainbow gradient tokens for the `ultrathink`/`ultraplan` keywords. The monitoring reference expanded `source`/`decision_source` field descriptions with full per-value definitions. The install troubleshooting guide improved AVX diagnostics to explicitly cover VMs and VPS environments.

## Significant Changes

### Theme & Terminal Configuration

- **New `suggestion` base color token**: A `suggestion` token has been added to the base colors table, controlling autocomplete suggestions and selection highlights in pickers.
  > `suggestion` — Autocomplete suggestions and selection highlight in pickers
  - *Implication*: Developers customizing themes can now control autocomplete suggestion color separately from other text styles.
  - *Source*: [Terminal Config](https://code.claude.com/docs/en/terminal-config.md)

- **Four new fullscreen background tokens**: The fullscreen rendering section now documents four additional background color tokens.
  > | `userMessageBackgroundHover` | Background behind a message while hovered or expanded |
  > | `messageActionsBackground`   | Background behind the selected message when the action bar is open |
  > | `bashMessageBackgroundColor` | Background behind `!` shell command entries in the transcript |
  > | `memoryBackgroundColor`      | Background behind `#` memory entries in the transcript |
  - *Implication*: Theme authors can now fine-tune hover states, the message action bar, shell command entries, and memory entries individually rather than relying on fallback colors.
  - *Source*: [Terminal Config](https://code.claude.com/docs/en/terminal-config.md)

- **New "Usage meter and speaker labels" section**: A new subsection documents four tokens for the `/usage` view and message attribution labels.
  > Adjust the bar shown in the `/usage` view and the labels that distinguish your messages from Claude's.
  >
  > | `rate_limit_fill`  | Filled portion of the usage meter |
  > | `rate_limit_empty` | Unfilled portion of the usage meter |
  > | `briefLabelYou`    | Color of the `You` label on your messages |
  > | `briefLabelClaude` | Color of the `Claude` label on assistant messages |
  - *Implication*: Teams building branded or accessibility-focused environments can now control the usage meter bar colors and the speaker label colors for both the human and assistant turns.
  - *Source*: [Terminal Config](https://code.claude.com/docs/en/terminal-config.md)

- **Shimmer token pairs explicitly listed**: The shimmer section now enumerates all six paired shimmer tokens by name instead of giving only a generic description.
  > * `claude` and `claudeShimmer`
  > * `warning` and `warningShimmer`
  > * `permission` and `permissionShimmer`
  > * `promptBorder` and `promptBorderShimmer`
  > * `inactive` and `inactiveShimmer`
  > * `fastMode` and `fastModeShimmer`
  - *Implication*: Theme authors no longer need to guess which base tokens have shimmer counterparts.
  - *Source*: [Terminal Config](https://code.claude.com/docs/en/terminal-config.md)

- **Rainbow gradient tokens for `ultrathink` and `ultraplan`**: New token family documented for the seven-color rainbow gradient rendered on these keywords in the prompt input.
  > The `ultrathink` and `ultraplan` keywords in the prompt input are rendered with a seven-color rainbow gradient. The token names follow the pattern `rainbow_<color>` and `rainbow_<color>_shimmer`, where `<color>` is `red`, `orange`, `yellow`, `green`, `blue`, `indigo`, or `violet`.
  - *Implication*: Theme authors can override all 14 rainbow tokens (7 base + 7 shimmer) to match a custom palette or suppress the gradient effect.
  - *Source*: [Terminal Config](https://code.claude.com/docs/en/terminal-config.md)

### Monitoring & Observability

- **Full per-value explanation for `source` / `decision_source` fields**: The `tool_decision` event `source` attribute, the file-edit counter `source` field, and the tool execution span `decision_source` field now include a complete definition for each possible value instead of a bare list.
  > * `"config"`: Decided automatically without prompting, based on project settings, enterprise managed policy, `--allowedTools` or `--disallowedTools` flags, the active permission mode, or because the tool is inherently safe.
  > * `"hook"`: A `PreToolUse` or `PermissionRequest` hook returned the decision.
  > * `"user_permanent"`: Emitted when the user chose "Always allow" when prompted, saving a rule to their personal settings. Also emitted for later calls that match that saved rule. Treated as an accept.
  > * `"user_temporary"`: Emitted when the user chose "Yes" or "Yes, for this session" when prompted, without saving a rule. Also emitted for later calls in the same session that match that session-scoped allow. Treated as an accept.
  > * `"user_abort"`: Emitted when the user dismissed the permission prompt without answering. Treated as a reject.
  > * `"user_reject"`: Emitted when the user chose "No" when prompted, or a call matched a deny rule in their personal settings. Treated as a reject.
  - *Implication*: Teams building dashboards or alerts on telemetry data can now correctly classify accept vs. reject outcomes and distinguish automatic config-driven decisions from interactive user choices.
  - *Source*: [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **Cross-reference links added to `source` descriptions**: The `source` attribute in the `claude_code.tool.blocked_on_user` span table and the inline descriptions in the file-edit counter and tool execution span now link to the `#tool-decision-event` anchor for the full definitions.
  - *Implication*: Readers navigating the monitoring reference will find consistent, navigable cross-references rather than repeated inline definitions.
  - *Source*: [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage.md)

### Installation Troubleshooting

- **AVX detection improved for VMs and VPS environments**: The "Missing instruction set on older CPUs" entry was renamed to "Missing AVX instruction set" and expanded to cover hypervisors that do not pass AVX through to the guest.
  > On a VPS or VM, run `grep -m1 -ow avx /proc/cpuinfo`; an empty result means AVX is not available to the guest.
  - *Implication*: Users running Claude Code in cloud VMs now have an explicit diagnostic command. The Linux CPU model command was also updated from a `cat | grep | head` pipeline to the more direct `grep -m1 "model name" /proc/cpuinfo`.
  - *Source*: [Troubleshoot Install](https://code.claude.com/docs/en/troubleshoot-install.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| terminal-config.md | Modified | +31 / -6 | New `suggestion` token, four new fullscreen background tokens, new "Usage meter and speaker labels" section, explicit shimmer token list, rainbow gradient tokens for `ultrathink`/`ultraplan` |
| monitoring-usage.md | Modified | +14 / -8 | Full per-value definitions for `source`/`decision_source` fields; cross-reference links added |
| troubleshoot-install.md | Modified | +5 / -1 | AVX troubleshooting expanded to cover VMs/VPS with explicit `grep` diagnostic command |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-04*
