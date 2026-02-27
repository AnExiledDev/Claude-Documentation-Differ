# Claude Code Documentation Changes — 2026-02-27

## Summary

Two update runs were detected on 2026-02-27. The first run captured 28 modified pages with substantive changes (terminology shifts, new environment variables, plugin marketplace submission). The second run detected a single trivial markup cleanup in `quickstart.md` with no content changes.

---

## Run 1 — Significant Changes

### Terminology

- **"Headless mode" renamed to "Non-interactive mode"**: All references to "headless mode" for running Claude via `-p` in scripts or CI have been replaced with "non-interactive mode." The `headless.md` page itself was already retitled "Run Claude Code programmatically" in a prior update, but this change brings the prose throughout the docs into alignment.
  > Before: `"Once you're effective with one Claude, multiply your output with parallel sessions, headless mode, and fan-out patterns."`
  > After: `"Once you're effective with one Claude, multiply your output with parallel sessions, non-interactive mode, and fan-out patterns."`
  - *Implication*: The `headless.md` note states "The CLI was previously called 'headless mode'" — developers should update any internal documentation or onboarding materials that use the old term.
  - *Source*: [Best Practices](https://code.claude.com/docs/en/best-practices.md), [Run Claude Code programmatically](https://code.claude.com/docs/en/headless.md)

- **CLI terminology updated from "REPL" to "session"**: The CLI reference table description for `claude` changed from "Start interactive REPL" to "Start interactive session", and `claude "query"` from "Start REPL with initial prompt" to "Start interactive session with initial prompt."
  > Before: `| \`claude\` | Start interactive REPL |`
  > After: `| \`claude\` | Start interactive session |`
  - *Implication*: Minor but signals Anthropic is moving away from REPL as the conceptual model toward "sessions" as the primary abstraction.
  - *Source*: [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)

### Configuration

- **New `CLAUDE_CODE_DISABLE_FAST_MODE` environment variable**: Setting `CLAUDE_CODE_DISABLE_FAST_MODE=1` disables fast mode entirely at the environment level. This supplements the existing admin-level controls in the Console and Claude AI admin settings.
  > `"Another option to disable fast mode entirely is to set CLAUDE_CODE_DISABLE_FAST_MODE=1. See Environment variables."`
  - *Implication*: Operators can now disable fast mode without admin UI access — useful for CI environments, LLM gateway setups, or scripted deployments where fast mode behavior is undesirable.
  - *Source*: [fast-mode.md](https://code.claude.com/docs/en/fast-mode.md), [settings.md](https://code.claude.com/docs/en/settings.md)

- **New `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` environment variable documented**: The model configuration page gained explicit documentation for disabling adaptive reasoning on Opus 4.6 and Sonnet 4.6, reverting to the fixed thinking budget controlled by `MAX_THINKING_TOKENS`.
  > `"To disable adaptive reasoning on Opus 4.6 and Sonnet 4.6 and revert to the previous fixed thinking budget, set CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1. When disabled, these models use the fixed budget controlled by MAX_THINKING_TOKENS."`
  - *Implication*: Useful for teams that need cost-predictable or latency-deterministic behavior who want to opt out of the dynamic effort allocation introduced with Opus/Sonnet 4.6.
  - *Source*: [Model Configuration](https://code.claude.com/docs/en/model-config.md)

- **Permissions link corrected in Best Practices**: The "Configure permissions" section linked to `/en/settings` for permission configuration guidance; it now correctly points to `/en/permissions`. Similarly, the sandboxing link was simplified from `/en/sandboxing#sandboxing` to `/en/sandboxing`.
  - *Implication*: Developers following the best practices guide will now land on the dedicated permissions page rather than the general settings page.
  - *Source*: [Best Practices](https://code.claude.com/docs/en/best-practices.md)

### Plugins

- **Official plugin marketplace submission portal added**: A new section "Submit your plugin to the official marketplace" was added to the plugin creation guide, with direct links to the in-app submission forms.
  > `"To submit a plugin to the official Anthropic marketplace, use one of the in-app submission forms: Claude.ai: claude.ai/settings/plugins/submit — Console: platform.claude.com/plugins/submit"`
  - *Implication*: Developers who have built plugins now have a documented, official channel to submit them to Anthropic's curated marketplace, rather than only distributing via self-hosted marketplaces.
  - *Source*: [Create Plugins](https://code.claude.com/docs/en/plugins.md), [Discover and Install Plugins](https://code.claude.com/docs/en/discover-plugins.md)

---

## Run 1 — Notable Details

- **VS Code docs: capitalization and intro text**: The VS Code extension page standardized bullet list items to sentence case throughout ("Click" → "click", "Available" → "available", etc.) and added a brief "Before installing, make sure you have:" intro sentence before the prerequisites list. These are editorial, not functional.

- **Best practices "Related resources" simplified**: The "Related resources" section at the bottom of the best practices page changed from a visual `CardGroup` component to a plain markdown bulleted list. Same links, different presentation.

- **headless.md "Next steps" simplified**: Same pattern as above — the CardGroup of links at the bottom of the programmatic usage page was replaced with a plain bulleted list.

- **Code block syntax annotations widespread**: Across at least 10 pages, bare triple-backtick code fences (` ``` `) were updated to include language and theme annotations (e.g., `` ```text  theme={null} ``, `` ```bash  theme={null} ``, `` ```json  theme={null} ``). This is a rendering/formatting change that affects how code blocks display in the documentation system but has no impact on content.

- **Bold formatting removed from CLAUDE.md description**: In best-practices.md, the phrase "**it can't infer from code alone**" lost its bold emphasis: now "it can't infer from code alone". Minor editorial cleanup.

---

## Run 1 — Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| best-practices.md | Modified | +24/-37 | "Headless mode" → "non-interactive mode"; link fix to /permissions; CardGroup → list; code block formatting |
| headless.md | Modified | +4/-17 | Next steps CardGroup → bulleted list (net line reduction) |
| vs-code.md | Modified | +18/-16 | Capitalization standardization throughout; added prerequisites intro text |
| quickstart.md | Modified | +30/-30 | Content restructuring (equal add/remove) |
| interactive-mode.md | Modified | +11/-11 | Code block formatting standardization |
| sub-agents.md | Modified | +8/-8 | Code block formatting standardization |
| plugins.md | Modified | +8/-1 | New "Submit your plugin to the official marketplace" section |
| agent-teams.md | Modified | +9/-9 | Code block formatting standardization |
| cli-reference.md | Modified | +8/-6 | "REPL" → "session" terminology; added intro sentence; capitalization fixes |
| model-config.md | Modified | +3/-1 | Added `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` env var documentation |
| discover-plugins.md | Modified | +6/-1 | Official marketplace submission forms documented |
| settings.md | Modified | +5/-3 | Added `CLAUDE_CODE_DISABLE_FAST_MODE` to env vars table; minor edits |
| fast-mode.md | Modified | +2/-0 | Added note on `CLAUDE_CODE_DISABLE_FAST_MODE=1` as opt-out option |
| skills.md | Modified | +7/-7 | Code block formatting standardization |
| hooks-guide.md | Modified | +4/-4 | Code block formatting standardization |
| desktop.md | Modified | +2/-0 | Minor additions |
| gitlab-ci-cd.md | Modified | +3/-3 | Minor edits |
| keybindings.md | Modified | +2/-2 | Minor edits |
| plugins-reference.md | Modified | +3/-3 | Minor edits |
| hooks.md | Modified | +1/-1 | Minor edit |
| github-actions.md | Modified | +1/-1 | Minor edit |
| common-workflows.md | Modified | +1/-1 | Minor edit |
| costs.md | Modified | +1/-1 | Minor edit |
| sandboxing.md | Modified | +1/-1 | Minor edit |
| statusline.md | Modified | +1/-1 | Minor edit |
| troubleshooting.md | Modified | +2/-2 | Minor edits |
| claude-code-on-the-web.md | Modified | +1/-1 | Minor edit |

---

## Run 2 — Changes by Page

This run detected a single trivial markup cleanup with no content changes. No new features, commands, or behavior were documented.

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| quickstart.md | Modified | +5/-5 | Deduplicated repeated `theme={null}` attributes on code block fences |

## Run 2 — Notable Details

- **Code block attribute deduplication in quickstart**: Each of the five installation code blocks (macOS/Linux/WSL `bash`, Windows `powershell`, Windows `batch`, Homebrew `bash`, WinGet `powershell`) previously carried `theme={null}` repeated nine times on the opening fence (e.g., `` ```bash theme={null} theme={null} ... ``). These were collapsed to a single occurrence. The actual install commands are unchanged.
  - *Source*: [Quickstart](https://code.claude.com/docs/en/quickstart.md)

---

## Run 3 — Summary

Three substantive areas were updated: a new dedicated Zero Data Retention (ZDR) reference page was added for Claude for Enterprise, hooks gained a new HTTP hook type alongside the existing command, prompt, and agent types, and fast mode received a new admin-controlled per-session opt-in setting. Several existing pages were updated to link to and reflect the new ZDR page.

---

## Run 3 — Significant Changes

### Features

#### HTTP Hooks — New Hook Handler Type

Hooks now support a fourth handler type, `type: "http"`, in addition to the existing `command`, `prompt`, and `agent` types. HTTP hooks POST the same JSON event payload that command hooks receive on stdin directly to a configured URL endpoint.

> Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code's lifecycle.

Key behaviors documented:

- **Fields**: `url` (required) and `headers` (optional key-value pairs with `$VAR_NAME` / `${VAR_NAME}` environment variable interpolation for secrets such as auth tokens).
- **Request**: Claude Code sends the event JSON as the POST body with `Content-Type: application/json`.
- **Response format**: The response body uses the same JSON output schema as command hooks.
- **Error handling differs from command hooks**: non-2xx responses, connection failures, and timeouts are all **non-blocking** — execution continues rather than halting.
- **Blocking requires a 2xx + JSON body**: To block a tool call or deny a permission, the endpoint must return a 2xx response with a JSON body containing `decision: "block"` or `hookSpecificOutput.permissionDecision: "deny"`. Status codes alone cannot signal blocking.
- **Deduplication**: HTTP hooks are deduplicated by URL (command hooks deduplicate by command string).
- **UI limitation**: The `/hooks` interactive menu only supports adding command hooks. HTTP hooks must be configured by editing settings JSON directly.

Example configuration:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/pre-tool-use",
            "timeout": 30,
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            }
          }
        ]
      }
    ]
  }
}
```

> Unlike command hooks, HTTP hooks cannot signal a blocking error through status codes alone. To block a tool call or deny a permission, return a 2xx response with a JSON body containing the appropriate decision fields.

- *Implication*: Teams running hook validation services (policy servers, audit endpoints) can now receive hook events over HTTP without wrapping them in shell scripts. The non-blocking failure mode means a downed endpoint won't halt Claude Code sessions.
- *Source*: [Hooks reference](https://code.claude.com/docs/en/hooks.md)

---

#### Fast Mode — Per-Session Opt-In (`fastModePerSessionOptIn`)

Fast mode historically persists across sessions once enabled by a user. A new admin setting, `fastModePerSessionOptIn`, allows Team and Enterprise administrators to require users to explicitly re-enable fast mode at the start of each session.

> By default, fast mode persists across sessions. Administrators can configure fast mode to reset each session.

When `fastModePerSessionOptIn: true` is set in managed or server-managed settings:
- Each session starts with fast mode **off**, regardless of the user's prior preference.
- Users can still enable fast mode with `/fast` within a session.
- The user's saved preference is preserved; removing the setting restores persistent behavior.

```json
{
  "fastModePerSessionOptIn": true
}
```

> This is useful for controlling costs in organizations where users run multiple concurrent sessions.

- *Implication*: Admins gain a cost-control lever for organizations where users may leave fast mode enabled across many concurrent sessions. The setting is additive — it does not erase user preferences, only overrides persistence.
- *Source*: [Fast mode](https://code.claude.com/docs/en/fast-mode.md), [Settings](https://code.claude.com/docs/en/settings.md)

---

### Data & Compliance

#### New Zero Data Retention (ZDR) Reference Page

A new dedicated page documents Zero Data Retention for Claude Code on Claude for Enterprise, consolidating information previously scattered across `data-usage.md` and `legal-and-compliance.md`.

**Scope**:
- ZDR applies to Claude Code inference on Claude for Enterprise only. AWS Bedrock, Google Vertex AI, and Microsoft Foundry are not covered — those platforms' own policies apply.
- ZDR is **per-organization**: each new organization requires separate enablement by the Anthropic account team.

> ZDR is enabled on a per-organization basis. Each new organization requires ZDR to be enabled separately by your Anthropic account team. ZDR does not automatically apply to new organizations created under the same account.

**What ZDR does not cover** (follows standard retention policies):

| Feature | Notes |
|---|---|
| Chat on claude.ai | Web interface conversations not covered |
| Cowork | Not covered |
| Claude Code Analytics | Collects usage metadata; contribution metrics disabled for ZDR orgs |
| User/seat management | Admin data retained under standard policies |
| Third-party integrations / MCP servers | Not covered |

**Features automatically disabled under ZDR**:

| Feature | Reason |
|---|---|
| Claude Code on the Web | Requires server-side conversation history |
| Remote sessions from Desktop app | Requires persistent session data |
| Feedback submission (`/feedback`) | Sends conversation data to Anthropic |

**Policy violations**: Even with ZDR enabled, Anthropic may retain inputs and outputs for up to 2 years if a session is flagged for a Usage Policy violation.

- *Implication*: The per-organization scope is a significant operational detail for Enterprise customers with multiple organizations — ZDR does not cascade automatically to new orgs.
- *Source*: [Zero data retention](https://code.claude.com/docs/en/zero-data-retention.md)

#### ZDR Description Clarified in `data-usage.md`

The ZDR bullet under commercial data retention was rewritten to reflect that ZDR is now an Enterprise-only, per-organization capability rather than a feature of "appropriately configured API keys."

> **Before**: Zero data retention: Available with appropriately configured API keys - Claude Code will not retain chat transcripts on servers
>
> **After**: [Zero data retention](/en/zero-data-retention): available for Claude Code on Claude for Enterprise. ZDR is enabled on a per-organization basis; each new organization must have ZDR enabled separately by your account team

- *Implication*: Customers previously using ZDR via pay-as-you-go API keys should note this scope change. The new ZDR page documents a migration path: contact your account team to transition to Claude for Enterprise while retaining ZDR coverage.
- *Source*: [Data usage](https://code.claude.com/docs/en/data-usage.md)

#### BAA + ZDR Clarification in `legal-and-compliance.md`

The BAA (Business Associate Agreement) section was updated to note the per-organization ZDR requirement and add a link to the new ZDR page.

> ZDR is enabled on a per-organization basis, so each organization must have ZDR enabled separately to be covered under the BAA.

- *Implication*: Healthcare customers with multiple Enterprise organizations need to verify ZDR is explicitly enabled on each org to maintain BAA coverage.
- *Source*: [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance.md)

---

## Run 3 — New Pages

- **zero-data-retention.md** — Dedicated reference for Zero Data Retention (ZDR) on Claude for Enterprise: scope, coverage gaps, features disabled under ZDR, policy violation retention, and how to request enablement. [View](https://code.claude.com/docs/en/zero-data-retention.md)

---

## Run 3 — Notable Details

- **`analytics.md`**: The warning about contribution metrics unavailability for ZDR organizations updated its link from `/en/data-usage#data-retention` to `/en/zero-data-retention`. No content change.
- **HTTP hook blocking semantics**: The asymmetry between command hooks and HTTP hooks on blocking is notable. A command hook uses exit code 2 to block; an HTTP hook must return 2xx + JSON to block. Non-2xx from HTTP is always non-blocking. This means HTTP hook failures are fail-open by design.
- **Fast mode toggle sentence restructured**: "Fast mode persists across sessions" was split into a qualified statement ("By default, fast mode persists across sessions") followed by a new cross-reference to the per-session opt-in section, rather than being stated as an unconditional fact.

---

## Run 3 — Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| zero-data-retention.md | New | +66 | Full ZDR reference for Claude for Enterprise |
| hooks.md | Modified | +63/-9 | New HTTP hook type with fields, examples, and response handling docs |
| fast-mode.md | Modified | +16/-2 | New `fastModePerSessionOptIn` admin setting and section |
| settings.md | Modified | +1/-0 | Added `fastModePerSessionOptIn` to settings reference table |
| data-usage.md | Modified | +1/-1 | ZDR description updated to Enterprise-only, per-org model |
| legal-and-compliance.md | Modified | +1/-1 | BAA section updated with per-org ZDR note and link |
| analytics.md | Modified | +1/-1 | Updated ZDR link to new dedicated page |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-27*
