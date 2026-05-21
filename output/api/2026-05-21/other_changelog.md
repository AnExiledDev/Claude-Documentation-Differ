# Claude API Documentation Changes — 2026-05-21

## Summary

Ten pages were modified, focused on workspace management and the Compliance API. The most substantive change is a new "Claude Code workspace" section documenting Anthropic's auto-provisioned workspace for Claude Code users, including unique per-user API key behavior and spend-limit capabilities. Compliance API docs were also updated to introduce `generated_files` (tool-produced binary files) and a new `claude_code_user` organization role.

---

## Significant Changes

### Workspaces

- **New "Claude Code workspace" section**: Anthropic automatically creates a dedicated **Claude Code** workspace the first time any organization member signs in to Claude Code through their Console account. All subsequent Claude Code sign-ins add members to this same workspace.

  > Claude Code mints a per-user API key in this workspace at sign-in. You cannot create keys in it manually from the Console.
  > A Claude Code key stops working if its owner is removed from the workspace or organization, unlike standard workspace keys.

  Key behaviors documented:
  - Rate limits are tracked **separately** from other workspaces; admins can cap its share of the organization's limits under Settings > Workspaces.
  - It is the **only workspace that supports per-user monthly spend limits**.
  - Archiving this workspace disables Claude Code sign-in through Console billing for the **entire organization**.

  > Archiving the Claude Code workspace disables Claude Code sign-in through Console billing for the whole organization.

  - *Implication*: Admins managing Claude Code rollout need to treat this workspace differently from standard workspaces — it cannot be managed the same way (no manual key creation, archive has org-wide impact).
  - *Source*: [Workspaces](https://platform.claude.com/docs/en/manage-claude/workspaces.md)

### Compliance API — Generated Files

- **New `generated_files` field on assistant messages**: The Get Chat Messages endpoint now surfaces a `generated_files` array on assistant messages, representing binary files the assistant produced via tool use during the conversation (e.g., PDFs, spreadsheets, slide decks). This is distinct from `files` (user uploads) and `artifacts` (versioned text documents).

  > `generated_files` are binary files the assistant created during the conversation through tool use (for example, PDFs, spreadsheets, or slide decks).

  Two new endpoints are referenced for this resource type:
  - **Download a Claude-generated file**: `claude_gen_file_*` ID → binary content
  - **Get generated-file metadata**: `claude_gen_file_*` ID → metadata only

  The retrieve table now covers four ID prefixes: `claude_file_*`, `claude_gen_file_*`, `claude_artifact_version_*`, and `claude_proj_doc_*`.

  - *Implication*: Compliance and eDiscovery workflows that consume assistant message content must now handle a third binary resource type alongside user-uploaded files and artifacts.
  - *Source*: [Compliance — Retrieve and delete chats, files, and projects](https://platform.claude.com/docs/en/manage-claude/compliance-content-data.md)

- **Clarified Enterprise-only scope for content endpoints**: The page note was rewritten to make explicit that the chat, file, and project content endpoints are **Claude Enterprise plan only**, not just generally Compliance API-gated.

  > The endpoints on this page retrieve and delete claude.ai content, which is available only to organizations on the Claude Enterprise plan.

  - *Implication*: Claude Console organizations with Compliance API access can use the Activity Feed but cannot call the chat/file/project content endpoints.
  - *Source*: [Compliance — Retrieve and delete chats, files, and projects](https://platform.claude.com/docs/en/manage-claude/compliance-content-data.md)

### Compliance API — New Organization Role

- **`claude_code_user` added to `organization_role` enum**: The List Organization Users endpoint documentation now includes `claude_code_user` as a valid value for the `organization_role` field, alongside existing roles (`admin`, `billing`, `developer`, `managed`, `membership_admin`, `owner`, `primary_owner`, `user`).

  > The `organization_role` field carries the user's built-in membership level within the listed organization (one of `admin`, `billing`, `claude_code_user`, `developer`, `managed`, `membership_admin`, `owner`, `primary_owner`, or `user`)

  - *Implication*: Compliance integrations that enumerate users and branch on role must handle this new value to correctly classify Claude Code users in directory reports.
  - *Source*: [Compliance — List organizations, users, roles, and groups](https://platform.claude.com/docs/en/manage-claude/compliance-org-data.md)

---

## Minor Changes

- **api-and-data-retention.md**: Small addition (+2/-0 lines). Likely a clarifying note or new retention detail. [View](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention.md)
- **compliance-activity-feed.md**: Single-line rewording (+1/-1). [View](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed.md)
- **data-residency.md**: Single-line update (+1/-1). [View](https://platform.claude.com/docs/en/manage-claude/data-residency.md)
- **wif-reference.md**: One-line addition (+1/-0). [View](https://platform.claude.com/docs/en/manage-claude/wif-reference.md)
- **workload-identity-federation.md**: Minor rewording (+2/-2). [View](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation.md)
- **get-started.md**: Minor rewording (+2/-2). [View](https://platform.claude.com/docs/en/get-started.md)
- **intro.md**: Minor rewording (+3/-3). [View](https://platform.claude.com/docs/en/intro.md)

---

## Notable Details

- The `workspaces.md` archive warning now explicitly cross-references the Claude Code workspace, warning that archiving it "immediately revokes all API keys in that workspace" and prevents org-wide Claude Code Console sign-in — two distinct consequences bundled into a single destructive action.
- Example JSON responses in `compliance-content-data.md` now reference `claude-opus-4-7` as the model value in chat metadata. This appears in illustrative response payloads, not model capability documentation.
- The Claude Code workspace is described as the **only workspace** supporting per-user monthly spend limits — a unique capability not available in any other workspace type.

---

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| workspaces.md | Modified | SIGNIFICANT | +30/-5 | New "Claude Code workspace" section with auto-provisioning, per-user keys, spend limits, and archive warning |
| compliance-content-data.md | Modified | SIGNIFICANT | +14/-10 | Added `generated_files` resource type; clarified Enterprise-only scope for content endpoints |
| compliance-org-data.md | Modified | SIGNIFICANT | +3/-2 | Added `claude_code_user` to `organization_role` enum |
| intro.md | Modified | SIGNIFICANT | +3/-3 | Minor rewording |
| api-and-data-retention.md | Modified | MINOR | +2/-0 | Small addition |
| workload-identity-federation.md | Modified | MINOR | +2/-2 | Minor rewording |
| get-started.md | Modified | MINOR | +2/-2 | Minor rewording |
| compliance-activity-feed.md | Modified | MINOR | +1/-1 | Single-line rewording |
| data-residency.md | Modified | MINOR | +1/-1 | Single-line update |
| wif-reference.md | Modified | MINOR | +1/-0 | One-line addition |

---

*Generated from Claude API documentation changes detected on 2026-05-21*
