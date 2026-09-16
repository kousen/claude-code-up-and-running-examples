import pytest

from main import create_app, normalize_city
from weather_client import ForecastDay, WeatherLookupError, WeatherReport


class FakeWeatherClient:
    def __init__(self, report=None, error=None):
        self.report = report
        self.error = error
        self.requested_cities = []

    def get_weather(self, city_name):
        self.requested_cities.append(city_name)
        if self.error:
            raise self.error
        return self.report


@pytest.fixture
def sample_report():
    return WeatherReport(
        city_name="New York",
        current_date="Friday, May 22",
        current_temp_c=21,
        current_weather="Clouds",
        min_temp_c=18,
        max_temp_c=24,
        wind_speed=4.2,
        forecast=[
            ForecastDay("Fri", "Clouds", 21),
            ForecastDay("Sat", "Rain", 19),
        ],
    )


def test_normalize_city_trims_and_formats_city_names():
    assert normalize_city("  new york  ") == "New York"


def test_home_rejects_blank_city_without_calling_weather_client(sample_report):
    fake_client = FakeWeatherClient(sample_report)
    app = create_app(fake_client)

    response = app.test_client().post("/", data={"search": "   "})

    assert response.status_code == 400
    assert b"Please enter a city name" in response.data
    assert fake_client.requested_cities == []


def test_home_redirects_to_normalized_city_path(sample_report):
    app = create_app(FakeWeatherClient(sample_report))

    response = app.test_client().post("/", data={"search": "  new york  "})

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/New%20York")


def test_weather_route_renders_report(sample_report):
    fake_client = FakeWeatherClient(sample_report)
    app = create_app(fake_client)

    response = app.test_client().get("/new%20york")

    assert response.status_code == 200
    assert b"New York" in response.data
    assert b"21 deg C" in response.data
    assert fake_client.requested_cities == ["New York"]


def test_weather_route_redirects_when_city_lookup_fails():
    app = create_app(FakeWeatherClient(error=WeatherLookupError("not found")))

    response = app.test_client().get("/Atlantis")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/error")
