# lyrics-trainer

A small browser-based vocabulary/lyrics trainer — the "doghouse" project
used to introduce Claude Code in the early chapters.

## Chapter phases

| Folder | Chapter | State |
| --- | --- | --- |
| `ch02-first-doghouse/` | Ch. 2 — Getting Started | Initial vibe-coded version |
| `ch03-local-storage/` | Ch. 3 — Talking to Claude Code | Local persistence added |
| `ch04-tested-modules/` | Ch. 4 — When Vibe Coding Isn't Enough | Refactored toward a testable core |

It also makes a brief return in Ch. 5 to introduce the branch-first habit
before the book moves on to the Flask weather app.

## Stack

JavaScript, HTML, and CSS for the app itself. Tests may be written in
TypeScript (Vitest or Jest).

## Upstream reference

A fuller implementation of the lyrics-trainer concept lives at
<https://github.com/kousen/lyrics_trainer>. The versions in this folder are the
book-shaped snapshots used to teach specific Claude Code workflows — they
are deliberately smaller and may diverge from the upstream.

