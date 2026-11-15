"""HTTP gateway for an Azure DevOps MCP server."""

import os
import re

from fastmcp import Client, FastMCP
from fastmcp.client.transports import StdioTransport, StreamableHttpTransport


def create_server(environ: dict[str, str] | None = None) -> FastMCP:
    config = os.environ if environ is None else environ
    mode = config.get("AZURE_DEVOPS_MCP_MODE", "local").lower()
    organization = config.get("AZURE_DEVOPS_ORGANIZATION", "").strip()
    if not organization:
        raise ValueError("Set AZURE_DEVOPS_ORGANIZATION to your Azure DevOps organization name")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", organization):
        raise ValueError("AZURE_DEVOPS_ORGANIZATION must be an organization name, not a URL")
    if mode == "local":
        transport = StdioTransport(
            command="npx",
            args=["-y", "@azure-devops/mcp", organization],
            env=dict(config),
        )
    elif mode == "remote":
        token = config.get("AZURE_DEVOPS_MCP_TOKEN", "").strip()
        if not token:
            raise ValueError("Set AZURE_DEVOPS_MCP_TOKEN to a Microsoft Entra access token")
        transport = StreamableHttpTransport(
            f"https://mcp.dev.azure.com/{organization}",
            headers={"Authorization": f"Bearer {token}"},
        )
    else:
        raise ValueError("AZURE_DEVOPS_MCP_MODE must be local or remote")
    return FastMCP.from_client(Client(transport), name="Azure DevOps MCP gateway")


def main() -> None:
    create_server().run(transport="streamable-http", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
