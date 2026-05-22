// Wires the pure core to the DOM and to localStorage. This is the only file
// that touches the browser; the state and the math live in the other modules.
import { lines } from "./texts.js";
import { createLineTrainer } from "./lineTrainer.js";
import { loadSavedIndex, saveIndex } from "./storage.js";

const trainer = createLineTrainer(lines, loadSavedIndex(localStorage, lines.length));

const lineEl = document.getElementById("line");
const counterEl = document.getElementById("counter");
const nextBtn = document.getElementById("next");
const previousBtn = document.getElementById("previous");

function render() {
  lineEl.textContent = trainer.currentLine();
  counterEl.textContent =
    `Line ${trainer.currentIndex() + 1} of ${lines.length}`;
}

nextBtn.addEventListener("click", () => {
  trainer.next();
  saveIndex(localStorage, trainer.currentIndex());
  render();
});

previousBtn.addEventListener("click", () => {
  trainer.previous();
  saveIndex(localStorage, trainer.currentIndex());
  render();
});

document.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight") {
    trainer.next();
    saveIndex(localStorage, trainer.currentIndex());
    render();
  }
});

render();
