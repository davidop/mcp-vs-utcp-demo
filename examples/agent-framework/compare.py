"""Read-only workflow; no model, credentials or cloud resources required.
API pattern: https://learn.microsoft.com/python/api/agent-framework-core/agent_framework.workflowbuilder
"""
import asyncio
import json
import sys
from pathlib import Path
from typing_extensions import Never
from agent_framework import WorkflowBuilder, WorkflowContext, executor
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from utcp.utcp_client import UtcpClient

ROOT = Path(__file__).resolve().parents[2]

@executor(id="compare_stock")
async def compare_stock(sku: str, ctx: WorkflowContext[Never, str]) -> None:
    if sku != "DEMO-001":
        raise ValueError("Only the synthetic fixture is allowed")
    async with stdio_client(StdioServerParameters(command=sys.executable, args=[str(ROOT / "src/mcp-server/server.py")])) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            response = await session.call_tool("get_stock", {"sku": sku})
            if response.isError:
                raise RuntimeError("MCP tool failed")
            mcp_result = json.loads(response.content[0].text)
    client = await UtcpClient.create(config={"manual_call_templates": [{"name": "inventory", "call_template_type": "http", "url": "http://127.0.0.1:8090/inventory.json", "http_method": "GET"}]})
    try:
        utcp_result = await client.call_tool("inventory.get_stock", {"sku": sku})
        if isinstance(utcp_result, str):
            utcp_result = json.loads(utcp_result)
    finally:
        await client.close()
    expected = {"sku": sku, "stock": 42}
    if mcp_result != expected or utcp_result != expected:
        raise RuntimeError("Protocol parity failed")
    await ctx.yield_output(json.dumps({"MCP": mcp_result, "UTCP": utcp_result}))

async def main():
    workflow = WorkflowBuilder(start_executor=compare_stock).build()
    events = await workflow.run("DEMO-001")
    outputs = events.get_outputs()
    assert len(outputs) == 1
    result = json.loads(outputs[0])
    assert result["MCP"] == result["UTCP"] == {"sku": "DEMO-001", "stock": 42}
    print(json.dumps(result))

if __name__ == "__main__":
    asyncio.run(main())
