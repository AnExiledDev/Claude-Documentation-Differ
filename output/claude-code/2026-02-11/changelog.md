# Claude Code CLI Documentation Changes - February 11, 2026

## TL;DR
Two significant updates today: Anthropic added **server-managed settings** for centralized enterprise configuration and expanded Chrome integration to support **Microsoft Edge**. Server-managed settings enable Teams/Enterprise admins to push configurations without MDM, while Edge support broadens browser automation options for all users.

## New Features & Capabilities

### **Server-Managed Settings (Public Beta)**
A major new enterprise feature allowing administrators to centrally configure Claude Code through Claude.ai's web interface, without requiring device management infrastructure.

> "Server-managed settings allow administrators to centrally configure Claude Code through a web-based interface on Claude.ai. Claude Code clients automatically receive these settings when users authenticate with their organization credentials."

**Key capabilities:**
- **Web-based configuration**: Manage settings through Claude.ai admin console (Admin Settings > Claude Code > Managed settings)
- **Automatic delivery**: Settings pushed to clients at startup and hourly polling
- **Zero infrastructure**: No MDM or endpoint management required
- **Teams & Enterprise only**: Requires Claude Code 2.1.30 or later
- **Network requirement**: Direct connection to `api.anthropic.com`

**Configuration precedence:**
> "When both are present, server-managed settings take precedence and the local `managed-settings.json` file is not used."

This means server-managed settings outrank even endpoint-managed settings deployed via MDM.

### **Microsoft Edge Support for Browser Integration**
The Chrome integration feature (previously Chrome-only) now works with Microsoft Edge. Claude Code can control and automate tasks in Edge using the same Claude in Chrome extension, which is available in the Chrome Web Store for both browsers.

> "Chrome integration is in beta and currently works with Google Chrome and Microsoft Edge."

Requirements now include:
> "Google Chrome or Microsoft Edge browser"
>
> "Claude in Chrome extension version 1.0.36 or higher, available in the Chrome Web Store for both browsers"

**What this means:**
- Users who prefer Edge over Chrome can now use Claude Code's browser automation features
- Cross-platform support: Edge works on macOS, Linux, and Windows (same as Chrome)
- Same extension, multiple browsers via Chrome Web Store
- Other Chromium browsers (Brave, Arc) remain unsupported

### **Security Approval Dialogs**
New security mechanism for potentially dangerous settings:

> "Certain settings that could pose security risks require explicit user approval before being applied:
> * Shell command settings: settings that execute shell commands
> * Custom environment variables: variables not in the known safe allowlist
> * Hook configurations: any hook definition"

Users must approve these settings before Claude Code proceeds. In non-interactive mode (`-p` flag), settings apply without approval.

### **Audit Logging for Settings Changes**
> "Audit log events for settings changes are available through the compliance API or audit log export. Contact your Anthropic account team for access."

This suggests enterprise-grade compliance tracking is now available for configuration changes.

## Behavior Changes

### **Fast Mode Performance Specification**
Fast mode documentation now includes concrete performance metrics:

- **Before**: "Fast mode delivers faster Opus 4.6 responses"
- **After**: "Fast mode is a high-speed configuration for Claude 4.6, making the model 2.5x faster"

This clarifies that fast mode achieves a 2.5x speedup through API configuration changes, not model differences.

### **Settings Hierarchy Enhancement**
The settings precedence documentation now explicitly mentions both managed settings approaches:

- **Before**: "Managed settings (`managed-settings.json`)"
- **After**: "Managed settings ([`managed-settings.json`](/en/permissions#managed-settings) or [server-managed settings](/en/server-managed-settings))"

This confirms that both approaches occupy the same tier in the settings hierarchy, with server-managed taking precedence when both exist.

## Hidden Gems

### **Caching Behavior Window**
The documentation reveals a security consideration for first-launch scenarios:

> "First launch without cached settings:
> * Claude Code fetches settings asynchronously
> * If the fetch fails, Claude Code continues without managed settings
> * There is a brief window before settings load where restrictions are not yet enforced"

This suggests there's a race condition on first launch where managed settings haven't loaded yet. Organizations with strict security requirements should be aware of this window.

### **Plugin Marketplace Restrictions**
A note in the settings documentation hints at plugin marketplace controls:

> "Managed deployments can also restrict **plugin marketplace additions** using..."

While the full sentence is cut off in the diff, this reveals that plugin marketplace access can be centrally controlled—an undocumented capability for enterprise deployments.

### **Tamper Resistance Model**
The security considerations section provides frank disclosure about client-side limitations:

> "Server-managed settings provide centralized policy enforcement, but they operate as a client-side control. On unmanaged devices, users with admin or sudo access can modify the Claude Code binary, filesystem, or network configuration."

This is notable for its honesty about the threat model. The documentation explicitly describes scenarios like cached file tampering, file deletion, and API unavailability.

### **Third-Party Provider Bypass**
Important limitation for organizations using alternative infrastructure:

> "Platform availability: Server-managed settings require a direct connection to `api.anthropic.com` and are not available when using third-party model providers:
> * Amazon Bedrock
> * Google Vertex AI
> * Microsoft Foundry
> * Custom API endpoints via `ANTHROPIC_BASE_URL` or LLM gateways"

This means organizations using Bedrock/Vertex cannot use server-managed settings and must rely on endpoint-managed configurations.

## New Documentation Pages

### **`server-managed-settings.md`**
A comprehensive 162-line documentation page covering:
- Requirements and setup instructions
- Comparison table between server-managed and endpoint-managed approaches
- Step-by-step configuration guide with JSON examples
- Settings delivery behavior (fetch, caching, polling)
- Security approval dialog specifications
- Platform availability and limitations
- Audit logging capabilities
- Security threat model analysis

The page includes practical examples like enforcing permission deny lists for sensitive files (`.env`, secrets directories) combined with `disableBypassPermissionsMode`.

## Technical Details

### **Server-Managed Settings**
**Version Requirements:**
- Minimum version: Claude Code 2.1.30
- Network requirement: Direct access to `api.anthropic.com`
- Plan requirement: Claude for Teams or Claude for Enterprise

**Polling and Update Behavior:**
- Settings fetched at startup
- Hourly polling during active sessions
- Most settings apply automatically without restart
- OpenTelemetry configuration requires full restart

**Role-Based Access Control:**
Only these roles can manage server-managed settings:
- Primary Owner
- Owner

**Current Beta Limitations:**
- Uniform application to all users (no per-group configurations yet)
- MCP server configurations cannot be distributed via server-managed settings

**Managed-Only Settings Support:**
Server-managed settings support all regular settings plus managed-only settings like:
- `disableBypassPermissionsMode`
- Permission deny lists
- Shell command restrictions

### **Edge Native Messaging Host Configuration**

Edge-specific paths for the native messaging host configuration file that enables communication between Claude Code and the browser:

**macOS**:
- Chrome: `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
- Edge: `~/Library/Application Support/Microsoft Edge/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`

**Linux**:
- Chrome: `~/.config/google-chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
- Edge: `~/.config/microsoft-edge/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`

**Windows Registry**:
- Chrome: `HKCU\Software\Google\Chrome\NativeMessagingHosts\`
- Edge: `HKCU\Software\Microsoft\Edge\NativeMessagingHosts\`

These paths are useful for troubleshooting connection issues between Claude Code and the browser extension.

**Browser Requirements:**
- Minimum required versions: extension v1.0.36+, Claude Code v2.0.73+
- Direct Anthropic plan (Pro, Max, Team, or Enterprise) required
- WSL (Windows Subsystem for Linux) not supported

---
*Generated from Claude Code CLI documentation changes detected on February 11, 2026*
