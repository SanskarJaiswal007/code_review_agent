"""Reusable LangChain and LangGraph agent harness."""

from .core import Harness
from .mcp_tools import MCPTools


def hello(name: str) -> str:
    return f"Hello, {name} from harness!"


__all__ = ["Harness", "MCPTools", "hello"]
