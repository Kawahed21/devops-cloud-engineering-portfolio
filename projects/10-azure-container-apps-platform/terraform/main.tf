terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

resource "azurerm_resource_group" "platform" {
  name     = "${var.name_prefix}-rg"
  location = var.location
  tags     = local.tags
}

resource "azurerm_log_analytics_workspace" "platform" {
  name                = "${var.name_prefix}-logs"
  location            = azurerm_resource_group.platform.location
  resource_group_name = azurerm_resource_group.platform.name
  sku                 = "PerGB2018"
  retention_in_days   = var.log_retention_days
  tags                = local.tags
}

resource "azurerm_container_app_environment" "platform" {
  name                       = "${var.name_prefix}-env"
  location                   = azurerm_resource_group.platform.location
  resource_group_name        = azurerm_resource_group.platform.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.platform.id
  tags                       = local.tags
}

resource "azurerm_container_app" "hello" {
  name                         = "${var.name_prefix}-app"
  container_app_environment_id = azurerm_container_app_environment.platform.id
  resource_group_name          = azurerm_resource_group.platform.name
  revision_mode                = "Single"
  tags                         = local.tags

  template {
    min_replicas = var.min_replicas
    max_replicas = var.max_replicas
    container {
      name   = "hello"
      image  = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }

  ingress {
    external_enabled = true
    target_port      = 80
    transport        = "auto"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}

locals {
  tags = {
    Project     = var.name_prefix
    ManagedBy   = "Terraform"
    Environment = "lab"
  }
}
