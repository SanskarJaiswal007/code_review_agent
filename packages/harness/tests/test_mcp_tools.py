import pytest

from harness import MCPTools


def test_bearer_token_provider_is_read_for_each_connection() -> None:
    tokens = iter(["first", "second"])
    tools = MCPTools(bearer_token=lambda: next(tokens))

    assert tools._client().transport.headers == {"Authorization": "Bearer first"}
    assert tools._client().transport.headers == {"Authorization": "Bearer second"}


def test_custom_auth_header_is_supported() -> None:
    tools = MCPTools(headers={"X-API-Key": "secret"})

    assert tools._client().transport.headers == {"X-API-Key": "secret"}


def test_conflicting_authorization_is_rejected() -> None:
    with pytest.raises(ValueError, match="either bearer_token"):
        MCPTools(bearer_token="token", headers={"authorization": "Basic something"})


def test_empty_bearer_token_is_rejected() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        MCPTools(bearer_token="")._client()
