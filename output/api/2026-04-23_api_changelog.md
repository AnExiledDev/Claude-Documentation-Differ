# Claude API Documentation Changes — 2026-04-23

## Summary

All 34 modified pages are within the Admin API reference. The changes add `curl` example requests to every Admin API endpoint and introduce a new `workspace_restricted_developer` workspace role. Three delete response schemas (`InviteDeleteResponse`, `UserDeleteResponse`, `MemberDeleteResponse`) were formally documented for the first time.

## Significant Changes

### Admin API

- **New `workspace_restricted_developer` workspace role**: The `workspace_role` enum has been expanded with a new role value across all workspace member operations (create, retrieve, list, update, and the `WorkspaceMember` domain type).

  > `workspace_role: "workspace_user" or "workspace_developer" or "workspace_restricted_developer" or 2 more`

  This new role sits between `workspace_user` and `workspace_developer`. Administrators can now assign members a restricted developer role, enabling finer-grained access control within workspaces.
  - *Implication*: Any code that validates or switches on `workspace_role` values should be updated to handle `"workspace_restricted_developer"`. Existing members are not affected automatically.
  - *Source*: [Workspaces Members](https://platform.claude.com/docs/en/api/admin/workspaces/members.md)

- **Formal documentation of delete response schemas**: Three response schemas that were previously undocumented or implicit are now explicitly defined in the API reference:

  - `InviteDeleteResponse = object { id: string, type: "invite_deleted" }`
  - `UserDeleteResponse = object { id: string, type: "user_deleted" }`
  - `MemberDeleteResponse = object { type: "workspace_member_deleted", user_id: string, workspace_id: string }`

  Note that `MemberDeleteResponse` returns `user_id` and `workspace_id` rather than a single `id`, unlike the other delete responses.
  - *Implication*: Developers relying on delete response shapes can now reference the formal schema. The asymmetry in `MemberDeleteResponse` is worth noting for response parsing code.
  - *Sources*: [Invites](https://platform.claude.com/docs/en/api/admin/invites.md), [Users](https://platform.claude.com/docs/en/api/admin/users.md), [Workspaces Members](https://platform.claude.com/docs/en/api/admin/workspaces/members.md)

- **`curl` examples added to all Admin API endpoints**: Every Admin API operation now includes a working `curl` example using `$ANTHROPIC_ADMIN_KEY`. All examples use the `anthropic-version: 2023-06-01` header and `X-Api-Key` for authentication. This covers the full surface area: organizations, invites, users, workspaces, workspace members, API keys, usage reports, and cost reports.

  > ```http
  > curl https://api.anthropic.com/v1/organizations/workspaces/$WORKSPACE_ID/members \
  >     -H 'Content-Type: application/json' \
  >     -H 'anthropic-version: 2023-06-01' \
  >     -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY" \
  >     -d '{"user_id": "user_01WCz1FkmYMm4gnmykNKUu3Q", "workspace_role": "workspace_user"}'
  > ```

  - *Implication*: Documentation-only change; no API behavior changed. Useful for quick prototyping and verifying authentication setup.
  - *Source*: [Admin API](https://platform.claude.com/docs/en/api/admin.md)

## Notable Details

- The `MemberDeleteResponse` schema notably includes `workspace_id` in its response, while `InviteDeleteResponse` and `UserDeleteResponse` only return `id` and `type`. This structural difference is now clearly documented.
- The expanded `workspace_role` enum in list/retrieve responses means the role `"workspace_restricted_developer"` may already be appearing in API responses for some organizations — the documentation update makes this official.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| admin.md | Modified | +305/-7 | Added curl examples for all inline endpoints; added `InviteDeleteResponse`, `UserDeleteResponse`, `MemberDeleteResponse` schemas; added `workspace_restricted_developer` role |
| admin/workspaces.md | Modified | +141/-8 | Added curl examples; added `workspace_restricted_developer` role to workspace member domain type; added `MemberDeleteResponse` schema |
| admin/workspaces/members.md | Modified | +92/-8 | Added curl examples; added `workspace_restricted_developer` role; added `MemberDeleteResponse` schema |
| admin/invites.md | Modified | +55/-1 | Added curl examples; added `InviteDeleteResponse` schema |
| admin/users.md | Modified | +54/-1 | Added curl examples; added `UserDeleteResponse` schema |
| admin/api_keys.md | Modified | +27/-1 | Added curl examples for retrieve, list, update |
| admin/workspaces/members/create.md | Modified | +20/-3 | Added curl example; added `workspace_restricted_developer` to request body and response |
| admin/workspaces/members/update.md | Modified | +19/-3 | Added curl example; added `workspace_restricted_developer` to request body and response |
| admin/usage_report.md | Modified | +16/-0 | Added curl examples for messages and Claude Code usage report endpoints |
| admin/invites/create.md | Modified | +14/-1 | Added curl example |
| admin/workspaces/create.md | Modified | +13/-1 | Added curl example |
| admin/workspaces/update.md | Modified | +13/-1 | Added curl example |
| admin/api_keys/update.md | Modified | +11/-1 | Added curl example |
| admin/users/update.md | Modified | +13/-1 | Added curl example |
| admin/workspaces/members/delete.md | Modified | +10/-1 | Added curl example |
| admin/workspaces/members/list.md | Modified | +12/-2 | Added curl example; updated role enum |
| admin/workspaces/members/retrieve.md | Modified | +12/-2 | Added curl example; updated role enum |
| admin/invites/delete.md | Modified | +10/-1 | Added curl example |
| admin/users/delete.md | Modified | +10/-1 | Added curl example |
| admin/workspaces/archive.md | Modified | +10/-1 | Added curl example |
| admin/api_keys/list.md | Modified | +9/-1 | Added curl example |
| admin/api_keys/retrieve.md | Modified | +9/-1 | Added curl example |
| admin/cost_report/retrieve.md | Modified | +9/-1 | Added curl example |
| admin/invites/list.md | Modified | +9/-1 | Added curl example |
| admin/invites/retrieve.md | Modified | +9/-1 | Added curl example |
| admin/organizations/me.md | Modified | +9/-1 | Added curl example |
| admin/usage_report/retrieve_claude_code.md | Modified | +9/-1 | Added curl example |
| admin/usage_report/retrieve_messages.md | Modified | +9/-1 | Added curl example |
| admin/users/list.md | Modified | +9/-1 | Added curl example |
| admin/users/retrieve.md | Modified | +9/-1 | Added curl example |
| admin/workspaces/list.md | Modified | +9/-1 | Added curl example |
| admin/workspaces/retrieve.md | Modified | +9/-1 | Added curl example |
| admin/cost_report.md | Modified | +8/-0 | Added curl example |
| admin/organizations.md | Modified | +8/-0 | Added curl example |

---
*Generated from Claude API documentation changes detected on 2026-04-23*
