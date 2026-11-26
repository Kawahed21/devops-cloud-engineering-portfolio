variable "aws_region" {
  description = "AWS region for the lab"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Short resource name prefix"
  type        = string
  default     = "portfolio-lab"
}

variable "vpc_cidr" {
  description = "Non-overlapping VPC IPv4 CIDR"
  type        = string
  default     = "10.40.0.0/16"
}

variable "availability_zones" {
  description = "Explicit AZ names to keep the deployment topology deterministic"
  type        = list(string)
  default     = ["ap-south-1a", "ap-south-1b"]
  validation {
    condition     = length(var.availability_zones) == 2
    error_message = "Provide exactly two availability zone names."
  }
}

variable "enable_nat_gateways" {
  description = "Create one NAT Gateway per AZ; incurs hourly and data charges"
  type        = bool
  default     = false
}
