# Claude Code Documentation Changes — 2026-04-11

## Summary

Version 2.1.101 (April 10, 2026) shipped with 35+ changelog entries covering new commands, security fixes, session-handling improvements, and numerous bug fixes. Alongside the release, documentation was updated to reflect OS CA certificate store integration for enterprise TLS proxies, revised cost estimates for enterprise deployments, a clarified MCP server scope hierarchy, and expanded PowerShell parity across several tool-behavior pages.

## Significant Changes

### Features & New Commands (v2.1.101)

- **`/team-onboarding` command**: New bundled command that generates a teammate ramp-up guide from your local Claude Code usage history.
  > `Added /team-onboarding command to generate a teammate ramp-up guide from your local Claude Code usage`
  - *Implication*: Teams can automate onboarding documentation without manual effort.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **OS CA certificate store trusted by default**: Enterprise TLS-inspection proxies (CrowdStrike Falcon, Zscaler) now work without additional setup when their root certificate is installed in the OS trust store.
  > `Added OS CA certificate store trust by default, so enterprise TLS proxies work without extra setup (set CLAUDE_CODE_CERT_STORE=bundled to use only bundled CAs)`
  - *Implication*: Eliminates the need to set `NODE_EXTRA_CA_CERTS` in most enterprise environments. Opt out with `CLAUDE_CODE_CERT_STORE=bundled`.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`/ultraplan` and remote sessions auto-create cloud environment**: Previously required web setup before remote-session commands would function.
  > `/ultraplan and other remote-session features now auto-create a default cloud environment instead of requiring web setup first`
  - *Implication*: Removes a manual prerequisite step for remote/cloud-based sessions.
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

- **`claude -p --resume <name>` accepts session titles**: The `--resume` flag now accepts the session titles set via `/rename` or `--name`, not just session IDs.
  > `Improved claude -p --resume <name> to accept session titles set via /rename or --name`
  - *Source*: [Changelog](https://code.claude.com/docs/en/changelog.md)

### Network Configuration

- **New `CLAUDE_CODE_CERT_STORE` environment variable**: Controls which CA certificate sources Claude Code uses for TLS. Accepts a comma-separated list of `bundled` (Mozilla CA set shipped with Claude Code) and `system` (OS trust store). Default is `bundled,system`.
  > `CLAUDE_CODE_CERT_STORE` accepts a comma-separated list of sources. Recognized values are `bundled` for the Mozilla CA set shipped with Claude Code and `system` for the operating system trust store. The default is `bundled,system`.
  >
  > `CLAUDE_CODE_CERT_STORE has no dedicated settings.json schema key. Set it via the env block in ~/.claude/settings.json or directly in the process environment.`
  - *Implication*: Operators can now restrict Claude Code to only the bundled Mozilla CAs (`bundled`) or only the OS store (`system`), or combine both. Requires the native binary distribution — the Node.js runtime ignores this variable.
  - *Source*: [Network Configuration](https://code.claude.com/docs/en/network-config.md), [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

### Cost Estimates Updated

- **Revised enterprise cost benchmarks**: The per-developer cost figures were updated upward to reflect broader enterprise deployment data.

  | Metric | Old estimate | New estimate |
  |--------|-------------|-------------|
  | Average per active day | ~$6 | ~$13 |
  | 90th-percentile per active day | <$12 | <$30 |
  | Monthly per developer | ~$100–200 | ~$150–250 |

  > `Across enterprise deployments, the average cost is around $13 per developer per active day and $150-250 per developer per month, with costs remaining below $30 per active day for 90% of users.`
  - *Implication*: Teams sizing budgets should revise upward. The docs now recommend running a small pilot group to establish a baseline before broader rollout.
  - *Source*: [Costs](https://code.claude.com/docs/en/costs.md)

### MCP Server Scope Hierarchy

- **Explicit 5-level scope hierarchy documented**: The MCP precedence rules were rewritten from prose into a numbered list and expanded to explicitly include plugin-provided servers and claude.ai connectors.

  > When the same server is defined in more than one place, Claude Code connects to it once, using the definition from the highest-precedence source:
  > 1. Local scope
  > 2. Project scope
  > 3. User scope
  > 4. Plugin-provided servers
  > 5. claude.ai connectors
  >
  > The three scopes match duplicates by name. Plugins and connectors match by endpoint, so one that points at the same URL or command as a server above is treated as a duplicate.

  - *Implication*: Plugin-provided MCP servers can now be overridden by any local/project/user-scope server with the same endpoint, not just the same name. This is a meaningful behavioral clarification for plugin authors.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

### Hooks: `allowManagedHooksOnly` Exemption for Force-Enabled Plugins

- **Plugins force-enabled via `enabledPlugins` in managed settings are now exempt from `allowManagedHooksOnly`**: Previously, the setting blocked *all* plugin hooks when enabled. Now, hooks from plugins explicitly listed in managed settings `enabledPlugins` are allowed through.
  > `Hooks from plugins force-enabled in managed settings enabledPlugins are exempt, so administrators can distribute vetted hooks through an organization marketplace.`
  >
  > `Trust is granted by full plugin@marketplace ID, so a plugin with the same name from a different marketplace stays blocked`
  - *Implication*: Enterprise admins can now use `allowManagedHooksOnly` to lock down user-defined hooks while still distributing approved hooks via a managed plugin marketplace. The trust anchor is the full `plugin@marketplace` identifier, not just the plugin name.
  - *Source*: [Hooks](https://code.claude.com/docs/en/hooks.md), [Settings](https://code.claude.com/docs/en/settings.md), [Permissions](https://code.claude.com/docs/en/permissions.md)

### Sub-agent Working Directory Behavior

- **Working directory semantics for subagents explicitly documented**: Subagents start in the main conversation's CWD. `cd` commands inside a subagent do not persist between Bash or PowerShell tool calls, and do not affect the main conversation's working directory.
  > `A subagent starts in the main conversation's current working directory. Within a subagent, cd commands do not persist between Bash or PowerShell tool calls and do not affect the main conversation's working directory. To give the subagent an isolated copy of the repository instead, set isolation: worktree.`
  - *Implication*: Subagent scripts that rely on `cd` to change directories must use absolute paths or chain commands. The `isolation: worktree` frontmatter field is the correct way to give a subagent a separate working tree.
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

### Bash & PowerShell Tool Parity

- **Bash working-directory carry-over scoped to main session only**: The docs now explicitly state that working directory changes from `cd` only carry over in the *main* session; subagents never inherit them.
  > `When Claude runs cd in the main session, the new working directory carries over to later Bash commands... Subagent sessions never carry over working directory changes.`
  - *Source*: [Tools Reference](https://code.claude.com/docs/en/tools-reference.md)

- **PowerShell tool shares Bash working-directory reset rules**: The same `cd`-reset behavior (and `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR`) now explicitly applies to PowerShell commands, not just Bash.
  > `The same main-session working-directory reset behavior described under the Bash tool section applies to PowerShell commands, including the CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR environment variable.`
  - *Source*: [Tools Reference](https://code.claude.com/docs/en/tools-reference.md)

- **PowerShell subprocesses inherit `TRACEPARENT`**: The distributed tracing context variable is now passed to both Bash and PowerShell subprocesses (previously documented as Bash-only).
  > `When tracing is active, Bash and PowerShell subprocesses automatically inherit a TRACEPARENT environment variable...`
  - *Source*: [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage.md)

### Bedrock Mantle: `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` Clarification

- **`ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` now explicitly covers Bedrock Mantle**: The env-vars table and the Bedrock Mantle variable reference table both updated to reflect that this region override applies to both standard Bedrock and the Mantle endpoint.
  > `Override AWS region for the Haiku-class model when using Bedrock or Bedrock Mantle`

  The Mantle-specific variables table gained a new row:

  | Variable | Purpose |
  |----------|---------|
  | `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | Override AWS region for the Haiku-class model (shared with Bedrock) |

  - *Source*: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md), [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

### Scheduled Tasks

- **Dynamic `/loop` may use the Monitor tool directly**: A new note explains that when Claude determines a dynamic loop schedule, it may invoke the Monitor tool instead of re-running a prompt on an interval.
  > `When you ask for a dynamic /loop schedule, Claude may use the Monitor tool directly. Monitor runs a background script and streams each output line back, which avoids polling altogether and is often more token-efficient and responsive than re-running a prompt on an interval.`
  - *Implication*: Users relying on `/loop` for CI monitoring may get a different (more efficient) execution path than expected; the task will still appear in the scheduled task list.
  - *Source*: [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks.md)

## Notable Details

- **`CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` description updated**: Now reads "in the main session" and explicitly mentions PowerShell, aligning with the tool-reference docs.
- **`/claude-api` command description updated**: "Managed Agents reference" was separated out as its own description element, clarifying that Managed Agents docs are a distinct reference area from the core API languages. ([Commands](https://code.claude.com/docs/en/commands.md))
- **Settings resilience**: An unrecognized hook event name in `settings.json` no longer causes the *entire file* to be ignored — only the bad entry is skipped. Relevant for teams who may have stale or typo'd hook event names in config.
- **A command injection vulnerability in the POSIX `which` fallback used by LSP binary detection was fixed** in v2.1.101. No configuration changes required.
- **Memory docs**: The "Manage sessions" link was removed from the See Also section of `memory.md` — minor navigation cleanup.
- **Contact Sales CTA**: An A/B-tested `ContactSalesCard` component was injected into the top of `amazon-bedrock.md`, `google-vertex-ai.md`, `microsoft-foundry.md`, and `third-party-integrations.md`. This is a rendered UI element on the docs site and has no functional impact on the CLI.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| amazon-bedrock.md | Modified | +188/-6 | ContactSalesCard UI component added; `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` added to Mantle variable table |
| changelog.md | Modified | +49/-0 | v2.1.101 release notes added (35+ entries) |
| google-vertex-ai.md | Modified | +180/-0 | ContactSalesCard UI component added |
| microsoft-foundry.md | Modified | +180/-0 | ContactSalesCard UI component added |
| third-party-integrations.md | Modified | +180/-0 | ContactSalesCard UI component added |
| network-config.md | Modified | +27/-1 | New "CA certificate store" section; `CLAUDE_CODE_CERT_STORE` documented |
| mcp.md | Modified | +8/-2 | Scope hierarchy expanded to 5 levels with plugin/connector dedup rules |
| settings.md | Modified | +3/-2 | `allowManagedHooksOnly` description updated to reflect plugin exemption |
| hooks.md | Modified | +1/-1 | `allowManagedHooksOnly` exemption for force-enabled plugin hooks documented |
| permissions.md | Modified | +1/-1 | `allowManagedHooksOnly` description updated |
| env-vars.md | Modified | +3/-2 | `CLAUDE_CODE_CERT_STORE` added; `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` and `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` descriptions updated |
| tools-reference.md | Modified | +3/-1 | Bash `cd` scoped to main session; PowerShell shares same rules |
| sub-agents.md | Modified | +2/-0 | Working directory behavior for subagents documented |
| scheduled-tasks.md | Modified | +2/-0 | Note about Monitor tool use in dynamic `/loop` |
| costs.md | Modified | +3/-3 | Cost estimates revised upward; pilot group recommendation moved |
| monitoring-usage.md | Modified | +1/-1 | PowerShell added to TRACEPARENT inheritance |
| commands.md | Modified | +1/-1 | `/claude-api` description updated |
| statusline.md | Modified | +1/-1 | Notifications description clarified |
| memory.md | Modified | +0/-1 | "Manage sessions" link removed from See Also |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-11*
