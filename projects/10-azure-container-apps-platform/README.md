# 10: Azure Container Apps Platform

## Objective
Provision a minimal Azure Container Apps environment using Terraform, backed by Log Analytics for platform logs. The sample uses Microsoft's public hello-world container image and scale-to-zero configuration.

## Architecture
- Resource Group for isolation and lifecycle management.
- Log Analytics workspace with configurable retention.
- Container Apps managed environment connected to Log Analytics.
- Container App with external HTTP ingress, one active revision and bounded replica settings.

## Prerequisites
- Azure subscription and Azure CLI.
- Terraform 1.5+.
- Permission to create resource groups, Log Analytics workspaces and Container Apps resources.

## Validate without deploying
```bash
az login
az account show
export TF_VAR_subscription_id="$(az account show --query id -o tsv)"
cd terraform
terraform init
terraform fmt -check
terraform validate
terraform plan
```

Terraform plan may require provider downloads and an authenticated subscription context. No apply is performed by CI.

## Deploy and clean up (manual)
Review the plan and regional pricing first. If approved, run `terraform apply`, verify the app URL, then run `terraform destroy` and confirm the resource group is removed. Log Analytics ingestion/retention and Container Apps compute may incur charges.

## Security considerations
- The sample is intentionally public and unauthenticated; do not deploy sensitive workloads with this ingress configuration.
- Add authentication, managed identity, private networking, ingress restrictions and image provenance before production.
- Replace the hello-world image with an immutable digest from a trusted registry.
- Use federated workload identity for CI; do not store service-principal secrets in source control.
- Keep subscription ID in an environment variable or secure CI variable, not a committed tfvars file.

## Validation boundary
This project provides infrastructure code and a deployment runbook. A real Azure plan/apply and live endpoint test require an authorized subscription and cost approval. No Azure resources are created automatically.
