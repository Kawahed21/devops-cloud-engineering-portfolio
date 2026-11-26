# Portfolio Implementation Progress

Last updated: 2026-11-26

This tracker separates committed code from validations actually executed. Cloud deployment is intentionally not performed automatically.

| Project | Committed implementation | Validation evidence / remaining |
|---|---|---|
| 01 AWS Terraform | VPC, two public/private AZ subnets, IGW, public/private route tables, optional AZ-local NAT Gateways, restricted default security group, variables and outputs | GitHub Actions Terraform formatting job passed on commit `d5b94527`; Checkov initially found issues, which were addressed in later commits. Latest Checkov rerun pending. No AWS plan/apply run. |
| 02 FastAPI container | API root, health/readiness, Prometheus metrics, Dockerfile, requirements and pytest suite | **Passed locally:** `pytest -q` — 3 passed in 0.31s using exact committed app/test source. GitHub Actions Python test job also passed on `d5b94527`. Docker image build not run locally. |
| 03 Kubernetes Helm | Deployment, Service, probes, resource controls and pod hardening | GitHub Actions Helm lint and template-render jobs passed on `d5b94527`. No cluster deployment run. |
| 04 DevSecOps | Gitleaks, Checkov and Trivy GitHub Actions workflow | Gitleaks passed on earlier run. Checkov findings were addressed; Trivy action ref was corrected. Latest security workflow rerun pending. |
| 05 Observability | Prometheus scrape config, alert rules, Docker Compose, Grafana datasource/dashboard provisioning | **Passed:** YAML parsing for Compose, Prometheus scrape/alert config and Grafana provisioning; Grafana dashboard JSON parsed with 4 panels. Docker/Prometheus/Grafana runtime not run locally. |
| 06 Azure Sentinel | Failed-sign-in and low-frequency IP KQL examples with workspace guidance | Requires compatible Log Analytics/Sentinel workspace and synthetic sign-in events; not executed. |

## CI evidence
- Portfolio CI run `45864408011` completed successfully for commit `d5b94527`: documentation, Python API tests, Terraform formatting and Helm lint/render all passed.
- Later commits added Grafana assets and hardened Terraform/security workflows. Their CI/security runs are being checked separately; do not infer that the latest commit has passed until its runs complete.

## Outstanding work
- Verify latest GitHub Actions and DevSecOps run results; fix failures.
- Run Terraform provider validation/plan in an approved AWS environment (no apply without explicit cost approval).
- Run Docker Compose and Prometheus/Grafana integration tests.
- Validate KQL against synthetic records in a test Sentinel workspace.
- Add Alertmanager routing, persistent volumes and production auth/TLS controls.
- Add sanitized screenshots and deployment evidence only after actual execution.

## Environment limitations
The local execution container cannot resolve github.com for a git clone and does not have Terraform, Helm or Docker installed. GitHub Actions supplies Terraform/Helm validation and Python tests. Docker and cloud-dependent validation remain outstanding.

## Cloud safety
No billable AWS or Azure resources are created by this automation. AWS apply and Sentinel workspace ingestion require separate cost review and explicit approval. Never commit secrets, Terraform state, kubeconfigs, tokens or customer data.
