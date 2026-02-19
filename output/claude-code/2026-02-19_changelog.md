# Claude Code Documentation Changes — 2026-02-19

## Summary

This update removes `delegate` permission mode from Claude Code across all documentation, simplifies agent team navigation from bidirectional `Shift+Up/Down` to unidirectional `Shift+Down` cycling, and introduces comprehensive model version pinning guidance for Bedrock, Vertex AI, and Foundry deployments. OpenTelemetry monitoring receives several attribute additions and renames, including a new `prompt.id` correlation attribute and `last_assistant_message` field for `Stop` and `SubagentStop` hooks.

---

## Significant Changes

### Agent Teams: Delegate Mode Removed

- **`delegate` permission mode removed from Claude Code**: The `delegate` mode, which restricted agent team leads to coordination-only tools (spawning, messaging, shutting down teammates, and managing tasks), has been removed from the permission modes table and all related documentation.
  > *Previously*: `delegate` — Coordination-only mode for agent team leads. Restricts the lead to team management tools, so all implementation work happens through teammates. Only available when an agent team is active.
  - *Implication*: The `defaultMode: "delegate"` setting and `permissionMode: "delegate"` in sub-agent YAML frontmatter are no longer valid options. The `Shift+Tab` cycle (Normal → Auto-Accept → Plan) no longer includes a Delegate step.
  - *Source*: [Permissions](https://code.claude.com/docs/en/permissions.md), [Sub-agents](https://code.claude.com/docs/en/sub-agents.md), [Agent teams](https://code.claude.com/docs/en/agent-teams.md)

- **Agent team teammate navigation simplified to `Shift+Down` only**: Navigation between teammates changed from `Shift+Up/Down` (bidirectional selection) to `Shift+Down` only, which cycles forward through teammates and wraps back to the lead after the last one.
  > The lead's terminal lists all teammates and what they're working on. Use Shift+Down to cycle through teammates and message them directly. After the last teammate, Shift+Down wraps back to the lead.
  - *Implication*: `Shift+Up` no longer does anything for teammate navigation. Workflows relying on reverse-cycling to a specific teammate must now cycle forward.
  - *Source*: [Agent teams](https://code.claude.com/docs/en/agent-teams.md)

---

### Model Configuration: Version Pinning for Third-Party Providers

- **New dedicated guidance for pinning model versions on Bedrock, Vertex AI, and Foundry**: All three provider setup pages now include an explicit "Pin model versions" step (previously "Model configuration"), with a `<Warning>` block and provider-specific example environment variables. A new consolidated section in `model-config.md` centralizes this guidance.

  > **Warning**: Pin specific model versions for every deployment. If you use model aliases (`sonnet`, `opus`, `haiku`) without pinning, Claude Code may attempt to use a newer model version that isn't available in your Bedrock account, breaking existing users when Anthropic releases updates.

  The three environment variables to set are `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, and `ANTHROPIC_DEFAULT_HAIKU_MODEL`, with provider-specific model ID formats:

  | Provider  | Example |
  | :-------- | :------ |
  | Bedrock   | `us.anthropic.claude-opus-4-6-v1` |
  | Vertex AI | `claude-opus-4-6` |
  | Foundry   | `claude-opus-4-6` |

  - *Implication*: Enterprise teams deploying Claude Code to multiple users via a cloud provider should treat model pinning as a required setup step. Without it, a Claude Code update rolling out a new default model alias can silently break users whose cloud accounts don't yet have that model enabled.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md), [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md), [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai.md), [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry.md), [Third-party integrations](https://code.claude.com/docs/en/third-party-integrations.md)

- **`settings.availableModels` allowlist behavior clarified for third-party providers**: The allowlist filters on model aliases (`opus`, `sonnet`, `haiku`), not on provider-specific model IDs.
  > The `settings.availableModels` allowlist still applies when using third-party providers. Filtering matches on the model alias (`opus`, `sonnet`, `haiku`), not the provider-specific model ID.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

---

### Extended Context: Availability Expanded

- **Sonnet 4.6 added to 1M token context support, subscriber access added**: Previously only Opus 4.6 was documented with 1M context. The updated documentation adds Sonnet 4.6 and expands availability to Pro, Max, Teams, and Enterprise subscribers via the "extra usage" billing mechanism.
  > Opus 4.6 and Sonnet 4.6 support a [1 million token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) for long sessions with large codebases.
  >
  > * **API and pay-as-you-go users**: full access to 1M context
  > * **Pro, Max, Teams, and Enterprise subscribers**: available with extra usage enabled

  Billing detail added: standard rates apply until the session exceeds 200K tokens; beyond 200K, requests are charged at long-context pricing with dedicated rate limits.

  - *Implication*: Subscribers who previously couldn't use 1M context can now enable it via extra usage. The 1M context window is explicitly labeled as "currently in beta."
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

---

### Hooks: `last_assistant_message` Field Added

- **`Stop` and `SubagentStop` hooks now receive the final assistant message directly**: Both hook types include a new `last_assistant_message` field containing the text content of Claude's final response, eliminating the need to parse the transcript JSONL file to access it.

  `SubagentStop`:
  > In addition to the [common input fields], SubagentStop hooks receive `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path`, and `last_assistant_message`. ... The `last_assistant_message` field contains the text content of the subagent's final response, so hooks can access it without parsing the transcript file.

  `Stop`:
  > In addition to the [common input fields], Stop hooks receive `stop_hook_active` and `last_assistant_message`. ... The `last_assistant_message` field contains the text content of Claude's final response, so hooks can access it without parsing the transcript file.

  - *Implication*: Hooks that route, log, or conditionally trigger based on Claude's response output no longer need to read and parse the transcript file. This simplifies hook implementations significantly.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md)

---

### OpenTelemetry Monitoring: Attribute Additions and Renames

Several attribute-level changes to the OTel schema — relevant to teams with existing telemetry pipelines:

- **New `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` environment variable**: Controls metrics temporality (default: `delta`). Set to `cumulative` if your backend expects cumulative metrics.
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **New `user.id` and `user.email` standard attributes**: `user.id` is an anonymous identifier always included. `user.email` is included when authenticated via OAuth.
  > When authenticated via OAuth, `user.email` is included in telemetry attributes. If this is a concern for your organization, work with your telemetry backend to filter or redact this field.
  - *Implication*: Telemetry pipelines may now receive user email addresses for OAuth-authenticated sessions. Organizations with privacy requirements should plan to filter this field.
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **New `prompt.id` event correlation attribute**: A UUID v4 that links all events (user prompt, API requests, tool results) produced while processing a single user prompt.
  > When a user submits a prompt, Claude Code may make multiple API calls and run several tools. The `prompt.id` attribute lets you tie all of those events back to the single prompt that triggered them.
  >
  > `prompt.id` is intentionally excluded from metrics because each prompt generates a unique ID, which would create an ever-growing number of time series. Use it for event-level analysis and audit trails only.
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **`tool` attribute renamed to `tool_name` on edit/write metrics**: The attribute tracking which tool triggered a file edit event (`"Edit"`, `"Write"`, `"NotebookEdit"`) is renamed from `tool` to `tool_name`.
  - *Implication*: Breaking change for metric queries filtering on the `tool` attribute for `claude_code.edit_file_counter` or similar metrics.
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **Tool result event: `decision`/`source` renamed to `decision_type`/`decision_source`**: Attributes on the tool result event are renamed. `decision` → `decision_type`, `source` → `decision_source`. New attributes added: `tool_result_size_bytes`, `mcp_server_scope`.
  - *Implication*: Breaking change for pipelines querying `decision` or `source` on tool result events.
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **Active time counter gains `type` attribute**: Values are `"user"` (keyboard interactions) or `"cli"` (tool execution and AI response generation). Previously, CLI processing time was not separately tracked.
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **New `speed` attribute on API request and API error events**: Indicates whether fast mode was active (`"fast"` or `"normal"`).
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **`"hook"` added as a valid `decision_source` / `source` value**: Tool decision events and tool result events now include `"hook"` as a possible source, alongside `"config"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, and `"user_reject"`.
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **Bash tool `tool_parameters` fields updated**: `sandbox` renamed to `dangerouslyDisableSandbox`. New field `git_commit_id` added (the commit SHA when a `git commit` command succeeds).
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

- **`status_code` on API error events clarified as a string**: Now documented as returning `"undefined"` for non-HTTP errors rather than being absent.
  - *Source*: [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage.md)

---

### Configuration: `spinnerTipsOverride` Setting Added

- **New `spinnerTipsOverride` setting for custom spinner tips**: Enterprise deployments can now replace or augment the built-in loading spinner tips with custom strings (e.g., internal tool reminders or onboarding hints).
  > `spinnerTipsOverride` — Override spinner tips with custom strings. `tips`: array of tip strings. `excludeDefault`: if `true`, only show custom tips; if `false` or absent, custom tips are merged with built-in tips.
  - *Example*: `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

---

## Notable Details

- **Vertex AI region/endpoint notes consolidated**: Two separate `<Note>` blocks (one for regional, one for global endpoint limitations) were merged into a single note for clarity, with no change in actual behavior documented.
- **Vertex AI prompt caching note de-emphasized**: The `<Note>` block about prompt caching on Vertex AI was converted to inline prose and merged with the `/login`/`/logout` disabled note. No behavior change.
- **Bedrock "We recommend" → imperative phrasing**: "We recommend creating a dedicated AWS account" changed to "Create a dedicated AWS account." Same for Vertex AI's GCP project recommendation. Phrasing shift toward prescriptive guidance.
- **Desktop comparison table updated**: The feature comparison table for CLI vs Desktop removes `delegate` from the CLI permission modes list and removes the "Agent teams and `delegate` mode" limitation entry, replacing it with simply "Agent teams."
- **`ANTHROPIC_SMALL_FAST_MODEL` deprecation note remains**: The deprecation notice for `ANTHROPIC_SMALL_FAST_MODEL` in favor of `ANTHROPIC_DEFAULT_HAIKU_MODEL` is unchanged and still present.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| monitoring-usage.md | Modified | +75 / -49 | New `prompt.id` correlation, `user.id`/`user.email` attributes, temporality preference env var, attribute renames, `speed` field on API events |
| model-config.md | Modified | +37 / -7 | New "Pin models for third-party deployments" section; extended context expanded to Sonnet 4.6 and subscribers |
| google-vertex-ai.md | Modified | +23 / -19 | "Model configuration" → "Pin model versions" with Warning; consolidated region/endpoint notes |
| microsoft-foundry.md | Modified | +17 / -4 | New "Pin model versions" section with Warning; setup step clarified |
| interactive-mode.md | Modified | +17 / -17 | Removed delegate mode from Shift+Tab description; reformatted shortcuts table |
| amazon-bedrock.md | Modified | +22 / -8 | "Model configuration" → "Pin model versions" with Warning; pre-setup note on pinning |
| agent-teams.md | Modified | +4 / -12 | Removed "Use delegate mode" section; navigation changed from Shift+Up/Down to Shift+Down only |
| sub-agents.md | Modified | +8 / -9 | `delegate` removed from permissionMode options and table |
| permissions.md | Modified | +7 / -8 | `delegate` mode removed from permission modes table |
| hooks.md | Modified | +6 / -4 | `last_assistant_message` field added to Stop and SubagentStop hook inputs |
| desktop.md | Modified | +3 / -3 | `delegate` removed from permission modes comparison; "Agent teams and delegate mode" limitation simplified |
| third-party-integrations.md | Modified | +4 / -0 | New "Pin model versions for cloud providers" section |
| settings.md | Modified | +1 / -0 | New `spinnerTipsOverride` setting |
| common-workflows.md | Modified | +1 / -1 | Removed delegate mode reference from Shift+Tab cycle description |
| how-claude-code-works.md | Modified | +0 / -1 | Removed delegate mode from Shift+Tab mode list |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-19*
