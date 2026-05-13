terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }

  subscription_id = var.subscription_id
}

# Resource Group
resource "azurerm_resource_group" "weather_rg" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    project     = "weather-data-engineering"
    environment = var.environment
    managed_by  = "terraform"
  }
}

# Storage Account (ADLS Gen2)
resource "azurerm_storage_account" "weather_adls" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.weather_rg.name
  location                 = azurerm_resource_group.weather_rg.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  is_hns_enabled           = true  # Enable hierarchical namespace for ADLS

  tags = {
    project = "weather-data-engineering"
  }
}

# ADLS Container
resource "azurerm_storage_data_lake_gen2_filesystem" "weather_container" {
  name               = var.adls_container_name
  storage_account_id = azurerm_storage_account.weather_adls.id
}

# Key Vault
resource "azurerm_key_vault" "weather_kv" {
  name                = var.keyvault_name
  location            = azurerm_resource_group.weather_rg.location
  resource_group_name = azurerm_resource_group.weather_rg.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    key_permissions = [
      "Get",
      "List",
      "Create",
    ]

    secret_permissions = [
      "Get",
      "List",
      "Set",
      "Delete",
    ]
  }

  tags = {
    project = "weather-data-engineering"
  }
}

# SQL Server (Placeholder - do NOT deploy real credentials)
resource "azurerm_mssql_server" "weather_sql" {
  name                         = var.sql_server_name
  resource_group_name          = azurerm_resource_group.weather_rg.name
  location                     = azurerm_resource_group.weather_rg.location
  version                      = "12.0"
  administrator_login          = "dummy_admin"  # Placeholder
  administrator_login_password = "P@ssw0rd1234!"  # Placeholder - change in production

  tags = {
    project = "weather-data-engineering"
  }
}

# SQL Database
resource "azurerm_mssql_database" "weather_db" {
  name           = var.sql_database_name
  server_id      = azurerm_mssql_server.weather_sql.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  sku_name       = "Basic"  # Placeholder - upgrade in production
  max_size_gb    = 2

  tags = {
    project = "weather-data-engineering"
  }
}

# Data Lake Path Structure (Placeholder - actual paths managed via code)
resource "azurerm_storage_data_lake_gen2_path" "staging" {
  path               = "staging/weather"
  file_system_name   = azurerm_storage_data_lake_gen2_filesystem.weather_container.name
  storage_account_id = azurerm_storage_account.weather_adls.id
  resource           = "directory"
}

resource "azurerm_storage_data_lake_gen2_path" "bronze" {
  path               = "bronze/weather"
  file_system_name   = azurerm_storage_data_lake_gen2_filesystem.weather_container.name
  storage_account_id = azurerm_storage_account.weather_adls.id
  resource           = "directory"
}

resource "azurerm_storage_data_lake_gen2_path" "silver" {
  path               = "silver/weather"
  file_system_name   = azurerm_storage_data_lake_gen2_filesystem.weather_container.name
  storage_account_id = azurerm_storage_account.weather_adls.id
  resource           = "directory"
}

resource "azurerm_storage_data_lake_gen2_path" "gold" {
  path               = "gold/weather"
  file_system_name   = azurerm_storage_data_lake_gen2_filesystem.weather_container.name
  storage_account_id = azurerm_storage_account.weather_adls.id
  resource           = "directory"
}

resource "azurerm_storage_data_lake_gen2_path" "archive" {
  path               = "archive/weather"
  file_system_name   = azurerm_storage_data_lake_gen2_filesystem.weather_container.name
  storage_account_id = azurerm_storage_account.weather_adls.id
  resource           = "directory"
}

# Data Factory
resource "azurerm_data_factory" "weather_adf" {
  name                = var.adf_name
  location            = azurerm_resource_group.weather_rg.location
  resource_group_name = azurerm_resource_group.weather_rg.name

  tags = {
    project = "weather-data-engineering"
  }
}

# Data Factory Linked Service - ADLS (Placeholder)
resource "azurerm_data_factory_linked_service_data_lake_storage_gen2" "adls_link" {
  name                 = "LinkedService_ADLS"
  data_factory_id      = azurerm_data_factory.weather_adf.id
  service_principal_id = data.azurerm_client_config.current.client_id
  service_principal_key = "dummy_key"  # Placeholder
  tenant_id            = data.azurerm_client_config.current.tenant_id
  url                  = "https://${azurerm_storage_account.weather_adls.name}.dfs.core.windows.net"
}

# Data Factory Linked Service - SQL Database (Placeholder)
resource "azurerm_data_factory_linked_service_sql_server" "sql_link" {
  name                = "LinkedService_SQL"
  data_factory_id     = azurerm_data_factory.weather_adf.id
  connection_string   = "Server=dummy;Database=dummy;User ID=dummy;Password=dummy;"  # Placeholder
}

# Get current Azure context
data "azurerm_client_config" "current" {}
