# Claude Code Documentation Changes — 2026-03-24

## Summary

This update introduces documentation for two significant new Desktop features — computer use (macOS, research preview) and Dispatch integration — along with a new platform comparison page. Supporting changes clarify scheduling options across surfaces, document what the sandbox does not cover, and add "right approach" guidance to remote-working pages.

## Significant Changes

### Features

#### Computer Use on Desktop (macOS)

- **New feature: Claude can control your screen and open apps**: The Desktop app now supports computer use on macOS (Pro and Max plans only, research preview). This lets Claude interact with native apps, the iOS simulator, desktop tools without a CLI, or anything only accessible via GUI.
  > *Computer use lets Claude open your apps, control your screen, and work directly on your machine the way you would. Ask Claude to test a native app in the iOS simulator, interact with a desktop tool that has no CLI, or automate something that only works through a GUI.*
  - *Implication*: Developers should note that computer use runs on the actual desktop, not inside the sandbox — the trust boundary is different from the sandboxed Bash tool. Per-app permission prompts gate each application and approvals are session-scoped (or 30-minute-scoped in Dispatch sessions).
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

- **App-level access tiers for computer use**: Access is tiered by app category and cannot be changed by users:

  | Tier | What Claude can do | Applies to |
  |---|---|---|
  | View only | See the app in screenshots | Browsers, trading platforms |
  | Click only | Click and scroll, but not type or use keyboard shortcuts | Terminals, IDEs |
  | Full control | Click, type, drag, and use keyboard shortcuts | Everything else |

  > *The [per-app access tiers] reinforce this: browsers are capped at view-only, and terminals and IDEs at click-only, steering Claude toward the dedicated tool even when computer use is active.*
  - *Implication*: Claude prefers the most precise tool first (connector → Bash → Chrome → computer use); screen control is reserved for things nothing else can reach.
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

- **Enable computer use**: Requires toggling on in **Settings > Desktop app > General** and granting two macOS system permissions: **Accessibility** and **Screen Recording**.
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

#### Dispatch Integration

- **New: Send tasks from your phone to Desktop**: Dispatch (the persistent conversation in the Cowork tab) can now spawn Claude Code sessions in the Desktop app. Task routing to Code happens explicitly ("open a Claude Code session and fix the login bug") or automatically for dev work (bug fixes, dependency updates, running tests, opening PRs). Sessions appear in the Code tab sidebar with a **Dispatch** badge; push notifications fire on completion.
  > *[Dispatch] is a persistent conversation with Claude that lives in the Cowork tab. You message Dispatch a task, and it decides how to handle it.*
  - *Implication*: Dispatch requires a Pro or Max plan and is not available on Team or Enterprise. Dispatch-spawned sessions that use computer use have 30-minute app-approval windows (not full-session like regular sessions).
  - *Source*: [Desktop](https://code.claude.com/docs/en/desktop.md)

### New Pages

- **[platforms.md](https://code.claude.com/docs/en/platforms.md)** — A new overview/index page: "Platforms and integrations". Covers where to run Claude Code (CLI, Desktop, VS Code, JetBrains, Web), how to connect tools (Chrome, GitHub Actions, GitLab CI/CD, Code Review, Slack), and a comparison table of all remote-access options (Dispatch, Remote Control, Channels, Slack, Scheduled tasks). Acts as a navigation hub for platform selection.

### Configuration & Documentation

- **Scheduling comparison table inlined across three pages**: All three scheduling pages previously included a shared `<Snippet file="scheduling-comparison.mdx" />`. This snippet has been replaced with an identical inline table on each page (desktop.md, scheduled-tasks.md, web-scheduled-tasks.md). Content is unchanged — the table compares Cloud, Desktop, and `/loop` scheduling across dimensions like machine requirements, persistence, file access, MCP servers, permission prompts, and minimum interval.
  > *Use **cloud tasks** for work that should run reliably without your machine. Use **Desktop tasks** when you need access to local files and tools. Use **`/loop`** for quick polling during a session.*
  - *Implication*: No behavior change. The inline approach makes each page fully self-contained.
  - *Source*: [Scheduled tasks (CLI)](https://code.claude.com/docs/en/scheduled-tasks.md), [Web scheduled tasks](https://code.claude.com/docs/en/web-scheduled-tasks.md), [Desktop](https://code.claude.com/docs/en/desktop.md)

- **"Choose the right approach" section added to Remote Control**: A new section at the end of the Remote Control page presents the full comparison table of remote-work options — Dispatch, Remote Control, Channels, Slack, and Scheduled tasks — with trigger, execution location, setup effort, and best-fit guidance for each.
  - *Implication*: Gives Remote Control users an off-ramp when a different approach fits better (e.g., Dispatch for fire-and-forget delegation, Channels for event-driven automation).
  - *Source*: [Remote Control](https://code.claude.com/docs/en/remote-control.md)

- **Sandboxing scope clarified**: A new "What sandboxing does not cover" section explicitly documents the sandbox's boundaries:
  > *The sandbox isolates Bash subprocesses. Other tools operate under different boundaries:*
  > - ***Built-in file tools**: Read, Edit, and Write use the permission system directly rather than running through the sandbox.*
  > - ***Computer use on Desktop**: when Claude opens apps and controls your screen on macOS, it runs on your actual desktop rather than in an isolated environment.*
  - *Implication*: Developers relying on the sandbox for full isolation should be aware that file tool access and computer use operate outside the sandbox perimeter.
  - *Source*: [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)

## Notable Details

- **CLI comparison table capitalization**: The CLI-vs-Desktop table in `desktop.md` had a minor capitalization normalization pass (e.g., `model dropdown` → `Model dropdown`, `not available` → `Not available`). No functional content changed.
- **Plugin marketplace walkthrough fix**: The example command in the `plugin-marketplaces.md` walkthrough was corrected from `/review` to `/quality-review`, matching the actual skill defined in the tutorial. This was a documentation bug.
- **Overview page gains Dispatch mention**: A single line was added to the "Work from anywhere" accordion: *"Message Dispatch a task from your phone and open the Desktop session it creates"*, linking to the new desktop.md anchor.
- **Total page count**: The docs metadata went from 68 to 69 pages, confirming `platforms.md` is the only net-new page.
- **Dispatch plan restriction**: Multiple places in the diff consistently note that Dispatch is Pro/Max only — not Team or Enterprise. This is a notable constraint for organizations.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| desktop.md | Modified | +110 / -23 | Computer use feature (4 new sections), Dispatch integration section, scheduling comparison table inlined, CLI comparison table updated with new rows and capitalization fixes |
| scheduled-tasks.md | Modified | +17 / -1 | Scheduling comparison snippet replaced with inline table |
| web-scheduled-tasks.md | Modified | +17 / -1 | Scheduling comparison snippet replaced with inline table |
| remote-control.md | Modified | +13 / -0 | "Choose the right approach" comparison table added; Dispatch added to related resources |
| sandboxing.md | Modified | +7 / -0 | "What sandboxing does not cover" section added |
| overview.md | Modified | +1 / -0 | Dispatch mention added to "Work from anywhere" accordion |
| plugin-marketplaces.md | Modified | +1 / -1 | Walkthrough example command corrected from `/review` to `/quality-review` |
| platforms.md | New | +78 | New platforms and integrations overview page |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-24*
