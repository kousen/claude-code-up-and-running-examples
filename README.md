# Claude Code: Up and Running — Examples

Companion code for the book *Claude Code: Up and Running* by Kenneth Kousen.

## How to use this repo

Clone once, then work in whichever project folder a chapter is using. The
`lyrics-trainer/` and `weather-app/` projects are fully self-contained: their
own dependencies, their own run/test commands, their own README files. MockHub
is the exception. The MockHub application code lives in its own GitHub
repository; this repo holds the book's surrounding skills, agents, prompts,
transcripts, and workflow artifacts.

## Related external repositories

A few of the book's examples have fuller upstream implementations or companion
projects that live in their own repositories. You do need the MockHub repository
for the skyscraper-scale application work in the later chapters (roughly Ch. 6-11,
except for the Ch. 8 codebase-exploration example, which uses a public framework
repository instead); the other external repos are useful references:

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
lyrics-trainer/          # Browser-based memorization trainer (the "doghouse")
  ch02-first-doghouse/     Initial vibe-coded single file
  ch03-local-persistence/  localStorage persistence added
  ch04-testable-core/      Refactored into tested modules
  ch05-navigation/         Branch-first navigation change + Playwright matrix

weather-app/             # Small Flask weather service (the "cabin")
  ch05-permissions/        Permissions, safety, secrets

mockhub/                 # Larger app: skills, sub-agents, MCP, and PR workflows
  ch06-skills/             PR-readiness skill plus the reviewer sub-agents

prompts/                 # Reusable prompts referenced in the text, by chapter
transcripts/             # Captured Claude Code session transcripts, by chapter
```

The `prompts/` and `transcripts/` folders are numbered to match the book's
chapters, so they skip any chapter that has no captured artifact (Chapter 6's
skills work lives under `mockhub/`, and Chapter 8 uses a public framework
repository rather than a captured session). The current chapter map for the
later, MockHub-centered chapters is: Chapter 7 (sub-agents and agent teams),
Chapter 9 (MCP), Chapter 10 (prompt to pull request), and Chapter 11 (review,
testing, debugging, and recovery).

This layout may evolve as chapters are finalized.
