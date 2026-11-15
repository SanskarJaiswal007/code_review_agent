"""Discover and call tools exposed by the local MCP app."""

from fastmcp import Client


class MCPTools:
    def __init__(self, url: str = "http://127.0.0.1:8000/mcp/") -> None:
        self.url = url

    async def list_tools(self):
        async with Client(self.url) as client:
            return await client.list_tools()

    async def call_tool(self, name: str, arguments: dict):
        async with Client(self.url) as client:
            return await client.call_tool(name, arguments)
