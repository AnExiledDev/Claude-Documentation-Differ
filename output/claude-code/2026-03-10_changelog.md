# Claude Code Documentation Changes — 2026-03-10

## Summary

A new **Code Review** managed service (research preview) has been added for Teams and Enterprise subscribers, enabling automatic multi-agent PR reviews posted as inline GitHub comments. Alongside this, the built-in `/review` slash command is deprecated in favor of a dedicated plugin, and `/review` has been replaced as the canonical example throughout skills, plugins, and marketplace documentation.

---

## Significant Changes

### New Feature: GitHub Code Review (Managed Service)

- **Automatic PR reviews via multi-agent analysis**: A new hosted Code Review service runs automatically when a pull request opens or updates on GitHub. A fleet of specialized agents analyze the diff against the full codebase in parallel on Anthropic infrastructure, then deduplicate and rank findings before posting them as inline PR comments.

  > "A fleet of specialized agents examine the code changes in the context of your full codebase, looking for logic errors, security vulnerabilities, broken edge cases, and subtle regressions."

  - *Implication*: No manual trigger required — reviews run without a `@claude` mention or CI workflow change. This is distinct from GitHub Actions, which requires explicit invocation.
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

- **Severity tagging system**: Findings are classified into three severity levels:

  | Marker | Severity     | Meaning                                                             |
  |--------|--------------|---------------------------------------------------------------------|
  | 🔴     | Normal       | A bug that should be fixed before merging                           |
  | 🟡     | Nit          | A minor issue, worth fixing but not blocking                        |
  | 🟣     | Pre-existing | A bug that exists in the codebase but was not introduced by this PR |

  - *Implication*: Reviews are non-blocking by design — findings don't approve or reject PRs, preserving existing review workflows.
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

- **`REVIEW.md` — new repo-level configuration file**: A new `REVIEW.md` file (placed at repository root) lets teams encode review-specific rules without polluting the general `CLAUDE.md`. It supports "always check", "style", and "skip" sections.

  > "`REVIEW.md`: review-only guidance, read exclusively during code reviews. Use it for rules that are strictly about what to flag or skip during review and would clutter your general `CLAUDE.md`."

  - *Implication*: Teams can now separate project-wide Claude instructions (`CLAUDE.md`) from code-review-specific policies (`REVIEW.md`). Claude auto-discovers `REVIEW.md` at the repo root with no configuration needed.
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

- **Availability and pricing**: Code Review is in **research preview**, available only to **Teams and Enterprise** subscribers. Not available to organizations with Zero Data Retention enabled. Reviews are billed by token usage, averaging **$15–25 per review**.

  > "Reviews scale in cost with PR size and complexity, completing in 20 minutes on average."

  - *Implication*: The "after every push" trigger mode multiplies costs by the number of pushes per PR. Admins can set monthly spend caps at `claude.ai/admin-settings/usage`. A per-repo cost column is visible in admin settings.
  - *Source*: [Code Review](https://code.claude.com/docs/en/code-review.md)

---

### Deprecation: Built-in `/review` Slash Command

- **`/review` command deprecated**: The built-in `/review` interactive-mode command is now marked deprecated. Users are directed to install the `code-review` plugin from the marketplace instead.

  > "`/review` — Deprecated. Install the [`code-review` plugin](https://github.com/anthropics/claude-code-marketplace/blob/main/code-review/README.md) instead: `claude plugin install code-review@claude-code-marketplace`"

  - *Implication*: Existing workflows using `/review` in interactive sessions will need to migrate to the plugin. The managed Code Review service (above) handles automated PR-level reviews; the plugin handles on-demand local reviews before pushing.
  - *Source*: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode.md)

---

### GitHub Actions: Cross-Reference and Prompt Updates

- **Link to Code Review added**: The GitHub Actions page intro now references the new managed Code Review service for teams that want reviews without a manual trigger.

  > "For automatic reviews posted on every PR without a trigger, see [GitHub Code Review](/en/code-review)."

  - *Source*: [GitHub Actions](https://code.claude.com/docs/en/github-actions.md)

- **PR review example prompt updated**: The Actions workflow example for automated PR reviews no longer uses the `/review` skill shorthand. It now uses an explicit plain-text prompt:

  > `prompt: "Review this pull request for code quality, correctness, and security. Analyze the diff, then post your findings as review comments."`

  - *Implication*: This reflects the deprecation of `/review` as a built-in command and encourages explicit prompt instructions in CI workflows.
  - *Source*: [GitHub Actions](https://code.claude.com/docs/en/github-actions.md)

- **"Commands" renamed to "Skills" in Action v1 key features**: The feature list entry previously called "Commands" (with examples `/review` or `/fix`) is now called "Skills", pointing to the skills documentation.

  > "**Skills** — Invoke installed [skills](/en/skills) directly from the prompt"

  - *Source*: [GitHub Actions](https://code.claude.com/docs/en/github-actions.md)

- **`prompt` parameter description clarified**: The Action v1 parameter table now describes `prompt` as accepting "plain text or a [skill](/en/skills) name" rather than "text or skill like `/review`".
  - *Source*: [GitHub Actions](https://code.claude.com/docs/en/github-actions.md)

---

### Documentation-Wide: `/review` Example Replacement

Following the deprecation of `/review`, all documentation examples that used `/review` as a canonical skill name have been updated to avoid confusion:

| Page | Old example | New example |
|------|------------|-------------|
| `features-overview.md` | `/review` runs your code review checklist | `/deploy` runs your deployment checklist |
| `features-overview.md` | `/review` skill (Skill + Subagent pattern) | `/audit` skill |
| `plugin-marketplaces.md` | `review-plugin` / `/review` skill walkthrough | `quality-review-plugin` / `/quality-review` skill |
| `plugins.md` | short skill name like `/review` | short skill name like `/deploy` |
| `skills.md` | `commands/review.md` / `/review` example | `commands/deploy.md` / `/deploy` example |

- *Implication*: These are example-only changes with no behavioral impact, but they signal that `/review` is no longer the idiomatic built-in example going forward.

---

### Overview Page: New Navigation Entry

- **Code Review added to "Where to use Claude Code" table**: The overview page now includes a row directing users to the managed Code Review service.

  > "Get automatic code review on every PR → [GitHub Code Review](/en/code-review)"

  - *Source*: [Overview](https://code.claude.com/docs/en/overview.md)

---

## New Pages

- **[code-review.md](https://code.claude.com/docs/en/code-review.md)** — Full documentation for the new managed GitHub Code Review service: how it works, admin setup (GitHub App installation, per-repo trigger configuration), `CLAUDE.md`/`REVIEW.md` customization, usage analytics, and pricing.

---

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `code-review.md` | New | +168 | Full documentation for managed GitHub Code Review service |
| `github-actions.md` | Modified | +13/-16 | Cross-reference to Code Review; prompt example and "Commands→Skills" rename |
| `features-overview.md` | Modified | +14/-14 | Example skill names updated from `/review` to `/deploy`/`/audit` |
| `plugin-marketplaces.md` | Modified | +12/-12 | Walkthrough example renamed from `review-plugin` to `quality-review-plugin` |
| `overview.md` | Modified | +1/-0 | New "Get automatic code review on every PR" navigation row |
| `interactive-mode.md` | Modified | +1/-1 | `/review` command marked deprecated, plugin install instructions added |
| `plugins.md` | Modified | +1/-1 | Example short skill name changed from `/review` to `/deploy` |
| `skills.md` | Modified | +1/-1 | Example changed from `review.md`/`/review` to `deploy.md`/`/deploy` |
| `changelog.md` | Modified | +1/-1 | Pull request counter incremented (292→294) |

---

*Generated from Claude Code CLI documentation changes detected on 2026-03-10*
