# Chapter 6 skills

Skill folders for Chapter 6 ("Skills and Hooks"). Copy into your project or
install personally under `~/.claude/skills/`.

The Java-oriented examples (`modernize-java`, `onboard`, `security-review`)
illustrate different frontmatter capabilities. The pattern transfers to any
stack.

| Skill | What it demonstrates |
| --- | --- |
| `docs/` | Minimal migration from a flat custom command (pairs with `../commands/docs.md`) |
| `modernize-java/` | `paths` triggering on `*.java`, `effort: medium` |
| `onboard/` | `context: fork` (clean parent context), `model: opus` |
| `security-review/` | `allowed-tools` (read-only), `disable-model-invocation` |
| `image-prompt/` | Structured-interview dialog for image-generation prompts |
| `osquery/` | Natural-language wrapper around a local CLI (`osqueryi --json`) with a `queries.md` reference file |
| `here-now/` | Remote REST publish workflow (`publish.sh`); syntax in the API docs, semantics in the skill. Upstream: `heredotnow/skill` on GitHub; book snapshot may lag the live skill. |

## Install

```bash
# One skill
cp -R examples/ch06/skills/docs .claude/skills/

# Or all chapter skills
mkdir -p .claude/skills
cp -R examples/ch06/skills/* .claude/skills/
```

Skills hot-reload in the current session when you edit a `SKILL.md`.
