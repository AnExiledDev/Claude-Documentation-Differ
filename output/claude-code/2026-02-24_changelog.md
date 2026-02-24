# Claude Code Documentation Changes — 2026-02-24

## Summary

Two pages were updated: the agent teams guide gained a new section on choosing team size, and the terminal configuration guide restructured its notification setup section to expand native notification support beyond iTerm 2 to Kitty and Ghostty, while clarifying how hooks relate to terminal notifications.

## Significant Changes

### Agent Teams

- **New guidance on choosing team size**: A new "Choose an appropriate team size" section formalizes best-practice sizing recommendations for agent teams, covering the three key constraints that limit returns from larger teams.

  > Start with 3-5 teammates for most workflows. This balances parallel work with manageable coordination. The examples in this guide use 3-5 teammates because that range works well across different task types.

  > Having 5-6 tasks per teammate keeps everyone productive without excessive context switching. If you have 15 independent tasks, 3 teammates is a good starting point.

  The section also calls out that token costs scale linearly (each teammate has its own context window), coordination overhead grows with team size, and diminishing returns set in past a certain point. The concrete ratio of 5–6 tasks per teammate is a useful heuristic not previously documented.

  - *Implication*: Developers running large teams should treat this as a budget/efficiency guide. The docs now explicitly caution that "three focused teammates often outperform five scattered ones."
  - *Source*: [Agent Teams](https://code.claude.com/docs/en/agent-teams.md)

### Terminal Configuration

- **Kitty and Ghostty now documented as natively supporting desktop notifications**: The notification setup section was broadened from iTerm 2-only coverage to a general "Terminal notifications" section that names Kitty and Ghostty as zero-configuration options.

  > Kitty and Ghostty support desktop notifications without additional configuration. iTerm 2 requires setup.

  Previously, the section was titled "iTerm 2 system notifications" and only covered iTerm 2. Users of Kitty or Ghostty had no documentation confirming native support.

  - *Implication*: Kitty and Ghostty users can expect desktop notifications to work out of the box, without configuring hooks or any additional terminal settings.
  - *Source*: [Terminal Config](https://code.claude.com/docs/en/terminal-config.md)

- **Notification event model clarified**: The section intro was rewritten to describe the notification model in event-driven terms, replacing a vague "never miss when Claude completes a task" framing.

  > When Claude finishes working and is waiting for your input, it fires a notification event. You can surface this event as a desktop notification through your terminal or run custom logic with notification hooks.

  - *Implication*: The "waiting for your input" framing makes clear the notification fires at the handoff point — useful context for configuring hooks that respond to idle state.
  - *Source*: [Terminal Config](https://code.claude.com/docs/en/terminal-config.md)

- **Hooks clarified as complementary to, not a replacement for, terminal notifications**: The renamed "Notification hooks" section (formerly "Custom notification hooks") explicitly states that hooks run alongside native notifications.

  > Hooks run alongside terminal notifications, not as a replacement.

  Previously, the section positioned hooks as an "advanced" alternative for users without native notification support. The new framing makes clear hooks and terminal notifications are additive — you can use both simultaneously.

  - *Implication*: Users who want both a desktop notification and a custom action (e.g., playing a sound) can configure both without one overriding the other.
  - *Source*: [Terminal Config](https://code.claude.com/docs/en/terminal-config.md)

- **iTerm 2 setup instructions simplified**: The iTerm 2 configuration steps were condensed from 4 steps to 3, replacing the indirect "Filter Alerts → Send escape sequence-generated alerts" flow with a direct "Notification Center Alerts" toggle as the first step. A new troubleshooting note was added:

  > If notifications aren't appearing, verify that your terminal app has notification permissions in your OS settings.

  - *Implication*: Addresses a common failure mode (OS-level notification permissions) that was previously undocumented.
  - *Source*: [Terminal Config](https://code.claude.com/docs/en/terminal-config.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `agent-teams.md` | Modified | +14 / -0 | Added "Choose an appropriate team size" section with 3–5 teammate recommendation and 5–6 tasks-per-teammate heuristic |
| `terminal-config.md` | Modified | +11 / -10 | Broadened notification setup to cover Kitty and Ghostty natively; clarified notification event model and hook coexistence |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-24*
