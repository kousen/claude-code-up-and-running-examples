# Claude Code: Up and Running — Examples

Companion code for the book *Claude Code: Up and Running* by Kenneth Kousen.

## How to use this repo

Clone once, then work in whichever project folder a chapter is using.
Each project (`lyrics-trainer/`, `weather-app/`, `mockhub/`) is **fully
self-contained** — its own dependencies, its own run/test commands, its
own README. There is no shared root build file. You should never need to
clone a second repository to follow along with the book.

## Related external repositories

A few of the book's examples have fuller upstream implementations or
companion projects that live in their own repositories. You don't need
them to work through the book, but they're useful for reference:

| Repo | Role |
| --- | --- |
| [kousen/certificate-service](https://github.com/kousen/certificate-service) | The "certificate service" project discussed in Ch. 1 (illustrative; not included here) |
| [kousen/lyrics_trainer](https://github.com/kousen/lyrics_trainer) | An existing, fuller implementation of the lyrics-trainer concept |
| [kousen/mockhub](https://github.com/kousen/mockhub) | The MockHub application itself — the book examples build skills/MCP/workflows *around* it |

## Layout

Examples are organized by **project**, then by **chapter phase**. The same
project evolves across multiple chapters, so each project folder contains
chapter-specific subfolders that represent its state at that point in the book.

```
lyrics-trainer/        # Browser-based vocab trainer (the "doghouse")
  ch02-first-doghouse/   Initial vibe-coded version
  ch03-local-storage/    Persistence added
  ch04-tested-modules/   Refactored toward tests

weather-app/           # Small Flask weather service (the "cabin")
  ch05-permissions/      Permissions, safety, secrets
  ch09-review-testing/   Test-first refactoring (if used here)

mockhub/               # Larger app used for skills, MCP, and PR workflows
  ch06-skills/           PR-readiness skill, sub-agents
  ch07-mcp/              MockHub as an MCP server
  ch08-prompt-to-pr/     Issue → plan → PR workflow
  ch09-review-testing/   Review, debugging, failure recovery

prompts/               # Reusable prompts referenced in the text, by chapter
transcripts/           # Captured Claude Code session transcripts, by chapter
```

This layout may evolve as chapters are finalized.
