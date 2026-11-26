# 04 — DevSecOps Pipeline

## Objective
Introduce automated security checks into CI so insecure source, exposed secrets, vulnerable container images and risky Terraform configuration are detected before release.

## Security controls
| Layer | Tool | Purpose |
|---|---|---|
| Source secrets | Gitleaks | Detect accidentally committed credentials |
| Infrastructure as Code | Checkov | Evaluate Terraform configuration |
| Container image | Trivy | Scan OS packages and application dependencies |
| Dependencies | pip-audit / Trivy | Identify known vulnerable packages |

## Pipeline stages
1. Checkout source.
2. Install dependencies and run unit tests.
3. Run Gitleaks against repository history/source.
4. Run Checkov on Terraform directories.
5. Build the container image.
6. Run Trivy image scan with a documented severity threshold.
7. Publish only after required checks pass and credentials are available.

## Policy decisions
- Fail builds on confirmed leaked secrets.
- Fail on critical vulnerabilities according to the team's risk policy.
- Review high findings and document exceptions with owner, rationale and expiry.
- Do not suppress findings globally just to obtain a green build.
- Pin actions to reviewed versions or immutable commit SHAs in hardened pipelines.

## Local examples
```bash
gitleaks detect --source . --no-git
checkov -d projects/01-terraform-aws-foundation
trivy fs --scanners vuln,misconfig,secret .
trivy image --severity HIGH,CRITICAL portfolio-api:local
```

## Acceptance criteria
- CI runs on pull requests and pushes to the default branch.
- Security checks produce readable logs.
- Secret findings block the pipeline.
- IaC and image scan scope is explicit.
- Exceptions are traceable and time-bound.

## Next improvements
Add SBOM generation, image signing with Cosign, provenance attestations, SLSA controls, OPA policies and deployment admission checks.
