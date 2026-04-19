# Claude API Documentation Changes — 2026-04-19

## Summary

One page was modified: the platform release notes. The change documents that Claude in Amazon Bedrock has moved from a research preview (invite-only, single region) to general availability for all Amazon Bedrock customers across 27 AWS regions. The April 7 entry's link was also updated to reflect the renamed documentation page.

## Significant Changes

### Platform Availability

- **Claude in Amazon Bedrock — General Availability**: A new bullet was added to the April 16, 2026 release notes entry documenting that Amazon Bedrock availability has expanded from a gated research preview to self-serve access for all Bedrock customers.
  > [Claude in Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock) is now open to all Amazon Bedrock customers. Claude Opus 4.7 and Claude Haiku 4.5 are available self-serve from the Bedrock console through the Messages API endpoint at `/anthropic/v1/messages`, in 27 AWS regions with global and regional endpoints.
  - *Implication*: Developers can now access Claude Opus 4.7 and Haiku 4.5 on Bedrock without contacting an account executive — previously only `us-east-1` was available and access was by invitation only.
  - *Source*: [Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

- **Amazon Bedrock documentation link updated**: The April 7 entry for the original research preview announcement was updated to point to the renamed documentation page. The old link referenced `/docs/en/build-with-claude/claude-in-amazon-bedrock-research-preview`; it now points to `/docs/en/build-with-claude/claude-in-amazon-bedrock`, consistent with the GA rename.
  - *Implication*: The research preview page has been consolidated into the main Bedrock integration page. Bookmarks to the old URL may break.
  - *Source*: [Release Notes](https://platform.claude.com/docs/en/release-notes/overview.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| release-notes/overview.md | Modified | +2 / -1 | Added Bedrock GA bullet to April 16 entry; updated April 7 Bedrock link to drop `-research-preview` suffix |

---
*Generated from Claude API documentation changes detected on 2026-04-19*
