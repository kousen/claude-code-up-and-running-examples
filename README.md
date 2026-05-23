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
for the Ch. 6-9 skyscraper-scale application work; the other external repos are
useful references:

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
  ch05-navigation/       Branch-first navigation change + Playwright matrix

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
