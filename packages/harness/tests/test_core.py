from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

from harness import Harness


def test_checkpoint_keeps_messages_in_same_thread() -> None:
    harness = Harness(
        model=FakeListChatModel(responses=["first answer", "second answer"]),
        checkpointer=InMemorySaver(),
    )

    harness.invoke({"messages": [{"role": "user", "content": "first"}]}, thread_id="review")
    result = harness.invoke(
        {"messages": [{"role": "user", "content": "second"}]}, thread_id="review"
    )

    assert [message.content for message in result["messages"]] == [
        "first",
        "first answer",
        "second",
        "second answer",
    ]


def test_explicit_long_term_memory_round_trip() -> None:
    harness = Harness(model=FakeListChatModel(responses=["unused"]), store=InMemoryStore())

    harness.put_memory(("repository", "review"), "rule", {"text": "check tests"})

    assert harness.get_memory(("repository", "review"), "rule") == {"text": "check tests"}
