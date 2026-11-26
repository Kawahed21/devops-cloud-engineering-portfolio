# Portfolio Implementation Progress

Last updated: 2026-11-26

Status reflects files committed to GitHub, not presumed deployment. Only record tests as passed after an actual test run or a successful GitHub Actions result.

| Project | Current implementation | Validation state |
|---|---|---|
| 01 AWS Terraform | VPC, two public/private AZ subnets, IGW, public/private route tables, optional AZ-local NAT Gateways, variables and outputs | Terraform CLI/provider validation pending |
| 02 FastAPI container | API, health/readiness endpoints, Prometheus metrics, Dockerfile, pytest tests | Local execution evidence pending; GitHub Actions CI should run tests |
| 03 Kubernetes Helm | Deployment, Service, probes, resource controls and pod hardening | Helm lint/render pending |
| 04 DevSecOps | Gitleaks, Checkov and Trivy GitHub Actions workflow | Workflow execution pending |
| 05 Observability | Prometheus scrape config, alert rules and Docker Compose | Compose and Prometheus config validation pending |
| 06 Azure Sentinel | Failed-sign-in and low-frequency IP KQL examples | Requires a compatible Log Analytics/Sentinel workspace |

## Outstanding work
- Run and fix all executable tests and static checks.
- Add Grafana provisioning/dashboard and Alertmanager routing.
- Validate Helm chart with Helm CLI and Terraform with Terraform CLI.
- Validate KQL against synthetic records in a test workspace.
- Review action pinning and supply-chain hardening.
- Add screenshots, sanitized run evidence and deployment notes only after execution.

## Cloud safety
No billable AWS or Azure resources are created by this repository automation. AWS apply and Sentinel workspace ingestion require separate cost review and explicit approval. Never commit secrets, Terraform state, kubeconfigs, tokens or customer data.
