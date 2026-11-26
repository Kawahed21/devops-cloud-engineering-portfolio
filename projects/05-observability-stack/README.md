# 05 — Observability Stack

## Objective
Collect application and infrastructure metrics, visualize service health and define actionable alerts using Prometheus, Grafana and Alertmanager.

## Architecture

```text
Python API /metrics
       |
   Prometheus ---- scrape / rules
       |                  |
    Grafana          Alertmanager
  dashboards          notifications
```

## Core service-level indicators
- Request rate (requests/second).
- Error ratio (5xx responses / total requests).
- Latency (p50, p95 and p99).
- Process/container CPU and memory.
- Availability from a synthetic health probe.

## Alert design principles
- Alert on user-visible symptoms, not every low-level fluctuation.
- Use a sustained evaluation window to reduce noise.
- Include severity, service, environment, summary and runbook link.
- Set ownership and an actionable response for every alert.
- Test firing and resolved notifications before relying on them.

## Example PromQL patterns
```promql
sum(rate(http_requests_total[5m]))
```

```promql
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
clamp_min(sum(rate(http_requests_total[5m])), 1)
```

```promql
histogram_quantile(
  0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)
```

Metric names depend on the instrumentation actually implemented by the service; adapt the queries to the exported metrics.

## Dashboard panels
1. Request throughput.
2. Error ratio.
3. Latency percentiles.
4. CPU and memory.
5. Instance/pod health.
6. Alert state and recent deployments.

## Acceptance criteria
- Prometheus successfully scrapes the target.
- Grafana dashboard shows populated time series.
- A controlled test condition fires an alert.
- Alert resolves after recovery.
- Runbook describes diagnosis and mitigation.

## Next improvements
Add OpenTelemetry traces, logs with Loki, exemplars, SLO/error-budget reporting and synthetic monitoring.
