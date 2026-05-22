# Chapter 5 weather-app reconciliation prompt

Foundation prompt. The Chapter 5 weather app is based on Ken's existing
bootcamp-style Flask exercise at
`~/Documents/OReilly/claude-code-training/exercises/python/weather-app`, then
trimmed into `weather-app/ch05-permissions/`.

The source app is intentionally doghouse-shaped: one `main.py`, form field
`search`, redirect to `/<city>`, direct OpenWeather calls, `OWM_API_KEY`, no
tests, and a requirements file with unrelated notebook dependencies. The Ch5
snapshot should preserve those real identifiers where they teach something, then
let the permission-bounded refactor create the cabin boundary: validation before
the API call, a mockable weather client, fake-key tests, and no committed real
`.env`.

```text
Create the Chapter 5 weather-app snapshot from the existing training exercise. Keep it modest and framework-light beyond Flask itself.

Requirements:
- A home page at GET / with a form field named search.
- A successful search redirects to /<city>, matching the source app.
- A small service module (a weather client) that uses OpenWeather geocoding, current-weather, and forecast endpoints.
- Templates that render either the forecast or an error.
- Tests for the service and the routes, using pytest.

Constraints:
- Read the API key from the environment as OWM_API_KEY. Never hard-code it or commit it. Pass it to OpenWeather as the appid query parameter at the last responsible moment.
- Make the weather client injectable so tests can pass a fake client. Do not make live network calls in tests; use a fake key and a mocked client or fixtures.
- Replace any real .env with .env.example.
- Trim requirements.txt to runtime/test dependencies only.
- Keep the structure small and readable.

Before writing code, show me the file layout and call out which boundaries changed: input validation, secrets, network access, dependencies, tests, and git publication.
```
