# Weather App: Chapter 5 Permissions

This snapshot is the Chapter 5 weather-app example for *Claude Code: Up and
Running*. It starts from Ken's bootcamp-style Flask weather app and preserves
the useful real-world shape:

- the home page accepts a `search` field
- successful searches redirect to `/<city>`
- weather data comes from OpenWeather geocoding, current-weather, and forecast
  endpoints
- the app reads the API key from `OWM_API_KEY`

The original training app was a doghouse: one `main.py`, direct `requests`
calls in the route handler, no tests, a real `.env`, and a notebook-heavy
requirements file. This snapshot is the Ch5 cabin state after a
permission-bounded refactor: secrets stay out of source, validation happens
before the API boundary, network calls live in a client module, and tests use
fakes instead of live OpenWeather calls.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put a real OpenWeather key in `.env` only if you plan to run the app manually.
Do not commit `.env`.

## Run

```bash
flask --app main run --debug
```

## Test

```bash
python -m pytest
```

The tests use fake keys and mocked clients. They should not make network calls.
