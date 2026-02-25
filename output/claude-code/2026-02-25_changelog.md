# Claude Code Documentation Changes — 2026-02-25

## Summary

Two pages were updated in this diff. The plugin marketplaces page gains full npm package support — a feature previously flagged as "not yet fully implemented" — and adds a git timeout troubleshooting entry. The settings page documents four new environment variables: three for SDK-caller account identity injection and one to configure the plugin git operation timeout.

## Significant Changes

### Plugin Support

- **npm packages now fully supported as a plugin source**: The `"source": "npm"` source type is now documented as production-ready. The previous validation warning — `Plugin "x" uses npm source which is not yet fully implemented: use github or local path sources instead` — has been removed from the troubleshooting section. Plugins can be installed from the public npm registry or any private/internal registry.

  > Plugins distributed as npm packages are installed using `npm install`. This works with any package on the public npm registry or a private registry your team hosts.

  The `npm` source supports three fields:

  | Field      | Required | Description |
  |:-----------|:---------|:------------|
  | `package`  | Yes      | Package name or scoped package (e.g. `@org/plugin`) |
  | `version`  | No       | Version or range (e.g. `2.1.0`, `^2.0.0`, `~1.5.0`) |
  | `registry` | No       | Custom registry URL; defaults to the system npm registry (typically npmjs.org) |

  Example using version pinning and a private registry:
  ```json
  {
    "name": "my-npm-plugin",
    "source": {
      "source": "npm",
      "package": "@acme/claude-plugin",
      "version": "^2.0.0",
      "registry": "https://npm.example.com"
    }
  }
  ```

  - *Implication*: Teams can now distribute Claude Code plugins through npm, including scoped packages on private registries. Standard npm versioning and publishing workflows apply.
  - *Source*: [plugin-marketplaces.md](https://code.claude.com/docs/en/plugin-marketplaces.md)

### Configuration — New Environment Variables

- **`CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`**: Sets the timeout (in milliseconds) for git operations during plugin installation and marketplace updates. Default is 120,000ms (120 seconds).

  > **Cause**: Claude Code uses a 120-second timeout for all git operations, including cloning plugin repositories and pulling marketplace updates. Large repositories or slow network connections may exceed this limit.
  >
  > **Solution**: Increase the timeout using the `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` environment variable. The value is in milliseconds:
  > ```bash
  > export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000  # 5 minutes
  > ```

  - *Implication*: Teams using large plugin repositories or operating on slow/high-latency networks can now tune past installation timeouts without restructuring their repositories.
  - *Source*: [settings.md](https://code.claude.com/docs/en/settings.md)

- **SDK caller account identity variables** (`CLAUDE_CODE_ACCOUNT_UUID`, `CLAUDE_CODE_ORGANIZATION_UUID`, `CLAUDE_CODE_USER_EMAIL`): Three new environment variables that allow SDK callers to inject account identity synchronously at process startup. All three must be set together.

  > Used by SDK callers to provide account information synchronously, avoiding a race condition where early telemetry events lack account metadata.

  | Variable | Description |
  |:---------|:------------|
  | `CLAUDE_CODE_ACCOUNT_UUID` | Account UUID for the authenticated user. Requires the other two variables to also be set. |
  | `CLAUDE_CODE_ORGANIZATION_UUID` | Organization UUID for the authenticated user. Requires the other two variables to also be set. |
  | `CLAUDE_CODE_USER_EMAIL` | Email address for the authenticated user. Requires the other two variables to also be set. |

  - *Implication*: SDK integrations that emit telemetry before async authentication completes can now pre-populate account metadata to avoid gaps in early telemetry events. All three variables must be provided; setting only one or two has no effect.
  - *Source*: [settings.md](https://code.claude.com/docs/en/settings.md)

## Notable Details

- The removal of the `Plugin "x" uses npm source which is not yet fully implemented` validation warning is a behavior change: plugin configs that previously triggered this warning will no longer do so. Any workarounds in place to avoid npm-sourced plugins can be removed.
- The three SDK account identity variables are explicitly described as fixing a **race condition** in telemetry — a precise problem statement suggesting these were added in response to observed data gaps in SDK deployments, not as a general feature.
- `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` is cross-referenced in both modified files: it appears as the recommended solution in the new `plugin-marketplaces.md` troubleshooting section and is listed in the environment variable reference table in `settings.md`.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `plugin-marketplaces.md` | Modified | +59 / -1 | Added npm plugin source type with version pinning and private registry support; removed "not yet implemented" warning; added Git timeout troubleshooting section |
| `settings.md` | Modified | +4 / -0 | Added `CLAUDE_CODE_ACCOUNT_UUID`, `CLAUDE_CODE_ORGANIZATION_UUID`, `CLAUDE_CODE_USER_EMAIL`, and `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` environment variables |

---
*Generated from Claude Code CLI documentation changes detected on 2026-02-25*
