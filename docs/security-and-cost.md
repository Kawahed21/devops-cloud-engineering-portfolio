# Security and Cost Guardrails

## Secrets
- Do not store cloud credentials, access keys, kubeconfigs, private keys, tokens or real environment files in Git.
- Use GitHub Actions secrets or a cloud-native secret manager for deployment credentials.
- Rotate any credential accidentally committed; deleting the file in a later commit does not revoke it.

## Infrastructure
- Use least-privilege IAM policies and security groups.
- Restrict SSH/RDP and administrative endpoints to trusted networks; prefer managed access mechanisms.
- Keep private workloads in private subnets and expose only required endpoints.
- Review Terraform plans and resource destruction carefully.

## Containers and Kubernetes
- Use minimal, maintained base images and scan them.
- Run containers as non-root where practical.
- Set CPU/memory requests and limits.
- Avoid plaintext Kubernetes Secrets in committed manifests.
- Apply network policies and RBAC appropriate to the cluster.

## Cost
- NAT Gateways, load balancers, managed Kubernetes clusters, log ingestion and always-on VMs can incur charges.
- Prefer local tools (LocalStack, kind, minikube, Docker) for learning where possible.
- Set budgets/alerts before provisioning cloud resources.
- Destroy temporary resources after each lab and verify that disks, IPs, snapshots and logs are not left behind.

## Data handling
All sample events and configuration in this repository are synthetic examples. Do not replace them with personal data, customer logs or production secrets.
