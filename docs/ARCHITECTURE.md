# Architecture Documentation

## System Architecture Overview

This document provides a detailed overview of the weather data engineering system architecture.

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      DATA SOURCES                             │
├─────────────────────────┬────────────────────────────────────┤
│   Weather APIs          │  CSV/JSON Files                    │
│   - Real-time data      │  - Historical data                 │
│   - 7 API calls/week    │  - Weekly/Monthly batch            │
└─────────────────────────┴────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  INGESTION LAYER (Python Scripts)     │
        │  - API fetching with retry logic      │
        │  - File reading (CSV/JSON/Parquet)    │
        │  - Error handling & logging           │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  ORCHESTRATION (Azure Data Factory)   │
        │  - Schedule weekly/monthly jobs       │
        │  - Copy activities (API → Staging)    │
        │  - Lookup activities (aggregations)   │
        │  - Error handling & retry policies    │
        │  - Archive triggers (month-end)       │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │   STORAGE LAYER (Azure ADLS Gen2)     │
        │  - Staging area (raw data)            │
        │  - Bronze layer (raw)                 │
        │  - Silver layer (cleaned)             │
        │  - Gold layer (insights)              │
        │  - Archive storage (historical)       │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  PROCESSING LAYER (Databricks)        │
        │  - Apache Spark/PySpark               │
        │  - Data transformations               │
        │  - Quality checks                     │
        │  - Aggregations                       │
        │  - SQL for analytics                  │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  ANALYTICS LAYER (SQL Database)       │
        │  - Country-level metrics              │
        │  - State-level insights               │
        │  - City-level analysis                │
        │  - Trends & patterns                  │
        └───────────────────────────────────────┘
```

## Medallion Architecture Details

### Bronze Layer (Raw Data)

**Purpose**: Store raw ingested data with minimal transformations

**Characteristics**:
- Preserves all source data
- Minimal transformations (format conversions only)
- Source-aligned schema
- Comprehensive metadata

**Tables**:
- `bronze_weather_api_<timestamp>` - Raw API data
- `bronze_weather_files_<timestamp>` - Raw file data
- `bronze_weather_api_archive` - Historical raw API data
- `bronze_weather_files_archive` - Historical raw file data

**Data Retention**: 90 days (original), unlimited (archive)

### Silver Layer (Cleaned & Validated)

**Purpose**: Provide conformed, high-quality data

**Characteristics**:
- Data quality checks passed
- Deduplication applied
- Null handling and type conversions
- Business logic applied
- Consistent naming conventions

**Transformations**:
- Standardize metric names (temperature → temperature_celsius)
- Handle missing values
- Convert units consistently
- Remove duplicates
- Add derived columns

**Tables**:
- `silver_weather_country_<timestamp>` - Country-level data
- `silver_weather_state_<timestamp>` - State-level data
- `silver_weather_city_<timestamp>` - City-level data
- Archive variants for each

### Gold Layer (Business Ready)

**Purpose**: Provide business-ready aggregations and insights

**Characteristics**:
- Aggregated metrics
- Trend calculations
- Business-aligned naming
- Optimized for analytics
- Ready for dashboarding

**Tables**:
- `gold_weather_country_aggregations` - Country metrics
- `gold_weather_state_aggregations` - State metrics
- `gold_weather_city_aggregations` - City metrics
- `gold_weather_trends_analysis` - Trend analysis
- `gold_weather_state_rankings` - State comparisons

**Aggregations**:
- Hourly, daily, weekly, monthly averages
- Min/max values per period
- Humidity and wind analysis
- Air quality indexes
- Trend direction (improving/declining)

## Data Flow - Weekly Processing

```
Monday 00:00 (Scheduled Trigger)
    │
    ├─→ Step 1: Ingest API Data
    │   └─→ Fetch weather for 50+ cities (USA & India)
    │   └─→ Error handling & retry on failure
    │   └─→ Save to ADLS staging
    │
    ├─→ Step 2: Ingest File Data
    │   └─→ Read historical CSV files
    │   └─→ Validate file format
    │   └─→ Save to ADLS staging
    │
    ├─→ Step 3: Bronze Transformations
    │   └─→ Apply minimal transformations
    │   └─→ Schema validation
    │   └─→ Load to Bronze layer
    │
    ├─→ Step 4: Silver Transformations
    │   └─→ Data cleaning & deduplication
    │   └─→ Quality checks
    │   └─→ Load to Silver layer
    │
    └─→ Step 5: Gold Aggregations
        └─→ Calculate country/state/city metrics
        └─→ Compute trends
        └─→ Load to Gold layer
```

## Data Flow - Month-End Archive Process

```
End of Month (e.g., Jan 31, 23:00)
    │
    ├─→ Step 1: Archive Bronze Data
    │   └─→ INSERT bronze_original → bronze_archive (APPEND)
    │   └─→ DELETE FROM bronze_original
    │   └─→ Verify counts
    │
    ├─→ Step 2: Archive Silver Data
    │   └─→ INSERT silver_original → silver_archive (APPEND)
    │   └─→ DELETE FROM silver_original
    │   └─→ Verify counts
    │
    ├─→ Step 3: Archive Gold Data
    │   └─→ INSERT gold_original → gold_archive (APPEND)
    │   └─→ DELETE FROM gold_original
    │   └─→ Verify counts
    │
    ├─→ Step 4: Validate Archive
    │   └─→ Check archive counts
    │   └─→ Verify metadata
    │   └─→ Generate report
    │
    └─→ Step 5: Cleanup Old Data
        └─→ Delete archives older than 2 years
        └─→ Optimize storage
```

## Data Quality Framework

### Quality Checks (Bronze → Silver)

1. **Schema Validation**
   - Required fields present
   - Data types correct
   - No unexpected columns

2. **Row Count Validation**
   - Minimum 100 records per batch
   - No zero-row batches

3. **Null Handling**
   - Max 5% null values per column
   - Critical columns (location, temp) must be non-null

4. **Duplicate Detection**
   - Remove exact duplicates
   - Flag near-duplicates
   - 0% duplicate tolerance

5. **Range Validation**
   - Temperature: -50 to 60°C
   - Humidity: 0 to 100%
   - Wind speed: 0 to 200 km/h

6. **Freshness Check**
   - Data should not be older than 24 hours
   - Alert if staleness detected

### Data Quality Report

Generated after each transformation:
```json
{
  "timestamp": "2026-05-13T10:30:00Z",
  "layer": "silver",
  "total_records": 5000,
  "records_passed": 4950,
  "records_failed": 50,
  "pass_rate": 99.0,
  "checks": {
    "schema": "PASSED",
    "row_count": "PASSED",
    "nulls": "PASSED",
    "duplicates": "PASSED",
    "ranges": "PASSED"
  }
}
```

## Technology Stack

### Cloud Platform
- **Azure ADLS Gen2**: Data lake storage
- **Azure Databricks**: Managed Spark clusters
- **Azure Data Factory**: Orchestration
- **Azure Key Vault**: Secrets management
- **Azure SQL Database**: Metadata & analytics

### Processing
- **Apache Spark 3.5.0**: Distributed processing
- **PySpark**: Python API for Spark
- **Python 3.8+**: Data engineering scripts

### Monitoring
- **Azure Application Insights**: Real-time monitoring
- **Structured Logging (JSON)**: Centralized logs

### Infrastructure
- **Terraform**: Infrastructure as Code
- **GitHub**: Version control

## Error Handling & Recovery

### API Error Handling

```python
# Exponential backoff strategy
Max Retries: 3
Initial Backoff: 1 second
Max Backoff: 60 seconds
Backoff Multiplier: 2x

Retry Schedule:
- Attempt 1 fails → wait 1s
- Attempt 2 fails → wait 2s
- Attempt 3 fails → wait 4s
- Final failure → alert & log
```

### Pipeline Error Handling

- **Data Ingestion Failure**: Retry with backoff, alert on failure
- **Quality Check Failure**: Log issue, hold data, notify
- **Processing Failure**: Partial rollback, capture state, retry
- **Archive Failure**: Alert operations team, pause new loads

### Monitoring & Alerting

- Email alerts on pipeline failures
- Dashboard for real-time monitoring
- Log aggregation in Application Insights
- Daily health check reports

## Scalability Considerations

### Horizontal Scaling
- Auto-scaling Databricks clusters (based on workload)
- Partitioned data for parallel processing
- Incremental loading (only new data)

### Vertical Scaling
- Increase cluster node size
- Allocate more memory/cores

### Optimization
- Parquet format for efficient storage
- Partition pruning (by date, location)
- Statistics collection for query optimization
- Caching frequently accessed data

## Security & Compliance

### Authentication & Authorization
- Azure AD integration
- Role-based access control (RBAC)
- Service principal for automation

### Data Protection
- Encryption at rest (ADLS, SQL)
- Encryption in transit (TLS 1.2+)
- Network isolation (VNet)

### Audit & Compliance
- Audit logging for all operations
- Data access tracking
- Retention policies enforced
- GDPR-compliant data handling

## Cost Optimization

### Storage
- Archive to cheaper tier after 90 days
- Compress parquet files
- Remove duplicates

### Compute
- Auto-scaling clusters
- Scheduled cluster shutdown
- Spot instances for non-critical jobs

### Network
- Minimize data transfer
- Use private endpoints
- Cache results

---

Last Updated: 2026-05-13
