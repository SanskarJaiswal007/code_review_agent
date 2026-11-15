# Azure DevOps MCP gateway

The app exposes the selected Azure DevOps MCP server's tools on a local HTTP endpoint. Select one upstream with `AZURE_DEVOPS_MCP_MODE`; the default is `local`.

## Local Azure DevOps server

Install Node.js 20 or later and set your Azure DevOps organization name. The gateway launches Microsoft's `@azure-devops/mcp` package through `npx` and uses its normal sign-in flow. From the repository root:

```bash
export AZURE_DEVOPS_ORGANIZATION=your-organization
export AZURE_DEVOPS_MCP_MODE=local
uv run --package mcp-app mcp-app
```

The first tool discovery may ask you to sign in and may download the npm package.

## Remote Azure DevOps server

Use an Azure DevOps organization backed by Microsoft Entra ID. Provide a valid Entra access token for the remote MCP service through the environment; tokens expire and must be refreshed outside this app.

```bash
export AZURE_DEVOPS_ORGANIZATION=your-organization
export AZURE_DEVOPS_MCP_MODE=remote
export AZURE_DEVOPS_MCP_TOKEN=your-entra-access-token
uv run --package mcp-app mcp-app
```

The remote upstream is `https://mcp.dev.azure.com/{organization}`. Only one upstream is active per gateway process.

## Agent connection

The gateway endpoint is `http://127.0.0.1:8000/mcp/`. The harness package includes `MCPTools` for discovering and calling the exposed tools:

```python
from harness.mcp_tools import MCPTools

tools = MCPTools()
available = await tools.list_tools()
result = await tools.call_tool(available[0].name, {})  # Supply that tool's required arguments.
```

The harness does not yet contain a decision-making agent loop. Tool names and argument schemas come from the selected Azure DevOps upstream.

## Postman

Send `POST` requests to the gateway endpoint with `Content-Type: application/json` and `Accept: application/json, text/event-stream`.

Initialize a session first:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"Postman","version":"1.0"}}}
```

Copy the `mcp-session-id` response header into an `Mcp-Session-Id` request header, then call the tool:

```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"hello","arguments":{"name":"Postman"}}}
```
