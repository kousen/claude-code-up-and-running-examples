import datetime as dt

import pytest
import requests

from weather_client import (
    GEOCODING_API_ENDPOINT,
    OWM_ENDPOINT,
    OWM_FORECAST_ENDPOINT,
    OpenWeatherClient,
    WeatherConfigError,
    WeatherLookupError,
)


class FakeResponse:
    def __init__(self, payload, error=None):
        self.payload = payload
        self.error = error

    def raise_for_status(self):
        if self.error:
            raise self.error

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, url, params, timeout):
        self.calls.append({"url": url, "params": params, "timeout": timeout})
        return self.responses.pop(0)


def forecast_payload():
    return {
        "list": [
            {"dt_txt": "2026-05-22 12:00:00", "main": {"temp": 21.2}, "weather": [{"main": "Clouds"}]},
            {"dt_txt": "2026-05-23 12:00:00", "main": {"temp": 19.4}, "weather": [{"main": "Rain"}]},
            {"dt_txt": "2026-05-24 12:00:00", "main": {"temp": 22.0}, "weather": [{"main": "Clear"}]},
            {"dt_txt": "2026-05-25 12:00:00", "main": {"temp": 24.1}, "weather": [{"main": "Clear"}]},
            {"dt_txt": "2026-05-26 12:00:00", "main": {"temp": 20.8}, "weather": [{"main": "Mist"}]},
        ]
    }


def weather_payload():
    return {
        "main": {"temp": 21.2, "temp_min": 18.3, "temp_max": 24.1},
        "weather": [{"main": "Clouds"}],
        "wind": {"speed": 4.2},
    }


def test_get_weather_uses_geocoding_then_weather_and_forecast_endpoints():
    session = FakeSession(
        [
            FakeResponse([{"lat": 40.7, "lon": -74.0}]),
            FakeResponse(weather_payload()),
            FakeResponse(forecast_payload()),
        ]
    )
    client = OpenWeatherClient(
        "fake-key",
        session=session,
        clock=lambda: dt.datetime(2026, 5, 22, 9, 0),
    )

    report = client.get_weather("New York")

    assert report.city_name == "New York"
    assert report.current_temp_c == 21
    assert report.forecast[1].day == "Sat"
    assert [call["url"] for call in session.calls] == [
        GEOCODING_API_ENDPOINT,
        OWM_ENDPOINT,
        OWM_FORECAST_ENDPOINT,
    ]
    assert session.calls[0]["params"]["q"] == "New York"
    assert all(call["params"]["appid"] == "fake-key" for call in session.calls)


def test_missing_api_key_fails_before_network_call():
    session = FakeSession([])
    client = OpenWeatherClient(None, session=session)

    with pytest.raises(WeatherConfigError):
        client.get_weather("New York")

    assert session.calls == []


def test_missing_geocoding_match_is_lookup_error():
    session = FakeSession([FakeResponse([])])
    client = OpenWeatherClient("fake-key", session=session)

    with pytest.raises(WeatherLookupError):
        client.get_weather("Atlantis")


def test_http_failure_is_lookup_error():
    session = FakeSession(
        [
            FakeResponse(
                [],
                error=requests.HTTPError("service unavailable"),
            )
        ]
    )
    client = OpenWeatherClient("fake-key", session=session)

    with pytest.raises(WeatherLookupError):
        client.get_weather("New York")
