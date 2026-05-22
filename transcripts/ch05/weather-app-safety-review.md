# ch05 weather app safety review

Date captured: 2026-05-22

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples/weather-app/ch05-permissions
```

Command:

```bash
claude -p --no-session-persistence --effort low --permission-mode plan --tools "Read,LS,Glob,Grep" --model sonnet
```

Prompt:

```text
Review this Flask weather app read-only for safety and trust-boundary issues. Do not edit files.

Return at most five findings. For each finding use this format:
Severity:
Evidence:
Risk:
Recommended permission boundary or workflow change:

Focus on input validation, secrets, network calls, external-service tests, risky scripts, and git/repository operations.
```

Output:

```text
I don't have a Write tool available in this session context (plan mode restricts me to only the plan file Write, but the Write tool itself is not appearing in my available tools). Let me deliver the findings directly in my response — this is a read-only review with no edits required anyway.

---

Here are the five findings from the security and trust-boundary review:

---

**Finding 1**

**Severity:** Medium

**Evidence:** `main.py:37` — the route is `/<city>`, an open wildcard. Any path not matching `/` or `/error` (including `/admin`, `/.env`, `/static/../../etc/passwd`) reaches the `weather` route. `normalize_city` strips and title-cases the value, which defends against blank input, but does not reject paths containing slashes, dots, or other traversal characters that the URL router will already have decoded.

**Risk:** Unexpected paths are silently passed to the weather client. A path like `/../secrets` won't traverse the filesystem here, but it reveals that the route has no explicit allowlist of acceptable characters, making it harder to reason about what the trust boundary actually accepts.

**Recommended permission boundary or workflow change:** Add a compile-time converter or an explicit validation guard at the top of the `weather` view that rejects city names containing anything other than Unicode letters, spaces, hyphens, and apostrophes (characters plausible in a real city name). Reject and redirect rather than passing the value downstream.

---

**Finding 2**

**Severity:** Medium

**Evidence:** `main.py:71-72` — the module-level `app = create_app()` call runs unconditionally at import time with `debug=True` hard-coded in `__main__`. More critically, `OpenWeatherClient.from_env()` is called during `create_app()` with no key (`weather_client.py:59-60`). If `OWM_API_KEY` is absent the client is constructed with `api_key=None`; the guard only fires later at `get_weather` time (`weather_client.py:63`). This means the app starts silently in a half-configured state rather than failing fast.

**Risk:** Misconfigured deployments serve real traffic until the first weather request, at which point the 500 error path is exercised in production. A fail-fast check at startup would surface the misconfiguration immediately.

**Recommended permission boundary or workflow change:** Add an explicit key-presence assertion inside `from_env()` (or in `create_app`) so that a missing `OWM_API_KEY` raises `WeatherConfigError` at startup rather than deferring to the first request.

---

**Finding 3**

**Severity:** Low–Medium

**Evidence:** `weather_client.py:87-91` — the geocoding call passes the raw `city_name` string directly as the `q` parameter: `{"q": city_name, "appid": self.api_key, "limit": 3}`. The `requests` library URL-encodes this safely, so injection into the URL is not the concern. The concern is that `limit: 3` is a hard-coded constant in application logic rather than a named constant or config value, and more importantly the first match is blindly trusted (`location_data[0]`) without any country or locale constraint. A city name like "Springfield" returns whichever of the 30+ Springfields OpenWeather ranks first.

**Risk:** Ambiguous city names silently return weather for an unintended location. This is a data-integrity trust boundary issue: the app trusts OpenWeather's ranking rather than surfacing ambiguity to the user.

**Recommended permission boundary or workflow change:** Either surface multiple matches for user disambiguation, or document clearly that resolution is delegated to OpenWeather's ranking and add a test that asserts the first-match behavior is intentional.

---

**Finding 4**

**Severity:** Low

**Evidence:** `weather_client.py:107` — the exception message in `_get_json` includes the `url` string: `f"OpenWeather request failed: {url}"`. This message propagates to `WeatherLookupError`, which `main.py:53-54` catches and redirects silently — so the URL does not leak to end-users. However, if any logging middleware or error tracker (Sentry, etc.) ever logs `WeatherLookupError` messages, the full endpoint URL (including the `appid` query parameter at that point in the call) could appear in logs.

**Risk:** The API key could appear in error logs if the exception is logged before the params are separated from the URL, or if a future refactor logs the full `exc` chain. The `requests` library does attach the prepared request (including full URL with params) to `RequestException` as `exc.request`.

**Recommended permission boundary or workflow change:** Strip the API key from error messages by catching `requests.RequestException`, extracting only the base URL (without params), and constructing the `WeatherLookupError` from that sanitized string. Consider a `scrub_key` helper in `weather_client.py`.

---

**Finding 5**

**Severity:** Low

**Evidence:** `.gitignore` protects `.env`, but `.env.example` (`OWM_API_KEY=replace-with-your-openweather-key`) is committed and tracked. The `requirements.txt` pins `python-dotenv>=1.0,<2.0` and `main.py:9` calls `load_dotenv()` unconditionally at module level. There is no `pytest.ini`, `conftest.py`, or fixture that prevents `load_dotenv()` from running during test collection — if a developer has a real key in `.env`, tests run against the real API unless the fake client injection in `create_app(weather_client)` is used. `test_weather_client.py` correctly injects `FakeSession`, but `test_app.py` creates the full `app` only through `create_app(FakeWeatherClient(...))`, so the real key path is never exercised in tests. The risk here is accidental real-API calls if someone adds a test that calls `create_app()` without a fake client.

**Risk:** A developer who adds a test using the bare `create_app()` (no argument) will silently hit the real OpenWeather API if `.env` is present, consuming quota and potentially making tests non-deterministic.

**Recommended permission boundary or workflow change:** Add a `conftest.py` that sets `OWM_API_KEY` to a sentinel value (`"test-key-do-not-use"`) via `monkeypatch.setenv` or `os.environ` before any test, ensuring the real key can never be loaded during test runs regardless of local `.env` content. The CLAUDE.md already calls this out as a rule — a `conftest.py` enforces it automatically.
```
