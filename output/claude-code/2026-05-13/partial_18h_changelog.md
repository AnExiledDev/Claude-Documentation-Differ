# Claude Code Documentation Changes — 2026-05-13

## Summary

Six pages were modified with no additions or removals. The dominant theme is an upcoming billing change: starting June 15, 2026, Agent SDK and `claude -p` usage on subscription plans will draw from a new monthly Agent SDK credit, separate from interactive usage limits. Separately, the ultrareview free-run expiration date (May 5, 2026) has been removed from all references, reflecting that the promotional deadline has now passed.

## Significant Changes

### Billing & Pricing

- **New Agent SDK credit tier launching June 15, 2026**: A new notice has been added prominently to the `headless.md`, `authentication.md`, and `legal-and-compliance.md` pages announcing a billing change for programmatic usage.
  > Starting June 15, 2026, Agent SDK and `claude -p` usage on subscription plans will draw from a new monthly Agent SDK credit, separate from your interactive usage limits.
  - *Implication*: Developers using `claude -p` or the Agent SDK in CI/CD pipelines or scripts on Pro/Max/Team/Enterprise plans will have their usage tracked against a separate monthly quota after this date. The linked support article ([Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)) contains specifics on the new credit amount and overage handling.
  - *Source*: [headless.md](https://code.claude.com/docs/en/headless.md), [authentication.md](https://code.claude.com/docs/en/authentication.md), [legal-and-compliance.md](https://code.claude.com/docs/en/legal-and-compliance.md)

- **Ultrareview free-run expiration date removed**: The "through May 5, 2026" deadline has been scrubbed from both the pricing table and the prose description in `ultrareview.md`, and the matching entry in `commands.md`.
  > | Pro  | 3 free runs | billed as extra usage |
  > | Max  | 3 free runs | billed as extra usage |

  Previously the table read "3 free runs through May 5, 2026". The prose has also been updated:
  > Pro and Max subscribers receive three free ultrareview runs to try the feature. These three runs are a one-time allotment per account and do not refresh.

  The removed clause was: *"and expire on May 5, 2026."*
  - *Implication*: The promotional deadline has passed. The free runs are now described as a permanent one-time allotment with no expiry, suggesting the promotion has either been made permanent or the docs are being cleaned up post-expiry. Either way, any tooling or documentation referencing the May 5 cutoff is now stale.
  - *Source*: [ultrareview.md](https://code.claude.com/docs/en/ultrareview.md), [commands.md](https://code.claude.com/docs/en/commands.md)

### Headless Mode Documentation

- **Billing notice now leads the page**: The `headless.md` page was restructured to place the new June 15, 2026 Agent SDK billing note *before* the introductory paragraph about the Agent SDK, rather than after it. The old note ("The CLI was previously called 'headless mode'") was removed entirely.
  - Additionally, the introductory sentence was changed from "To run Claude Code programmatically from the CLI" to "To run Claude Code in non-interactive mode", aligning with the renaming of headless mode to the Agent SDK.
  - *Implication*: The removal of the "previously called headless mode" note suggests Anthropic considers the rename sufficiently established that users no longer need the backward-compatibility reminder.
  - *Source*: [headless.md](https://code.claude.com/docs/en/headless.md)

## Minor Changes

- **fast-mode.md**: Fixed pricing display formatting — `\$30/150 MTok` corrected to `$30/$150 MTok` (both input and output token prices now shown with dollar signs). (+1/-1)
- **authentication.md**: Added the Agent SDK billing notice Note callout under the "Generate a long-lived token" section. (+4/-0)
- **legal-and-compliance.md**: Added the Agent SDK billing notice Note callout at the top of the page, before the Legal agreements section. (+4/-0)
- **commands.md**: Removed "through May 5, 2026" from the `/ultrareview` command entry's free-run description. (+1/-1)

## Notable Details

- The Agent SDK billing notice appears in three separate pages (authentication, headless, legal-and-compliance), suggesting a deliberate effort to ensure high visibility for this upcoming change before its June 15, 2026 effective date.
- The `headless.md` page drop of the "previously called headless mode" backward-compat note is a small but meaningful signal that the Agent SDK brand has replaced the old "headless mode" terminology in Anthropic's view.
- The ultrareview table's column width in the markdown source was also tightened (alignment padding removed), though this has no rendered effect.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| ultrareview.md | Modified | SIGNIFICANT | +6/-6 | Removed May 5, 2026 free-run expiry date from table and prose |
| headless.md | Modified | SIGNIFICANT | +4/-4 | Added Agent SDK billing notice; removed old "headless mode" rename note; reworded intro |
| authentication.md | Modified | MINOR | +4/-0 | Added Agent SDK billing notice under long-lived token section |
| legal-and-compliance.md | Modified | MINOR | +4/-0 | Added Agent SDK billing notice at top of page |
| commands.md | Modified | MINOR | +1/-1 | Removed "through May 5, 2026" from `/ultrareview` entry |
| fast-mode.md | Modified | MINOR | +1/-1 | Fixed `$30/$150 MTok` pricing display formatting |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-13*
