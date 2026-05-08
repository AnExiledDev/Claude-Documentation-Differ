# Claude API Documentation Changes — 2026-03-11

## Summary

One minor change to the pricing documentation: the reference link to Microsoft Foundry's pricing page was removed from the list of third-party platform pricing resources. No API behavior, pricing values, or other content changed.

## Notable Details

- **Microsoft Foundry pricing link removed from regional pricing note**: The sentence describing third-party platform pricing for the `inference_geo` parameter previously listed three platforms (AWS Bedrock, Google Vertex AI, and Microsoft Foundry). The Microsoft Foundry link has been removed, leaving only AWS Bedrock and Google Vertex AI.

  > Before: *"See [AWS Bedrock](https://aws.amazon.com/bedrock/pricing/), [Google Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/pricing), and [Microsoft Foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/#pricing) for details."*

  > After: *"See [AWS Bedrock](https://aws.amazon.com/bedrock/pricing/) and [Google Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/pricing) for details."*

  - *Implication*: Developers using Claude through Azure/Microsoft Foundry should consult Microsoft's documentation directly for current pricing; the omission of the link does not indicate a change in support status.
  - *Source*: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| about-claude/pricing.md | Modified | +1/-1 | Removed Microsoft Foundry pricing link from third-party platform list |

---
*Generated from Claude API documentation changes detected on 2026-03-11*
