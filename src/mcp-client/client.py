import asyncio, sys, time, json
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server = Path(__file__).resolve().parents[1] / "mcp-server" / "server.py"
    async with stdio_client(StdioServerParameters(command=sys.executable,args=[str(server)])) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert any(t.name == "get_stock" for t in tools.tools)
            start = time.perf_counter()
            result = await session.call_tool("get_stock", {"sku":"DEMO-001"})
            assert not result.isError
            print(json.dumps({"protocol":"MCP","elapsed_ms":(time.perf_counter()-start)*1000,"result":result.model_dump(mode="json")}))
if __name__ == "__main__":
    asyncio.run(main())
