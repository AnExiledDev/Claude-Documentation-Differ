# Claude Code Documentation Changes — 2026-02-17

## Summary

This update promotes Claude Sonnet 4.6 as the new default primary model across all Claude Code documentation, replacing Sonnet 4.5 (previously referenced as `claude-sonnet-4-5-20250929`). The most substantive functional addition is a new MCP section documenting how Claude.ai-configured MCP servers are automatically available in Claude Code sessions. A notable account-tier clarification also revises how the `default` model alias resolves for Pro and Team Standard plans.

## Significant Changes

### MCP Integration

- **Claude.ai MCP servers now available in Claude Code**: A new section documents that MCP servers configured in a Claude.ai account are automatically surfaced in Claude Code when the user is logged in with a Claude.ai account.
  > If you've logged into Claude Code with a [Claude.ai](https://claude.ai) account, MCP servers you've added in Claude.ai are automatically available in Claude Code.

  > Add servers at [claude.ai/settings/connectors](https://claude.ai/settings/connectors). On Team and Enterprise plans, only admins can add servers.

  > Claude.ai servers appear in the list with indicators showing they come from Claude.ai.

  - *Implication*: Users on Team/Enterprise plans should be aware that MCP server management is admin-controlled via Claude.ai and those servers propagate into Claude Code sessions automatically. The `/mcp` command within Claude Code now shows both locally configured and Claude.ai-sourced servers in a single list.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

### Model Version Promotion: Sonnet 4.5 → Sonnet 4.6

- **Default primary model updated to `claude-sonnet-4-6`**: All references to the previous default (`claude-sonnet-4-5-20250929`) have been replaced with `claude-sonnet-4-6` across provider integrations (Bedrock, Vertex AI, Microsoft Foundry), CI/CD configuration (GitHub Actions, GitLab CI/CD), CLI examples, settings, hooks, and monitoring docs.
  > `Primary model | global.anthropic.claude-sonnet-4-6` (Amazon Bedrock defaults table)

  > `Primary model | claude-sonnet-4-6` (Google Vertex AI defaults table)

  > `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>` (git commit attribution)

  - *Implication*: Developers using the `sonnet` alias or the documented default model IDs now target Sonnet 4.6. Hardcoded model strings in CI pipelines, settings files, or automation scripts should be reviewed. Note that `claude-haiku-4-5` remains unchanged as the small/fast model across all providers — Haiku is **not** automatically upgraded.
  - *Sources*: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md) · [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai.md) · [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry.md) · [GitHub Actions](https://code.claude.com/docs/en/github-actions.md) · [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd.md) · [CLI Reference](https://code.claude.com/docs/en/cli-reference.md) · [Settings](https://code.claude.com/docs/en/settings.md) · [Monitoring & Usage](https://code.claude.com/docs/en/monitoring-usage.md) · [Hooks](https://code.claude.com/docs/en/hooks.md)

- **Bedrock model ID format simplified**: The guidance note on Bedrock model IDs has been updated to drop references to version suffixes.
  > Previously: "The model ID format for Bedrock includes the region prefix (e.g., `us.anthropic.claude...`) and version suffix."

  > Now: "The model ID format for Bedrock includes a region prefix (for example, `us.anthropic.claude-sonnet-4-6`)."

  - *Implication*: The new `claude-sonnet-4-6` model ID on Bedrock does not require a dated version suffix or `:v1:0` postfix, simplifying configuration. This same simplified format is reflected across GitLab CI/CD examples and the Bedrock defaults table.
  - *Sources*: [GitHub Actions](https://code.claude.com/docs/en/github-actions.md) · [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd.md) · [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md)

### Model Configuration & Account Tiers

- **`default` model alias behavior revised for Pro and Team plans**: The table describing how the `default` alias resolves has been rewritten to distinguish between Team Premium and Team Standard.

  | Plan (before) | Default model |
  |---|---|
  | Max and Teams | Opus 4.6 |
  | Pro | Opus 4.6 |

  | Plan (after) | Default model |
  |---|---|
  | Max and Team Premium | Opus 4.6 |
  | Pro and Team Standard | Sonnet 4.6 |

  - *Implication*: Pro users and Team Standard subscribers will now default to Sonnet 4.6 (not Opus 4.6) when using the `default` model alias. Teams that relied on Opus-level capability by default on these plans should explicitly set the model in their configuration.
  - *Source*: [Model Configuration](https://code.claude.com/docs/en/model-config.md)

## Notable Details

- The `sonnet` model alias entry in `model-config.md` now reads "currently Sonnet 4.6" (was "currently Sonnet 4.5"), confirming the alias tracks the latest Sonnet release.
- The example value for the `model` setting in `settings.md` changed from `"claude-sonnet-4-5-20250929"` to `"claude-sonnet-4-6"` — this serves as the canonical reference for the new simplified model string format.
- The `[1m]` context window example in `model-config.md` is updated: `/model claude-sonnet-4-6[1m]` (was `/model claude-sonnet-4-5-20250929[1m]`). The 1M context window note in `google-vertex-ai.md` is also updated to reference Sonnet 4.6.
- The `SessionStart` hook payload example in `hooks.md` now shows `"model": "claude-sonnet-4-6"`, relevant for teams inspecting hook event data.
- The costs page now references Sonnet 4.6 in its ~$100-200/developer/month estimate.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| mcp.md | Modified | +25 / -0 | New section: Use MCP servers from Claude.ai |
| google-vertex-ai.md | Modified | +7 / -7 | Default primary model updated to `claude-sonnet-4-6`; 1M context note updated |
| amazon-bedrock.md | Modified | +6 / -6 | Default primary model updated to `claude-sonnet-4-6`; model ID format simplified |
| github-actions.md | Modified | +6 / -6 | Model examples updated to `claude-sonnet-4-6`; Bedrock model ID format note simplified |
| model-config.md | Modified | +4 / -4 | `sonnet` alias updated to Sonnet 4.6; `default` tier breakdown revised for Pro/Team Standard |
| monitoring-usage.md | Modified | +4 / -4 | Model identifier examples in metrics attributes updated to `claude-sonnet-4-6` |
| settings.md | Modified | +2 / -2 | `model` setting example and git commit attribution updated to Sonnet 4.6 |
| microsoft-foundry.md | Modified | +1 / -1 | `ANTHROPIC_DEFAULT_SONNET_MODEL` example updated to `claude-sonnet-4-6` |
| cli-reference.md | Modified | +1 / -1 | `--model` flag example updated to `claude-sonnet-4-6` |
| costs.md | Modified | +1 / -1 | Cost estimate reference model updated to Sonnet 4.6 |
| gitlab-ci-cd.md | Modified | +1 / -1 | Bedrock model ID example updated to `claude-sonnet-4-6` |
| hooks.md | Modified | +1 / -1 | `SessionStart` hook payload model example updated to `claude-sonnet-4-6` |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-17*
