# Chapter 6 — Standalone skills

Personal skills demonstrated in Chapter 6 ("Skills and Hooks") that are not tied
to any of the book's major projects.

| Skill | What it shows |
| --- | --- |
| `image-prompt/` | A structured-interview skill: instead of one-shotting an image prompt, it asks only the gaps that matter (subject, mood, text, aspect ratio, use case), then emits a finished prompt plus the reasoning behind each choice. The reusable part is the interview and the structure, not any single prompt. |

## Installing a skill

A skill is just a folder with a `SKILL.md` inside it. To use `image-prompt`
yourself, copy the folder into your skills directory:

```bash
# user-level (available in every project)
cp -R image-prompt ~/.claude/skills/

# or project-level (checked in with a repo)
cp -R image-prompt .claude/skills/
```

Then invoke it in a Claude Code session with `/image-prompt <your rough idea>`.
