import asyncio, json, sys, uuid
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from utcp.utcp_client import UtcpClient

async def main():
    server=Path(__file__).resolve().parents[1]/"src/mcp-server/server.py"
    async with stdio_client(StdioServerParameters(command=sys.executable,args=[str(server)])) as (read,write):
        async with ClientSession(read,write) as mcp:
            await mcp.initialize()
            utcp=await UtcpClient.create(config={"manual_call_templates":[{"name":"inventory","call_template_type":"http","url":"http://127.0.0.1:8090/inventory.json","http_method":"GET"}]})
            try:
                async def invoke_mcp(name,args):
                    result=await mcp.call_tool(name,args)
                    assert not result.isError, result
                    return json.loads(result.content[0].text)
                async def invoke_utcp(name,args):
                    result=await utcp.call_tool("inventory."+name,args)
                    return json.loads(result) if isinstance(result,str) else result
                sku={"sku":"DEMO-001"}
                for name,expected in [("get_stock",{"sku":"DEMO-001","stock":42}),("get_product",{"sku":"DEMO-001","name":"Demo product"})]:
                    assert await invoke_mcp(name,sku)==expected
                    assert await invoke_utcp(name,sku)==expected
                key=str(uuid.uuid4())
                order=await invoke_mcp("create_order",{**sku,"quantity":2,"idempotency_key":key})
                assert order["sku"]==sku["sku"] and order["quantity"]==2 and order["id"]
                assert await invoke_utcp("create_order",{**sku,"quantity":2,"Idempotency-Key":key})==order
                assert await invoke_mcp("create_order",{**sku,"quantity":2,"idempotency_key":key})==order
                print("Protocol parity passed")
            finally:
                await utcp.close()
if __name__=="__main__":
    asyncio.run(main())
