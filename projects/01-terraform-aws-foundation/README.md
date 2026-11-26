# 01 — Terraform AWS Foundation

## Objective
Create a reusable AWS network foundation using Terraform: one VPC, public and private subnets across two Availability Zones, an Internet Gateway, route tables and controlled outbound access through NAT.

## Architecture

```text
                         Internet
                            |
                     Internet Gateway
                            |
                 +----------+----------+
                 |       VPC           |
                 |                     |
          Public subnet A       Public subnet B
          NAT Gateway A         NAT Gateway B
                 |                     |
          Private subnet A      Private subnet B
          App workloads         App workloads
                 |                     |
                 +---- outbound egress-+
```

## Prerequisites
- AWS account with permission to create VPC networking resources.
- AWS CLI configured with a least-privilege lab identity.
- Terraform 1.5+.
- A selected region with at least two available AZs.

## Inputs to define
- `aws_region`: deployment region.
- `project_name`: resource name prefix.
- `vpc_cidr`: non-overlapping VPC CIDR.
- `availability_zones`: two AZ names in the selected region.
- Public/private subnet CIDRs per AZ.
- `enable_nat_gateways`: create one NAT Gateway per AZ (default `false`; NAT Gateways incur hourly and data-processing charges).
- `enable_vpc_flow_logs`: create VPC Flow Logs in CloudWatch (default `false`; ingestion and retention incur charges).
- `flow_log_retention_days`: CloudWatch log retention (default 7 days).

## Implementation sequence
1. Configure the AWS provider and required Terraform version.
2. Create the VPC with DNS support and hostnames enabled.
3. Create two public and two private subnets.
4. Attach an Internet Gateway and associate public route tables.
5. Add private route tables and NAT egress routes.
6. Add outputs for VPC and subnet IDs.
7. Run `terraform fmt -check`, `terraform validate` and `terraform plan`.
8. Review the plan; apply only after confirming region, CIDRs and cost.
9. Verify routes and subnet associations in AWS.
10. Run `terraform destroy` after the lab and verify cleanup.

## Optional VPC Flow Logs
Enable flow logging for monitored environments by setting `enable_vpc_flow_logs = true`. The module creates a CloudWatch log group with configurable retention, a narrowly scoped IAM role/policy, and an `ALL`-traffic VPC Flow Log. Keep it disabled for cost-sensitive labs unless you explicitly need the telemetry. Example:

```hcl
enable_vpc_flow_logs    = true
flow_log_retention_days = 7
```

The CloudWatch log group and IAM resources are created only when the flag is enabled.

## Validation checklist
- [ ] No CIDR overlap with existing networks.
- [ ] Public subnets have a route to the Internet Gateway.
- [ ] Private subnets have no direct public IP assignment.
- [ ] Private egress follows the selected NAT design.
- [ ] No inbound administrative access is opened to the world.
- [ ] Terraform state is stored securely and never committed.

## Cost and trade-offs
NAT Gateways and public IPv4 addresses can incur ongoing charges. A single NAT reduces lab cost but creates an AZ dependency and cross-AZ traffic. For production, assess resilience, egress controls and cost together.

## Deliverables
Terraform modules, variable documentation, architecture diagram, plan review notes, deployment evidence and cleanup evidence.

## Next improvements
Add VPC endpoints, centralized egress, Network Firewall, policy-as-code and remote state with locking.
