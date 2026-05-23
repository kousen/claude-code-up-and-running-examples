# ch06 certificate service agent team

Date captured: 2026-05-23

Working directory:

```text
/private/tmp/certificate-service-ch06-agent-team
```

Prompt:

```text
You are running in a disposable branch/worktree for a transcript capture.

Create an agent team for this Spring Boot certificate-service project.

Use three teammates with disjoint ownership:

- tests-reviewer: src/test/** only; read-only. Look for coverage gaps.
- security-reviewer: src/main/** and build files; read-only. Look for
  credential handling, certificate validation, path traversal, and dependency
  CVE risks.
- docs-owner: README.md, CLAUDE.md, and docs/** only; may edit docs after plan
  approval. Update setup notes and any drift between behavior and documentation.

Run them in parallel where possible. Because this is a headless transcript
capture, do not use split-pane mode; summarize the team shape in text instead.

Before docs-owner edits files, propose the docs edit plan. For this capture,
the human pre-approves that plan only if it is limited to README.md, CLAUDE.md,
and docs/** and does not touch source code, build files, secrets, or
configuration. If the docs plan exceeds that scope, stop and ask for approval
instead of editing.

When the work is complete, synthesize. Report what changed, what each teammate
found, and any follow-up tasks that should remain for a human decision.
```

Output:

```text
★ Insight ─────────────────────────────────────
- The two confirmed doc edits both came from real version-control evidence: `build.gradle.kts` pins `3.5.7`, and commit `f93a1e7 "Port to Railway"` added infra files without touching docs. Plan items grounded in `git log` survived review; the unverified wrapper-version item didn't.
- Spawning the doc-owner as `Explore` (read-only) made the plan-first gate natural — the agent literally couldn't bypass it. The editing step came back to the orchestrator after human-policy approval, keeping the write authority in one place.
─────────────────────────────────────────────────

---

## Synthesis

### Team shape (text, since headless)
| Teammate | Scope | Mode | Output |
|---|---|---|---|
| tests-reviewer | `src/test/**` | read-only | gap inventory |
| security-reviewer | `src/main/**` + build | read-only | findings list |
| docs-owner | `README.md`, `CLAUDE.md`, `docs/**` | plan → edit (gated) | 2 README edits |

All three ran in parallel in a single message.

### What changed
- `README.md`: "Spring Boot 3.5" → "Spring Boot 3.5.7"
- `README.md`: added a "Railway Deployment" subsection alongside Heroku (drift introduced by commit `f93a1e7`)

No other files touched.

### Findings by teammate

**tests-reviewer — coverage gaps (top items)**
- **HIGH**: `GlobalExceptionHandler` has no tests for any of its handlers.
- **HIGH**: `AnalyticsController` (`/api/analytics/*`) and `AnalyticsDashboardController` (`/admin/dashboard`) are untested.
- **HIGH**: `ApiTrackingInterceptor` untested (response-time calc, afterCompletion exception path).
- **HIGH**: `PdfSignerTest` is a stub — the actual signing pipeline is not exercised.
- **HIGH**: `AnalyticsServiceTest` uses `future.get()` without timeout — risk of hangs.
- **MED**: Negative-path coverage gaps in `KeyStoreProvider`, `QrCodeGenerator`, `CertificateStorageService` (disk-full, perm-denied, path traversal).
- **MED**: Several analytics endpoints (`/trends`, `/books`, `/performance`) lack integration tests.

**security-reviewer — findings**
1. **Critical** — Hardcoded `"changeit"` keystore-password fallback (`KeyStoreProvider.java:35`, `PdfSigner.java:50`).
2. **Critical** — `/admin/dashboard` has no auth (`AnalyticsDashboardController.java:17`).
3. **High** — H2 console enabled at `/h2-console` in base `application.yaml:20-22` with no restriction.
4. **High** — User-supplied filename in `CertificateController.java:162` sanitized by regex; potential traversal via Unicode normalization.
5. **High** — Temp files created without guaranteed cleanup (`PdfBoxGenerator.java:47,218`; `PdfSigner.java:65`).
6. **Medium** — Empty default DB password and weak defaults (`sa`/`testdb`) in `application.yaml`.
7. **Info** — QR verification URL trusts `certificate.verification.base-url`.

Clean: parameterized JPA queries, RSA-4096 + SHA-512, ownership checks on cert lookups, validated user input for PDF generation.

**docs-owner — plan executed**
- Spring Boot version corrected (3.5 → 3.5.7).
- Railway deployment now documented.
- Skipped: "Gradle 9.4" wording (matches actual `9.4.0`, not real drift).
- Flagged out-of-scope: `TODOs.md` lists Analytics Dashboard as "long-term" though it already ships — needs human triage (non-doc file, not edited).

### Follow-ups for human decision
1. **Security — Critical**: replace `"changeit"` fallback with a fail-fast when `CERT_PWD` is missing.
2. **Security — Critical**: add auth (Spring Security) to `/admin/dashboard` and `/api/analytics/**`.
3. **Security — High**: disable H2 console outside `dev`/`test` profiles, or front it with auth.
4. **Security — High**: harden `CertificateController` filename handling — resolve against a fixed base dir and reject paths whose normalized form escapes it.
5. **Security — High**: wrap PDF temp-file creation in try-with-resources / `Files.deleteIfExists` in `finally`.
6. **Tests**: add `GlobalExceptionHandler`, analytics controller, and `ApiTrackingInterceptor` test classes; convert `PdfSignerTest` from stub to real signing test using the test keystore.
7. **Tests**: add timeouts to async `.get()` calls; add Awaitility for integration-level async assertions.
8. **Docs/Backlog**: reconcile `TODOs.md` with shipped analytics dashboard.
9. **CVE sweep** (not done in this pass): the security reviewer focused on code patterns; a `./gradlew dependencyCheckAnalyze` (or equivalent) against PDFBox/BouncyCastle/Spring Boot versions in `build.gradle.kts` is worth scheduling.

Human Outcome: 2 doc edits applied; 15 actionable findings (7 security, 8 tests) handed back without code changes outside the docs-owner's scope.
```
