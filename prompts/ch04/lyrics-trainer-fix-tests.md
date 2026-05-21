# Chapter 4 lyrics-trainer fix-failing-tests prompt

Used if `npm test` fails after the refactor. The "explain the likely cause"
step is deliberate: it stops Claude Code from patching the symptom without
naming the assumption that broke. Append the exchange to the Ch4 transcript.

```text
The Vitest suite is failing. Read the failure output, explain the likely cause, then fix the related code and tests until the suite passes.

Keep the browser behavior unchanged. When you are done, summarize what changed and what you verified.
```
