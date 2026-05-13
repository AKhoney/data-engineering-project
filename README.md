# Weather Data Engineering Project

A professional, enterprise-grade data engineering project for collecting, processing, and analyzing weather data across USA and India. This project demonstrates modern data engineering practices using Azure Cloud services, Databricks, and Apache Spark.

## 📋 Project Overview

This project implements a complete data pipeline that:
- Ingests weather data from **live APIs** and **static files**
- Processes data for **countries, states, and major cities**
- Tracks multiple metrics: **temperature, humidity, wind, air quality, and more**
- Implements **Medallion Architecture** (Bronze → Silver → Gold layers)
- Manages **original and archive tables** with monthly/weekly archival
- Uses **Azure Data Factory** for orchestration
- Processes data with **Apache Spark & PySpark**
- Implements **enterprise-grade** logging, monitoring, error handling, and data quality

## 🏗️ Architecture

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                              │
├──────────────────────┬──────────────────────────────────────┤
│  Weather APIs        │  CSV/JSON Files                      │
│  (USA & India)       │  (Historical Data)                   │
└──────────────────────┴──────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         AZURE DATA FACTORY (Orchestration)                   │
│  - Copy Activities (API → Staging)                           │
│  - Lookup Activities (Aggregations)                          │
│  - Error Handling & Retry Logic                             │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            AZURE DATA LAKE STORAGE (ADLS)                    │
├──────────────┬────────────────┬─────────────┬────────────────┤
│   Staging    │   Bronze       │   Silver    │    Gold        │
│   (Raw)      │   (Raw Data)   │  (Cleaned)  │   (Insights)   │
└──────────────┴────────────────┴─────────────┴────────────────┘
       │              │              │              │
       │              ▼              ▼              ▼
       │         ┌──────────┐  ┌──────────┐  ┌──────────┐
       │         │ Original │  │ Original │  │ Original │
       │         │ Table    │  │ Table    │  │ Table    │
       │         └──────────┘  └──────────┘  └──────────┘
       │              │              │              │
       └──────────────┴──────────────┴──────────────┘
                      │
                      ▼
       ┌──────────────────────────────────────┐
       │   Archive Tables (Append Mode)       │
       │  - Historical Data                   │
       │  - Monthly/Weekly Archival           │
       └──────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│       DATABRICKS (Processing & Analytics)                    │
│  - PySpark Transformations                                   │
│  - Data Quality Validation                                   │
│  - State/City-level Aggregations                             │
└─────────────────────────────────────────────────────────────┘
```

### Medallion Architecture

```
BRONZE LAYER (Raw Data)
├── Original Table: Current week/month raw data
└── Archive Table: All historical raw data

SILVER LAYER (Cleaned & Validated)
├── Original Table: Current cleaned data
└── Archive Table: Historical cleaned data

GOLD LAYER (Business Ready Insights)
├── Original Table: Current insights & aggregations
├── Archive Table: Historical trends & patterns
├── Country-level aggregations
├── State-level aggregations
└── City-level aggregations
```

## 📁 Project Structure

```
data-engineering-weather/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── weather_client.py          # Weather API client
│   │   └── api_config.py              # API configuration
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── file_ingestion.py          # Read CSV/JSON files
│   │   └── api_ingestion.py           # Fetch from APIs
│   ├── transformations/
│   │   ├── __init__.py
│   │   ├── bronze_transformations.py  # Raw → Bronze
│   │   ├── silver_transformations.py  # Bronze → Silver
│   │   └── gold_transformations.py    # Silver → Gold
│   ├── validation/
│   │   ├── __init__.py
│   │   ├── data_quality.py            # Quality checks
│   │   ├── schema_validator.py        # Schema validation
│   │   └── anomaly_detection.py       # Data anomalies
│   ├── logging/
│   │   ├── __init__.py
│   │   └── logger.py                  # Structured logging
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config.py                  # Configuration management
│   │   └── constants.py               # Constants
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── spark_utils.py             # Spark helpers
│   │   ├── adls_utils.py              # ADLS operations
│   │   └── retry_logic.py             # Retry & backoff
│   └── archive/
│       ├── __init__.py
│       └── archive_manager.py         # Archive operations
├── terraform/
│   ├── main.tf                        # Main resources
│   ├── variables.tf                   # Variables & placeholders
│   ├── outputs.tf                     # Output values
│   ├── storage.tf                     # ADLS configuration
│   ├── databricks.tf                  # Databricks setup
│   ├── data_factory.tf                # ADF setup
│   ├── keyvault.tf                    # Key Vault
│   └── terraform.tfvars.example       # Example variables
├── adf-pipelines/
│   ├── pipeline-ingest-api.json       # ADF pipeline for API ingestion
│   ├── pipeline-ingest-files.json     # ADF pipeline for file ingestion
│   ├── pipeline-archive.json          # ADF pipeline for archival
│   ├── pipeline-master.json           # Master orchestration pipeline
│   └── linked-services-template.json  # Linked service templates
├── docs/
│   ├── ARCHITECTURE.md                # Detailed architecture
│   ├── SETUP_GUIDE.md                 # Setup instructions
│   ├── RUNBOOK.md                     # Operations runbook
│   ├── DATA_DICTIONARY.md             # Data schema documentation
│   ├── API_DOCUMENTATION.md           # API details
│   └── TROUBLESHOOTING.md             # Troubleshooting guide
├── config/
│   ├── dev-config.yaml                # Development environment
│   ├── staging-config.yaml            # Staging environment
│   └── prod-config.yaml               # Production environment
├── tests/
│   ├── __init__.py
│   ├── test_api_client.py             # API client tests
│   ├── test_transformations.py        # Transformation tests
│   └── test_validation.py             # Validation tests
├── .env.example                       # Environment template
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # Python dependencies
├── setup.py                           # Package setup
└── README.md                          # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Azure subscription (optional for local development)
- Databricks workspace (optional for local development)
- Git
- pip package manager

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/data-engineering-weather.git
   cd data-engineering-weather
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values (API keys, Azure credentials, etc.)
   ```

5. **Run tests**
   ```bash
   pytest tests/ -v
   ```

## 🔧 Configuration

All configuration is managed via:
- **`.env` file** - Secrets and credentials (DO NOT commit)
- **`config/` folder** - Environment-specific configs
- **Terraform variables** - Infrastructure parameters

### Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `AZURE_SUBSCRIPTION_ID` - Azure subscription
- `ADLS_ACCOUNT_NAME` - ADLS account name
- `DATABRICKS_TOKEN` - Databricks API token
- `WEATHER_API_KEY` - Weather service API key
- `ENVIRONMENT` - Current environment (development/staging/production)

## 📊 Data Pipeline

### Weekly/Monthly Processing

1. **Ingestion Phase**
   - ADF Copy Activity: Fetch API data → Staging
   - ADF Copy Activity: Read file data → Staging

2. **Bronze Layer**
   - Raw data from staging
   - Minimal transformations
   - Schema validation

3. **Silver Layer**
   - Data cleaning & deduplication
   - Null handling
   - Type conversions
   - Quality checks

4. **Gold Layer**
   - Business-ready aggregations
   - Country-level metrics
   - State-level insights
   - City-level analysis
   - Trend calculations

### Archive Process (Month-End/Weekend)

1. **Copy to Archive**
   - Original table → Archive table (APPEND)
   - Maintains full history

2. **Clear Original**
   - DELETE old data from Original table
   - INSERT new processed data
   - Fresh snapshot each period

## 🔍 Data Quality

Implemented quality checks:
- ✅ Schema validation (Avro/JSON)
- ✅ Row count monitoring
- ✅ Duplicate detection
- ✅ Null value checks
- ✅ Data freshness monitoring
- ✅ Anomaly detection
- ✅ Incremental load validation

## 📈 Monitoring & Logging

- **Structured Logging**: JSON format for easy parsing
- **Azure Application Insights**: Real-time monitoring
- **SLA Tracking**: Data freshness and latency metrics
- **Error Alerting**: Automatic notifications on failures
- **Audit Logs**: Track all data modifications

## 🔐 Security

- ✅ No credentials in code (uses `.env` & Key Vault)
- ✅ Encryption at rest (ADLS, databases)
- ✅ Encryption in transit (TLS)
- ✅ Access control (RBAC)
- ✅ Audit logging

## 💰 Cost Optimization

- Incremental loading (only process new data)
- Auto-scaling Databricks clusters
- Archive to cheaper storage tiers
- Optimized query patterns
- Partitioned data for faster access

## 🤝 Contributing

1. Create a feature branch
2. Make changes and add tests
3. Run `pytest tests/` to verify
4. Submit a pull request

## 📝 Documentation

- [Architecture Details](docs/ARCHITECTURE.md)
- [Setup Guide](docs/SETUP_GUIDE.md)
- [Operations Runbook](docs/RUNBOOK.md)
- [Data Dictionary](docs/DATA_DICTIONARY.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 🛠️ Tech Stack

- **Cloud**: Azure (ADLS, Databricks, Data Factory, Key Vault, SQL Database)
- **Processing**: Apache Spark, PySpark, Python 3.8+
- **Orchestration**: Azure Data Factory
- **IaC**: Terraform
- **Monitoring**: Application Insights
- **Testing**: pytest
- **Version Control**: Git, GitHub

## 📊 Metrics & KPIs

- Data freshness: Time from ingestion to availability
- Pipeline latency: End-to-end processing time
- Data quality score: % of records passing validation
- Archive success rate: % of archives completing successfully
- API uptime: % of successful API calls

## 📞 Support

For issues and questions:
- Check [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- Review logs in Azure Application Insights
- Submit an issue on GitHub

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

Created as a professional data engineering portfolio project.

---

**Last Updated**: 2026-05-13
