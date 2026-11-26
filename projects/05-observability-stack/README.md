# Prometheus and Grafana Observability Lab

## Start
From this directory, set a non-default Grafana password and start the stack:
```bash
export GRAFANA_ADMIN_PASSWORD='replace-with-a-strong-local-password'
docker compose config
docker compose up --build
``
- API health: http://localhost:8000/health
- API metrics: http://localhost:8000/metrics
- Prometheus targets: http://localhost:9090/targets
- Grafana: http://localhost:3000 (user: admin; password: value of GRAFANA_ADMIN_PASSWORD)

The dashboard and Prometheus datasource are provisioned from the checked-in files. Do not use the example fallback password outside an isolated local lab.

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

This lab provisions a basic Grafana dashboard and Prometheus alerts. Alertmanager routing/notification receivers, persistent volumes, TLS and authentication hardening are production follow-up work.
