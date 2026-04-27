# Claude Code Documentation Changes — 2026-04-27

## Summary

The development containers page (`devcontainer.md`) was substantially rewritten (+160/-49 lines), replacing a single reference-container walkthrough with a modular, task-oriented guide built around the new **Claude Code Dev Container Feature**. Three other pages received a minor terminology normalization ("devcontainers" → "dev containers"), and `network-config.md` gained a small callout about optional telemetry.

---

## Significant Changes

### Dev Container Documentation Overhaul

- **New Dev Container Feature for one-line installation**: The page now centers on the official `ghcr.io/anthropics/devcontainer-features/claude-code:1.0` feature, replacing the previous approach of cloning the reference repository as a starting point. Any project can now add Claude Code to an existing `devcontainer.json` without taking on the full reference container.

  > ```json
  > "features": {
  >   "ghcr.io/anthropics/devcontainer-features/claude-code:1.0": {}
  > }
  > ```

  - *Implication*: Teams can integrate Claude Code into their own dev containers in one block rather than adapting a full reference implementation.
  - *Source*: [Development containers](https://code.claude.com/docs/en/devcontainer.md)

- **Persist authentication across rebuilds via named volume**: The guide now explicitly documents mounting a named volume at `~/.claude` to avoid re-authentication on every container rebuild. Introduces the `CLAUDE_CONFIG_DIR` env var as the override if the volume is mounted elsewhere.

  > ```json
  > "mounts": [
  >   "source=claude-code-config,target=/home/node/.claude,type=volume"
  > ]
  > ```
  > To isolate state per project rather than sharing one volume across all repositories, include the `${devcontainerId}` variable in the source name.

  - *Implication*: Developers working in Codespaces or frequently rebuilding containers no longer need to re-authenticate each time.
  - *Source*: [Development containers](https://code.claude.com/docs/en/devcontainer.md)

- **Organization policy via `/etc/claude-code/managed-settings.json`**: A new "Enforce organization policy" section documents the Linux system-level managed settings path inside containers, with a Dockerfile snippet to install it. Links to server-managed settings for policies that must survive repository edits.

  > Claude Code reads `/etc/claude-code/managed-settings.json` on Linux and applies it at the highest precedence in the settings hierarchy, so values there override anything an engineer sets in `~/.claude` or the project's `.claude/` directory.

  - *Implication*: Organizations can ship policy with their container image, though the document is clear this is bypassed by anyone with repo write access — server-managed settings are recommended for stronger enforcement.
  - *Source*: [Development containers](https://code.claude.com/docs/en/devcontainer.md)

- **Disabling auto-update and telemetry via `containerEnv`**: The policy section documents `DISABLE_AUTOUPDATER` and `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` as `containerEnv` entries for reproducible and privacy-controlled builds.

  > ```json
  > "containerEnv": {
  >   "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
  >   "DISABLE_AUTOUPDATER": "1"
  > }
  > ```

  - *Implication*: CI and locked-down enterprise environments can pin behavior without modifying Claude Code's own config files.
  - *Source*: [Development containers](https://code.claude.com/docs/en/devcontainer.md)

- **`--dangerously-skip-permissions` guidance tightened**: The warning around running without permission prompts now explicitly calls out that the flag is rejected when Claude Code runs as root, that workspace file edits still appear on the host, and recommends pairing the flag with network egress restrictions. Also surfaces `auto` mode as an alternative for reducing prompts without disabling safety checks, and the `permissions.disableBypassPermissionsMode` managed setting to block the flag entirely.

  > Skipping permission prompts removes your opportunity to review tool calls before they run. Claude can still modify any file in the bind-mounted workspace, which appears directly on your host, and reach anything the container's network policy allows.

  - *Implication*: More nuanced guidance clarifies that container isolation does not eliminate all risk from `--dangerously-skip-permissions`.
  - *Source*: [Development containers](https://code.claude.com/docs/en/devcontainer.md)

- **Updated security warning: avoid mounting host secrets**: The top-level warning now adds an explicit recommendation not to mount `~/.ssh` or cloud credential files into the container, preferring repository-scoped or short-lived tokens.

  > Avoid mounting host secrets such as `~/.ssh` or cloud credential files into the container; prefer repository-scoped or short-lived tokens.

  - *Implication*: Directly addresses a common misconfiguration risk when using `--dangerously-skip-permissions`.
  - *Source*: [Development containers](https://code.claude.com/docs/en/devcontainer.md)

- **GitHub Codespaces auth persistence via secrets**: The rebuild persistence section now explains that `ANTHROPIC_API_KEY` or a `CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token` can be stored as a Codespaces secret to carry authentication across codespace rebuilds.

  > To carry authentication across codespaces, store `ANTHROPIC_API_KEY` or a `CLAUDE_CODE_OAUTH_TOKEN` from [`claude setup-token`](/en/authentication#generate-a-long-lived-token) as a Codespaces secret.

  - *Implication*: Codespaces users get a concrete, rebuild-safe auth strategy without manual re-sign-in.
  - *Source*: [Development containers](https://code.claude.com/docs/en/devcontainer.md)

- **Architecture diagram added**: A new collapsible accordion ("How dev containers work with your editor") includes a diagram showing the relationship between the host editor, Docker container, and workspace bind mount. Clarifies that editors without dev container support (e.g., plain Vim) are out of scope for this workflow.

  - *Source*: [Development containers](https://code.claude.com/docs/en/devcontainer.md)

### Network Configuration

- **Telemetry callout added to allowlist section**: A new sentence after the npm/binary distribution note directs readers to the telemetry opt-out docs before they finalize their proxy allowlist.

  > Claude Code also sends optional operational telemetry by default, which you can disable with environment variables. See [Telemetry services](/en/data-usage#telemetry-services) for how to disable it before finalizing your allowlist.

  - *Implication*: Admins building allowlists are now prompted to consider telemetry domains, reducing the chance of unexpected traffic from deployed containers.
  - *Source*: [Network configuration](https://code.claude.com/docs/en/network-config.md)

---

## Notable Details

- **"devcontainers" → "dev containers" terminology normalization**: Three pages (`permission-modes.md`, `sandboxing.md`, `security.md`) each had a single word changed from "devcontainers" to "dev containers", consistent with the rewritten devcontainer page and the Dev Containers spec's own capitalization style.

- **Reference container demoted from primary path to example**: The old guide led with the reference implementation as the getting-started path. The new page inverts this: the Dev Container Feature is now primary, and the reference container is a named "Try the reference container" section described as "a working example rather than a maintained base image."

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| devcontainer.md | Modified | +160 / -49 | Full rewrite: modular task-oriented guide, Dev Container Feature, persistence, policy, egress, and prompts |
| network-config.md | Modified | +2 / -0 | Added telemetry opt-out note before allowlist finalization |
| permission-modes.md | Modified | +1 / -1 | Terminology: "devcontainers" → "dev containers" |
| sandboxing.md | Modified | +1 / -1 | Terminology: "devcontainers" → "dev containers" |
| security.md | Modified | +1 / -1 | Terminology: "devcontainers" → "dev containers" |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-27*
