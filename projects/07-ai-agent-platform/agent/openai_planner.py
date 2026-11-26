from __future__ import annotations

import json
import os
from urllib.request import Request, urlopen

from agent.runtime import AgentStep, ToolCall


class OpenAIResponsesPlanner:
    """Optional OpenAI Responses API planner; execution remains in AgentRuntime."""

    def __init__(self, tools: list[dict], *, model: str = "gpt-4.1-mini", api_key: str | None = None):
        self.tools = tools
        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")

    def next_action(self, goal: str, history: list[AgentStep]) -> ToolCall | None:
        transcript = [{"role": "user", "content": goal}]
        for step in history:
            if step.call_id:
                transcript.append({
                    "type": "function_call",
                    "call_id": step.call_id,
                    "name": step.tool,
                    "arguments": json.dumps(step.arguments),
                })
                transcript.append({
                    "type": "function_call_output",
                    "call_id": step.call_id,
                    "output": json.dumps(step.result, default=str),
                })
            else:
                transcript.append({
                    "role": "assistant",
                    "content": f"Called {step.tool} with {json.dumps(step.arguments)}",
                })
                transcript.append({
                    "role": "user",
                    "content": f"Tool result: {json.dumps(step.result, default=str)}",
                })
        payload = {
            "model": self.model,
            "input": transcript,
            "tools": self.tools,
            "tool_choice": "auto",
        }
        request = Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        for item in data.get("output", []):
            if item.get("type") == "function_call":
                return ToolCall(
                    name=item["name"],
                    arguments=json.loads(item.get("arguments") or "{}"),
                    call_id=item.get("call_id"),
                )
        return None
