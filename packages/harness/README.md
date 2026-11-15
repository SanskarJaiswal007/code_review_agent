# Harness

`Harness` wraps a native LangGraph graph. Pass a LangChain chat model and tools
to build a default tool-calling agent, or pass an already compiled LangGraph
workflow. The underlying graph remains available as `harness.graph`.

```python
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from harness import Harness

harness = Harness(
    model=model,  # A LangChain chat model supplied by the application
    tools=tools,  # Native LangChain tools
    checkpointer=InMemorySaver(),
    store=InMemoryStore(),
    system_prompt="You are a code review assistant.",
)
result = await harness.ainvoke(
    {"messages": [HumanMessage(content="Review this pull request")]},
    thread_id="review-123",
)
```

Use a persistent LangGraph checkpointer and store in production. The
checkpointer retains conversation state for each thread. Long-term memory
requires application-specific nodes or tools that explicitly read and write
the store; passing a store alone does not create memories. The harness exposes
`put_memory`, `get_memory`, and `search_memories` for explicit store access.
`MCPTools` remains
available for direct access to the Azure DevOps gateway. To use its tools in
the agent, adapt the discovered MCP schemas and calls to LangChain tools.
