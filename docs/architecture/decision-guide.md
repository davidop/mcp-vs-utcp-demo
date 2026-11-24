# Decision guide / Guía de decisión

| Dimension | MCP | UTCP |
|---|---|---|
| Discovery | Protocol capability negotiation and tools/list | Manual and call templates |
| Invocation | MCP tool call | Native protocol via client plugin |
| Other capabilities | Resources, prompts and negotiated features | Tool calling focus |
| Existing REST APIs | Server adapter if not already exposed | Describe native endpoint |
| Security | Transport-specific authorization and server policies | Native credentials and client policies |
| Performance | Measure actual transport and implementation | Measure actual transport and implementation |

## Security boundaries
Treat tool descriptions and results as untrusted. Allowlist destinations, restrict redirects and outbound network access, protect credentials, validate parameters, require approvals for writes, and use idempotency keys. Local stdio is not equivalent to remote HTTP OAuth. Neither protocol guarantees safe agent behavior.

## Benchmark policy
Use identical payloads, backend, concurrency and connection reuse; separate cold discovery from warm calls. Record raw samples, failures, environment, versions and commit SHA. Compare stdio and Streamable HTTP separately. No universal winner can be inferred from a single lab.
