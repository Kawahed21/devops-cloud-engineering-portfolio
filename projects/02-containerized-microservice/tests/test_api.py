from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_contract():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "portfolio-api"

def test_health_and_readiness():
    assert client.get("/health").json() == {"status": "healthy"}
    assert client.get("/ready").json() == {"status": "ready"}

def test_metrics_endpoint_exposes_prometheus_format():
    client.get("/health")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "portfolio_http_requests_total" in response.text
