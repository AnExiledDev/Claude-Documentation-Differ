# Claude Code Documentation Changes — 2026-05-06

## Summary

The official changelog page received two updates today. A patch release entry for **v2.1.131** was added with two targeted bug fixes: a Windows-only VS Code extension activation failure and a Mantle endpoint authentication regression. Earlier in the day, the **v2.1.129** release entry was added, shipping three new flags/env vars, reverting gateway model discovery to opt-in, restoring the pre-2.1.124 Ctrl+R search scope default, and fixing 17 bugs.

---

## Significant Changes

### v2.1.131 Bug Fixes (May 6, 2026)

- **VS Code extension activation failure on Windows**: The extension failed to activate due to a hardcoded build path in the bundled SDK's `createRequire` polyfill.
  > "Fixed VS Code extension failing to activate on Windows due to a hardcoded build path in the bundled SDK (`createRequire` polyfill bug)"
  - *Implication*: Windows users who experienced silent VS Code extension failures should update to 2.1.131.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Mantle endpoint authentication fix**: Requests to Mantle endpoints were missing the `x-api-key` header, causing authentication failures.
  > "Fixed Mantle endpoint authentication failing with missing `x-api-key` header"
  - *Implication*: Developers using Mantle-backed endpoints who saw auth errors despite valid credentials should update to 2.1.131.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

### New CLI Flags and Environment Variables

- **`--plugin-url <url>` flag**: Loads a plugin `.zip` archive directly from a remote URL for the current session, without requiring a local `--plugin-dir`.
  > `Added --plugin-url <url> flag to fetch a plugin .zip archive from a URL for the current session`
  - *Implication*: Plugin distribution no longer requires local file delivery; useful for CI environments and quick prototyping.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`CLAUDE_CODE_FORCE_SYNC_OUTPUT=1` env var**: Forces synchronized terminal output on terminals where auto-detection fails (e.g. Emacs `eat`).
  > `Added CLAUDE_CODE_FORCE_SYNC_OUTPUT=1 env var to force-enable synchronized output on terminals that auto-detection misses (e.g. Emacs eat)`
  - *Implication*: Developers using non-standard terminal emulators — particularly Emacs users — now have a workaround for garbled/unsynchronized output.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE` env var**: When set on Homebrew or WinGet installations, Claude Code runs the package manager upgrade command in the background and prompts the user to restart.
  > `Added CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE: when set on Homebrew or WinGet installations, Claude Code runs the upgrade command in the background and prompts to restart`
  - *Implication*: Opt-in self-update behavior; teams can enable automatic upgrades via environment variable rather than running manual update commands.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

### Configuration & Plugin Changes

- **Plugin manifest schema change — `themes` and `monitors` move to `experimental`**: These fields should now be declared under `"experimental": { ... }` in plugin manifests. Top-level declarations continue to work but `claude plugin validate` will now emit a warning.
  > `Plugin manifests: themes and monitors should now be declared under "experimental": { ... }. Top-level declarations still work but claude plugin validate will warn`
  - *Implication*: Plugin authors should migrate manifests now to avoid future breakage. The `claude plugin validate` command is the recommended check.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`skillOverrides` setting now functional**: The setting accepts three values — `off` (hides from both model and `/` commands), `user-invocable-only` (hides from model only), and `name-only` (collapses description to name only).
  > `skillOverrides setting now works: off hides from model and /, user-invocable-only hides from model only, name-only collapses description`
  - *Implication*: Admins and advanced users can now reliably control skill visibility in both AI-invocation and manual-invocation contexts. This setting was previously documented but non-functional.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

### Behavior Changes and Reverted Defaults

- **Gateway model discovery reverted to opt-in**: The `/v1/models` gateway discovery feature for the `/model` picker is now opt-in via `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1`. It was automatically enabled in versions 2.1.126–2.1.128.
  > `Gateway /v1/models discovery for the /model picker is now opt-in via CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1 (was automatic in 2.1.126–2.1.128)`
  - *Implication*: Users on those intermediate versions who relied on automatic discovery must now set the env var explicitly to retain the behavior.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Ctrl+R history picker restores pre-2.1.124 default scope**: The Ctrl+R history picker now searches all prompts across all projects by default. Press Ctrl+S to narrow the search to the current project or session.
  > `Ctrl+R history picker now defaults to searching all prompts across all projects, matching pre-2.1.124 behavior. Press Ctrl+S to narrow to the current project or session`
  - *Implication*: This reverts a scope-narrowing regression introduced in 2.1.124. Ctrl+S is the new shortcut for the narrower scope that was previously the default.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Third-party deployments no longer see first-party spinner tips**: Bedrock, Vertex, Foundry, and `ANTHROPIC_BASE_URL` gateway users will no longer see spinner tips that reference Anthropic-owned surfaces.
  > `Third-party deployments (Bedrock, Vertex, Foundry, or ANTHROPIC_BASE_URL gateway) no longer see spinner tips pointing at first-party Anthropic surfaces`
  - *Implication*: Cleaner UX for enterprise deployments that route through non-Anthropic infrastructure.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`claude_code.pull_request.count` OTel metric broadened**: The metric now counts PRs and MRs created via MCP tools in addition to those created via shell commands.
  > `The claude_code.pull_request.count OTel metric now counts PRs/MRs created via MCP tools, not just shell commands`
  - *Implication*: Telemetry dashboards tracking PR creation will now reflect MCP-driven workflows, giving a more complete picture of developer activity.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **Policy refusal messages now include API Request ID**: Error messages shown when a policy refuses a request now include the API Request ID.
  > `Policy refusal error messages now include the API Request ID for easier support debugging`
  - *Implication*: Support cases involving policy refusals can now be traced to a specific API request without log scraping.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

---

### Bug Fixes

Notable fixes in v2.1.129 (17 total):

- **Prompt cache TTL downgrade**: Fixed 1-hour prompt cache TTL being silently downgraded to 5 minutes — a silent correctness issue where callers expecting the longer TTL were not informed of the change.
- **Cache-miss warning false positives**: Fixed spurious cache-miss warnings appearing after `/clear` or compaction when switching `/effort` or `/model`.
- **`Bash(mkdir *)` / `Bash(touch *)` allow rules not honored**: Fixed wildcard allow rules not being applied for in-project paths.
- **`deniedMcpServers` wildcard hostname matching**: Fixed `*://` scheme wildcards failing to match mixed-case hostnames.
- **Agent panel hidden on subagent runs (regression from 2.1.122)**: Fixed the agent panel below the prompt being hidden while subagents were running.
- **`/context` token waste**: Fixed `/context` dumping its ASCII visualization grid into the conversation, wasting ~1.6k tokens per invocation.
- **OAuth refresh race after wake-from-sleep**: Fixed a race condition that could log out all running sessions when the machine woke from sleep.
- **Enterprise settings policy scope**: Fixed server-managed settings policy not applying for enterprise/team users whose stored OAuth credentials lacked the `user:inference` scope.
- **External editor handoff (Ctrl+G)**: Fixed blanking the conversation history above the prompt when handing off to an external editor.
- **400 error display**: Fixed unrecognized 400 API status codes showing raw JSON instead of the underlying error message.
- **`/clear` not resetting terminal tab title**: Fixed after conversation `/clear`, the terminal tab title was not reset.
- **`/branch` success message missing session id**: Fixed the success message omitting the new branch's session id, which is required for `/resume`.
- **`/agents` Library list navigation**: Fixed arrow-key navigation — the highlighted agent now stays visible when the list exceeds the viewport height.
- **VSCode `/clear`**: Fixed `/clear` not clearing conversation context and the displayed transcript in the VS Code extension.
- **Bold headers with emoji**: Fixed bold headers containing keycap/ZWJ/skin-tone emoji losing trailing characters in fullscreen mode.
- **`/rename` session title chip**: Fixed the title chip disappearing while a permission or other dialog was active.
- **WebSocket debug noise**: Fixed a harmless WebSocket warning being logged as an error in `--debug` mode during voice mode.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/claude-code/en/changelog.md` | Modified | +35 / -0 | Added v2.1.131 (2 bug fixes) and v2.1.129 (3 new flags/env vars, 5 behavior changes, 17 bug fixes) release entries |

---

*Generated from Claude Code CLI documentation changes detected on 2026-05-06*
