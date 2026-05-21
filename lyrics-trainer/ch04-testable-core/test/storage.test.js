import { describe, it, expect } from "vitest";
import { DEFAULT_KEY, loadSavedIndex, saveIndex } from "../src/storage.js";
import { lines } from "../src/texts.js";

const LENGTH = lines.length;

// A minimal stand-in for localStorage backed by a plain object, so we can both
// seed reads and inspect writes.
function fakeStorage(initial = {}) {
  const store = { ...initial };
  return {
    getItem: (key) => (key in store ? store[key] : null),
    setItem: (key, value) => {
      store[key] = String(value);
    },
    store
  };
}

describe("loadSavedIndex", () => {
  it("resumes from a valid saved index", () => {
    expect(loadSavedIndex(fakeStorage({ [DEFAULT_KEY]: "3" }), LENGTH)).toBe(3);
    expect(loadSavedIndex(fakeStorage({ [DEFAULT_KEY]: "0" }), LENGTH)).toBe(0);
  });

  it("falls back to line 0 for invalid or out-of-range values", () => {
    expect(loadSavedIndex(fakeStorage({ [DEFAULT_KEY]: "abc" }), LENGTH)).toBe(0);
    expect(loadSavedIndex(fakeStorage({ [DEFAULT_KEY]: String(LENGTH) }), LENGTH)).toBe(0);
    expect(loadSavedIndex(fakeStorage({ [DEFAULT_KEY]: "-1" }), LENGTH)).toBe(0);
  });

  it("falls back to line 0 when nothing was saved", () => {
    expect(loadSavedIndex(fakeStorage(), LENGTH)).toBe(0);
  });

  it("reads from a custom key when given one", () => {
    const storage = fakeStorage({ "custom.key": "2" });
    expect(loadSavedIndex(storage, LENGTH, "custom.key")).toBe(2);
  });
});

describe("saveIndex", () => {
  it("writes the index under the default key", () => {
    const storage = fakeStorage();
    saveIndex(storage, 7);
    expect(storage.store[DEFAULT_KEY]).toBe("7");
  });

  it("writes under a custom key when given one", () => {
    const storage = fakeStorage();
    saveIndex(storage, 5, "custom.key");
    expect(storage.store["custom.key"]).toBe("5");
  });

  it("round-trips with loadSavedIndex", () => {
    const storage = fakeStorage();
    saveIndex(storage, 6);
    expect(loadSavedIndex(storage, LENGTH)).toBe(6);
  });
});
