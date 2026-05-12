# Claude Code Documentation Changes — 2026-05-12

## Summary

Ten documentation pages were updated in this batch. The largest change is fast mode's expansion to support Claude Opus 4.7, with an opt-in env var now and an automatic cutover scheduled for May 14, 2026. Supporting changes land across env vars, monitoring, sandboxing, plugins, and several clarification rewrites.

## Significant Changes

### Fast Mode

- **Fast mode now supports Opus 4.7**: Fast mode previously ran exclusively on Opus 4.6. It now also runs on Opus 4.7, controlled by the new `CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE` environment variable. Opus 4.7 will become the default fast mode model on **May 14, 2026**.
  > On May 14, 2026, Opus 4.7 becomes the default fast mode model. Until then, opt in by setting `CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE=1`.
  - *Implication*: Developers who want to preview the upcoming default can set the env var now. Those who prefer to stay on Opus 4.6 don't need to change anything before May 14.
  - *Source*: [Fast Mode](https://code.claude.com/docs/en/fast-mode.md)

- **Shared rate limit pool for Opus 4.6 and 4.7 fast mode**: Both Opus versions draw from the same fast mode rate limit pool. Pricing is $30/$150 MTok for both.
  > Fast mode for Opus 4.6 and Opus 4.7 share the same rate limit pool: usage on either model draws from the same limits.
  - *Implication*: Switching between Opus 4.6 and 4.7 fast mode does not reset or separate rate limit accounting.
  - *Source*: [Fast Mode](https://code.claude.com/docs/en/fast-mode.md)

- **Rate limit fallback updated**: When fast mode hits its rate limit, it now falls back to "standard speed on the same Opus version" rather than specifically "standard Opus 4.6".
  - *Implication*: The behavior is symmetric whether you're on Opus 4.6 or 4.7 fast mode.
  - *Source*: [Fast Mode](https://code.claude.com/docs/en/fast-mode.md)

### Monitoring / OpenTelemetry

- **New `claude_code.feedback_survey` OTEL event**: A new event type is now logged to your OpenTelemetry collector when a session quality survey appears or is answered. This is the telemetry counterpart to the new `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL` opt-in.
  > **Event Name**: `claude_code.feedback_survey`
  >
  > **Attributes**: ... `event_type`: Survey lifecycle event, for example `"appeared"`, `"responded"`, or `"transcript_prompt_appeared"` ... `enabled_via_override`: `true` when `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL` is set.
  - *Implication*: Organizations that block Anthropic-bound traffic but want to capture survey response data can route it to their own OTEL collector and filter on `enabled_via_override` to confirm the override is applied fleet-wide.
  - *Source*: [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage.md)

### Configuration / System Prompt Flags

- **Expanded guidance on append vs. replace system prompt flags** (`cli-reference.md`): The single-sentence guidance on when to use `--append-system-prompt` vs. `--system-prompt`/`--system-prompt-file` was replaced with a multi-paragraph decision guide that distinguishes coding-assistant use cases from pipeline/non-human-watched agents.
  > Choose based on whether Claude Code's default identity still fits your task. Use an append flag when Claude should remain a coding assistant that also follows your extra rules... Use a replacement flag when the surface, identity, or permission model differs from Claude Code's, like a non-coding agent in a pipeline that no human watches.
  - *Implication*: Developers building scripted pipelines now get clear direction to use replacement flags and accept responsibility for reconstructing tool guidance and safety instructions. The new text also cross-links to output styles, CLAUDE.md, and the Agent SDK guide on system prompts.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

- **`--exclude-dynamic-system-prompt-sections` description updated**: The list of what is moved from the system prompt now says "git-repo flag" instead of "git status".
  - *Implication*: Minor precision improvement — the flag moves the presence/absence indicator for git repos, not full git status output.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

### Output Styles

- **Clarified comparisons between output styles, CLAUDE.md, and `--append-system-prompt`**: Both the "vs. CLAUDE.md / --append-system-prompt" and "vs. Agents" sections were rewritten to lead with a decision rule rather than a mechanics description.
  > Choose based on whether Claude should stop acting as a coding assistant or keep its default role and learn more. Output styles replace the software-engineering parts of Claude Code's system prompt with your own role and voice... CLAUDE.md and `--append-system-prompt` both keep Claude Code's default identity and add to it.
  - *Implication*: The rewrite makes the tradeoffs actionable: output styles for identity changes, CLAUDE.md/`--append-system-prompt` for additive conventions, subagents for scoped delegation.
  - *Source*: [Output Styles](https://code.claude.com/docs/en/output-styles.md)

### Plugins

- **`--plugin-dir` now accepts `.zip` archives** (requires Claude Code v2.1.128+): Previously `--plugin-dir` only accepted a directory path. It now also accepts a `.zip` archive of the plugin directory.
  > The flag also accepts a `.zip` archive of the plugin directory, which requires Claude Code v2.1.128 or later.
  - *Implication*: Plugin authors can distribute and test zipped builds without unpacking first. Useful for CI workflows that produce plugin archives.
  - *Source*: [Plugins](https://code.claude.com/docs/en/plugins.md)

### Sandboxing

- **AppArmor profile instructions added for Ubuntu 24.04+**: Ubuntu 24.04's default AppArmor policy blocks bubblewrap (`bwrap`) from creating user namespaces needed for sandboxing. The docs now include a ready-to-paste AppArmor profile and reload command.
  > On Ubuntu 24.04 and later, the default AppArmor policy prevents bubblewrap from creating the user namespaces it needs for isolation. Add an AppArmor profile that grants `bwrap` this capability.
  - *Implication*: Users on Ubuntu 24.04+ who encounter sandboxing failures now have explicit remediation steps. The profile is scoped to `bwrap` itself and does not affect commands run inside the sandbox.
  - *Source*: [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)

## Minor Changes

- **env-vars.md**: Added two new environment variables — `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL` (routes survey ratings to your OTEL collector when nonessential traffic is blocked) and `CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE` (opts `/fast` into Opus 4.7). Updated `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY` docs to note `DO_NOT_TRACK` also disables surveys. (+3/-1)

- **data-usage.md**: `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` is now listed as a condition that suppresses the transcript-upload follow-up prompt (previously omitted from that list). Added `DO_NOT_TRACK` to the list of vars that disable the feedback survey. Added `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL=1` opt-back-in for organizations using their own OTEL collector. (+2/-2)

- **permissions.md**: `echo`, `pwd`, and `which` added to the built-in read-only command set that never prompts for permission. (+1/-1)

- **routines.md**: Clarified that locally added MCP servers (`claude mcp add`) are machine-local and don't appear in the routines connector list. Guidance added: add them at `claude.ai/customize/connectors` or declare them in a committed `.mcp.json` to use them in a routine. (+2/-0)

## Migration Notes

- **Fast mode default model change on May 14, 2026**: `/fast` will automatically switch to Opus 4.7. If you need to stay on Opus 4.6 fast mode after that date, documentation does not currently describe a pin mechanism — watch for further guidance. To preview Opus 4.7 fast mode today, set `CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE=1`.

## Notable Details

- The `fast-mode.md` description was generalized from "Claude Opus 4.6" to "Claude Opus" throughout, signaling that fast mode is now a model-family feature rather than tied to a specific version.
- `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL` has no effect unless one of the blocking vars (`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, `DISABLE_TELEMETRY`, or `DO_NOT_TRACK`) is already set — it is an opt-back-in within a blocked configuration, not a standalone routing flag.
- The `enabled_via_override` OTEL attribute on `feedback_survey` events is emitted as a **boolean**, not a string — a detail that matters for OTEL filter expressions.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| fast-mode.md | Modified | SIGNIFICANT | +44/-10 | Fast mode expanded to Opus 4.7; new opt-in env var; May 14 cutover date |
| sandboxing.md | Modified | SIGNIFICANT | +20/-0 | AppArmor profile instructions for Ubuntu 24.04+ bubblewrap fix |
| output-styles.md | Modified | SIGNIFICANT | +18/-9 | Rewrote comparison sections to lead with decision guidance |
| monitoring-usage.md | Modified | SIGNIFICANT | +18/-0 | New `claude_code.feedback_survey` OTEL event documented |
| cli-reference.md | Modified | SIGNIFICANT | +4/-2 | Expanded system prompt flag guidance; `--exclude-dynamic-system-prompt-sections` wording fix |
| plugins.md | Modified | SIGNIFICANT | +6/-0 | `--plugin-dir` now accepts `.zip` archives (v2.1.128+) |
| env-vars.md | Modified | MINOR | +3/-1 | Two new env vars; `DO_NOT_TRACK` added to survey disable list |
| data-usage.md | Modified | MINOR | +2/-2 | Survey suppression conditions updated; OTEL opt-back-in documented |
| routines.md | Modified | MINOR | +2/-0 | Clarified local MCP servers vs. connectors for routines |
| permissions.md | Modified | MINOR | +1/-1 | `echo`, `pwd`, `which` added to read-only command set |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-12*
