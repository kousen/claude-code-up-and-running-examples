import { describe, it, expect } from "vitest";
import { createLineTrainer, normalizeIndex } from "../src/lineTrainer.js";
import { lines } from "../src/texts.js";

const LENGTH = lines.length;

describe("normalizeIndex", () => {
  it("keeps a valid in-range integer", () => {
    expect(normalizeIndex(0, LENGTH)).toBe(0);
    expect(normalizeIndex(3, LENGTH)).toBe(3);
    expect(normalizeIndex(LENGTH - 1, LENGTH)).toBe(LENGTH - 1);
  });

  it("coerces a numeric string", () => {
    expect(normalizeIndex("5", LENGTH)).toBe(5);
  });

  it("falls back to 0 for non-numeric, non-integer, or out-of-range values", () => {
    expect(normalizeIndex("abc", LENGTH)).toBe(0);
    expect(normalizeIndex("3.5", LENGTH)).toBe(0);
    expect(normalizeIndex(-1, LENGTH)).toBe(0);
    expect(normalizeIndex(LENGTH, LENGTH)).toBe(0); // off the end
    expect(normalizeIndex(99, LENGTH)).toBe(0);
    expect(normalizeIndex(null, LENGTH)).toBe(0);
  });
});

describe("createLineTrainer", () => {
  it("starts on line 0 by default", () => {
    const trainer = createLineTrainer(lines);
    expect(trainer.currentIndex()).toBe(0);
    expect(trainer.currentLine()).toBe(lines[0]);
  });

  it("resumes from a valid initial index", () => {
    const trainer = createLineTrainer(lines, 4);
    expect(trainer.currentIndex()).toBe(4);
    expect(trainer.currentLine()).toBe(lines[4]);
  });

  it("normalizes an invalid initial index to 0", () => {
    expect(createLineTrainer(lines, 99).currentIndex()).toBe(0);
    expect(createLineTrainer(lines, "nope").currentIndex()).toBe(0);
  });

  it("advances to the next line and returns it", () => {
    const trainer = createLineTrainer(lines);
    expect(trainer.next()).toBe(lines[1]);
    expect(trainer.currentIndex()).toBe(1);
    expect(trainer.next()).toBe(lines[2]);
    expect(trainer.currentIndex()).toBe(2);
  });

  it("wraps from the last line back to the first", () => {
    const trainer = createLineTrainer(lines, LENGTH - 1);
    expect(trainer.next()).toBe(lines[0]);
    expect(trainer.currentIndex()).toBe(0);
  });

  it("moves to the previous line and returns it", () => {
    const trainer = createLineTrainer(lines, 3);
    expect(trainer.previous()).toBe(lines[2]);
    expect(trainer.currentIndex()).toBe(2);
  });

  it("wraps from the first line back to the last", () => {
    const trainer = createLineTrainer(lines);
    expect(trainer.previous()).toBe(lines[LENGTH - 1]);
    expect(trainer.currentIndex()).toBe(LENGTH - 1);
  });
});
