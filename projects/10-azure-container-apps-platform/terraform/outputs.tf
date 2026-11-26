output "resource_group_name" {
  value = azurerm_resource_group.platform.name
}

output "container_app_url" {
  value = "https://${azurerm_container_app.hello.latest_revision_fqdn}"
}
