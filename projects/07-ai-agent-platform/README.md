# 07: Secure AI Agent Runtime

## Objective
A testable tool-using agent runtime with a provider-neutral planner protocol, an optional OpenAI Responses API planner, explicit tool allowlists, bounded execution and an auditable execution trace.

## Architecture
1. The planner proposes one structured function call.
2. The runtime validates the tool name against a static allowlist.
3. The runtime executes only the registered Python function.
4. The result is appended to a trace and returned to the planner.
5. Execution stops when the planner returns no action or the step budget is reached.

The OpenAI adapter sends the goal and prior tool results to the Responses API. It does not execute model-selected tools. Tool execution stays in the local runtime and is constrained by the configured allowlist.

## Run tests
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Optional model integration
Set `OPENAI_API_KEY` in the environment and construct `OpenAIResponsesPlanner` with function schemas for the tools registered in `AgentRuntime`. Never put API keys in source control. Model calls may incur API charges; tests mock the HTTP response and do not call a paid endpoint.

## Safety controls
- No arbitrary Python, shell, filesystem or network tool is exposed by default.
- Unknown tool names fail closed.
- Maximum step count prevents unbounded loops.
- Empty goals are rejected.
- Model-provided arguments must be validated by each tool.
- Tools should be read-only by default; side-effecting tools require explicit authorization, input validation, idempotency and audit controls.
- Add per-user authorization, rate limits, PII controls and trace redaction before production.

## Limitations
This is a small agent orchestration reference, not a production autonomous agent. It does not persist state or include human approval UI, distributed tracing, evaluations or retry policies. Use deterministic tests and sandboxed tools before expanding its permissions.
