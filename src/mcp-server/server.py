import os
import httpx
from mcp.server.fastmcp import FastMCP

BASE = os.environ.get("API_BASE", "http://127.0.0.1:8080")
mcp = FastMCP("inventory-demo")

@mcp.tool()
async def get_stock(sku: str) -> dict:
    """Get stock for a synthetic inventory SKU."""
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(BASE + "/stock/" + httpx.URL("").copy_with(path=sku).raw_path.decode().lstrip("/"))
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")
