# Claude Code Documentation Changes — 2026-03-11

## Summary

Two meaningful changes landed in this cycle: a new `/btw` command for ephemeral side questions that never enter conversation history, and a shift in plugin documentation from "restart Claude Code" to "run `/reload-plugins`" — reflecting that plugin changes no longer require a full restart. Cross-references to both features were added across multiple pages.

## Significant Changes

### Features

- **New `/btw` command for ephemeral side questions**: A new interactive-mode command, `/btw <question>`, lets users ask quick questions about the current session without adding anything to the conversation history. The question and answer appear in a dismissible overlay.
  > "Side questions have full visibility into the current conversation, so you can ask about code Claude has already read, decisions it made earlier, or anything else from the session. The question and answer are ephemeral: they appear in a dismissible overlay and never enter the conversation history."

  Key characteristics documented:
  - **Available while Claude is working**: `/btw` can be invoked mid-turn without interrupting the main response.
  - **No tool access**: Claude cannot read files, run commands, or search when answering — it answers only from existing context.
  - **Single response**: no follow-up turns; use a normal prompt if a back-and-forth is needed.
  - **Low cost**: reuses the parent conversation's prompt cache, so additional cost is minimal.
  - Dismissed with **Space**, **Enter**, or **Escape**.

  > "`/btw` is the inverse of a subagent: it sees your full conversation but has no tools, while a subagent has full tools but starts with an empty context."

  - *Implication*: Developers can quickly check details (file names, earlier decisions, config values) during long-running tasks without polluting the context window or interrupting Claude's work.
  - *Source*: [Interactive mode](https://code.claude.com/docs/en/interactive-mode.md)

### Configuration

- **Plugin changes no longer require a restart — use `/reload-plugins`**: Documentation across the plugins guides has been updated to replace "restart Claude Code" with "run `/reload-plugins`" as the way to pick up plugin changes. A new note clarifies that LSP server configuration changes are the remaining exception still requiring a full restart.
  > "As you make changes to your plugin, run `/reload-plugins` to pick up the updates without restarting. Changes to LSP server configuration still require a full restart."

  This change appears in three locations in `plugins.md`:
  1. After modifying a skill during quickstart development
  2. After installing a plugin that contains Agent Skills
  3. During the test/iterate loop for local plugin development

  The `discover-plugins.md` auto-update notification wording was also updated accordingly:
  > "If any plugins were updated, you'll see a notification prompting you to run `/reload-plugins`."
  (Previously: "you'll see a notification suggesting you restart Claude Code.")

  - *Implication*: Plugin development iteration is faster — skill and hook changes can be loaded in-session without losing conversation context.
  - *Source*: [Create plugins](https://code.claude.com/docs/en/plugins.md), [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins.md)

### Cross-references Added

- **`/btw` added to best practices context management section**: The "Manage context aggressively" section in best practices now recommends `/btw` as a low-cost way to check details without growing the context window.
  > "For quick questions that don't need to stay in context, use `/btw`. The answer appears in a dismissible overlay and never enters conversation history, so you can check a detail without growing context."
  - *Source*: [Best practices](https://code.claude.com/docs/en/best-practices.md)

- **`/btw` added to sub-agents guidance**: The sub-agents page now directs users toward `/btw` when they want to ask about something already in their conversation rather than spin up a subagent.
  > "For a quick question about something already in your conversation, use `/btw` instead of a subagent. It sees your full context but has no tool access, and the answer is discarded rather than added to history."
  - *Source*: [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

## Notable Details

- The `/btw` command table entry in `interactive-mode.md` uses a URL-encoded anchor (`#side-questions-with-%2Fbtw`) to link to the new section, which indicates the section header includes a literal `/` character — a minor detail relevant to anyone building tooling that parses these docs.
- The `changelog.md` page reflects a GitHub repo star count update (76.2k → 76.3k) and an open PR count change (318 → 329). These are scraped UI metadata from the GitHub repository mirror and are not meaningful documentation changes.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| interactive-mode.md | Modified | +20 / -0 | New `/btw` command added to command table and new "Side questions with /btw" section |
| plugins.md | Modified | +3 / -3 | Three instances of "restart Claude Code" replaced with "run `/reload-plugins`"; one instance adds "without restarting" and notes LSP still requires restart |
| discover-plugins.md | Modified | +1 / -1 | Auto-update notification wording updated to reference `/reload-plugins` instead of restart |
| sub-agents.md | Modified | +2 / -0 | Added cross-reference to `/btw` as alternative for quick in-context questions |
| best-practices.md | Modified | +1 / -0 | Added `/btw` recommendation in context management section |
| changelog.md | Modified | +2 / -2 | GitHub star/PR count metadata update (noise) |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-11*
