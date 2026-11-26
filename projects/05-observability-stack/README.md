# Prometheus and Grafana Observability Lab

## Start the stack
From this directory, set a non-default Grafana password and start the services:

```bash
export GRAFANA_ADMIN_PASSWORD='replace-with-a-strong-local-password'
docker compose config
docker compose up --build -d
```

- API health: http://localhost:8000/health
- API metrics: http://localhost:8000/metrics
- Prometheus targets: http://localhost:9090/targets
- Grafana: http://localhost:3000 (user: `admin`; password: `GRAFANA_ADMIN_PASSWORD`)

The dashboard and Prometheus datasource are provisioned from the checked-in files. Do not use the example fallback password outside an isolated local lab.

## Generate requests and inspect metrics

```bash
for i in $(seq 1 20); do curl -fsS http://localhost:8000/health >/dev/null; done
curl -fsS http://localhost:8000/metrics
```

Prometheus scrapes the API by Compose service DNS name and loads alert rules from `prometheus/alerts.yml`. The rules detect a missing scrape target and a sustained HTTP 5xx ratio above five percent; they are evaluated by Prometheus but no Alertmanager notification receiver is configured in this lab. Stop the stack with:

```bash
docker compose down
```

## PromQL examples

Request rate:

```promql
sum(rate(portfolio_http_requests_total[5m]))
```

95th percentile request duration:

```promql
histogram_quantile(0.95, sum by (le) (rate(portfolio_http_request_duration_seconds_bucket[5m])))
```

## Validation
The CI integration test builds the API image, starts API/Prometheus/Grafana with Docker Compose, checks API health and metrics, verifies Prometheus reports the API target as up, and checks Grafana health. The local YAML/JSON configuration checks are also run separately.

## Production follow-up
Alertmanager routing/notification receivers, persistent volumes, TLS, authentication hardening, retention policies and dashboards-as-code review remain production follow-up work.
