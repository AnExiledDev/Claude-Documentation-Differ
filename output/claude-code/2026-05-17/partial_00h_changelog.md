# Claude Code Documentation Changes — 2026-05-17

## Summary

Three documentation pages were updated in this cycle. The most significant addition is a new "Run Claude Code" step in the Microsoft Foundry setup guide, completing the end-to-end configuration walkthrough. Two minor clarifications were made: one to `effortLevel` settings constraints in model configuration, and one to skill substitution expansion behavior.

## Significant Changes

### Integrations

- **Microsoft Foundry: Added "Step 5 — Run Claude Code" to setup guide**: A new section was added completing the Foundry setup walkthrough with explicit startup instructions and a note clarifying that Foundry has no interactive setup wizard.
  > "Claude Code reads `CLAUDE_CODE_USE_FOUNDRY` and the other Foundry variables from the environment and connects to your Azure resource on the first prompt. Unlike Bedrock and Vertex AI, Foundry has no interactive setup wizard, so the environment variables in steps 3 and 4 are the only configuration path."
  - *Implication*: Developers configuring Claude Code with Azure AI Foundry now have a complete, explicit step sequence; there is no fallback interactive wizard, making correct environment variable setup the sole configuration path.
  - *Source*: [microsoft-foundry.md](https://code.claude.com/docs/en/microsoft-foundry.md)

## Minor Changes

- **model-config.md**: Clarified accepted `effortLevel` values in settings files. The entry now explicitly lists `low`, `medium`, `high`, and `xhigh` as valid, and notes that `max` is session-only and not accepted in the settings file. (+1/-1 lines)
- **skills.md**: Added a note that skill variable substitution runs only once over the original file — command output is not re-scanned for further placeholders, preventing chained placeholder expansion. (+2/-0 lines)

## Notable Details

- The `effortLevel` clarification in `model-config.md` effectively surfaces a constraint that was previously undocumented: the `max` effort value (available via `/model` or `--effort`) cannot be persisted in settings. Developers who set `max` will need to pass it per-session.
- The skills substitution note makes explicit that the `!<command>` expansion is single-pass. This is a behavioral boundary that could affect authors writing complex skill templates expecting nested or chained command substitution.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| microsoft-foundry.md | Modified | SIGNIFICANT | +10/-0 | Added "Step 5: Run Claude Code" section to Foundry setup guide |
| model-config.md | Modified | MINOR | +1/-1 | Clarified valid `effortLevel` values; noted `max` is session-only |
| skills.md | Modified | MINOR | +2/-0 | Noted that substitution is single-pass; commands cannot chain placeholder expansion |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-17*
