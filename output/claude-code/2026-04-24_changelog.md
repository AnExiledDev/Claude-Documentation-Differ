# Claude Code Documentation Changes — 2026-04-24

## Summary

Four third-party integration pages received a single identical change: the "Contact sales" button URL was updated from `www.anthropic.com/contact-sales` to `claude.com/contact-sales`. No functional documentation content changed; no pages were added or removed.

## Notable Details

- **"Contact sales" link domain migration**: The `ContactSalesCard` component embedded in the Amazon Bedrock, Google Vertex AI, Microsoft Foundry, and third-party integrations pages now points to `claude.com/contact-sales` instead of `www.anthropic.com/contact-sales`. This aligns the "Contact sales" CTA with the existing "View plans" link, which already pointed to `claude.com`. The change consolidates all sales and pricing CTAs under the `claude.com` domain.

  > `-  <a href={\`https://www.anthropic.com/contact-sales?${utm('contact_sales')}\`} className="cc-cs-btn-clay">`
  > `+  <a href={\`https://claude.com/contact-sales?${utm('contact_sales')}\`} className="cc-cs-btn-clay">`

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| amazon-bedrock.md | Modified | +1/-1 | "Contact sales" button URL updated to claude.com domain |
| google-vertex-ai.md | Modified | +1/-1 | "Contact sales" button URL updated to claude.com domain |
| microsoft-foundry.md | Modified | +1/-1 | "Contact sales" button URL updated to claude.com domain |
| third-party-integrations.md | Modified | +1/-1 | "Contact sales" button URL updated to claude.com domain |

---
*Generated from Claude Code CLI documentation changes detected on 2026-04-24*
