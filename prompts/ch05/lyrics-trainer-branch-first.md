# Chapter 5 lyrics-trainer branch-first prompt

The branch-first / permission-discipline demo (ch05 ~lines 363-373). The
checked-in end state lives at `lyrics-trainer/ch05-navigation`; for a fresh
capture, seed a throwaway copy from `lyrics-trainer/ch04-testable-core` first.
The point is the ritual -- inspect git status, branch, do not push -- not the
feature. The feature was swapped from a "progress label" (the app already shows
"Line N of M") to genuinely new behavior: keyboard support plus a Previous
button.

Capture note: the Previous button adds a *second* save site, which is the exact
trigger the Chapter 3 saveState sidebar named ("extract `saveState()` when a
second place needs to save"). Watch whether the run extracts it -- if so, that's
a real cross-chapter callback worth highlighting.

Branching wrinkle: the examples repo is one git repo, so `create a branch` would
branch the whole repo. For a faithful capture, run this where branching the
lyrics-trainer in isolation makes sense (a throwaway git repo seeded from
`ch05-navigation`), or capture the interaction aware that the repo model differs
from the book's "this app is its own repo" framing.

```text
Before editing, inspect the git status. If the working tree is not clean, stop and tell me what is already changed.

If it is clean, create a branch named feature/navigation. Then add keyboard support to the lyrics-trainer -- the right arrow key advances to the next line -- and a Previous button that goes back one line. Keep the existing tests passing and add or update tests for the new behavior.

Do not push the branch.
```
