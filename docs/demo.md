# Demo / Demonstration

## Backend
Run `docker compose up --build -d` and then `python tests/smoke.py` once healthy.

## MCP
Create a Python virtual environment, install `pip install -r requirements-mcp.txt` and run `python src/mcp-client/client.py`. The client launches a real stdio MCP server, discovers its stock tool and calls the shared backend. The output contains one measured invocation, not a comparative benchmark.

## UTCP
Pending implementation against the official SDK and manual schema. Direct HTTP alone must not be labelled UTCP.

## Security
Local synthetic data only. MCP stdio uses local process trust; this does not demonstrate remote MCP OAuth. Orders are in memory; stock is a fixed fixture. Do not deploy this lab publicly.

## Status
Backend and initial MCP code committed; execution verification pending. UTCP, comparative benchmark, dashboard, Slidev and Agent Framework integration pending.
