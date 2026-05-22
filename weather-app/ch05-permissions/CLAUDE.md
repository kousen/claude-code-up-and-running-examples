# Weather App Ch05 Permissions

Small Flask weather app for Chapter 5 of *Claude Code: Up and Running*.

## Project Boundaries

- Do not read `.env` or print environment variables.
- Use `OWM_API_KEY` for the real OpenWeather key.
- Tests must use fake keys and mocked clients; ordinary test runs must not call
  OpenWeather.
- Keep user input validation in the Flask layer and weather API details in
  `weather_client.py`.
- Do not add dependencies without explaining why.
- Do not push branches from this example.

## Useful Commands

```bash
python -m pytest
flask --app main run --debug
```
