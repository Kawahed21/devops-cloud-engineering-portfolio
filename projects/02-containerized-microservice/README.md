# 02 — Containerized Python Microservice

## Objective
Build a small HTTP service with health checks, unit tests and a reproducible Docker image. Use it as the workload for the Kubernetes, security and observability labs.

## Service contract
- `GET /`: service identity and status.
- `GET /health`: liveness endpoint.
- `GET /ready`: readiness endpoint.
- `GET /metrics`: Prometheus request counter and latency histogram. Route labels use registered route templates to avoid unbounded URL cardinality.
- Listen on port 8000 inside the container.

## Suggested stack
Python 3.12, FastAPI, Uvicorn, pytest and Docker. Keep dependencies pinned in a lock/requirements file.

## Build and test workflow
1. Create an application package and typed request/response models.
2. Add tests for successful responses, health and error handling.
3. Run tests locally with a clean virtual environment.
4. Build a multi-stage or slim Docker image.
5. Run as a non-root user and expose only port 8000.
6. Add a container health check.
7. Tag images with immutable commit identifiers.
8. Scan the image before publishing it to a registry.

## Local validation example
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest -q
docker build -t portfolio-api:local .
docker run --rm -p 8000:8000 portfolio-api:local
curl -fsS http://localhost:8000/health
```

## Operational requirements
- Graceful shutdown and structured logs.
- No secrets baked into image layers.
- Non-root runtime user.
- Resource limits when deployed to Kubernetes.
- Clear distinction between liveness and readiness checks.

## Acceptance criteria
- Tests pass from a clean environment.
- Image starts without privileged mode.
- Health endpoint returns a successful status.
- Image can be run locally and later deployed by the Helm project.

## Next improvements
Add OpenAPI contract tests, dependency vulnerability checks, OpenTelemetry traces, rate limiting and a non-root distroless runtime.
