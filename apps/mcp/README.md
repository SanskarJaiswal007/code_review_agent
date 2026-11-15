# MCP app

From the repository root, start the HTTP server:

```bash
uv run --package mcp-app mcp-app
```

The MCP endpoint is `http://127.0.0.1:8000/mcp/`. Send `POST` requests with `Content-Type: application/json` and `Accept: application/json, text/event-stream`.

Initialize a session first:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"Postman","version":"1.0"}}}
```

Copy the `mcp-session-id` response header into an `Mcp-Session-Id` request header, then call the tool:

```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"hello","arguments":{"name":"Postman"}}}
```
