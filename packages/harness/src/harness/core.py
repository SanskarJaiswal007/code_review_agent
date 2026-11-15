"""Thin wrapper around a LangGraph workflow or LangChain agent graph."""

from collections.abc import Sequence
from typing import Any

from langchain.agents import create_agent
from langchain_core.language_models import BaseChatModel
from langgraph.store.base import BaseStore


class Harness:
    """Run a native graph with optional thread state and long-term storage.

    ``workflow`` may be an already compiled LangGraph graph. Otherwise a
    LangChain tool-calling agent is built from ``model`` and ``tools``.
    A store is available to graph nodes but does not automatically save memory.
    """

    def __init__(
        self,
        *,
        model: BaseChatModel | str | None = None,
        tools: Sequence[Any] = (),
        checkpointer: Any = None,
        store: BaseStore | None = None,
        system_prompt: str | None = None,
        workflow: Any = None,
    ) -> None:
        self.graph: Any
        self.checkpointer = checkpointer
        self.store = store
        if workflow is not None:
            self.graph = workflow
        else:
            if model is None:
                raise ValueError("Provide either a model or a compiled workflow")
            self.graph = create_agent(
                model=model,
                tools=list(tools),
                system_prompt=system_prompt,
                checkpointer=checkpointer,
                store=store,
            )

    def _config(self, thread_id: str | None, config: dict | None) -> dict:
        result = dict(config or {})
        if thread_id is not None:
            if not thread_id:
                raise ValueError("thread_id must not be empty")
            configurable = dict(result.get("configurable", {}))
            configurable["thread_id"] = thread_id
            result["configurable"] = configurable
        elif self.checkpointer is not None and not result.get("configurable", {}).get("thread_id"):
            raise ValueError("A thread_id is required when using a checkpointer")
        return result

    def invoke(
        self, input: Any, *, thread_id: str | None = None, config: dict | None = None, **kwargs: Any
    ) -> Any:
        return self.graph.invoke(input, config=self._config(thread_id, config), **kwargs)

    async def ainvoke(
        self, input: Any, *, thread_id: str | None = None, config: dict | None = None, **kwargs: Any
    ) -> Any:
        return await self.graph.ainvoke(input, config=self._config(thread_id, config), **kwargs)

    def stream(
        self, input: Any, *, thread_id: str | None = None, config: dict | None = None, **kwargs: Any
    ):
        return self.graph.stream(input, config=self._config(thread_id, config), **kwargs)

    def astream(
        self, input: Any, *, thread_id: str | None = None, config: dict | None = None, **kwargs: Any
    ):
        return self.graph.astream(input, config=self._config(thread_id, config), **kwargs)

    def put_memory(self, namespace: tuple[str, ...], key: str, value: dict[str, Any]) -> None:
        """Explicitly save a JSON-like memory in the configured LangGraph store."""
        if self.store is None:
            raise ValueError("Configure a store before using long-term memory")
        self.store.put(namespace, key, value)

    def get_memory(self, namespace: tuple[str, ...], key: str) -> dict[str, Any] | None:
        """Return a stored memory value, or None when the key is absent."""
        if self.store is None:
            raise ValueError("Configure a store before using long-term memory")
        item = self.store.get(namespace, key)
        return None if item is None else item.value

    def search_memories(
        self, namespace: tuple[str, ...], *, query: str | None = None, limit: int = 10
    ):
        """Search a memory namespace using the store's search capability."""
        if self.store is None:
            raise ValueError("Configure a store before using long-term memory")
        return self.store.search(namespace, query=query, limit=limit)
