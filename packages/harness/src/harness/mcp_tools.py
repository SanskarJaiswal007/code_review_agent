"""Discover and call tools exposed by an HTTP MCP server."""

from collections.abc import Callable, Mapping

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport


class MCPTools:
    def __init__(
        self,
        url: str = "http://127.0.0.1:8000/mcp/",
        *,
        bearer_token: str | Callable[[], str] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        """Configure HTTP credentials for each MCP connection.

        A token provider is called for every request, so expiring tokens can be
        refreshed outside this class. Custom headers support other auth schemes.
        """
        if bearer_token is not None and any(
            key.lower() == "authorization" for key in headers or {}
        ):
            raise ValueError("Use either bearer_token or an Authorization header")
        self.url = url
        self.bearer_token = bearer_token
        self.headers = dict(headers or {})

    def _client(self) -> Client:
        headers = dict(self.headers)
        if self.bearer_token is not None:
            token = self.bearer_token() if callable(self.bearer_token) else self.bearer_token
            if not token:
                raise ValueError("Bearer token must not be empty")
            headers["Authorization"] = f"Bearer {token}"
        return Client(StreamableHttpTransport(self.url, headers=headers or None))

    async def list_tools(self):
        async with self._client() as client:
            return await client.list_tools()

    async def call_tool(self, name: str, arguments: dict):
        async with self._client() as client:
            return await client.call_tool(name, arguments)
