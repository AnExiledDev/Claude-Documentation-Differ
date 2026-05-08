# Claude API Documentation Changes — 2026-02-23

## Summary

Seven pages were modified in this update. The most substantive changes are a major restructuring of the `develop-tests.md` evaluation guide (which now absorbs the previously separate "define success" page), additions to the output consistency guardrails guide (new "Keep Claude in character" section), and a significant trimming of inline workspace documentation from the Administration API page.

## Significant Changes

### Testing and Evaluation

- **`develop-tests.md` expanded into a combined success criteria + evaluations guide**: The page was renamed from "Create strong empirical evaluations" to "Define success criteria and build evaluations" and now incorporates content that previously lived on a separate `define-success` page. The new guide covers defining SMART criteria (Specific, Measurable, Achievable, Relevant), common success dimensions, eval design principles, and grading methods — all in one document.
  > "Building a successful LLM-based application starts with clearly defining your success criteria and then designing evaluations to measure performance against them. This cycle is central to prompt engineering."
  - *Implication*: The `/docs/en/test-and-evaluate/define-success` URL is no longer referenced; all inbound links in the use-case guides and prompt engineering overview have been updated to point to `/docs/en/test-and-evaluate/develop-tests`. Any bookmarks or external links to the old `define-success` path may break.
  - *Source*: [Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)

- **"Brainstorm evaluations" next-step card replaced with a claude.ai link**: The "Next steps" card at the bottom of the evals page previously linked to the prompt engineering overview. It now links directly to `https://claude.ai/` with the suggestion to drop the page into a Claude chat to brainstorm criteria.
  > "Brainstorm success criteria for your use case with Claude on claude.ai. **Tip**: Drop this page into the chat as guidance for Claude!"
  - *Implication*: This is a pattern shift — official docs now actively directing developers to use Claude itself as a planning tool for evaluation design.
  - *Source*: [Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)

### Guardrails and Consistency

- **New "Keep Claude in character" section added to `increase-consistency.md`**: A new subsection was appended to the output consistency guide covering role-based prompting techniques, including using system prompts to define a persona and preparing Claude with example scenario-response pairs.
  > "For role-based applications, maintaining consistent character requires deliberate prompting."
  - The section includes an enterprise chatbot example (AcmeBot) showing how to structure system and user prompts for persona persistence, constraint enforcement, and handling edge-case queries.
  - *Implication*: This content was previously hinted at in the customer-support-chat guide (via a now-removed link to a separate `keep-claude-in-character` page). It has been folded directly into the consistency guide.
  - *Source*: [Increase output consistency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency)

### Administration API

- **Workspace code examples removed; replaced with a pointer to the Workspaces guide**: The Workspaces section of the Administration API page previously contained inline `curl` examples for creating, listing, and archiving workspaces. These have been removed. The section now reads as a single-line cross-reference.
  > "For a comprehensive guide to workspaces, including Console and API examples, see [Workspaces](/docs/en/build-with-claude/workspaces)."
  - *Implication*: Developers who previously used this page as a quick reference for workspace API calls must now navigate to the dedicated Workspaces page.
  - *Source*: [Administration API](https://platform.claude.com/docs/en/build-with-claude/administration-api)

- **Workspace FAQ entries removed from Administration API page**: Five FAQ accordion sections covering workspace limits (max 100), the Default Workspace, org role effects on workspace access, assignable workspace roles, and role change behavior have been removed from the Administration API FAQ. A new pointer directs readers to `workspaces#faq` instead.
  > "For workspace-specific questions, see the [Workspaces FAQ](/docs/en/build-with-claude/workspaces#faq)."
  - *Implication*: These workspace rules (e.g., 100-workspace limit, Default Workspace behavior, role inheritance rules) still exist in documentation — they have been moved, not deleted. The Administration API page is now scoped more narrowly to org members, invites, and API keys.
  - *Source*: [Administration API](https://platform.claude.com/docs/en/build-with-claude/administration-api)

- **Usage/cost and Claude Code analytics sections condensed**: Verbose descriptions of the Usage endpoint and Cost endpoint, with their full URLs, were replaced with brief one-line links to their respective dedicated pages.
  - Before: detailed bullet descriptions of `/v1/organizations/usage_report/messages` and `/v1/organizations/cost_report` with explanations of dimensions.
  - After: `"Track your organization's usage and costs with the [Usage and Cost API](/docs/en/build-with-claude/usage-cost-api)."`
  - *Source*: [Administration API](https://platform.claude.com/docs/en/build-with-claude/administration-api)

## Notable Details

- **`keep-claude-in-character` as a standalone reference is gone**: The customer-support-chat guide previously linked to `/docs/en/test-and-evaluate/strengthen-guardrails/keep-claude-in-character` as a distinct page. That link has been replaced with a link to `increase-consistency`. The content now lives inside `increase-consistency.md` as a subsection rather than a dedicated page.

- **Prefill deprecation note present in `increase-consistency.md`**: The page continues to carry an existing note that prefilling is deprecated for Claude Opus 4.6, Claude Sonnet 4.6, and Claude Sonnet 4.5, directing developers to use structured outputs or system prompt instructions instead. This note was not changed in this update but is worth noting for developers reading the page for the first time.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `about-claude/use-case-guides/customer-support-chat.md` | Modified | +2 / -2 | Updated link targets: `define-success` → `develop-tests`; `keep-claude-in-character` → `increase-consistency` |
| `about-claude/use-case-guides/legal-summarization.md` | Modified | +1 / -1 | Updated link from `define-success` to `develop-tests` |
| `about-claude/use-case-guides/ticket-routing.md` | Modified | +1 / -1 | Updated link from `define-success` to `develop-tests` |
| `build-with-claude/administration-api.md` | Modified | +6 / -73 | Removed workspace curl examples and FAQ; condensed usage/analytics sections to cross-references |
| `build-with-claude/prompt-engineering/overview.md` | Modified | +1 / -1 | Combined two linked pages (`define-success` + `develop-tests`) into a single reference |
| `test-and-evaluate/develop-tests.md` | Modified | +106 / -7 | Major expansion: absorbed success-criteria content, added SMART criteria framework, common criteria catalogue, multidimensional examples |
| `test-and-evaluate/strengthen-guardrails/increase-consistency.md` | Modified | +18 / -1 | Added "Keep Claude in character" section with role prompting guidance and enterprise chatbot example |

---
*Generated from Claude API documentation changes detected on 2026-02-23*
