from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Protocol


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]
    call_id: str | None = None


@dataclass(frozen=True)
class AgentStep:
    tool: str
    arguments: dict[str, Any]
    result: Any
    call_id: str | None = None


class Planner(Protocol):
    def next_action(self, goal: str, history: list[AgentStep]) -> ToolCall | None:
        """Return the next approved-tool request, or None when finished."""


class AgentError(RuntimeError):
    pass


class AgentRuntime:
    """Executes planner requests only against explicitly registered tools."""

    def __init__(
        self,
        planner: Planner,
        tools: dict[str, Callable[..., Any]],
        *,
        max_steps: int = 5,
    ) -> None:
        if max_steps < 1:
            raise ValueError("max_steps must be positive")
        self.planner = planner
        self.tools = dict(tools)
        self.max_steps = max_steps

    def run(self, goal: str) -> list[AgentStep]:
        if not goal.strip():
            raise ValueError("goal must not be empty")

        history: list[AgentStep] = []
        for _ in range(self.max_steps):
            call = self.planner.next_action(goal, history)
            if call is None:
                return history
            tool = self.tools.get(call.name)
            if tool is None:
                raise AgentError(f"Tool is not allowlisted: {call.name}")
            if not isinstance(call.arguments, dict):
                raise AgentError("Tool arguments must be an object")
            result = tool(**call.arguments)
            history.append(AgentStep(call.name, call.arguments, result, call.call_id))
        raise AgentError("Maximum agent steps exceeded")
