// Line-navigation core. No DOM, no storage — just the index state and the math
// around it, so the whole thing can be constructed and driven from tests.

// Coerce an arbitrary stored/initial value into a usable index. A valid value
// (an integer in [0, length)) is returned as-is; anything else — non-numeric,
// non-integer, negative, off the end, or absent — falls back to 0.
export function normalizeIndex(value, length) {
  const n = Number(value);
  if (!Number.isInteger(n) || n < 0 || n >= length) {
    return 0;
  }
  return n;
}

// A small stateful trainer over `lines`. Holds the current index internally and
// exposes just enough to render and move through the lines.
export function createLineTrainer(lines, initialIndex = 0) {
  let index = normalizeIndex(initialIndex, lines.length);

  return {
    currentLine() {
      return lines[index];
    },
    currentIndex() {
      return index;
    },
    // Advance to the next line, wrapping back to the first after the last one,
    // and return the line now showing.
    next() {
      index = (index + 1) % lines.length;
      return lines[index];
    },
    // Move to the previous line, wrapping from the first line to the last one.
    previous() {
      index = (index - 1 + lines.length) % lines.length;
      return lines[index];
    }
  };
}
