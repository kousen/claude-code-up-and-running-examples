# Chapter 5: Lyrics Trainer Playwright Matrix

Use from a fresh branch or disposable working copy of
`lyrics-trainer/ch05-navigation`.

```text
Add a Playwright browser-test suite for the lyrics-trainer navigation change.

Create a small TypeScript Playwright test that verifies:

- the page starts on line 1
- clicking Next advances to line 2
- pressing ArrowRight advances to line 3
- clicking Previous returns to line 2
- reloading keeps the saved line
- the browser console has no application errors

Configure the suite to run across Chrome, Firefox, WebKit, Mobile Chrome, and
Mobile Safari. Add npm scripts for running the browser tests and opening the
HTML report. Keep the existing Vitest unit tests passing.

After the implementation, run the unit tests and the Playwright browser matrix.
Summarize the result as a compact table and point me to the HTML report.
```
