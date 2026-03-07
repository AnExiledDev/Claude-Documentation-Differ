# Claude API Documentation Changes — 2026-03-07

## Summary

Four SDK documentation pages received minor code example improvements: corrected boilerplate, adjusted `hidelines`/`nocheck` code block annotations, and fixed a Ruby pagination loop. No API endpoints, parameters, or behaviors changed.

## Notable Details

### SDKs

- **Ruby — Pagination loop corrected**: The manual pagination example using `#next_page?` was changed from a one-time `if` check to a proper `while` loop, and now iterates over all items in each page.
  > Before:
  > ```ruby
  > if page.next_page?
  >   new_page = page.next_page
  >   puts(new_page.data[0].id)
  > end
  > ```
  > After:
  > ```ruby hidelines={1}
  > page = client.messages.batches.list(limit: 20)
  > while page.next_page?
  >   page = page.next_page
  >   page.data&.each { |batch| puts(batch.id) }
  > end
  > ```
  - *Implication*: The previous example only retrieved one additional page. The corrected loop now demonstrates full iteration over all pages, which is the intended usage pattern.
  - *Source*: [Ruby SDK](https://platform.claude.com/docs/en/api/sdks/ruby.md)

- **Ruby — Code examples made self-contained**: Three additional Ruby examples (file uploads, undocumented properties, undocumented endpoints) gained `require "anthropic"` / client initialization lines and `hidelines` or `nocheck` annotations to suppress them in rendered output. This keeps examples runnable as-is when copied.
  - *Source*: [Ruby SDK](https://platform.claude.com/docs/en/api/sdks/ruby.md)

- **C# — Manual pagination example completed**: The manual pagination code block annotation changed from `nocheck` to `hidelines={1..5}`, and four setup lines were added (`using Anthropic;`, `using System;`, blank line, `AnthropicClient client = new();`). The lines are hidden in rendered output but make the snippet compilable.
  - *Source*: [C# SDK](https://platform.claude.com/docs/en/api/sdks/csharp.md)

- **TypeScript — Error handling example simplified**: The error handling code block dropped `hidelines={1..4}` and removed the four hidden import/client-initialization lines entirely (`import Anthropic`, `const client = new Anthropic()`). The block now starts directly at the API call. This assumes a shared client context rather than embedding setup in every example.
  - *Source*: [TypeScript SDK](https://platform.claude.com/docs/en/api/sdks/typescript.md)

- **Errors page — Python example annotation cleaned up**: Removed the `nocheck` flag from the Python streaming `.stream()` / `.get_final_message()` code block. No code content changed.
  - *Source*: [Errors](https://platform.claude.com/docs/en/api/errors.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `sdks/ruby.md` | Modified | +14 / -8 | Pagination loop corrected (if → while); setup boilerplate added to three examples with hidelines/nocheck annotations |
| `sdks/csharp.md` | Modified | +4 / -1 | Manual pagination example completed with imports and client init; annotation changed from nocheck to hidelines={1..5} |
| `sdks/typescript.md` | Modified | +1 / -5 | Error handling example stripped of hidden import lines; annotation simplified |
| `errors.md` | Modified | +1 / -2 | Removed `nocheck` annotation from Python streaming example |

---
*Generated from Claude API documentation changes detected on 2026-03-07*
