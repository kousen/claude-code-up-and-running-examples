# Chapter 4 lyrics-trainer add-tests prompt

The main cabin-transition prompt: run against `lyrics-trainer/ch04-testable-core`
(seeded from the Ch3 single-file app). It asks for a test plan and file plan
before editing, which is what exposes the refactor pressure. Capture the plan,
the proposed file layout, the refactor, and the test run.

```text
Add automated tests for the current lyrics-trainer behavior:
- advancing to the next line
- wrapping at the end
- resuming from localStorage
- falling back to line 0 when the saved index is invalid

Keep the browser behavior unchanged. Keep the app framework-free. Use the smallest project structure that lets those behaviors be tested.

Before editing, show me the test plan and file plan. If there are multiple reasonable approaches, ask me to choose.
```
