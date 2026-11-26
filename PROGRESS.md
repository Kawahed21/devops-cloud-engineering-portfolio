# Portfolio Implementation Progress

Last updated: 2026-11-26

This tracker distinguishes committed implementation from validation actually executed. No cloud deployment is performed automatically.

## Project status

| # | Project | Implementation committed | Validation status |
|---|---|---|---|
| 01 | AWS Terraform foundation | VPC, public/private subnets across two AZs, IGW, route tables, optional NAT, restricted default SG, optional CloudWatch VPC Flow Logs with IAM role/policy | Earlier Terraform formatting passed. Latest flow-log addition and Checkov scan have not yet been rerun. No AWS plan/apply. |
| 02 | FastAPI container | Health/readiness API, Prometheus metrics, Dockerfile and pytest suite | 3 tests passed locally; earlier GitHub Actions Python job passed. Docker build/runtime not yet verified end-to-end. |
| 03 | Kubernetes Helm | Deployment, Service, probes, resources and hardened pod security context | Earlier Helm lint and template render passed. No cluster deployment. |
| 04 | DevSecOps pipeline | Gitleaks, Checkov and Trivy image scanning | Gitleaks passed. Latest recorded Checkov failed only on missing VPC Flow Logs; those resources have now been added. Trivy action reference was invalid and has been updated to released tag `v0.36.0`. Both fixes await a manual pipeline run. |
| 05 | Observability | Prometheus, alert rules, Docker Compose and Grafana provisioning/dashboard | YAML and JSON parsing passed; dashboard has four panels. Docker Compose integration not yet run. |
| 06 | Azure Sentinel detection | Failed-sign-in and rare-IP KQL examples | Requires a compatible Sentinel workspace and synthetic events; not executed. |
| 07 | Secure AI agent runtime | Planner protocol, allowlisted tool execution, bounded steps, execution trace and deterministic tools | Four pytest cases committed; CI job added, execution pending. No external model provider or side-effecting tools connected. |
| 08 | RAG knowledge assistant | Chunking, embedder/generator protocols, cosine retrieval, top-k context and source attribution | Four pytest cases committed; CI job added, execution pending. In-memory index and deterministic test adapters only; no production model/vector DB. |
| 09 | AWS serverless platform | API Gateway HTTP API, Python Lambda, DynamoDB, Terraform, least-privilege write role and encryption/PITR | Five Lambda handler tests committed; CI job added, execution pending. Terraform validation pending; no AWS deployment. |
| 10 | Azure Container Apps platform | Resource group, Log Analytics, Container Apps environment/app, ingress and bounded scaling via Terraform | Terraform formatting/provider validation pending. No Azure plan/apply or live endpoint test. |

## Pipeline controls

- Both `.github/workflows/ci.yml` and `.github/workflows/security.yml` now use `workflow_dispatch` only.
- Pushes and pull requests no longer launch repeated pipeline runs while implementation is in progress.
- The manual CI workflow now includes documentation checks, existing API tests, AI-agent tests, RAG tests, AWS Lambda tests, Terraform formatting/validation and Helm lint/render.
- The manual security workflow scans repository secrets, Terraform files across the repository, and the container image.
- Run the workflows manually once the implementation batch is ready; do not treat unexecuted workflows as passing.

## Previous CI evidence

- Portfolio CI run `45864502079` passed on commit `70f888e4`, before the new AI/RAG/AWS/Azure projects were added.
- DevSecOps run `45864502176` failed: Gitleaks passed; Checkov flagged VPC Flow Logs as missing; Trivy action tag `0.33.1` could not be resolved. Flow Logs support and a valid Trivy action release tag have since been committed but not rerun.
- Earlier CI run `45864408011` passed documentation, Python API tests, Terraform formatting and Helm lint/render for the earlier six-project baseline.

## Remaining validation and engineering work

1. Run Python tests for projects 07, 08 and 09; fix any failures.
2. Run Terraform fmt/init/validate for projects 01, 09 and 10; resolve provider/schema issues.
3. Run Checkov across all Terraform projects and fix findings rather than suppressing them without justification.
4. Run Trivy against the built API image and resolve critical/high vulnerabilities or document accepted exceptions.
5. Run Docker Compose integration tests for the observability stack.
6. Add retrieval evaluation and persistent vector storage to the RAG project; optional OpenAI adapters are committed but have not been tested against a live account.
7. Validate Sentinel KQL using synthetic records in a test workspace.
8. Add Azure/AWS deployment workflows using OIDC/federated identity, approval gates and teardown guidance; do not provision resources without explicit approval.
9. Add screenshots, test reports and deployment evidence only after actual runs.

## Environment limitations

The local execution container cannot clone GitHub and does not have Terraform, Helm or Docker installed. GitHub Actions is configured as the validation environment. Cloud-dependent tests require separately authorized AWS/Azure environments.

## Cost and security guardrails

No billable AWS or Azure resources are created by these commits. NAT Gateways, CloudWatch Flow Logs, DynamoDB, Log Analytics and Container Apps can incur charges. Cloud apply/deploy operations require explicit approval and cost review. Never commit credentials, tokens, Terraform state, kubeconfigs or customer data.
