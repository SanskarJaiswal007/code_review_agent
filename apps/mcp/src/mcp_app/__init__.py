from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")


@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name} from mcp!"


def main() -> None:
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
