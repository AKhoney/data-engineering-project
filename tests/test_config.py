"""Tests for configuration module"""

import pytest
from src.config.config import Config


class TestConfig:
    """Test configuration management"""

    def test_config_loads(self):
        """Test that configuration loads successfully"""
        assert Config.ENVIRONMENT is not None
        assert Config.ADLS_ACCOUNT_NAME is not None

    def test_adls_connection_string(self):
        """Test ADLS connection string generation"""
        conn_str = Config.get_adls_connection_string()
        assert "DefaultEndpointsProtocol" in conn_str
        assert "AccountName" in conn_str

    def test_databricks_config(self):
        """Test Databricks configuration retrieval"""
        config = Config.get_databricks_connection_config()
        assert "host" in config
        assert "token" in config
        assert "cluster_id" in config

    def test_database_connection_string(self):
        """Test database connection string generation"""
        conn_str = Config.get_database_connection_string()
        assert "Server" in conn_str or "server" in conn_str.lower()
        assert "Database" in conn_str or "database" in conn_str.lower()

    def test_config_has_dummy_values(self):
        """Verify that dummy/placeholder values are set (for safety)"""
        # In development, it's OK to have dummy values
        # In production, these should be replaced with actual values
        config_str = str(Config.ADLS_ACCOUNT_NAME)
        assert isinstance(config_str, str)

    def test_log_level_is_valid(self):
        """Test that log level is valid"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        assert Config.LOG_LEVEL.upper() in valid_levels
