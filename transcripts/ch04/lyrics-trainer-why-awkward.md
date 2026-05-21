# ch04 lyrics trainer why awkward

Date captured: 2026-05-21

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples/lyrics-trainer/ch04-testable-core
```

Prompt:

```text
The current lyrics-trainer works in the browser. Why is it awkward to test?
```

Output:

```text
Now I can give you a concrete answer. Here's the whole app — and the problem is that everything lives tangled together in one `<script>` block inside `index.html`.

## Why it's awkward to test

**1. The logic isn't reachable from a test.** There's interesting logic here worth testing — `loadIndex()` (lines 104–110) validates stored values, and the "next" handler wraps around with modulo (line 123). But these functions are defined *inside* an inline `<script>` tag. There's nothing to `import`. A test runner like Vitest or Jest can't get a handle on `loadIndex` or the wrap-around behavior without loading and parsing the entire HTML page.

**2. Logic and the DOM are fused.** Look at how the pieces depend on each other:

- `loadIndex()` reads `localStorage` directly (line 105) — a browser global.
- `render()` reaches for `document.getElementById` results (lines 118–119) — it can't run without a real DOM.
- The wrap-around math (line 123) is glued to a click handler, `localStorage.setItem`, and `render()` all in one arrow function.

So even the *pure* logic — "given index 13 of 14, next should be 0" — can't be exercised on its own. To test it you'd have to stand up a full browser-like environment (jsdom or a headless browser), simulate a click, and read text back out of a DOM node. That's an end-to-end test pretending to be a unit test: slow, brittle, and it tells you little about *why* something broke.

**3. Global mutable state.** `currentIndex` (line 112) is a module-level `let`. There's no way to reset it between test cases or construct a fresh instance — every test would pollute the next.

**4. Hidden dependencies on browser globals.** `localStorage`, `document`, and `addEventListener` are all assumed to exist. In a plain Node test process, none of them do. You'd have to mock all three before any code could run.

`★ Insight ─────────────────────────────────────`
- The core testability problem is **coupling**: pure decision logic (index validation, wrap-around) is welded to **side effects** (DOM writes, localStorage I/O). Tests want the decisions; the side effects are what make tests expensive.
- This is why "ch04-testable-core" is the next step — the standard fix is to extract the pure logic into a separate module that takes its dependencies as *inputs and outputs* rather than reaching for globals.
- A good litmus test: "Can I verify this behavior without a browser?" If no, the logic is trapped.
`─────────────────────────────────────────────────`

The chapter name — **testable-core** — tells you where this is heading: pull the decision logic out into its own importable, browser-free module, leaving a thin DOM layer on top that's the only part needing a browser.

Want me to walk through *which* functions to extract first, or would you like to take a crack at sketching the seam yourself? Given the chapter goal, the most interesting design decision is **what shape the extracted core should take** — a class holding `currentIndex`, or pure functions that take state in and return new state out. That choice drives everything downstream.
```
