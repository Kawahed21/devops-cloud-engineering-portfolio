# Portfolio Roadmap

## Delivery phases

### Phase 1: Infrastructure as Code
- Define a VPC, public and private subnets across two Availability Zones.
- Add Internet Gateway, route tables and NAT egress.
- Parameterize CIDRs, region, environment and availability zones.
- Review the plan before apply; destroy lab resources after validation.

### Phase 2: Application container
- Implement a minimal HTTP API with a health endpoint.
- Add unit tests and a deterministic Docker build.
- Run tests before building/publishing an image.
- Add image tagging by commit SHA; avoid relying only on `latest`.

### Phase 3: Kubernetes packaging
- Package the application with Helm.
- Configure replicas, probes, requests/limits and service exposure.
- Validate install, upgrade, rollback and uninstall on a local cluster.

### Phase 4: Secure delivery
- Scan source secrets, dependencies, container image and IaC.
- Make findings visible in CI and document accepted exceptions.
- Pin third-party actions to reviewed versions or immutable SHAs.

### Phase 5: Observability
- Expose application metrics.
- Scrape metrics with Prometheus.
- Visualize service health and latency in Grafana.
- Route actionable alerts through Alertmanager.

### Phase 6: Cloud security analytics
- Learn Sentinel tables and KQL using synthetic events.
- Build detections with clear intent, entity mapping and severity.
- Test queries against sample data before enabling production rules.

## Evidence to add after each lab
- Architecture diagram and deployment topology.
- Sanitized command output and test reports.
- Screenshots of dashboards or successful deployments.
- Cost estimate and cleanup evidence.
- Known limitations and follow-up improvements.

Do not claim a project is deployed or production-ready until the implementation has been executed, tested and reviewed.
