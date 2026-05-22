# Chapter 5 weather-app validation prompt

The narrow, permission-bounded change (ch05 ~lines 450-465). It demonstrates
"permission as forcing function": the no-network / no-secrets constraints push
the design toward a mockable client. Capture the clarifying questions, the diff,
and the pytest run.

```text
Add validation for the submitted city name:

- reject empty or whitespace-only input
- trim leading and trailing whitespace
- preserve normal city names with spaces, such as "New York"
- show a user-friendly error message
- do not call the weather API when validation fails

Add tests for the route and service behavior. Run pytest.

Do not add dependencies. Do not make live network calls. Do not read or print real API keys. If the current tests require network access, stop and explain before changing them.
```
