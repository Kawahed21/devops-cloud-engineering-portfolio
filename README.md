# DevOps & Cloud Engineering Portfolio

A hands-on portfolio of ten infrastructure, platform engineering, CI/CD, security, observability, AI engineering and cloud labs. Each project is documented with its objective, architecture, prerequisites, implementation plan, validation, security considerations, cost controls and extension ideas.

> **Status and integrity:** This repository is a documented implementation portfolio. Code, tests and infrastructure definitions are committed here. Validation evidence is tracked in [PROGRESS.md](PROGRESS.md). Cloud resources have not been provisioned; AWS/Azure plans and live deployments require separate credentials and explicit cost approval. Follow each lab's validation steps and replace example values before deployment. Never commit credentials, private keys, tokens, tenant secrets or real customer data.

## Projects

| # | Project | Primary technologies | Outcome |
|---|---|---|---|
| 01 | [Terraform AWS Foundation](projects/01-terraform-aws-foundation/README.md) | Terraform, AWS VPC, subnets, routing, NAT, IAM | Reproducible network foundation |
| 02 | [Containerized Python Microservice](projects/02-containerized-microservice/README.md) | Python, Docker, pytest, GitHub Actions | Tested API image and CI workflow |
| 03 | [Kubernetes Helm Platform](projects/03-kubernetes-helm-platform/README.md) | Kubernetes, Helm, probes, resources | Deployable and configurable workload |
| 04 | [DevSecOps Pipeline](projects/04-devsecops-pipeline/README.md) | GitHub Actions, Trivy, Checkov, Gitleaks | Security gates across source, IaC and images |
| 05 | [Observability Stack](projects/05-observability-stack/README.md) | Prometheus, Grafana, Alertmanager | Metrics, dashboards and actionable alerts |
| 06 | [Azure Sentinel Detection Lab](projects/06-azure-sentinel-detection-lab/README.md) | Microsoft Sentinel, KQL, sample events | Detection engineering lab with KQL examples |\n| 07 | [Secure AI Agent Runtime](projects/07-ai-agent-platform/README.md) | Python, tool allowlists, bounded execution, pytest | Auditable tool-using agent foundation |\n| 08 | [RAG Knowledge Assistant](projects/08-rag-knowledge-assistant/README.md) | Python, chunking, embeddings interface, retrieval | Testable retrieval-augmented generation core |\n| 09 | [AWS Serverless Platform](projects/09-aws-serverless-platform/README.md) | API Gateway, Lambda, DynamoDB, Terraform | Serverless HTTP API with least-privilege IAM |\n| 10 | [Azure Container Apps Platform](projects/10-azure-container-apps-platform/README.md) | Azure Container Apps, Log Analytics, Terraform | Container platform with bounded scaling and logging |

## Suggested learning and delivery order

1. Build the AWS network foundation and understand routing/security boundaries.
2. Build, test and containerize the sample API.
3. Deploy it to local Kubernetes using Helm.
4. Add security checks to the CI workflow.
5. Instrument the service and validate alert rules.
6. Explore Sentinel KQL using synthetic events in a non-production workspace.\n7. Extend the secure agent runtime with an approved model provider and tool evaluation harness.\n8. Connect the RAG core to a persistent vector store and evaluate retrieval quality.\n9. Deploy the AWS serverless sample only after reviewing the plan and estimated charges.\n10. Deploy the Azure Container Apps sample only after reviewing the plan, identity and ingress security.

## Repository layout

```text
.
├── projects/
│   ├── 01-terraform-aws-foundation/
│   ├── 02-containerized-microservice/
│   ├── 03-kubernetes-helm-platform/
│   ├── 04-devsecops-pipeline/
│   ├── 05-observability-stack/
│   ├── 06-azure-sentinel-detection-lab/\n│   ├── 07-ai-agent-platform/\n│   ├── 08-rag-knowledge-assistant/\n│   ├── 09-aws-serverless-platform/\n│   └── 10-azure-container-apps-platform/
├── docs/
│   ├── portfolio-roadmap.md
│   └── security-and-cost.md
└── .github/workflows/
    └── ci.yml
```

## About

This portfolio demonstrates practical DevOps and cloud engineering patterns relevant to AWS, Azure, Linux, Docker, Kubernetes, Terraform, CI/CD, monitoring and security. It is intended as a lab and a foundation for iterative, evidence-backed project work.

## License

MIT. See [LICENSE](LICENSE).
