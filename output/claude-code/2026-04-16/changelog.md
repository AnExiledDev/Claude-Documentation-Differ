# Claude Code Documentation Changes — 2026-04-16

## Summary

This update reflects the v2.1.111 release. Major additions include the `/ultrareview` command for cloud-based multi-agent code review (research preview), the new `xhigh` effort level for Opus 4.7, and a new plugin dependency versioning system with semver constraints. Auto mode has been promoted out of flag-gated preview and is now available in the `Shift+Tab` cycle for Max, Team, Enterprise, and API plan users without `--enable-auto-mode`.

---

## Significant Changes

### Models

- **Opus 4.7 now the primary model with `xhigh` effort as default**: The model configuration page was substantially rewritten to document Opus 4.7 as the current flagship. On the Anthropic API, the `opus` alias now resolves to Opus 4.7 (requires v2.1.111+). Default by plan:
  > "**Max and Team Premium**: defaults to Opus 4.7 / **Pro, Team Standard, Enterprise, and Anthropic API**: defaults to Sonnet 4.6 / **Bedrock, Vertex, and Foundry**: defaults to Sonnet 4.5"
  - *Implication*: Enterprise pay-as-you-go and API users should note: "On April 23, 2026, the default model for Enterprise pay-as-you-go and Anthropic API users will change to Opus 4.7. To keep a different default, set `ANTHROPIC_MODEL` or the `model` field in server-managed settings."
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

- **New `xhigh` effort level for Opus 4.7**: Five effort levels are now available on Opus 4.7 — `low`, `medium`, `high`, `xhigh`, `max` — with `xhigh` sitting between `high` and `max`. Opus 4.6 and Sonnet 4.6 retain four levels (`low`, `medium`, `high`, `max`; no `xhigh`). The default on Opus 4.7 is `xhigh` for all plans and providers.
  > "When you first run Opus 4.7, Claude Code applies `xhigh` even if you previously set a different effort level for Opus 4.6 or Sonnet 4.6. Run `/effort` again to choose a different level after switching."
  - *Implication*: Users upgrading to Opus 4.7 will see higher token spend by default compared to Opus 4.6. Run `/effort high` or lower to reduce costs on routine tasks. If a level the active model doesn't support is set, Claude Code falls back to the highest supported level at or below it (`xhigh` → `high` on Opus 4.6).
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

- **Adaptive reasoning documented for Opus 4.7**: New subsection "Adaptive reasoning and fixed thinking budgets" explains that Opus 4.7 always uses adaptive reasoning; the existing escape hatch (`CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`) does not apply to it.
  > "Opus 4.7 always uses adaptive reasoning. The fixed thinking budget mode and `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` do not apply to it."
  > "On Opus 4.6 and Sonnet 4.6, you can set `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` to revert to the previous fixed thinking budget controlled by `MAX_THINKING_TOKENS`."
  - *Implication*: Teams relying on `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` to enforce fixed thinking behavior must remain on Opus 4.6 or Sonnet 4.6.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

- **New capability values for third-party model pinning**: Two new values can be added to `_SUPPORTED_CAPABILITIES` to unlock Opus 4.7-specific features on custom Bedrock/Vertex/Foundry endpoints:

  | Capability value    | Enables                                 |
  |---------------------|-----------------------------------------|
  | `xhigh_effort`      | The `xhigh` effort level (v2.1.111+)    |
  | `adaptive_thinking` | Adaptive reasoning per-step allocation  |

  - *Implication*: Operators pinning Opus 4.7 via an ARN or custom deployment name should add `xhigh_effort` and `adaptive_thinking` to `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` to surface these features in the CLI.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

---

### Features

- **`/ultrareview` — cloud-based multi-agent code review**: New command and new documentation page. Launches a fleet of reviewer agents in a remote sandbox; every finding is independently reproduced and verified before being reported.
  > "Compared to a local `/review`, ultrareview offers: **Higher signal**: every reported finding is independently reproduced and verified, so the results focus on real bugs rather than style suggestions / **Broader coverage**: many reviewer agents explore the change in parallel / **No local resource use**: the review runs entirely in a remote sandbox, so your terminal stays free for other work while it runs"
  - Usage: `/ultrareview` reviews current branch vs. default branch (including uncommitted/staged changes); `/ultrareview 1234` reviews a specific GitHub PR directly from GitHub.
  - Duration: typically 5–10 minutes; runs as a background task, trackable via `/tasks`.
  - Pricing: Pro and Max receive 3 free runs (one-time, non-refreshing allotment); after that, billed as extra usage ($5–$20 per review depending on change size). Team and Enterprise have no free runs.
  - Requirements: Claude.ai account authentication required. Not available with API-key-only auth, Bedrock, Vertex AI, Foundry, or Zero Data Retention organizations.
  - *Source*: [Find bugs with ultrareview](https://code.claude.com/docs/en/ultrareview.md)

- **Effort level controls fully documented**: The `/effort` command, `effortLevel` setting, `--effort` flag, and `CLAUDE_CODE_EFFORT_LEVEL` environment variable are now documented with a decision table. The `/model` picker shows a left/right arrow slider for effort on supported models. Current effort level appears next to the logo/spinner (e.g., "with low effort").
  - Effort can also be set per-skill or per-subagent via the `effort:` frontmatter field, which overrides the session level but not the environment variable.
  - `max` effort is session-only by default (resets on restart unless set via `CLAUDE_CODE_EFFORT_LEVEL`).
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md), [Commands](https://code.claude.com/docs/en/commands.md)

---

### Plugins

- **Plugin dependency version constraints** (new page): Plugin authors can now declare semver version constraints on plugin dependencies in `plugin.json`. Requires Claude Code v2.1.110+.
  > "A plugin can depend on other plugins by listing them in `plugin.json` or in its marketplace entry. By default, a dependency tracks the latest available version… Version constraints let you hold a dependency at a tested version range until you choose to move."

  Example `plugin.json`:
  ```json
  {
    "name": "deploy-kit",
    "version": "3.1.0",
    "dependencies": [
      "audit-logger",
      { "name": "secrets-vault", "version": "~2.1.0" }
    ]
  }
  ```
  - Version resolution uses git tags in the format `{plugin-name}--v{version}`. Accepts any semver range expression (`~`, `^`, `>=`, `=`, hyphen ranges).
  - When multiple plugins constrain the same dependency, Claude Code intersects their ranges. Incompatible ranges produce a `range-conflict` error and disable the dependent plugin.
  - Error states (`range-conflict`, `dependency-version-unsatisfied`, `no-matching-tag`) are visible in `claude plugin list`, `/plugin`, and `/doctor`. Check programmatically with `claude plugin list --json` and read the `errors` field.
  - *Implication*: Plugin authors distributing through git-backed marketplaces should begin tagging releases using the `{name}--v{version}` convention to support downstream pinning.
  - *Source*: [Constrain plugin dependency versions](https://code.claude.com/docs/en/plugin-dependencies.md)

- **Plugins reference updated**: The manifest schema's `dependencies` field now documents version constraint objects alongside bare plugin-name strings. The reference cross-links to the new `plugin-dependencies` page.
  - *Source*: [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md)

---

### Auto Mode

- **Auto mode no longer requires `--enable-auto-mode` flag**: Auto mode now appears in the `Shift+Tab` cycle for eligible accounts without needing a launch flag.
  > "On Max, Team, Enterprise, and Anthropic API plans, auto mode appears in the `Shift+Tab` cycle without the `--enable-auto-mode` flag."
  - *Implication*: Users on eligible plans who were unaware of the flag will now see auto mode in the cycle after upgrading to v2.1.111.
  - *Source*: [Permission modes](https://code.claude.com/docs/en/permission-modes.md)

- **Auto mode model requirement updated to include Opus 4.7**: Eligible models are now "Claude Sonnet 4.6, Opus 4.6, or Opus 4.7 on Team, Enterprise, and API plans; Claude Opus 4.7 only on Max plans."
  - *Implication*: Max subscribers must use Opus 4.7 specifically; Sonnet 4.6 and Opus 4.6 are not eligible on Max.
  - *Source*: [Permission modes](https://code.claude.com/docs/en/permission-modes.md)

---

### Desktop

- **"Cowork tab unavailable on Intel Macs" limitation removed**: The section documenting this restriction has been deleted from the Desktop documentation page, indicating the limitation has been resolved.
  - *Source*: [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md)

---

### Environment Variables

- **`CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` scoped to Opus 4.6 and Sonnet 4.6**: The variable description now explicitly notes it has no effect on Opus 4.7.
  > "Set to `1` to disable adaptive reasoning on Opus 4.6 and Sonnet 4.6 and fall back to the fixed thinking budget controlled by `MAX_THINKING_TOKENS`. Has no effect on Opus 4.7, which always uses adaptive reasoning"
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

- **`OTEL_LOG_RAW_API_BODIES`** documented: Emits full API request and response bodies as OpenTelemetry log events for debugging.
  - *Source*: [Environment variables](https://code.claude.com/docs/en/env-vars.md)

---

## New Pages

- **[plugin-dependencies.md](https://code.claude.com/docs/en/plugin-dependencies.md)** — Complete guide for plugin authors on declaring semver version constraints on plugin dependencies in `plugin.json`. Covers constraint syntax (semver ranges), the git tag naming convention (`{name}--v{version}`), multi-plugin constraint intersection, error diagnosis, and resolution steps.

- **[ultrareview.md](https://code.claude.com/docs/en/ultrareview.md)** — Documentation for the `/ultrareview` research preview command (v2.1.86+). Covers CLI usage, PR mode (pass a PR number), pricing tiers and free run allotments, background task tracking via `/tasks`, and a side-by-side comparison against `/review`.

---

## Notable Details

- **`max` effort is session-only**: Unlike `low`, `medium`, `high`, and `xhigh` (which persist across sessions), `max` resets at session end unless set via `CLAUDE_CODE_EFFORT_LEVEL`. This is a behavioral difference not obvious from the level name.
- **`xhigh` silent fallback**: Setting `xhigh` on Opus 4.6 or Sonnet 4.6 silently falls back to `high`. Operators should be aware of this when mixing model versions in fleet deployments.
- **`/less-permission-prompts` skill added in v2.1.111**: Scans transcripts for common read-only Bash and MCP calls and proposes a prioritized allowlist for `.claude/settings.json`. Not yet separately documented beyond the changelog entry.
- **Windows PowerShell tool rolling out**: v2.1.111 adds a progressive rollout of a PowerShell tool on Windows, opt-in/out via `CLAUDE_CODE_USE_POWERSHELL_TOOL`. Also available on Linux/macOS with `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` (requires `pwsh` in PATH).
- **Plan file names now derived from prompts**: v2.1.111 changes plan file naming from random words to prompt-derived slugs (e.g., `fix-auth-race-snug-otter.md`). Scripts that locate plan files by name pattern may need updating.
- **Read-only bash commands with glob patterns no longer prompt**: Commands like `ls *.ts` and commands starting with `cd <project-dir> &&` no longer trigger a permission prompt in v2.1.111.
- **`/ultrareview` extra usage requirement**: The account or organization must have extra usage enabled before a paid review can launch. Run `/extra-usage` to check or change the setting.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| plugin-dependencies.md | New | +104 | Guide for plugin dependency versioning with semver constraints |
| ultrareview.md | New | +85 | Documentation for /ultrareview cloud code review command |
| model-config.md | Modified | +75/-33 | Opus 4.7 default model, xhigh effort level, adaptive reasoning sections |
| changelog.md | Modified | +39/-1 | v2.1.111 release notes added |
| commands.md | Modified | +80/-79 | /ultrareview added, /effort updated for xhigh, /review cross-links ultrareview |
| common-workflows.md | Modified | +11/-11 | Minor updates (model version references) |
| plugins-reference.md | Modified | +18/-13 | dependencies field with version constraints documented |
| desktop.md | Modified | +8/-13 | Removed Intel Mac Cowork limitation section; auto mode model requirements updated |
| permission-modes.md | Modified | +5/-11 | Auto mode no longer requires flag; Opus 4.7 model requirement added |
| amazon-bedrock.md | Modified | +7/-4 | Minor updates (model version references) |
| google-vertex-ai.md | Modified | +6/-4 | Minor updates (model version references) |
| env-vars.md | Modified | +4/-3 | CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING scoped to 4.6 models; OTEL_LOG_RAW_API_BODIES added |
| microsoft-foundry.md | Modified | +4/-2 | Minor updates (model version references) |
| sub-agents.md | Modified | +3/-3 | Minor updates |
| vs-code.md | Modified | +3/-3 | Minor updates |
| settings.md | Modified | +3/-1 | Minor additions |
| cli-reference.md | Modified | +2/-2 | Minor updates |
| fast-mode.md | Modified | +1/-1 | Minor update |
| github-actions.md | Modified | +1/-1 | Minor update |
| skills.md | Modified | +1/-1 | Minor update |
| statusline.md | Modified | +1/-1 | Minor update |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-16*
