# Weather App: Chapter 5 Permissions

This snapshot is the Chapter 5 weather-app example for *Claude Code: Up and
Running*. It is based on the Python exercises from Ken's `claude-code-training`
materials -- especially the Flask API and weather-app exercises -- plus his
updated `python-weather-app` fork, preserving the useful real-world shape:

- the home page accepts a `search` field
- successful searches redirect to `/<city>`
- weather data comes from OpenWeather geocoding plus the One Call 3.0 current
  and daily forecast endpoint
- the app reads the API key from `OWM_API_KEY`

The original training version was a doghouse: one `main.py`, direct `requests`
calls in the route handler, old OpenWeather 2.5 current/forecast calls, no
tests, a real `.env`, and a notebook-heavy requirements file. This snapshot is
the Ch5 cabin state after a permission-bounded modernization: secrets stay out
of source, validation happens before the API boundary, OpenWeather integration
lives in a client module, One Call 3.0 replaces the older weather/forecast pair,
and tests use fakes instead of live OpenWeather calls.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put a real OpenWeather key in `.env` only if you plan to run the app manually.
Do not commit `.env`.

If you already have a key stored under another local variable, export it as
`OWM_API_KEY` for this app before running Flask.

## Run

```bash
flask --app main run --debug
```

## Test

```bash
python -m pytest
```

The tests use fake keys and mocked clients. They should not make network calls.
