# force-push-guard (Chapter 6 sidebar: Mods)

A minimal Claude Code mod. It registers one `tool.call` hook, limited to Bash,
that refuses any `git push` with `--force` or `-f` before the command runs.

Validated 2026-10-02 on Claude Code 2.1.287 (mods shipped in that release):

```
$ claude plugin validate ./force-push-guard
  ❯ ./register.js hooks: tool.call{tool=Bash}
  ❯ ./register.js calls: nothing on $
✔ Validation passed
```

Try it for one session without installing:

```
claude --plugin-dir ./force-push-guard
```

Docs: https://code.claude.com/docs/en/plugins/mods/overview
