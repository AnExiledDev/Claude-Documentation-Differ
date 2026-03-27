# Claude API Documentation Changes — 2026-03-27

## Summary

One page was updated in this diff: the Ruby SDK documentation. The change updates a cross-reference link in the "Input schema and tool calling" section to point to a more specific tool runner page rather than the general tool use implementation guide.

## Significant Changes

### SDKs

- **Ruby SDK — Tool Use Cross-Reference Updated**: The link in the "Input schema and tool calling" section now points to a dedicated "Tool Runner (SDK)" page instead of the general "Implementing Tool Use" page.
  > Before: `see [Implementing Tool Use](/docs/en/agents-and-tools/tool-use/implement-tool-use)`
  > After: `see [Tool Runner (SDK)](/docs/en/agents-and-tools/tool-use/tool-runner)`
  - *Implication*: Developers following the Ruby SDK docs for tool calling will now be directed to a dedicated tool runner reference (`/docs/en/agents-and-tools/tool-use/tool-runner`) rather than the broader tool use implementation guide. This suggests the tool runner documentation has been split into its own page.
  - *Source*: [Ruby SDK](https://platform.claude.com/docs/en/api/sdks/ruby.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/api/sdks/ruby.md` | Modified | +1 / -1 | Updated cross-reference link for tool use documentation from general implementation guide to dedicated tool runner page |
