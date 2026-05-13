variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
  default     = "dummy-subscription-id-12345678-1234-1234-1234-123456789012"
}

variable "resource_group_name" {
  description = "Azure Resource Group name"
  type        = string
  default     = "rg-weather-data-engineering"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "East US"
}

variable "environment" {
  description = "Environment name (development, staging, production)"
  type        = string
  default     = "development"
}

variable "storage_account_name" {
  description = "Azure Storage Account name for ADLS Gen2"
  type        = string
  default     = "stweatherdataeng"
  validation {
    condition     = length(var.storage_account_name) <= 24
    error_message = "Storage account name must be less than 24 characters."
  }
}

variable "adls_container_name" {
  description = "ADLS container name"
  type        = string
  default     = "weather-data-lake"
}

variable "keyvault_name" {
  description = "Azure Key Vault name"
  type        = string
  default     = "kvweatherdataeng"
}

variable "sql_server_name" {
  description = "SQL Server name"
  type        = string
  default     = "sqlweatherdataeng"
}

variable "sql_database_name" {
  description = "SQL Database name"
  type        = string
  default     = "weather_db"
}

variable "adf_name" {
  description = "Azure Data Factory name"
  type        = string
  default     = "adfweatherdataeng"
}

variable "databricks_workspace_name" {
  description = "Databricks workspace name"
  type        = string
  default     = "dbxweatherdataeng"
}

variable "spark_cluster_name" {
  description = "Spark cluster name"
  type        = string
  default     = "cluster-weather-processing"
}

# Tags to apply to all resources
variable "common_tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    project    = "weather-data-engineering"
    managed_by = "terraform"
  }
}
