# Claude API Documentation Changes — 2026-04-03

## Summary

One page was modified in today's update. The strict tool use documentation received a new "Data retention" section clarifying how tool schemas are cached, the HIPAA eligibility status of the feature, and specific guidance on what data must not appear in schema definitions.

## Significant Changes

### Tools

- **Data Retention Guidance Added to Strict Tool Use**: A new `## Data retention` section was appended to the strict tool use page. It documents that tool `input_schema` definitions are compiled into grammars and cached for up to 24 hours, that prompts and responses are not retained beyond the API response, and that the feature is HIPAA eligible with important restrictions on PHI placement.
  > Strict tool use compiles tool `input_schema` definitions into grammars using the same pipeline as structured outputs. Tool schemas are temporarily cached for up to 24 hours since last use. Prompts and responses are not retained beyond the API response.

  > Strict tool use is HIPAA eligible, but **PHI must not be included in tool schema definitions**. The API caches compiled schemas separately from message content, and these cached schemas do not receive the same PHI protections as prompts and responses. Do not include PHI in `input_schema` property names, `enum` values, `const` values, or `pattern` regular expressions. PHI should only appear in message content (prompts and responses), where it is protected under HIPAA safeguards.

  - *Implication*: Developers building HIPAA-covered applications must ensure that no protected health information appears in tool schema definitions (property names, enum values, const values, or regex patterns). PHI must be confined to message content only.
  - *Source*: [Strict Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use.md)

## Notable Details

- The new section cross-references the [structured outputs](/docs/en/build-with-claude/structured-outputs) page to explain the schema compilation pipeline, and links to [API and data retention](/docs/en/build-with-claude/api-and-data-retention) for full ZDR and HIPAA eligibility details across all features.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| [strict-tool-use.md](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use.md) | Modified | +9 / -1 | Added "Data retention" section covering schema caching, HIPAA eligibility, and PHI restrictions |
