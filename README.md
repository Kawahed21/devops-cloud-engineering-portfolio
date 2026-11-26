# DevOps & Cloud Engineering Portfolio

A hands-on portfolio of six infrastructure, platform engineering, CI/CD, security, observability and cloud-security labs. Each project is documented with its objective, architecture, prerequisites, implementation plan, validation, security considerations, cost controls and extension ideas.

> **Status and integrity:** This repository is a documented implementation portfolio. The project guides and starter configuration are committed here; cloud resources have not been provisioned and pipelines have not been executed by this repository publication. Follow each lab's validation steps and replace example values before deployment. Never commit credentials, private keys, tokens, tenant secrets or real customer data.

## Projects

| # | Project | Primary technologies | Outcome |
|---|---|---|---|
| 01 | [Terraform AWS Foundation](projects/01-terraform-aws-foundation/README.md) | Terraform, AWS VPC, subnets, routing, NAT, IAM | Reproducible network foundation |
| 02 | [Containerized Python Microservice](projects/02-containerized-microservice/README.md) | Python, Docker, pytest, GitHub Actions | Tested API image and CI workflow |
| 03 | [Kubernetes Helm Platform](projects/03-kubernetes-helm-platform/README.md) | Kubernetes, Helm, probes, resources | Deployable and configurable workload |
| 04 | [DevSecOps Pipeline](projects/04-devsecops-pipeline/README.md) | GitHub Actions, Trivy, Checkov, Gitleaks | Security gates across source, IaC and images |
| 05 | [Observability Stack](projects/05-observability-stack/README.md) | Prometheus, Grafana, Alertmanager | Metrics, dashboards and actionable alerts |
| 06 | [Azure Sentinel Detection Lab](projects/06-azure-sentinel-detection-lab/README.md) | Microsoft Sentinel, KQL, sample events | Documented analytics-rule lab |

## Suggested learning and delivery order

1. Build the AWS network foundation and understand routing/security boundaries.
2. Build, test and containerize the sample API.
3. Deploy it to local Kubernetes using Helm.
4. Add security checks to the CI workflow.
5. Instrument the service and validate alert rules.
6. Explore Sentinel KQL using synthetic events in a non-production workspace.

## Repository layout

```text
.
├── projects/
│   ├── 01-terraform-aws-foundation/
│   ├── 02-containerized-microservice/
│   ├── 03-kubernetes-helm-platform/
│   ├── 04-devsecops-pipeline/
│   ├── 05-observability-stack/
│   └── 06-azure-sentinel-detection-lab/
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
