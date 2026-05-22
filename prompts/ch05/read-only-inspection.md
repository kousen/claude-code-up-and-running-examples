# Chapter 5 read-only inspection prompt

The escalation-ladder boundary prompt. Run it against a project to make Claude
Code classify the work before doing it. In Ch5 it is used twice -- once on the
lyrics-trainer (small trust surface) and once on the weather app (wider trust
surface) -- to produce the two inspection summaries in the chapter.

```text
Start by inspecting the project read-only. Tell me:

- what you need to read
- what you expect to change
- which commands you expect to run
- whether any step needs network access, credentials, git publication, or external services

Do not edit files or run write-capable commands until I approve the plan.
```
