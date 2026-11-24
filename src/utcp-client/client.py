import asyncio, json, time
from utcp.utcp_client import UtcpClient

async def main():
    start = time.perf_counter()
    client = await UtcpClient.create(config={"manual_call_templates":[{"name":"inventory","call_template_type":"http","url":"http://127.0.0.1:8090/inventory.json","http_method":"GET"}]})
    discovery = (time.perf_counter()-start)*1000
    try:
        start = time.perf_counter()
        result = await client.call_tool("inventory.get_stock", {"sku":"DEMO-001"})
        elapsed = (time.perf_counter()-start)*1000
        if isinstance(result,str): result = json.loads(result)
        assert result == {"sku":"DEMO-001","stock":42}, result
        print(json.dumps({"protocol":"UTCP","discovery_ms":discovery,"elapsed_ms":elapsed,"result":result}))
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
