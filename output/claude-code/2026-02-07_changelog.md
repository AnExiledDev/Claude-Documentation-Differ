# Claude Code CLI Documentation Changes - February 7, 2026

## TL;DR
Claude Code has introduced **Fast Mode**, a new research preview feature that delivers faster Opus 4.6 responses at a higher token cost. Users can now toggle between speed-optimized and cost-optimized modes using the `/fast` command, with fast mode offering lower latency for interactive work at premium pricing ($30/150 MTok, discounted 50% until Feb 16).

## New Features & Capabilities

### **Fast Mode for Opus 4.6**
A game-changing new feature that lets users trade cost for speed in real-time:

> "Fast mode delivers faster Opus 4.6 responses at a higher cost per token. Toggle it on with `/fast` when you need speed for interactive work like rapid iteration or live debugging, and toggle it off when cost matters more than latency."

**Key characteristics:**
- Same model quality, just faster API configuration
- Toggle via `/fast` command or `"fastMode": true` in settings
- Automatic model switch to Opus 4.6 when enabled
- Visual indicator: `↯` icon appears next to prompt
- Persists across sessions

**Pricing structure:**
- Fast mode (<200K): $30 input / $150 output per MTok
- Fast mode (>200K): $60 input / $225 output per MTok
- Limited-time 50% discount for all plans until February 16, 2026
- Compatible with 1M token extended context window

> "Fast mode is not a different model. It uses the same Opus 4.6 with a different API configuration that prioritizes speed over cost efficiency. You get identical quality and capabilities, just faster responses."

## Behavior Changes

### **Fast Mode Context Repricing**
Switching to fast mode mid-conversation has cost implications:

> "When you switch into fast mode mid-conversation, you pay the full fast mode uncached input token price for the entire conversation context. This costs more than if you had enabled fast mode from the start."

This encourages users to decide on fast mode at session start rather than toggling mid-stream.

### **Model Persistence After Disabling**
When disabling fast mode, the behavior differs from typical mode toggles:

> "When you disable fast mode with `/fast` again, you remain on Opus 4.6. The model does not revert to your previous model. To switch to a different model, use `/model`."

## Hidden Gems

### **Automatic Rate Limit Fallback**
Fast mode includes intelligent degradation handling:

> "Fast mode has separate rate limits from standard Opus 4.6. When you hit the fast mode rate limit or run out of extra usage credits: 1. Fast mode automatically falls back to standard Opus 4.6 2. The `↯` icon turns gray to indicate cooldown 3. You continue working at standard speed and pricing 4. When the cooldown expires, fast mode automatically re-enables"

This suggests sophisticated rate limiting infrastructure that can dynamically switch configurations without interrupting user workflow.

### **Fast Mode vs Effort Level Combinations**
The documentation reveals you can stack optimizations:

> "You can combine both: use fast mode with a lower [effort level](/en/model-config#adjust-effort-level) for maximum speed on straightforward tasks."

This implies fast mode is orthogonal to the existing effort level system - opening up interesting optimization strategies.

### **Third-Party Cloud Provider Limitations**
An important restriction revealed:

> "Not available on third-party cloud providers: fast mode is not available on Amazon Bedrock, Google Vertex AI, or Microsoft Azure Foundry. Fast mode is available through the Anthropic Console API and for Claude subscription plans using extra usage."

This suggests fast mode requires specific Anthropic infrastructure that isn't available through partner cloud providers.

## Technical Details

### **Requirements & Access Control**
Fast mode has specific enablement requirements:

- **Extra usage required**: Must be enabled in billing settings
- **Teams/Enterprise gating**: Admins must explicitly enable fast mode
  - Console API customers: [Claude Code preferences](https://platform.claude.com/claude-code/preferences)
  - Teams/Enterprise: [Admin Settings > Claude Code](https://claude.ai/admin-settings/claude-code)
- **Usage billing**: Fast mode tokens billed to extra usage immediately, don't count against plan's included usage
- **Organization controls**: Admins can disable for entire organizations

> "If your admin has not enabled fast mode for your organization, the `/fast` command will show 'Fast mode has been disabled by your organization.'"

### **Recommended Use Cases**
The documentation provides clear guidance on when to use each mode:

**Fast mode best for:**
- Rapid iteration on code changes
- Live debugging sessions
- Time-sensitive work with tight deadlines

**Standard mode better for:**
- Long autonomous tasks where speed matters less
- Batch processing or CI/CD pipelines
- Cost-sensitive workloads

### **Research Preview Status**
Important caveat for production users:

> "Fast mode is a research preview feature. This means: The feature may change based on feedback, Availability and pricing are subject to change, The underlying API configuration may evolve"

## New Documentation Pages

### `docs/claude-code/en/fast-mode.md`
A comprehensive 131-line guide covering:
- How to toggle fast mode on/off
- Detailed cost tradeoff analysis
- Decision framework for when to use fast mode
- Requirements and access control
- Rate limit behavior and automatic fallback
- Comparison with effort level adjustments
- Organization admin enablement instructions

This is a fully-fledged feature launch with complete documentation, not just an experimental add-on.

## Integration Notes

The `/fast` command is available in both:
- Claude Code CLI (primary focus of this documentation)
- Claude Code VS Code Extension

This suggests coordinated feature rollout across the entire Claude Code ecosystem.

---
*Generated from Claude Code CLI documentation changes detected on February 7, 2026*

*Total pages in documentation: 55 (up from 54)*
