# Claude Code Documentation Changes — 2026-05-10

## Summary

One page was modified today: the hooks guide received a new dedicated section explaining how Claude Code merges results when multiple hooks match the same event. The change replaces a two-line inline note with a full subsection that includes parallel execution semantics, merge precedence rules, and a worked example.

## Significant Changes

### Configuration — Hooks

- **New "Combine results from multiple hooks" section**: The hooks guide previously described multi-hook result merging in two inline sentences placed before the hook type list. Those sentences have been removed and replaced with a dedicated subsection that substantially expands coverage (+32/-2 lines).

  Three key points are now explicitly documented:

  1. **All matching hooks run to completion** — a `deny` from one hook does not short-circuit sibling hooks:

     > When multiple hooks match the same event, every hook's command runs to completion before Claude Code merges the results. One hook returning `deny` does not stop sibling hooks from executing. Don't rely on one hook's `deny` to suppress side effects in another hook.

     - *Implication*: Developers who assumed an early `deny` would prevent side effects (e.g., audit logging or network calls) in co-registered hooks need to revisit their hook designs.

  2. **Merge precedence is now explicit**: `deny` overrides `ask`, which overrides `allow`. `additionalContext` from every hook is accumulated and forwarded to Claude together.

     > After all matching hooks finish, Claude Code combines their outputs. For `PreToolUse` permission decisions, the most restrictive answer wins: `deny` overrides `ask`, which overrides `allow`. Text from `additionalContext` is kept from every hook and passed to Claude together.

  3. **Worked example added**: The section includes a concrete JSON configuration registering two `PreToolUse` hooks on `Bash` — one for audit logging (exits 0) and one for blocking `rm -rf` (exits 2) — and walks through the parallel execution outcome:

     > When Claude tries to run `rm -rf /tmp/build`, both hooks execute in parallel. The logging hook writes the command to `~/.claude/bash.log` and exits 0, which reports no decision. The guardrail hook exits 2, which denies the tool call. The deny wins, so Claude Code blocks the command and shows Claude the guardrail's stderr. The log entry is still written because the logging hook already ran.

     - *Implication*: This is now the canonical pattern for combining observability hooks with enforcement hooks. Both concerns can be implemented as independent, decoupled hooks without needing to merge their logic.

  - *Source*: [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)

## Notable Details

- The removed two-line inline note was positioned immediately before the hook type table, which may have caused it to be overlooked. Moving this content into its own named section with a `###` heading makes it directly linkable and easier to find in the table of contents.
- The new section explicitly states hooks within a matcher run **in parallel**, not sequentially — a previously undocumented execution detail with significant implications for hook authors who care about ordering or isolation.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| hooks-guide.md | Modified | +32 / -2 | New "Combine results from multiple hooks" subsection replaces a two-sentence inline note; adds parallel execution semantics, merge precedence rules, and a two-hook worked example |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-10*
