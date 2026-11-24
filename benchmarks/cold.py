"""Cold client lifecycle benchmark; backend and discovery HTTP server remain warm."""
import asyncio
import json
import sys
import time
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from utcp.utcp_client import UtcpClient

SERVER = Path(__file__).resolve().parents[1] / "src/mcp-server/server.py"
EXPECTED = {"sku": "DEMO-001", "stock": 42}

async def mcp_call():
    async with stdio_client(StdioServerParameters(command=sys.executable, args=[str(SERVER)])) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            await session.list_tools()
            result = await session.call_tool("get_stock", {"sku": "DEMO-001"})
            if result.isError:
                raise RuntimeError(str(result.content))
            return json.loads(result.content[0].text)

async def utcp_call():
    client = await UtcpClient.create(config={"manual_call_templates": [{"name": "inventory", "call_template_type": "http", "url": "http://127.0.0.1:8090/inventory.json", "http_method": "GET"}]})
    try:
        result = await client.call_tool("inventory.get_stock", {"sku": "DEMO-001"})
        return json.loads(result) if isinstance(result, str) else result
    finally:
        await client.close()

async def main():
    failures = 0
    calls = [("MCP", mcp_call), ("UTCP", utcp_call)]
    for i in range(20):
        for name, call in (calls if i % 2 == 0 else reversed(calls)):
            start = time.perf_counter()
            error = None
            try:
                result = await asyncio.wait_for(call(), timeout=60)
                if result != EXPECTED:
                    raise ValueError(repr(result))
            except Exception as exc:
                error = repr(exc)
                failures += 1
            print(json.dumps({"protocol": name, "iteration": i, "phase": "cold_client_lifecycle", "elapsed_ms": (time.perf_counter()-start)*1000, "ok": error is None, "error": error}), flush=True)
    return int(failures > 0)

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
