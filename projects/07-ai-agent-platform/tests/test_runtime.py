import pytest

from agent.runtime import AgentError, AgentRuntime, ToolCall
from agent.tools import word_count


class SequencePlanner:
    def __init__(self, calls):
        self.calls = iter(calls)

    def next_action(self, goal, history):
        return next(self.calls, None)


def test_executes_allowlisted_tool_and_returns_trace():
    planner = SequencePlanner([ToolCall("word_count", {"text": "hello agent"}) , None])
    runtime = AgentRuntime(planner, {"word_count": word_count})
    trace = runtime.run("Count words")
    assert len(trace) == 1
    assert trace[0].result == {"words": 2, "characters": 11}


def test_rejects_unregistered_tool():
    runtime = AgentRuntime(
        SequencePlanner([ToolCall("delete_everything", {}), None]),
        {"word_count": word_count},
    )
    with pytest.raises(AgentError, match="not allowlisted"):
        runtime.run("Unsafe request")


def test_enforces_step_budget():
    calls = [ToolCall("word_count", {"text": "x"}) for _ in range(3)] + [None]
    runtime = AgentRuntime(SequencePlanner(calls), {"word_count": word_count}, max_steps=2)
    with pytest.raises(AgentError, match="Maximum agent steps"):
        runtime.run("Repeat")


def test_rejects_empty_goal():
    runtime = AgentRuntime(SequencePlanner([None]), {})
    with pytest.raises(ValueError, match="goal"):
        runtime.run("  ")
