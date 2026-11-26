# Portfolio Implementation Progress

Last updated: 2026-11-26

This tracker separates committed code from validations actually executed. Cloud deployment is intentionally not performed automatically.

| Project | Committed implementation | Validation evidence / remaining |
|---|---|---|
| 01 AWS Terraform | VPC, two public/private AZ subnets, IGW, public/private route tables, optional AZ-local NAT Gateways, variables and outputs | Terraform CLI is unavailable in this execution environment; fmt/validate/plan remain pending. NAT is disabled by default to avoid accidental charges. |
| 02 FastAPI container | API root, health/readiness, Prometheus metrics, Dockerfile, requirements and pytest suite | **Passed:** `pytest -q` — 3 passed in 0.31s using the exact committed app and test source in an isolated local test directory. Docker image build not run (Docker CLI unavailable). |
| 03 Kubernetes Helm | Deployment, Service, probes, resource controls and pod hardening | Helm lint/render not run (Helm CLI unavailable). |
| 04 DevSecOps | GitHub Actions workflow for Gitleaks, Checkov and Trivy; CI workflow includes API tests, Terraform format and Helm checks | Workflow execution pending GitHub Actions. |
| 05 Observability | Prometheus scrape config, alert rules and Docker Compose stack | **Passed:** YAML parse checks for Compose, Prometheus scrape config and alert rules using PyYAML. Docker Compose/Prometheus runtime validation not run (Docker CLI unavailable). |
| 06 Azure Sentinel | Failed-sign-in and low-frequency IP KQL examples with workspace guidance | Requires compatible Log Analytics/Sentinel workspace and sample events; not executed. |

## Outstanding work
- Inspect GitHub Actions results and fix any failed jobs.
- Run Terraform fmt/validate with Terraform CLI and provider initialization.
- Run Helm lint/template with Helm CLI and deploy only to a disposable cluster after image publication.
- Add Grafana dashboard provisioning and Alertmanager receiver configuration.
- Validate KQL against synthetic records in a test workspace.
- Add sanitized screenshots and deployment evidence only after actual execution.

## Environment limitations
The execution container could not resolve github.com for a git clone and does not have Terraform, Helm or Docker installed. GitHub connector writes were used to commit the project files. This prevents local Docker, Helm and Terraform execution in this run; those checks are included in GitHub Actions where applicable.

## Cloud safety
No billable AWS or Azure resources are created by this automation. AWS apply and Sentinel workspace ingestion require separate cost review and explicit approval. Never commit secrets, Terraform state, kubeconfigs, tokens or customer data.
