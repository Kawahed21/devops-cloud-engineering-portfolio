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
