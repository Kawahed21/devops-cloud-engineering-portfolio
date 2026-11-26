variable "aws_region" {
  type        = string
  description = "AWS deployment region"
  default     = "ap-south-1"
}

variable "project_name" {
  type        = string
  description = "Lowercase resource prefix"
  default     = "portfolio-serverless"
}

variable "lambda_vpc_cidr" {
  description = "CIDR range for the private Lambda VPC"
  type        = string
  default     = "10.20.0.0/16"
}

variable "lambda_availability_zones" {
  description = "Two explicit Availability Zones for the private Lambda subnets"
  type        = list(string)
  default     = ["ap-south-1a", "ap-south-1b"]
  validation {
    condition     = length(var.lambda_availability_zones) == 2
    error_message = "Exactly two Lambda Availability Zones must be supplied."
  }
}
