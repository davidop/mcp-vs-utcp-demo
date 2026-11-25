# Benchmark methodology
Record each invocation as JSONL with protocol, elapsed_ms and ok. Separate discovery and invocation; do not mix cold process launches with warm sessions. Use at least 100 warm calls per protocol, identical SKU and payload, and report SDK versions, transport, runner, commit, concurrency and failures. The aggregate.py script computes median and nearest-rank p95 from successful samples. It does not generate samples. 

## First verified CI observation / Primera observación verificada

Run: https://github.com/davidop/mcp-vs-utcp-demo/actions/runs/45508080670 (2026-11-24 UTC). Tested PR merge commit: `d5b8c9afcdbdd3f37e8771c30fcfe8d5cf995842`. Values transcribed from the benchmark job logs, rounded to three decimals.

| Lifecycle | Protocol | Attempts | Failures | p50 ms | p95 ms |
|---|---|---:|---:|---:|---:|
| Warm | MCP | 100 | 0 | 8.315 | 13.470 |
| Warm | UTCP | 100 | 0 | 1.511 | 2.136 |
| Cold | MCP | 20 | 0 | 511.836 | 529.035 |
| Cold | UTCP | 20 | 0 | 3.687 | 5.172 |

The run measures only get_stock for DEMO-001, sequentially, alternating protocol order. Cold includes MCP subprocess launch, initialization, discovery and teardown versus UTCP client creation, HTTP discovery and close; backend remains warm. Warm excludes discovery. This is an architecture-specific comparison, not a protocol-wide ranking. No LLM, token billing, network WAN or concurrent workload was measured. Raw JSONL and environment metadata are available in the run's benchmark-evidence artifact; independent raw-sample audit and repeated runs remain pending.

En esta configuración concreta UTCP presenta menor latencia observada; no implica superioridad universal. El arranque del subproceso MCP domina la comparación en frío. No se han medido tokens facturados ni concurrencia. Pendiente repetir y auditar las muestras crudas.
