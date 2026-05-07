# Claude Code Documentation Changes — 2026-05-07

## Summary

Seven documentation pages were updated with no pages added or removed (+44/-13 lines total). The largest change introduces a new `gcpAuthRefresh` setting for automatic GCP credential refresh in the Google Vertex AI guide. Two new settings (`claudeMdExcludes` and `syntaxHighlightingDisabled`) are also documented, along with a new `force-for-plugin` output style frontmatter field for plugin authors.

## Significant Changes

### Google Vertex AI

- **New `gcpAuthRefresh` setting for automatic GCP credential refresh**: When Claude Code detects expired or unloadable GCP credentials, it now runs a configurable command to obtain fresh credentials before retrying the request.
  > Claude Code supports automatic credential refresh for GCP through the `gcpAuthRefresh` setting. When Claude Code detects that your GCP credentials are expired or cannot be loaded, it runs the configured command to obtain new credentials before retrying the request.

  Example configuration in settings:
  ```json
  {
    "gcpAuthRefresh": "gcloud auth application-default login",
    "env": {
      "ANTHROPIC_VERTEX_PROJECT_ID": "your-project-id"
    }
  }
  ```
  > The command's output is displayed to the user, but interactive input isn't supported. This works well for browser-based authentication flows where the CLI shows a URL and you complete authentication in the browser. The refresh command times out after three minutes if authentication does not complete. If you set `gcpAuthRefresh` in project settings such as `.claude/settings.json`, the command runs only after you accept the workspace trust prompt.
  - *Implication*: Removes the need to manually re-authenticate mid-session when GCP credentials expire. Works with `gcloud`'s browser-based flow. Three-minute timeout and workspace trust restriction are important operational details.
  - *Source*: [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai.md)

- **Clarified `ANTHROPIC_VERTEX_PROJECT_ID` precedence**: The project ID resolution order is now explicitly documented — `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT`, and the credential file referenced by `GOOGLE_APPLICATION_CREDENTIALS` all take precedence over `ANTHROPIC_VERTEX_PROJECT_ID`. If none are set, the project ID falls back to the `gcloud` configuration or the attached service account.
  > Claude Code uses `ANTHROPIC_VERTEX_PROJECT_ID` as the project ID for Vertex AI requests. The `GCLOUD_PROJECT` and `GOOGLE_CLOUD_PROJECT` environment variables and the credential file referenced by `GOOGLE_APPLICATION_CREDENTIALS` take precedence over it. If none of these are set, the project ID is resolved from your `gcloud` configuration or the attached service account.
  - *Implication*: Teams already using standard GCP environment variables don't need `ANTHROPIC_VERTEX_PROJECT_ID`; it now has the lowest priority in the resolution chain.
  - *Source*: [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai.md), [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **New "Could not load the default credentials" troubleshooting entry**: The troubleshooting section now includes specific guidance for this common GCP authentication error, pointing to `gcloud auth application-default login`, `GOOGLE_APPLICATION_CREDENTIALS`, and the credential configuration section.
  - *Source*: [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai.md)

### Settings

- **New `claudeMdExcludes` setting**: Allows specifying glob patterns or absolute paths of `CLAUDE.md` files to skip during memory loading. Patterns match against absolute file paths. Applies only to user, project, and local memory — managed policy files cannot be excluded.
  > Glob patterns or absolute paths of `CLAUDE.md` files to skip when loading memory. Patterns match against absolute file paths. Only applies to user, project, and local memory; managed policy files cannot be excluded.
  - *Implication*: Solves a practical problem for monorepos and projects with vendor directories that contain their own `CLAUDE.md` files. The default example (`["**/vendor/**/CLAUDE.md"]`) signals the intended use case.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

- **New `syntaxHighlightingDisabled` setting**: Disables syntax highlighting globally across diffs, code blocks, and file previews. This is broader than the existing `CLAUDE_CODE_SYNTAX_HIGHLIGHT=false` env var, which only affects diff output.
  > To also disable highlighting in code blocks and file previews, use the [`syntaxHighlightingDisabled`](/en/settings) setting.
  - *Implication*: Developers who previously used `CLAUDE_CODE_SYNTAX_HIGHLIGHT=false` for complete highlighting suppression now have a persistent setting-level alternative. The env var retains its narrower scope (diffs only).
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md), [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

- **New `gcpAuthRefresh` setting entry**: Formally documented in the settings reference alongside a link to the Vertex AI advanced credential configuration section.
  > Custom script that refreshes GCP Application Default Credentials when they expire or cannot be loaded.
  - *Source*: [Settings](https://code.claude.com/docs/en/settings.md)

### Output Styles

- **New `force-for-plugin` frontmatter field**: Plugin-shipped output styles can now declare themselves as automatic — applied whenever the plugin is enabled, without requiring users to manually select the style. Overrides the user's `outputStyle` setting.
  > `force-for-plugin`: Plugin output styles only: apply this style automatically whenever the plugin is enabled, without requiring users to select it. Overrides the user's `outputStyle` setting. If multiple enabled plugins set this, the first one loaded wins.
  - *Implication*: Plugin authors can now enforce a specific output style as part of their plugin experience. When multiple plugins declare `force-for-plugin`, load order determines which wins — plugin authors and users should be aware of this conflict behavior.
  - *Source*: [Output Styles](https://code.claude.com/docs/en/output-styles.md)

- **Output style file locations expanded to three levels**: The documentation now lists a third location — managed policy (`.claude/output-styles` inside the managed settings directory) — alongside user (`~/.claude/output-styles`) and project (`.claude/output-styles`).
  - *Implication*: Enterprise administrators can now deploy organization-wide output styles via the managed settings directory.
  - *Source*: [Output Styles](https://code.claude.com/docs/en/output-styles.md)

### Memory

- **Hooks guidance added to CLAUDE.md troubleshooting**: The memory debugging section now explicitly redirects users from `CLAUDE.md` to hooks for lifecycle-bound instructions (e.g., before every commit, after each file edit).
  > If the instruction is something that must run at a specific point, such as before every commit or after each file edit, write it as a [hook](/en/hooks-guide) instead. Hooks execute as shell commands at fixed lifecycle events and apply regardless of what Claude decides to do.
  - *Implication*: Addresses a common misuse pattern — `CLAUDE.md` instructions are best-effort suggestions to Claude; hooks guarantee deterministic execution at lifecycle events.
  - *Source*: [Memory](https://code.claude.com/docs/en/memory.md)

### MCP

- **Enterprise MCP deployment cross-reference added**: The MCP installation scopes introduction now notes that administrators can deploy servers at the enterprise level via managed configuration.
  > Administrators can also deploy servers at the enterprise level via [managed configuration](#managed-mcp-configuration).
  - *Implication*: Small discoverability improvement for enterprise admins reading the scopes section who may not have found the managed configuration subsection.
  - *Source*: [MCP](https://code.claude.com/docs/en/mcp.md)

### Plugin Discovery

- **`.git` suffix required for non-GitHub git URLs**: The documentation now explicitly states that when adding a plugin from a non-GitHub Git host using a full URL, the `.git` suffix must be included so Claude Code clones the repository rather than treating the URL as a direct link to a hosted `marketplace.json` file.
  > Add any git repository by providing the full URL. This works with any Git host, including GitLab, Bitbucket, and self-hosted servers. Include the `.git` suffix so Claude Code clones the repository rather than treating the URL as a direct link to a hosted `marketplace.json` file.
  - *Implication*: Without `.git`, Claude Code interprets the URL as pointing to a `marketplace.json` file directly. This was likely a silent failure mode for GitLab/Bitbucket/self-hosted plugin installs before this fix.
  - *Source*: [Discover Plugins](https://code.claude.com/docs/en/discover-plugins.md)

## Notable Details

- The `gcpAuthRefresh` setting and the clarified `ANTHROPIC_VERTEX_PROJECT_ID` precedence are directly linked — both reflect the same underlying GCP credential resolution refactor, where `ANTHROPIC_VERTEX_PROJECT_ID` is now the lowest-priority project ID source rather than the only one.
- `syntaxHighlightingDisabled` (setting) and `CLAUDE_CODE_SYNTAX_HIGHLIGHT=false` (env var) now have explicitly different scopes: the env var covers diff output only; the setting covers diffs, code blocks, and file previews. Both remain supported.
- The `force-for-plugin` field defaults to `false`, meaning existing plugin output styles are unaffected unless plugin authors explicitly opt in.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| google-vertex-ai.md | Modified | +22/-1 | New `gcpAuthRefresh` credential refresh section; clarified project ID precedence; new troubleshooting entry for default credential errors |
| output-styles.md | Modified | +13/-8 | New `force-for-plugin` frontmatter field; managed policy added as third output style file location |
| settings.md | Modified | +3/-0 | Documented `claudeMdExcludes`, `gcpAuthRefresh`, and `syntaxHighlightingDisabled` settings |
| memory.md | Modified | +2/-0 | Added hooks cross-reference in CLAUDE.md troubleshooting guidance |
| env-vars.md | Modified | +2/-2 | Clarified `ANTHROPIC_VERTEX_PROJECT_ID` precedence; added `syntaxHighlightingDisabled` cross-reference to `CLAUDE_CODE_SYNTAX_HIGHLIGHT` |
| mcp.md | Modified | +1/-1 | Added enterprise managed configuration cross-reference in scopes section |
| discover-plugins.md | Modified | +1/-1 | Clarified `.git` suffix requirement for non-GitHub git host plugin URLs |

---
*Generated from Claude Code CLI documentation changes detected on 2026-05-07*
