# Claude API Documentation Changes — 2026-03-19

## Summary

One page was modified: the platform release notes overview. The primary developer-facing change is the addition of a March 18, 2026 entry announcing new model capability fields in the Models API. A minor platform branding rename ("Claude Developer Platform" → "Claude Platform") and a URL correction for the Models API link were also included.

## Significant Changes

### API

- **Models API now returns capability fields**: The `GET /v1/models` and `GET /v1/models/{model_id}` endpoints have been updated to include new fields in their responses.
  > "We've added model capability fields to the Models API. `GET /v1/models` and `GET /v1/models/{model_id}` now return `max_input_tokens`, `max_tokens`, and a `capabilities` object. Query the API to discover what each model supports."
  - *Implication*: Developers can now programmatically introspect model limits and capabilities at runtime without hardcoding values — useful for dynamic model selection and validation logic.
  - *Source*: [Release Notes Overview](https://platform.claude.com/docs/en/release-notes/overview.md)

## Notable Details

- **Platform branding rename**: The release notes page heading changed from "Claude Developer Platform" to "Claude Platform", with the subtitle updated to match. This is a cosmetic/branding change with no API impact.
- **Models API URL correction**: An internal documentation link to the Models API was updated from `/docs/en/api/models-list` to `/docs/en/api/models/list`. This corrects a broken link in the December 17, 2024 GA announcement entry.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `release-notes/overview.md` | Modified | +6 / -3 | Added March 18, 2026 entry for Models API capability fields; renamed platform title; fixed Models API URL |

---
*Generated from Claude API documentation changes detected on 2026-03-19*
