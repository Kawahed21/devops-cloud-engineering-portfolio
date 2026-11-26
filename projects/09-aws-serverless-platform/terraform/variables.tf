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
