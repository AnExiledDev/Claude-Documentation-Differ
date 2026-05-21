# Claude API Documentation Changes — 2026-05-21

## Summary

Eight new documentation pages introduce MCP Tunnels, a beta (Research Preview) feature for connecting Claude to MCP servers running in private networks via outbound-only Cloudflare tunnels, without exposing inbound firewall ports. Alongside this, existing tool documentation received substantial updates: the Agent Skills quickstart was rewritten with multi-SDK examples, the computer use tool got a new agent loop implementation, and the `define-tools` guide documents a new `input_examples` field. Web search and web fetch tools also document support for a new model (Claude Mythos Preview).

---

## Significant Changes

### MCP Tunnels (New Beta Feature)

- **New MCP Tunnels feature — connect Claude to private MCP servers**: Eight new pages document the full MCP Tunnels system, a beta (Research Preview) that enables Claude to reach MCP servers inside private networks through an outbound-only encrypted tunnel. Traffic flows through Cloudflare's network as a transport; Anthropic's proxy component terminates inner TLS so Cloudflare cannot read payloads. No inbound ports need to be opened.

  > "MCP tunnels let you connect Claude to Model Context Protocol (MCP) servers that run inside your private network. Traffic flows over an outbound-only connection, so you don't need to open inbound firewall ports, expose services to the public internet, or allowlist Anthropic's IP ranges on your origin."

  Key facts:
  - **Beta header** (Tunnels Admin API): `anthropic-beta: mcp-tunnels-2026-05-19`
  - **MCP connector beta header** (Messages API): `anthropic-beta: mcp-client-2025-11-20`
  - **Tunnels API auth**: Requires `Bearer` token with `org:manage_tunnels` scope obtained via [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation); Admin API keys are not accepted.
  - **Limit**: Up to 10 active tunnels per organization; up to 2 active CA certificates per tunnel (allows zero-downtime rotation).
  - **Deployment options**: Helm (Kubernetes) or Docker Compose; both support programmatic access (WIF) or manual credential supply.
  - **Architecture**: Two components run inside your network — `cloudflared` (tunnel agent, outbound-only) and a proxy image (`mcp-proxy`) that terminates inner TLS and routes to upstream MCP servers.
  - **Network requirements**: `api.anthropic.com:443` for provisioning; Cloudflare tunnel edge `198.41.192.0/19` / `2606:4700:a0::/44` on port 7844 for the running tunnel.
  - **ZDR/HIPAA eligibility**: Separate page required; see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).
  - *Implication*: Developers can now expose private/internal MCP servers to Claude without making them publicly accessible. Production deployments should use the Helm or Docker Compose guides, not the local quickstart.
  - *Source*: [MCP tunnels overview](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview.md)

- **Tunnels API beta header and certificate spec**: The Reference page documents required headers for all Tunnels API calls and strict CA/server certificate requirements.

  > "All MCP tunnels endpoints require a bearer token with the `org:manage_tunnels` scope obtained through Workload Identity Federation. Admin API keys are not accepted."

  Certificate requirements for self-issued PKI:
  - CA certificate: PEM-encoded, `BasicConstraints` with `CA:TRUE` (critical), `SubjectKeyIdentifier`, `KeyUsage` including `keyCertSign`, RSA 2048+ or ECDSA P-256+.
  - Server certificate: wildcard SAN `*.<tunnel-domain>` covers all routes; must be signed directly by a registered CA (no intermediates); 90-day validity recommended.
  - *Implication*: Developers managing their own PKI must follow these exact requirements; the `mcp-proxy` `setup` binary generates compliant certs automatically for programmatic deployments.
  - *Source*: [MCP tunnels reference](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/reference.md)

### Agent Skills

- **Agent Skills quickstart — major rewrite with multi-SDK examples**: The quickstart was substantially rewritten (+1169/-283 lines), adding full code examples in Python, TypeScript, C#, Go, Java, and CLI for every step. A new **Step 1** now shows how to list available Anthropic-managed Skills using the Skills API before creating a message.

  > ```python
  > # List Anthropic-managed Skills
  > skills = client.beta.skills.list(source="anthropic")
  > for skill in skills.data:
  >     print(f"{skill.id}: {skill.display_title}")
  > ```

  File ID extraction was also updated: the previous approach used `jq` and `--transform` CLI flags; the current approach explicitly handles both `python` and `bash` code-execution tool result types in application code.
  - *Implication*: Developers building against the Skills API now have complete, copy-pasteable SDK examples; the `beta: skills-2025-10-02` header is required.
  - *Source*: [Agent Skills quickstart](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart.md)

### Tool Use

- **`input_examples` field added to tool definitions**: The `define-tools` page now documents an optional `input_examples` array field on tool definitions, providing concrete example inputs to help Claude understand how to call complex tools correctly.

  > "Add an optional `input_examples` field to your tool definition with an array of example input objects. Each example must be valid according to the tool's `input_schema`."

  Example:
  ```json
  {
    "name": "get_weather",
    "input_schema": { ... },
    "input_examples": [
      {"location": "San Francisco, CA", "unit": "fahrenheit"},
      {"location": "Tokyo, Japan", "unit": "celsius"}
    ]
  }
  ```
  The page also now explicitly mentions `defer_loading` and `allowed_callers` as optional tool definition properties (pointing to the Tool reference for full details).
  - *Implication*: Developers with tools that have nested objects, optional parameters, or format-sensitive inputs can now provide schema-validated examples directly in the tool definition rather than relying on description alone.
  - *Source*: [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools.md)

- **Bash tool — added multi-SDK quick start examples**: The bash tool page was expanded (+138 lines) to include quick start code examples across all major SDKs: Python, TypeScript, C#, Go, Java, PHP, Ruby, and CLI. Tool type `bash_20250124` is demonstrated across all examples.
  - *Implication*: Developers can now copy working bash tool boilerplate for any supported SDK.
  - *Source*: [Bash tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool.md)

- **Computer use tool — agent loop and display scaling code rewritten**: The computer use documentation received a major update (+1645/-218 lines). The agent loop implementation now follows a clearer pattern with explicit history management, and new code sections document display scaling (resizing screenshots before sending to Claude, then scaling coordinates back up).

  > "# When capturing screenshot\n# Resize image to scaled dimensions before sending to Claude\n# When handling Claude's coordinates, scale them back up"

  Beta headers documented:
  - `computer-use-2025-11-24` — for Claude Opus 4.7, Opus 4.6, Sonnet 4.6, Opus 4.5
  - `computer-use-2025-01-24` — for Claude Sonnet 4.5, Haiku 4.5, Opus 4.1, Sonnet 4 (deprecated), Opus 4 (deprecated)
  - *Implication*: The new agent loop pattern is cleaner for production use; the display scaling guidance is important for correctly interpreting screen coordinates on high-DPI displays.
  - *Source*: [Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md)

- **Web search tool — Claude Mythos Preview support added**: The web search documentation now lists [Claude Mythos Preview](https://anthropic.com/glasswing) as a supported model for the `web_search_20260209` tool version (with dynamic filtering). A new note clarifies Mythos Preview availability by platform.

  > "The latest web search tool version (`web_search_20260209`) supports dynamic filtering with Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6."

  > "For Claude Mythos Preview, web search is supported on the Claude API, Microsoft Foundry, and Vertex AI. Web search is not available for Mythos Preview on Amazon Bedrock or Claude Platform on AWS."
  - *Implication*: Developers using Mythos Preview can now use `web_search_20260209` with dynamic filtering; note the Bedrock/AWS Platform exclusion.
  - *Source*: [Web search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool.md)

- **Web fetch tool — Claude Mythos Preview support added**: Similarly, the web fetch page now includes Mythos Preview in the supported model list for `web_fetch_20260209`, with a platform availability note.

  > "The latest web fetch tool version (`web_fetch_20260209`) supports dynamic filtering with Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6."

  > "For Claude Mythos Preview, web fetch is available on the Claude API and Microsoft Foundry. It is not currently available for Mythos Preview on Amazon Bedrock or Vertex AI."
  - *Implication*: Mythos Preview fetch support is more restricted than web search (no Vertex AI); developers should check the notes carefully when targeting specific platforms.
  - *Source*: [Web fetch tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md)

- **Code execution tool — model compatibility table updated**: Minor model additions, including Mythos Preview support for `code_execution_20260120` and a clarification that code execution is **free** when used alongside `web_search_20260209` or `web_fetch_20260209`.

  > "Code execution is free when used with web search or web fetch. When `web_search_20260209` or `web_fetch_20260209` is included in your request, there are no additional charges for code execution tool calls beyond the standard input and output token costs."
  - *Implication*: Using the latest web search or web fetch tool versions removes the extra cost of code execution, which Claude uses internally for dynamic filtering.
  - *Source*: [Code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md)

---

## Minor Changes

- **tool-use/overview.md**: Single-line change (+1/-1), likely a model identifier or minor wording update.

---

## New Pages

- **mcp-tunnels/overview.md** — Architecture, security model, network requirements, and usage instructions for the MCP Tunnels beta. [View](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview.md)
- **mcp-tunnels/quickstart.md** — Local Docker Compose quickstart for testing MCP tunnels with manual credentials and a sample FastMCP server. [View](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/quickstart.md)
- **mcp-tunnels/console.md** — Console UI guide: creating tunnels, registering CA certificates, retrieving tokens, and attaching tunneled servers to Managed Agent sessions. [View](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/console.md)
- **mcp-tunnels/deploy-helm.md** — Production Kubernetes deployment using the Anthropic Helm chart, with both programmatic (WIF) and manual credential flows. [View](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/deploy-helm.md)
- **mcp-tunnels/deploy-compose.md** — Production Docker Compose deployment on a VM, with both programmatic (WIF) and manual credential flows. [View](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/deploy-compose.md)
- **mcp-tunnels/reference.md** — Proxy configuration fields, Tunnels REST API reference, certificate requirements, and setup CLI (`setup init`, `setup renew-cert`) documentation. [View](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/reference.md)
- **mcp-tunnels/security.md** — Hardening guidance (OAuth on every server, `upstream.allowed_ips` restriction, image pinning), breach response steps, and tunnel teardown procedure. [View](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/security.md)
- **mcp-tunnels/troubleshooting.md** — Quick-reference table and debugging guide for connectivity, TLS, IP validation, and OAuth routing issues. [View](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/troubleshooting.md)

---

## Notable Details

- **MCP Tunnels Admin API beta header is date-versioned**: `anthropic-beta: mcp-tunnels-2026-05-19` — this is separate from the `mcp-client-2025-11-20` header used in Messages API calls to invoke tunneled MCP servers.
- **`setup renew-cert` supports `--renew-before` flag**: Setting `--renew-before=720h` makes the renewal command a no-op when more than 30 days remain — safe to run on a fixed cron schedule without unnecessary certificate churn.
- **Cloudflare receives limited metadata only**: The overview explicitly states Cloudflare sees egress IP, host fingerprint, connection timing, and byte volume — but not MCP request/response payloads, because inner TLS is terminated by the proxy using a certificate that only the deploying organization holds.
- **Tunnel token rotation is non-disruptive**: "Rotation does not sever cloudflared connections that are already established, so you can rotate, redeploy with the new value, and let the old connections drain."
- **`web_search_20260209` and `web_fetch_20260209` dynamic filtering requires code execution**: The note in web-search-tool.md confirms: "Dynamic filtering requires the code execution tool to be enabled."

---

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| mcp-tunnels/overview.md | New | SIGNIFICANT | — | MCP Tunnels beta overview: architecture, security model, API usage |
| mcp-tunnels/quickstart.md | New | SIGNIFICANT | — | Local Docker Compose quickstart for MCP Tunnels |
| mcp-tunnels/console.md | New | SIGNIFICANT | — | Console UI management for tunnels and certificates |
| mcp-tunnels/deploy-helm.md | New | SIGNIFICANT | — | Kubernetes/Helm deployment guide |
| mcp-tunnels/deploy-compose.md | New | SIGNIFICANT | — | Docker Compose production deployment guide |
| mcp-tunnels/reference.md | New | SIGNIFICANT | — | Proxy config, Tunnels API, cert requirements, setup CLI |
| mcp-tunnels/security.md | New | SIGNIFICANT | — | Hardening, breach response, teardown |
| mcp-tunnels/troubleshooting.md | New | SIGNIFICANT | — | Debugging guide with quick-reference table |
| agent-skills/quickstart.md | Modified | SIGNIFICANT | +1169/-283 | Major rewrite; multi-SDK examples; new Skills listing step |
| tool-use/computer-use-tool.md | Modified | SIGNIFICANT | +1645/-218 | New agent loop patterns; display scaling guidance; multi-SDK |
| tool-use/bash-tool.md | Modified | SIGNIFICANT | +138/-0 | Added multi-SDK quick start code examples |
| tool-use/define-tools.md | Modified | SIGNIFICANT | +42/-0 | New `input_examples` field documented |
| tool-use/web-fetch-tool.md | Modified | SIGNIFICANT | +11/-9 | Added Claude Mythos Preview support; platform availability note |
| tool-use/web-search-tool.md | Modified | SIGNIFICANT | +9/-7 | Added Claude Mythos Preview support; platform availability note |
| tool-use/code-execution-tool.md | Modified | SIGNIFICANT | +7/-5 | Model compatibility updates; free-with-web-tools pricing note |
| tool-use/overview.md | Modified | MINOR | +1/-1 | Minor wording or model reference update |

---

*Generated from Claude API documentation changes detected on 2026-05-21*
