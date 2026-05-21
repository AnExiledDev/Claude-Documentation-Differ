# Documentation Diff Report

**Comparing:** `7173cf90fde7b6096c959cbd3e7fd59673ae391e` → `HEAD`
**Generated:** 2026-05-21T23:01:18.749262+00:00

## Summary

- New pages: 2
- Removed pages: 0
- Modified pages: 13

## New Pages

- `docs/claude-code/en/managed-mcp.md`
- `docs/claude-code/en/sandbox-environments.md`

## Modified Pages

### `docs/claude-code/en/admin-setup.md`

+12 / -12 lines

### `docs/claude-code/en/auto-mode-config.md`

+1 / -1 lines

### `docs/claude-code/en/changelog.md`

+32 / -13 lines

### `docs/claude-code/en/desktop.md`

+1 / -1 lines

### `docs/claude-code/en/devcontainer.md`

+1 / -0 lines

### `docs/claude-code/en/glossary.md`

+1 / -1 lines

### `docs/claude-code/en/mcp.md`

+1 / -227 lines

**Removed sections:**
- ### Option 1: Exclusive control with managed-mcp.json
- ### Option 2: Policy-based control with allowlists and denylists
- #### Restriction options
- #### Example configuration
- #### How command-based restrictions work
- #### How URL-based restrictions work
- #### Allowlist behavior (`allowedMcpServers`)
- #### Denylist behavior (`deniedMcpServers`)
- #### Important notes

### `docs/claude-code/en/permission-modes.md`

+2 / -2 lines

### `docs/claude-code/en/permissions.md`

+2 / -2 lines

### `docs/claude-code/en/sandboxing.md`

+211 / -177 lines

**New sections:**
- # Configure the sandboxed Bash tool
- ## Get started
- ### Set up Linux and WSL2
- ## Configure sandboxing
- ## How sandboxing works
- ### Filesystem isolation
- ### Network isolation
- ### OS-level enforcement
- ## How sandboxing relates to permissions and permission modes
- ### Permission rules
- ### Permission modes
- ## Configure the sandbox for your organization
- ### Enforce sandboxing with managed settings
- ### Keep developers from widening the policy
- ## Troubleshooting
- ## Limitations
- ### Security limitations
- ### Platform and tool compatibility
- ### Scope

**Removed sections:**
- # Sandboxing
- ## Overview
- ## Why sandboxing matters
- ## How it works
- ### Filesystem isolation
- ### Network isolation
- ### OS-level enforcement
- ## Getting started
- ### Prerequisites
- ### Enable sandboxing
- ### Configure sandboxing
- #### Granting subprocess write access to specific paths
- ## Security benefits
- ### Protection against prompt injection
- ### Reduced attack surface
- ### Transparent operation
- ## Security Limitations
- ## How sandboxing relates to permissions
- ## Advanced usage
- ### Integration with existing security tools
- ## Best practices
- ## Open source
- ## Limitations
- ## What sandboxing does not cover

### `docs/claude-code/en/security.md`

+6 / -5 lines

### `docs/claude-code/en/server-managed-settings.md`

+1 / -1 lines

### `docs/claude-code/en/settings.md`

+10 / -10 lines
