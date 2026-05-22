# ch05 lyrics trainer Playwright matrix

Date captured: 2026-05-22

This file records the committed Playwright suite and its test output. It is not
a verbatim Claude Code transcript.

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples/lyrics-trainer/ch05-navigation
```

Representative prompt:

```text
Add a Playwright browser-test suite for the lyrics-trainer navigation change.
Create a small TypeScript Playwright test that verifies the navigation controls,
ArrowRight shortcut, reload persistence, and lack of application console errors.
Configure the suite to run across Chrome, Firefox, WebKit, Mobile Chrome, and
Mobile Safari. Keep the existing Vitest unit tests passing.
```

Unit-test command:

```bash
npm test
```

Unit-test output:

```text
Test Files  2 passed (2)
Tests       17 passed (17)
```

Browser-matrix command:

```bash
npx playwright test --reporter=list,html
```

Representative browser-matrix output:

```text
Running 5 tests using 5 workers

  ✓  [Chrome]        navigation controls and keyboard shortcuts move between lines
  ✓  [Firefox]       navigation controls and keyboard shortcuts move between lines
  ✓  [WebKit]        navigation controls and keyboard shortcuts move between lines
  ✓  [Mobile Chrome] navigation controls and keyboard shortcuts move between lines
  ✓  [Mobile Safari] navigation controls and keyboard shortcuts move between lines

5 passed
```

HTML report:

```bash
npx playwright show-report
```

Notes:

- The suite uses Playwright projects so the same TypeScript test runs against
  browser and mobile profiles.
- The WebKit and Mobile Safari projects use Playwright's WebKit engine and
  device emulation rather than driving the Safari application directly.
- The generated `playwright-report/` and `test-results/` directories are local
  artifacts and are ignored by git.
