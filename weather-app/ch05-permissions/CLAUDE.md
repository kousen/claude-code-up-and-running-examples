# Weather App Ch05 Permissions

Small Flask weather app for Chapter 5 of *Claude Code: Up and Running*.

This snapshot is distilled from Ken's `claude-code-training` Python exercises
-- especially the Flask API and weather-app exercises -- plus his
`python-weather-app` fork. The Chapter 5 version modernizes the API boundary to
OpenWeather One Call 3.0 and keeps the app small enough to show the
doghouse-to-cabin transition.

## Project Boundaries

- Do not read `.env` or print environment variables.
- Use `OWM_API_KEY` for the real OpenWeather key.
- Tests must use fake keys and mocked clients; ordinary test runs must not call
  OpenWeather.
- Keep user input validation in the Flask layer and weather API details in
  `weather_client.py`.
- Use OpenWeather geocoding plus One Call 3.0 from the client module; do not put
  API calls directly in route handlers.
- Do not add dependencies without explaining why.
- Do not push branches from this example.

## Useful Commands

```bash
python -m pytest
flask --app main run --debug
```
