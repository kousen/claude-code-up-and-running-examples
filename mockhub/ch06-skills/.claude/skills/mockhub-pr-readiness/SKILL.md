---
description: Prepare a MockHub branch for pull request review. Use when the user asks whether a branch is PR-ready, asks for a pre-PR review, or asks to check feature work before publishing.
disable-model-invocation: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(git status *)
  - Bash(git diff *)
  - Bash(git log *)
  - Bash(./gradlew test *)
  - Bash(npm test *)
  - Bash(npm run test *)
  - Bash(npm run lint *)
---

# MockHub PR Readiness

Start by inspecting the working tree. If there are unrelated changes, separate
them in the report instead of reverting them.

Check:

1. The branch has a clear issue or feature scope.
2. Backend changes follow feature-based package boundaries.
3. Controllers do not access repositories directly.
4. DTOs are records and entities do not leak through controllers.
5. Tests cover the changed backend, frontend, integration, or browser behavior.
6. No real credentials are read, printed, or required for tests.
7. The diff does not add broad agent permissions or release shortcuts.
8. Documentation changed when behavior changed.
9. CI-relevant commands are documented if they differ from local checks.

Run the narrowest useful checks first. Prefer fast tests during the review, then
recommend slower integration or browser suites when the blast radius justifies
them.

Report:

- files changed
- commands run
- tests passed, failed, skipped, or not run
- risks or missing checks
- whether the branch is ready, nearly ready, or not ready
- remaining human decisions

Do not push, deploy, change secrets, or merge branches.
