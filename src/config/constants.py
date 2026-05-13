"""Constants used across the project"""

# Geographic Configuration
COUNTRIES = {
    "USA": {
        "name": "United States of America",
        "code": "US",
        "states": ["California", "Texas", "Florida", "New York", "Pennsylvania"],
    },
    "India": {
        "name": "India",
        "code": "IN",
        "states": ["Maharashtra", "Karnataka", "Tamil Nadu", "Delhi", "Gujarat"],
    },
}

# Major Cities by State (Sample)
MAJOR_CITIES = {
    "USA": {
        "California": ["Los Angeles", "San Francisco", "San Diego", "San Jose"],
        "Texas": ["Houston", "Dallas", "Austin", "San Antonio"],
        "Florida": ["Miami", "Tampa", "Jacksonville", "Orlando"],
        "New York": ["New York City", "Buffalo", "Rochester", "Syracuse"],
        "Pennsylvania": ["Philadelphia", "Pittsburgh", "Allentown", "Erie"],
    },
    "India": {
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
        "Karnataka": ["Bangalore", "Mysore", "Mangalore", "Hubli"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem"],
        "Delhi": ["Delhi", "New Delhi"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    },
}

# Weather Metrics
WEATHER_METRICS = [
    "temperature",
    "humidity",
    "wind_speed",
    "wind_direction",
    "pressure",
    "precipitation",
    "visibility",
    "air_quality_index",
    "uv_index",
    "cloud_coverage",
]

# Data Quality Thresholds
DATA_QUALITY_THRESHOLDS = {
    "min_row_count": 100,
    "max_null_percentage": 5.0,
    "duplicate_threshold": 0.0,
    "temperature_range": (-50, 60),  # Celsius
    "humidity_range": (0, 100),
    "wind_speed_max": 200,  # km/h
}

# Archive Configuration
ARCHIVE_SCHEDULE = {
    "frequency": "month-end",
    "retention_period_days": 730,  # 2 years
    "schedule_day": 28,  # Month-end check
}

# Retry Configuration
RETRY_CONFIG = {
    "max_retries": 3,
    "initial_backoff_seconds": 1,
    "max_backoff_seconds": 60,
    "backoff_multiplier": 2,
}

# Logging Configuration
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# Table Names (Templates)
TABLE_NAMING = {
    "bronze": "{layer}_weather_{location_type}_{timestamp}",
    "silver": "{layer}_weather_{location_type}_{timestamp}",
    "gold": "{layer}_weather_{location_type}_{metric}_{timestamp}",
}

# Location Types
LOCATION_TYPES = ["country", "state", "city"]

# Data Processing Windows
PROCESSING_WINDOWS = {
    "weekly": 7,
    "monthly": 30,
}

# API Rate Limiting
API_RATE_LIMIT_CONFIG = {
    "requests_per_minute": 100,
    "timeout_seconds": 30,
}

# File Formats
SUPPORTED_FORMATS = ["csv", "json", "parquet"]

# Date Formats
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
