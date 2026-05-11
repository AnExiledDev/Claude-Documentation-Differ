# Claude API Documentation Changes — 2026-05-11

## Summary

Two pages in the `manage-claude` section received minor updates. All Admin API code examples in the usage/cost documentation had an environment variable renamed from `$ADMIN_API_KEY` to `$ANTHROPIC_ADMIN_KEY`. The workspaces page had two section headings reworded from "Via the …" to "Using the …".

## Significant Changes

### Admin API

- **Admin API key environment variable renamed in examples**: All curl code examples in the usage and cost API documentation now reference `$ANTHROPIC_ADMIN_KEY` instead of `$ADMIN_API_KEY` as the environment variable holding the Admin API key.
  > ```diff
  > -  --header "x-api-key: $ADMIN_API_KEY"
  > +  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
  > ```
  - *Implication*: This is a documentation example change only — the actual HTTP header (`x-api-key`) is unchanged. Developers who have local scripts modelled after these examples should rename their environment variable to `ANTHROPIC_ADMIN_KEY` to stay consistent with current documentation. The new name avoids ambiguity (it is clearly scoped to Anthropic) and may align with a convention used by Anthropic tooling.
  - *Source*: [Usage & Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api.md)

## Notable Details

- **Workspaces page section headings reworded**: The headings "Via the Console" and "Via the Admin API" were updated to "Using the Console" and "Using the Admin API" respectively. This is a cosmetic wording change with no functional impact.
  - *Source*: [Workspaces](https://platform.claude.com/docs/en/manage-claude/workspaces.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `manage-claude/usage-cost-api.md` | Modified | +11 / -11 | Renamed `$ADMIN_API_KEY` → `$ANTHROPIC_ADMIN_KEY` in all 11 curl examples |
| `manage-claude/workspaces.md` | Modified | +2 / -2 | Reworded two section headings ("Via the …" → "Using the …") |

---
*Generated from Claude API documentation changes detected on 2026-05-11*
