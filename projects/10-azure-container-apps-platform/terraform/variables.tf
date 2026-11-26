variable "subscription_id" {
  description = "Azure subscription ID supplied through TF_VAR_subscription_id"
  type        = string
  sensitive   = true
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "Central India"
}

variable "name_prefix" {
  description = "Globally unique lowercase prefix, 3-20 characters"
  type        = string
  default     = "portfolio-ca"
  validation {
    condition     = can(regex("^[a-z0-9-]{3,20}$", var.name_prefix))
    error_message = "name_prefix must be 3-20 lowercase letters, digits or hyphens."
  }
}

variable "log_retention_days" {
  type        = number
  description = "Log Analytics retention days"
  default     = 30
  validation {
    condition     = var.log_retention_days >= 30 && var.log_retention_days <= 730
    error_message = "Log retention must be between 30 and 730 days."
  }
}

variable "min_replicas" {
  type        = number
  description = "Minimum Container Apps replicas"
  default     = 0
  validation {
    condition     = var.min_replicas >= 0 && var.min_replicas <= var.max_replicas
    error_message = "min_replicas must be non-negative and no greater than max_replicas."
  }
}

variable "max_replicas" {
  type        = number
  description = "Maximum Container Apps replicas"
  default     = 2
  validation {
    condition     = var.max_replicas >= 1 && var.max_replicas <= 10
    error_message = "max_replicas must be between one and ten."
  }
}
