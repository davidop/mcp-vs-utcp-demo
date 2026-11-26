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

## Guía de decisión en español

| Dimensión | MCP | UTCP |
|---|---|---|
| Descubrimiento | Negociación de capacidades y tools/list | Manual y plantillas de llamada |
| Invocación | Llamada a herramienta MCP | Protocolo nativo mediante plugin cliente |
| Capacidades adicionales | Recursos, prompts y capacidades negociadas | Centrado en invocación de herramientas |
| API REST existente | Adaptador servidor si no está expuesta | Descripción del endpoint nativo |
| Seguridad | Autorización según transporte y políticas del servidor | Credenciales nativas y políticas del cliente |
| Rendimiento | Medir transporte e implementación reales | Medir transporte e implementación reales |

### Decisión arquitectónica

Seleccionar MCP cuando la interoperabilidad con hosts compatibles y las capacidades negociadas sean requisitos principales. Evaluar UTCP cuando existan APIs nativas estables y se quiera evitar un intermediario de invocación. Una arquitectura híbrida es válida: mantener el contrato de negocio común y elegir el mecanismo de acceso por consumidor. No asumir que eliminar un salto implica reducir tokens: el contexto enviado al modelo depende de los esquemas y del host.

### Límites de seguridad

Tratar descripciones y respuestas como datos no confiables. Restringir destinos, redirecciones y salida de red; proteger credenciales, validar parámetros, exigir aprobación para escrituras sensibles y aplicar idempotencia. Stdio local no equivale a HTTP remoto con OAuth. Ninguno de los protocolos garantiza por sí solo un agente seguro.

### Interpretación de las mediciones

Mantener iguales payloads, backend, concurrencia y reutilización de conexiones. Separar descubrimiento en frío de llamadas en caliente. Conservar muestras, errores, entorno, versiones y SHA. Comparar stdio y Streamable HTTP por separado; este laboratorio no demuestra un ganador universal. Las estimaciones de contexto no son mediciones de facturación de un LLM.
