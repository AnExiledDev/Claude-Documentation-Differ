# Claude API Documentation Changes — 2026-04-27

## Summary

One page was modified: the Managed Agents Memory documentation. The specific beta limits table (with explicit numeric values for stores, memories, storage, and retention) has been removed and replaced with a generic statement deferring to default limits.

## Significant Changes

### Managed Agents — Memory

- **Beta limits table removed from Memory documentation**: The "Limits" section previously contained a detailed table of explicit numeric constraints for memory stores during the beta period. This table has been replaced with a single sentence referencing unspecified "default capacity and rate limits."

  > *Before:*
  > "The following limits apply while this feature is in beta. [Contact support](https://support.claude.com) if you need higher limits."
  >
  > *(followed by a table listing:)*
  > | Limit | Value |
  > | --- | --- |
  > | Memory stores per organization | 1,000 |
  > | Memories per store | 2,000 |
  > | Total storage per store | 100 MB (104,857,600 bytes) |
  > | Versions per store | 250,000 |
  > | Size per memory | 100 kB (102,400 bytes) |
  > | Version history retention | 30 days |
  > | Memory stores per session | 8 |
  > | `instructions` field per attachment | 4,096 characters |

  > *After:*
  > "Default capacity and rate limits apply to memory stores while this feature is in beta. [Contact support](https://support.claude.com) if you need higher limits."

  - *Implication*: Developers can no longer rely on the previously documented specific numeric limits. The shift to "default capacity and rate limits" without enumeration suggests the specific values may be in flux during beta, or limits are now managed separately (e.g., per-org, per-tier). Teams building against memory store constraints should contact support to confirm current effective limits.
  - *Source*: [Managed Agents — Memory](https://platform.claude.com/docs/en/managed-agents/memory.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/managed-agents/memory.md` | Modified | +1 / -12 | Removed explicit beta limits table; replaced with reference to default limits |

---
*Generated from Claude API documentation changes detected on 2026-04-27*
