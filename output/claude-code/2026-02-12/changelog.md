# Claude Code CLI Documentation Changes - February 12, 2026

## TL;DR
A single but significant clarification: Claude for Teams now requires a newer version (2.1.38+) for server-managed settings, while Enterprise users can continue using 2.1.30+. This suggests Teams and Enterprise are diverging in their technical requirements.

## Version Requirement Changes

### Server-Managed Settings Version Split

**What Changed**: Different minimum versions now required for Teams vs Enterprise plans

- **Claude for Teams**: Now requires version **2.1.38 or later** (up from 2.1.30)
- **Claude for Enterprise**: Still requires version **2.1.30 or later**

> "Claude Code version 2.1.38 or later for Claude for Teams, or version 2.1.30 or later for Claude for Enterprise"

**Why This Matters**:
- Suggests Claude for Teams may be getting newer features or different server-managed settings capabilities than Enterprise
- Organizations on Teams plan may need to upgrade to access server-managed settings
- Points to possible feature parity differences between subscription tiers
- Could indicate that versions 2.1.30-2.1.37 had Teams-specific issues with server-managed settings

## Hidden Gems

- **8-version gap between tiers**: The fact that Teams requires 2.1.38 while Enterprise only needs 2.1.30 suggests either:
  - A bug or compatibility issue in versions 2.1.30-2.1.37 that only affects Teams deployments
  - Teams is being used as a testing ground for newer server-managed settings features before Enterprise adoption
  - Different authentication or API integration paths between the two tiers

## Technical Details

**File Modified**: `docs/claude-code/en/server-managed-settings.md`

**Prerequisites for Server-Managed Settings** (updated):
- Claude for Teams: v2.1.38+
- Claude for Enterprise: v2.1.30+
- Network access to `api.anthropic.com` (unchanged)

---
*Generated from Claude Code CLI documentation changes detected on February 12, 2026*
