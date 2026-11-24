# Azure API Management: MCP or UTCP?

## Reference architecture
Existing APIs remain behind APIM in both designs.

- MCP: agent → MCP client → MCP server → APIM → backend.
- UTCP: agent → UTCP client → APIM → backend, with a trusted manual for discovery.

APIM remains the policy enforcement point for API authentication, authorization, quotas and telemetry. The client or MCP server must acquire correctly scoped credentials; neither protocol bypasses APIM policies.

## Architecture decision record
Prefer evaluating direct invocation when the existing API contract is sufficient and the agent runtime supports it. Introduce MCP when its interoperability, abstraction, context capabilities or composition justify the adapter. An MCP server may itself be exposed through APIM; the extra hop is not necessarily a separately managed service.

## Production acceptance
- Verify Entra ID token audience and scopes, delegated versus application permissions.
- Validate manual provenance, allowed hosts and methods; prevent arbitrary outbound requests.
- Preserve correlation IDs and redact secrets.
- Require explicit approval for order creation where appropriate.
- Measure equivalent payloads, authentication, connection reuse, transport and deployment topology.
- Do not extrapolate local stdio results to Azure network deployments.

This is a proposed architecture, not a validated Azure deployment.
