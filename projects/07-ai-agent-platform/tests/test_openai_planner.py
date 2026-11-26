import json

import pytest

from agent.openai_planner import OpenAIResponsesPlanner


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps(self.payload).encode()


def test_parses_function_call(monkeypatch):
    def fake_urlopen(request, timeout):
        assert request.full_url.endswith("/v1/responses")
        assert request.get_header("Authorization") == "Bearer test-key"
        return FakeResponse({
            "output": [{
                "type": "function_call",
                "name": "lookup",
                "arguments": '{"query":"status"}',
            }]
        })

    monkeypatch.setattr("agent.openai_planner.urlopen", fake_urlopen)
    planner = OpenAIResponsesPlanner(
        [{"type": "function", "name": "lookup", "parameters": {"type": "object"}}],
        api_key="test-key",
    )
    call = planner.next_action("Check status", [])
    assert call.name == "lookup"
    assert call.arguments == {"query": "status"}


def test_no_tool_call_finishes(monkeypatch):
    monkeypatch.setattr(
        "agent.openai_planner.urlopen",
        lambda request, timeout: FakeResponse({"output": [{"type": "message"}]}),
    )
    planner = OpenAIResponsesPlanner([], api_key="test-key")
    assert planner.next_action("Done", []) is None


def test_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        OpenAIResponsesPlanner([])
