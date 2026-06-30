# Legacy custom slash commands (kept for contrast)

This folder holds the **old** flat-command form from `.claude/commands/`.
Chapter 6 of the book keeps one entry here (`docs.md`) on purpose so you can
compare it to the skill version in `../skills/docs/`.

The other commands from the original training set were migrated to skills:

| Old (`.claude/commands/`) | New (`../skills/<name>/SKILL.md`) |
| --- | --- |
| `modernize-java.md` | `skills/modernize-java/` |
| `onboard.md` | `skills/onboard/` |
| `security-review.md` | `skills/security-review/` |

Skill versions can do things flat command files cannot: frontmatter for `paths`
triggering, `allowed-tools` scoping, `context: fork` execution,
`disable-model-invocation` for explicit-only skills, and `$ARGUMENTS`
substitution.

If a command and a skill share a name, the skill wins.

## Install the legacy command

```bash
mkdir -p .claude/commands
cp examples/ch06/commands/docs.md .claude/commands/
```

Then invoke `/docs` in a Claude Code session.
