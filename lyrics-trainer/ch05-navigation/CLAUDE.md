# Lyrics Trainer

Small browser app for practicing a public-domain text one line at a time.
The Chapter 5 version keeps the app framework-free while adding navigation
behavior and repeatable browser checks.

## Current architecture

- `index.html` provides the page shell.
- JavaScript modules under `src/` contain testable behavior.
- `src/main.js` is DOM glue only.
- Unit tests live under `test/` and run with Vitest.
- Browser tests live under `e2e/` and run with Playwright Test.

## Commands

- `npm test` -- run unit tests.
- `npm start` -- serve the app locally at `http://localhost:8000`.
- `npm run test:browser` -- run the Playwright browser matrix.
- `npm run test:browser:report` -- run the matrix and generate an HTML report.
- `npm run show-report` -- open the latest Playwright HTML report.

## Conventions

- Prefer plain JavaScript modules before adding a framework.
- Keep browser APIs behind small functions so core behavior can be tested.
- Do not add a build step unless a later chapter explicitly calls for one.
- Use public-domain text in examples.
- Treat `playwright-report/` and `test-results/` as local generated artifacts.

## Workflow

- For nontrivial changes, propose a plan before editing.
- After a feature lands, run tests and then review the whole app for issues
  the change introduced or revealed.
