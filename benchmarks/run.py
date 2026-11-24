import asyncio, json, sys, time, platform
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from utcp.utcp_client import UtcpClient

N=100
EXPECTED={"sku":"DEMO-001","stock":42}
async def measure(name, call):
    for i in range(N):
        start=time.perf_counter()
        error=None
        try:
            result=await call()
            assert result==EXPECTED, repr(result)
        except Exception as e:
            error=str(e)
        print(json.dumps({"protocol":name,"elapsed_ms":(time.perf_counter()-start)*1000,"ok":error is None,"error":error,"iteration":i}),flush=True)
        if error: raise RuntimeError(error)

async def main():
    server=Path(__file__).resolve().parents[1]/"src/mcp-server/server.py"
    async with stdio_client(StdioServerParameters(command=sys.executable,args=[str(server)])) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            await session.list_tools()
            async def mcp_call():
                result=await session.call_tool("get_stock",{"sku":"DEMO-001"})
                assert not result.isError
                return json.loads(result.content[0].text)
            await measure("MCP",mcp_call)
    client=await UtcpClient.create(config={"manual_call_templates":[{"name":"inventory","call_template_type":"http","url":"http://127.0.0.1:8090/inventory.json","http_method":"GET"}]})
    try:
        async def utcp_call():
            result=await client.call_tool("inventory.get_stock", {"sku":"DEMO-001"})
            return json.loads(result) if isinstance(result,str) else result
        await measure("UTCP",utcp_call)
    finally:
        await client.close()
if __name__=="__main__":
    asyncio.run(main())
