# Claude Code CLI Documentation Changes - February 9, 2026

## TL;DR
The documentation now explicitly acknowledges that custom environment images and snapshots are **not yet supported** in Claude Code on the web, clarifying that SessionStart hooks are the current workaround. New sections detail specific limitations including proxy compatibility issues with Bun, network access requirements, and performance considerations for hooks that run on every session start.

## Behavior Changes

### **Dependency Management**: From Feature to Workaround
The framing of dependency management in remote environments has shifted significantly:

- **Before**: Presented as a straightforward feature using SessionStart hooks
- **After**: Now explicitly labeled as a workaround with known limitations

> Custom environment images and snapshots are not yet supported. As a workaround, you can use SessionStart hooks to install packages when a session starts. This approach has known limitations.

**Implications**: This suggests custom environment images/snapshots are planned features that will eventually provide a better solution than the current hook-based approach.

### **Hook Execution Scope**: Clarification on Local vs Remote

The documentation restructured how it explains controlling where hooks run:

- **Old approach**: Dedicated section "Local vs remote execution" with general guidance
- **New approach**: Integrated into "Dependency management limitations" with explicit acknowledgment that **there is no hook configuration to scope a hook to remote sessions only**

> There is no hook configuration to scope a hook to remote sessions only. To skip local execution, check the `CLAUDE_CODE_REMOTE` environment variable in your script

This is now positioned as a limitation rather than a feature, suggesting scoped hook configuration may be coming.

## Hidden Gems

### **Package Manager Proxy Incompatibility**
The documentation now explicitly calls out proxy compatibility issues:

> Some package managers do not work correctly with this proxy. Bun is a known example.

**What this reveals**:
- Claude Code on the web routes all traffic through a security proxy
- This proxy implementation has compatibility issues with certain tools
- The team is aware of specific failures (Bun) and may be tracking others
- Suggests the proxy is non-standard enough to break some HTTP clients

### **Network Access Tier System**
References to network access tiers ("No internet", "Limited", "Full") reveal a more granular security model:

> If your environment is configured with "No internet" access, these hooks will fail. Use "Limited" (the default) or "Full" network access.

**Interesting details**:
- Three distinct network access levels exist
- "Limited" is the default (not "No internet")
- The "Limited" tier includes a default allowlist with common registries (npm, PyPI, RubyGems, crates.io)

## Technical Details

### **New Environment Variable: `CLAUDE_ENV_FILE`**
While not new, the documentation now more prominently features this variable:

> SessionStart hooks can persist environment variables for subsequent Bash commands by writing to the file specified in the `CLAUDE_ENV_FILE` environment variable.

This enables hooks to set environment variables that survive beyond the hook execution.

### **Performance Consideration: Hook Startup Latency**
New guidance on optimizing hook performance:

> Hooks run each time a session starts or resumes, adding startup latency. Keep install scripts fast by checking whether dependencies are already present before reinstalling.

**Best practice revealed**: Check for existing dependencies before installing to avoid redundant work on session resume.

### **Example Script Update**
The example installation script was refined to show the recommended pattern:

```bash
#!/bin/bash
# Only run in remote environments
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

Notable: The comment changed from "Example: Only run in remote environments" to just "Only run in remote environments", making it clearer this is the recommended approach.

## Documentation Structure Changes

### **New Sections**
- **"Dependency management limitations"**: Dedicated section cataloging the constraints of the current hook-based approach
- **"Persist environment variables"**: Elevated from subsection to more prominent position with clearer guidance

### **Removed Sections**
- **"Local vs remote execution"**: Consolidated into the limitations section, repositioning this from a feature to a workaround consideration

## What This Tells Us

1. **Roadmap hints**: Custom environment images and snapshots are planned but not yet implemented
2. **Transparency shift**: The team is being more upfront about current limitations rather than presenting workarounds as full solutions
3. **Production learnings**: The specific callout of Bun and proxy issues suggests real-world user feedback
4. **Security architecture**: The network access tier system and security proxy indicate a sophisticated sandboxing approach for remote execution

---
*Generated from Claude Code CLI documentation changes detected on February 9, 2026*
