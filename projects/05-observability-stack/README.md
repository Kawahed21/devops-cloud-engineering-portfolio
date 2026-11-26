# Prometheus Observability Lab

## Start
From this directory:
```bash
docker compose config
docker compose up --build
``
- API health: http://localhost:8000/health
- API metrics: http://localhost:8000/metrics
- Prometheus targets: http://localhost:9090/targets

Generate requests:
```bash
for i in $(seq 1 20); do curl -fsS http://localhost:8000/health >/dev/null; done
``

Prometheus scrapes the API by Compose service DNS name and loads alert rules from `prometheus/alerts.yml`. Stop with `docker compose down`.

## PromQL examples
```promql
sum(rate(portfolio_http_requests_total[5m]))
``
```promql
histogram_quantile(0.95, sum by (le) (rate(portfolio_http_request_duration_seconds_bucket[5m])))
``

This starter includes Prometheus and alert rules. Grafana dashboards and Alertmanager notification receivers are follow-up work; do not call the stack production-ready until those are configured and tested.
