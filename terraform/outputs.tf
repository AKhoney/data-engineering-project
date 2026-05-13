output "resource_group_id" {
  description = "ID of the created resource group"
  value       = azurerm_resource_group.weather_rg.id
}

output "storage_account_id" {
  description = "ID of the ADLS storage account"
  value       = azurerm_storage_account.weather_adls.id
}

output "storage_account_name" {
  description = "Name of the ADLS storage account"
  value       = azurerm_storage_account.weather_adls.name
}

output "adls_endpoint" {
  description = "Primary ADLS endpoint"
  value       = azurerm_storage_account.weather_adls.primary_dfs_endpoint
}

output "container_id" {
  description = "ID of the ADLS container"
  value       = azurerm_storage_data_lake_gen2_filesystem.weather_container.id
}

output "keyvault_id" {
  description = "ID of the Key Vault"
  value       = azurerm_key_vault.weather_kv.id
}

output "keyvault_uri" {
  description = "URI of the Key Vault"
  value       = azurerm_key_vault.weather_kv.vault_uri
}

output "sql_server_id" {
  description = "ID of the SQL Server"
  value       = azurerm_mssql_server.weather_sql.id
}

output "sql_server_name" {
  description = "Name of the SQL Server"
  value       = azurerm_mssql_server.weather_sql.name
}

output "sql_server_fqdn" {
  description = "Fully Qualified Domain Name of the SQL Server"
  value       = azurerm_mssql_server.weather_sql.fully_qualified_domain_name
}

output "sql_database_id" {
  description = "ID of the SQL Database"
  value       = azurerm_mssql_database.weather_db.id
}

output "adf_id" {
  description = "ID of Azure Data Factory"
  value       = azurerm_data_factory.weather_adf.id
}

output "adf_name" {
  description = "Name of Azure Data Factory"
  value       = azurerm_data_factory.weather_adf.name
}

output "adls_paths" {
  description = "Created ADLS paths"
  value = {
    staging = azurerm_storage_data_lake_gen2_path.staging.path
    bronze  = azurerm_storage_data_lake_gen2_path.bronze.path
    silver  = azurerm_storage_data_lake_gen2_path.silver.path
    gold    = azurerm_storage_data_lake_gen2_path.gold.path
    archive = azurerm_storage_data_lake_gen2_path.archive.path
  }
}

output "connection_strings" {
  description = "Connection information (DO NOT share in public repo)"
  value = {
    adls_account_name = azurerm_storage_account.weather_adls.name
    sql_server_fqdn   = azurerm_mssql_server.weather_sql.fully_qualified_domain_name
    keyvault_name     = azurerm_key_vault.weather_kv.name
  }
  sensitive = true
}
