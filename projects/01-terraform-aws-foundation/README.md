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
          NAT Gateway A         (optional public tier)
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
- NAT strategy: one NAT per AZ for resilience, or one shared NAT for a lower-cost lab.

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
Add VPC endpoints, flow logs, centralized egress, Network Firewall, policy-as-code and remote state with locking.
