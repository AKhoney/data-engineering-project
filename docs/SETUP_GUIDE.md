# Setup & Deployment Guide

Complete guide for setting up the Weather Data Engineering project locally and in Azure.

## Prerequisites

### Local Development
- Python 3.8 or higher
- Git
- pip package manager
- VS Code or preferred IDE

### Azure Deployment
- Active Azure subscription
- Azure CLI installed
- Terraform 1.0+
- Databricks workspace
- Storage account with ADLS Gen2 enabled

## Step 1: Local Setup

### 1.1 Clone Repository

```bash
git clone https://github.com/yourusername/data-engineering-weather.git
cd data-engineering-weather
```

### 1.2 Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 1.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 1.4 Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your actual values
# Required values:
# - WEATHER_API_KEY: Your weather service API key
# - AZURE_SUBSCRIPTION_ID: Your Azure subscription ID
# - ADLS_ACCOUNT_NAME: Your ADLS storage account name
```

### 1.5 Verify Installation

```bash
python -c "import pyspark; print(f'PySpark version: {pyspark.__version__}')"
python -c "from src.config.config import Config; print('Configuration loaded successfully')"
```

## Step 2: Local Development Testing

### 2.1 Run Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_api_client.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### 2.2 Test API Client

```bash
# Create test script
python -c "
from src.api.weather_client import WeatherAPIClient
client = WeatherAPIClient()
print('API Client initialized successfully')
"
```

### 2.3 Test Configuration

```bash
python -c "
from src.config.config import Config
Config.validate()
print(f'Environment: {Config.ENVIRONMENT}')
print(f'ADLS Account: {Config.ADLS_ACCOUNT_NAME}')
"
```

## Step 3: Azure Infrastructure Setup

### 3.1 Prepare Terraform Variables

```bash
cd terraform

# Copy example variables file
cp terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars with your values
nano terraform.tfvars

# Required variables:
# - subscription_id
# - resource_group_name
# - location (e.g., "East US")
# - storage_account_name
# - databricks_workspace_name
```

### 3.2 Initialize Terraform

```bash
# Initialize Terraform
terraform init

# Verify configuration
terraform fmt -recursive
terraform validate
```

### 3.3 Plan Infrastructure

```bash
# See what resources will be created
terraform plan -out=tfplan

# Review the plan output carefully
# Resources to be created:
# - Azure Resource Group
# - Storage Account (ADLS Gen2)
# - Databricks Workspace
# - SQL Database
# - Key Vault
# - Data Factory
```

### 3.4 Deploy Infrastructure (Do NOT run in production yet)

```bash
# Apply the plan (creates actual resources)
terraform apply tfplan

# Wait for completion (10-15 minutes typical)
```

### 3.5 Verify Deployment

```bash
# Get outputs
terraform output

# Check created resources in Azure Portal
# Verify:
# - Resource group exists
# - Storage account created with ADLS container
# - Databricks workspace running
# - SQL database accessible
```

## Step 4: Configure Azure Services

### 4.1 Configure ADLS Paths

```bash
# Create folder structure in ADLS
az storage fs directory create \
  --name staging \
  --file-system <container-name> \
  --account-name <storage-account-name>

az storage fs directory create \
  --name bronze \
  --file-system <container-name> \
  --account-name <storage-account-name>

az storage fs directory create \
  --name silver \
  --file-system <container-name> \
  --account-name <storage-account-name>

az storage fs directory create \
  --name gold \
  --file-system <container-name> \
  --account-name <storage-account-name>

az storage fs directory create \
  --name archive \
  --file-system <container-name> \
  --account-name <storage-account-name>
```

### 4.2 Create Azure Key Vault Secrets

```bash
# Store API key in Key Vault
az keyvault secret set \
  --vault-name <keyvault-name> \
  --name "weather-api-key" \
  --value "<your-api-key>"

# Store database password
az keyvault secret set \
  --vault-name <keyvault-name> \
  --name "db-password" \
  --value "<your-db-password>"
```

### 4.3 Configure Databricks

1. Open Databricks workspace
2. Create cluster with:
   - Spark version: 13.0+
   - Python version: 3.10+
   - Node type: Standard (4-8GB RAM)
   - Auto-termination: 30 minutes
3. Install libraries:
   - pandas
   - pyspark
   - python-dotenv
   - pyyaml

### 4.4 Create SQL Database

```bash
# Create database and tables
# (Use Azure Portal or Azure Data Studio)
# Tables needed:
# - bronze_weather_original
# - bronze_weather_archive
# - silver_weather_original
# - silver_weather_archive
# - gold_weather_original
# - gold_weather_archive
```

## Step 5: Deploy Data Pipelines

### 5.1 Upload Python Modules to Databricks

```bash
# Package Python modules
python setup.py sdist

# Upload to Databricks (or use git integration)
databricks workspace import_dir . /Workspace/weather-project
```

### 5.2 Create ADF Pipelines

1. Open Azure Data Factory
2. Create linked services for:
   - ADLS storage
   - Databricks cluster
   - SQL database
3. Create pipelines from templates:
   - `adf-pipelines/pipeline-ingest-api.json`
   - `adf-pipelines/pipeline-ingest-files.json`
   - `adf-pipelines/pipeline-archive.json`
   - `adf-pipelines/pipeline-master.json`

### 5.3 Configure Triggers

1. **Weekly Ingestion** (Monday 00:00 UTC)
   - Triggers: pipeline-master
   - Frequency: Weekly
   - Day: Monday

2. **Archive** (Month-end)
   - Triggers: pipeline-archive
   - Frequency: Monthly
   - Day: Last day of month

## Step 6: Monitoring & Verification

### 6.1 Check Pipeline Runs

```bash
# Monitor ADF pipeline runs
az datafactory pipeline-run query-by-factory \
  --resource-group <resource-group> \
  --factory-name <adf-name>
```

### 6.2 Verify Data in ADLS

```bash
# List files in staging
az storage fs file list \
  --file-system <container> \
  --path "staging" \
  --account-name <storage-account>
```

### 6.3 Check Application Insights

1. Open Application Insights
2. View logs and metrics
3. Set up alerts for failures

## Step 7: Production Deployment Checklist

Before deploying to production:

- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Infrastructure tested in staging
- [ ] Backup strategy defined
- [ ] Disaster recovery plan documented
- [ ] Monitoring alerts configured
- [ ] Team trained on operations
- [ ] Runbooks created
- [ ] Cost estimates reviewed
- [ ] Security review completed

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pyspark'"

```bash
# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: "Failed to authenticate with Azure"

```bash
# Solution: Re-authenticate with Azure CLI
az login
az account set --subscription <subscription-id>
```

### Issue: "ADLS connection failed"

1. Check storage account name in .env
2. Verify account key is correct
3. Check network connectivity
4. Verify RBAC permissions

### Issue: "Databricks cluster not responding"

1. Check cluster status in Databricks workspace
2. Verify cluster is running
3. Check cluster logs for errors
4. Restart cluster if needed

## Performance Tuning

### Optimize Spark Jobs

```python
# In your Spark code:
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.shuffle.partitions", "200")
```

### Optimize Storage Queries

```sql
-- Use partition pruning
SELECT * FROM silver_weather 
WHERE date >= '2026-01-01' AND date <= '2026-05-13'

-- Use statistics
ANALYZE TABLE silver_weather COMPUTE STATISTICS
```

---

**Last Updated**: 2026-05-13
