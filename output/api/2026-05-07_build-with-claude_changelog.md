# Claude API Documentation Changes — 2026-05-07

## Summary

Seven pages in the `build-with-claude` section were updated. The primary changes are: (1) a documentation restructuring where management-related pages (`data-residency`, `api-and-data-retention`, `usage-cost-api`) moved from `/build-with-claude/` to a new `/manage-claude/` path, with internal links updated across six pages; and (2) PHP SDK improvements to the Files API, most notably the addition of a native `download()` method that replaces a previous manual REST workaround.

## Significant Changes

### PHP SDK — Files API

- **`download()` method now available in PHP SDK**: The PHP SDK previously lacked a native file download method. Documentation explicitly noted: "The PHP SDK doesn't include a file download method. Use `retrieveMetadata()` for file info, then download the file content via the REST API." This workaround (manually constructing HTTP headers and using `file_get_contents()` against the REST endpoint) has been replaced with a direct SDK call.
  > ```php
  > // Before: manual REST API workaround with custom HTTP context
  > $context = stream_context_create([
  >     'http' => [
  >         'header' => implode("\r\n", [
  >             "x-api-key: $apiKey",
  >             "anthropic-version: 2023-06-01",
  >             "anthropic-beta: files-api-2025-04-14",
  >         ]),
  >     ],
  > ]);
  > $fileContent = file_get_contents("https://api.anthropic.com/v1/files/$fileId/content", false, $context);
  >
  > // After: native SDK method
  > $fileContent = $client->beta->files->download($fileId);
  > ```
  - *Implication*: PHP developers no longer need to manually manage API keys, version headers, or beta flags to download files — the SDK handles it natively.
  - *Source*: [Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide.md), [Files API](https://platform.claude.com/docs/en/build-with-claude/files.md)

- **PHP SDK method signatures simplified to positional arguments**: Several PHP Files API methods were updated from named `fileID:` keyword arguments to positional arguments, aligning with updated SDK conventions.
  > ```php
  > // Before
  > $file = $client->beta->files->retrieveMetadata(fileID: $fileId);
  > $result = $client->beta->files->delete(fileID: $fileId);
  >
  > // After
  > $file = $client->beta->files->retrieveMetadata($fileId);
  > $result = $client->beta->files->delete($fileId);
  > ```
  - *Implication*: Existing PHP code using named `fileID:` arguments may need updating for SDK compatibility.
  - *Source*: [Files API](https://platform.claude.com/docs/en/build-with-claude/files.md), [Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide.md)

- **PHP file upload updated to use `FileParam::fromResource()`**: The PHP upload example changed from passing a bare resource handle to using `FileParam::fromResource()` with an explicit content type.
  > ```php
  > // Before
  > $file = $client->beta->files->upload(
  >     file: fopen('/path/to/document.pdf', 'r'),
  > );
  >
  > // After
  > $file = $client->beta->files->upload(
  >     FileParam::fromResource(fopen('/path/to/document.pdf', 'rb'), contentType: 'application/pdf'),
  > );
  > ```
  - *Implication*: Explicit `contentType` specification via `FileParam::fromResource()` is the new recommended pattern for file uploads in PHP.
  - *Source*: [Files API](https://platform.claude.com/docs/en/build-with-claude/files.md)

### Documentation Restructuring — `/manage-claude/` Path

- **Management-related docs moved from `/build-with-claude/` to `/manage-claude/`**: Internal links to `api-and-data-retention`, `data-residency`, and `usage-cost-api` were updated across six pages to reflect a new URL structure.

  Affected link targets:
  - `/docs/en/build-with-claude/api-and-data-retention` → `/docs/en/manage-claude/api-and-data-retention`
  - `/docs/en/build-with-claude/data-residency` → `/docs/en/manage-claude/data-residency`
  - `/docs/en/build-with-claude/usage-cost-api` → `/docs/en/manage-claude/usage-cost-api`

  - *Implication*: Any external bookmarks or hardcoded links to these pages under `/build-with-claude/` may break. Developers referencing ZDR eligibility, data residency, or usage cost documentation should update their saved links.
  - *Source*: [Batch Processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing.md), [Fast Mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode.md), [Files API](https://platform.claude.com/docs/en/build-with-claude/files.md), [Overview](https://platform.claude.com/docs/en/build-with-claude/overview.md), [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md), [Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide.md), [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md)

## Notable Details

- **`skills-guide.md` code example format changed**: The multi-SDK "Creating and downloading an Excel file" example switched from a `<Tabs>/<Tab>` MDX component to a `<CodeGroup>` component. This is a documentation rendering change with no API impact, but it also removed the PHP-specific note about the missing download method (since the method now exists).

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| skills-guide.md | Modified | +8/-60 | PHP Files API download now uses native SDK method; `<Tabs>` replaced with `<CodeGroup>`; ZDR link path updated |
| files.md | Modified | +9/-29 | PHP upload uses `FileParam::fromResource()`; `retrieveMetadata()` and `delete()` use positional args; `download()` uses positional args; ZDR link path updated |
| fast-mode.md | Modified | +2/-2 | Links to `data-residency` and `usage-cost-api` updated to `/manage-claude/` path |
| overview.md | Modified | +2/-2 | Links to `data-residency` and `api-and-data-retention` updated to `/manage-claude/` path |
| batch-processing.md | Modified | +1/-1 | Link to `api-and-data-retention` updated to `/manage-claude/` path |
| prompt-caching.md | Modified | +1/-1 | Link to `api-and-data-retention` updated to `/manage-claude/` path |
| structured-outputs.md | Modified | +1/-1 | Link to `api-and-data-retention` updated to `/manage-claude/` path |

---
*Generated from Claude API documentation changes detected on 2026-05-07*
