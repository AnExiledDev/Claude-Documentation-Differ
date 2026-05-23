# Claude API Documentation Changes — 2026-05-23

## Summary

Eight pages in the agents-and-tools section were updated. The most substantial change is a major expansion of the fine-grained tool streaming page (+643/-100 lines), which adds complete code examples for six additional SDKs (C#, Go, Java, PHP, Ruby, and updated TypeScript/Python). Across all MCP tunnels documentation pages, the internal Docker Compose service name was renamed from `mcp-gateway` to `mcp-proxy`, and the feature label was lowercased from "Research Preview" to "research preview".

## Significant Changes

### Tool Use

- **Fine-Grained Tool Streaming — Expanded SDK Coverage**: The page now includes full working examples for C#, Go, Java, PHP, and Ruby in both the usage and accumulation sections. Previously only Python and TypeScript were covered. The `eager_input_streaming` property is demonstrated in each SDK's idiomatic style.
  > `Stream tool inputs without server-side JSON buffering for latency-sensitive applications.`
  - *Implication*: Developers using C#, Go, Java, PHP, or Ruby SDKs can now follow complete, copy-paste-ready examples rather than adapting Python/TypeScript code.
  - *Source*: [Fine-grained tool streaming](https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming.md)

- **Fine-Grained Tool Streaming — Chunking Behavior Note Simplified**: The inline benchmark showing before/after chunk timing (15s vs 3s delay with example chunk sequences) was removed and replaced with a concise statement.
  > Before: "With fine-grained tool streaming, tool use chunks start streaming faster, and are often longer and contain fewer word breaks. This is because of differences in chunking behavior. [followed by before/after chunk examples]"
  > After: "With fine-grained tool streaming, tool input chunks start arriving sooner because the server skips JSON-validation buffering. Chunks are typically longer and contain fewer mid-token breaks as a side effect."
  - *Implication*: The timing numbers and raw chunk examples are gone; readers get a conceptual explanation instead of concrete benchmarks.
  - *Source*: [Fine-grained tool streaming](https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming.md)

- **Fine-Grained Tool Streaming — Accumulator Helper Guidance Updated**: The tip about SDK helpers was reworded to be more concise, and the "Accumulating tool input deltas" section now explicitly clarifies when to use the manual pattern vs. the SDK accumulator.
  > "Where your SDK provides an accumulator helper (as used in the first example on this page), it handles this for you. The manual pattern is for SDKs without a helper, or when you need to react to partial input before the block closes."
  - *Implication*: C# and PHP examples include inline notes that those SDKs do not currently provide a stream accumulator for tool input, so the manual pattern is required.
  - *Source*: [Fine-grained tool streaming](https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming.md)

- **MCP Tunnels Docker Compose — Service Renamed from `mcp-gateway` to `mcp-proxy`**: All Docker Compose configuration blocks, volume mounts, config file references, and `network_mode` values were updated to use the new `mcp-proxy` service name. Config files are now named `mcp-proxy.yaml` instead of `mcp-gateway.yaml`.
  > Before: `network_mode: "service:mcp-gateway"` and `- ./config/mcp-gateway.yaml:/etc/mcp-gateway/config.yaml:ro`
  > After: `network_mode: "service:mcp-proxy"` and `- ./config/mcp-proxy.yaml:/etc/mcp-gateway/config.yaml:ro`
  - *Implication*: Existing deployments that copied earlier Docker Compose configurations must rename the service and config file accordingly. This is a breaking change for any deployment following the old docs.
  - *Source*: [Deploy with Docker Compose](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/deploy-compose.md)

- **MCP Tunnels Quickstart — Service Renamed from `mcp-gateway` to `mcp-proxy`**: The quickstart's Docker Compose YAML blocks (both macOS/Linux and Windows/PowerShell variants) were updated to use `mcp-proxy` as the service name and `mcp-proxy.yaml` as the config filename. Log inspection commands were also updated.
  > Before: `docker compose logs mcp-gateway | grep "route configured"`
  > After: `docker compose logs mcp-proxy | grep "route configured"`
  - *Implication*: Anyone following the quickstart guide should use the new service name in all `docker compose` commands.
  - *Source*: [MCP Tunnels Quickstart](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/quickstart.md)

- **MCP Tunnels Reference — Default Kubernetes Secret Name Changed**: The default value for the `--output` flag on both the `setup` and `renew-cert` subcommands changed from `k8s-secret:mcp-gateway` to `k8s-secret:mcp-tunnel`.
  > Before: `k8s-secret:mcp-gateway` (auto-detected when running in a Kubernetes pod; required otherwise)
  > After: `k8s-secret:mcp-tunnel` (auto-detected when running in a Kubernetes pod; required otherwise)
  - *Implication*: Kubernetes deployments using the auto-detected default secret name will write to a differently named secret. Existing deployments that relied on the `mcp-gateway` secret name must either pass `--output k8s-secret:mcp-gateway` explicitly or migrate the secret.
  - *Source*: [MCP Tunnels Reference](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/reference.md)

- **MCP Tunnels Troubleshooting — Service Name Updated in Remediation Steps**: Troubleshooting table entries and restart commands referencing `mcp-gateway` were updated to `mcp-proxy`. The example YAML filename in the `upstream.allowed_ips` snippet was also updated.
  > Before: `Add --url http://localhost:8080 and network_mode: "service:mcp-gateway" to the cloudflared service.`
  > After: `Add --url http://localhost:8080 and network_mode: "service:mcp-proxy" to the cloudflared service.`
  - *Implication*: Troubleshooting steps now match the renamed service; operators following old runbooks need to update `docker compose restart mcp-proxy` commands.
  - *Source*: [MCP Tunnels Troubleshooting](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/troubleshooting.md)

### CLI

- **Fine-Grained Tool Streaming — CLI Example Updated**: The CLI (`ant`) invocation was corrected to use `--format jsonl` and pipe output through `jq` instead of using `--transform usage`.
  > Before: `ant messages create --stream --transform usage <<'YAML'`
  > After: `ant messages create --stream --format jsonl <<'YAML' | jq 'select(.type == "message_delta") | .usage'`
  - *Implication*: The `--transform usage` flag was removed from the CLI example in favor of explicit `jq` filtering, which more clearly shows how to extract usage data from the JSONL stream.
  - *Source*: [Fine-grained tool streaming](https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming.md)

## Minor Changes

- **console.md**: Lowercased "Research Preview" to "research preview" in the feature note (+1/-1 lines)
- **deploy-helm.md**: Lowercased "Research Preview" to "research preview" in the feature note (+1/-1 lines)
- **security.md**: Lowercased "Research Preview" to "research preview" in the feature note (+1/-1 lines)

## Migration Notes

**Breaking: MCP Tunnels service and config file rename**

The Docker Compose service previously named `mcp-gateway` is now `mcp-proxy`. Config files previously named `mcp-gateway.yaml` are now `mcp-proxy.yaml`. The Kubernetes secret default changed from `k8s-secret:mcp-gateway` to `k8s-secret:mcp-tunnel`. Any existing deployments based on the earlier documentation must be updated:

1. Rename `config/mcp-gateway.yaml` to `config/mcp-proxy.yaml`
2. Rename the `mcp-gateway` service to `mcp-proxy` in `docker-compose.yaml`
3. Update all `network_mode: "service:mcp-gateway"` references to `"service:mcp-proxy"`
4. Update `docker compose restart` and `docker compose logs` commands to use `mcp-proxy`
5. For Kubernetes: the auto-detected secret name is now `mcp-tunnel`; pass `--output k8s-secret:mcp-gateway` explicitly if you need to maintain the old name

## Notable Details

- The C# and PHP SDK accumulation examples include explicit inline comments noting that those SDKs do not currently provide a stream accumulator helper for tool input, making the manual pattern the only supported approach for those languages.
- The Python streaming example in the usage section was simplified: the `for event in stream: pass` loop was removed, leaving only `stream.get_final_message()`, which is cleaner.
- The TypeScript `toolInputs` type changed from `Record<number, string>` to `Map<number, string>` in the accumulation example.

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| [fine-grained-tool-streaming.md](https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming.md) | modified | SIGNIFICANT | +643/-100 | Major expansion: adds C#, Go, Java, PHP, Ruby SDK examples; simplifies chunking note; clarifies accumulator guidance; updates CLI example |
| [deploy-compose.md](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/deploy-compose.md) | modified | SIGNIFICANT | +9/-9 | Renames `mcp-gateway` service and config file to `mcp-proxy` throughout |
| [quickstart.md](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/quickstart.md) | modified | SIGNIFICANT | +11/-11 | Renames `mcp-gateway` service and config file to `mcp-proxy` in all Compose blocks |
| [troubleshooting.md](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/troubleshooting.md) | modified | SIGNIFICANT | +5/-5 | Updates troubleshooting steps and restart commands to use `mcp-proxy` |
| [reference.md](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/reference.md) | modified | SIGNIFICANT | +3/-3 | Changes default `--output` Kubernetes secret from `mcp-gateway` to `mcp-tunnel` |
| [console.md](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/console.md) | modified | MINOR | +1/-1 | Lowercases "Research Preview" to "research preview" |
| [deploy-helm.md](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/deploy-helm.md) | modified | MINOR | +1/-1 | Lowercases "Research Preview" to "research preview" |
| [security.md](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/security.md) | modified | MINOR | +1/-1 | Lowercases "Research Preview" to "research preview" |
