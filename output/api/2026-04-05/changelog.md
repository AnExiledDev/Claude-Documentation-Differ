# Claude API Documentation Changes — 2026-04-05

## Summary

One page was modified today with a single substantive change: the maximum upload size limit for custom Agent Skills was raised from 8 MB to 30 MB. This limit appears in two locations within the skills guide — once in the upload requirements section and once in the request limits reference table.

## Significant Changes

### Agent Skills

- **Custom Skill upload size limit increased from 8 MB to 30 MB**: The maximum total file size for custom Skill uploads has been raised nearly fourfold. Both the requirements checklist and the request limits table now reflect the new 30 MB ceiling.
  > - Total upload size must be under 30&nbsp;MB
  - *Implication*: Developers building larger custom Skills (with more scripts, resources, or a heavier `SKILL.md`) can now upload packages up to 30 MB without hitting the previous 8 MB cap. No API or code changes are required to take advantage of the higher limit.
  - *Source*: [Using Agent Skills with the API](https://platform.claude.com/docs/en/build-with-claude/skills-guide.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/build-with-claude/skills-guide.md` | Modified | +2 / -2 | Skill upload size limit updated from 8 MB to 30 MB in requirements and request limits sections |
