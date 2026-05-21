# Chapter 3 lyrics-trainer local-persistence prompt

Used for the `lyrics-trainer/ch03-local-persistence` capture. Continues the
Chapter 2 single-file app by adding `localStorage` persistence.

```text
Add local persistence to the lyrics-trainer. When the user advances to a new line, save the current line index to localStorage. When the page loads, check localStorage and resume from the saved position if one exists. If the saved position is out of range for the current text, fall back to line 0.

Success condition: reload the page after advancing a few lines and the app resumes at the same line. Corrupt or out-of-range stored values fall back safely to the first line.

Keep the current single-file structure. Add the storage logic where it naturally fits, but don't extract modules or introduce a build step.

Before you start, do you have any questions for me? Is there anything I'm missing? Are there any other options I've neglected?
```
