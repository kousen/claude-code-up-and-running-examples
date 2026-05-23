# Chapter 6 MockHub Artifacts

Chapter 6 uses MockHub to teach skills, sub-agents, and agent teams. The
MockHub application code lives in its own repository:

<https://github.com/kousen/mockhub>

The book will eventually reference a specific MockHub tag or commit when the
text is frozen. Until then, clone the MockHub repository separately and treat
these files as the agent-facing artifacts you can copy into that working tree.

## Layout

```text
.claude/
  skills/
    mockhub-pr-readiness/
      SKILL.md
  agents/
    mockhub-test-reviewer.md
    mockhub-security-reviewer.md
    mockhub-docs-reviewer.md
```

The skill is a repeatable workflow. The agents are separate review lenses. The
chapter's main point is that these are different boundaries, not a ladder.
