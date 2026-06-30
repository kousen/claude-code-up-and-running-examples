# Chapter 6 — Skills and Hooks

Companion artifacts for Chapter 6. These are **source templates**, not a
ready-to-run Claude Code project. Copy files into `.claude/commands/` or
`.claude/skills/` in whatever repo you are working in.

```
examples/ch06/
  commands/          # legacy flat slash commands (before-and-after contrast)
    README.md        # migration table
    docs.md
  skills/            # skill folders (`<name>/SKILL.md`)
    README.md        # per-skill index
    docs/
    modernize-java/
    onboard/
    security-review/
    image-prompt/
    osquery/
```

MockHub-specific skills and reviewer agents live separately under
`mockhub/ch06-skills/` because they belong to the skyscraper application
workflow, not this generic teaching set.

## Quick start

```bash
# Legacy command (flat file)
cp examples/ch06/commands/docs.md .claude/commands/

# Migrated skill (folder + frontmatter)
cp -R examples/ch06/skills/docs .claude/skills/

# A featured demo skill from the chapter
cp -R examples/ch06/skills/image-prompt ~/.claude/skills/
```

See `commands/README.md` for the command-to-skill migration table and
`skills/README.md` for what each skill is meant to teach.
