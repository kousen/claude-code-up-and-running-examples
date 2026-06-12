# ch05 lyrics trainer "What Did We Forget?" capture

Date captured: 2026-06-12

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples/lyrics-trainer/ch05-navigation
```

Commands:

```bash
claude -p "Look at the overall system again. What do you think? Are there changes we should make? Any cleanup steps we should do?"
claude -p "What have we forgotten to include that we should consider adding? What do other similar apps have that we don't? What would make our app unique?"
```

Model: Claude Code default (Fable 5). Outputs below are verbatim.

## Response 1: step-back review

All green — 17 unit tests and the 5-browser Playwright matrix all pass, working tree is clean, and the generated artifacts (`playwright-report/`, `test-results/`, `node_modules/`) are already covered by the repo-root `.gitignore`. Here's my assessment of the system as it stands.

## Overall: healthy, with one real gap

The architecture is doing exactly what the CLAUDE.md conventions ask for: `lineTrainer.js` and `storage.js` are pure and dependency-injected, `main.js` is the only file that touches the browser, and the tests sit at the right altitudes (Vitest for logic, Playwright for wiring). Nothing here needs restructuring.

`★ Insight ─────────────────────────────────────`
The storage module's design — taking any object with `getItem`/`setItem` rather than importing `localStorage` directly — is why the unit tests run in 117ms with no jsdom. This "ports and adapters in miniature" pattern is the main reason the test pyramid here is cheap to maintain.
`─────────────────────────────────────────────────`

### 1. Keyboard navigation is asymmetric (the one functional issue)

`src/main.js:32-38` handles **ArrowRight → next**, but there's no **ArrowLeft → previous**. The UI offers both buttons, so users will reasonably expect both arrows to work. The e2e test only exercises ArrowRight, which is why this never surfaced.

### 2. `main.js` repeats itself three times

Each handler is the same three-line ritual: move, save, render. Adding ArrowLeft as a fourth copy would make it worse. A small `move(direction)` helper would collapse all four call sites and guarantee you can never forget the `saveIndex` step in a future handler.

### 3. Minor test observations (fine to leave)

- The mobile Playwright projects pass the `keyboard.press("ArrowRight")` step because emulation still dispatches key events — that's testing wiring, not a real mobile interaction, which is acceptable but worth knowing.
- There's no e2e coverage of Previous via keyboard or of wrap-around; the unit tests cover wrap thoroughly, so I wouldn't add e2e weight there.

### 4. Cleanup: almost nothing to do

The only stale items are local `playwright-report/` and `test-results/` directories from a June 5 run — already gitignored, safe to delete or leave. CLAUDE.md and package.json accurately describe the current state.

---

If you'd like to fix the asymmetry, this is a nice spot for you to shape: the interesting decision is whether the keydown handler should become a small key→action lookup (easily extensible — Home/End to jump to first/last line is a natural Chapter 5 follow-on) or just a second `if` branch (simpler, matches the current style). I can prepare `main.js` with the shared `move()` helper and leave the key-mapping decision to you, or implement it whole — your call.

## Response 2: feature discovery

I've reviewed the whole app — it's a clean little machine: `lineTrainer.js` holds the index math, `storage.js` persists position, `main.js` glues them to a Previous/Next card showing Sonnet 18. Here's my assessment, organized around your three questions.

## What we've forgotten

These are gaps in things the app already half-promises:

1. **ArrowLeft.** `main.js:32-38` handles ArrowRight but not ArrowLeft, even though a Previous button exists. Anyone who discovers one arrow key will try the other. This is the most obvious oversight.
2. **Silent wrap-around.** Hitting Next on line 14 jumps to line 1 with no signal. For a *memorization* tool that's disorienting — you don't know you finished a pass. A "completed a pass" indicator, or disabling wrap in favor of an explicit "Start over," is a genuine design decision.
3. **Dark mode is declared but not delivered.** `index.html:8` sets `color-scheme: light dark`, but every color is hardcoded light (`#f5f1e8` background, `#2a2a2a` text). A dark-mode user gets dark scrollbars on a cream page. Either honor `prefers-color-scheme` or drop the declaration.
4. **No way to jump.** With 14 lines it's tolerable, but there's no "go to line N" or "restart from the top" — you click Next up to 13 times. Even a clickable progress dot per line would fix it.
5. **Touch users.** On a phone, swipe left/right is the expected gesture for this exact card UI. The buttons work, but it feels web-1.0 on mobile.
6. **One hardcoded text.** `texts.js` exports a single `lines` array, and the title is baked into the HTML. The module name is plural — the structure is already asking for `{ title, lines }` objects and a text picker.

## What similar apps have that we don't

The big one: **we built a reader, not a trainer.** The app is named Lyrics Trainer, but nothing ever tests recall — it just displays lines. Comparable memorization tools center on some form of *retrieval practice*:

- **Hide-then-reveal:** show the line blurred or hidden, user recites from memory, clicks to reveal and self-grades. (Flashcard apps like Anki are built entirely on this loop.)
- **Progressive word hiding:** verse-memorization apps typically let you fade a line out in stages — full text → first letters only ("S I c t t a s d?") → nothing. This is remarkably effective for poetry and song lyrics specifically.
- **Type-it-back:** show line N, user types line N+1, app diffs against the real text.
- **Spaced repetition:** lines you stumble on come back sooner. Probably overkill for a 14-line example, but it's the defining feature of the category.
- Smaller table stakes: progress bar, session stats ("3 passes today"), shuffle/quiz order.

## What would make ours unique

Most lyric/verse trainers treat text as flat lines. Ours is a *sonnet*, and poetry has structure no generic flashcard app uses:

- **Structure-aware hints:** when recalling line N, hint with its rhyme partner (Sonnet 18 is ABAB CDCD EFEF GG — "this line rhymes with *day*"). That's a memorization cue real actors and students use, and almost no app supports it.
- **Quatrain-level navigation:** practice by quatrain/couplet rather than the whole poem, matching how people actually chunk verse.
- **First-letter mode** is rare enough in general-purpose apps that doing it well, framework-free, would itself be distinctive.

`★ Insight ─────────────────────────────────────`
- The current architecture makes most of these cheap: because `createLineTrainer` is pure and DOM-free, a "reveal state" or "hidden-word level" is just more index-like state in the same closure, testable in Vitest without a browser — the chapter's "browser APIs behind small functions" convention is exactly what pays off here.
- The one suggestion that *fights* the architecture is spaced repetition: it needs per-line history in storage, which outgrows the current single-integer `saveIndex` design. That's the feature that would force a real schema decision.
`─────────────────────────────────────────────────`

If I were picking for the book's purposes, the highest value-to-size ratio is: **ArrowLeft + hide/reveal recall mode**, because reveal mode is the smallest change that turns the reader into an actual trainer, and it creates a meaningful state-design choice (is "revealed" part of the trainer core, or DOM-glue state in `main.js`?) — a nice fit for a chapter about keeping behavior testable. Say the word and I'll plan it out.
