import os
from urllib.parse import quote
import httpx
from mcp.server.fastmcp import FastMCP

BASE = os.environ.get("API_BASE", "http://127.0.0.1:8080")
mcp = FastMCP("inventory-demo")

async def get(path, sku):
    async with httpx.AsyncClient(timeout=5, trust_env=False) as client:
        response = await client.get(BASE + path + quote(sku, safe=""))
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_stock(sku: str) -> dict:
    """Get stock for a synthetic inventory SKU."""
    return await get("/stock/", sku)

@mcp.tool()
async def get_product(sku: str) -> dict:
    """Get product details for a synthetic inventory SKU."""
    return await get("/products/", sku)

@mcp.tool()
async def create_order(sku: str, quantity: int, idempotency_key: str) -> dict:
    """Create a synthetic order with an explicit idempotency key."""
    async with httpx.AsyncClient(timeout=5, trust_env=False) as client:
        response = await client.post(BASE + "/orders", json={"sku":sku,"quantity":quantity}, headers={"Idempotency-Key":idempotency_key})
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")
