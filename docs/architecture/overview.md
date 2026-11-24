# Architecture / Arquitectura

Both paths use the same synthetic inventory API. The UTCP manual is discovery metadata, not an invocation proxy.

```mermaid
flowchart LR
  C[Demo client] --> M[MCP client]
  M -->|JSON-RPC / stdio| S[MCP server]
  S -->|HTTP| A[ASP.NET Core API]
  C --> U[UTCP client]
  U -. discovery .-> D[UTCP manual]
  U -->|Native HTTP| A
  classDef m fill:#e0f2fe,stroke:#0284c7,color:#172554
  classDef u fill:#ede9fe,stroke:#7c3aed,color:#312e81
  class M,S m
  class U,D u
```

## MCP sequence

```mermaid
sequenceDiagram
  participant C as MCP client
  participant S as MCP server
  participant A as Inventory API
  C->>S: initialize
  S-->>C: capabilities
  C->>S: tools/list
  S-->>C: tool schemas
  C->>S: tools/call
  S->>A: GET stock
  A-->>S: JSON
  S-->>C: Tool result
```

## UTCP sequence

```mermaid
sequenceDiagram
  participant C as UTCP client
  participant M as Manual host
  participant A as Inventory API
  C->>M: Fetch manual
  M-->>C: Tool definitions and call templates
  C->>A: Native HTTP request
  A-->>C: JSON result
```

MCP servers can implement tools directly; an extra downstream API is not mandatory. UTCP may require gateways for policy enforcement. This diagram describes the lab, not every possible deployment.
