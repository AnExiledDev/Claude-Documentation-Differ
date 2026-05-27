# Claude Code Documentation Changes — 2026-05-27

## Summary

Two substantial new pages were added: a comprehensive guide for configuring Claude Code in monorepos and large codebases, and a full reference for the new `security-guidance` plugin that reviews code changes for vulnerabilities during active sessions. The best-practices page gained a new "Add an adversarial review step" section, and the CLI reference underwent a large in-place rewrite (+66/-66 lines).

---

## Significant Changes

### Security

- **New `security-guidance` plugin documentation**: A dedicated page documents the official Anthropic `security-guidance` plugin, which hooks into Claude's edit, stop, and commit lifecycle to review code for vulnerabilities and instruct Claude to fix them in the same session. Three review layers are described:
  - **Per-edit pattern match** (no model call, zero cost): scans for `eval(`, `pickle`, `dangerouslySetInnerHTML`, `.github/workflows/` edits, and other risky patterns
  - **End-of-turn diff review**: a separate Claude instance reviews all files changed during a turn; fires in the background and re-prompts if issues are found
  - **Commit/push agentic review**: a deeper review that reads callers and surrounding code; capped at 20 reviews per rolling hour

  > "The plugin does not ask the same Claude instance that wrote the code to grade itself. The per-edit check is a deterministic string match with no model involved. The end-of-turn and commit reviews run as a separate Claude call with a fresh context and a security-focused prompt."

  - *Implication*: Developers can extend the plugin with project-specific patterns (`.claude/security-patterns.yaml`) and guidance (`.claude/claude-security-guidance.md`). End-of-turn and commit reviews default to **Claude Opus 4.7**; use `SECURITY_REVIEW_MODEL` and `SG_AGENTIC_MODEL` to override. Requires Claude Code CLI v2.1.144+ and Python 3.8+.
  - *Source*: [Catch security issues as Claude writes code](https://code.claude.com/docs/en/security-guidance.md)

- **`discover-plugins.md` — "Automatic security review" section added**: The plugin discovery page now includes a dedicated subsection linking the `security-guidance` plugin to its new reference page.
  > "The `security-guidance` plugin reviews each change Claude makes for common vulnerabilities and instructs Claude to fix what it finds in the same session."
  - *Source*: [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins.md)

### Large Codebases & Monorepos

- **New large-codebases guide**: A detailed guide covers how to scope Claude Code to relevant portions of large repositories. Key settings and techniques documented:

  | Capability | Mechanism |
  |---|---|
  | Load only relevant conventions | Per-directory `CLAUDE.md` files |
  | Exclude irrelevant CLAUDE.md files | `claudeMdExcludes` setting |
  | Block reads of build output / vendored code | `Read` deny rules in `permissions.deny` |
  | Symbol navigation without file scanning | Code intelligence plugins (LSP) |
  | Sparse worktrees for large repos | `worktree.sparsePaths` |
  | Cross-package file access | `additionalDirectories` / `--add-dir` |
  | Package-scoped skills | Per-directory `.claude/skills/` |

  > "In a large codebase, a single CLAUDE.md at the repository root tends to either grow to cover every subsystem's conventions, costing context on instructions unrelated to the current task, or stay too generic to be useful."

  - *Implication*: `claudeMdExcludes` accepts glob patterns matched against absolute paths; arrays merge across settings scopes (user, project, local, managed). `worktree.sparsePaths` enables git sparse-checkout so worktrees only check out listed directories plus root-level files. The `additionalDirectories` setting grants file access only and does **not** load skills or CLAUDE.md from added directories; `--add-dir` does load skills when `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` is set.
  - *Source*: [Set up Claude Code in a monorepo or large codebase](https://code.claude.com/docs/en/large-codebases.md)

### Best Practices

- **New "Add an adversarial review step" section**: The best-practices page gained a new section on using separate Claude sessions or subagents as reviewers to catch issues the writing session may miss.

  > "A fresh context improves code review since Claude won't be biased toward code it just wrote."

  The page also elaborates on the Writer/Reviewer parallel session pattern, where one session implements and a second session reviews with clean context:

  - *Implication*: Developers are now explicitly directed toward multi-session quality workflows as a documented best practice, not just an incidental capability.
  - *Source*: [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices.md)

### CLI Reference

- **Major in-place rewrite (+66/-66 lines)**: The CLI reference was substantially rewritten at equivalent length. Notable additions observed in the current content:
  - `--resume` now documents that background sessions appear in the picker **marked with `bg`** as of v2.1.144
  - `--install [version]` accepts `stable`, `latest`, or a specific version like `2.1.118`
  - `--exclude-dynamic-system-prompt-sections` flag documented: moves per-machine system prompt sections into the first user message to improve prompt-cache reuse across users/machines running the same task
  - `--fallback-model` documented as applying to print mode (`-p`) and background sessions only (ignored in interactive sessions)
  - Typo suggestion behavior noted: mistyped subcommands now print `Did you mean claude <command>?` and exit

  - *Implication*: The note that `claude --help` does not list every flag is now explicitly called out — developers should consult the documentation page rather than relying on `--help` output alone.
  - *Source*: [CLI reference](https://code.claude.com/docs/en/cli-reference.md)

---

## Minor Changes

- **admin-setup.md**: Minor addition (+1/-0 lines). [View](https://code.claude.com/docs/en/admin-setup.md)
- **amazon-bedrock.md**: Minor rewording (+1/-1 lines). [View](https://code.claude.com/docs/en/amazon-bedrock.md)
- **common-workflows.md**: Small addition (+2/-0 lines). [View](https://code.claude.com/docs/en/common-workflows.md)
- **google-vertex-ai.md**: Minor rewording (+1/-1 lines). [View](https://code.claude.com/docs/en/google-vertex-ai.md)
- **hooks-guide.md**: Small addition (+2/-0 lines). [View](https://code.claude.com/docs/en/hooks-guide.md)
- **mcp.md**: Minor rewording (+1/-1 lines). [View](https://code.claude.com/docs/en/mcp.md)
- **microsoft-foundry.md**: Minor rewording (+1/-1 lines). [View](https://code.claude.com/docs/en/microsoft-foundry.md)
- **security.md**: Small addition (+1/-0 lines). [View](https://code.claude.com/docs/en/security.md)
- **memory.md**: Rewording in memory documentation (+3/-3 lines). [View](https://code.claude.com/docs/en/memory.md)
- **plugins-reference.md**: Rewording in plugin reference (+3/-3 lines). [View](https://code.claude.com/docs/en/plugins-reference.md)

---

## New Pages

- **large-codebases.md** — Comprehensive guide for configuring Claude Code in monorepos and large single-tree codebases. Covers per-directory CLAUDE.md layering, `claudeMdExcludes`, `worktree.sparsePaths`, `additionalDirectories`, code intelligence plugins, and per-directory skills. [View](https://code.claude.com/docs/en/large-codebases.md)
- **security-guidance.md** — Full reference for the `security-guidance` plugin. Documents per-edit pattern matching, end-of-turn diff review, and commit/push agentic review. Includes custom rule authoring, environment variable controls, cost implications, and integration architecture. [View](https://code.claude.com/docs/en/security-guidance.md)

---

## Notable Details

- The `security-guidance` plugin's commit/push review is **agentic** (multiple model turns per commit), capped at 20 reviews per rolling hour. If commit review findings duplicate end-of-turn findings, Claude is not re-prompted — so a clean session produces no visible output from the commit layer.
- `worktree.sparsePaths` and `symlinkDirectories` are read from your **starting directory** before the worktree is created. After the worktree exists, settings load from the worktree root — meaning deny rules or other settings needed inside worktrees must be duplicated at the repository root's `.claude/settings.json`.
- The `additionalDirectories` setting and `--add-dir` flag differ in what they load: `additionalDirectories` grants file access only; `--add-dir` also loads skills from the added directory. CLAUDE.md and rules from `--add-dir` directories load only when `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` is set.
- The CLI reference explicitly calls out that `claude --help` does **not** list every flag — a flag's absence from `--help` does not mean it is unavailable.

---

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| large-codebases.md | New | SIGNIFICANT | new page | Monorepo and large codebase configuration guide |
| security-guidance.md | New | SIGNIFICANT | new page | Security guidance plugin full reference |
| best-practices.md | Modified | SIGNIFICANT | +29/-3 | New "Add an adversarial review step" section |
| cli-reference.md | Modified | SIGNIFICANT | +66/-66 | Large in-place rewrite of CLI flags and commands |
| discover-plugins.md | Modified | SIGNIFICANT | +4/-0 | New "Automatic security review" section |
| memory.md | Modified | SIGNIFICANT | +3/-3 | Minor rewording |
| plugins-reference.md | Modified | SIGNIFICANT | +3/-3 | Minor rewording |
| admin-setup.md | Modified | MINOR | +1/-0 | Small addition |
| amazon-bedrock.md | Modified | MINOR | +1/-1 | Minor rewording |
| common-workflows.md | Modified | MINOR | +2/-0 | Small addition |
| google-vertex-ai.md | Modified | MINOR | +1/-1 | Minor rewording |
| hooks-guide.md | Modified | MINOR | +2/-0 | Small addition |
| mcp.md | Modified | MINOR | +1/-1 | Minor rewording |
| microsoft-foundry.md | Modified | MINOR | +1/-1 | Minor rewording |
| security.md | Modified | MINOR | +1/-0 | Small addition |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-27*
