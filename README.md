# MCP vs UTCP — Engineering Lab

![Architecture comparison](docs/assets/architecture.svg)

[![Backend CI](https://github.com/davidop/mcp-vs-utcp-demo/actions/workflows/backend.yml/badge.svg)](https://github.com/davidop/mcp-vs-utcp-demo/actions/workflows/backend.yml)
[![Protocol CI](https://github.com/davidop/mcp-vs-utcp-demo/actions/workflows/protocols.yml/badge.svg)](https://github.com/davidop/mcp-vs-utcp-demo/actions/workflows/protocols.yml)

Independent, evidence-driven comparison / Comparativa independiente basada en evidencias.

- [Architecture and sequence diagrams](docs/architecture/overview.md)
- [Decision and security guide](docs/architecture/decision-guide.md)
- [Specification](specs/001-comparison.md)
- [Branding policy](docs/assets/BRANDING.md)

Hands-on comparison of two tool calling architectures, using the same .NET 10 inventory API. / Comparativa práctica de dos arquitecturas de invocación de herramientas sobre una API común.

**Status:** initial integration code committed; CI verification pending. No performance conclusions yet.

## Run locally
```bash
docker compose up --build -d
python -m pip install -r requirements-mcp.txt -r requirements-utcp.txt
python tests/smoke.py
python src/mcp-client/client.py
```
In another terminal / En otra terminal:
```bash
python -m http.server 8090 --bind 127.0.0.1 --directory manuals
```
Then / Después:
```bash
python src/utcp-client/client.py
```

MCP uses SDK stdio client/server; UTCP discovers a static HTTP manual and invokes the REST endpoint directly. The initial UTCP tool exposes a fixed demo SKU, not general parameter parity yet. The manual server is for discovery only. No LLM or paid API required.

Single invocation measurements are smoke-test observations, not benchmarks. Future work: identical parameter schemas, warm/cold repeated runs, dashboard, Slidev and optional Agent Framework integration.

## Engineering deliverables

- [Azure APIM architecture decision](docs/architecture/azure-apim.md)
- [Benchmark runner](benchmarks/run.py) and [methodology](benchmarks/README.md)
- [Benchmark CI and artifacts](https://github.com/davidop/mcp-vs-utcp-demo/actions/workflows/benchmark.yml)
- [Evidence dashboard](dashboard/index.html)
- [Slidev deck](slides/slides.md)
- [Release acceptance checklist](docs/release-checklist.md)

The benchmark and Pages workflows are configured, not yet verified. The dashboard imports measured JSON; it does not generate synthetic performance data.

## Official references
- https://modelcontextprotocol.io/
- https://github.com/universal-tool-calling-protocol/python-utcp

See [specification](specs/001-comparison.md). Local synthetic data only.
