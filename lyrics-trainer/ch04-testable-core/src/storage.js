// Reading and writing the resume position. Functions take a Storage-like
// object (anything with getItem/setItem) so the browser passes localStorage
// while tests pass a lightweight fake — no jsdom required.
import { normalizeIndex } from "./lineTrainer.js";

export const DEFAULT_KEY = "lyricsTrainer.lineIndex";

// Decide which line to resume on, reusing the core's validation rather than
// duplicating it: any invalid or absent saved value falls back to line 0.
export function loadSavedIndex(storage, lineCount, key = DEFAULT_KEY) {
  return normalizeIndex(storage.getItem(key), lineCount);
}

// Persist the current position.
export function saveIndex(storage, index, key = DEFAULT_KEY) {
  storage.setItem(key, String(index));
}
