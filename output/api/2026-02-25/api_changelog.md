# Claude API Documentation Changes — 2026-02-25

## Summary

One page was modified. Four IP addresses previously flagged as "in use but phasing out as of January 15, 2026" have been officially reclassified as phased out and consolidated into the existing "Phased out IP addresses" section. No new pages or removals.

## Significant Changes

### Network / IP Addresses

- **Four IP addresses promoted to "Phased out" status**: The addresses `34.162.46.92/32`, `34.162.102.82/32`, `34.162.136.91/32`, and `34.162.142.92/32` were previously listed with a deprecation warning ("still in use, but will be phased out starting January 15, 2026"). They have now been merged into the "Phased out IP addresses" section alongside the previously retired `34.162.183.95/32`.

  > Before:
  > *The following individual IP addresses are still in use, but will be phased out starting January 15, 2026.*
  > ```
  > 34.162.46.92/32
  > 34.162.102.82/32
  > 34.162.136.91/32
  > 34.162.142.92/32
  > ```
  >
  > After (merged into existing section):
  > **Phased out IP addresses** — The following IP addresses are no longer in use by Anthropic. If you have previously allowlisted these addresses, you should remove them from your firewall rules.

  - *Implication*: Developers who maintain firewall allowlists for outbound Anthropic traffic should remove these four addresses if they haven't already. The January 15, 2026 cutover date has passed; these IPs are now officially retired.
  - *Source*: [IP Addresses](https://platform.claude.com/docs/en/api/ip-addresses.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `docs/api/en/api/ip-addresses.md` | Modified | +3 / -8 | Retired four previously-warned IP addresses into the phased-out section |

---
*Generated from Claude API documentation changes detected on 2026-02-25*
