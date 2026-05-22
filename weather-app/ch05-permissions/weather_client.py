import datetime as dt
import os
from dataclasses import dataclass

import requests


GEOCODING_API_ENDPOINT = "https://api.openweathermap.org/geo/1.0/direct"
ONE_CALL_API_ENDPOINT = "https://api.openweathermap.org/data/3.0/onecall"


class WeatherLookupError(Exception):
    """Raised when a city cannot be resolved or weather data cannot be parsed."""


class WeatherConfigError(Exception):
    """Raised when required weather-service configuration is missing."""


@dataclass(frozen=True)
class ForecastDay:
    day: str
    weather: str
    temp_c: int


@dataclass(frozen=True)
class WeatherReport:
    city_name: str
    current_date: str
    current_temp_c: int
    current_weather: str
    min_temp_c: int
    max_temp_c: int
    wind_speed: float
    forecast: list[ForecastDay]

    def to_template_context(self):
        return {
            "city_name": self.city_name,
            "current_date": self.current_date,
            "current_temp": self.current_temp_c,
            "current_weather": self.current_weather,
            "min_temp": self.min_temp_c,
            "max_temp": self.max_temp_c,
            "wind_speed": self.wind_speed,
            "forecast": self.forecast,
        }


class OpenWeatherClient:
    def __init__(self, api_key, session=None, clock=None):
        self.api_key = api_key
        self.session = session or requests.Session()
        self.clock = clock or dt.datetime.now

    @classmethod
    def from_env(cls, env_var="OWM_API_KEY"):
        return cls(os.getenv(env_var))

    def get_weather(self, city_name):
        if not self.api_key:
            raise WeatherConfigError("OWM_API_KEY is not configured")

        lat, lon = self._lookup_coordinates(city_name)
        weather_data = self._get_json(
            ONE_CALL_API_ENDPOINT,
            {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",
                "exclude": "minutely,hourly,alerts",
            },
        )
        return self._build_report(city_name, weather_data)

    def _lookup_coordinates(self, city_name):
        location_data = self._get_json(
            GEOCODING_API_ENDPOINT,
            {"q": city_name, "appid": self.api_key, "limit": 3},
        )
        if not location_data:
            raise WeatherLookupError(f"No OpenWeather location for {city_name}")

        first_match = location_data[0]
        try:
            return first_match["lat"], first_match["lon"]
        except KeyError as exc:
            raise WeatherLookupError("OpenWeather location response missing lat/lon") from exc

    def _get_json(self, url, params):
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise WeatherLookupError(f"OpenWeather request failed: {url}") from exc

    def _build_report(self, city_name, weather_data):
        try:
            today = self.clock()
            current = weather_data["current"]
            daily = weather_data["daily"]
            current_weather = current["weather"][0]["main"]
            forecast = [
                ForecastDay(
                    day=dt.datetime.fromtimestamp(item["dt"]).strftime("%a"),
                    weather=item["weather"][0]["main"],
                    temp_c=round(item["temp"]["day"]),
                )
                for item in daily[:5]
            ]

            return WeatherReport(
                city_name=city_name,
                current_date=today.strftime("%A, %B %d"),
                current_temp_c=round(current["temp"]),
                current_weather=current_weather,
                min_temp_c=round(daily[0]["temp"]["min"]),
                max_temp_c=round(daily[0]["temp"]["max"]),
                wind_speed=current["wind_speed"],
                forecast=forecast,
            )
        except (KeyError, IndexError, TypeError) as exc:
            raise WeatherLookupError("OpenWeather response shape was unexpected") from exc
