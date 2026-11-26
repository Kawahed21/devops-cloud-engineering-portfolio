import json

import pytest

from agent.openai_planner import OpenAIResponsesPlanner
from agent.runtime import AgentStep


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
                "call_id": "call_123",
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
    assert call.call_id == "call_123"


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

def test_sends_function_call_output_for_previous_tool(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["payload"] = json.loads(request.data.decode())
        return FakeResponse({"output": [{"type": "message"}]})

    monkeypatch.setattr("agent.openai_planner.urlopen", fake_urlopen)
    planner = OpenAIResponsesPlanner([], api_key="test-key")
    planner.next_action(
        "Check status",
        [AgentStep("lookup", {"query": "status"}, {"state": "ok"}, "call_123")],
    )
    transcript = captured["payload"]["input"]
    assert transcript[1]["type"] == "function_call"
    assert transcript[1]["call_id"] == "call_123"
    assert transcript[2]["type"] == "function_call_output"
    assert transcript[2]["output"] == '{"state": "ok"}'
