# Claude Code Documentation Changes — 2026-04-03

## Summary

Two pages were updated: the Amazon Bedrock setup guide received clarifications to console navigation and added AWS Organizations support for the use case form submission, and the Desktop quickstart page was restructured to surface download links and subscription requirements earlier in the page flow.

## Significant Changes

### Integrations

- **Amazon Bedrock: AWS Organizations support for use case form**: A new paragraph documents that AWS Organizations users can submit the Anthropic use case form once from the management account via the `PutUseCaseForModelAccess` API, with approval automatically extending to child accounts.
  > If you use AWS Organizations, you can submit the form once from the management account using the [`PutUseCaseForModelAccess` API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html). This call requires the `bedrock:PutUseCaseForModelAccess` IAM permission. Approval extends to child accounts automatically.
  - *Implication*: Enterprise/org admins can unblock all child accounts in a single step rather than repeating the use case form submission per account.
  - *Source*: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md)

- **Amazon Bedrock: Updated console navigation path for use case form**: Step 3 of the use case form process changed from **Chat/Text playground** to selecting a model from the **Model catalog**. Step 4 now confirms that access is granted immediately upon submission.
  > 3. Select an Anthropic model from the **Model catalog**
  > 4. Complete the use case form. Access is granted immediately after submission.
  - *Implication*: The previous navigation path (Chat/Text playground) no longer reflects the current Bedrock console UI. Users following the old instructions would not have been able to locate the form.
  - *Source*: [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md)

### Desktop App

- **Desktop quickstart: Download links and subscription notice moved above the fold**: Platform download links (macOS, Windows x64, Windows ARM64) and the Pro/Max/Team/Enterprise subscription requirement note were relocated from inside the numbered Install steps to the top of the page, before the introductory walkthrough text.
  > Claude Code requires a [Pro, Max, Team, or Enterprise subscription](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=desktop_quickstart_pricing).
  - *Implication*: Visitors now see download options and the subscription requirement before reading any setup steps, reducing time-to-download and surfacing the paywall earlier.
  - *Source*: [Desktop Quickstart](https://code.claude.com/docs/en/desktop-quickstart.md)

- **Desktop quickstart: "Download the app" and "Sign in" steps merged into one**: The two-step install sequence was collapsed into a single step titled "Install and sign in". The in-step download options are now plain bullet links rather than visual Cards.
  > * [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs): universal build for Intel and Apple Silicon
  > * [Windows x64](https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code&utm_medium=docs): for x64 processors
  > * [Windows ARM64](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code&utm_medium=docs): for ARM processors
  - *Implication*: The Windows ARM64 installer now has a clearly labeled direct link — previously it was labeled ambiguously as "download here".
  - *Source*: [Desktop Quickstart](https://code.claude.com/docs/en/desktop-quickstart.md)

- **Desktop quickstart: Interface screenshot removed**: The light/dark mode `<Frame>` containing screenshots of the Claude Code Desktop "Code" tab was removed from the page introduction.
  - *Implication*: The page is lighter to load but loses the visual orientation aid for first-time users.
  - *Source*: [Desktop Quickstart](https://code.claude.com/docs/en/desktop-quickstart.md)

## Notable Details

- The Bedrock page previously stated that use case submission is "done once per account" — this was tightened to "once per AWS account", a small but meaningful precision distinguishing AWS accounts from Anthropic accounts.
- The IAM permissions reference in Bedrock step 1 changed from "see more on that below" to "described below" — minor wording tightening with no functional change.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `amazon-bedrock.md` | Modified | +6 / -4 | Updated Bedrock console navigation steps; added AWS Organizations `PutUseCaseForModelAccess` API documentation |
| `desktop-quickstart.md` | Modified | +22 / -26 | Moved download links and subscription note above the fold; merged install steps; removed desktop screenshot |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-03*
