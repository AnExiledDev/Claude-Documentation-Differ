# Claude Code Documentation Changes — 2026-03-12

## Summary

Six pages were modified to document the v2.1.73 release. The headline change is a new `modelOverrides` setting that lets enterprise administrators map individual model picker entries to provider-specific IDs (Bedrock ARNs, Vertex AI version names, Foundry deployment names). The `/output-style` command was deprecated in favor of `/config`, and output styles are now locked at session start to stabilize prompt caching.

## Significant Changes

### Configuration

- **New `modelOverrides` setting for per-version provider ID mapping**: A new settings key lets administrators route each specific model version to a distinct provider endpoint, going beyond the single-ID-per-family constraint of the existing `ANTHROPIC_DEFAULT_*_MODEL` environment variables.
  > `modelOverrides` maps individual Anthropic model IDs to the provider-specific strings that Claude Code sends to your provider's API. When a user selects a mapped model in the `/model` picker, Claude Code uses your configured value instead of the built-in default.
  > This lets enterprise administrators route each model version to a specific Bedrock inference profile ARN, Vertex AI version name, or Foundry deployment name for governance, cost allocation, or regional routing.

  Example from the docs:
  ```json
  {
    "modelOverrides": {
      "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
      "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
      "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
    }
  }
  ```
  Key behavior notes documented:
  - Keys must be exact Anthropic model IDs from the Models overview (including date suffixes); unknown keys are silently ignored.
  - On Bedrock, `modelOverrides` takes precedence over inference profiles auto-discovered at startup.
  - Values supplied via `ANTHROPIC_MODEL`, `--model`, or `ANTHROPIC_DEFAULT_*_MODEL` are passed to the provider as-is and are **not** transformed by `modelOverrides`.
  - `availableModels` allowlist is evaluated against the Anthropic model ID (not the override value), so alias entries like `"opus"` still match even when versions are mapped to ARNs.
  - *Implication*: Enterprises can now expose multiple versions of the same model family in the `/model` picker, each routed to a separate inference profile — enabling cost allocation and governance without end users bypassing organizational controls.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md), [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md), [Settings](https://code.claude.com/docs/en/settings.md)

- **`modelOverrides` added to settings reference table**: The settings page now includes `modelOverrides` in its configuration key reference.
  > `modelOverrides` — Map Anthropic model IDs to provider-specific model IDs such as Bedrock inference profile ARNs. Each model picker entry uses its mapped value when calling the provider API.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Deprecations

- **`/output-style` command deprecated; output style now fixed at session start**: The `/output-style` slash command has been removed from the command reference table. Output style selection has moved to `/config` → **Output style**. Critically, the output style is now applied once at session start and cannot be changed mid-session.
  > Because the output style is set in the system prompt at session start, changes take effect the next time you start a new session. This keeps the system prompt stable throughout a conversation so prompt caching can reduce latency and cost.

  The `outputStyle` field can still be set directly in a settings file:
  ```json
  { "outputStyle": "Explanatory" }
  ```
  - *Implication*: Developers who relied on `/output-style` to switch styles mid-session will need to restart the session instead. The trade-off is improved prompt cache hit rates and lower latency/cost for long sessions.
  - *Source*: [Output styles](https://code.claude.com/docs/en/output-styles.md), [Interactive mode](https://code.claude.com/docs/en/interactive-mode.md)

### Features (v2.1.73 Release)

- **Default Opus model on Bedrock, Vertex AI, and Microsoft Foundry changed to Opus 4.6**: The default was previously Opus 4.1. Administrators who have pinned models via environment variables are unaffected; those relying on defaults will now use Opus 4.6 automatically.
  - *Implication*: Unmanaged deployments on third-party providers will silently upgrade to Opus 4.6 after updating Claude Code. Review existing model pin configurations.

- **SSL error guidance for OAuth and connectivity failures**: Claude Code now surfaces actionable guidance (including `NODE_EXTRA_CA_CERTS`) when login or connectivity checks fail due to SSL certificate errors, which is common behind corporate proxies.

- **`/effort` works while Claude is responding**: The effort level command can now be adjusted mid-response, matching the behavior of `/model`.

- **Up arrow after interrupting Claude**: Now restores the interrupted prompt and rewinds the conversation in a single step rather than requiring separate actions.

### Bug Fixes (v2.1.73)

Notable fixes included in this release:

| Area | Fix |
|------|-----|
| Subagents | Model aliases (`opus`/`sonnet`/`haiku`) were silently downgraded to older versions on Bedrock, Vertex, and Foundry |
| Subagents | Background bash processes spawned by subagents were not cleaned up on agent exit |
| Performance | Freezes and 100% CPU loops triggered by permission prompts for complex bash commands |
| Performance | Deadlock when many skill files changed simultaneously (e.g. `git pull` in a large `.claude/skills/` directory) |
| Sessions | Bash tool output lost when running multiple Claude Code sessions in the same project directory |
| Sessions | `SessionStart` hooks firing twice when resuming via `--resume` or `--continue` |
| Hooks | JSON-output hooks injecting no-op `system-reminder` messages into the model's context on every turn |
| Commands | `/resume` showing the current session in the picker |
| Commands | `/ide` crashing with `onInstall is not defined` when auto-installing the extension |
| Commands | `/loop` not available on Bedrock/Vertex/Foundry and when telemetry was disabled |
| Linux | Sandbox failing to start with "ripgrep (rg) not found" on native builds |
| Linux | Native modules not loading on Amazon Linux 2 and other glibc 2.26 systems |
| Voice | Session corruption when a slow connection overlaps a new recording |
| Remote Control | `"media_type: Field required"` API error when receiving images |
| Windows | `/heapdump` failing with `EEXIST` error when the Desktop folder already exists |
| VS Code | HTTP 400 errors for users behind proxies or on Bedrock/Vertex with Claude 4.5 models |

### Documentation — Output Styles Comparison

- **Added "Output Styles vs. Skills" comparison**: The output-styles page now explicitly documents when to use output styles versus skills.
  > Output styles modify how Claude responds (formatting, tone, structure) and are always active once selected. Skills are task-specific prompts that you invoke with `/skill-name` or that Claude loads automatically when relevant. Use output styles for consistent formatting preferences; use skills for reusable workflows and tasks.
  - *Source*: [Output styles](https://code.claude.com/docs/en/output-styles.md)

### Amazon Bedrock — Inference Profile Mapping

- **New section: "Map each model version to an inference profile"**: The Bedrock page now includes a dedicated example showing how to use `modelOverrides` to expose multiple Opus versions simultaneously, each routed to its own application inference profile ARN.
  > If your organization needs to expose several versions of the same family in the `/model` picker, each routed to its own application inference profile ARN, use the `modelOverrides` setting in your settings file instead.
  - *Implication*: Administrators who previously had to choose a single Opus inference profile can now offer users a choice of Opus 4.1, 4.5, and 4.6, each mapped to a distinct ARN.
  - *Source*: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md)

## Notable Details

- The `interactive-mode.md` diff is large (+62/-63 lines) but the actual content change is small: `/output-style [style]` was removed from the command table, and `/config`'s description was expanded to mention output style management. The rest of the diff is a table column-width reformatting with no semantic change.
- The `output-styles.md` frontmatter description for the `description` field was updated from "Used only in the UI of `/output-style`" to "shown in the `/config` picker" — confirming the deprecation extends to all UI references.
- Star count (76.7k → 76.8k) and open PR count (332 → 336) changed in the changelog page scrape; these are metadata noise from the GitHub page render and carry no documentation significance.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| amazon-bedrock.md | Modified | +18 / -0 | New section: map model versions to Bedrock inference profile ARNs via `modelOverrides` |
| changelog.md | Modified | +29 / -2 | v2.1.73 release notes added |
| interactive-mode.md | Modified | +62 / -63 | `/output-style` removed from command table; `/config` description updated; table reformatted |
| model-config.md | Modified | +26 / -0 | New section: `modelOverrides` setting with full behavior documentation |
| output-styles.md | Modified | +16 / -11 | `/output-style` command replaced by `/config`; session-start locking explained; Skills comparison added |
| settings.md | Modified | +1 / -0 | `modelOverrides` added to settings reference table |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-12*
