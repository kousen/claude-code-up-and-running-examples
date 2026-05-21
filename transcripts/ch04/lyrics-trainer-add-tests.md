# ch04 lyrics trainer add tests

Date captured: 2026-05-21

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples/lyrics-trainer/ch04-testable-core
```

Prompt:

```text
Add automated tests for the current lyrics-trainer behavior:
- advancing to the next line
- wrapping at the end
- resuming from localStorage
- falling back to line 0 when the saved index is invalid

Keep the browser behavior unchanged. Keep the app framework-free. Use the smallest project structure that lets those behaviors be tested.

Before editing, show me the test plan and file plan. If there are multiple reasonable approaches, ask me to choose.
```

Initial Claude Code output, excerpted:

```text
The test run needs your approval to execute `node` -- go ahead and approve it, or run `node --test` yourself in that folder. Either way, here's the current state.

## What's done

- **`lyrics-core.js`** -- pure logic, dual-target (browser global `LyricsCore` + Node `require`). Double-clicking `index.html` still works.
- **`lyrics-core.test.js`** -- all six tests covering your four behaviors, using only `node:test`/`node:assert`. No `npm install`, no `package.json`, framework-free.
- **`index.html`** -- now calls `nextIndex(...)` and `loadIndex(...)` from the core; DOM wiring and visible behavior unchanged.

## One piece left for you -- and it's the interesting one

I deliberately left `loadIndex` in `lyrics-core.js:32` unimplemented. This is the function with a real design decision behind it, not boilerplate: **what counts as a "valid" saved index?**

In `lyrics-core.js`, replace the `// <-- your 4-5 lines here` placeholder:

const stored = Number(raw);
if (!Number.isInteger(stored) || stored < 0 || stored >= length) {
  return 0;
}
return stored;
```

Continuation prompt:

```text
Please continue, but align this Chapter 4 example with the book's intended file layout and the existing figure: package.json, src/lineTrainer.js, src/storage.js, src/texts.js, src/main.js, test/lineTrainer.test.js, and test/storage.test.js. Use Vitest behind an npm test script. Keep the browser behavior unchanged, keep the app framework-free, and do not add a build step. Fill in the validation yourself rather than leaving a TODO for me. Run npm test when you are done, and summarize the plan, changed files, and test result.
```

Claude Code output, excerpted:

```text
## Plan

Restructure the single-file app into the book's intended module layout, with the pure logic (line navigation, storage validation) split out so Vitest can import the same `src/*.js` files the browser runs -- no build step, no bundler, framework-free. `main.js` is the only DOM-touching file.

## Changed files

| File | Status | Contents |
|------|--------|----------|
| `package.json` | new | `"type": "module"`, `"test": "vitest run"`, vitest as the only devDependency |
| `src/texts.js` | new | exports `lines` (the 14-line sonnet) |
| `src/lineTrainer.js` | new | `nextIndex(current, length)` -- advance + wrap |
| `src/storage.js` | new | `STORAGE_KEY`, `loadIndex(storage, length)` (validation filled in), `saveIndex(storage, index)` |
| `src/main.js` | new | imports the three modules, wires DOM + `localStorage`; behavior identical to before |
| `test/lineTrainer.test.js` | new | advance, wrap |
| `test/storage.test.js` | new | resume, + 3 fallback cases (non-numeric, out-of-range, missing) using a fake storage object |
| `index.html` | modified | inline script replaced with `<script type="module" src="src/main.js">`; removed old `lyrics-core.js` |
| `lyrics-core.js`, `lyrics-core.test.js` | deleted | superseded by the `src/`/`test/` layout |

## Test result

Not yet run -- `npm install` and `npm test` are both waiting on a permission approval that I can't grant. The tests are written against 7 cases total (2 navigation + 5 storage).

Browser caveat: because this now uses native ES modules with no build step, `index.html` must be opened via a local server, not double-clicked.
```

Follow-up prompt:

```text
Please revise the Chapter 4 refactor so the line-navigation state lives in the testable core, matching the book's intended snippets. Specifically: src/lineTrainer.js should export createLineTrainer(lines, initialIndex = 0) plus normalizeIndex(value, length). createLineTrainer should expose currentLine(), currentIndex(), and next(). src/storage.js should export DEFAULT_KEY = "lyricsTrainer.lineIndex", loadSavedIndex(storage, lineCount, key = DEFAULT_KEY), and saveIndex(storage, index, key = DEFAULT_KEY), using normalizeIndex rather than duplicating validation. src/main.js should create a trainer from the saved index and keep DOM glue thin. Keep src/texts.js and the Vitest layout. Update tests so createLineTrainer, normalizeIndex, loadSavedIndex, and saveIndex are covered. Preserve visible browser behavior. Also add aria-live="polite" to the changing line/counter region and darken the counter color enough for normal small text. Run npm test if the permission system allows it; if not, say so and summarize the changed files.
```

Claude Code output, excerpted:

```text
The cleanest win here is that `loadSavedIndex` is now **three lines that delegate** to `normalizeIndex`. Before, validation lived in two places; now there's one rule, and the trainer, the loader, and the constructor all enforce it identically.

## Changed files

**`src/lineTrainer.js`** -- Replaced the lone `nextIndex` with:
- `normalizeIndex(value, length)` -- the shared coercion/validation.
- `createLineTrainer(lines, initialIndex = 0)` -- stateful closure holding the index; exposes `currentLine()`, `currentIndex()`, and `next()`.

**`src/storage.js`** -- Now imports `normalizeIndex` and exports:
- `DEFAULT_KEY = "lyricsTrainer.lineIndex"`.
- `loadSavedIndex(storage, lineCount, key = DEFAULT_KEY)` -- delegates validation to `normalizeIndex`.
- `saveIndex(storage, index, key = DEFAULT_KEY)` -- key-parameterized.

**`src/main.js`** -- Glue only: builds `trainer` from `loadSavedIndex(...)`, and the click handler is `trainer.next()` -> `saveIndex(...)` -> `render()`. No app state lives here anymore.

**`index.html`** -- `aria-live="polite"` added to both `#counter` and `#line`; counter color darkened `#999` -> `#6a6a6a`.

**`test/lineTrainer.test.js`** -- Rewritten: covers `normalizeIndex` and `createLineTrainer`.

**`test/storage.test.js`** -- Rewritten with an object-backed fake storage: covers `loadSavedIndex` and the previously untested `saveIndex`.

`npm test` now comes back as "requires approval" rather than running.
```

Verification run outside Claude Code:

```text
> lyrics-trainer-ch04@1.0.0 test
> vitest run

 RUN  v4.1.7 ~/Documents/books/claude-code-up-and-running-examples/lyrics-trainer/ch04-testable-core

 Test Files  2 passed (2)
      Tests  15 passed (15)
   Duration  122ms
```

Browser smoke check outside Claude Code:

```text
Served with `python3 -m http.server 8024`, opened at http://127.0.0.1:8024/.

Before click:
Line 2 of 14
Thou art more lovely and more temperate:

After click:
Line 3 of 14
Rough winds do shake the darling buds of May,

After reload:
Line 3 of 14
Rough winds do shake the darling buds of May,
```
