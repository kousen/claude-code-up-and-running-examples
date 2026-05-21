# ch04 lyrics trainer whole app review

Date captured: 2026-05-21

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples/lyrics-trainer/ch04-testable-core
```

Prompt:

```text
Now that the refactor and tests are done, step back and review the whole app again. Look for issues this change introduced or revealed: state management, test gaps, naming, accessibility, and places where the single-page structure is starting to strain. Don't make changes yet; report findings with severity and recommendation.
```

Output:

```text
Tests are green (15 passing). The refactor is clean — pure core in `lineTrainer.js`, storage behind an injectable interface, `main.js` reduced to DOM glue. Here's my review of what the change introduced or left exposed.

`★ Insight ─────────────────────────────────────`
- The seam you created (passing a `Storage`-like object into `storage.js`) is the chapter's real win — it lets you test persistence with a plain-object fake and no jsdom. The remaining gaps are mostly about what happens *outside* that seam: the unguarded browser boundary in `main.js`.
- `normalizeIndex` is reused as the single validation choke point for both initial state and storage reads. That's good DRY, but it means its edge-case behavior (e.g. `Number(true) === 1`) silently governs both paths.
`─────────────────────────────────────────────────`

## Findings

### State management

**M1 — Model/view desync if `localStorage.setItem` throws.** `main.js:18-22`
The click handler calls `trainer.next()` (mutates index), then `saveIndex(...)`, then `render()`. If `setItem` throws (Safari private mode, quota), the exception fires *between* the mutation and the render: the trainer has already advanced but the screen never updates, and the next click advances again. The model and view drift apart on the one failure mode persistence actually has.
*Recommendation:* render before/independently of saving, or wrap the save so a storage failure can't block the render.

**M2 — No guard on the storage boundary at startup.** `main.js:7`, `storage.js:11`
`loadSavedIndex` calls `storage.getItem` directly. If storage is disabled/throws, module init throws and the whole app fails to render — even though a sensible fallback (line 0) exists. The chapter's stated goal is "keep browser APIs behind small functions"; `storage.js` is the right place to also absorb their failures.
*Recommendation:* try/catch in `loadSavedIndex`/`saveIndex`, falling back to 0 / no-op.

**L1 — `main.js` reaches into `lines.length` rather than asking the trainer.** `main.js:15`
The counter computes `of ${lines.length}` from the imported array, duplicating knowledge the trainer already owns. Low risk today (same array reference) but it's a second source of truth for "how many lines."
*Recommendation:* expose `trainer.total()` and let glue stop importing `lines` for the count.

### Test gaps

**M3 — Empty/degenerate `lines` is an untested crash.** `lineTrainer.js:30`
With an empty array, `next()` computes `(index + 1) % 0 === NaN` and `currentLine()` returns `undefined`. No guard, no test. `texts.js` always has content today, so this is latent — but it's exactly the kind of edge a "testable core" should pin down.
*Recommendation:* either document the precondition or guard + test it.

**L2 — `normalizeIndex` truthy-boolean surprise is untested.** `lineTrainer.js:7`
`Number(true) === 1` → treated as a valid index 1; `""` and `" "` coerce to 0. Harmless from real `localStorage` (always strings), but the function is exported and reused, so the boundary deserves a test documenting intent.

**L3 — No coverage of the DOM glue or counter formatting.** `main.js`
By design `main.js` is untested, but the `Line X of Y` string and the wiring have zero coverage. Acceptable for the chapter; worth naming as a deliberate gap (a later chapter could add a Playwright/jsdom smoke test).

### Naming

**L4 — `texts.js` exports `lines`.** File name says "texts," export says "lines" — mild concept mismatch. And `createLineTrainer(lines, ...)` shadows the module export with a generic param of the same name. Both readable, but if multi-text support arrives the vocabulary will need sorting out.

### Accessibility

**M4 — Two competing `aria-live="polite"` regions.** `index.html:79-80`
Both the counter and the line update on every Next, so a screen reader queues two announcements per click ("Line 3 of 14" *and* the line text). It's chatty and the ordering isn't guaranteed meaningful.
*Recommendation:* make the line the single live region; drop `aria-live` from the counter (or mark it `aria-hidden` for SR purposes).

**L5 — `color-scheme: light dark` declared but colors are hardcoded light.** `index.html:8-13`
You opt into dark-mode form-control rendering, but the body background/text are fixed light values, so dark-mode users get a light page with possibly mismatched controls. Either honor dark mode with a `prefers-color-scheme` block or drop the declaration.

**L6 — No `<main>` landmark.** Content sits in a bare `div.card`. Minor structural a11y gap.

### Single-page structure strain

**M5 — Persistence key assumes exactly one text.** `storage.js:6`
`DEFAULT_KEY` is a single global. The architecture currently bakes in "one poem": `texts.js` exports one array, the trainer is constructed once, and resume position is stored under one key. The moment a text *selector* arrives, resume positions collide across texts and the trainer needs re-creation. This is the clearest place the single-page structure will strain next.
*Recommendation:* when multi-text lands, namespace the storage key per text and make text selection the thing that constructs the trainer.

**L7 — Title duplicates the data.** `index.html:5,77`
"Sonnet 18" is hardcoded in two places in the HTML and is implicit in `texts.js`. Change the text and the title goes stale. Fine now; a coupling to remember.

---

**Severity tally:** 0 high, 5 medium (M1–M5), 7 low. Nothing blocks the chapter. The two I'd weigh most: **M1/M2** (the storage boundary is the one place this app talks to a flaky browser API, and it's currently unguarded) and **M5** (the single-text assumption is the architectural seam most likely to tear in the next feature). No changes made — let me know which you'd like to address.
```
