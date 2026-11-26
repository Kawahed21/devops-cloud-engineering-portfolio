# 07 — Secure AI Agent Runtime

## Objective
A small, auditable agent runtime demonstrating bounded planning, explicit tool allowlists, typed tool calls, deterministic execution and an execution trace. The project intentionally separates the planner from execution so a model provider can be swapped without granting a model arbitrary code or shell access.

## Architecture
1. A planner proposes one structured tool call.
2. The runtime validates the tool name against a static allowlist.
3. The runtime executes the registered Python function.
4. The result is appended to an auditable trace and passed to the planner.
5. Execution stops when the planner returns no action or the step budget is reached.

## Safety controls
- No arbitrary Python, shell, filesystem or network tool is exposed.
- Unknown tool names fail closed.
- Maximum step count prevents unbounded loops.
- Empty goals are rejected.
- Tools should be read-only by default; side-effecting tools require separate authorization, input validation, idempotency and audit controls.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Example
The tests use a deterministic planner stub. This keeps CI reproducible and avoids requiring API keys or paid model calls. A production extension can implement the Planner protocol using an LLM tool-calling API, but must validate model output and retain the runtime allowlist as the enforcement boundary.

## Limitations
This repository component is an agent orchestration foundation, not a production autonomous agent. It does not connect to a model provider, persist state, or perform external side effects. Provider integration, authentication, approval workflows, tracing and evaluation datasets are planned follow-ups.
