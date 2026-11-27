# DevOps & Cloud Engineering Portfolio

A hands-on portfolio of ten infrastructure, platform engineering, CI/CD, security, observability, AI engineering and cloud labs. Each project is documented with its objective, architecture, prerequisites, implementation, validation, security considerations, cost controls and extension ideas.

> **Status and integrity:** Code, tests and infrastructure definitions are committed here. Validation evidence is tracked in [PROGRESS.md](PROGRESS.md). Automated checks have passed as recorded in the tracker. Cloud resources have not been provisioned; AWS/Azure plans and live deployments require separate credentials and explicit cost approval. Never commit credentials, private keys, tokens, tenant secrets or real customer data.

## Projects

| # | Project | Primary technologies | Outcome |
|---|---|---|---|
| 01 | [Terraform AWS Foundation](projects/01-terraform-aws-foundation/README.md) | Terraform, AWS VPC, subnets, routing, NAT, IAM | Reproducible network foundation |
| 02 | [Containerized Python Microservice](projects/02-containerized-microservice/README.md) | Python, Docker, pytest, GitHub Actions | Tested API image and CI workflow |
| 03 | [Kubernetes Helm Platform](projects/03-kubernetes-helm-platform/README.md) | Kubernetes, Helm, probes, resources | Deployable and configurable workload |
| 04 | [DevSecOps Pipeline](projects/04-devsecops-pipeline/README.md) | GitHub Actions, Trivy, Checkov, Gitleaks | Security gates across source, IaC and images |
| 05 | [Observability Stack](projects/05-observability-stack/README.md) | Prometheus, Grafana, Docker Compose | Metrics, dashboards and actionable alerts |
| 06 | [Azure Sentinel Detection Lab](projects/06-azure-sentinel-detection-lab/README.md) | Microsoft Sentinel, KQL, synthetic fixtures, pytest | KQL contract tests and analyst detection guidance |
| 07 | [Secure AI Agent Runtime](projects/07-ai-agent-platform/README.md) | Python, OpenAI Responses API, tool allowlists | Bounded, auditable tool-using agent |
| 08 | [RAG Knowledge Assistant](projects/08-rag-knowledge-assistant/README.md) | Python, embeddings, retrieval, generation | Testable retrieval-augmented generation core |
| 09 | [AWS Serverless Platform](projects/09-aws-serverless-platform/README.md) | API Gateway, Lambda, DynamoDB, Terraform | Private-network serverless API with security controls |
| 10 | [Azure Container Apps Platform](projects/10-azure-container-apps-platform/README.md) | Azure Container Apps, Log Analytics, Terraform | Container platform with bounded scaling and logging |

## Suggested learning and delivery order

1. Build the AWS network foundation and understand routing/security boundaries.
2. Build, test and containerize the sample API.
3. Deploy it to local Kubernetes using Helm.
4. Add security checks to the CI workflow.
5. Instrument the service and validate alert rules.
6. Explore Sentinel KQL using synthetic events in a non-production workspace.
7. Extend the secure agent runtime with an approved model provider and tool evaluation harness.
8. Connect the RAG core to a persistent vector store and evaluate retrieval quality.
9. Deploy the AWS serverless sample only after reviewing the plan and estimated charges.
10. Deploy the Azure Container Apps sample only after reviewing the plan, identity and ingress security.

## Repository layout

```text
.
├── projects/
│   ├── 01-terraform-aws-foundation/
│   ├── 02-containerized-microservice/
│   ├── 03-kubernetes-helm-platform/
│   ├── 04-devsecops-pipeline/
│   ├── 05-observability-stack/
│   ├── 06-azure-sentinel-detection-lab/
│   ├── 07-ai-agent-platform/
│   ├── 08-rag-knowledge-assistant/
│   ├── 09-aws-serverless-platform/
│   └── 10-azure-container-apps-platform/
├── docs/
│   ├── portfolio-roadmap.md
│   └── security-and-cost.md
└── .github/workflows/
    ├── ci.yml
    ├── security.yml
    └── final-validation.yml
```

## Validation

The automated validation workflow runs on demand, and the Sentinel contract suite also runs when its project files or workflow change on `main`. See [PROGRESS.md](PROGRESS.md) for exact run IDs, test counts and remaining cloud/workspace-dependent work. Local Sentinel tests do not replace live KQL execution in a test workspace.

## About

This portfolio demonstrates practical DevOps and cloud engineering patterns relevant to AWS, Azure, Linux, Docker, Kubernetes, Terraform, CI/CD, monitoring, security and AI engineering. It is intended as an evidence-backed lab portfolio and a foundation for further iteration.

## License

MIT. See [LICENSE](LICENSE).
