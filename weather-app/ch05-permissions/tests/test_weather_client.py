import datetime as dt

import pytest
import requests

from weather_client import (
    GEOCODING_API_ENDPOINT,
    ONE_CALL_API_ENDPOINT,
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


def one_call_payload():
    return {
        "current": {
            "temp": 21.2,
            "weather": [{"main": "Clouds"}],
            "wind_speed": 4.2,
        },
        "daily": [
            {"dt": 1779451200, "temp": {"day": 21.2, "min": 18.3, "max": 24.1}, "weather": [{"main": "Clouds"}]},
            {"dt": 1779537600, "temp": {"day": 19.4, "min": 16.0, "max": 21.0}, "weather": [{"main": "Rain"}]},
            {"dt": 1779624000, "temp": {"day": 22.0, "min": 18.0, "max": 25.0}, "weather": [{"main": "Clear"}]},
            {"dt": 1779710400, "temp": {"day": 24.1, "min": 20.0, "max": 26.0}, "weather": [{"main": "Clear"}]},
            {"dt": 1779796800, "temp": {"day": 20.8, "min": 17.0, "max": 23.0}, "weather": [{"main": "Mist"}]},
        ],
    }


def test_get_weather_uses_geocoding_then_one_call_endpoint():
    session = FakeSession(
        [
            FakeResponse([{"lat": 40.7, "lon": -74.0}]),
            FakeResponse(one_call_payload()),
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
        ONE_CALL_API_ENDPOINT,
    ]
    assert session.calls[0]["params"]["q"] == "New York"
    assert all(call["params"]["appid"] == "fake-key" for call in session.calls)
    assert session.calls[1]["params"]["exclude"] == "minutely,hourly,alerts"


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
