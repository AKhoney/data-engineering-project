"""Configuration Management Module"""

import os
from dotenv import load_dotenv
from typing import Dict, Any
import yaml

load_dotenv()


class Config:
    """Base configuration class"""

    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    # Azure Configuration
    AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID", "dummy-subscription-id")
    AZURE_RESOURCE_GROUP = os.getenv("AZURE_RESOURCE_GROUP", "dummy-resource-group")
    AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT", "dummystorageaccount")
    AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY", "dummy-storage-key")

    # ADLS Configuration
    ADLS_ACCOUNT_NAME = os.getenv("ADLS_ACCOUNT_NAME", "dummy_adls_account")
    ADLS_CONTAINER = os.getenv("ADLS_CONTAINER", "dummy_container")
    ADLS_STAGING_PATH = os.getenv("ADLS_STAGING_PATH", "/staging/weather")
    ADLS_BRONZE_PATH = os.getenv("ADLS_BRONZE_PATH", "/bronze/weather")
    ADLS_SILVER_PATH = os.getenv("ADLS_SILVER_PATH", "/silver/weather")
    ADLS_GOLD_PATH = os.getenv("ADLS_GOLD_PATH", "/gold/weather")
    ADLS_ARCHIVE_PATH = os.getenv("ADLS_ARCHIVE_PATH", "/archive/weather")

    # Databricks Configuration
    DATABRICKS_HOST = os.getenv("DATABRICKS_HOST", "https://adb-dummy.azuredatabricks.net")
    DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN", "dummy-token")
    DATABRICKS_CLUSTER_ID = os.getenv("DATABRICKS_CLUSTER_ID", "dummy-cluster-id")

    # Database Configuration
    DB_SERVER = os.getenv("DB_SERVER", "dummy-server.database.windows.net")
    DB_NAME = os.getenv("DB_NAME", "weather_db")
    DB_USER = os.getenv("DB_USER", "dummy_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "dummy_password")

    # Key Vault
    KEY_VAULT_NAME = os.getenv("KEY_VAULT_NAME", "dummy-keyvault")

    # API Configuration
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "dummy-api-key")
    API_RATE_LIMIT = int(os.getenv("API_RATE_LIMIT", "100"))
    API_TIMEOUT_SECONDS = int(os.getenv("API_TIMEOUT_SECONDS", "30"))

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = os.getenv("LOG_FORMAT", "json")

    # Application Insights
    APPINSIGHTS_INSTRUMENTATION_KEY = os.getenv(
        "APPINSIGHTS_INSTRUMENTATION_KEY", "dummy-instrumentation-key"
    )

    # Data Processing
    SPARK_MASTER = os.getenv("SPARK_MASTER", "local[*]")
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))

    # Archive Configuration
    ARCHIVE_FREQUENCY = os.getenv("ARCHIVE_FREQUENCY", "month-end")  # month-end, weekend
    ARCHIVE_RETENTION_DAYS = int(os.getenv("ARCHIVE_RETENTION_DAYS", "730"))  # 2 years

    # Data Quality
    QUALITY_CHECK_ENABLED = os.getenv("QUALITY_CHECK_ENABLED", "true").lower() == "true"
    DUPLICATE_CHECK_ENABLED = os.getenv("DUPLICATE_CHECK_ENABLED", "true").lower() == "true"

    @staticmethod
    def load_env_config(env: str = None) -> Dict[str, Any]:
        """Load environment-specific configuration from YAML"""
        env = env or Config.ENVIRONMENT
        config_path = f"config/{env}-config.yaml"

        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}

    @staticmethod
    def get_adls_connection_string() -> str:
        """Generate ADLS connection string (for reference only)"""
        return f"DefaultEndpointsProtocol=https;AccountName={Config.ADLS_ACCOUNT_NAME};AccountKey={Config.AZURE_STORAGE_KEY};EndpointSuffix=core.windows.net"

    @staticmethod
    def get_databricks_connection_config() -> Dict[str, str]:
        """Get Databricks connection configuration"""
        return {
            "host": Config.DATABRICKS_HOST,
            "token": Config.DATABRICKS_TOKEN,
            "cluster_id": Config.DATABRICKS_CLUSTER_ID,
        }

    @staticmethod
    def get_database_connection_string() -> str:
        """Generate database connection string"""
        return f"Driver={{ODBC Driver 17 for SQL Server}};Server={Config.DB_SERVER};Database={Config.DB_NAME};Uid={Config.DB_USER};Pwd={Config.DB_PASSWORD}"

    @classmethod
    def validate(cls) -> bool:
        """Validate critical configuration is set"""
        required_configs = [
            cls.ADLS_ACCOUNT_NAME,
            cls.DATABRICKS_HOST,
            cls.WEATHER_API_KEY,
        ]

        for config in required_configs:
            if config.startswith("dummy"):
                print(f"WARNING: Using dummy configuration. Please set actual values in .env file")
                return False
        return True
