# 04 — DevSecOps Pipeline

## Objective
Introduce automated security checks into CI so insecure source, exposed secrets, vulnerable container images and risky Terraform configuration are detected before release.

## Security controls
| Layer | Tool | Purpose |
|---|---|---|
| Source secrets | Gitleaks | Detect accidentally committed credentials |
| Infrastructure as Code | Checkov | Evaluate Terraform configuration |
| Container image | Trivy | Scan OS packages and application dependencies |
| Dependencies | Trivy image scan | Identify known OS and installed-library vulnerabilities |

## Pipeline stages
1. Manually dispatch the workflow from GitHub Actions.
2. Run the project test suites in the validation workflow.
3. Run Gitleaks against repository history/source.
4. Run Checkov across Terraform directories.
5. Build the API container image.
6. Run Trivy against OS packages and installed libraries, failing on HIGH and CRITICAL findings.
7. Publish only after required checks pass and credentials are available. Image publishing is not configured in this repository.

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
- The current workflows use manual `workflow_dispatch` triggers; pushes and pull requests do not start scans automatically.
- Security checks produce readable logs.
- Secret findings block the pipeline.
- IaC and image scan scope is explicit.
- Exceptions are traceable and time-bound.

## Next improvements
Add SBOM generation, image signing with Cosign, provenance attestations, SLSA controls, OPA policies and deployment admission checks.
