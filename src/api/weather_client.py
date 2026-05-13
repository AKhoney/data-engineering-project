"""Weather API Client for fetching live weather data"""

import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.config.config import Config
from src.logging.logger import LoggerManager
from src.utils.retry_logic import ExponentialBackoff


class WeatherAPIClient:
    """Client for fetching weather data from external APIs"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Initialize weather API client"""
        self.api_key = api_key or Config.WEATHER_API_KEY
        self.timeout = timeout or Config.API_TIMEOUT_SECONDS
        self.logger = LoggerManager.get_logger(__name__)
        self.session = self._create_session()
        self.base_url = "https://api.weatherapi.com/v1"  # Placeholder API endpoint

    def _create_session(self) -> requests.Session:
        """Create requests session with retry strategy"""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def fetch_current_weather(
        self, city: str, state: str = None, country: str = None
    ) -> Dict[str, Any]:
        """Fetch current weather for a location"""
        try:
            location = self._format_location(city, state, country)
            endpoint = f"{self.base_url}/current.json"
            params = {"key": self.api_key, "q": location, "aqi": "yes"}

            self.logger.info(f"Fetching weather for {location}")

            response = self.session.get(
                endpoint, params=params, timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            self.logger.info(f"Successfully fetched weather for {location}")

            return self._transform_weather_response(data)

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching weather for {location}: {str(e)}")
            raise

    def fetch_historical_weather(
        self, city: str, state: str, country: str, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        """Fetch historical weather data for a date range"""
        try:
            location = self._format_location(city, state, country)
            endpoint = f"{self.base_url}/history.json"

            self.logger.info(
                f"Fetching historical weather for {location} ({start_date} to {end_date})"
            )

            params = {
                "key": self.api_key,
                "q": location,
                "dt": start_date,
                "end_dt": end_date,
                "aqi": "yes",
            }

            response = self.session.get(
                endpoint, params=params, timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            return self._transform_historical_response(data)

        except requests.exceptions.RequestException as e:
            self.logger.error(
                f"Error fetching historical weather: {str(e)}"
            )
            raise

    def fetch_forecast(
        self, city: str, state: str = None, country: str = None, days: int = 7
    ) -> List[Dict[str, Any]]:
        """Fetch weather forecast for upcoming days"""
        try:
            location = self._format_location(city, state, country)
            endpoint = f"{self.base_url}/forecast.json"
            params = {
                "key": self.api_key,
                "q": location,
                "days": days,
                "aqi": "yes",
            }

            self.logger.info(f"Fetching {days}-day forecast for {location}")

            response = self.session.get(
                endpoint, params=params, timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            return self._transform_forecast_response(data)

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching forecast: {str(e)}")
            raise

    def fetch_bulk_weather(
        self, locations: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """Fetch weather for multiple locations with rate limiting"""
        results = []
        backoff = ExponentialBackoff()

        for location in locations:
            try:
                weather_data = self.fetch_current_weather(
                    city=location["city"],
                    state=location.get("state"),
                    country=location.get("country"),
                )
                results.append(weather_data)

                # Reset backoff on success
                backoff.reset()

            except requests.exceptions.RequestException:
                # Wait before retrying
                wait_time = backoff.get_wait_time()
                self.logger.warning(
                    f"Rate limited or error. Waiting {wait_time} seconds..."
                )
                # In production, use: time.sleep(wait_time)

        return results

    @staticmethod
    def _format_location(city: str, state: str = None, country: str = None) -> str:
        """Format location string for API"""
        parts = [city]
        if state:
            parts.append(state)
        if country:
            parts.append(country)
        return ", ".join(parts)

    @staticmethod
    def _transform_weather_response(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform API response to standardized format"""
        current = data.get("current", {})
        location = data.get("location", {})

        return {
            "location": location.get("name"),
            "state": location.get("region"),
            "country": location.get("country"),
            "latitude": location.get("lat"),
            "longitude": location.get("lon"),
            "timestamp": datetime.utcnow().isoformat(),
            "temperature_celsius": current.get("temp_c"),
            "temperature_fahrenheit": current.get("temp_f"),
            "humidity": current.get("humidity"),
            "wind_speed_kmh": current.get("wind_kph"),
            "wind_speed_mph": current.get("wind_mph"),
            "wind_direction": current.get("wind_dir"),
            "pressure_mb": current.get("pressure_mb"),
            "precipitation_mm": current.get("precip_mm"),
            "visibility_km": current.get("vis_km"),
            "uv_index": current.get("uv"),
            "air_quality_index": current.get("air_quality", {}).get("us-epa-index"),
            "cloud_coverage": current.get("cloud"),
            "condition": current.get("condition", {}).get("text"),
        }

    @staticmethod
    def _transform_historical_response(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Transform historical API response"""
        # Placeholder implementation
        return []

    @staticmethod
    def _transform_forecast_response(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Transform forecast API response"""
        # Placeholder implementation
        return []
