# ch05 weather app trust map

Date captured: 2026-05-22

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples/weather-app/ch05-permissions
```

Command:

```bash
claude -p --no-session-persistence --permission-mode plan --tools "Read,LS,Glob,Grep" --model sonnet
```

Prompt:

```text
Inspect this Flask weather app read-only. Do not edit files yet.

Report:
- request paths and handlers
- where user input enters the system
- where network calls happen
- where credentials are read
- what tests exist
- which actions you would need permission to take to improve safety
```

Output:

```text
The `Write` tool isn't available in this context, so I'll deliver the inspection report as text directly.

---

`★ Insight ─────────────────────────────────────`
Flask's `app.config` dict is used here as a dependency-injection slot — `WEATHER_CLIENT` is stored there so tests can swap in a fake without monkey-patching. This is a clean pattern for testable Flask apps that avoids global state.
`─────────────────────────────────────────────────`

---

## Request Paths and Handlers

| Route | Methods | Handler | Location |
|---|---|---|---|
| `/` | GET | Render search form | `main.py:35` |
| `/` | POST | Normalise city, redirect to `/<city>` | `main.py:23–33` |
| `/<city>` | GET | Fetch weather, render city page | `main.py:38–56` |
| `/error` | GET | Render static error page | `main.py:59–63` |

---

## Where User Input Enters the System

1. **Form POST body** — `request.form.get("search")` at `main.py:24`, passed through `normalize_city()` which strips whitespace and title-cases with `string.capwords`.
2. **URL path segment** — `/<city>` captures the city name directly from the URL at `main.py:38`, also passed through `normalize_city()`.

`normalize_city` is the **only sanitisation layer**. It normalises presentation but does not validate character set, length, or content beyond rejecting blank strings.

---

## Where Network Calls Happen

All outbound I/O is in `weather_client.py`, only reachable through `OpenWeatherClient.get_weather()`:

| Call # | Method | Endpoint | Location |
|---|---|---|---|
| 1 | Geocoding | `https://api.openweathermap.org/geo/1.0/direct` | `weather_client.py:88` |
| 2 | Current weather | `https://api.openweathermap.org/data/2.5/weather` | `weather_client.py:67` |
| 3 | Five-day forecast | `https://api.openweathermap.org/data/2.5/forecast` | `weather_client.py:76` |

All three share a single `requests.Session`, carry a 10-second timeout (`weather_client.py:103`), and pass the API key as a query parameter (`appid=`).

---

## Where Credentials Are Read

- `OpenWeatherClient.from_env()` at `weather_client.py:59–60` calls `os.getenv("OWM_API_KEY")`.
- `load_dotenv()` at `main.py:9` loads `.env` before `create_app()` runs, so the key is available at startup.
- The key is stored on `self.api_key` and sent as a query param in every API call — never logged, never rendered, never echoed back to the user.

---

## What Tests Exist

**`tests/test_app.py`** — Flask layer, uses `FakeWeatherClient` in-file; zero network calls.

| Test | What it covers |
|---|---|
| `test_normalize_city_trims_and_formats_city_names` | Normaliser unit test |
| `test_home_rejects_blank_city_without_calling_weather_client` | 400 on blank POST; client not called |
| `test_home_redirects_to_normalized_city_path` | POST normalises and redirects |
| `test_weather_route_renders_report` | GET renders city page from fake report |
| `test_weather_route_redirects_when_city_lookup_fails` | `WeatherLookupError` → redirect to `/error` |

**`tests/test_weather_client.py`** — Client layer, uses `FakeSession`/`FakeResponse`; zero network calls.

| Test | What it covers |
|---|---|
| `test_get_weather_uses_geocoding_then_weather_and_forecast_endpoints` | 3-call sequence, correct params |
| `test_missing_api_key_fails_before_network_call` | `WeatherConfigError` before any HTTP |
| `test_missing_geocoding_match_is_lookup_error` | Empty geocoding response → `WeatherLookupError` |
| `test_http_failure_is_lookup_error` | HTTP error → `WeatherLookupError` |

**Coverage gaps:**
- `WeatherConfigError` path in the Flask layer (`main.py:46–52`) — renders a 500, but has no test.
- The `/error` route itself has no test.

---

## Actions That Would Require Permission

These are the improvements I identified, ranked by severity, along with what permission each requires:

| # | Issue | Severity | File(s) to change |
|---|---|---|---|
| 1 | **No input length cap** — `/<city>` passes arbitrarily long strings to the geocoding API | Medium | `main.py` |
| 2 | **No character-set validation** — any Unicode passes `normalize_city`; could trigger unexpected API behaviour | Low–Medium | `main.py` |
| 3 | **`WeatherConfigError` branch untested in Flask layer** (`main.py:46–52`) | Low | `tests/test_app.py` |
| 4 | **`/error` route untested** | Low | `tests/test_app.py` |
| 5 | **`debug=True` in `__main__` block** (`main.py:72`) — leaks tracebacks if accidentally run in production | Low | `main.py` |
| 6 | **API key sent as query param** — visible in server/proxy logs; unavoidable (OWM API design), but worth noting | Info | `weather_client.py` |
| 7 | **No rate limiting** — every GET `/<city>` fires 3 API calls unconditionally | Info | `main.py` (+ new dependency) |

Items 1–5 are edits to existing files and stay within the project's stated boundaries. Item 7 would require adding a dependency (`Flask-Limiter`), which CLAUDE.md says needs a justification.
```
