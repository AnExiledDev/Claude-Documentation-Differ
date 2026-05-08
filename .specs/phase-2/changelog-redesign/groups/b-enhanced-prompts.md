---
group: b
title: Enhanced Changelog Prompts
issue: "2.3"
parallel: false
depends_on: [a]
files:
  - lib/prompts/claude_code.md (modify)
  - lib/prompts/api.md (modify)
---

## Acceptance Criteria

- [x] Both prompts include triage awareness: instruct Claude to read `triage.json` if it exists in the workspace
- [x] Triage instructions: respect rule-based classifications unless strong reason to override; note overrides with `[AI override: reason]`
- [x] Output schema includes explicit sections: Summary, Significant Changes (grouped), Minor Changes (bullet list), Changes by Page (table)
- [x] Significant Changes section: each entry has description, implication, source URL, before/after if applicable
- [x] Minor Changes section: brief bullet list at bottom, no deep analysis needed
- [x] Migration Notes section: only if breaking changes detected
- [x] Both prompts retain their source-specific analysis guidance (CLI features vs API endpoints)
- [x] Triage is soft dependency: prompts say "if triage.json exists" not "read triage.json" (backward compat)
- [x] Prompt structure is consistent between claude_code.md and api.md (shared sections, source-specific guidance)
