# Chapter 2 lyrics-trainer first run

Date captured: 2026-05-18

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples/lyrics-trainer/ch02-first-doghouse
```

Prompt:

```text
I want a single-page web app that helps me practice memorizing a text one line at a time.

Use Shakespeare's Sonnet 18, starting with "Shall I compare thee to a summer's day?"
Show one line at a time, with a Next button that advances to the next line. When it reaches the end, loop back to the first line.

Build the first version as plain HTML, CSS, and JavaScript. No framework, no build step, no dependencies. If one index.html file is enough, use one file.

Keep the app simple but pleasant enough to open in a browser and use immediately.
```

Output:

```text
Done. Open `index.html` in any browser — it shows one line of Sonnet 18 at a time with a line counter, and Next wraps from line 14 back to line 1.

★ Insight ─────────────────────────────────────
- The `min-height: 4.5rem` on `.line` reserves space for two-line wrapping on narrow screens, so the button doesn't jump up and down as you click through — small detail, but it prevents a jarring layout shift.
- `color-scheme: light dark` is a one-liner that tells the browser to render form controls (like the button's focus ring) appropriately for the user's OS theme, even though the page itself uses fixed colors.
- Line 12 has a textual variant worth knowing: the Quarto reads *"When in eternal lines to time thou grow'st"* — I used the standard Quarto reading. If you have a preferred edition (some print "shades" here), it's a one-line edit in the `lines` array.
─────────────────────────────────────────────────

**One spot where your judgment would shape the feature** (optional, ~5 lines): right now Next just shows the next line — pure passive reading. For a *memorization* trainer, a common pattern is to hide the line and require you to recite it from memory before revealing. If you'd like that, the meaningful choice is *how* the reveal works:

- **Click-to-reveal:** show only the line number, click "Show" to reveal, then "Next"
- **Type-to-check:** input box, compare what you typed against the line, show diff
- **Progressive blur:** line is blurred/faded, hover or click to sharpen

Each shapes the trainer's character. Want to add one of these, or leave it as plain reading for now?
```

Manuscript-use notes:

- Use the `Done` line to replace the placeholder "Claude Code should..." prose.
- Use the `min-height` note as the most relevant "Claude explains a small UI decision" example.
- Save the `color-scheme` note for possible later UI polish discussion.
- Do not use the Shakespeare textual-variant aside in Chapter 2 unless the chapter needs a short note about public-domain source choices.
- Treat the reveal-mode suggestions as the first opportunity to demonstrate human direction: leave the feature out for now because Chapter 2 should remain a tiny doghouse.

## Follow-up summary response

Prompt:

```text
Leave it as plain reading for now. This first version is meant to stay intentionally simple.

Please give me:
1. the file or files you created,
2. the command or action to open it,
3. a very short summary of how the code works,
4. any assumptions worth noting for the book transcript.
```

Ken note:

```text
Normally Claude Code asks me to start a server here (like `python3 ...` to run a local server) rather than simply asking me to double-click on a file.
```

Response:

````text
## 1. Files created

- `index.html` — single file, ~95 lines, contains HTML, CSS, and JavaScript inline.

## 2. How to open it

```
open index.html
```

(Or double-click the file in Finder. No server, no build step.)

## 3. How the code works

- **Data:** the 14 lines of Sonnet 18 are stored as a JavaScript array of strings.
- **State:** a single `currentIndex` variable tracks which line is showing.
- **Render:** a `render()` function writes `lines[currentIndex]` into the page and updates the "Line X of 14" counter.
- **Advance:** the Next button's click handler does `currentIndex = (currentIndex + 1) % lines.length` and re-renders — the modulo handles wrap-around from line 14 back to line 1.
- **Styling:** a centered card on a warm parchment background, serif font (Georgia) for the verse, sans-serif treatment for the chrome (counter, button).

## 4. Assumptions worth noting for the book transcript

- **Text edition:** used the standard Quarto reading throughout, including line 12 *"When in eternal lines to time thou grow'st"* (some editions print "shades").
- **No persistence:** refreshing the page resets to line 1. No `localStorage`, no URL state.
- **No keyboard shortcut:** Next is click-only (Space/Enter work because the button has focus after the first click, but that's browser default behavior, not explicit code).
- **No Previous button, no progress bar beyond the counter** — kept deliberately minimal per the "first doghouse" framing.
- **`color-scheme: light dark`** is set so the button's focus ring renders correctly in either OS theme, but the page itself uses fixed light colors — it does *not* adapt to dark mode.
- **Accessibility basics only:** semantic `<button>`, visible focus outline, sufficient contrast. No ARIA live region announcing line changes to screen readers.
````

Manuscript-use notes:

- The raw response said `open index.html`; in the Chapter 2 transcript, use `! open index.html` because the action happens inside a Claude Code session. Add a caveat that this works because the first version has no modules, fetches, framework tooling, or server-sensitive behavior.
- The "No persistence" assumption tees up Chapter 3's localStorage feature.
- The accessibility note is useful later if Chapter 3 or Chapter 4 wants a "what did we leave out?" prompt.

## Browser-open command

Prompt/action inside Claude Code:

```text
! open index.html
```

Response:

```text
(Bash completed with no output)
```

Manuscript-use note:

- This is the normal quiet success path for macOS `open`; the visible result is the browser window/tab, not terminal output.
