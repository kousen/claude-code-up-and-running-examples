# Lyrics Trainer

Small browser app for practicing a public-domain text one line at a time.
The Chapter 4 version keeps the app framework-free while moving behavior into
testable JavaScript modules.

## Current architecture

- `index.html` provides the page shell.
- JavaScript modules under `src/` contain testable behavior.
- `src/main.js` is DOM glue only.
- Unit tests live under `test/` and run with Vitest.

## Commands

- `npm test` -- run unit tests.
- `npm start` -- serve the app locally at `http://localhost:8000`.

## Conventions

- Prefer plain JavaScript modules before adding a framework.
- Keep browser APIs behind small functions so core behavior can be tested.
- Do not add a build step unless a later chapter explicitly calls for one.
- Use public-domain text in examples.

## Workflow

- For nontrivial changes, propose a plan before editing.
- After a feature lands, run tests and then review the whole app for issues
  the change introduced or revealed.
