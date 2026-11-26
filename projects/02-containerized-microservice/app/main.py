from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI(title="Portfolio API", version="1.0.0")
REQUESTS = Counter("portfolio_http_requests_total", "HTTP requests", ["method", "path", "status"])
LATENCY = Histogram("portfolio_http_request_duration_seconds", "HTTP request duration")

@app.middleware("http")
async def collect_metrics(request: Request, call_next):
    with LATENCY.time():
        response = await call_next(request)
    REQUESTS.labels(request.method, request.url.path, str(response.status_code)).inc()
    return response

@app.get("/", tags=["service"])
def root():
    return {"service": "portfolio-api", "status": "ok", "version": app.version}

@app.get("/health", tags=["operations"])
def health():
    return {"status": "healthy"}

@app.get("/ready", tags=["operations"])
def ready():
    return {"status": "ready"}

@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
