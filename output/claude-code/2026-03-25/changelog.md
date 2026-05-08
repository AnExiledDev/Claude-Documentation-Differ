# Claude Code Documentation Changes — 2026-03-25

## Summary

One documentation page was modified: `model-config.md`, specifically the "Adjust effort level" section. The changes clarify how `max` effort persists (only via env var), expand the default effort scope to cover Sonnet 4.6 and all providers (Bedrock, Vertex, API), add guidance on when to use higher effort levels, and document a new `ultrathink` prompt keyword for per-turn deep reasoning.

## Significant Changes

### Model Configuration — Effort Level

- **`max` effort persistence now requires `CLAUDE_CODE_EFFORT_LEVEL` env var**: The previous docs stated `max` "applies to the current session without persisting." The new wording clarifies it "does not persist across sessions **except through the `CLAUDE_CODE_EFFORT_LEVEL` environment variable**."
  > `max` is available on Opus 4.6 only and does not persist across sessions except through the `CLAUDE_CODE_EFFORT_LEVEL` environment variable.
  - *Implication*: To keep `max` effort across restarts, set `CLAUDE_CODE_EFFORT_LEVEL=max`. Using `/effort max` alone will not survive a session restart.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

- **Default effort expanded to Sonnet 4.6 and all providers**: The prior text only noted "Opus 4.6 defaults to medium effort for Max and Team subscribers." This has been replaced with a broader statement that covers both Sonnet 4.6 and Opus 4.6, and explicitly includes Bedrock, Vertex AI, and direct API access.
  > Opus 4.6 and Sonnet 4.6 default to medium effort. This applies to all providers, including Bedrock, Vertex AI, and direct API access.
  - *Implication*: Sonnet 4.6 users on third-party providers should now expect medium effort as the default — this was previously undocumented and may reflect a recent behavior change.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

- **New guidance: reserve `high`/`max` for genuinely complex tasks**: New documentation explicitly discourages setting high effort globally, noting that the model can overthink routine coding work at elevated effort levels.
  > Medium is the recommended level for most coding tasks: it balances speed and reasoning depth, and higher levels can cause the model to overthink routine work. Reserve `high` or `max` for tasks that genuinely benefit from deeper reasoning, such as hard debugging problems or complex architectural decisions.
  - *Implication*: Developers who have globally set `high` effort should reconsider — medium is now the documented best practice for everyday use.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

- **New `ultrathink` prompt keyword for single-turn high effort**: Including the word `ultrathink` in a prompt triggers high effort for that turn only, without changing the session's persistent effort level.
  > For one-off deep reasoning without changing your session setting, include "ultrathink" in your prompt to trigger high effort for that turn.
  - *Implication*: Provides a lightweight, inline mechanism to escalate reasoning depth on a per-prompt basis — useful for occasional complex tasks without touching effort configuration.
  - *Source*: [Model configuration](https://code.claude.com/docs/en/model-config.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/claude-code/en/model-config.md` | Modified | +7 / -1 | Effort level section: `max` persistence via env var, Sonnet 4.6 default expanded to all providers, medium-effort guidance added, `ultrathink` keyword documented |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-25*
