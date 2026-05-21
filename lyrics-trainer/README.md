# lyrics-trainer

A small browser-based vocabulary/lyrics trainer — the "doghouse" project
used to introduce Claude Code in the early chapters.

## Chapter phases

| Folder | Chapter | State |
| --- | --- | --- |
| `ch02-first-doghouse/` | Ch. 2 — Getting Started | Initial vibe-coded version |
| `ch03-local-persistence/` | Ch. 3 — Talking to Claude Code | Local persistence added |
| `ch04-testable-core/` | Ch. 4 — When Vibe Coding Isn't Enough | Refactored toward a testable core |

It also makes a brief return in Ch. 5 to introduce the branch-first habit
before the book moves on to the Flask weather app.

## Stack

JavaScript, HTML, and CSS for the app itself. Chapter 4 uses native JavaScript
modules and Vitest, so run it through the local server script in that folder
rather than opening `index.html` directly from disk.

## Upstream reference

A fuller implementation of the lyrics-trainer concept lives at
<https://github.com/kousen/lyrics_trainer>. The versions in this folder are the
book-shaped snapshots used to teach specific Claude Code workflows — they
are deliberately smaller and may diverge from the upstream.
