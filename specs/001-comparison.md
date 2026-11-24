# MCP vs UTCP — specification

## Goal
Compare real MCP and UTCP clients against the same synthetic inventory API, without requiring an LLM or paid cloud service.

## Acceptance criteria
- ASP.NET Core .NET 10 API exposes product and stock reads and idempotent order creation.
- MCP client discovers and calls tools through an MCP server using a supported SDK.
- UTCP client discovers a valid manual and invokes the same API using a supported UTCP SDK.
- Both paths return equivalent business results; tests reset synthetic state between runs.
- Benchmark records cold and warm discovery separately from invocation, p50/p95, failures, sample size and environment. No invented measurements.
- Local-only defaults; no real credentials or customer data. Restrict tool destinations and validate inputs. Document authentication differences.
- CI runs integration tests and publishes raw benchmark artifacts.
- Spanish and English documentation, architecture diagrams, Slidev and dashboard show actual measured results.
- Microsoft Agent Framework integration is a separate optional example, not a prerequisite.

## References
- https://modelcontextprotocol.io/
- https://utcp.io/
- https://github.com/universal-tool-calling-protocol/utcp-specification

## Status
Specification only; implementation and verification pending.
