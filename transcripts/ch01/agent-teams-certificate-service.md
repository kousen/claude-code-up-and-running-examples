⏺ I'll set up a three-teammate agent team for this Spring Boot project. Let me launch all three in parallel so
   the test review, security review, and documentation work happen concurrently, then I'll synthesize.

  ★ Insight ─────────────────────────────────────
  Two of these tasks (test-gap and security review) are read-only analysis, while the docs task makes actual
  edits. Running them in parallel is safe because they touch different concerns — but I'm scoping the docs
  agent to only README.md/CLAUDE.md so it can't collide with anything the reviewers are reading.
  ─────────────────────────────────────────────────

⏺ java-test-quality-expert(Review tests for coverage gaps)
  ⎿  Bash(find /Users/kennethkousen/Documents/java/certificate-service/src/test -type f | sort)
     Running…
     Bash(for f in src/main/java/com/kousen/cert/analytics/service/AnalyticsService.java
         src/main/java/com/kousen/cert/analytics/service/MetricsAggregationService.java
         src/main/java/com/kousen/cert/analytics/service/CertificateMetadataService.java
         src/main/java/com/kousen/cert/analytics/controller/AnalyticsController.java
         src/main/java/com/kousen/cert/analytics/controller/AnalyticsDashboardController.java
         src/main/java/com/kousen/cert/analytics/interceptor/ApiTrackingInterceptor.java; do echo "=== $f
         ==="; wc -l "$f"; done)
     Running…
     Bash(for f in src/main/java/com/kousen/cert/controller/CertificateController.java
         src/main/java/com/kousen/cert/controller/VerificationController.java
         src/main/java/com/kousen/cert/controller/HomeController.java
  Two of these tasks (test-gap and security review) are read-only analysis, while the docs task makes actual
  edits. Running them in parallel is safe because they touch different concerns — but I'm scoping the docs
  agent to only README.md/CLAUDE.md so it can't collide with anything the reviewers are reading.
  ─────────────────────────────────────────────────

⏺ java-test-quality-expert(Review tests for coverage gaps)
  ⎿  Bash(docker info >/dev/null 2>&1 && echo "DOCKER AVAILABLE" || echo "DOCKER NOT AVAILABLE -
         testcontainers tests skipped")
     Read(/Users/kennethkousen/Documents/java/certificate-service/build/reports/jacoco/test/jacocoTestReport.c
         sv)
     Bash(for x in /Users/kennethkousen/Documents/java/certificate-service/build/test-results/test/*.xml; do
     Bash(grep -o 'skipped message[^/]*' /Users/kennethkousen/Documents/java/certificate-service/build/test-re
         sults/test/TEST-com.kousen.cert.analytics.integration.AnalyticsIntegrationTest.xml | head; echo
         "---"; grep -A2 '<skipped' /Users/kennethkousen/Documents/java/certificate-service/build/test-results
     Bash(grep -rl "CertificateMetadataService\|ApiTrackingInterceptor\|AnalyticsController\|HomeController\|Q
         rCodeUtil\|GlobalExceptionHandler" /Users/kennethkousen/Documents/java/certificate-service/src/test/
         2>/dev/null; echo "=== integration test file ==="; sed -n '1,60p'
         /Users/kennethkousen/Documents/java/certificate-service/src/test/java/com/kousen/cert/integration/Cer
          /var/run/docker.sock 2>/dev/null || echo "no /var/run/docker.sock"; ls -la ~/.docker/run/docker.sock
          2>/dev/null; ls -la ~/.colima/default/docker.sock 2>/dev/null)
   the test review, security review, and documentation work happen concurrently, then I'll synthesize.

  ★ Insight ─────────────────────────────────────
  Two of these tasks (test-gap and security review) are read-only analysis, while the docs task makes actual
  edits. Running them in parallel is safe because they touch different concerns — but I'm scoping the docs
  agent to only README.md/CLAUDE.md so it can't collide with anything the reviewers are reading.
  ─────────────────────────────────────────────────

⏺ java-test-quality-expert(Review tests for coverage gaps)
  ⎿  Done (27 tool uses · 75.5k tokens · 2m 45s)
  (ctrl+o to expand)

⏺ Agent(Review code for security issues)
  ⎿  Done (18 tool uses · 54.2k tokens · 1m 33s)
  (ctrl+o to expand)

⏺ Agent(Update documentation for accuracy)
  ⎿  Done (28 tool uses · 49.3k tokens · 2m 1s)
  (ctrl+o to expand)


All three teammates have finished. Here's the synthesis.

## What changed

Only the **documentation teammate** made edits (the test and security teammates were read-only by design). Net diff:

```
 CLAUDE.md |  6 +++---
 README.md | 53 +++++++++++++++++++++++++++++++++++++++++++----------
 2 files changed, 46 insertions(+), 13 deletions(-)
```

- **CLAUDE.md**: corrected "Java 21 / Spring Boot 3.4.4" → "Java 25 (toolchain) / Spring Boot 3.5.7, Kotlin DSL build"; removed the non-existent `DATABASE_DRIVER` env var and documented the real DB vars + `HIBERNATE_DDL_AUTO` default of `update`.
- **README.md**: version corrections (Java 25, Spring Boot 3.5, Gradle 9.4 wrapper, JDK 25); documented the previously-undocumented `GET /api/certificates/signature-info` endpoint; added a full environment-variable table, a "Signing Keystore" setup section, the six allowed book titles, and the `X-Certificate-Id`/`X-Certificate-Status` response headers.

## What each teammate found

**🧪 Test coverage** — Suite passes (18 classes, ~65 methods, JaCoCo configured). Strong on crypto/PDF core; weak on controllers, the analytics REST layer, and DB compatibility. Top gaps:
- **High:** `AnalyticsIntegrationTest` (the only PostgreSQL test) is **silently skipped** — Testcontainers can't find Docker, so the H2-vs-Postgres dialect concern CLAUDE.md calls out is never actually exercised. No `@DataJpaTest` validates the custom JPQL. `CertificateController` error/404 paths untested.
- **Medium:** `GlobalExceptionHandler` 32%, `AnalyticsController` ~14% (3 of 5 endpoints never called), `CertificateMetadataService` has no dedicated test, monthly aggregation + cleanup untested, and the analytics error-swallowing "safety net" is never forced to fail.

**🔒 Security** — JPA queries are clean (all parameterized), no key material committed, Thymeleaf auto-escapes. But two **remotely exploitable, compounding** issues:
- **CRITICAL C1:** No authentication anywhere — `/admin/dashboard`, `/api/analytics/**` (purchaser PII), and certificate generation are fully public. `spring-boot-starter-security` isn't even on the classpath, though the prod logging config hints it was intended.
- **CRITICAL C2:** Path traversal in `CertificateController.java:162-166` → `CertificateStorageService.getCertificate()` — `{filename:.+}` + unvalidated `resolve()` allows reading arbitrary files (e.g., the keystore). Combined with C1 = unauthenticated arbitrary file read.
- **High:** Default keystore password `"changeit"` if `CERT_PWD` unset (`KeyStoreProvider.java:33-37`); H2 console enabled in the base profile; `ddl-auto: update` in production.

## Follow-up tasks needing a human decision

1. **Fix C1/C2 first** — these are the priority. Add Spring Security for `/admin/**` and the analytics/storage endpoints; normalize+validate the download path against the storage root. *(No code was changed — this is your call on scope.)*
2. **Keystore password (H1):** decide whether to fail-fast when `CERT_PWD` is unset in production rather than defaulting to `changeit`.
3. **PostgreSQL in CI:** decide whether Testcontainers should run on every build (needs Docker in CI) or nightly — but the current silent-skip should change either way.
4. **`ddl-auto: update` in prod:** keep, or move to `validate` + migrations (Flyway/Liquibase).
5. **Dead-code check:** confirm whether `QrCodeUtil` and `FontTester` (both 0% coverage) are live or should be removed/excluded.
6. **URL mismatch (docs):** `application.yaml`'s hardcoded `SERVER_URL` default (a Heroku URL) doesn't match the README's advertised `certificate-service.kousenit.com` — needs reconciliation.

Want me to act on any of these? The most impactful next step is wiring up Spring Security + the path-traversal fix (C1/C2) — I'd recommend doing those together since they're the exploitable pair.
