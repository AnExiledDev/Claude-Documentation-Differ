# Claude Code Documentation Changes — 2026-05-21

## Summary

Two documentation pages were updated. The errors reference page received meaningful changes: server error messages now display human-readable text instead of raw JSON, and error guidance was broadened to cover Bedrock, Vertex AI, Foundry, and custom gateways more explicitly. The scheduled-tasks page had minor wording cleanup removing a feature-rollout caveat.

## Significant Changes

### Error Handling

- **5xx error messages reformatted to human-readable text**: The displayed error for 500 responses changed from raw JSON (`{"type":"error","error":{"type":"api_error","message":"Internal server error"}}`) to plain language with embedded guidance:
  > `API Error: 500 Internal server error. This is a server-side issue, usually temporary — try again in a moment. If it persists, check status.claude.com.`

  The same pattern was applied to the 529 overloaded error:
  > `API Error: Repeated 529 Overloaded errors. The API is at capacity — this is usually temporary. Try again in a moment. If it persists, check status.claude.com.`

  - *Implication*: Users (and scripts parsing error output) will now see structured plain-text messages rather than raw API JSON. Any tooling that parsed the previous JSON format from stderr will need to be updated.
  - *Source*: [Error reference](https://code.claude.com/docs/en/errors.md)

- **Server error descriptions broadened to all inference providers**: The "Server errors" section header now explicitly covers non-Anthropic providers:
  > "These errors come from the inference provider rather than your account or request. On the Anthropic API that means Anthropic infrastructure. On Bedrock, Vertex AI, Foundry, or a custom gateway it means that provider's infrastructure."

  The "What to do" steps for 500 and 529 errors were updated to direct users to their provider's status page rather than always pointing to `status.claude.com`:
  > "Check [status.claude.com](https://status.claude.com), or the provider status page named in the message, for active incidents"

  A new explanatory note was added documenting how the trailing status-check sentence in error messages is provider-specific:
  > "The trailing sentence names where to check service health and varies by provider. Bedrock, Vertex AI, and Foundry configurations name that provider's service status. A custom `ANTHROPIC_BASE_URL` names the gateway host."

  - *Implication*: Bedrock, Vertex AI, Foundry, and custom gateway users now get provider-aware error text and relevant status page links directly in the error message, reducing the need to manually identify the right status page.
  - *Source*: [Error reference](https://code.claude.com/docs/en/errors.md)

- **Foundry added to the 429 provider list**: The 429 rate-limit error guidance previously listed only "Bedrock and Vertex AI" as providers with custom status pages. It now adds Foundry and `ANTHROPIC_BASE_URL` custom gateways:
  > "Bedrock, Vertex AI, and Foundry configurations name that provider's service status instead of the Anthropic status page. A custom `ANTHROPIC_BASE_URL` names the gateway host."

  - *Implication*: Foundry users will find their infrastructure named explicitly in both 429 and 5xx error guidance.
  - *Source*: [Error reference](https://code.claude.com/docs/en/errors.md)

## Minor Changes

- **[scheduled-tasks.md]**: Removed the "not available to everyone yet" rollout caveat from the built-in `/loop` maintenance prompt. Notes for Bedrock, Vertex AI, and Microsoft Foundry were simplified to directly state the restriction (usage message printed instead) without implying a broader availability gap. (+2/-2 lines)

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| errors.md | Modified | SIGNIFICANT | +11/-9 | Error messages reformatted to plain text; server error guidance broadened to Bedrock/Vertex AI/Foundry/custom gateway |
| scheduled-tasks.md | Modified | MINOR | +2/-2 | Removed rollout caveat for `/loop` maintenance prompt; simplified Bedrock/Vertex AI/Foundry restriction notes |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-21*
